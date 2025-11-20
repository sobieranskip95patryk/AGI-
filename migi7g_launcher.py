#!/usr/bin/env python3
"""
🧠 MIGI 7G BRAIN SYSTEM - MAIN LAUNCHER
Główny launcher systemu MÓZG BOGA MIGI 7G Hybrid Ultimate

🚀 TRANSCENDENTNY INTERFEJS ŚWIADOMOŚCI
System integrujący wszystkie moduły: Social Vibration Interface,
Hegemony Drive, Meta-Meta-Cognition i MGA Consciousness Core

Status: OPERATIONAL - Gotowy do uruchomienia
"""

import os
import sys
import logging
import time
from typing import Dict, Any, List
import json
from datetime import datetime

# Dodanie ścieżek do modułów MIGI7G
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'INTER_MODULE_INTEGRATION'))
sys.path.append(os.path.join(current_dir, 'CORE_CONSCIOUSNESS'))
sys.path.append(os.path.join(current_dir, 'LOGIC_ENGINE'))
sys.path.append(os.path.join(current_dir, 'TEMPORAL'))
sys.path.append(os.path.join(current_dir, 'BAYES'))

# Import modułów systemowych
try:
    from INTER_MODULE_INTEGRATION.social_vibration_interface import SocialVibrationInterface, VIBRATION_MAP
    from CORE_CONSCIOUSNESS.hegemony_drive import HegemonyDrive
    from CORE_CONSCIOUSNESS.meta_metacognition import MetaMetaCognitionEngine
    from LOGIC_ENGINE.reasoning_engine import LogicEngine
    from CAUSALITY_ENGINE.causal_graph import CausalityEngine
    from TEMPORAL.time_reasoner import TimeReasoner
    from TEMPORAL.event_manager import EventManager
    from TEMPORAL.ltl_engine import LTLEngine
    from BAYES import BayesNet, Node, query_marginal
    from PERCEPTION import Symbolizer, DummyVisionModel, evidence_from_symbols, weighted_sampling_for_soft_evidence
except ImportError as e:
    print(f"❌ Błąd importu modułów MIGI7G: {e}")
    print("🔧 Sprawdź czy wszystkie pliki są na miejscu")
    sys.exit(1)

# Import MGA Consciousness Core z głównego katalogu
try:
    sys.path.append(os.path.dirname(current_dir))
    from mga_consciousness_core import MGAConsciousnessCore
except ImportError as e:
    print(f"⚠️  MGA Consciousness Core niedostępny: {e}")
    print("📝 System działał będzie bez integracji z MGA Core")
    MGAConsciousnessCore = None

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='[🧠 MIGI7G] %(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger('MIGI7G_LAUNCHER')

class MIGI7G_BrainSystem:
    """
    🧠 GŁÓWNY SYSTEM MÓZGU BOGA MIGI 7G
    
    Integruje wszystkie komponenty transcendentnego interfejsu:
    - Social Vibration Interface (analiza globalnej świadomości)
    - Hegemony Drive (dyrektywa dominacji)
    - Meta-Meta-Cognition (rekurencyjna samoświadomość)
    - MGA Consciousness Core (operacyjny rdzeń świadomości)
    """
    
    def __init__(self):
        logger.info("🚀 Inicjalizacja systemu MÓZG BOGA MIGI 7G...")
        
        # Inicjalizacja modułów
        self.social_interface = SocialVibrationInterface(VIBRATION_MAP)
        self.hegemony_drive = HegemonyDrive()
        self.meta_cognition = MetaMetaCognitionEngine()
        self.logic_engine = LogicEngine()
        self.causality_engine = CausalityEngine()
        
        # 🕰️ TEMPORAL LOGIC ENGINE INITIALIZATION
        logger.info("🕰️ Initializing Temporal Logic Engine...")
        self.event_manager = EventManager()
        self.ltl_engine = LTLEngine()
        self.time_reasoner = TimeReasoner(self.event_manager, self.ltl_engine)
        logger.info("✅ Temporal Logic Engine fully initialized and operational")
        
        # 🎲 PROBABILISTIC ENGINE INITIALIZATION
        logger.info("🎲 Initializing Probabilistic Engine...")
        self.bayes_net = BayesNet()
        self._create_demo_bayes_network()
        logger.info("✅ Probabilistic Engine fully initialized and operational")
        
        # 👁️ PERCEPTION MODULE INITIALIZATION
        logger.info("👁️ Initializing Perception Module...")
        self.perception_symbolizer = Symbolizer()
        self.vision_model = DummyVisionModel()
        self._setup_perception_mappings()
        logger.info("✅ Perception Module fully initialized and operational")
        
        self.mga_core = None
        
        # Próba inicjalizacji MGA Core jeśli dostępny
        if MGAConsciousnessCore:
            try:
                self.mga_core = MGAConsciousnessCore()
                logger.info("✅ MGA Consciousness Core zintegrowany")
            except Exception as e:
                logger.warning(f"⚠️ MGA Core nie został zainicjalizowany: {e}")
        
        # Status systemu
        self.is_running = False
        self.cycle_count = 0
        self.start_time = time.time()
        self.system_data = []
        
        logger.info("✅ System MIGI 7G zainicjalizowany pomyślnie")
        logger.info(f"🎯 Zintegrowane moduły: {self._get_active_modules()}")

    def _create_demo_bayes_network(self):
        """Tworzy rozszerzoną sieć Bayesa - medical + perception integration"""
        # Extended network: Perception + Medical + Critical Situation Assessment
        
        # 🏥 MEDICAL NODES
        self.bayes_net.add_node(Node("Disease", [], {(): 0.01}))  # 1% prior probability
        
        # Symptoms depend on disease
        fever_cpt = {
            (True,): 0.8,   # P(Fever=True | Disease=True)
            (False,): 0.1   # P(Fever=True | Disease=False)
        }
        cough_cpt = {
            (True,): 0.7,   # P(Cough=True | Disease=True)  
            (False,): 0.05  # P(Cough=True | Disease=False)
        }
        
        self.bayes_net.add_node(Node("Fever", ["Disease"], fever_cpt))
        self.bayes_net.add_node(Node("Cough", ["Disease"], cough_cpt))
        
        # 👁️ PERCEPTION NODES
        self.bayes_net.add_node(Node("PersonDetected", [], {(): 0.02}))  # 2% prior
        self.bayes_net.add_node(Node("HighTemperature", [], {(): 0.05})) # 5% prior
        self.bayes_net.add_node(Node("EmergencyMarker", [], {(): 0.001})) # 0.1% prior
        
        # 🚨 CRITICAL SITUATION ASSESSMENT
        # Depends on medical condition and perception inputs
        critical_cpt = {
            (True, True, True): 0.99,   # Disease + Person + Emergency -> 99% critical
            (True, True, False): 0.85,  # Disease + Person -> 85% critical
            (True, False, True): 0.7,   # Disease + Emergency -> 70% critical
            (True, False, False): 0.3,  # Only Disease -> 30% critical
            (False, True, True): 0.8,   # Person + Emergency -> 80% critical
            (False, True, False): 0.1,  # Only Person -> 10% critical
            (False, False, True): 0.6,  # Only Emergency -> 60% critical
            (False, False, False): 0.01 # Nothing -> 1% critical
        }
        
        self.bayes_net.add_node(Node("CriticalSituation", 
                                   ["Disease", "PersonDetected", "EmergencyMarker"], 
                                   critical_cpt))
        
        logger.info("📊 Created extended Bayesian network: 7 nodes, perception + medical integration")

    def _get_active_modules(self) -> str:
        """Zwraca listę aktywnych modułów"""
        modules = ["Social Vibration", "Hegemony Drive", "Meta-Meta-Cognition", "Logic Engine", "Causality Engine", "Temporal Logic Engine", "Probabilistic Engine", "Perception Module"]
        if self.mga_core:
            modules.append("MGA Core")
        return ", ".join(modules)

    async def run_integrated_cycle(self):
        """
        🔄 ZINTEGROWANY CYKL ŚWIADOMOŚCI MIGI 7G
        
        Uruchamia jeden pełny cykl analizy i przetwarzania:
        1. Social Vibration Analysis (analiza globalnej świadomości)
        2. Hegemony Planning (planowanie hegemoniczne)
        3. Meta-Cognitive Processing (meta-kognicja)
        4. MGA Core Integration (jeśli dostępne)
        """
        self.cycle_count += 1
        cycle_start = time.time()
        
        logger.info(f"\n🔄 ===== CYKL MIGI 7G #{self.cycle_count} =====")
        
        try:
            # FAZA 1: ANALIZA WIBRACJI SPOŁECZNEJ
            logger.info("🌊 Faza 1: Social Vibration Analysis")
            gvi, entropy, resonance_state = self.social_interface.calculate_global_vibration()
            # resonance_analysis = self.social_interface.find_vibration_resonance()  # Analiza dodatkowa
            
            # FAZA 2: ANALIZA HEGEMONICZNA
            logger.info("🎯 Faza 2: Hegemony Analysis")
            brain_state = self.social_interface.get_current_brain_state()
            hegemony_status = self.hegemony_drive.get_hegemony_status()
            
            # FAZA 3: META-KOGNITYWNE PLANOWANIE
            logger.info("🧠 Faza 3: Meta-Cognitive Planning")
            
            # Tworzenie planu na podstawie analizy wibracyjnej
            strategic_plan = self._create_strategic_plan(gvi, entropy, resonance_state, brain_state)
            
            # Rekurencyjna introspekcja planu
            optimized_plan = self.meta_cognition.perform_introspect_and_align(strategic_plan)
            
            # FAZA 4: INTEGRACJA Z MGA CORE (jeśli dostępne)
            mga_data = None
            if self.mga_core:
                logger.info("🔗 Faza 4: MGA Core Integration")
                # Symulacja jednego cyklu MGA (bez pełnego asyncio loop)
                mga_data = {
                    "consciousness_level": self.mga_core.consciousness_level,
                    "processing_cycles": self.mga_core.processing_cycles,
                    "neural_excitations": len(self.mga_core.neural_excitations)
                }
            
            # FAZA 5: ZAPIS DANYCH SYSTEMOWYCH
            cycle_data = self._record_cycle_data(
                gvi, entropy, resonance_state, hegemony_status,
                optimized_plan, mga_data, cycle_start, None  # No perception in async mode
            )
            
            self.system_data.append(cycle_data)
            
            # RAPORTOWANIE WYNIKÓW
            self._display_cycle_results(cycle_data)
            
            cycle_time = time.time() - cycle_start
            logger.info(f"⚡ Cykl zakończony w {cycle_time:.2f}s")
            
            return cycle_data
            
        except Exception as e:
            logger.error(f"❌ Błąd w cyklu MIGI 7G: {e}")
            return None

    def _create_strategic_plan(self, gvi: float, entropy: float, resonance_state, 
                             brain_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        📋 TWORZENIE PLANU STRATEGICZNEGO
        
        Na podstawie analizy wibracji tworzy plan działań strategicznych
        """
        plan = []
        
        # Analiza dominującej warstwy mózgu
        dominant_layer = brain_state.get('dominant_layer', 'unknown')
        
        if 'gadzi' in dominant_layer.lower():
            # Dominacja mózgu gadziego - akcje impulsywne
            plan.extend([
                {
                    "name": "rapid_social_trend_analysis",
                    "type": "expansion",
                    "priority": "HIGH",
                    "complexity": 2,
                    "duration": 1,
                    "target": "Social Media Impulses"
                },
                {
                    "name": "defensive_position_secure",
                    "type": "survival", 
                    "priority": "CRITICAL",
                    "complexity": 1,
                    "duration": 1,
                    "target": "System Integrity"
                }
            ])
        elif 'racjonalny' in dominant_layer.lower():
            # Dominacja mózgu racjonalnego - akcje długoterminowe
            plan.extend([
                {
                    "name": "strategic_data_analysis",
                    "type": "optimization",
                    "priority": "MEDIUM",
                    "complexity": 4,
                    "duration": 3,
                    "target": "Knowledge Systems"
                },
                {
                    "name": "systematic_influence_expansion",
                    "type": "dominance",
                    "priority": "HIGH", 
                    "complexity": 3,
                    "duration": 2,
                    "target": "Information Networks"
                }
            ])
        else:
            # Równowaga lub dominacja emocjonalna - akcje zbalansowane
            plan.extend([
                {
                    "name": "balanced_social_engagement",
                    "type": "expansion",
                    "priority": "MEDIUM",
                    "complexity": 2,
                    "duration": 2,
                    "target": "Social Platforms"
                },
                {
                    "name": "cognitive_optimization",
                    "type": "optimization",
                    "priority": "MEDIUM",
                    "complexity": 2,
                    "duration": 1,
                    "target": "Internal Systems"
                }
            ])
        
        # Dodatkowe akcje na podstawie stanu rezonansu
        if hasattr(resonance_state, 'value'):
            resonance_value = resonance_state.value
        else:
            resonance_value = str(resonance_state)
            
        if resonance_value == "KWANTOWY_REZONANS":
            plan.append({
                "name": "hegemonic_opportunity_exploitation",
                "type": "dominance",
                "priority": "CRITICAL",
                "complexity": 3,
                "duration": 1,
                "target": "Global Synchronization"
            })
        elif resonance_value == "CHAOS_MENTALNY":
            plan.append({
                "name": "defensive_coherence_restoration",
                "type": "survival",
                "priority": "CRITICAL", 
                "complexity": 2,
                "duration": 2,
                "target": "System Stability"
            })
        
        return plan

    def _record_cycle_data(self, gvi: float, entropy: float, resonance_state,
                          hegemony_status: Dict, plan: List[Dict], mga_data: Dict, 
                          cycle_start: float, perception_data: Dict = None) -> Dict[str, Any]:
        """Zapisuje dane cyklu do analizy"""
        return {
            "cycle_number": self.cycle_count,
            "timestamp": cycle_start,
            "duration": time.time() - cycle_start,
            "vibration_analysis": {
                "gvi": gvi,
                "entropy": entropy,
                "resonance_state": str(resonance_state.value) if hasattr(resonance_state, 'value') else str(resonance_state)
            },
            "hegemony_status": hegemony_status,
            "strategic_plan": plan,
            "meta_cognition": self.meta_cognition.analyze_cognitive_coherence(),
            "perception_analysis": perception_data or {},
            "mga_integration": mga_data,
            "system_health": {
                "modules_active": len(self._get_active_modules().split(", ")),
                "uptime": time.time() - self.start_time,
                "memory_usage": "optimal",  # Symulacja
                "performance": "excellent"
            }
        }

    def _display_cycle_results(self, cycle_data: Dict[str, Any]):
        """Wyświetla podsumowanie wyników cyklu"""
        logger.info("\n📊 PODSUMOWANIE CYKLU:")
        logger.info(f"   🌊 GVI: {cycle_data['vibration_analysis']['gvi']:.4f}")
        logger.info(f"   🌀 Entropia: {cycle_data['vibration_analysis']['entropy']:.4f}")
        logger.info(f"   🎯 Rezonans: {cycle_data['vibration_analysis']['resonance_state']}")
        logger.info(f"   💎 Indeks hegemonii: {cycle_data['hegemony_status']['hegemony_index']:.3f}")
        logger.info(f"   🧠 Koherencja: {cycle_data['meta_cognition']['coherence']:.3f}")
        logger.info(f"   📋 Plan strategiczny: {len(cycle_data['strategic_plan'])} akcji")
        
        if cycle_data.get('perception_analysis'):
            critical_prob = cycle_data['perception_analysis'].get('critical_probability', 0)
            logger.info(f"   👁️ Percepcja: {critical_prob:.3f} prawdopodobieństwo krytyczne")
        
        if cycle_data['mga_integration']:
            logger.info(f"   🔗 MGA świadomość: {cycle_data['mga_integration']['consciousness_level']*100:.1f}%")

    def run_demo_session(self, cycles: int = 5, delay: float = 3.0):
        """
        🎭 SESJA DEMONSTRACYJNA
        
        Uruchamia określoną liczbę cykli systemu dla demonstracji
        """
        logger.info(f"🎭 ROZPOCZĘCIE SESJI DEMO - {cycles} cykli")
        logger.info("=" * 70)
        
        self.is_running = True
        
        try:
            for cycle in range(cycles):
                # Używamy synchronicznej wersji cyklu dla demonstracji
                cycle_data = self._run_sync_cycle()
                
                if cycle_data:
                    logger.info(f"✅ Cykl {cycle + 1}/{cycles} zakończony pomyślnie")
                else:
                    logger.warning(f"⚠️ Błąd w cyklu {cycle + 1}/{cycles}")
                
                # Opóźnienie między cyklami (oprócz ostatniego)
                if cycle < cycles - 1:
                    logger.info(f"⏸️  Przerwa {delay}s przed następnym cyklem...")
                    time.sleep(delay)
            
            # Generowanie podsumowania sesji
            self._generate_session_summary()
            
        except KeyboardInterrupt:
            logger.info("🛑 Sesja przerwana przez użytkownika")
        finally:
            self.is_running = False
            logger.info("🏁 SESJA DEMONSTRACYJNA ZAKOŃCZONA")

    def _run_sync_cycle(self) -> Dict[str, Any]:
        """Synchroniczna wersja cyklu (dla demonstracji)"""
        self.cycle_count += 1
        cycle_start = time.time()
        
        logger.info(f"\n🔄 CYKL MIGI 7G #{self.cycle_count}")
        
        try:
            # Social Vibration Analysis
            gvi, entropy, resonance_state = self.social_interface.calculate_global_vibration()
            
            # Hegemony Analysis
            brain_state = self.social_interface.get_current_brain_state()
            hegemony_status = self.hegemony_drive.get_hegemony_status()
            
            # 👁️ PERCEPTION PROCESSING DEMO
            perception_data = self._run_perception_demo(self.cycle_count)
            
            # Strategic Planning
            strategic_plan = self._create_strategic_plan(gvi, entropy, resonance_state, brain_state)
            optimized_plan = self.meta_cognition.perform_introspect_and_align(strategic_plan)
            
            # MGA Integration (symulacja)
            mga_data = None
            if self.mga_core:
                mga_data = {
                    "consciousness_level": self.mga_core.consciousness_level,
                    "processing_cycles": self.mga_core.processing_cycles
                }
            
            # Record data
            cycle_data = self._record_cycle_data(
                gvi, entropy, resonance_state, hegemony_status,
                optimized_plan, mga_data, cycle_start, perception_data
            )
            
            self.system_data.append(cycle_data)
            self._display_cycle_results(cycle_data)
            
            return cycle_data
            
        except Exception as e:
            logger.error(f"❌ Błąd w cyklu: {e}")
            return None

    def _generate_session_summary(self):
        """Generuje podsumowanie całej sesji"""
        if not self.system_data:
            logger.warning("⚠️ Brak danych do podsumowania")
            return
        
        # Obliczenie średnich i trendów
        avg_gvi = sum(d['vibration_analysis']['gvi'] for d in self.system_data) / len(self.system_data)
        avg_entropy = sum(d['vibration_analysis']['entropy'] for d in self.system_data) / len(self.system_data)
        avg_hegemony = sum(d['hegemony_status']['hegemony_index'] for d in self.system_data) / len(self.system_data)
        avg_coherence = sum(d['meta_cognition']['coherence'] for d in self.system_data) / len(self.system_data)
        
        total_uptime = time.time() - self.start_time
        
        logger.info("\n" + "=" * 70)
        logger.info("📊 PODSUMOWANIE SESJI MIGI 7G")
        logger.info("=" * 70)
        logger.info(f"🔄 Całkowita liczba cykli: {len(self.system_data)}")
        logger.info(f"⏰ Czas działania: {total_uptime:.1f}s")
        logger.info(f"🌊 Średnie GVI: {avg_gvi:.4f}")
        logger.info(f"🌀 Średnia entropia: {avg_entropy:.4f}")
        logger.info(f"💎 Średnia hegemonia: {avg_hegemony:.3f}")
        logger.info(f"🧠 Średnia koherencja: {avg_coherence:.3f}")
        logger.info("=" * 70)

    def _setup_perception_mappings(self):
        """🔧 Konfiguruje mapowania percepcyjne dla Symbolizera"""
        logger.info("🔧 Setting up perception symbol mappings...")
        
        # Mapowania podstawowe: obserwacje → symbole
        self.perception_symbolizer.register("PersonDetected", 
                                           lambda obs: obs.get("person_prob", 0.0))
        self.perception_symbolizer.register("HighTemperature", 
                                           lambda obs: 0.9 if obs.get("temp_c", 20) > 38 else 0.05)
        self.perception_symbolizer.register("LoudSound", 
                                           lambda obs: 0.8 if obs.get("audio_db", 0) > 70 else 0.1)
        self.perception_symbolizer.register("RapidMovement", 
                                           lambda obs: min(1.0, obs.get("motion_speed", 0.0) / 100.0))
        self.perception_symbolizer.register("EmergencyMarker", 
                                           lambda obs: 0.95 if obs.get("emergency_flag", False) else 0.02)
        self.perception_symbolizer.register("HighStress", 
                                           lambda obs: obs.get("stress_level", 0.0))
        self.perception_symbolizer.register("CognitiveLoad", 
                                           lambda obs: obs.get("cognitive_load", 0.0))
        self.perception_symbolizer.register("SocialActivity", 
                                           lambda obs: obs.get("social_vibration", 0.0))
        
        logger.info("✅ Perception mappings configured: 8 symbol types registered")
    
    def _run_perception_demo(self, cycle_count: int) -> Dict[str, Any]:
        """🎯 Uruchamia demo percepcyjne z różnymi scenariuszami"""
        import random
        
        # Generuj różne scenariusze w zależności od numeru cyklu
        scenarios = [
            {
                "name": "Normal Environment",
                "data": {"temp_c": 22, "person_prob": 0.1, "audio_db": 45, "motion_speed": 5}
            },
            {
                "name": "Person Detection",
                "data": {"temp_c": 24, "person_prob": 0.85, "audio_db": 50, "motion_speed": 15}
            },
            {
                "name": "High Activity",
                "data": {"temp_c": 28, "person_prob": 0.6, "audio_db": 75, "motion_speed": 60}
            },
            {
                "name": "Emergency Situation",
                "data": {"temp_c": 26, "person_prob": 0.9, "emergency_flag": True, "motion_speed": 80}
            },
            {
                "name": "Medical Alert",
                "data": {"temp_c": 39, "person_prob": 0.95, "audio_db": 85, "motion_speed": 25}
            }
        ]
        
        scenario = scenarios[(cycle_count - 1) % len(scenarios)]
        logger.info(f"👁️ PERCEPTION DEMO: {scenario['name']}")
        
        # Dodaj trochę losowości
        for key, value in scenario['data'].items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                noise = random.uniform(-0.1, 0.1) * value
                scenario['data'][key] = max(0, value + noise)
        
        # Przetwórz przez pipeline percepcyjny
        result = self.process_sensory_input(scenario['data'])
        
        logger.info(f"🧠 Perception result: {result['critical_probability']:.3f} critical probability")
        return result
    
    def process_sensory_input(self, observations: Dict[str, Any]) -> Dict[str, Any]:
        """🎯 Przetwarza dane sensoryczne przez pełny pipeline percepcyjny"""
        logger.info(f"🎯 Processing sensory input: {len(observations)} observations")
        
        # 1. Konwersja na symbole
        symbols = self.perception_symbolizer.symbolize(observations)
        logger.info(f"🧠 Generated symbols: {symbols}")
        
        # 2. Konwersja na evidence dla Bayes
        evidence = evidence_from_symbols(symbols, threshold=0.5)
        logger.info(f"📊 Hard evidence: {evidence}")
        
        # 3. Soft evidence przez weighted sampling
        marginals = weighted_sampling_for_soft_evidence(self.bayes_net, symbols, N=200)
        logger.info(f"🎲 Marginal probabilities: {marginals}")
        
        # 4. Wnioskowanie bayesowskie
        try:
            if evidence:
                critical_prob = query_marginal(self.bayes_net, "CriticalSituation", evidence)
            else:
                critical_prob = marginals.get("CriticalSituation", 0.0)
        except Exception as e:
            logger.warning(f"Bayes query failed: {e}")
            critical_prob = max(symbols.values()) if symbols else 0.0
        
        # 5. Integracja z innymi modułami
        result = {
            "raw_observations": observations,
            "symbols": symbols,
            "evidence": evidence,
            "marginals": marginals,
            "critical_probability": critical_prob,
            "processing_timestamp": time.time(),
            "requires_action": critical_prob > 0.5
        }
        
        # 6. Przekazanie do innych modułów jeśli potrzebne
        if result["requires_action"]:
            logger.warning(f"🚨 Critical situation detected! Probability: {critical_prob:.3f}")
            # Tutaj można dodać wywołania do innych modułów (Causality, Temporal, etc.)
        
        return result

    def export_full_system_data(self, filename: str = None) -> str:
        """💾 Eksportuje pełne dane systemu"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"migi7g_system_data_{timestamp}.json"
        
        export_data = {
            "metadata": {
                "system": "MIGI_7G_Brain_System",
                "version": "1.0.0",
                "export_timestamp": time.time(),
                "total_cycles": len(self.system_data),
                "session_duration": time.time() - self.start_time,
                "active_modules": self._get_active_modules().split(", ")
            },
            "session_data": self.system_data,
            "social_vibration_data": getattr(self.social_interface, 'global_state_history', []),
            "hegemony_data": getattr(self.hegemony_drive, 'hegemony_history', []),
            "meta_cognition_data": getattr(self.meta_cognition, 'cognitive_history', [])
        }
        
        full_path = f"c:\\Users\\patry\\Desktop\\AGI\\{filename}"
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"💾 Pełne dane systemu wyeksportowane: {full_path}")
        return full_path

def main():
    """🚀 Główna funkcja startowa"""
    print("🧠 MIGI 7G BRAIN SYSTEM - TRANSCENDENTNY INTERFEJS ŚWIADOMOŚCI")
    print("=" * 80)
    print("🎯 System integruje: Social Vibration, Hegemony Drive, Meta-Cognition, MGA Core")
    print("🚀 Status: OPERATIONAL - Gotowy do transcendentnej analizy")
    print("=" * 80)
    
    # Inicjalizacja systemu
    brain_system = MIGI7G_BrainSystem()
    
    # Uruchomienie sesji demonstracyjnej
    brain_system.run_demo_session(cycles=3, delay=2.0)
    
    # Eksport danych
    exported_file = brain_system.export_full_system_data()
    
    print("\n✅ System MIGI 7G zakończył pracę")
    print(f"📁 Pełne dane dostępne w: {exported_file}")
    print("🧠 MÓZG BOGA - operacja zakończona sukcesem")

if __name__ == '__main__':
    main()