"""
Przykład użycia Function Calling w systemie MIGI_7G
Pokazuje jak zintegrować wywoływanie funkcji z głównym systemem
"""

import asyncio
import logging
from typing import Dict, Any
import sys
import os

# Dodaj ścieżkę do modułów MIGI_7G
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import komponentów function calling
from FUNCTION_CALLING.migi_integration import migi_function_calling
from FUNCTION_CALLING.engine import tool
from pydantic import BaseModel, Field

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Przykładowe niestandardowe narzędzia

class WeatherRequest(BaseModel):
    """Request model for weather information"""
    location: str = Field(description="City name or coordinates")
    units: str = Field(default="metric", description="Temperature units (metric/imperial)")

@tool(name="get_weather", description="Get current weather for a location", pydantic_model=WeatherRequest)
def get_weather(request: WeatherRequest) -> Dict[str, Any]:
    """Symuluje pobieranie danych pogodowych"""
    import random
    
    # Symulacja danych pogodowych
    temperatures = {"metric": (15, 25), "imperial": (59, 77)}
    temp_range = temperatures.get(request.units, (15, 25))
    
    return {
        "location": request.location,
        "temperature": random.randint(*temp_range),
        "units": request.units,
        "condition": random.choice(["sunny", "cloudy", "rainy", "snowy"]),
        "humidity": random.randint(30, 90),
        "description": f"Current weather in {request.location}"
    }

class NewsRequest(BaseModel):
    """Request model for news"""
    category: str = Field(default="general", description="News category")
    count: int = Field(default=5, description="Number of articles")

@tool(name="get_news", description="Get latest news headlines", pydantic_model=NewsRequest)
def get_news(request: NewsRequest) -> Dict[str, Any]:
    """Symuluje pobieranie wiadomości"""
    
    # Symulacja nagłówków
    headlines = [
        "AI System Achieves Breakthrough in Digital Consciousness",
        "New Research Shows Promise in Artificial Empathy",
        "Tech Giants Invest in Cognitive Architecture Development", 
        "Scientists Develop Advanced Neural-Semantic Framework",
        "Artificial Intelligence Shows Emotional Intelligence Growth"
    ]
    
    return {
        "category": request.category,
        "headlines": headlines[:request.count],
        "count": len(headlines[:request.count]),
        "timestamp": "2025-11-20T12:00:00Z"
    }

class FileOperationRequest(BaseModel):
    """Request model for file operations"""
    operation: str = Field(description="Operation type: read, write, list")
    path: str = Field(description="File or directory path")
    content: str = Field(default="", description="Content for write operations")

@tool(name="file_operations", description="Perform file system operations", pydantic_model=FileOperationRequest)
def file_operations(request: FileOperationRequest) -> Dict[str, Any]:
    """Wykonuje operacje na plikach (tylko safe operations)"""
    import os
    
    try:
        if request.operation == "list":
            if os.path.exists(request.path) and os.path.isdir(request.path):
                files = os.listdir(request.path)
                return {
                    "operation": "list",
                    "path": request.path,
                    "files": files,
                    "count": len(files)
                }
            else:
                return {"error": "Directory not found", "path": request.path}
        
        elif request.operation == "read":
            if os.path.exists(request.path) and os.path.isfile(request.path):
                # Bezpieczne czytanie tylko plików tekstowych
                try:
                    with open(request.path, 'r', encoding='utf-8') as f:
                        content = f.read(1000)  # Limit to 1000 chars
                    return {
                        "operation": "read",
                        "path": request.path,
                        "content": content,
                        "truncated": len(content) == 1000
                    }
                except UnicodeDecodeError:
                    return {"error": "File is not a text file", "path": request.path}
            else:
                return {"error": "File not found", "path": request.path}
        
        elif request.operation == "write":
            # Tylko w bezpiecznych lokalizacjach
            safe_dirs = ["temp", "tmp", "test"]
            if any(safe_dir in request.path for safe_dir in safe_dirs):
                with open(request.path, 'w', encoding='utf-8') as f:
                    f.write(request.content)
                return {
                    "operation": "write",
                    "path": request.path,
                    "bytes_written": len(request.content.encode('utf-8'))
                }
            else:
                return {"error": "Write operation not allowed in this location"}
        
        else:
            return {"error": f"Unknown operation: {request.operation}"}
            
    except Exception as e:
        return {"error": str(e), "operation": request.operation}

async def demonstrate_function_calling():
    """Demonstracja system function calling"""
    
    print("🧠 MIGI_7G Function Calling Demonstration")
    print("=" * 50)
    
    # Wyświetl dostępne narzędzia
    tools = migi_function_calling.get_available_tools()
    print(f"\n📋 Available Tools ({len(tools)}):")
    for tool in tools:
        print(f"  • {tool['name']}: {tool['description']}")
    
    # Przykłady użycia
    test_messages = [
        "What's the current system information?",
        "Calculate 15 * 23 + 7",
        "What time is it now?",
        "Show me MIGI system status with all details",
        "Get weather for Warsaw",
        "Switch to Hunter archetype",
        "Show me the latest news headlines",
        "Get telemetry data for NSF and Logic_Engine modules"
    ]
    
    print(f"\n🧪 Testing {len(test_messages)} scenarios:")
    print("-" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[{i}] User: {message}")
        
        try:
            result = await migi_function_calling.process_message_with_tools(message)
            
            # Wyświetl odpowiedź asystenta
            response = result["response"]
            print(f"Assistant: {response['content']}")
            
            # Wyświetl wyniki narzędzi
            if result["tool_results"]:
                print("🔧 Tool Results:")
                for tool_result in result["tool_results"]:
                    if tool_result.success:
                        print(f"  ✅ {tool_result.tool_call_id}: {tool_result.content}")
                        if tool_result.execution_time:
                            print(f"     ⏱️ Execution time: {tool_result.execution_time:.3f}s")
                    else:
                        print(f"  ❌ {tool_result.tool_call_id}: {tool_result.error}")
            
        except Exception as e:
            print(f"❌ Error processing message: {e}")
        
        print("-" * 30)
    
    print("\n✅ Function Calling demonstration completed!")

async def interactive_mode():
    """Tryb interaktywny function calling"""
    
    print("\n🎮 Interactive Function Calling Mode")
    print("Type your messages, 'help' for available tools, 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'help':
                tools = migi_function_calling.get_available_tools()
                print(f"\n📋 Available Tools ({len(tools)}):")
                for tool in tools:
                    print(f"  • {tool['name']}: {tool['description']}")
                continue
            
            if user_input.lower() == 'clear':
                migi_function_calling.clear_conversation_history()
                print("🧹 Conversation history cleared")
                continue
            
            if not user_input:
                continue
            
            # Przetwórz wiadomość
            result = await migi_function_calling.process_message_with_tools(user_input)
            
            # Wyświetl odpowiedź
            response = result["response"]
            print(f"\nMIGI: {response['content']}")
            
            # Wyświetl wyniki narzędzi
            if result["tool_results"]:
                print("\n🔧 Tool Results:")
                for tool_result in result["tool_results"]:
                    if tool_result.success:
                        print(f"  ✅ {tool_result.content}")
                        if tool_result.execution_time:
                            print(f"     ⏱️ {tool_result.execution_time:.3f}s")
                    else:
                        print(f"  ❌ Error: {tool_result.error}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    """Główna funkcja demonstracyjna"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="MIGI_7G Function Calling Demo")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Run in interactive mode")
    parser.add_argument("--demo", "-d", action="store_true",
                       help="Run demonstration scenarios")
    
    args = parser.parse_args()
    
    if args.interactive:
        await interactive_mode()
    elif args.demo:
        await demonstrate_function_calling()
    else:
        # Domyślnie uruchom demo, potem interactive
        await demonstrate_function_calling()
        await interactive_mode()

if __name__ == "__main__":
    asyncio.run(main())