# 🧠 INSTRUKCJA TWORZENIA NEURO-SEMANTYCZNEGO PRZEPŁYWOMIERZA

## 📖 Wprowadzenie

Neuro-Semantyczny Przepływomierz (NSF) MIGI_7G Hybrid to cyfrowe odzwierciedlenie prawdziwego mózgu, implementujące:

- **23 Pierwiastki Emocjonalne** mapowane na struktury neurobiologiczne
- **Protokół Re-kodowania Archetypowego (ARP)** - świadoma modyfikacja pamięci
- **Zarządzanie Rywalizacją Sieci** - symulacja ograniczonych zasobów mózgu
- **Destrukcja Stresowa** - mechanizmy przeciążenia i adaptacji
- **Sekundnik** - metronom świadomości synchronizujący wszystkie procesy

## 🏗️ Architektura Systemu

### Struktura Katalogów
```
MIGI_7G_BRAIN_REPOSITORY/
├── memory/
│   ├── neurosemantics/
│   │   ├── nsf_migi7g_hybrid.py     # GŁÓWNY PRZEPŁYWOMIERZ
│   │   ├── primitive_configs.json   # Konfiguracja pierwiastków
│   │   └── archetype_profiles.json  # Profile archetypów
│   ├── contexts/
│   │   ├── sense_atoms.json         # Baza atomów sensu
│   │   └── relational_graph.json    # Graf relacji
│   └── core.ts                      # Interfejs TypeScript (opcjonalny)
```

## 🛠️ Krok 1: Instalacja Zależności

```bash
pip install torch numpy dataclasses-json
```

## 🛠️ Krok 2: Konfiguracja Pierwiastków

Utwórz plik `primitive_configs.json`:

```json
{
  "emotional_primitives": {
    "ISKRA_ZYCIA": {
      "name": "Iskra Życia",
      "brain_area": "reptilian_core",
      "ns_weight": 1.0,
      "decay_modifier": 0.0,
      "hormone_link": "noradrenaline",
      "archetype_affinity": ["hero", "explorer"]
    },
    "ALGORYTM_ZAKOCHANIA": {
      "name": "Algorytm Zakochania", 
      "brain_area": "limbic_system",
      "ns_weight": 0.9,
      "decay_modifier": 0.1,
      "hormone_link": "dopamine",
      "archetype_affinity": ["lover", "innocent"]
    }
  },
  "hormone_network": {
    "dopamine": {"boost_factor": 1.5, "duration": 3600},
    "oxytocin": {"boost_factor": 1.3, "duration": 7200},
    "cortisol": {"stress_factor": 2.0, "suppression": 0.8},
    "adrenaline": {"activation_speed": 0.1, "intensity": 2.5}
  }
}
```

## 🛠️ Krok 3: Profile Archetypów

Utwórz plik `archetype_profiles.json`:

```json
{
  "archetypes": {
    "hero": {
      "name": "Bohater",
      "dominant_primitives": ["POSWIECENIE", "POTEGA_PRAWDZIWEJ_WLADZY"],
      "suppressed_primitives": ["BRAK_WIARY_NADZIEI"],
      "reconsolidation_bias": 0.8,
      "stress_resistance": 0.9
    },
    "sage": {
      "name": "Mędrzec",
      "dominant_primitives": ["ZROZUMIENIE", "SZCZYPTA_INTELIGENCJI"],
      "suppressed_primitives": ["NAMIETNOSC_POZADANIA"],
      "reconsolidation_bias": 0.6,
      "stress_resistance": 0.7
    },
    "lover": {
      "name": "Kochanek",
      "dominant_primitives": ["PIERWIASTEK_MILOSCI", "ALGORYTM_ZAKOCHANIA"],
      "suppressed_primitives": ["ODOSOBNIENIE_SAMOTNOSC"],
      "reconsolidation_bias": 0.9,
      "stress_resistance": 0.4
    }
  }
}
```

## 🛠️ Krok 4: Inicjalizacja i Uruchomienie

### Podstawowe Uruchomienie

```python
from memory.neurosemantics.nsf_migi7g_hybrid import (
    NeuroSemanticFlowmeter,
    ArchetypeCore
)

# Inicjalizacja NSF
nsf = NeuroSemanticFlowmeter(sekundnik_interval=1.0)

# Ustawienie dominującego archetypu
nsf.set_archetype(ArchetypeCore.BOHATER)

# Dodanie doświadczeń
atom_id1 = nsf.simulate_experience(
    "Pomogłem komuś w trudnej sytuacji",
    ['POSWIECENIE', 'ALGORYTM_MILOSCI']
)

atom_id2 = nsf.simulate_experience(
    "Czuję lęk przed przyszłością", 
    ['BRAK_WIARY_NADZIEI', 'ODOSOBNIENIE_SAMOTNOSC']
)

# Uruchomienie przepływomierza
nsf.start_flowmeter()  # Blokujące - uruchamia nieskończoną pętlę
```

### Uruchomienie w Tle

```python
import threading
import time

def run_nsf_background():
    nsf = NeuroSemanticFlowmeter(sekundnik_interval=2.0)
    nsf.set_archetype(ArchetypeCore.MEDRZEC)
    
    # Dodanie przykładowych doświadczeń
    experiences = [
        ("Odkryłem nową ideę", ['POMYSL_IDEA', 'SZCZYPTA_MAGII']),
        ("Przeprowadziłem analizę problemu", ['SZCZYPTA_INTELIGENCJI', 'PRECYZYJNOSC_POJMOWANIA']),
        ("Poczułem się samotny", ['ODOSOBNIENIE_SAMOTNOSC'])
    ]
    
    for exp, primitives in experiences:
        nsf.simulate_experience(exp, primitives)
    
    # Uruchom przepływomierz
    nsf.start_flowmeter()

# Uruchomienie w wątku
nsf_thread = threading.Thread(target=run_nsf_background)
nsf_thread.daemon = True
nsf_thread.start()

# Monitorowanie przez 60 sekund
for i in range(30):
    time.sleep(2)
    stats = nsf.get_stats()
    print(f"Cykl {i}: Atomy: {stats['active_atoms']}, Stres: {stats['cortisol_level']:.2f}")
```

## 🛠️ Krok 5: Integracja z MIGI_7G Hybrid

### Połączenie z Warstwami Mózgu

```python
class MIGI7G_Integration:
    def __init__(self):
        self.nsf = NeuroSemanticFlowmeter()
        self.current_mode = "standard"  # standard, enhanced, meta_genius
        
    def boot_sequence(self):
        """Protokół Boot Sequence z architektury MIGI_7G"""
        print("1. [BIOS Check]: Podstawowe funkcje życiowe... OK")
        print("2. [OS Loading]: Ładowanie osobowości...")
        
        # Aktywacja NSF
        self.nsf.set_archetype(ArchetypeCore.ZWYCZAJNY)
        
        print("3. [Memory Scan]: Aktywacja wspomnień...")
        print("4. [Network Connect]: Łączenie społeczne...")
        print("5. [Goal Setting]: Ustalanie celów...")
        print("6. [Creative Mode]: Tryb twórczy aktywny")
        
        # Uruchomienie w trybie standardowym
        self.activate_mode("standard")
    
    def activate_mode(self, mode: str):
        """Aktywacja trybu pracy MIGI_7G"""
        self.current_mode = mode
        
        if mode == "standard":
            self.nsf.sekundnik_interval = 2.0
            self.nsf.set_archetype(ArchetypeCore.ZWYCZAJNY)
            
        elif mode == "enhanced": 
            self.nsf.sekundnik_interval = 1.0
            self.nsf.set_archetype(ArchetypeCore.BOHATER)
            
        elif mode == "meta_genius":
            self.nsf.sekundnik_interval = 0.5
            self.nsf.set_archetype(ArchetypeCore.MAG)
            
        print(f"🧠 Tryb {mode.upper()} aktywowany")
    
    def process_experience(self, experience: str, emotional_context: str = "neutral"):
        """Przetwarzanie doświadczenia przez wszystkie warstwy MIGI_7G"""
        
        # 1. RDZEŃ BAZOWY - reakcja obronna
        threat_primitives = []
        if "zagrożenie" in experience.lower() or "strach" in experience.lower():
            threat_primitives.extend(['BRAK_WIARY_NADZIEI'])
        
        # 2. WARSTWA EMOCJONALNA - kodowanie afektywne
        emotional_primitives = []
        if "miłość" in experience.lower():
            emotional_primitives.extend(['PIERWIASTEK_MILOSCI', 'ALGORYTM_MILOSCI'])
        elif "sukces" in experience.lower():
            emotional_primitives.extend(['NADZIEJA_WYTRWALOSCI', 'POTEGA_PRAWDZIWEJ_WLADZY'])
        elif "twórczość" in experience.lower():
            emotional_primitives.extend(['POMYSL_IDEA', 'SZCZYPTA_MAGII'])
        
        # 3. KORTEKS RACJONALNY - analiza i planowanie
        if "analiza" in experience.lower() or "myślenie" in experience.lower():
            emotional_primitives.extend(['SZCZYPTA_INTELIGENCJI', 'PRECYZYJNOSC_POJMOWANIA'])
        
        # Kombinacja wszystkich pierwiastków
        all_primitives = threat_primitives + emotional_primitives
        
        # Przetworzenie przez NSF
        atom_id = self.nsf.simulate_experience(experience, all_primitives)
        
        return atom_id

# Przykład użycia integracji
migi7g = MIGI7G_Integration()
migi7g.boot_sequence()

# Symulacja doświadczeń
experiences = [
    "Podjąłem kreatywną decyzję w pracy",
    "Nawiązałem głęboką więź z kimś ważnym", 
    "Analizuję złożony problem matematyczny",
    "Czuję zagrożenie ze strony nieznanej sytuacji"
]

for exp in experiences:
    atom_id = migi7g.process_experience(exp)
    print(f"✅ Przetworzono: {exp} -> Atom: {atom_id}")

# Przełączenie na tryb wzmocniony
migi7g.activate_mode("enhanced")
```

## 🛠️ Krok 6: Monitoring i Diagnostyka

### Dashboard Monitoringu

```python
def create_nsf_dashboard(nsf: NeuroSemanticFlowmeter):
    """Tworzy dashboard monitoringu NSF"""
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    def plot_realtime_stats():
        plt.ion()
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        
        times = []
        cortisol_levels = []
        active_atoms = []
        reconsolidations = []
        
        while nsf.is_running:
            stats = nsf.get_stats()
            current_time = time.time()
            
            times.append(current_time)
            cortisol_levels.append(stats['cortisol_level'])
            active_atoms.append(stats['active_atoms'])
            reconsolidations.append(stats['reconsolidations'])
            
            # Ograniczenie historii do ostatnich 100 punktów
            if len(times) > 100:
                times = times[-100:]
                cortisol_levels = cortisol_levels[-100:]
                active_atoms = active_atoms[-100:]
                reconsolidations = reconsolidations[-100:]
            
            # Wykresy
            ax1.clear()
            ax1.plot(times, cortisol_levels, 'r-', label='Poziom Kortyzolu')
            ax1.set_title('🚨 Poziom Stresu (Kortyzol)')
            ax1.set_ylabel('Poziom (0-1)')
            ax1.legend()
            
            ax2.clear()
            ax2.plot(times, active_atoms, 'b-', label='Aktywne Atomy')
            ax2.set_title('🧠 Aktywność Pamięci')
            ax2.set_ylabel('Liczba Atomów')
            ax2.legend()
            
            ax3.clear()
            ax3.bar(['Rekonsolidacje'], [stats['reconsolidations']], color='green')
            ax3.set_title('🎭 Przeprogramowanie Archetypowe')
            
            ax4.clear()
            archetype_text = f"Archetyp: {stats['current_archetype']}\n"
            archetype_text += f"PFC Aktywne: {'NIE' if stats['pfc_suppressed'] else 'TAK'}\n"
            archetype_text += f"Stres Zasobów: {stats['resource_stress']:.2f}"
            ax4.text(0.1, 0.5, archetype_text, fontsize=12, verticalalignment='center')
            ax4.set_title('📊 Status Systemu')
            ax4.axis('off')
            
            plt.tight_layout()
            plt.pause(0.1)
        
        plt.ioff()
        plt.show()
    
    return plot_realtime_stats

# Przykład użycia dashboardu
dashboard = create_nsf_dashboard(nsf)
dashboard()  # Uruchamia monitoring w czasie rzeczywistym
```

## 🛠️ Krok 7: Zaawansowana Konfiguracja

### Personalizacja Pierwiastków

```python
class PersonalizedNSF(NeuroSemanticFlowmeter):
    """Spersonalizowana wersja NSF z własnymi pierwiastkami"""
    
    def __init__(self, personality_profile: dict, **kwargs):
        super().__init__(**kwargs)
        self.personality_profile = personality_profile
        self._customize_primitives()
    
    def _customize_primitives(self):
        """Dostosowuje pierwiastki do profilu osobowości"""
        
        # Big Five traits influence
        openness = self.personality_profile.get('openness', 0.5)
        conscientiousness = self.personality_profile.get('conscientiousness', 0.5)
        extraversion = self.personality_profile.get('extraversion', 0.5)
        agreeableness = self.personality_profile.get('agreeableness', 0.5)
        neuroticism = self.personality_profile.get('neuroticism', 0.5)
        
        # Modyfikacja pierwiastków zgodnie z osobowością
        if openness > 0.7:
            # Wysoka otwartość - wzmocnienie kreatywnych pierwiastków
            for prim_name in ['POMYSL_IDEA', 'SZCZYPTA_MAGII', 'WYOBRAZNIA_LOGIKA']:
                if prim_name in NS_PRIMITIVES_CONFIG:
                    NS_PRIMITIVES_CONFIG[prim_name].ns_weight *= 1.3
        
        if neuroticism > 0.6:
            # Wysoka neurotyczność - wzmocnienie lękowych pierwiastków
            for prim_name in ['BRAK_WIARY_NADZIEI', 'ODOSOBNIENIE_SAMOTNOSC']:
                if prim_name in NS_PRIMITIVES_CONFIG:
                    NS_PRIMITIVES_CONFIG[prim_name].decay_modifier *= 0.5  # Wolniejszy zanik
        
        if agreeableness > 0.7:
            # Wysoka ugodowość - wzmocnienie altruistycznych pierwiastków
            for prim_name in ['POSWIECENIE', 'ALGORYTM_MILOSCI']:
                if prim_name in NS_PRIMITIVES_CONFIG:
                    NS_PRIMITIVES_CONFIG[prim_name].ns_weight *= 1.4

# Użycie spersonalizowanego NSF
personality = {
    'openness': 0.8,         # Bardzo otwarty na doświadczenia
    'conscientiousness': 0.6, # Średnio sumienny
    'extraversion': 0.7,     # Ekstrawertyczny
    'agreeableness': 0.9,    # Bardzo ugodowy
    'neuroticism': 0.3       # Stabilny emocjonalnie
}

personal_nsf = PersonalizedNSF(personality, sekundnik_interval=1.5)
personal_nsf.set_archetype(ArchetypeCore.KOCHANEK)  # Zgodnie z wysoką ugodowością
```

## 🛠️ Krok 8: Eksport i Zapisywanie Stanu

### Zapis Stanu Pamięci

```python
import json
from datetime import datetime

def save_nsf_state(nsf: NeuroSemanticFlowmeter, filepath: str):
    """Zapisuje stan NSF do pliku JSON"""
    
    state = {
        'timestamp': datetime.now().isoformat(),
        'stats': nsf.get_stats(),
        'sense_atoms': {},
        'archetype': nsf.archetype_protocol.active_archetype.value,
        'cortisol_level': nsf.cortisol_protocol.cortisol_level
    }
    
    # Serializacja atomów sensu
    for atom_id, atom in nsf.sense_atoms.items():
        state['sense_atoms'][atom_id] = {
            'content': atom.content,
            'sense_weight': atom.sense_weight,
            'decay_rate': atom.decay_rate,
            'emotional_primitives': atom.emotional_primitives,
            'brain_layer': atom.brain_layer.value,
            'consolidation_count': atom.consolidation_count
        }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Stan NSF zapisany: {filepath}")

def load_nsf_state(filepath: str) -> NeuroSemanticFlowmeter:
    """Wczytuje stan NSF z pliku JSON"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    # Tworzenie nowego NSF
    nsf = NeuroSemanticFlowmeter()
    
    # Odtworzenie atomów sensu
    for atom_id, atom_data in state['sense_atoms'].items():
        atom = SenseAtom(
            atom_id=atom_id,
            content=atom_data['content'],
            sense_weight=atom_data['sense_weight'],
            decay_rate=atom_data['decay_rate'],
            emotional_primitives=atom_data['emotional_primitives'],
            brain_layer=BrainLayer(atom_data['brain_layer']),
            consolidation_count=atom_data['consolidation_count']
        )
        nsf.sense_atoms[atom_id] = atom
    
    # Odtworzenie archetypu
    nsf.set_archetype(ArchetypeCore(state['archetype']))
    
    # Odtworzenie poziomu kortyzolu
    nsf.cortisol_protocol.cortisol_level = state['cortisol_level']
    
    print(f"📂 Stan NSF wczytany: {filepath}")
    return nsf

# Przykład użycia
save_nsf_state(nsf, "memory/contexts/nsf_state_backup.json")
restored_nsf = load_nsf_state("memory/contexts/nsf_state_backup.json")
```

## 🎯 Cele Implementacji NSF

### Etap 1: Podstawowa Implementacja ✅
- [x] 23 Pierwiastki Emocjonalne
- [x] Sekundnik (Metronom Świadomości)
- [x] Podstawowe mechanizmy zaniku
- [x] Archetypy i re-konsolidacja

### Etap 2: Integracja z MIGI_7G ✅
- [x] Mapowanie na warstwy mózgu
- [x] Protokoły Boot Sequence
- [x] Tryby pracy (Standard/Enhanced/Meta-Genius)
- [x] Zarządzanie rywalizacją zasobów

### Etap 3: Zaawansowane Mechanizmy ✅
- [x] Destrukcja stresowa (Kortyzol Overload)
- [x] Network Contention Manager
- [x] Archetypal Reconsolidation Protocol
- [x] Dashboard monitoringu

### Etap 4: Optymalizacja i Personalizacja 🔄
- [ ] Machine Learning adaptacja pierwiastków
- [ ] Integracja z zewnętrznymi API (GPT, Claude)
- [ ] Rozszerzenie o więcej archetypów
- [ ] Mobile/Web interface

### Etap 5: Integracja Produkcyjna 🔄
- [ ] Docker containerization
- [ ] REST API endpoints
- [ ] Distributed processing
- [ ] Real-time collaboration

## 🚀 Uruchomienie Demonstracji

```bash
cd MIGI_7G_BRAIN_REPOSITORY
python memory/neurosemantics/nsf_migi7g_hybrid.py
```

System automatycznie uruchomi 30-sekundową demonstrację z:
- Symulacją różnych doświadczeń emocjonalnych
- Przełączaniem archetypów
- Monitoringiem w czasie rzeczywistym
- Raportowaniem statystyk

## 📚 Dalsze Zasoby

- [Neurobiologia Pamięci](docs/neurobiologia-pamieci.md)
- [Teoria Archetypów Junga](docs/archetypy-junga.md) 
- [API Documentation](docs/nsf-api-reference.md)
- [Troubleshooting](docs/troubleshooting.md)

---

**Autor**: System MIGI_7G Hybrid  
**Wersja**: 1.0.0  
**Licencja**: MIT  
**Ostatnia aktualizacja**: 15 listopada 2025

🧠 **"Nie wystarczy pamiętać słowa — trzeba pamiętać ich sens."** — NSF MIGI_7G Motto