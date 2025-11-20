"""
🧠 MIGI_7G Structured Outputs System
=================================

Zapewnia schemat-enforced responses dla Function Calling Engine,
umożliwiając zwracanie strukturyzowanych danych JSON z gwarancją typu.

Obsługuje:
- Pydantic schematy z pełną walidacją
- Nested objects i complex types
- Enums, dates, i custom validators
- Real-time schema validation
- Error handling i type coercion

Author: MIGI_7G Brain
Version: 1.0.0
"""

from datetime import date, datetime
from enum import Enum
from typing import List, Dict, Optional, Any, Union, Type
from pydantic import BaseModel, Field, validator, ValidationError
import json
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# =========================================
# 📊 CORE STRUCTURED OUTPUT TYPES
# =========================================

class OutputFormat(str, Enum):
    """Supported output formats for structured responses"""
    JSON = "json"
    DICT = "dict" 
    PYDANTIC = "pydantic"

class ValidationLevel(str, Enum):
    """Validation strictness levels"""
    STRICT = "strict"      # Full validation, raise on errors
    LENIENT = "lenient"    # Coerce types when possible
    DISABLED = "disabled"  # No validation

# =========================================
# 📋 COMMON SCHEMA TYPES
# =========================================

class Currency(str, Enum):
    """Supported currencies"""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    PLN = "PLN"
    BTC = "BTC"

class Priority(str, Enum):
    """Task/item priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Status(str, Enum):
    """Generic status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

# =========================================
# 🧾 DOCUMENT PARSING SCHEMAS
# =========================================

class Address(BaseModel):
    """Standard address schema"""
    street: str = Field(description="Street address")
    city: str = Field(description="City name")
    postal_code: str = Field(description="Postal/ZIP code")
    country: str = Field(description="Country name")
    
    @validator('postal_code')
    def validate_postal_code(cls, v):
        """Basic postal code validation"""
        if not v or len(v.strip()) < 3:
            raise ValueError("Postal code must be at least 3 characters")
        return v.strip()

class LineItem(BaseModel):
    """Generic line item for invoices, orders, etc."""
    description: str = Field(description="Item description")
    quantity: int = Field(description="Number of units", ge=1)
    unit_price: float = Field(description="Price per unit", ge=0)
    total_price: Optional[float] = Field(description="Total line price", ge=0, default=None)
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.total_price is None:
            self.total_price = self.quantity * self.unit_price

class Invoice(BaseModel):
    """Complete invoice parsing schema"""
    vendor_name: str = Field(description="Vendor company name")
    vendor_address: Address = Field(description="Vendor address")
    invoice_number: str = Field(description="Unique invoice ID")
    invoice_date: date = Field(description="Invoice issue date")
    line_items: List[LineItem] = Field(description="Invoice line items")
    total_amount: float = Field(description="Total amount due", ge=0)
    currency: Currency = Field(description="Invoice currency")
    due_date: Optional[date] = Field(description="Payment due date", default=None)
    
    @validator('line_items')
    def validate_line_items(cls, v):
        """Ensure at least one line item"""
        if not v:
            raise ValueError("Invoice must have at least one line item")
        return v

# =========================================
# 📊 DATA ANALYSIS SCHEMAS  
# =========================================

class DataPoint(BaseModel):
    """Single data point for analysis"""
    timestamp: datetime = Field(description="Data point timestamp")
    value: float = Field(description="Numeric value")
    category: str = Field(description="Data category")
    metadata: Optional[Dict[str, Any]] = Field(description="Additional metadata")

class AnalysisResult(BaseModel):
    """Analysis results container"""
    summary: str = Field(description="Analysis summary")
    total_points: int = Field(description="Number of data points analyzed", ge=0)
    average_value: float = Field(description="Average value")
    min_value: float = Field(description="Minimum value")
    max_value: float = Field(description="Maximum value")
    categories: List[str] = Field(description="Unique categories found")
    insights: List[str] = Field(description="Key insights from analysis")
    confidence_score: float = Field(description="Confidence in results", ge=0, le=1)

# =========================================
# 🎯 TASK MANAGEMENT SCHEMAS
# =========================================

class Task(BaseModel):
    """Task management schema"""  
    id: str = Field(description="Unique task identifier")
    title: str = Field(description="Task title")
    description: str = Field(description="Detailed task description")
    priority: Priority = Field(description="Task priority level")
    status: Status = Field(description="Current task status")
    created_at: datetime = Field(description="Task creation timestamp")
    due_date: Optional[datetime] = Field(description="Task due date", default=None)
    assigned_to: Optional[str] = Field(description="Assignee name/ID", default=None)
    tags: List[str] = Field(description="Task tags", default_factory=list)
    progress: float = Field(description="Completion percentage", ge=0, le=100, default=0)

class TaskReport(BaseModel):
    """Task reporting schema"""
    report_date: date = Field(description="Report generation date")
    total_tasks: int = Field(description="Total number of tasks", ge=0)
    completed_tasks: int = Field(description="Completed tasks", ge=0)
    pending_tasks: int = Field(description="Pending tasks", ge=0)
    overdue_tasks: int = Field(description="Overdue tasks", ge=0)
    completion_rate: float = Field(description="Overall completion rate", ge=0, le=1)
    tasks_by_priority: Dict[Priority, int] = Field(description="Tasks grouped by priority")
    top_priorities: List[Task] = Field(description="Highest priority tasks")

# =========================================
# 🔧 STRUCTURED OUTPUT ENGINE
# =========================================

@dataclass
class StructuredOutputConfig:
    """Configuration for structured outputs"""
    validation_level: ValidationLevel = ValidationLevel.STRICT
    output_format: OutputFormat = OutputFormat.PYDANTIC
    include_metadata: bool = True
    pretty_json: bool = True

class StructuredOutputEngine:
    """
    🧠 Core engine for handling structured outputs with Pydantic validation
    
    Features:
    - Schema validation and type enforcement
    - Multiple output formats (JSON, dict, Pydantic)
    - Error handling and graceful degradation
    - Custom schema registration
    - Real-time validation
    """
    
    def __init__(self, config: Optional[StructuredOutputConfig] = None):
        self.config = config or StructuredOutputConfig()
        self.registered_schemas: Dict[str, Type[BaseModel]] = {}
        self._register_builtin_schemas()
        
    def _register_builtin_schemas(self):
        """Register built-in schemas"""
        schemas = {
            'invoice': Invoice,
            'address': Address,
            'line_item': LineItem,
            'task': Task,
            'task_report': TaskReport,
            'analysis_result': AnalysisResult,
            'data_point': DataPoint
        }
        
        for name, schema in schemas.items():
            self.registered_schemas[name] = schema
            logger.debug(f"Registered schema: {name}")
    
    def register_schema(self, name: str, schema: Type[BaseModel]) -> None:
        """Register a custom Pydantic schema"""
        if not issubclass(schema, BaseModel):
            raise ValueError(f"Schema {name} must inherit from Pydantic BaseModel")
            
        self.registered_schemas[name] = schema
        logger.info(f"✅ Registered custom schema: {name}")
    
    def get_schema(self, name: str) -> Optional[Type[BaseModel]]:
        """Get registered schema by name"""
        return self.registered_schemas.get(name)
    
    def list_schemas(self) -> List[str]:
        """List all registered schema names"""
        return list(self.registered_schemas.keys())
    
    def parse_with_schema(self, 
                         data: Union[str, dict], 
                         schema_name: str) -> Any:
        """
        Parse data using registered schema
        
        Args:
            data: Raw data (JSON string or dict)
            schema_name: Name of registered schema
            
        Returns:
            Parsed and validated object
            
        Raises:
            ValueError: If schema not found or validation fails
        """
        schema = self.get_schema(schema_name)
        if not schema:
            raise ValueError(f"Schema '{schema_name}' not registered")
        
        try:
            # Parse JSON string if needed
            if isinstance(data, str):
                data = json.loads(data)
                
            # Validate with schema
            validated_obj = schema(**data)
            
            # Return in requested format
            return self._format_output(validated_obj)
            
        except ValidationError as e:
            if self.config.validation_level == ValidationLevel.STRICT:
                raise ValueError(f"Validation failed: {e}")
            elif self.config.validation_level == ValidationLevel.LENIENT:
                logger.warning(f"Validation warning: {e}")
                return self._format_output(data)  # Return raw data
            else:  # DISABLED
                return self._format_output(data)
                
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    def _format_output(self, obj: Any) -> Any:
        """Format output according to config"""
        if isinstance(obj, BaseModel):
            if self.config.output_format == OutputFormat.JSON:
                return obj.json(indent=2 if self.config.pretty_json else None)
            elif self.config.output_format == OutputFormat.DICT:
                return obj.dict()
            else:  # PYDANTIC
                return obj
        else:
            return obj
    
    def validate_data(self, 
                     data: Union[str, dict], 
                     schema: Type[BaseModel]) -> tuple[bool, Optional[str]]:
        """
        Validate data against schema without parsing
        
        Returns:
            (is_valid, error_message)
        """
        try:
            if isinstance(data, str):
                data = json.loads(data)
            schema(**data)
            return True, None
        except (ValidationError, json.JSONDecodeError) as e:
            return False, str(e)
    
    def get_schema_info(self, schema_name: str) -> Dict[str, Any]:
        """Get detailed schema information"""
        schema = self.get_schema(schema_name)
        if not schema:
            return {"error": f"Schema '{schema_name}' not found"}
        
        return {
            "name": schema_name,
            "schema": schema.schema(),
            "fields": list(schema.__fields__.keys()),
            "description": schema.__doc__ or "No description available"
        }

# =========================================
# 🔌 FUNCTION CALLING INTEGRATION
# =========================================

def create_structured_tool(name: str, 
                          description: str,
                          input_schema: Type[BaseModel],
                          output_schema: Type[BaseModel]):
    """
    Create a structured tool with input/output validation
    
    This is a factory function that creates tools with automatic
    Pydantic validation for both inputs and outputs.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Validate inputs
            try:
                validated_input = input_schema(**kwargs)
                kwargs = validated_input.dict()
            except ValidationError as e:
                return {"error": f"Input validation failed: {e}"}
            
            # Execute function
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                return {"error": f"Execution failed: {e}"}
            
            # Validate outputs
            try:
                if isinstance(result, dict):
                    validated_output = output_schema(**result)
                    return validated_output.dict()
                else:
                    return result
            except ValidationError as e:
                logger.warning(f"Output validation failed: {e}")
                return result  # Return raw result if validation fails
        
        wrapper.__name__ = name
        wrapper.__doc__ = description
        wrapper.input_schema = input_schema
        wrapper.output_schema = output_schema
        
        return wrapper
    
    return decorator

# =========================================
# 🧪 EXAMPLE USAGE & TESTING
# =========================================

def demo_structured_outputs():
    """Demonstrate structured outputs functionality"""
    print("🧠 MIGI_7G Structured Outputs Demo")
    print("=" * 50)
    
    engine = StructuredOutputEngine()
    
    # Demo 1: Invoice parsing
    print("\n📋 Demo 1: Invoice Parsing")
    invoice_data = {
        "vendor_name": "MIGI Corp",
        "vendor_address": {
            "street": "123 AI Street",
            "city": "Neural City",
            "postal_code": "12345",
            "country": "Poland"
        },
        "invoice_number": "INV-2025-001",
        "invoice_date": "2025-01-15",
        "line_items": [
            {"description": "AI Processing", "quantity": 10, "unit_price": 100.0},
            {"description": "Data Analysis", "quantity": 5, "unit_price": 200.0}
        ],
        "total_amount": 2000.0,
        "currency": "USD"
    }
    
    try:
        invoice = engine.parse_with_schema(invoice_data, "invoice")
        print(f"✅ Invoice parsed successfully: {invoice.vendor_name}")
        print(f"   Total: {invoice.total_amount} {invoice.currency}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Demo 2: Task management
    print("\n🎯 Demo 2: Task Management")
    task_data = {
        "id": "task-001",
        "title": "Implement Structured Outputs",
        "description": "Add Pydantic schema validation to MIGI_7G",
        "priority": "high",
        "status": "active",
        "created_at": "2025-01-20T10:00:00",
        "progress": 75.5
    }
    
    try:
        task = engine.parse_with_schema(task_data, "task")
        print(f"✅ Task parsed: {task.title}")
        print(f"   Progress: {task.progress}%")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Demo 3: Schema listing
    print(f"\n📊 Available Schemas: {', '.join(engine.list_schemas())}")

if __name__ == "__main__":
    demo_structured_outputs()