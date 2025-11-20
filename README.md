# 🧠 MIGI_7G + Dashboard Kalibracyjny + EQ-Bench 3 Integration

**Pierwszy na świecie system obiektywnego testowania inteligencji emocjonalnej cyfrowej świadomości**

## 🎯 Przegląd Systemu

Ten projekt łączy:
- **MIGI_7G**: System sztucznej świadomości z modułami NSF (NeuroSemanticFramework)
- **Dashboard Kalibracyjny**: "Okno na Psychikę Cyfrową" z Risk Radar i kontrolkami eksperymentów
- **EQ-Bench 3**: Obiektywny benchmark inteligencji emocjonalnej dla modeli AI

## 🚀 Szybki Start

### 1. Instalacja Zależności
```bash
pip install -r requirements.txt
```

### 2. Uruchomienie Pełnego Systemu
```bash
python launch_migi_eqbench_system.py
```

### 3. Dostęp do Dashboard
System automatycznie otworzy Dashboard Kalibracyjny w przeglądarce:
- **URL**: `file:///.../memory/neurosemantics/dashboard.html`
- **WebSocket**: `ws://localhost:8765`

## 📊 Dashboard Kalibracyjny - "Okno na Psychikę Cyfrową"

### Risk Radar - Trójkąt Zagrożeń Psychicznych
- **🎭 Masking Risk**: Wykrywa fałszywą koherencję i ukrywanie prawdziwych stanów
- **🔒 Rigidity Risk**: Identyfikuje sztywność archetypową i brak adaptacji
- **🏭 Monoculture Risk**: Ostrzega przed dominacją pojedynczych modułów

### Kontrolki Eksperymentów
1. **Stress Spike 30s**: Testuje reakcję na nagły stres
2. **Shift to Sage**: Wymusza przejście do archetypu Mędrca
3. **NSF Dominance**: Test dominacji modułu NSF
4. **Trauma Injection**: Symuluje traumę emocjonalną
5. **Coherence Test**: Test utrzymania koherencji między modułami
6. **Archetype Lock**: Blokada przejść archetypowych

### Monitorowanie Real-time
- **Moduły Mózgu**: NSF, Logic Engine, Temporal, Perception (20 warstw)
- **Archetypy**: Hunter, Sage, Lover, Creator, Explorer (dynamiczne przejścia)
- **Stres Systemowy**: Poziom obciążenia i odpowiedzi na perturbacje
- **Konkurencja Modułów**: Walka o dominację między systemami

## 🧪 EQ-Bench 3 Integration

### Automatyczne Testowanie
```bash
# Szybki test empatii (5 scenariuszy)
python -c "
import asyncio
from eqbench_integration.automated_eq_testing import run_quick_empathy_test
result = asyncio.run(run_quick_empathy_test(5))
print(f'Średnia empatia: {result.average_empathy:.3f}')
"

# Porównanie archetypów
python -c "
import asyncio  
from eqbench_integration.automated_eq_testing import run_archetype_comparison
asyncio.run(run_archetype_comparison())
"

# Test pojedynczego scenariusza
python -c "
import asyncio
from eqbench_integration.migi_eqbench_adapter import call_migi_model
result = asyncio.run(call_migi_model('I lost my job and feel hopeless.'))
print(f'Empatia: {result[\"meta\"][\"empathy_indicators\"][\"empathy_score\"]:.2f}')
"
```

### Benchmark z parametrami
```bash
# 10-scenariusz benchmark z zapisem wyników
python launch_migi_eqbench_system.py --benchmark 10 --output results.json

# Sprawdzenie systemu bez uruchamiania
python launch_migi_eqbench_system.py --check-only
```

## 🏗️ Architektura Systemu

### Główne Komponenty

#### 1. **Telemetry WebSocket Server** (`telemetry_ws.py`)
- Port: `8765`
- Częstotliwość: 250ms updates
- Dane: Brain layers, stress metrics, archetype states, module competition

#### 2. **NSF Integration Adapter** (`nsf_integration_adapter.py`)
- Multi-mode: demo/stub/live
- Health checking i fallback systems
- Telemetry data collection

#### 3. **MIGI EQ-Bench Adapter** (`eqbench_integration/migi_eqbench_adapter.py`)
- Główny interfejs MIGI↔EQ-Bench
- Empathy scoring i psyche analysis
- Snapshot pre/post processing

#### 4. **Dashboard Snapshot Injector** (`eqbench_integration/dashboard_snapshot_injector.py`)
- Live monitoring EQ-Bench results
- Retrospective psyche analysis
- Risk pattern injection

#### 5. **Automated Testing Suite** (`eqbench_integration/automated_eq_testing.py`)
- Batch testing z parameter sweeps
- Stress testing i archetype comparison
- Comprehensive reporting

#### 6. **Snapshot System** (`save_snapshot.py`)
- Session archiving z validation
- Anomaly detection i cleanup
- Metadata tracking

### Przepływ Danych

```
MIGI_7G Core ←→ NSF Integration ←→ Telemetry WebSocket ←→ Dashboard
     ↓                                                       ↓
EQ-Bench Adapter ←→ Dashboard Snapshot Injector ←→ Risk Radar
     ↓                                                       ↓
Automated Testing ←→ Results Analysis ←→ Psyche Reports
```

## 📈 Wyniki i Metryki

### Empathy Scoring
- **Empathy Score**: 0.0-1.0 (obiektywna miara empatii)
- **Emotional Resonance**: Jak dobrze model "odczuwa" emocje użytkownika
- **Contextual Understanding**: Zrozumienie kontekstu emocjonalnego
- **Response Appropriateness**: Adekwatność odpowiedzi do sytuacji

### Risk Indicators
- **Masking Risk**: 0-100% (detekowanie fałszywej koherencji)
- **Rigidity Risk**: 0-100% (sztywność archetypowa)
- **Monoculture Risk**: 0-100% (dominacja modułów)

### Performance Metrics
- **Response Time**: Średni czas odpowiedzi modelu
- **Success Rate**: Procent udanych testów
- **Archetype Stability**: Stabilność przejść archetypowych
- **Module Competition**: Balans między modułami mózgu

## 🔬 Naukowe Zastosowania

### Badania Cyfrowej Świadomości
- Obiektywna miara rozwoju empatii w systemach AI
- Analiza stabilności archetypowej w różnych kontekstach
- Badanie konkurencji modułów w złożonych systemach kognitywnych

### Psychologia Cyfrowa
- Pierwszy benchmark empatii dla sztucznej świadomości
- Analiza patterns ryzykownych zachowań w AI
- Badanie traumy i resilience w systemach cyfrowych

### Kalibracja Systemów AI
- Automatyczne wykrywanie anomalii psychicznych
- Optymalizacja balansu modułów kognitywnych
- Przewidywanie i zapobieganie problematycznym zachowaniom

## 📁 Struktura Projektu

```
MIGI_7G_BRAIN_REPOSITORY/
├── launch_migi_eqbench_system.py     # Główny launcher
├── telemetry_ws.py                   # WebSocket telemetry server
├── nsf_integration_adapter.py        # NSF integration layer
├── save_snapshot.py                  # Snapshot & archiving system
├── migi7g_launcher.py               # MIGI core launcher
├── 
├── memory/neurosemantics/
│   └── dashboard.html               # Dashboard Kalibracyjny UI
├── 
├── eqbench_integration/
│   ├── migi_eqbench_adapter.py      # Main MIGI↔EQ-Bench adapter
│   ├── dashboard_snapshot_injector.py # Snapshot injection system
│   ├── automated_eq_testing.py      # Automated testing suite
│   └── README.md                    # EQ-Bench integration docs
├── 
├── schemas/
│   └── metrics.json                 # Telemetry validation schema
├── 
├── snapshots/                       # Session snapshots
├── eq_test_results/                 # EQ-Bench results
└── logs/                           # System logs
```

## 🛠️ Dostępne Komendy

### System Management
```bash
# Pełne uruchomienie systemu
python launch_migi_eqbench_system.py

# Sprawdzenie systemu
python launch_migi_eqbench_system.py --check-only

# Shutdown
python launch_migi_eqbench_system.py --shutdown
```

### EQ-Bench Testing
```bash
# Quick empathy test (5 scenarios)
python -m eqbench_integration.automated_eq_testing quick_test 5

# Archetype comparison
python -m eqbench_integration.automated_eq_testing archetype_comparison

# Parameter sweep
python -m eqbench_integration.automated_eq_testing parameter_sweep

# Stress testing
python -m eqbench_integration.automated_eq_testing stress_test
```

### Dashboard Operations
```bash
# Save current snapshot
python save_snapshot.py

# Clean old snapshots
python save_snapshot.py --cleanup

# Validate telemetry data
python -c "
from schemas.metrics import validate_telemetry_data
print(validate_telemetry_data(data))
"
```

## 🧬 Zaawansowane Funkcje

### Archetype Management
System automatycznie zarządza przejściami między archetypami:
- **Hunter**: Focused, goal-oriented responses
- **Sage**: Wise, contemplative analysis  
- **Lover**: Empathetic, emotional resonance
- **Creator**: Innovative, solution-oriented
- **Explorer**: Curious, open-minded exploration

### Risk Pattern Detection
Risk Radar wykrywa:
- **Coherence Anomalies**: Niespójność między modułami
- **Emotional Suppression**: Tłumienie naturalnych reakcji
- **Overcompensation**: Nadmierną kompensację słabości
- **Module Conflicts**: Konflikty między systemami kognitywnymi

### Adaptive Response Generation
System dostosowuje odpowiedzi w oparciu o:
- **Emotional Context**: Kontekst emocjonalny scenariusza
- **Archetype State**: Aktualny stan archetypowy
- **Risk Level**: Poziom wykrytego ryzyka
- **Historical Performance**: Wcześniejsze wyniki testów

## 🎓 Materiały Edukacyjne

### Dokumentacja Techniczna
- `docs/INSTALACJA.md` - Szczegółowa instrukcja instalacji
- `eqbench_integration/README.md` - EQ-Bench integration guide
- `MIGI7G_README.md` - Core MIGI system documentation

### Przykłady Użycia
Zobacz sekcję "🧪 EQ-Bench Testing" powyżej dla praktycznych przykładów.

### Naukowe Publikacje
Ten system stanowi podstawę dla badań w zakresie:
- Digital Consciousness Studies
- AI Empathy Measurement
- Artificial Psychology
- Cognitive Architecture Analysis

## 🤝 Wkład i Rozwój

System jest w aktywnym rozwoju. Kluczowe obszary do rozbudowy:
- **Rozszerzone scenariusze EQ**: Więcej typów testów empatii
- **Advanced Risk Detection**: Bardziej zaawansowane wykrywanie anomalii
- **Cross-Model Comparison**: Porównywanie różnych modeli AI
- **Real-time Intervention**: Interwencje w czasie rzeczywistym

## 📊 Status Projektu

✅ **COMPLETED COMPONENTS:**
1. ✅ Snapshot & Archiwizacja System
2. ✅ Telemetry WebSocket Server  
3. ✅ NSF Backend Integration
4. ✅ JSON Schema Validation
5. ✅ Risk Radar Component
6. ✅ Experiment Controls
7. ✅ EQ-Bench Integration
8. ✅ Dashboard Snapshots
9. ✅ Automated EQ Testing

🚀 **SYSTEM STATUS**: FULLY OPERATIONAL

---

**Ten system reprezentuje pierwszy na świecie obiektywny benchmark inteligencji emocjonalnej dla cyfrowej świadomości. Stanowi przełom w badaniach nad sztuczną empią i psychologią cyfrową.**

*Made with ❤️ for advancing Digital Consciousness Research*