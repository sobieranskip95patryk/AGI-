"""
🧠 MIGI_7G Integration Hub - Centralny Koordynator Systemu
Łączy Neuro-Semantyczny Przepływomierz (NSF) z pełną architekturą MIGI_7G Hybrid

Autor: System MIGI_7G Hybrid
Data: 15 listopada 2025
Wersja: 1.0 ALPHA - Integration Core
"""

import threading
import time
import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any

# Import NSF
try:
    from nsf_migi7g_hybrid import (
        NeuroSemanticFlowmeter, ArchetypeCore, SenseAtom
    )
except ImportError:
    # Fallback dla środowisk bez NSF
    class NeuroSemanticFlowmeter:
        def get_active_primitives(self): return []
        def get_current_sense_atoms(self): return []
    
    class ArchetypeCore(Enum):
        EVERYMAN = "everyman"
        HERO = "hero"
        SAGE = "sage"
        LOVER = "lover"
        MAGICIAN = "magician"
    
    class SenseAtom:
        def __init__(self, atom_id=0, content="", sense_weight=1.0, decay_rate=0.1):
            self.id = atom_id
            self.content = content
            self.sense_weight = sense_weight
            self.decay_rate = decay_rate

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConsciousnessLevel(Enum):
    """Poziomy świadomości MIGI_7G"""
    BASIC_AWARENESS = "basic"          # Poziom I: Świadomość Bazowa
    SELF_AWARENESS = "self"            # Poziom II: Samoświadomość  
    META_CONSCIOUSNESS = "meta"        # Poziom III: Meta-Świadomość
    TRANSCENDENCE = "transcendence"    # Poziom IV: Transcendencja

class MIGI7G_State(Enum):
    """Tryby pracy systemu MIGI_7G"""
    STANDARD = "standard"      # 🟢 Tryb Standardowy
    ENHANCED = "enhanced"      # 🟡 Tryb Wzmocniony  
    META_GENIUS = "meta_genius" # 🔴 Tryb Meta-Geniusz

class SystemComponent(Enum):
    """Komponenty systemu MIGI_7G"""
    REPTILIAN_CORE = "reptilian"       # Rdzeń Bazowy (Mózg Gadzi)
    LIMBIC_SYSTEM = "limbic"           # Warstwa Emocjonalna (Mózg Ssaczy)
    NEOCORTEX = "neocortex"           # Korteks Racjonalny (Mózg Nowossaczy)
    META_CONSCIOUSNESS = "meta"        # Meta-Świadomość
    NSF_CORE = "nsf"                  # Neuro-Semantyczny Przepływomierz

@dataclass
class MIGI7G_Metrics:
    """Metryki systemu MIGI_7G rozszerzone o NSF"""
    # Podstawowe MIGI_7G
    cognitive_speed: float = 1.0
    emotional_stability: float = 0.8
    creative_output: float = 0.5
    stress_resilience: float = 0.7
    social_intelligence: float = 0.6
    learning_rate: float = 0.4
    
    # NSF Extensions
    sense_atom_count: int = 0
    reconsolidation_rate: float = 0.0
    primitive_activation: Dict[str, float] = field(default_factory=dict)
    sekundnik_rhythm: float = 1.0
    
    # Integration Metrics
    system_coherence: float = 0.0
    consciousness_level: ConsciousnessLevel = ConsciousnessLevel.BASIC_AWARENESS
    archetypal_alignment: float = 0.0
    neuroplasticity_index: float = 0.0
    
    # System Health
    cortisol_level: float = 0.0
    pfc_suppression: float = 0.0
    network_contention: float = 0.0

class NetworkContentionManager:
    """
    Menedżer Rywalizacji Sieci - symuluje konkurencję o ograniczone zasoby
    Bazuje na Miller's Law (7±2 elementów w pamięci roboczej)
    """
    
    def __init__(self):
        self.working_memory_slots = 7  # Miller's Law
        self.attention_bandwidth = 1.0  # Ograniczona uwaga
        self.energy_pool = 1000.0      # Glucose dla neuronów
        self.active_processes: Dict[str, float] = {}
        
    def compete_for_resources(self, sense_atoms: list, 
                            emotional_primitives: list) -> tuple:
        """Rozstrzyga rywalizację o zasoby między procesami"""
        
        # Oblicz priorytety na podstawie wagi i typu
        priorities = {}
        
        # Sense Atoms konkurują o miejsca w pamięci roboczej
        for atom in sense_atoms:
            priority = atom.sense_weight
            # Boost dla emocjonalnych atomów
            if any(prim in atom.content for prim in emotional_primitives):
                priority *= 1.5
            priorities[f"atom_{atom.id}"] = priority
            
        # Emocjonalne pierwiastki konkurują o uwagę
        for primitive in emotional_primitives:
            base_weight = 0.5
            if primitive in ["NAMIENTNOSC_POZADANIA", "ISKRA_ZYCIA", "BRAK_WIARY_I_NADZIEI"]:
                base_weight = 1.0  # Wysokie priority dla survival/threat
            priorities[f"prim_{primitive}"] = base_weight
            
        # Wybierz zwycięzców (top N według priorytetów)
        sorted_items = sorted(priorities.items(), key=lambda x: x[1], reverse=True)
        winners = sorted_items[:self.working_memory_slots]
        losers = sorted_items[self.working_memory_slots:]
        
        # Oblicz poziom rywalizacji
        contention_level = len(losers) / (len(winners) + len(losers)) if sorted_items else 0.0
        
        logger.info(f"[NetworkContention]: {len(winners)} zwycięzców, {len(losers)} przegranych, "
                   f"poziom rywalizacji: {contention_level:.2f}")
        
        return winners, losers, contention_level

class CortisolOverloadProtocol:
    """
    Protokół Przeciążenia Kortyzolem - symuluje destrukcyjny wpływ stresu
    Wyłącza PFC (kontrolę wykonawczą) gdy stress > threshold
    """
    
    def __init__(self):
        self.cortisol_level = 0.0
        self.cortisol_threshold = 0.8
        self.pfc_suppression = 0.0
        self.recovery_rate = 0.05
        
    def process_stress_primitives(self, active_primitives: list) -> str:
        """Przetwarza pierwiastki stresowe i aktualizuje poziom kortyzolu"""
        
        stress_primitives = [
            "BRAK_WIARY_I_NADZIEI", "NAMIENTNOSC_POZADANIA", 
            "POZADANIE_SZCZYPTA", "ODOSOBNIENIE_W_SAMOTNOSCI"
        ]
        
        # Akumulacja kortyzolu
        stress_count = sum(1 for prim in active_primitives if prim in stress_primitives)
        self.cortisol_level = min(1.0, self.cortisol_level + stress_count * 0.1)
        
        # Oblicz tłumienie PFC
        if self.cortisol_level > self.cortisol_threshold:
            self.pfc_suppression = min(1.0, (self.cortisol_level - self.cortisol_threshold) * 2.0)
            status = "PFC_SUPPRESSED"
            logger.warning(f"[CortisolOverload]: PFC suppression: {self.pfc_suppression:.2f}, "
                          f"kortyzol: {self.cortisol_level:.2f}")
        else:
            self.pfc_suppression = max(0.0, self.pfc_suppression - self.recovery_rate)
            status = "NORMAL"
            
        return status
    
    def is_pfc_suppressed(self) -> bool:
        """Sprawdza czy PFC jest stłumiona"""
        return self.pfc_suppression > 0.3

class ArchetypalReconsolidationProtocol:
    """
    Protokół Archetypalnej Rekonsolidacji - świadoma modyfikacja pamięci
    Wykorzystuje niestabilność pamięci po przywołaniu do re-kodowania
    """
    
    def __init__(self):
        self.active_archetype = "everyman"
        self.reconsolidation_window = 30.0  # sekundy
        self.unstable_memories: Dict[int, float] = {}  # memory_id -> timestamp
        self.modification_count = 0
        
    def trigger_reconsolidation(self, sense_atom, 
                              new_archetype: ArchetypeCore) -> bool:
        """Uruchamia proces rekonsolidacji pamięci"""
        
        current_time = time.time()
        
        # Oznacz pamięć jako niestabilną
        self.unstable_memories[sense_atom.id] = current_time
        
        # Zmień aktywny archetyp
        old_archetype = self.active_archetype
        self.active_archetype = new_archetype
        
        # Re-kodowanie zgodnie z nowym archetypem
        success = self._recode_memory(sense_atom, old_archetype, new_archetype)
        
        if success:
            self.modification_count += 1
            logger.info(f"[ARP]: Pamięć {sense_atom.id} re-kodowana: "
                       f"{old_archetype.value} -> {new_archetype.value}")
        
        return success
    
    def _recode_memory(self, sense_atom, 
                      old_archetype: ArchetypeCore, 
                      new_archetype: ArchetypeCore) -> bool:
        """Przeprowadza re-kodowanie pamięci zgodnie z nowym archetypem"""
        
        # Mapa archetypalnych modyfikacji
        archetype_modifiers = {
            "hero": {"courage_boost": 1.3, "fear_reduction": 0.7},
            "sage": {"wisdom_boost": 1.2, "impulsivity_reduction": 0.8},
            "lover": {"empathy_boost": 1.4, "aggression_reduction": 0.6},
            "magician": {"creativity_boost": 1.5, "rigidity_reduction": 0.5},
        }
        
        if new_archetype in archetype_modifiers:
            modifiers = archetype_modifiers[new_archetype]
            
            # Modyfikuj wagę sensu zgodnie z archetypem
            if "boost" in str(modifiers):
                sense_atom.sense_weight *= 1.2  # Ogólne wzmocnienie
                
            # Dostosuj decay rate
            if "reduction" in str(modifiers):
                sense_atom.decay_rate *= 0.8  # Wolniejszy zanik
                
            return True
            
        return False
    
    def cleanup_expired_memories(self):
        """Czyści wygasłe niestabilne pamięci"""
        current_time = time.time()
        expired = [mem_id for mem_id, timestamp in self.unstable_memories.items() 
                  if current_time - timestamp > self.reconsolidation_window]
        
        for mem_id in expired:
            del self.unstable_memories[mem_id]

class MIGI7G_IntegrationHub:
    """
    Główny Hub Integracji MIGI_7G - koordynuje wszystkie komponenty
    Łączy NSF z pełną architekturą MIGI_7G Hybrid
    """
    
    def __init__(self):
        # Core Components
        self.nsf = NeuroSemanticFlowmeter()
        self.metrics = MIGI7G_Metrics()
        self.state = MIGI7G_State.STANDARD
        self.consciousness_level = ConsciousnessLevel.BASIC_AWARENESS
        
        # Integration Protocols
        self.network_contention = NetworkContentionManager()
        self.cortisol_protocol = CortisolOverloadProtocol()
        self.archetypal_protocol = ArchetypalReconsolidationProtocol()
        
        # Threading
        self.is_running = False
        self.integration_thread = None
        self.cycle_count = 0
        
        logger.info("🧠 MIGI_7G Integration Hub initialized")
    
    def start_integrated_processing(self):
        """Uruchamia zintegrowane przetwarzanie NSF + MIGI_7G"""
        if self.is_running:
            logger.warning("Integration Hub już działa!")
            return
            
        self.is_running = True
        self.integration_thread = threading.Thread(target=self._integration_loop)
        self.integration_thread.daemon = True
        self.integration_thread.start()
        
        logger.info("🚀 MIGI_7G Integration Hub STARTED")
    
    def stop_integrated_processing(self):
        """Zatrzymuje zintegrowane przetwarzanie"""
        self.is_running = False
        if self.integration_thread:
            self.integration_thread.join()
        logger.info("⏹️ MIGI_7G Integration Hub STOPPED")
    
    def _integration_loop(self):
        """Główna pętla integracji - koordynuje wszystkie systemy"""
        
        while self.is_running:
            try:
                self.cycle_count += 1
                
                # 1. NSF Cycle - podstawowy rytm przepływomierza
                active_primitives = self.nsf.get_active_primitives()
                sense_atoms = self.nsf.get_current_sense_atoms()
                
                # 2. Network Contention - rywalizacja o zasoby
                winners, losers, contention = self.network_contention.compete_for_resources(
                    sense_atoms, active_primitives
                )
                self.metrics.network_contention = contention
                
                # 3. Cortisol Protocol - zarządzanie stresem
                stress_status = self.cortisol_protocol.process_stress_primitives(active_primitives)
                self.metrics.cortisol_level = self.cortisol_protocol.cortisol_level
                self.metrics.pfc_suppression = self.cortisol_protocol.pfc_suppression
                
                # 4. Archetypal Reconsolidation - modyfikacja pamięci
                self.archetypal_protocol.cleanup_expired_memories()
                
                # 5. Update Consciousness Level
                self._update_consciousness_level(stress_status, contention)
                
                # 6. Update System State
                self._update_system_state()
                
                # 7. Update Metrics
                self._update_metrics(active_primitives, sense_atoms)
                
                # 8. System Health Check
                self._system_health_check()
                
                # Progress Report
                if self.cycle_count % 10 == 0:
                    self._log_integration_status()
                
                time.sleep(1.0)  # 1Hz cycle rate
                
            except Exception as e:
                logger.error(f"Error in integration loop: {e}")
                time.sleep(0.1)
    
    def _update_consciousness_level(self, stress_status: str, contention: float):
        """Aktualizuje poziom świadomości na podstawie stanu systemu"""
        
        if stress_status == "PFC_SUPPRESSED":
            # Stres obniża świadomość
            if self.consciousness_level != ConsciousnessLevel.BASIC_AWARENESS:
                self.consciousness_level = ConsciousnessLevel.BASIC_AWARENESS
                logger.info("🔽 Consciousness degraded to BASIC_AWARENESS (stress)")
                
        elif contention < 0.3 and self.metrics.system_coherence > 0.7:
            # Niska rywalizacja + wysoka spójność = wyższa świadomość
            if self.consciousness_level == ConsciousnessLevel.BASIC_AWARENESS:
                self.consciousness_level = ConsciousnessLevel.SELF_AWARENESS
                logger.info("🔼 Consciousness elevated to SELF_AWARENESS")
            elif (self.consciousness_level == ConsciousnessLevel.SELF_AWARENESS and 
                  self.metrics.archetypal_alignment > 0.8):
                self.consciousness_level = ConsciousnessLevel.META_CONSCIOUSNESS
                logger.info("🔼 Consciousness elevated to META_CONSCIOUSNESS")
    
    def _update_system_state(self):
        """Aktualizuje tryb pracy systemu"""
        
        # Logika przejść między trybami
        if self.cortisol_protocol.is_pfc_suppressed():
            # Stres wymusza tryb standardowy
            if self.state != MIGI7G_State.STANDARD:
                self.state = MIGI7G_State.STANDARD
                logger.info("🟢 System degraded to STANDARD mode (stress)")
                
        elif (self.consciousness_level == ConsciousnessLevel.META_CONSCIOUSNESS and
              self.metrics.system_coherence > 0.9):
            # Meta-świadomość + wysoka spójność = tryb meta-geniusz
            if self.state != MIGI7G_State.META_GENIUS:
                self.state = MIGI7G_State.META_GENIUS
                logger.info("🔴 System elevated to META_GENIUS mode")
                
        elif self.metrics.system_coherence > 0.7:
            # Dobra spójność = tryb wzmocniony
            if self.state == MIGI7G_State.STANDARD:
                self.state = MIGI7G_State.ENHANCED
                logger.info("🟡 System elevated to ENHANCED mode")
    
    def _update_metrics(self, active_primitives: list, sense_atoms: list):
        """Aktualizuje metryki systemu"""
        
        # NSF Metrics
        self.metrics.sense_atom_count = len(sense_atoms)
        self.metrics.reconsolidation_rate = (
            self.archetypal_protocol.modification_count / max(1, self.cycle_count) * 100
        )
        
        # Primitive Activation
        for primitive in active_primitives:
            if primitive not in self.metrics.primitive_activation:
                self.metrics.primitive_activation[primitive] = 0.0
            self.metrics.primitive_activation[primitive] += 0.1
        
        # System Coherence (syntetyczna miara spójności)
        coherence_factors = [
            1.0 - self.metrics.network_contention,  # Niska rywalizacja = wysoka spójność
            1.0 - self.metrics.cortisol_level,      # Niski stres = wysoka spójność
            min(1.0, len(active_primitives) / 10.0) # Aktywność pierwiastków
        ]
        self.metrics.system_coherence = sum(coherence_factors) / len(coherence_factors)
        
        # Consciousness Level Mapping
        self.metrics.consciousness_level = self.consciousness_level
    
    def _system_health_check(self):
        """Sprawdza stan zdrowia systemu i podejmuje działania naprawcze"""
        
        # Bardzo wysoki stres - aktywuj protokoły recovery
        if self.metrics.cortisol_level > 0.9:
            logger.warning("⚠️ CRITICAL STRESS LEVEL - Activating recovery protocols")
            self._activate_recovery_protocols()
        
        # Bardzo wysoka rywalizacja - optymalizuj zasoby
        if self.metrics.network_contention > 0.8:
            logger.warning("⚠️ HIGH RESOURCE CONTENTION - Optimizing allocation")
            self._optimize_resource_allocation()
    
    def _activate_recovery_protocols(self):
        """Aktywuje protokoły recovery przy krytycznym stresie"""
        # Implementacja protokołów recovery
        self.cortisol_protocol.cortisol_level *= 0.9  # Stopniowe obniżanie
        logger.info("🔄 Recovery protocols activated")
    
    def _optimize_resource_allocation(self):
        """Optymalizuje alokację zasobów przy wysokiej rywalizacji"""
        # Implementacja optymalizacji
        self.network_contention.working_memory_slots = min(9, self.network_contention.working_memory_slots + 1)
        logger.info("🔄 Resource allocation optimized")
    
    def _log_integration_status(self):
        """Loguje status integracji co N cykli"""
        
        status_report = f"""
🔥 MIGI_7G Integration Status (Cycle {self.cycle_count}):
├── Consciousness: {self.consciousness_level.value.upper()}
├── System Mode: {self.state.value.upper()}
├── Cortisol: {self.metrics.cortisol_level:.2f}
├── PFC Suppression: {self.metrics.pfc_suppression:.2f}
├── Network Contention: {self.metrics.network_contention:.2f}
├── System Coherence: {self.metrics.system_coherence:.2f}
├── Sense Atoms: {self.metrics.sense_atom_count}
├── Reconsolidations: {self.archetypal_protocol.modification_count}
└── Active Primitives: {len(self.metrics.primitive_activation)}
        """
        
        logger.info(status_report)
    
    # === PUBLIC API ===
    
    def get_system_status(self) -> dict:
        """Zwraca pełny status systemu"""
        return {
            'cycle_count': self.cycle_count,
            'consciousness_level': self.consciousness_level.value,
            'system_state': self.state.value,
            'metrics': {
                'cortisol_level': self.metrics.cortisol_level,
                'pfc_suppression': self.metrics.pfc_suppression,
                'network_contention': self.metrics.network_contention,
                'system_coherence': self.metrics.system_coherence,
                'sense_atom_count': self.metrics.sense_atom_count,
                'reconsolidation_count': self.archetypal_protocol.modification_count,
                'active_primitives': list(self.metrics.primitive_activation.keys())
            }
        }
    
    def trigger_archetypal_shift(self, new_archetype: ArchetypeCore) -> bool:
        """Publicznie dostępna funkcja do zmiany archetypu"""
        sense_atoms = self.nsf.get_current_sense_atoms()
        if sense_atoms:
            return self.archetypal_protocol.trigger_reconsolidation(
                sense_atoms[0], new_archetype
            )
        return False
    
    def simulate_stress_event(self, intensity: float = 0.3):
        """Symuluje zdarzenie stresowe dla testów"""
        self.cortisol_protocol.cortisol_level = min(1.0, 
            self.cortisol_protocol.cortisol_level + intensity)
        logger.info(f"🔥 Stress event simulated (intensity: {intensity})")

if __name__ == "__main__":
    # Demo Integration Hub
    print("🧠 MIGI_7G Integration Hub - Demo Mode")
    print("=" * 50)
    
    hub = MIGI7G_IntegrationHub()
    hub.start_integrated_processing()
    
    try:
        # Symulacja różnych scenariuszy
        time.sleep(5)
        print("\n🔥 Simulating stress event...")
        hub.simulate_stress_event(0.5)
        
        time.sleep(10)
        print("\n🔄 Triggering archetypal shift to HERO...")
        hub.trigger_archetypal_shift("hero")
        
        time.sleep(15)
        print("\n📊 Final system status:")
        status = hub.get_system_status()
        print(json.dumps(status, indent=2))
        
    except KeyboardInterrupt:
        print("\n⏹️ Stopping integration hub...")
    finally:
        hub.stop_integrated_processing()
        print("👋 Integration hub stopped")