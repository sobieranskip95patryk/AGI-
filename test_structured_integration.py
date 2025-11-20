"""
🧠 MIGI_7G Structured Outputs Integration Test
=============================================

Test integracji Structured Outputs z Function Calling Engine.
Sprawdza czy wszystkie komponenty działają razem poprawnie.
"""

import sys
sys.path.append('.')

from FUNCTION_CALLING.engine import function_calling_engine
from FUNCTION_CALLING.structured_outputs import StructuredOutputEngine
import json

def test_structured_integration():
    """Test integracji Structured Outputs z Function Calling Engine"""
    print("🧠 MIGI_7G Structured Outputs Integration Test")
    print("=" * 60)
    
    # Test 1: Sprawdź czy structured engine jest dostępny
    print("\n🔧 Test 1: Structured Engine Availability")
    if hasattr(function_calling_engine, 'structured_engine'):
        if function_calling_engine.structured_engine:
            print("✅ Structured Outputs engine is available")
            print(f"   Available schemas: {len(function_calling_engine.list_schemas())} schemas")
        else:
            print("❌ Structured Outputs engine is None")
    else:
        print("❌ Structured Outputs engine not found")
    
    # Test 2: List schemas
    print("\n📋 Test 2: Schema Listing")
    try:
        schemas = function_calling_engine.list_schemas()
        print(f"✅ Found {len(schemas)} schemas:")
        for schema in schemas:
            print(f"   - {schema}")
    except Exception as e:
        print(f"❌ Error listing schemas: {e}")
    
    # Test 3: Get schema info
    print("\n📊 Test 3: Schema Information")
    try:
        invoice_info = function_calling_engine.get_schema_info("invoice")
        if "error" not in invoice_info:
            print("✅ Invoice schema info retrieved:")
            print(f"   - Name: {invoice_info['name']}")
            print(f"   - Fields: {len(invoice_info['fields'])} fields")
            print(f"   - Description: {invoice_info['description'][:50]}...")
        else:
            print(f"❌ Error: {invoice_info['error']}")
    except Exception as e:
        print(f"❌ Error getting schema info: {e}")
    
    # Test 4: Parse data with schema
    print("\n🔍 Test 4: Data Parsing with Schema")
    invoice_data = {
        "vendor_name": "Test Corp",
        "vendor_address": {
            "street": "123 Test St",
            "city": "Test City",
            "postal_code": "12345",
            "country": "Poland"
        },
        "invoice_number": "TEST-001",
        "invoice_date": "2025-01-20",
        "line_items": [
            {"description": "Test Service", "quantity": 1, "unit_price": 100.0}
        ],
        "total_amount": 100.0,
        "currency": "USD"
    }
    
    try:
        parsed_invoice = function_calling_engine.parse_with_schema(invoice_data, "invoice")
        print("✅ Invoice data parsed successfully")
        print(f"   Vendor: {parsed_invoice.vendor_name}")
        print(f"   Total: {parsed_invoice.total_amount} {parsed_invoice.currency}")
        print(f"   Items: {len(parsed_invoice.line_items)} items")
    except Exception as e:
        print(f"❌ Error parsing invoice: {e}")
    
    # Test 5: Tool registration and execution
    print("\n🔧 Test 5: Tool Registration")
    tools_before = len(function_calling_engine.tools)
    
    # Register tools from engine.py
    try:
        # Check if tools are already registered
        print(f"✅ Function Calling Engine has {tools_before} tools registered")
        
        # List some tool names
        tool_names = list(function_calling_engine.tools.keys())[:5]
        print(f"   Sample tools: {', '.join(tool_names)}")
        
    except Exception as e:
        print(f"❌ Error checking tools: {e}")
    
    # Test 6: Validate tool outputs
    print("\n🧪 Test 6: Tool Output Validation")
    from FUNCTION_CALLING.structured_outputs import Invoice
    
    test_output = {
        "vendor_name": "MIGI Test",
        "vendor_address": {
            "street": "456 AI St",
            "city": "Neural City",
            "postal_code": "54321",
            "country": "Poland"
        },
        "invoice_number": "VALID-001",
        "invoice_date": "2025-01-20",
        "line_items": [
            {"description": "AI Processing", "quantity": 2, "unit_price": 500.0}
        ],
        "total_amount": 1000.0,
        "currency": "USD"
    }
    
    try:
        is_valid, error = function_calling_engine.validate_output(test_output, Invoice)
        if is_valid:
            print("✅ Tool output validation passed")
        else:
            print(f"❌ Tool output validation failed: {error}")
    except Exception as e:
        print(f"❌ Error validating output: {e}")
    
    print("\n🎉 Integration test completed!")

if __name__ == "__main__":
    test_structured_integration()