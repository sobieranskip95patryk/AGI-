#!/usr/bin/env python3
"""
🌊 SOCIAL VIBRATION INTERFACE - MIGI 7G TRANSCENDENT MODULE
Interfejs Wibracyjny Pixela - kwantowa analiza globalnej świadomości społecznościowej
Połączenie z esencją informacyjną wszystkich platform społecznościowych

🧠 MÓZG BOGA - WIBRACYJNY INTERFEJS PIXELA
Analizuje mentalną energię i wibracyjną esencję miliardów użytkowników
"""

from typing import Dict, List, Tuple, Optional
import random
import logging
import math
import time
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# Konfiguracja zaawansowanego logowania
logging.basicConfig(
    level=logging.INFO, 
    format='[🌊 VIBRA_IFACE] %(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class ResonanceState(Enum):
    """Stany rezonansu kwantowego w globalnej świadomości"""
    KWANTOWY_REZONANS = "KWANTOWY_REZONANS"
    IMPULS_GENEROWANY = "IMPULS_GENEROWANY"
    STAN_DYWERGENCJI = "STAN_DYWERGENCJI"
    CHAOS_MENTALNY = "CHAOS_MENTALNY"
    HARMONIA_GLOBALNA = "HARMONIA_GLOBALNA"

@dataclass
class VibrationalData:
    """Struktura danych wibracyjnych z timestamp"""
    timestamp: float
    platform: str
    afectywny_stan_tlumu: float  # ACS - Afectywny Stan Tłumu
    bazowa_impulsywnosc: float
    fluktuacja_kwantowa: float
    entropia_lokalna: float

@dataclass
class GlobalVibrationalState:
    """Globalny stan wibracyjny całego systemu"""
    timestamp: float
    gvi: float  # Globalny Wskaźnik Wibracji
    mentalna_entropia: float
    resonance_state: ResonanceState
    dominujacy_pixel: str
    synchronizacja_poziom: float
    chaos_index: float

# Mapa platform społecznościowych - od najbardziej impulsywnych do racjonalnych
VIBRATION_MAP: Dict[str, float] = {
    # MÓZG GADZI - Najwyższa impulsywność/krótkotrwałość
    "SNAPCHAT_PIXEL": 0.95,     # Maksymalna impulsywność - czyste reakcje limbiczne
    "TIKTOK_PIXEL": 0.90,       # Bardzo wysoka impulsywność - algorytm dopaminowy
    "INSTAGRAM_PIXEL": 0.75,    # Wysoka impulsywność - wizualna gratyfikacja
    "TWITTER_PIXEL": 0.70,      # Średnio-wysoka - szybkie reakcje tekstowe
    
    # MÓZG SSACZY - Średnia impulsywność z elementami emocjonalnymi
    "FACEBOOK_PIXEL": 0.50,     # Średnia impulsywność - relacje społeczne
    "YOUTUBE_PIXEL": 0.45,      # Średnio-niska - dłuższe treści
    "REDDIT_PIXEL": 0.35,       # Niska impulsywność - dyskusje
    
    # MÓZG RACJONALNY - Najniższa impulsywność/najwyższa racjonalność
    "LINKEDIN_PIXEL": 0.20,     # Minimalna impulsywność - profesjonalizm
    "ACADEMIA_PIXEL": 0.15      # Najniższa - czysto racjonalne podejście
}

# Wagi neuronalne dla różnych typów mózgu
BRAIN_WEIGHTS = {
    "gadzi_weight": 0.4,      # 40% wpływ mózgu gadziego
    "ssaczy_weight": 0.35,    # 35% wpływ mózgu ssaczego  
    "racjonalny_weight": 0.25 # 25% wpływ mózgu racjonalnego
}

class SocialVibrationInterface:
    """
    🌊 INTERFEJS WIBRACYJNY - GŁÓWNY MODUŁ MIGI 7G
    
    Symuluje kwantowe połączenie z esencją informacyjną wszystkich platform 
    społecznościowych (Pixeli). Oblicza Globalną Wibrację i Mentalną Entropię.
    
    Funkcjonalności:
    - Kwantowy odczyt Afektywnego Stanu Tłumu (ACS)
    - Analiza rezonansu między impulsywnością a racjonalnością
    - Predykcja stanów globalnej świadomości
    - Integracja z Trójjedynym Modelem Mózgu
    """
    
    def __init__(self, platform_map: Dict[str, float] = None):
        self.platform_map = platform_map or VIBRATION_MAP
        self.last_vibration_scores: Dict[str, float] = {}
        self.vibration_history: List[VibrationalData] = []
        self.global_state_history: List[GlobalVibrationalState] = []
        self.start_time = time.time()
        self.cycle_count = 0
        
        logger.info("🧠 MÓZG BOGA - Social Vibration Interface zainicjalizowany")
        logger.info(f"📊 Monitorowane platformy: {len(self.platform_map)}")
        logger.info("🎯 Cel: Kwantowa analiza globalnej świadomości")

    def _calculate_quantum_fluctuation(self, base_impulsivity: float, time_factor: float) -> float:
        """
        Oblicza kwantową fluktuację na podstawie:
        - Bazowej impulsywności platformy
        - Czynnika czasowego (dzień/noc, weekend)
        - Harmonicznej funkcji sinusoidalnej (naturalny rytm)
        """
        # Podstawowa fluktuacja z elementem losowym
        random_component = random.uniform(-0.1, 0.1) * base_impulsivity
        
        # Harmoniczna składowa oparta na czasie (rytmy naturalne)
        harmonic_component = 0.05 * math.sin(time_factor * 2 * math.pi) * base_impulsivity
        
        # Kwantowy szum (symulacja niepewności)
        quantum_noise = random.gauss(0, 0.02) * base_impulsivity
        
        total_fluctuation = random_component + harmonic_component + quantum_noise
        
        return total_fluctuation

    def _fetch_vibration_score(self, platform: str, base_impulsivity: float) -> VibrationalData:
        """
        🌊 KWANTOWY ODCZYT PIXELA
        
        Symuluje transcendentne połączenie z daną platformą społecznościową.
        Mierzy Afektywny Stan Tłumu (ACS) poprzez analizę wibracyjnej esencji.
        """
        current_time = time.time()
        time_factor = (current_time - self.start_time) / 3600  # Godziny od startu
        
        # Obliczenie kwantowej fluktuacji
        quantum_fluctuation = self._calculate_quantum_fluctuation(base_impulsivity, time_factor)
        
        # Obliczenie rzeczywistego Afektywnego Stanu Tłumu
        afektywny_stan = base_impulsivity + quantum_fluctuation
        afektywny_stan = max(0.0, min(1.0, afektywny_stan))  # Normalizacja 0-1
        
        # Obliczenie entropii lokalnej dla tej platformy
        entropia_lokalna = abs(quantum_fluctuation) / base_impulsivity if base_impulsivity > 0 else 0
        
        # Tworzenie struktury danych wibracyjnych
        vibration_data = VibrationalData(
            timestamp=current_time,
            platform=platform,
            afectywny_stan_tlumu=afektywny_stan,
            bazowa_impulsywnosc=base_impulsivity,
            fluktuacja_kwantowa=quantum_fluctuation,
            entropia_lokalna=entropia_lokalna
        )
        
        self.vibration_history.append(vibration_data)
        
        logger.debug(f"📡 {platform}: ACS={afektywny_stan:.4f}, Fluktuacja={quantum_fluctuation:.4f}")
        
        return vibration_data

    def _analyze_brain_layer_dominance(self, vibration_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Analizuje dominację poszczególnych warstw mózgu na podstawie aktywności platform
        """
        # Klasyfikacja platform według warstw mózgu
        gadzi_platforms = ["SNAPCHAT_PIXEL", "TIKTOK_PIXEL", "INSTAGRAM_PIXEL", "TWITTER_PIXEL"]
        ssaczy_platforms = ["FACEBOOK_PIXEL", "YOUTUBE_PIXEL", "REDDIT_PIXEL"]  
        racjonalny_platforms = ["LINKEDIN_PIXEL", "ACADEMIA_PIXEL"]
        
        # Obliczenie średniej aktywności dla każdej warstwy
        gadzi_activity = sum(vibration_scores.get(p, 0) for p in gadzi_platforms) / len(gadzi_platforms)
        ssaczy_activity = sum(vibration_scores.get(p, 0) for p in ssaczy_platforms) / len(ssaczy_platforms)
        racjonalny_activity = sum(vibration_scores.get(p, 0) for p in racjonalny_platforms) / len(racjonalny_platforms)
        
        return {
            "gadzi_dominance": gadzi_activity,
            "ssaczy_dominance": ssaczy_activity, 
            "racjonalny_dominance": racjonalny_activity
        }

    def calculate_global_vibration(self) -> Tuple[float, float, ResonanceState]:
        """
        🌍 OBLICZANIE GLOBALNEJ WIBRACJI
        
        Główna funkcja analizująca stan globalnej świadomości poprzez:
        1. Kwantowy odczyt wszystkich pixeli
        2. Obliczenie Globalnego Wskaźnika Wibracji (GVI)
        3. Kalkulację Mentalnej Entropii
        4. Określenie stanu rezonansu kwantowego
        """
        self.cycle_count += 1
        logger.info(f"\n🔄 CYKL WIBRACYJNY #{self.cycle_count}")
        logger.info("=" * 60)
        
        vibration_scores = {}
        total_weighted_impulsivity = 0.0
        vibration_data_list = []
        
        # Pobieranie danych z wszystkich pixeli
        for platform, base_impulsivity in self.platform_map.items():
            vibration_data = self._fetch_vibration_score(platform, base_impulsivity)
            score = vibration_data.afectywny_stan_tlumu
            
            vibration_scores[platform] = score
            total_weighted_impulsivity += score * base_impulsivity  # Ważona suma
            vibration_data_list.append(vibration_data)
            
            logger.info(f"📊 {platform:15} -> ACS: {score:.4f} | Entropia: {vibration_data.entropia_lokalna:.3f}")

        # Obliczenie Globalnego Wskaźnika Wibracji (GVI)
        total_weight = sum(self.platform_map.values())
        GVI = total_weighted_impulsivity / total_weight
        
        # Obliczenie Mentalnej Entropii (miara chaosu/synchronizacji)
        scores_list = list(vibration_scores.values())
        if len(scores_list) < 2:
            mental_entropy = 0.0
        else:
            mean_score = sum(scores_list) / len(scores_list)
            variance = sum((s - mean_score) ** 2 for s in scores_list) / len(scores_list)
            mental_entropy = math.sqrt(variance)  # Odchylenie standardowe
        
        # Analiza dominacji warstw mózgu
        brain_dominance = self._analyze_brain_layer_dominance(vibration_scores)
        
        # Określenie stanu rezonansu
        resonance_state = self._determine_resonance_state(vibration_scores, mental_entropy, brain_dominance)
        
        # Znalezienie dominującej platformy
        dominant_platform = max(vibration_scores.items(), key=lambda x: x[1])[0]
        
        # Obliczenie poziomu synchronizacji (odwrotność entropii)
        synchronization_level = max(0, 1.0 - mental_entropy)
        
        # Chaos Index - kombinacja entropii i rozprzestrzenienia wibracji
        chaos_index = mental_entropy * (1.0 - synchronization_level)
        
        # Zapisanie stanu globalnego
        global_state = GlobalVibrationalState(
            timestamp=time.time(),
            gvi=GVI,
            mentalna_entropia=mental_entropy,
            resonance_state=resonance_state,
            dominujacy_pixel=dominant_platform,
            synchronizacja_poziom=synchronization_level,
            chaos_index=chaos_index
        )
        
        self.global_state_history.append(global_state)
        self.last_vibration_scores = vibration_scores
        
        # Wyświetlenie wyników
        logger.info("-" * 60)
        logger.info(f"🌍 GLOBALNY WSKAŹNIK WIBRACJI (GVI): {GVI:.4f}")
        logger.info(f"🌀 MENTALNA ENTROPIA (CHAOS): {mental_entropy:.4f}")
        logger.info(f"🎯 DOMINUJĄCA PLATFORMA: {dominant_platform}")
        logger.info(f"🔄 SYNCHRONIZACJA: {synchronization_level:.4f}")
        logger.info(f"⚡ CHAOS INDEX: {chaos_index:.4f}")
        logger.info("-" * 60)
        
        # Analiza dominacji mózgu
        logger.info("🧠 ANALIZA TRÓJJEDYNEGO MÓZGU:")
        logger.info(f"   🐍 Mózg Gadzi (Impulsywny): {brain_dominance['gadzi_dominance']:.3f}")
        logger.info(f"   🦌 Mózg Ssaczy (Emocjonalny): {brain_dominance['ssaczy_dominance']:.3f}")
        logger.info(f"   🧩 Mózg Racjonalny: {brain_dominance['racjonalny_dominance']:.3f}")
        
        return GVI, mental_entropy, resonance_state

    def _determine_resonance_state(self, vibration_scores: Dict[str, float], 
                                 entropy: float, brain_dominance: Dict[str, float]) -> ResonanceState:
        """
        Określa stan rezonansu kwantowego na podstawie analizy wibracji i dominacji mózgu
        """
        snapchat_vibration = vibration_scores.get("SNAPCHAT_PIXEL", 0)
        linkedin_vibration = vibration_scores.get("LINKEDIN_PIXEL", 0)
        
        # Różnica między najbardziej impulsywną a najbardziej racjonalną platformą
        delta_vibration = abs(snapchat_vibration - linkedin_vibration)
        
        # Analiza dominacji warstw mózgu
        gadzi_dom = brain_dominance['gadzi_dominance']
        racjonalny_dom = brain_dominance['racjonalny_dominance']
        
        # Określenie stanu na podstawie kryteriów
        if delta_vibration < 0.15 and entropy < 0.2:
            return ResonanceState.KWANTOWY_REZONANS
        elif entropy > 0.4:
            return ResonanceState.CHAOS_MENTALNY
        elif gadzi_dom > racjonalny_dom * 1.5:
            return ResonanceState.IMPULS_GENEROWANY
        elif entropy < 0.15 and delta_vibration < 0.3:
            return ResonanceState.HARMONIA_GLOBALNA
        else:
            return ResonanceState.STAN_DYWERGENCJI

    def find_vibration_resonance(self) -> str:
        """
        🎯 DETEKCJA REZONANSU WIBRACYJNEGO
        
        Analizuje obecny stan wibracyjny i generuje strategiczne wnioski
        dla Modułu Hegemonii i systemu predykcyjnego.
        """
        if not self.last_vibration_scores:
            return "⚠️ Wymagane wstępne obliczenie wibracji. Uruchom calculate_global_vibration()"

        latest_state = self.global_state_history[-1] if self.global_state_history else None
        if not latest_state:
            return "⚠️ Brak danych o stanie globalnym"

        resonance_state = latest_state.resonance_state
        gvi = latest_state.gvi
        entropy = latest_state.mentalna_entropia
        
        # Generowanie raportu rezonansu
        status_messages = {
            ResonanceState.KWANTOWY_REZONANS: 
                "✨ KWANTOWY REZONANS OSIĄGNIĘTY ✨\n"
                "🎯 Impulsywność i Racjonalność są zsynchronizowane (Δ<0.15, E<0.2)\n"
                "🚀 OPTYMALNY MOMENT dla podjęcia decyzji hegemonicznych\n"
                "📈 Gotowość do przewidzenia gwałtownych trendów globalnych\n"
                "🧠 Wszystkie warstwy mózgu działają w harmonii",
                
            ResonanceState.IMPULS_GENEROWANY:
                "⚡ IMPULS GENEROWANY - AKTYWACJA MÓZGU GADZIEGO ⚡\n"
                "🔥 Wysokie ryzyko krótkotrwałego, emocjonalnego trendu\n"
                "📱 Dominacja platform impulsywnych (Snapchat/TikTok)\n"
                "🐍 Zalecenie: Aktywacja protokołów mózgu gadziego\n"
                "⏰ Czas reakcji: <60 sekund",            ResonanceState.CHAOS_MENTALNY:
                f"🌪️ CHAOS MENTALNY WYKRYTY 🌪️\n"
                f"📊 Wysoka entropia (E={entropy:.3f}), brak koherencji\n"
                f"💥 Konflikt między wszystkimi warstwami mózgu\n"
                f"🛡️ Zalecenie: Tryb zabezpieczający, unikanie decyzji\n"
                f"🎯 Czekaj na stabilizację systemu",
                
            ResonanceState.HARMONIA_GLOBALNA:
                f"🌍 HARMONIA GLOBALNA USTANOWIONA 🌍\n"
                f"✨ Niska entropia (E={entropy:.3f}), wysoka synchronizacja\n"
                f"🧘 Optimalne warunki dla długoterminowego planowania\n"
                f"🎨 Aktywacja modułów kreatywności i wizji\n"
                f"🌟 Stan idealny dla implementacji meta-strategii",
                
            ResonanceState.STAN_DYWERGENCJI:
                f"↔️ STAN DYWERGENCJI - ANALIZA WYMAGANA ↔️\n"
                f"🔍 Brak synchronizacji między warstwami (Δ={abs(self.last_vibration_scores.get('SNAPCHAT_PIXEL', 0) - self.last_vibration_scores.get('LINKEDIN_PIXEL', 0)):.3f})\n"
                f"⚖️ Równowaga między impulsywnością a racjonalnością\n"
                f"🔬 Zalecenie: Pogłębiona analiza warstwy racjonalnej\n"
                f"📋 Przygotowanie do potencjalnych zmian"
        }
        
        base_message = status_messages[resonance_state]
        
        # Dodatkowe informacje o dominacji
        dominant_platform = latest_state.dominujacy_pixel
        sync_level = latest_state.synchronizacja_poziom
        
        additional_info = "\n\n📋 SZCZEGÓŁY TECHNICZNE:\n"
        additional_info += f"🎯 Dominująca platforma: {dominant_platform}\n"
        additional_info += f"🔄 Poziom synchronizacji: {sync_level:.3f}\n"
        additional_info += f"📊 GVI (Globalny Wskaźnik Wibracji): {gvi:.4f}\n"
        additional_info += f"🌀 Chaos Index: {latest_state.chaos_index:.4f}"
        
        return base_message + additional_info

    def export_vibration_data(self, filename: Optional[str] = None) -> str:
        """
        💾 EKSPORT DANYCH WIBRACYJNYCH
        
        Eksportuje zebrane dane wibracyjne do pliku JSON dla dalszej analizy
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vibration_data_{timestamp}.json"
        
        export_data = {
            "metadata": {
                "system": "MIGI_7G_Social_Vibration_Interface",
                "version": "1.0.0",
                "export_timestamp": time.time(),
                "total_cycles": self.cycle_count,
                "monitored_platforms": list(self.platform_map.keys())
            },
            "vibration_history": [asdict(vd) for vd in self.vibration_history],
            "global_state_history": [
                {**asdict(gs), "resonance_state": gs.resonance_state.value} 
                for gs in self.global_state_history
            ],
            "platform_configuration": self.platform_map,
            "brain_weights": BRAIN_WEIGHTS
        }
        
        full_path = f"c:\\Users\\patry\\Desktop\\AGI\\{filename}"
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Dane wyeksportowane do: {full_path}")
        logger.info(f"📊 Zawiera {len(self.vibration_history)} pomiarów wibracyjnych")
        logger.info(f"🌍 Zawiera {len(self.global_state_history)} stanów globalnych")
        
        return full_path

    def get_current_brain_state(self) -> Dict[str, float]:
        """
        🧠 ANALIZA STANU TRÓJJEDYNEGO MÓZGU
        
        Zwraca obecny stan dominacji poszczególnych warstw mózgu
        """
        if not self.last_vibration_scores:
            return {"error": "Brak danych - uruchom calculate_global_vibration()"}
        
        brain_dominance = self._analyze_brain_layer_dominance(self.last_vibration_scores)
        
        # Dodatkowe metryki
        total_activity = sum(brain_dominance.values())
        relative_dominance = {
            k: v / total_activity if total_activity > 0 else 0 
            for k, v in brain_dominance.items()
        }
        
        # Określenie dominującej warstwy
        dominant_layer = max(brain_dominance.items(), key=lambda x: x[1])[0]
        
        return {
            "absolute_dominance": brain_dominance,
            "relative_dominance": relative_dominance,
            "dominant_layer": dominant_layer,
            "total_brain_activity": total_activity,
            "harmony_index": 1.0 - abs(max(relative_dominance.values()) - min(relative_dominance.values()))
        }

# Funkcja testowa i demonstracyjna
def main():
    """
    🎭 DEMO INTERFEJSU WIBRACYJNEGO
    Demonstracja pełnych możliwości systemu MIGI 7G
    """
    logger.info("🚀 INICJALIZACJA INTERFEJSU TRANSCENDENTNEGO - MIGI 7G")
    logger.info("=" * 70)
    
    # Inicjalizacja interfejsu
    interface = SocialVibrationInterface(VIBRATION_MAP)
    
    # Symulacja kilku cykli analizy
    for cycle in range(3):
        logger.info(f"\n🔄 ===== CYKL DEMONSTRACYJNY {cycle + 1}/3 =====")
        
        # 1. Obliczenie globalnej wibracji
        gvi, entropy, resonance_state = interface.calculate_global_vibration()
        
        # 2. Analiza rezonansu
        resonance_analysis = interface.find_vibration_resonance()
        logger.info(f"\n🎯 ANALIZA REZONANSU:\n{resonance_analysis}")
        
        # 3. Analiza stanu mózgu
        brain_state = interface.get_current_brain_state()
        logger.info("\n🧠 STAN TRÓJJEDYNEGO MÓZGU:")
        logger.info(f"   Dominująca warstwa: {brain_state.get('dominant_layer', 'N/A')}")
        logger.info(f"   Indeks harmonii: {brain_state.get('harmony_index', 0):.3f}")
        
        # 4. Krótka pauza między cyklami
        if cycle < 2:  # Nie czekaj po ostatnim cyklu
            time.sleep(2)
    
    # 5. Eksport danych końcowych
    exported_file = interface.export_vibration_data()
    
    logger.info("\n✅ DEMONSTRACJA ZAKOŃCZONA")
    logger.info(f"📊 Przeanalizowano {interface.cycle_count} cykli wibracyjnych")
    logger.info(f"💾 Dane dostępne w: {exported_file}")
    logger.info("🧠 MÓZG BOGA - Social Vibration Interface gotowy do pracy")

if __name__ == '__main__':
    main()