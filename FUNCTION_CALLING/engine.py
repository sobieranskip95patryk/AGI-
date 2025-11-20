"""
MIGI_7G Function Calling System
Implementuje wywoływanie funkcji zewnętrznych dla systemu MIGI_7G

Funkcjonalności:
- Integracja z zewnętrznymi API
- Wywoływanie narzędzi lokalnych
- Obsługa równoległych wywołań
- Automatyczne mapowanie funkcji
- Walidacja argumentów z Pydantic
"""

import asyncio

import logging
import inspect
from typing import Dict, List, Any, Callable, Optional, Union, Type
from dataclasses import dataclass
from pydantic import BaseModel, Field, ValidationError

import time

# Import Structured Outputs system
try:
    from .structured_outputs import (
        StructuredOutputEngine, 
        StructuredOutputConfig,

        create_structured_tool
    )
    STRUCTURED_OUTPUTS_AVAILABLE = True
except ImportError:
    STRUCTURED_OUTPUTS_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class ToolCall:
    """Reprezentuje wywołanie narzędzia"""
    id: str
    name: str
    arguments: Dict[str, Any]
    
@dataclass
class ToolResult:
    """Reprezentuje wynik wywołania narzędzia"""
    tool_call_id: str
    content: Any
    success: bool
    error: Optional[str] = None
    execution_time: Optional[float] = None

class ToolDefinition:
    """Definicja narzędzia dla MIGI_7G"""
    
    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters_schema: Optional[Dict[str, Any]] = None,
        pydantic_model: Optional[Type[BaseModel]] = None
    ):
        self.name = name
        self.description = description
        self.function = function
        self.parameters_schema = parameters_schema
        self.pydantic_model = pydantic_model
        
        # Auto-generate schema from Pydantic model if provided
        if pydantic_model and not parameters_schema:
            self.parameters_schema = pydantic_model.model_json_schema()
    
    def to_dict(self) -> Dict[str, Any]:
        """Konwertuje definicję narzędzia na słownik dla API"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters_schema or self._generate_schema_from_function()
        }
    
    def _generate_schema_from_function(self) -> Dict[str, Any]:
        """Automatycznie generuje schema z sygnatury funkcji"""
        sig = inspect.signature(self.function)
        properties = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
                
            param_schema = {"type": "string"}  # Default type
            
            # Try to infer type from annotation
            if param.annotation != inspect.Parameter.empty:
                if param.annotation is int:
                    param_schema["type"] = "integer"
                elif param.annotation is float:
                    param_schema["type"] = "number"
                elif param.annotation is bool:
                    param_schema["type"] = "boolean"
                elif param.annotation is list:
                    param_schema["type"] = "array"
                elif param.annotation is dict:
                    param_schema["type"] = "object"
            
            properties[param_name] = param_schema
            
            # Add to required if no default value
            if param.default == inspect.Parameter.empty:
                required.append(param_name)
        
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

class FunctionCallingEngine:
    """Główny silnik wywoływania funkcji dla MIGI_7G"""
    
    def __init__(self, structured_outputs_config: Optional['StructuredOutputConfig'] = None):
        self.tools: Dict[str, ToolDefinition] = {}
        self.parallel_calling_enabled = True
        self.max_concurrent_calls = 5
        self.execution_timeout = 30.0
        
        # Initialize Structured Outputs if available
        if STRUCTURED_OUTPUTS_AVAILABLE:
            self.structured_engine = StructuredOutputEngine(structured_outputs_config)
            logger.info("✅ Structured Outputs engine initialized")
        else:
            self.structured_engine = None
            logger.warning("⚠️ Structured Outputs not available")
        
    def register_tool(
        self,
        name: str,
        function: Callable,
        description: str,
        parameters_schema: Optional[Dict[str, Any]] = None,
        pydantic_model: Optional[Type[BaseModel]] = None
    ) -> None:
        """Rejestruje nowe narzędzie w systemie"""
        tool_def = ToolDefinition(
            name=name,
            description=description,
            function=function,
            parameters_schema=parameters_schema,
            pydantic_model=pydantic_model
        )
        
        self.tools[name] = tool_def
        logger.info(f"📋 Registered tool: {name}")
    
    def register_tool_from_decorator(self, tool_def: ToolDefinition) -> None:
        """Rejestruje narzędzie z dekoratora"""
        self.tools[tool_def.name] = tool_def
        logger.info(f"🎯 Registered tool from decorator: {tool_def.name}")
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Zwraca definicje wszystkich narzędzi dla API"""
        return [tool.to_dict() for tool in self.tools.values()]
    
    async def execute_tool_call(self, tool_call: ToolCall) -> ToolResult:
        """Wykonuje pojedyncze wywołanie narzędzia"""
        start_time = time.time()
        
        try:
            # Sprawdź czy narzędzie istnieje
            if tool_call.name not in self.tools:
                return ToolResult(
                    tool_call_id=tool_call.id,
                    content=None,
                    success=False,
                    error=f"Tool '{tool_call.name}' not found"
                )
            
            tool_def = self.tools[tool_call.name]
            
            # Walidacja argumentów z Pydantic jeśli dostępne
            if tool_def.pydantic_model:
                try:
                    validated_args = tool_def.pydantic_model(**tool_call.arguments)
                    # Konwertuj Pydantic model na dict dla funkcji
                    if hasattr(validated_args, 'model_dump'):
                        call_args = validated_args.model_dump()
                    else:
                        call_args = validated_args.dict()
                except ValidationError as e:
                    return ToolResult(
                        tool_call_id=tool_call.id,
                        content=None,
                        success=False,
                        error=f"Argument validation failed: {str(e)}"
                    )
            else:
                call_args = tool_call.arguments
            
            # Wykonaj funkcję z timeoutem
            try:
                if asyncio.iscoroutinefunction(tool_def.function):
                    result = await asyncio.wait_for(
                        tool_def.function(**call_args),
                        timeout=self.execution_timeout
                    )
                else:
                    result = await asyncio.wait_for(
                        asyncio.get_event_loop().run_in_executor(
                            None, lambda: tool_def.function(**call_args)
                        ),
                        timeout=self.execution_timeout
                    )
                
                execution_time = time.time() - start_time
                
                return ToolResult(
                    tool_call_id=tool_call.id,
                    content=result,
                    success=True,
                    execution_time=execution_time
                )
                
            except asyncio.TimeoutError:
                return ToolResult(
                    tool_call_id=tool_call.id,
                    content=None,
                    success=False,
                    error=f"Tool execution timeout ({self.execution_timeout}s)"
                )
                
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"❌ Tool execution error for {tool_call.name}: {str(e)}")
            
            return ToolResult(
                tool_call_id=tool_call.id,
                content=None,
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    async def execute_tool_calls(self, tool_calls: List[ToolCall]) -> List[ToolResult]:
        """Wykonuje wiele wywołań narzędzi (równolegle jeśli włączone)"""
        if not tool_calls:
            return []
        
        logger.info(f"🔧 Executing {len(tool_calls)} tool calls")
        
        if self.parallel_calling_enabled and len(tool_calls) > 1:
            # Wykonanie równoległe z ograniczeniem concurrent calls
            semaphore = asyncio.Semaphore(self.max_concurrent_calls)
            
            async def bounded_execute(tool_call: ToolCall) -> ToolResult:
                async with semaphore:
                    return await self.execute_tool_call(tool_call)
            
            results = await asyncio.gather(
                *[bounded_execute(call) for call in tool_calls],
                return_exceptions=True
            )
            
            # Konwertuj exceptions na ToolResult
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append(ToolResult(
                        tool_call_id=tool_calls[i].id,
                        content=None,
                        success=False,
                        error=str(result)
                    ))
                else:
                    processed_results.append(result)
            
            return processed_results
        else:
            # Wykonanie sekwencyjne
            results = []
            for tool_call in tool_calls:
                result = await self.execute_tool_call(tool_call)
                results.append(result)
            
            return results
    
    # =========================================
    # 🧠 STRUCTURED OUTPUTS METHODS
    # =========================================
    
    def register_structured_tool(self, 
                                name: str,
                                description: str,
                                input_schema: Type[BaseModel],
                                output_schema: Type[BaseModel]):
        """Register a tool with structured input/output validation"""
        if not STRUCTURED_OUTPUTS_AVAILABLE:
            raise RuntimeError("Structured Outputs not available")
            
        def decorator(func):
            # Create structured function with validation
            structured_func = create_structured_tool(
                name, description, input_schema, output_schema
            )(func)
            
            # Register with parameters from input schema
            self.register_tool(
                name=name,
                function=structured_func,
                description=description,
                parameters_schema=input_schema.model_json_schema(),
                pydantic_model=input_schema
            )
            
            return structured_func
            
        return decorator
    
    def parse_with_schema(self, data: Union[str, dict], schema_name: str) -> Any:
        """Parse data using registered schema"""
        if not self.structured_engine:
            raise RuntimeError("Structured Outputs not available")
            
        return self.structured_engine.parse_with_schema(data, schema_name)
    
    def validate_output(self, 
                       data: Union[str, dict], 
                       schema: Type[BaseModel]) -> tuple[bool, Optional[str]]:
        """Validate output data against schema"""
        if not self.structured_engine:
            return True, None  # Skip validation if not available
            
        return self.structured_engine.validate_data(data, schema)
    
    def list_schemas(self) -> List[str]:
        """List available structured output schemas"""
        if not self.structured_engine:
            return []
            
        return self.structured_engine.list_schemas()
    
    def get_schema_info(self, schema_name: str) -> Dict[str, Any]:
        """Get information about a specific schema"""
        if not self.structured_engine:
            return {"error": "Structured Outputs not available"}
            
        return self.structured_engine.get_schema_info(schema_name)

# Globalna instancja silnika
function_calling_engine = FunctionCallingEngine()

def tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    parameters_schema: Optional[Dict[str, Any]] = None,
    pydantic_model: Optional[Type[BaseModel]] = None
):
    """
    Dekorator do rejestracji funkcji jako narzędzia MIGI_7G
    
    Przykład użycia:
    
    @tool(name="get_weather", description="Get weather for a location")
    def get_weather(location: str, unit: str = "celsius"):
        return {"location": location, "temperature": 20, "unit": unit}
    
    Lub z Pydantic:
    
    class WeatherRequest(BaseModel):
        location: str = Field(description="City name")
        unit: str = Field(default="celsius", description="Temperature unit")
    
    @tool(name="get_weather", description="Get weather", pydantic_model=WeatherRequest)
    def get_weather(request: WeatherRequest):
        return {"location": request.location, "temperature": 20}
    """
    def decorator(func: Callable) -> Callable:
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"Execute {tool_name}"
        
        tool_def = ToolDefinition(
            name=tool_name,
            description=tool_description,
            function=func,
            parameters_schema=parameters_schema,
            pydantic_model=pydantic_model
        )
        
        function_calling_engine.register_tool_from_decorator(tool_def)
        return func
    
    return decorator

# Wbudowane narzędzia dla MIGI_7G

class SystemInfoRequest(BaseModel):
    """Request model for system info"""
    include_memory: bool = Field(default=True, description="Include memory information")
    include_cpu: bool = Field(default=True, description="Include CPU information")

@tool(name="get_system_info", description="Get current system information", pydantic_model=SystemInfoRequest)
def get_system_info(request: SystemInfoRequest) -> Dict[str, Any]:
    """Pobiera informacje o systemie"""
    import psutil
    import platform
    
    info = {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "timestamp": time.time()
    }
    
    if request.include_memory:
        memory = psutil.virtual_memory()
        info["memory"] = {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent
        }
    
    if request.include_cpu:
        info["cpu"] = {
            "count": psutil.cpu_count(),
            "percent": psutil.cpu_percent(interval=1)
        }
    
    return info

class MathCalculationRequest(BaseModel):
    """Request model for math calculations"""
    expression: str = Field(description="Mathematical expression to evaluate")
    precision: int = Field(default=10, description="Decimal precision for results")

@tool(name="calculate", description="Perform mathematical calculations", pydantic_model=MathCalculationRequest)
def calculate(request: MathCalculationRequest) -> Dict[str, Any]:
    """Wykonuje obliczenia matematyczne"""
    import math
    
    try:
        # Bezpieczne środowisko dla eval
        safe_dict = {
            "__builtins__": {},
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow, "divmod": divmod,
            "math": math, "pi": math.pi, "e": math.e,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "sqrt": math.sqrt, "log": math.log, "exp": math.exp
        }
        
        result = eval(request.expression, safe_dict)
        
        if isinstance(result, float):
            result = round(result, request.precision)
        
        return {
            "expression": request.expression,
            "result": result,
            "type": type(result).__name__
        }
        
    except Exception as e:
        return {
            "expression": request.expression,
            "error": str(e),
            "result": None
        }

class TimestampRequest(BaseModel):
    """Request model for timestamp operations"""
    format: str = Field(default="%Y-%m-%d %H:%M:%S", description="Time format string")
    timezone: Optional[str] = Field(default=None, description="Timezone (e.g., 'UTC', 'US/Eastern')")

@tool(name="get_current_time", description="Get current time and date", pydantic_model=TimestampRequest)
def get_current_time(request: TimestampRequest) -> Dict[str, Any]:
    """Pobiera aktualny czas"""
    from datetime import datetime
    import pytz
    
    try:
        if request.timezone:
            tz = pytz.timezone(request.timezone)
            now = datetime.now(tz)
        else:
            now = datetime.now()
        
        return {
            "timestamp": now.timestamp(),
            "formatted": now.strftime(request.format),
            "timezone": str(now.tzinfo) if now.tzinfo else "local",
            "iso_format": now.isoformat()
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "timestamp": None
        }

# Eksportuj główne komponenty
__all__ = [
    'FunctionCallingEngine',
    'ToolDefinition', 
    'ToolCall',
    'ToolResult',
    'tool',
    'function_calling_engine'
]