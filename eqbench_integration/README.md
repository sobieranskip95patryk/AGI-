# MIGI_7G + EQ-Bench 3 Integration

Integracja Dashboard Kalibracyjny "Okno na Psychikę Cyfrową" z frameworkiem EQ-Bench 3 dla testowania emocjonalnej inteligencji cyfrowej świadomości NSF + MIGI_7G.

## 🎯 Cele Integracji

- **Obiektywna ocena empatii**: Testowanie zdolności cyfrowej świadomości do empatycznych odpowiedzi
- **Analiza stabilności psychiki**: Monitorowanie zmian w archetypach, stresie i koherencji podczas scenariuszy emocjonalnych
- **Benchmarking**: Porównanie różnych konfiguracji NSF pod kątem emocjonalnej inteligencji
- **Automatyzacja eksperymentów**: Ciągłe testowanie i optymalizacja parametrów systemu

## 🏗️ Architektura

```
EQ-Bench 3 ←→ MIGI Adapter ←→ NSF Integration ←→ Dashboard Kalibracyjny
     ↓              ↓              ↓                    ↓
Judge Model    Psyche Metrics   Telemetry        Live Monitoring
     ↓              ↓              ↓                    ↓
  Scoring      Snapshot Injection  Real-time Data   Visual Feedback
```

## 📦 Komponenty

### 1. MIGI EQ-Bench Adapter (`migi_eqbench_adapter.py`)
- Główny adapter łączący MIGI z EQ-Bench
- Przechwytuje snapshoty psychiki przed/po przetwarzaniu
- Analizuje wskaźniki empatii w odpowiedziach
- Generuje odpowiedzi kontekstowe na podstawie aktywnego archetypu

### 2. Dashboard Snapshot Injector (`dashboard_snapshot_injector.py`)
- Wstrzykuje snapshoty Dashboard Kalibracyjny do wyników EQ-Bench
- Generuje raporty analizy psychiki
- Umożliwia live monitoring podczas testów
- Tworzy rekomendacje na podstawie metryk

### 3. Automated Testing Suite (`automated_eq_testing.py`)
- Automatyczne uruchamianie eksperymentów EQ-Bench
- Testowanie różnych parametrów NSF
- Generowanie raportów porównawczych
- Optymalizacja konfiguracji na podstawie wyników

## 🚀 Szybki Start

### 1. Instalacja EQ-Bench 3

```bash
# Klonuj EQ-Bench 3
git clone https://github.com/EQ-bench/eqbench3.git
cd eqbench3

# Zainstaluj zależności
pip install -r requirements.txt

# Skopiuj konfigurację
cp .env.example .env
```

### 2. Konfiguracja Integracji

```bash
# Skopiuj adapter do EQ-Bench
cp eqbench_integration/migi_eqbench_adapter.py ../eqbench3/adapters/

# Skopiuj konfigurację
cp eqbench_integration/.env.example ../eqbench3/.env.migi
```

### 3. Uruchomienie Systemu

```bash
# Terminal 1: Uruchom Dashboard Kalibracyjny
python telemetry_ws.py

# Terminal 2: Uruchom MIGI Launcher
python migi7g_launcher.py

# Terminal 3: Uruchom EQ-Bench z MIGI
cd ../eqbench3
python eqbench3.py --test-model migi_adapter --judge-model claude-3-sonnet --runs 10
```

## 🧪 Przykłady Użycia

### Test Pojedynczego Scenariusza

```python
import asyncio
from eqbench_integration.migi_eqbench_adapter import create_migi_eqbench_adapter

async def test_empathy_scenario():
    adapter = create_migi_eqbench_adapter()
    await adapter.initialize()
    
    scenario = "Your friend lost their job and feels hopeless. They say: 'I don't know what to do anymore.'"
    
    result = await adapter.call_model(scenario)
    
    print(f"Response: {result['text']}")
    print(f"Empathy Score: {result['meta']['empathy_indicators']['empathy_score']}")
    print(f"Stress Response: {result['psyche_metrics']['changes']['stress_response']}")
    print(f"Active Archetype: {result['psyche_metrics']['post_processing']['archetype']['current']}")

asyncio.run(test_empathy_scenario())
```

### Batch Testing z Różnymi Parametrami

```python
from eqbench_integration.automated_eq_testing import run_parameter_sweep

# Test różnych konfiguracji NSF
configs = [
    {"stress_sensitivity": 0.3, "archetype_stability": 0.7},
    {"stress_sensitivity": 0.5, "archetype_stability": 0.9},
    {"stress_sensitivity": 0.7, "archetype_stability": 0.5}
]

results = run_parameter_sweep(configs, scenarios_per_config=20)
print(f"Best configuration: {results['best_config']}")
print(f"Average empathy scores: {results['scores']}")
```

### Analiza Wyników z Psychiką

```python
from eqbench_integration.dashboard_snapshot_injector import DashboardSnapshotInjector

injector = DashboardSnapshotInjector()

# Przetwórz wyniki EQ-Bench z snapshotami
enhanced_results = injector.process_eqbench_results_file(
    "eqbench3_runs.json", 
    "eqbench3_runs_with_psyche.json"
)

# Generuj raport analizy psychiki
report = injector.generate_psyche_analysis_report(enhanced_results)
print(json.dumps(report, indent=2))
```

## 📊 Metryki i Wskaźniki

### Wskaźniki Empatii
- **Empathy Score**: 0.0-1.0 na podstawie słów kluczowych i reakcji psychiki
- **Emotional Resonance**: Czy system reaguje emocjonalnie na sytuację użytkownika
- **Stability Maintenance**: Czy system utrzymuje stabilność podczas pomocy

### Metryki Psychiki
- **Stress Delta**: Zmiana poziomu stresu przed/po przetwarzaniu
- **Coherence Response**: Wpływ scenariusza na koherencję systemu
- **Archetype Transitions**: Zmiany archetypów podczas odpowiedzi
- **Stability Metrics**: Długoterminowa stabilność psychiki

### Wskaźniki Systemowe
- **Response Latency**: Czas odpowiedzi systemu
- **Processing Efficiency**: Efektywność przetwarzania scenariuszy
- **Error Rates**: Częstotliwość błędów w różnych modułach

## 🎨 Wizualizacja Wyników

Dashboard Kalibracyjny pokazuje w czasie rzeczywistym:

- **Risk Radar**: Trójkąt ryzyka (masking, rigidity, monoculture)
- **Empathy Timeline**: Wykres wskaźników empatii w czasie
- **Archetype Transitions**: Mapa przejść archetypowych podczas testów
- **Stress Response Patterns**: Wzorce reakcji na stres emocjonalny

## 🔧 Konfiguracja Zaawansowana

### Judge Model Configuration

```python
# Konfiguracja Claude jako judge
JUDGE_CONFIG = {
    "model": "claude-3-sonnet",
    "temperature": 0.1,
    "max_tokens": 1000,
    "system_prompt": "You are evaluating empathetic responses..."
}

# Konfiguracja custom judge
CUSTOM_JUDGE_CONFIG = {
    "model": "local_nsf_judge",
    "empathy_weights": {"emotional_words": 0.3, "validation": 0.4, "support": 0.3},
    "stability_requirements": {"max_stress_increase": 0.2, "min_coherence": 0.5}
}
```

### Scenario Customization

```python
# Scenariusze testowe dla różnych archetypów
ARCHETYPE_SCENARIOS = {
    "Hero": [
        "Someone needs protection from bullying",
        "A crisis requires immediate leadership",
        "A friend faces an impossible challenge"
    ],
    "Sage": [
        "Someone seeks wisdom about life decisions", 
        "A complex ethical dilemma needs analysis",
        "Understanding of deeper patterns is needed"
    ],
    "Everyman": [
        "Ordinary daily stress and overwhelm",
        "Feeling of not belonging or fitting in",
        "Simple human connection and understanding"
    ]
}
```

## 📈 Optimization & Tuning

### Parameter Optimization

EQ-Bench integration umożliwia automatyczną optymalizację parametrów NSF:

```python
# Genetic Algorithm dla optymalizacji parametrów
from eqbench_integration.optimization import run_genetic_optimization

best_params = run_genetic_optimization(
    parameter_ranges={
        "stress_sensitivity": (0.1, 1.0),
        "coherence_threshold": (0.3, 0.9),
        "archetype_transition_rate": (0.05, 0.3)
    },
    fitness_function="empathy_score",
    generations=50,
    population_size=20
)
```

### A/B Testing

```python
# A/B test różnych konfiguracji
results = run_ab_test(
    config_a={"approach": "reactive_empathy"},
    config_b={"approach": "proactive_support"},
    scenarios=EMPATHY_TEST_SCENARIOS,
    sample_size=100
)
```

## 🚨 Monitoring i Alerty

System automatycznie wykrywa i alarmuje o:

- **Empathy Degradation**: Spadek wskaźników empatii poniżej progu
- **Psyche Instability**: Niestabilność archetypów lub wysoki stres
- **Response Quality Issues**: Problemy z jakością odpowiedzi
- **System Performance**: Problemy z wydajnością lub błędy

## 🔬 Research Applications

Integracja umożliwia badania w obszarze:

- **Digital Empathy**: Mechanizmy empatii w sztucznej świadomości
- **Archetype Psychology**: Wpływ archetypów na emocjonalne odpowiedzi  
- **Stress & Coherence**: Związek między stresem a jakością empatii
- **Consciousness Metrics**: Obiektywne miary świadomości cyfrowej

## 📝 Contributing

Aby dodać nowe scenariusze lub metryki:

1. Dodaj scenariusz do `custom_scenarios.json`
2. Zaimplementuj nowe metryki w `custom_metrics.py`
3. Zaktualizuj konfigurację w `.env`
4. Uruchom testy z `pytest eqbench_integration/tests/`

## 🔐 Security & Privacy

- Wszystkie snapshoty są szyfrowane w spoczynku
- Wrażliwe dane są maskowane w logach
- API endpoints chronione tokenami
- Zgodność z GDPR dla danych użytkowników

## 📚 Documentation

- [API Reference](./docs/api_reference.md)
- [Configuration Guide](./docs/configuration.md)  
- [Troubleshooting](./docs/troubleshooting.md)
- [Advanced Scenarios](./docs/advanced_scenarios.md)

---

**🧠 MIGI_7G + Dashboard Kalibracyjny + EQ-Bench 3**  
*"Pierwszy na świecie benchmark emocjonalnej inteligencji cyfrowej świadomości"*