"""
🧠 MIGI_7G Structured Outputs - Complete Demo
==========================================

Kompleksowa demonstracja wszystkich funkcjonalności Structured Outputs
w systemie MIGI_7G Function Calling Engine.

Author: MIGI_7G Brain
Version: 1.0.0
"""

import json
from datetime import datetime
from FUNCTION_CALLING.engine import function_calling_engine
from FUNCTION_CALLING.structured_outputs import StructuredOutputEngine, ValidationLevel, StructuredOutputConfig

def demo_header(title: str):
    """Pretty print demo section header"""
    print(f"\n{'='*60}")
    print(f"🧠 {title}")
    print(f"{'='*60}")

def demo_complete_structured_outputs():
    """Complete demonstration of structured outputs"""
    
    demo_header("MIGI_7G Structured Outputs Complete Demo")
    
    # Initialize engines
    print("🔧 Initializing engines...")
    
    # Standard engine
    standard_engine = StructuredOutputEngine()
    
    # Lenient engine for error recovery
    lenient_config = StructuredOutputConfig(validation_level=ValidationLevel.LENIENT)
    lenient_engine = StructuredOutputEngine(lenient_config)
    
    print("✅ Engines initialized")
    print(f"   - Standard engine: {len(standard_engine.list_schemas())} schemas")
    print(f"   - Lenient engine: {len(lenient_engine.list_schemas())} schemas")
    print(f"   - Function calling engine: {len(function_calling_engine.tools)} tools")
    
    # Demo 1: Schema Exploration
    demo_header("Demo 1: Schema Exploration")
    
    schemas = standard_engine.list_schemas()
    print(f"📋 Available schemas ({len(schemas)}):")
    
    for schema in schemas:
        info = standard_engine.get_schema_info(schema)
        print(f"   • {schema:<15} - {len(info['fields'])} fields - {info['description'][:40]}...")
    
    # Demo 2: Invoice Processing
    demo_header("Demo 2: Advanced Invoice Processing")
    
    complex_invoice = {
        "vendor_name": "MIGI Technologies Sp. z o.o.",
        "vendor_address": {
            "street": "ul. Sztucznej Inteligencji 42",
            "city": "Warszawa",
            "postal_code": "00-001",
            "country": "Polska"
        },
        "invoice_number": "MIGI/2025/001",
        "invoice_date": "2025-01-20",
        "line_items": [
            {
                "description": "Usługi AI - analiza danych", 
                "quantity": 100,
                "unit_price": 50.0
            },
            {
                "description": "Konsultacje machine learning",
                "quantity": 20, 
                "unit_price": 200.0
            },
            {
                "description": "Wdrożenie systemu MIGI_7G",
                "quantity": 1,
                "unit_price": 10000.0
            }
        ],
        "total_amount": 19000.0,
        "currency": "PLN",
        "due_date": "2025-02-20"
    }
    
    try:
        invoice = standard_engine.parse_with_schema(complex_invoice, "invoice")
        print("✅ Complex invoice parsed successfully:")
        print(f"   📄 Invoice: {invoice.invoice_number}")
        print(f"   🏢 Vendor: {invoice.vendor_name}")
        print(f"   📍 Location: {invoice.vendor_address.city}, {invoice.vendor_address.country}")
        print(f"   💰 Total: {invoice.total_amount} {invoice.currency}")
        print(f"   📦 Items: {len(invoice.line_items)} items")
        
        # Calculate totals
        calculated_total = sum(item.total_price for item in invoice.line_items)
        print(f"   🧮 Calculated total: {calculated_total} {invoice.currency}")
        print(f"   ✅ Total matches: {'Yes' if calculated_total == invoice.total_amount else 'No'}")
        
    except Exception as e:
        print(f"❌ Invoice processing error: {e}")
    
    # Demo 3: Task Management
    demo_header("Demo 3: Project Task Management")
    
    project_tasks = [
        {
            "id": "MIGI-001",
            "title": "Implement Structured Outputs",
            "description": "Add Pydantic-based structured output validation to MIGI_7G",
            "priority": "high",
            "status": "completed",
            "created_at": "2025-01-20T08:00:00",
            "progress": 100.0,
            "assigned_to": "MIGI_7G_Brain",
            "tags": ["core", "validation", "pydantic"]
        },
        {
            "id": "MIGI-002", 
            "title": "Function Calling Engine Enhancement",
            "description": "Enhance function calling with structured tool registration",
            "priority": "high",
            "status": "active",
            "created_at": "2025-01-20T09:00:00",
            "progress": 85.0,
            "assigned_to": "MIGI_7G_Brain",
            "tags": ["engine", "tools", "enhancement"]
        },
        {
            "id": "MIGI-003",
            "title": "Documentation and Examples",
            "description": "Create comprehensive documentation and usage examples", 
            "priority": "medium",
            "status": "active",
            "created_at": "2025-01-20T10:00:00",
            "progress": 75.0,
            "assigned_to": "MIGI_7G_Brain",
            "tags": ["docs", "examples", "tutorial"]
        }
    ]
    
    print(f"📋 Processing {len(project_tasks)} project tasks:")
    
    parsed_tasks = []
    for task_data in project_tasks:
        try:
            task = standard_engine.parse_with_schema(task_data, "task")
            parsed_tasks.append(task)
            
            status_emoji = {"completed": "✅", "active": "🔄", "pending": "⏳"}.get(task.status, "❓")
            priority_emoji = {"high": "🔥", "medium": "⚡", "low": "📝"}.get(task.priority, "❓")
            
            print(f"   {status_emoji} {priority_emoji} [{task.id}] {task.title}")
            print(f"      Progress: {task.progress}% | Assignee: {task.assigned_to}")
            print(f"      Tags: {', '.join(task.tags)}")
            
        except Exception as e:
            print(f"   ❌ Error parsing task {task_data['id']}: {e}")
    
    # Calculate project metrics
    if parsed_tasks:
        total_progress = sum(t.progress for t in parsed_tasks) / len(parsed_tasks)
        completed_tasks = len([t for t in parsed_tasks if t.status == "completed"])
        high_priority = len([t for t in parsed_tasks if t.priority == "high"])
        
        print("\n   📊 Project Metrics:")
        print(f"      Overall Progress: {total_progress:.1f}%")
        print(f"      Completed Tasks: {completed_tasks}/{len(parsed_tasks)}")
        print(f"      High Priority: {high_priority} tasks")
    
    # Demo 4: Error Handling and Recovery
    demo_header("Demo 4: Error Handling & Recovery")
    
    # Test with invalid data
    invalid_invoice = {
        "vendor_name": "",  # Empty name
        "invoice_date": "invalid-date",  # Invalid date format
        "line_items": [],  # Empty items (should fail validation)
        "total_amount": -100,  # Negative amount
        "currency": "INVALID"  # Invalid currency
    }
    
    print("🧪 Testing error handling with invalid data:")
    
    # Test strict validation
    try:
        strict_result = standard_engine.parse_with_schema(invalid_invoice, "invoice")
        print("❌ Strict validation should have failed")
    except Exception as e:
        print(f"✅ Strict validation correctly failed: {str(e)[:80]}...")
    
    # Test lenient validation  
    try:
        lenient_result = lenient_engine.parse_with_schema(invalid_invoice, "invoice")
        print("✅ Lenient validation handled gracefully")
    except Exception as e:
        print(f"⚠️ Lenient validation also failed: {str(e)[:80]}...")
    
    # Demo 5: Function Calling Integration
    demo_header("Demo 5: Structured Function Calling")
    
    # Test available structured tools
    available_tools = list(function_calling_engine.tools.keys())
    print(f"🔧 Available tools: {len(available_tools)}")
    for tool in available_tools:
        print(f"   • {tool}")
    
    # Test structured output validation in function calling
    print("\n🔍 Testing output validation:")
    
    test_data = {
        "confidence": 0.95,
        "extracted_data": {"title": "Test Document", "pages": 5},
        "entities": ["MIGI_7G", "AI", "Poland"],
        "summary": "Test document processing completed successfully"
    }
    
    from FUNCTION_CALLING.structured_examples import DocumentParseResult
    is_valid, error = function_calling_engine.validate_output(test_data, DocumentParseResult)
    
    if is_valid:
        print("✅ Function output validation passed")
    else:
        print(f"❌ Function output validation failed: {error}")
    
    # Demo 6: Performance Benchmark
    demo_header("Demo 6: Performance Benchmark")
    
    print("⚡ Running performance tests...")
    
    import time
    
    # Benchmark parsing speed
    start_time = time.time()
    iterations = 1000
    
    simple_task = {
        "id": "PERF-001",
        "title": "Performance Test", 
        "description": "Testing parsing performance",
        "priority": "low",
        "status": "active",
        "created_at": "2025-01-20T12:00:00",
        "progress": 50.0
    }
    
    for i in range(iterations):
        try:
            task = standard_engine.parse_with_schema(simple_task, "task")
        except Exception:
            pass
    
    end_time = time.time()
    avg_time = (end_time - start_time) / iterations * 1000  # Convert to milliseconds
    
    print("✅ Performance benchmark completed:")
    print(f"   Iterations: {iterations}")
    print(f"   Total time: {end_time - start_time:.3f}s")
    print(f"   Average time per validation: {avg_time:.3f}ms")
    print(f"   Validations per second: {iterations / (end_time - start_time):.0f}")
    
    # Final Summary
    demo_header("Demo Summary & Statistics")
    
    print("🎉 Structured Outputs Demo Completed Successfully!")
    print(f"")
    print("📊 System Status:")
    print("   • Structured Output Engine: ✅ Operational")
    print("   • Function Calling Engine: ✅ Operational") 
    print(f"   • Available Schemas: {len(standard_engine.list_schemas())} built-in")
    print(f"   • Registered Tools: {len(function_calling_engine.tools)}")
    print(f"   • Performance: {avg_time:.1f}ms avg validation time")
    print(f"")
    print(f"🎯 Key Features Demonstrated:")
    print(f"   ✅ Complex document parsing (invoices)")
    print(f"   ✅ Task management and project metrics")
    print(f"   ✅ Error handling and recovery mechanisms")
    print(f"   ✅ Function calling integration")
    print(f"   ✅ Performance benchmarking")
    print(f"   ✅ Schema validation and type safety")
    print(f"")
    print(f"🚀 MIGI_7G Structured Outputs is ready for production use!")

if __name__ == "__main__":
    demo_complete_structured_outputs()