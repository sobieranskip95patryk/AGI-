"""
MIGI_7G Function Calling Integration
Integruje system wywoływania funkcji z głównym systemem MIGI_7G
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from FUNCTION_CALLING.engine import function_calling_engine, ToolCall, ToolResult

logger = logging.getLogger(__name__)

class MIGIFunctionCallingIntegration:
    """Integracja Function Calling z systemem MIGI_7G"""
    
    def __init__(self, migi_system=None):
        self.migi_system = migi_system
        self.engine = function_calling_engine
        self.conversation_history = []
        
    async def process_message_with_tools(
        self, 
        message: str, 
        available_tools: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Przetwarza wiadomość z możliwością wywoływania narzędzi
        
        Args:
            message: Wiadomość użytkownika
            available_tools: Lista dostępnych narzędzi (None = wszystkie)
        
        Returns:
            Słownik z odpowiedzią i wywołanymi narzędziami
        """
        
        # Dodaj wiadomość do historii
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Przygotuj definicje narzędzi
        tool_definitions = self.engine.get_tool_definitions()
        
        # Filtruj narzędzia jeśli określono
        if available_tools:
            tool_definitions = [
                tool for tool in tool_definitions 
                if tool["name"] in available_tools
            ]
        
        logger.info(f"🔧 Available tools: {[t['name'] for t in tool_definitions]}")
        
        # Tutaj normalnie byłoby wywołanie do LLM (Grok, GPT, etc.)
        # Na razie symulujemy odpowiedź z wywołaniami narzędzi
        simulated_response = await self._simulate_llm_response_with_tools(
            message, tool_definitions
        )
        
        # Dodaj odpowiedź asystenta do historii
        self.conversation_history.append(simulated_response)
        
        # Wykonaj wywołania narzędzi jeśli są
        tool_results = []
        if "tool_calls" in simulated_response:
            tool_calls = [
                ToolCall(
                    id=call["id"],
                    name=call["function"]["name"], 
                    arguments=json.loads(call["function"]["arguments"])
                )
                for call in simulated_response["tool_calls"]
            ]
            
            tool_results = await self.engine.execute_tool_calls(tool_calls)
            
            # Dodaj wyniki narzędzi do historii
            for result in tool_results:
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": result.tool_call_id,
                    "content": json.dumps(result.content) if result.success else result.error
                })
        
        return {
            "response": simulated_response,
            "tool_results": tool_results,
            "conversation_history": self.conversation_history
        }
    
    async def _simulate_llm_response_with_tools(
        self, 
        message: str, 
        tool_definitions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Symuluje odpowiedź LLM z wywołaniami narzędzi
        W prawdziwej implementacji tutaj byłoby wywołanie do API
        """
        
        # Prosta logika wykrywania potrzeb narzędzi
        tool_calls = []
        response_content = ""
        
        # Wykryj potrzebę informacji o systemie
        if any(keyword in message.lower() for keyword in ["system", "memory", "cpu", "info"]):
            tool_calls.append({
                "id": f"call_{len(tool_calls)}_system",
                "type": "function",
                "function": {
                    "name": "get_system_info",
                    "arguments": json.dumps({
                        "include_memory": True,
                        "include_cpu": True
                    })
                }
            })
        
        # Wykryj potrzebę obliczeń
        if any(keyword in message.lower() for keyword in ["calculate", "math", "compute", "+", "-", "*", "/"]):
            # Wyciągnij wyrażenie matematyczne (bardzo proste)
            import re
            math_pattern = r'[\d+\-*/().\s]+'
            matches = re.findall(math_pattern, message)
            if matches:
                expression = matches[0].strip()
                tool_calls.append({
                    "id": f"call_{len(tool_calls)}_calc",
                    "type": "function", 
                    "function": {
                        "name": "calculate",
                        "arguments": json.dumps({
                            "expression": expression,
                            "precision": 2
                        })
                    }
                })
        
        # Wykryj potrzebę czasu
        if any(keyword in message.lower() for keyword in ["time", "date", "when", "clock"]):
            tool_calls.append({
                "id": f"call_{len(tool_calls)}_time",
                "type": "function",
                "function": {
                    "name": "get_current_time", 
                    "arguments": json.dumps({
                        "format": "%Y-%m-%d %H:%M:%S",
                        "timezone": None
                    })
                }
            })
        
        if tool_calls:
            response_content = f"Pozwól mi sprawdzić to dla Ciebie używając dostępnych narzędzi..."
            return {
                "role": "assistant",
                "content": response_content,
                "tool_calls": tool_calls
            }
        else:
            response_content = f"Rozumiem Twoją wiadomość: '{message}'. Obecnie nie potrzebuję żadnych narzędzi do odpowiedzi."
            return {
                "role": "assistant", 
                "content": response_content
            }
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Zwraca listę dostępnych narzędzi"""
        return self.engine.get_tool_definitions()
    
    def register_custom_tool(
        self,
        name: str,
        function: callable,
        description: str,
        parameters_schema: Optional[Dict[str, Any]] = None
    ):
        """Rejestruje niestandardowe narzędzie"""
        self.engine.register_tool(
            name=name,
            function=function,
            description=description,
            parameters_schema=parameters_schema
        )
        logger.info(f"✅ Registered custom tool: {name}")
    
    def clear_conversation_history(self):
        """Czyści historię konwersacji"""
        self.conversation_history = []
        logger.info("🧹 Conversation history cleared")

# Przykładowe narzędzia specyficzne dla MIGI_7G

from FUNCTION_CALLING.engine import tool
from pydantic import BaseModel, Field

class MIGIStatusRequest(BaseModel):
    """Request model for MIGI system status"""
    include_modules: bool = Field(default=True, description="Include module status")
    include_archetypes: bool = Field(default=True, description="Include archetype status")
    include_metrics: bool = Field(default=False, description="Include detailed metrics")

@tool(name="get_migi_status", description="Get MIGI_7G system status", pydantic_model=MIGIStatusRequest)
def get_migi_status(request: MIGIStatusRequest) -> Dict[str, Any]:
    """Pobiera status systemu MIGI_7G"""
    import time
    
    status = {
        "system": "MIGI_7G",
        "status": "operational",
        "timestamp": time.time(),
        "uptime": "unknown"  # Tutaj byłaby prawdziwa logika
    }
    
    if request.include_modules:
        status["modules"] = {
            "NSF": {"status": "active", "load": 0.7},
            "Logic_Engine": {"status": "active", "load": 0.5},
            "Temporal": {"status": "active", "load": 0.3},
            "Perception": {"status": "active", "load": 0.8},
            "Bayes": {"status": "active", "load": 0.4}
        }
    
    if request.include_archetypes:
        status["archetypes"] = {
            "current": "Sage",
            "stability": 0.85,
            "transitions_today": 12,
            "available": ["Hunter", "Sage", "Lover", "Creator", "Explorer"]
        }
    
    if request.include_metrics:
        status["metrics"] = {
            "empathy_score": 0.78,
            "coherence": 0.92,
            "stress_level": 0.15,
            "risk_radar": {
                "masking": 0.12,
                "rigidity": 0.08,
                "monoculture": 0.05
            }
        }
    
    return status

class ArchetypeTransitionRequest(BaseModel):
    """Request model for archetype transition"""
    target_archetype: str = Field(description="Target archetype name")
    force_transition: bool = Field(default=False, description="Force immediate transition")
    duration: Optional[int] = Field(default=None, description="Transition duration in seconds")

@tool(name="trigger_archetype_transition", description="Trigger archetype transition in MIGI_7G", pydantic_model=ArchetypeTransitionRequest)
def trigger_archetype_transition(request: ArchetypeTransitionRequest) -> Dict[str, Any]:
    """Wyzwala przejście archetypowe w systemie MIGI_7G"""
    import time
    
    valid_archetypes = ["Hunter", "Sage", "Lover", "Creator", "Explorer"]
    
    if request.target_archetype not in valid_archetypes:
        return {
            "success": False,
            "error": f"Invalid archetype. Valid options: {valid_archetypes}",
            "current_archetype": "Sage"
        }
    
    # Symulacja przejścia archetypowego
    transition_time = request.duration or 5
    
    return {
        "success": True,
        "transition": {
            "from": "Sage",
            "to": request.target_archetype,
            "forced": request.force_transition,
            "estimated_duration": transition_time,
            "started_at": time.time()
        },
        "message": f"Archetype transition to {request.target_archetype} initiated"
    }

class TelemetryRequest(BaseModel):
    """Request model for telemetry data"""
    modules: Optional[List[str]] = Field(default=None, description="Specific modules to get data for")
    time_range: int = Field(default=60, description="Time range in seconds")
    include_raw: bool = Field(default=False, description="Include raw telemetry data")

@tool(name="get_telemetry_data", description="Get MIGI_7G telemetry data", pydantic_model=TelemetryRequest)
def get_telemetry_data(request: TelemetryRequest) -> Dict[str, Any]:
    """Pobiera dane telemetryczne z systemu MIGI_7G"""
    import time
    import random
    
    modules = request.modules or ["NSF", "Logic_Engine", "Temporal", "Perception", "Bayes"]
    
    telemetry = {
        "timestamp": time.time(),
        "time_range": request.time_range,
        "modules": {}
    }
    
    for module in modules:
        telemetry["modules"][module] = {
            "status": "active",
            "load": random.uniform(0.1, 0.9),
            "memory_usage": random.uniform(100, 500),  # MB
            "operations_per_second": random.randint(50, 200),
            "last_activity": time.time() - random.randint(1, 30)
        }
    
    if request.include_raw:
        telemetry["raw_data"] = {
            "brain_layers": [random.uniform(0, 1) for _ in range(20)],
            "stress_metrics": [random.uniform(0, 0.5) for _ in range(10)],
            "archetype_weights": {
                arch: random.uniform(0, 1) 
                for arch in ["Hunter", "Sage", "Lover", "Creator", "Explorer"]
            }
        }
    
    return telemetry

# Globalna instancja integracji
migi_function_calling = MIGIFunctionCallingIntegration()

__all__ = [
    'MIGIFunctionCallingIntegration', 
    'migi_function_calling'
]