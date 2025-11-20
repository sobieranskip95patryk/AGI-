# 🔧 MIGI_7G Function Calling System

## Przegląd

System Function Calling umożliwia systemowi MIGI_7G korzystanie z zewnętrznych narzędzi i API, znacznie rozszerzając jego możliwości interakcji ze światem cyfrowym i fizycznym.

## 🎯 Główne Funkcjonalności

### Wywoływanie Narzędzi
- **Lokalne funkcje**: Wykonywanie funkcji w systemie
- **Zewnętrzne API**: Komunikacja z zewnętrznymi serwisami  
- **Równoległe wywołania**: Jednoczesne wykonywanie wielu narzędzi
- **Walidacja argumentów**: Automatyczna walidacja z Pydantic
- **Timeout handling**: Zabezpieczenie przed zawieszeniem

### Integracja z MIGI_7G
- **Kontekst archetypowy**: Narzędzia dostosowane do aktualnego archetypu
- **Telemetria**: Monitoring wywołań narzędzi
- **Historia konwersacji**: Zachowanie kontekstu między wywołaniami
- **Risk assessment**: Ocena ryzyka wywoływanych funkcji

## 🏗️ Architektura

```
┌─────────────────────────────────────────────────────────────┐
│                    MIGI_7G Core System                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│               Function Calling Engine                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │ Tool        │ │ Validation  │ │ Execution Manager   │   │
│  │ Registry    │ │ Engine      │ │ (Async/Parallel)    │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   External Tools                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │ System      │ │ Web APIs    │ │ File Operations     │   │
│  │ Tools       │ │             │ │                     │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 📚 Użycie

### 1. Podstawowe Użycie

```python
from FUNCTION_CALLING.migi_integration import migi_function_calling

# Przetwórz wiadomość z możliwością wywołania narzędzi
result = await migi_function_calling.process_message_with_tools(
    "What's the current system status and time?"
)

print(result["response"]["content"])
for tool_result in result["tool_results"]:
    print(f"Tool: {tool_result.content}")
```

### 2. Rejestracja Własnych Narzędzi

#### Z Pydantic (Rekomendowane)

```python
from FUNCTION_CALLING.engine import tool
from pydantic import BaseModel, Field

class WeatherRequest(BaseModel):
    location: str = Field(description="City name")
    units: str = Field(default="metric", description="Temperature units")

@tool(name="get_weather", description="Get weather data", pydantic_model=WeatherRequest)
def get_weather(request: WeatherRequest):
    return {
        "location": request.location,
        "temperature": 20,
        "units": request.units
    }
```

#### Z Raw Schema

```python
@tool(
    name="calculate_distance",
    description="Calculate distance between two points",
    parameters_schema={
        "type": "object",
        "properties": {
            "lat1": {"type": "number", "description": "First point latitude"},
            "lon1": {"type": "number", "description": "First point longitude"},
            "lat2": {"type": "number", "description": "Second point latitude"},
            "lon2": {"type": "number", "description": "Second point longitude"}
        },
        "required": ["lat1", "lon1", "lat2", "lon2"]
    }
)
def calculate_distance(lat1, lon1, lat2, lon2):
    # Implementacja obliczania dystansu
    return {"distance": 123.45, "unit": "km"}
```

### 3. Async Tools

```python
@tool(name="fetch_data", description="Fetch data from API")
async def fetch_data(url: str):
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

## 🛠️ Wbudowane Narzędzia

### System Tools

#### get_system_info
```python
# Pobiera informacje o systemie
result = await call_tool("get_system_info", {
    "include_memory": True,
    "include_cpu": True
})
```

#### calculate
```python
# Wykonuje obliczenia matematyczne
result = await call_tool("calculate", {
    "expression": "sqrt(16) + 2 * 3",
    "precision": 2
})
```

#### get_current_time
```python
# Pobiera aktualny czas
result = await call_tool("get_current_time", {
    "format": "%Y-%m-%d %H:%M:%S",
    "timezone": "Europe/Warsaw"
})
```

### MIGI-Specific Tools

#### get_migi_status
```python
# Status systemu MIGI_7G
result = await call_tool("get_migi_status", {
    "include_modules": True,
    "include_archetypes": True,
    "include_metrics": True
})
```

#### trigger_archetype_transition
```python
# Zmiana archetypu
result = await call_tool("trigger_archetype_transition", {
    "target_archetype": "Hunter",
    "force_transition": False,
    "duration": 10
})
```

#### get_telemetry_data
```python
# Dane telemetryczne
result = await call_tool("get_telemetry_data", {
    "modules": ["NSF", "Logic_Engine"],
    "time_range": 300,
    "include_raw": True
})
```

## ⚙️ Konfiguracja

### Engine Settings

```python
from FUNCTION_CALLING.engine import function_calling_engine

# Włącz/wyłącz równoległe wywołania
function_calling_engine.parallel_calling_enabled = True

# Maksymalna liczba jednoczesnych wywołań
function_calling_engine.max_concurrent_calls = 5

# Timeout dla wykonania narzędzia (sekundy)
function_calling_engine.execution_timeout = 30.0
```

### Tool Choice Modes

```python
# Auto - model decyduje czy wywołać narzędzia
result = await process_with_tools(message, tool_choice="auto")

# Required - wymuś wywołanie narzędzi
result = await process_with_tools(message, tool_choice="required")

# None - wyłącz narzędzia
result = await process_with_tools(message, tool_choice="none")

# Specific tool - wymuś konkretne narzędzie
result = await process_with_tools(message, tool_choice={
    "type": "function",
    "function": {"name": "get_weather"}
})
```

## 🔒 Bezpieczeństwo

### Walidacja Argumentów
- **Pydantic validation**: Automatyczna walidacja typów i wartości
- **Schema compliance**: Sprawdzanie zgodności ze schematem
- **Input sanitization**: Czyszczenie danych wejściowych

### Execution Safety
- **Timeout protection**: Ochrona przed zawieszeniem
- **Resource limits**: Ograniczenia zasobów
- **Safe execution context**: Bezpieczne środowisko wykonania
- **Error isolation**: Izolacja błędów

### Access Control
- **Tool whitelisting**: Lista dozwolonych narzędzi
- **Permission system**: System uprawnień
- **Audit logging**: Logowanie wszystkich wywołań

## 📊 Monitoring i Debugowanie

### Logging

```python
import logging

# Włącz szczegółowe logowanie
logging.getLogger("FUNCTION_CALLING").setLevel(logging.DEBUG)

# Monitoruj wykonanie narzędzi
logger.info(f"Tool {tool_name} executed in {execution_time:.3f}s")
```

### Metrics

```python
# Statystyki wywołań narzędzi
stats = function_calling_engine.get_execution_stats()
print(f"Total calls: {stats['total_calls']}")
print(f"Success rate: {stats['success_rate']:.2%}")
print(f"Average execution time: {stats['avg_execution_time']:.3f}s")
```

### Error Handling

```python
try:
    result = await execute_tool_call(tool_call)
    if not result.success:
        logger.error(f"Tool failed: {result.error}")
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
```

## 🚀 Przykłady Zaawansowane

### Łańcuchowe Wywołania Narzędzi

```python
# Przykład: Pobierz pogodę, następnie zasugeruj ubranie
@tool(name="suggest_clothing", description="Suggest clothing based on weather")
async def suggest_clothing(temperature: float, condition: str):
    if temperature < 10:
        return {"suggestion": "Warm jacket and pants"}
    elif condition == "rainy":
        return {"suggestion": "Raincoat and umbrella"}
    else:
        return {"suggestion": "Light clothing"}

# Użycie w konwersacji będzie automatycznie łączyć narzędzia
```

### Narzędzia z Kontekstem MIGI

```python
@tool(name="archetype_appropriate_response")
async def archetype_appropriate_response(message: str, current_archetype: str):
    """Generuje odpowiedź dostosowaną do aktualnego archetypu"""
    
    archetype_styles = {
        "Hunter": "Direct, action-oriented response",
        "Sage": "Thoughtful, analytical response", 
        "Lover": "Empathetic, caring response",
        "Creator": "Innovative, solution-focused response",
        "Explorer": "Curious, open-minded response"
    }
    
    style = archetype_styles.get(current_archetype, "Balanced response")
    
    return {
        "archetype": current_archetype,
        "style": style,
        "adapted_message": f"[{current_archetype} mode] {message}"
    }
```

### Integracja z External APIs

```python
@tool(name="search_web", description="Search the web for information")
async def search_web(query: str, num_results: int = 5):
    """Wyszukuje informacje w internecie"""
    import aiohttp
    
    # Przykład integracji z API wyszukiwarki
    async with aiohttp.ClientSession() as session:
        params = {"q": query, "num": num_results}
        async with session.get("https://api.search.com/search", params=params) as response:
            results = await response.json()
            return {
                "query": query,
                "results": results.get("items", []),
                "total_results": len(results.get("items", []))
            }
```

## 🎭 Integracja z Archetypami

System automatycznie dostosowuje narzędzia do aktualnego archetypu:

```python
# Hunter - Narzędzia fokusowane na działanie
hunter_tools = ["execute_command", "get_status", "trigger_action"]

# Sage - Narzędzia analityczne
sage_tools = ["analyze_data", "get_insights", "calculate_probability"]

# Lover - Narzędzia społeczne i empatyczne  
lover_tools = ["check_sentiment", "get_social_data", "analyze_emotions"]

# Creator - Narzędzia kreatywne
creator_tools = ["generate_content", "create_design", "brainstorm_ideas"]

# Explorer - Narzędzia eksploracyjne
explorer_tools = ["search_web", "discover_connections", "explore_data"]
```

## 📈 Performance Optimization

### Parallel Execution
- Automatyczne wykrywanie niezależnych wywołań
- Limit jednoczesnych operacji
- Load balancing między narzędziami

### Caching
- Cache wyników dla często używanych narzędzi
- Inteligentne invalidation
- Memory-based i persistent cache

### Resource Management
- Memory limits dla narzędzi
- CPU throttling dla długotrwałych operacji
- Network timeout handling

## 🔮 Przyszłe Rozszerzenia

### Planowane Funkcjonalności
- **Plugin system**: Dynamiczne ładowanie narzędzi
- **Tool marketplace**: Repozytorium narzędzi społeczności
- **Advanced routing**: Inteligentne przekierowanie wywołań
- **ML-based optimization**: Optymalizacja wyboru narzędzi

### Integracje
- **Grok API**: Natywna integracja z Grok
- **OpenAI Functions**: Kompatybilność z OpenAI
- **Anthropic Claude**: Wsparcie dla Claude
- **Local LLMs**: Integracja z lokalnymi modelami

---

## 🎯 Przykład Kompletnej Implementacji

Zobacz `FUNCTION_CALLING/demo.py` dla pełnego przykładu implementacji i użycia systemu Function Calling w MIGI_7G.

```bash
# Uruchom demonstrację
python FUNCTION_CALLING/demo.py --demo

# Tryb interaktywny
python FUNCTION_CALLING/demo.py --interactive

# Pełny test (demo + interactive)
python FUNCTION_CALLING/demo.py
```

System Function Calling przekształca MIGI_7G w potężną platformę zdolną do interakcji z szerokim spektrum zewnętrznych zasobów, znacznie rozszerzając jego możliwości i praktyczne zastosowania.