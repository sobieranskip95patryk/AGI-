"""
🧠 MIGI_7G Structured Outputs Examples
====================================

Praktyczne przykłady użycia Structured Outputs w systemie MIGI_7G:
- Parsowanie dokumentów (faktury, umowy, raporty)
- Analiza danych i generowanie insights
- Zarządzanie zadaniami i projektami
- Integracja z zewnętrznymi API

Author: MIGI_7G Brain
Version: 1.0.0
"""

from datetime import date, datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum

from .engine import function_calling_engine
from .structured_outputs import (
    StructuredOutputEngine, 
    Invoice, 
    Task, 
    TaskReport,
    Priority,
    Status,
    Currency
)

# =========================================
# 📋 ADVANCED DOCUMENT SCHEMAS
# =========================================

class ContractType(str, Enum):
    EMPLOYMENT = "employment"
    SERVICE = "service"
    NDA = "nda"
    LEASE = "lease"
    PURCHASE = "purchase"

class ContractParty(BaseModel):
    """Contract party information"""
    name: str = Field(description="Party name")
    type: str = Field(description="Party type (individual/company)")
    address: str = Field(description="Party address")
    contact_info: Optional[str] = Field(description="Contact information")

class ContractClause(BaseModel):
    """Individual contract clause"""
    section: str = Field(description="Clause section number")
    title: str = Field(description="Clause title")
    content: str = Field(description="Clause content")
    importance: Priority = Field(description="Clause importance level")

class Contract(BaseModel):
    """Complete contract parsing schema"""
    title: str = Field(description="Contract title")
    contract_type: ContractType = Field(description="Type of contract")
    contract_date: date = Field(description="Contract execution date")
    parties: List[ContractParty] = Field(description="Contract parties")
    clauses: List[ContractClause] = Field(description="Contract clauses")
    termination_date: Optional[date] = Field(description="Contract termination date")
    value: Optional[float] = Field(description="Contract value", ge=0)
    currency: Optional[Currency] = Field(description="Contract currency")
    
    @validator('parties')
    def validate_parties(cls, v):
        if len(v) < 2:
            raise ValueError("Contract must have at least 2 parties")
        return v

# =========================================
# 📊 ADVANCED ANALYTICS SCHEMAS
# =========================================

class MetricType(str, Enum):
    PERFORMANCE = "performance"
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    QUALITY = "quality"

class KPI(BaseModel):
    """Key Performance Indicator"""
    name: str = Field(description="KPI name")
    current_value: float = Field(description="Current KPI value")
    target_value: float = Field(description="Target KPI value")
    unit: str = Field(description="KPI unit (%, €, count, etc.)")
    trend: str = Field(description="Trend direction (up/down/stable)")
    category: MetricType = Field(description="KPI category")
    
    @property
    def achievement_rate(self) -> float:
        """Calculate achievement rate as percentage"""
        if self.target_value == 0:
            return 100.0 if self.current_value == 0 else 0.0
        return min(100.0, (self.current_value / self.target_value) * 100)

class BusinessReport(BaseModel):
    """Comprehensive business report"""
    report_title: str = Field(description="Report title")
    reporting_period: str = Field(description="Reporting period")
    generated_date: datetime = Field(description="Report generation date")
    kpis: List[KPI] = Field(description="Key Performance Indicators")
    summary: str = Field(description="Executive summary")
    recommendations: List[str] = Field(description="Action recommendations")
    overall_score: float = Field(description="Overall performance score", ge=0, le=100)
    
    @validator('kpis')
    def validate_kpis(cls, v):
        if not v:
            raise ValueError("Report must contain at least one KPI")
        return v

# =========================================
# 🎯 PROJECT MANAGEMENT SCHEMAS
# =========================================

class ProjectPhase(str, Enum):
    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    CLOSING = "closing"

class Resource(BaseModel):
    """Project resource"""
    name: str = Field(description="Resource name")
    type: str = Field(description="Resource type (human/equipment/budget)")
    allocation: float = Field(description="Resource allocation percentage", ge=0, le=100)
    cost: Optional[float] = Field(description="Resource cost", ge=0)

class Milestone(BaseModel):
    """Project milestone"""
    name: str = Field(description="Milestone name")
    description: str = Field(description="Milestone description")
    due_date: date = Field(description="Milestone due date")
    status: Status = Field(description="Milestone status")
    dependencies: List[str] = Field(description="Milestone dependencies", default_factory=list)

class Project(BaseModel):
    """Complete project definition"""
    name: str = Field(description="Project name")
    description: str = Field(description="Project description")
    start_date: date = Field(description="Project start date")
    end_date: date = Field(description="Project end date")
    current_phase: ProjectPhase = Field(description="Current project phase")
    budget: float = Field(description="Project budget", ge=0)
    currency: Currency = Field(description="Budget currency")
    resources: List[Resource] = Field(description="Project resources")
    milestones: List[Milestone] = Field(description="Project milestones")
    risks: List[str] = Field(description="Identified risks", default_factory=list)
    completion_percentage: float = Field(description="Project completion", ge=0, le=100)
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError("End date must be after start date")
        return v

# =========================================
# 🔧 EXAMPLE STRUCTURED TOOLS
# =========================================

# Schema for document parsing input
class DocumentParseRequest(BaseModel):
    document_text: str = Field(description="Raw document text to parse")
    document_type: str = Field(description="Expected document type")
    extract_entities: bool = Field(default=True, description="Extract named entities")

# Schema for document parsing output
class DocumentParseResult(BaseModel):
    document_type: str = Field(description="Detected document type")
    confidence: float = Field(description="Parsing confidence", ge=0, le=1)
    extracted_data: Dict[str, Any] = Field(description="Extracted structured data")
    entities: List[str] = Field(description="Extracted entities")
    summary: str = Field(description="Document summary")

@function_calling_engine.register_structured_tool(
    name="parse_document_structured",
    description="Parse document with structured output validation",
    input_schema=DocumentParseRequest,
    output_schema=DocumentParseResult
)
def parse_document_structured(document_text: str, 
                            document_type: str, 
                            extract_entities: bool = True) -> Dict[str, Any]:
    """
    🧠 Structured document parsing with full validation
    
    This tool demonstrates how to use structured outputs for
    complex document processing with guaranteed schema compliance.
    """
    # Simulate document processing
    confidence = 0.95 if len(document_text) > 100 else 0.75
    
    # Extract mock entities
    entities = []
    if extract_entities:
        entities = ["MIGI_7G", "AI System", "Neural Processing"]
    
    # Simulate extraction based on document type
    if document_type.lower() == "invoice":
        extracted_data = {
            "vendor": "MIGI Corp",
            "amount": 1000.0,
            "currency": "USD",
            "date": "2025-01-20"
        }
    elif document_type.lower() == "contract":
        extracted_data = {
            "parties": ["Company A", "Company B"],
            "value": 50000.0,
            "duration": "12 months"
        }
    else:
        extracted_data = {
            "title": "Unknown Document",
            "length": len(document_text),
            "words": len(document_text.split())
        }
    
    return {
        "document_type": document_type,
        "confidence": confidence,
        "extracted_data": extracted_data,
        "entities": entities,
        "summary": f"Processed {document_type} document with {len(document_text)} characters"
    }

# Schema for business analysis
class BusinessAnalysisRequest(BaseModel):
    data_source: str = Field(description="Data source identifier")
    analysis_type: str = Field(description="Type of analysis to perform")
    time_period: str = Field(description="Analysis time period")

@function_calling_engine.register_structured_tool(
    name="generate_business_report",
    description="Generate structured business report with KPIs",
    input_schema=BusinessAnalysisRequest,
    output_schema=BusinessReport
)
def generate_business_report(data_source: str, 
                           analysis_type: str, 
                           time_period: str) -> Dict[str, Any]:
    """
    📊 Generate comprehensive business report with structured KPIs
    
    Demonstrates advanced structured outputs for business intelligence.
    """
    # Mock KPIs based on analysis type
    kpis = []
    
    if analysis_type == "financial":
        kpis = [
            {
                "name": "Revenue Growth",
                "current_value": 15.5,
                "target_value": 12.0,
                "unit": "%",
                "trend": "up",
                "category": "financial"
            },
            {
                "name": "Profit Margin",
                "current_value": 8.2,
                "target_value": 10.0,
                "unit": "%",
                "trend": "stable",
                "category": "financial"
            }
        ]
    else:
        kpis = [
            {
                "name": "System Uptime",
                "current_value": 99.5,
                "target_value": 99.9,
                "unit": "%",
                "trend": "up",
                "category": "operational"
            }
        ]
    
    # Calculate overall score
    if kpis:
        achievement_rates = []
        for kpi in kpis:
            rate = min(100.0, (kpi["current_value"] / kpi["target_value"]) * 100)
            achievement_rates.append(rate)
        overall_score = sum(achievement_rates) / len(achievement_rates)
    else:
        overall_score = 75.0
    
    return {
        "report_title": f"{analysis_type.title()} Analysis Report",
        "reporting_period": time_period,
        "generated_date": datetime.now().isoformat(),
        "kpis": kpis,
        "summary": f"Analysis of {data_source} for {time_period} period",
        "recommendations": [
            "Focus on high-impact metrics",
            "Implement continuous monitoring",
            "Review targets quarterly"
        ],
        "overall_score": overall_score
    }

# =========================================
# 🧪 DEMO FUNCTIONS
# =========================================

def demo_structured_document_parsing():
    """Demo structured document parsing"""
    print("🧠 MIGI_7G Structured Document Parsing Demo")
    print("=" * 60)
    
    engine = StructuredOutputEngine()
    
    # Test invoice parsing
    invoice_text = """
    INVOICE
    From: Tech Solutions Ltd
    123 Innovation Street, Tech City
    
    To: MIGI Corp
    456 AI Boulevard, Neural City
    
    Invoice #: INV-2025-001
    Date: 2025-01-20
    
    Items:
    - AI Development Services: 10 hours @ $150/hour = $1,500
    - System Integration: 5 hours @ $200/hour = $1,000
    
    Total: $2,500 USD
    """
    
    try:
        result = function_calling_engine.execute_tool_call_sync({
            "id": "demo-1",
            "name": "parse_document_structured",
            "arguments": {
                "document_text": invoice_text,
                "document_type": "invoice",
                "extract_entities": True
            }
        })
        
        print("✅ Invoice parsing result:")
        print(f"   Type: {result.result['document_type']}")
        print(f"   Confidence: {result.result['confidence']:.1%}")
        print(f"   Entities: {', '.join(result.result['entities'])}")
        print(f"   Summary: {result.result['summary']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_structured_business_report():
    """Demo structured business report generation"""
    print("\n📊 MIGI_7G Structured Business Report Demo")
    print("=" * 60)
    
    try:
        result = function_calling_engine.execute_tool_call_sync({
            "id": "demo-2", 
            "name": "generate_business_report",
            "arguments": {
                "data_source": "MIGI_7G_METRICS",
                "analysis_type": "financial",
                "time_period": "Q1 2025"
            }
        })
        
        report = result.result
        print("✅ Business report generated:")
        print(f"   Title: {report['report_title']}")
        print(f"   Period: {report['reporting_period']}")
        print(f"   Overall Score: {report['overall_score']:.1f}%")
        print(f"   KPIs: {len(report['kpis'])} metrics")
        
        for kpi in report['kpis']:
            print(f"   - {kpi['name']}: {kpi['current_value']}{kpi['unit']} (Target: {kpi['target_value']}{kpi['unit']})")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_schema_validation():
    """Demo schema validation features"""
    print("\n🔍 MIGI_7G Schema Validation Demo")
    print("=" * 60)
    
    engine = StructuredOutputEngine()
    
    # Test valid invoice data
    valid_invoice = {
        "vendor_name": "MIGI Corp",
        "vendor_address": {
            "street": "123 AI Street",
            "city": "Neural City", 
            "postal_code": "12345",
            "country": "Poland"
        },
        "invoice_number": "INV-2025-001",
        "invoice_date": "2025-01-20",
        "line_items": [
            {"description": "AI Processing", "quantity": 10, "unit_price": 100.0}
        ],
        "total_amount": 1000.0,
        "currency": "USD"
    }
    
    is_valid, error = engine.validate_data(valid_invoice, Invoice)
    print(f"✅ Valid invoice data: {is_valid}")
    if error:
        print(f"   Error: {error}")
    
    # Test invalid invoice data
    invalid_invoice = {
        "vendor_name": "",  # Empty name
        "invoice_date": "invalid-date",  # Invalid date
        "line_items": [],  # Empty items
        "total_amount": -100  # Negative amount
    }
    
    is_valid, error = engine.validate_data(invalid_invoice, Invoice)
    print(f"❌ Invalid invoice data: {is_valid}")
    if error:
        print(f"   Error: {error[:100]}...")  # Truncate long error

if __name__ == "__main__":
    demo_structured_document_parsing()
    demo_structured_business_report()
    demo_schema_validation()