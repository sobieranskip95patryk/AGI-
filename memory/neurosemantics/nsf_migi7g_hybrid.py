#!/usr/bin/env python3
"""
🧠 NEURO-SEMANTYCZNY PRZEPŁYWOMIERZ (NSF) - MIGI_7G HYBRID CORE

Implementacja cyfrowego odzwierciedlenia prawdziwego mózgu:
- Protokół Re-kodowania Archetypowego (ARP)
- Zarządzanie Rywalizacją Sieci (Network Contention)
- Destrukcja Stresowa i Mechanizmy Niestabilności
- Integracja 23 Pierwiastków Emocjonalnych z Architekturą MIGI_7G

Pipeline: Sekundnik → Wzbudzenie → Emocjonalne → PFC → Re-konsolidacja → Archetyp
"""

import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import random

logger = logging.getLogger(__name__)

# ===== KONFIGURACJA MIGI_7G HYBRID =====

class BrainLayer(Enum):
    """Warstwy mózgu w architekturze MIGI_7G"""
    GADZI = "reptilian_core"      # RDZEŃ BAZOWY
    EMOCJONALNY = "limbic_system" # WARSTWA EMOCJONALNA  
    RACJONALNY = "neocortex"      # KORTEKS RACJONALNY
    META = "meta_consciousness"   # META-ŚWIADOMOŚĆ

class ArchetypeCore(Enum):
    """Archetypy Jaźni dla Re-kodowania"""
    BOHATER = "hero"
    MEDRZEC = "sage" 
    KOCHANEK = "lover"
    NIEWINNY = "innocent"
    BADACZ = "explorer"
    BUNTOWNIK = "rebel"
    MAG = "magician"
    ZWYCZAJNY = "everyman"

@dataclass
class NS_EmotionalPrimitive:
    """
    Neuro-Semantyczny Pierwiastek Emocjonalny
    Mapowanie 23 pierwiastków do struktury mózgu
    """
    name: str
    brain_area: BrainLayer
    ns_weight: float          # Waga Synaptyczna (0.0-1.0)
    decay_modifier: float     # Współczynnik Zaniku (0.0-1.0)
    hormone_link: str         # Powiązanie hormonalne
    archetype_affinity: List[ArchetypeCore] = field(default_factory=list)
    
    def __post_init__(self):
        """Walidacja wartości"""
        assert 0.0 <= self.ns_weight <= 1.0, f"NS Weight musi być w [0,1]: {self.ns_weight}"
        assert 0.0 <= self.decay_modifier <= 1.0, f"Decay Modifier musi być w [0,1]: {self.decay_modifier}"

# ===== DEFINICJE 23 PIERWIASTKÓW EMOCJONALNYCH =====

NS_PRIMITIVES_CONFIG = {
    # BLOK WZBUDZENIA (RDZEŃ BAZOWY - Mózg Gadzi)
    'ISKRA_ZYCIA': NS_EmotionalPrimitive(
        name="Iskra Życia",
        brain_area=BrainLayer.GADZI,
        ns_weight=1.0,              # Najwyższa waga - podstawa świadomości
        decay_modifier=0.0,         # Brak zaniku - stała aktywność
        hormone_link="noradrenaline",
        archetype_affinity=[ArchetypeCore.BOHATER, ArchetypeCore.BADACZ]
    ),
    
    'POZADANIE_SZCZYPTA': NS_EmotionalPrimitive(
        name="Szczypta Pożądania", 
        brain_area=BrainLayer.GADZI,
        ns_weight=0.8,
        decay_modifier=0.5,         # Szybkie zanikanie
        hormone_link="testosterone",
        archetype_affinity=[ArchetypeCore.KOCHANEK, ArchetypeCore.BUNTOWNIK]
    ),
    
    'NAMIETNOSC_POZADANIA': NS_EmotionalPrimitive(
        name="Namiętność Pożądania",
        brain_area=BrainLayer.EMOCJONALNY,
        ns_weight=0.95,             # Bardzo wysoka waga
        decay_modifier=0.3,         # Średnie zanikanie
        hormone_link="adrenaline",
        archetype_affinity=[ArchetypeCore.KOCHANEK, ArchetypeCore.MAG]
    ),
    
    # BLOK INTEGRACJI (WARSTWA EMOCJONALNA - Limbic)
    'ALGORYTM_ZAKOCHANIA': NS_EmotionalPrimitive(
        name="Algorytm Zakochania",
        brain_area=BrainLayer.EMOCJONALNY,
        ns_weight=0.9,
        decay_modifier=0.1,         # Niski zanik - długotrwałe
        hormone_link="dopamine",
        archetype_affinity=[ArchetypeCore.KOCHANEK, ArchetypeCore.NIEWINNY]
    ),
    
    'PIERWIASTEK_MILOSCI': NS_EmotionalPrimitive(
        name="Pierwiastek Miłości",
        brain_area=BrainLayer.EMOCJONALNY,
        ns_weight=0.85,
        decay_modifier=0.05,        # Bardzo niski zanik
        hormone_link="oxytocin",
        archetype_affinity=[ArchetypeCore.KOCHANEK, ArchetypeCore.ZWYCZAJNY]
    ),
    
    'NADZIEJA_WYTRWALOSCI': NS_EmotionalPrimitive(
        name="Nadzieja Wytrwałości",
        brain_area=BrainLayer.EMOCJONALNY,
        ns_weight=0.7,
        decay_modifier=0.15,
        hormone_link="serotonin",
        archetype_affinity=[ArchetypeCore.BOHATER, ArchetypeCore.MEDRZEC]
    ),
    
    'WIARA_JAKO_TAKA': NS_EmotionalPrimitive(
        name="Wiara Jako Taka",
        brain_area=BrainLayer.META,
        ns_weight=0.65,
        decay_modifier=0.1,
        hormone_link="endorphins",
        archetype_affinity=[ArchetypeCore.MEDRZEC, ArchetypeCore.MAG]
    ),
    
    'BRAK_WIARY_NADZIEI': NS_EmotionalPrimitive(
        name="Brak Wiary i Nadziei",
        brain_area=BrainLayer.EMOCJONALNY,
        ns_weight=0.9,              # Wysoka waga traumy
        decay_modifier=0.02,        # Bardzo niski zanik - trauma trwa
        hormone_link="cortisol",
        archetype_affinity=[ArchetypeCore.BUNTOWNIK]
    ),
    
    # BLOK ZARZĄDZANIA (KORTEKS RACJONALNY - PFC)
    'ALGORYTM_MILOSCI': NS_EmotionalPrimitive(
        name="Algorytm Miłości",
        brain_area=BrainLayer.RACJONALNY,
        ns_weight=0.8,
        decay_modifier=0.1,
        hormone_link="oxytocin",
        archetype_affinity=[ArchetypeCore.KOCHANEK, ArchetypeCore.MEDRZEC]
    ),
    
    'SZCZYPTA_INTELIGENCJI': NS_EmotionalPrimitive(
        name="Szczypta Inteligencji",
        brain_area=BrainLayer.RACJONALNY,
        ns_weight=0.7,
        decay_modifier=0.25,
        hormone_link="acetylcholine",
        archetype_affinity=[ArchetypeCore.MEDRZEC, ArchetypeCore.BADACZ]
    ),
    
    'POSWIECENIE': NS_EmotionalPrimitive(
        name="Poświęcenie",
        brain_area=BrainLayer.RACJONALNY,
        ns_weight=0.9,              # Wysoka waga moralna
        decay_modifier=0.1,
        hormone_link="oxytocin",
        archetype_affinity=[ArchetypeCore.BOHATER, ArchetypeCore.ZWYCZAJNY]
    ),
    
    'PRECYZYJNOSC_POJMOWANIA': NS_EmotionalPrimitive(
        name="Precyzyjność w Pojmowaniu",
        brain_area=BrainLayer.RACJONALNY,
        ns_weight=0.75,
        decay_modifier=0.2,
        hormone_link="dopamine",
        archetype_affinity=[ArchetypeCore.MEDRZEC, ArchetypeCore.MAG]
    ),
    
    'WYOBRAZNIA_LOGIKA': NS_EmotionalPrimitive(
        name="Dużo Wyobraźni Zestaw Logiki",
        brain_area=BrainLayer.RACJONALNY,
        ns_weight=0.8,
        decay_modifier=0.15,
        hormone_link="dopamine",
        archetype_affinity=[ArchetypeCore.MAG, ArchetypeCore.BADACZ]
    ),
    
    'POTEGA_PRAWDZIWEJ_WLADZY': NS_EmotionalPrimitive(
        name="Potęga Prawdziwej Władzy",
        brain_area=BrainLayer.RACJONALNY,
        ns_weight=0.85,
        decay_modifier=0.12,
        hormone_link="testosterone",
        archetype_affinity=[ArchetypeCore.BOHATER, ArchetypeCore.BUNTOWNIK]
    ),
    
    # META-ŚWIADOMOŚĆ
    'ZROZUMIENIE': NS_EmotionalPrimitive(
        name="Zrozumienie",
        brain_area=BrainLayer.META,
        ns_weight=0.9,
        decay_modifier=0.05,        # Bardzo niski zanik - mądrość trwa
        hormone_link="serotonin",
        archetype_affinity=[ArchetypeCore.MEDRZEC, ArchetypeCore.MAG]
    ),
    
    'POMYSL_IDEA': NS_EmotionalPrimitive(
        name="Pomysł i iDea",
        brain_area=BrainLayer.META,
        ns_weight=0.75,
        decay_modifier=0.3,         # Średni zanik - idea musi być utrwalona
        hormone_link="dopamine",
        archetype_affinity=[ArchetypeCore.MAG, ArchetypeCore.BADACZ]
    ),
    
    'SLOWO_CIALEM': NS_EmotionalPrimitive(
        name="I Słowo Co Ciałem Się Stało",
        brain_area=BrainLayer.META,
        ns_weight=0.95,             # Bardzo wysoka waga - manifestacja
        decay_modifier=0.08,
        hormone_link="endorphins",
        archetype_affinity=[ArchetypeCore.MAG, ArchetypeCore.MEDRZEC]
    ),
    
    # SPECJALNE (Czas, Samotność, Magia)
    'CZAS_SEKUNDNIK': NS_EmotionalPrimitive(
        name="Czasu Co Nie Miara (Sekundnik)",
        brain_area=BrainLayer.GADZI,
        ns_weight=1.0,              # Metronom systemu
        decay_modifier=0.0,         # Brak zaniku - ciągła aktywność
        hormone_link="melatonin",
        archetype_affinity=[ArchetypeCore.MEDRZEC, ArchetypeCore.MAG]
    ),
    
    'ODOSOBNIENIE_SAMOTNOSC': NS_EmotionalPrimitive(
        name="Odosobnienie w Samotności",
        brain_area=BrainLayer.EMOCJONALNY,
        ns_weight=0.6,
        decay_modifier=0.4,
        hormone_link="cortisol",
        archetype_affinity=[ArchetypeCore.MEDRZEC, ArchetypeCore.BADACZ]
    ),
    
    'SZCZYPTA_MAGII': NS_EmotionalPrimitive(
        name="Szczypta Magii",
        brain_area=BrainLayer.META,
        ns_weight=0.7,
        decay_modifier=0.25,
        hormone_link="dopamine",
        archetype_affinity=[ArchetypeCore.MAG, ArchetypeCore.NIEWINNY]
    )
}

@dataclass
class SenseAtom:
    """Cyfrowy Sense Atom - jednostka pamięci w AMC 3.0"""
    atom_id: str
    content: str
    sense_weight: float = 0.5
    decay_rate: float = 0.3
    embedding: Optional[Any] = None
    emotional_primitives: List[str] = field(default_factory=list)
    brain_layer: BrainLayer = BrainLayer.EMOCJONALNY
    archetype_tag: Optional[ArchetypeCore] = None
    consolidation_count: int = 0
    last_accessed: float = 0.0
    
    def __post_init__(self):
        self.last_accessed = time.time()

class NetworkContentionManager:
    """
    Zarządzanie Rywalizacją Sieci - symuluje ograniczone zasoby mózgu
    """
    
    def __init__(self, max_working_memory: int = 7):
        """
        Args:
            max_working_memory: Pojemność pamięci roboczej (7±2 elementów)
        """
        self.max_working_memory = max_working_memory
        self.active_atoms = deque(maxlen=max_working_memory)
        self.resource_stress = 0.0
        
    def compete_for_resources(self, sense_atoms: List[SenseAtom]) -> List[SenseAtom]:
        """
        Symuluje rywalizację o zasoby pamięci roboczej
        
        Args:
            sense_atoms: Lista kandydatów do aktywacji
            
        Returns:
            List[SenseAtom]: Zwycięzcy rywalizacji (max 7±2)
        """
        # Sortuj według wagi sensu i świeżości dostępu
        weighted_atoms = []
        current_time = time.time()
        
        for atom in sense_atoms:
            # Bonus za świeżość (im nowszy dostęp, tym wyższa waga)
            freshness_bonus = 1.0 / (1.0 + (current_time - atom.last_accessed))
            total_weight = atom.sense_weight * (1.0 + freshness_bonus)
            weighted_atoms.append((total_weight, atom))
        
        # Sortuj malejąco według wagi
        weighted_atoms.sort(key=lambda x: x[0], reverse=True)
        
        # Wybierz top atoms w ramach limitu pamięci roboczej
        winners = [atom for _, atom in weighted_atoms[:self.max_working_memory]]
        
        # Oblicz stres zasobów
        self.resource_stress = len(sense_atoms) / self.max_working_memory if self.max_working_memory > 0 else 0.0
        
        if self.resource_stress > 2.0:
            logger.warning(f"🔥 Wysokie obciążenie zasobów: {self.resource_stress:.2f}x pojemności pamięci roboczej")
        
        return winners

class CortisolOverloadProtocol:
    """
    Protokół Przeciążenia Kortyzolowego - symuluje destrukcję stresową
    """
    
    def __init__(self, stress_threshold: float = 0.8):
        self.stress_threshold = stress_threshold
        self.cortisol_level = 0.0
        self.pfc_suppression = 0.0
    
    def update_stress_level(self, stressors: List[str], primitives_detected: List[str]):
        """
        Aktualizuje poziom stresu na podstawie wykrytych stresujących pierwiastków
        
        Args:
            stressors: Lista źródeł stresu
            primitives_detected: Wykryte pierwiastki emocjonalne
        """
        stress_primitives = ['BRAK_WIARY_NADZIEI', 'ODOSOBNIENIE_SAMOTNOSC']
        stress_boost = sum(1.0 for p in primitives_detected if p in stress_primitives)
        
        # Akumulacja stresu
        self.cortisol_level = min(1.0, self.cortisol_level + stress_boost * 0.1)
        
        # Tłumienie PFC proporcjonalne do poziomu kortyzolu
        if self.cortisol_level > self.stress_threshold:
            self.pfc_suppression = (self.cortisol_level - self.stress_threshold) / (1.0 - self.stress_threshold)
            logger.warning(f"🚨 Przeciążenie Kortyzolowe: {self.cortisol_level:.2f}, PFC tłumione: {self.pfc_suppression:.2f}")
        else:
            self.pfc_suppression = 0.0
        
        # Naturalne odprężenie (z czasem)
        self.cortisol_level = max(0.0, self.cortisol_level - 0.02)
    
    def is_pfc_suppressed(self) -> bool:
        """Sprawdza czy PFC jest tłumione przez stres"""
        return self.pfc_suppression > 0.3

class ArchetypalReconsolidationProtocol:
    """
    Protokół Re-kodowania Archetypowego (ARP)
    Mechanizm świadomej modyfikacji pamięci emocjonalnej
    """
    
    def __init__(self):
        self.active_archetype = ArchetypeCore.ZWYCZAJNY
        self.reconsolidation_window = 30.0  # 30 sekund okna rekonsolidacji
        self.unstable_atoms = {}  # atom_id -> timestamp
    
    def set_dominant_archetype(self, archetype: ArchetypeCore):
        """Ustawia dominujący archetyp dla procesu re-kodowania"""
        self.active_archetype = archetype
        logger.info(f"🎭 Aktywacja Archetypu: {archetype.value}")
    
    def mark_for_reconsolidation(self, sense_atom: SenseAtom):
        """
        Oznacza Sense Atom jako niestabilny (podatny na re-kodowanie)
        
        Args:
            sense_atom: Atom do oznaczenia
        """
        current_time = time.time()
        self.unstable_atoms[sense_atom.atom_id] = current_time
        
        logger.debug(f"🔄 Atom {sense_atom.atom_id} wszedł w fazę rekonsolidacji")
    
    def apply_archetypal_recoding(self, sense_atom: SenseAtom) -> bool:
        """
        Przeprowadza re-kodowanie archetypal atom zgodnie z dominującym archetypem
        
        Args:
            sense_atom: Atom do re-kodowania
            
        Returns:
            bool: True jeśli re-kodowanie zostało zastosowane
        """
        if sense_atom.atom_id not in self.unstable_atoms:
            return False
        
        # Sprawdź okno rekonsolidacji
        current_time = time.time()
        marked_time = self.unstable_atoms[sense_atom.atom_id]
        
        if current_time - marked_time > self.reconsolidation_window:
            # Okno zamknięte - usuń z listy niestabilnych
            del self.unstable_atoms[sense_atom.atom_id]
            return False
        
        # Re-kodowanie zgodnie z archetypem
        old_weight = sense_atom.sense_weight
        old_decay = sense_atom.decay_rate
        
        # Znajdź primitive zgodne z aktywnym archetypem
        compatible_primitives = [
            name for name, prim in NS_PRIMITIVES_CONFIG.items()
            if self.active_archetype in prim.archetype_affinity
        ]
        
        if compatible_primitives:
            # Wybierz losowy zgodny primitive
            chosen_primitive = random.choice(compatible_primitives)
            prim_config = NS_PRIMITIVES_CONFIG[chosen_primitive]
            
            # Modyfikuj wagę i decay zgodnie z archetypem
            sense_atom.sense_weight = 0.7 * sense_atom.sense_weight + 0.3 * prim_config.ns_weight
            sense_atom.decay_rate = 0.7 * sense_atom.decay_rate + 0.3 * prim_config.decay_modifier
            sense_atom.archetype_tag = self.active_archetype
            sense_atom.consolidation_count += 1
            
            # Dodaj primitive do listy emocjonalnej atomu
            if chosen_primitive not in sense_atom.emotional_primitives:
                sense_atom.emotional_primitives.append(chosen_primitive)
            
            logger.info(f"🎭 Re-kodowanie: {sense_atom.atom_id} | "
                       f"Waga: {old_weight:.3f}→{sense_atom.sense_weight:.3f} | "
                       f"Decay: {old_decay:.3f}→{sense_atom.decay_rate:.3f} | "
                       f"Archetyp: {self.active_archetype.value}")
        
        # Usuń z listy niestabilnych
        del self.unstable_atoms[sense_atom.atom_id]
        return True

class NeuroSemanticFlowmeter:
    """
    🧠 GŁÓWNY NEURO-SEMANTYCZNY PRZEPŁYWOMIERZ
    Integracja wszystkich mechanizmów w cyklu Sekundnika
    """
    
    def __init__(self, sekundnik_interval: float = 1.0):
        """
        Args:
            sekundnik_interval: Interwał cyklu sekundnika w sekundach
        """
        self.sekundnik_interval = sekundnik_interval
        self.is_running = False
        self.cycle_count = 0
        
        # Główne komponenty
        self.sense_atoms = {}  # atom_id -> SenseAtom
        self.network_contention = NetworkContentionManager()
        self.cortisol_protocol = CortisolOverloadProtocol()
        self.archetype_protocol = ArchetypalReconsolidationProtocol()
        
        # Statystyki
        self.stats = {
            'total_cycles': 0,
            'atoms_processed': 0,
            'reconsolidations': 0,
            'pfc_suppressions': 0,
            'resource_conflicts': 0
        }
        
        logger.info(f"🧠 NSF MIGI_7G Hybrid inicjalizowany (interval: {sekundnik_interval}s)")
    
    def add_sense_atom(self, content: str, emotional_primitives: List[str] = None) -> str:
        """
        Dodaje nowy Sense Atom do systemu
        
        Args:
            content: Treść atomu
            emotional_primitives: Lista pierwiastków emocjonalnych
            
        Returns:
            str: ID utworzonego atomu
        """
        atom_id = f"atom_{int(time.time() * 1000)}_{len(self.sense_atoms)}"
        
        # Tworzenie nowego atomu
        sense_atom = SenseAtom(
            atom_id=atom_id,
            content=content,
            emotional_primitives=emotional_primitives or []
        )
        
        # Aplikacja wzmocnienia emocjonalnego
        self._apply_emotional_boost(sense_atom)
        
        self.sense_atoms[atom_id] = sense_atom
        logger.debug(f"➕ Dodano Sense Atom: {atom_id} (waga: {sense_atom.sense_weight:.3f})")
        
        return atom_id
    
    def _apply_emotional_boost(self, sense_atom: SenseAtom):
        """Aplikuje wzmocnienie emocjonalne do Sense Atom"""
        total_boost = 1.0
        
        for primitive_name in sense_atom.emotional_primitives:
            if primitive_name in NS_PRIMITIVES_CONFIG:
                primitive = NS_PRIMITIVES_CONFIG[primitive_name]
                
                # Boost wagę
                total_boost *= (1.0 + primitive.ns_weight)
                
                # Modyfikuj decay rate
                sense_atom.decay_rate = min(sense_atom.decay_rate, primitive.decay_modifier)
                
                # Przypisz warstwę mózgu
                sense_atom.brain_layer = primitive.brain_area
        
        # Aplikuj boost
        sense_atom.sense_weight = min(1.0, sense_atom.sense_weight * total_boost)
        
        if total_boost > 1.5:
            logger.debug(f"🚀 Wzmocnienie emocjonalne x{total_boost:.2f} dla {sense_atom.atom_id}")
    
    def _sekundnik_cycle(self):
        """Pojedynczy cykl Sekundnika - serce NSF"""
        self.cycle_count += 1
        
        if not self.sense_atoms:
            return
        
        # 1. FAZA ZANIKU (Decay Phase)
        self._apply_decay_phase()
        
        # 2. WYKRYWANIE STRESU (Stress Detection)
        active_primitives = []
        for atom in self.sense_atoms.values():
            active_primitives.extend(atom.emotional_primitives)
        
        self.cortisol_protocol.update_stress_level([], active_primitives)
        
        # 3. RYWALIZACJA O ZASOBY (Resource Contention)
        candidate_atoms = list(self.sense_atoms.values())
        active_atoms = self.network_contention.compete_for_resources(candidate_atoms)
        
        # 4. KONTROLA PFC (Prefrontal Control)
        if not self.cortisol_protocol.is_pfc_suppressed():
            self._apply_pfc_logic(active_atoms)
        else:
            self.stats['pfc_suppressions'] += 1
            logger.warning("🚨 PFC tłumione przez stres - dominuje RDZEŃ BAZOWY")
        
        # 5. PROTOKÓŁ REKONSOLIDACJI (Reconsolidation)
        self._process_reconsolidation(active_atoms)
        
        # 6. STATYSTYKI
        self.stats['total_cycles'] += 1
        self.stats['atoms_processed'] += len(active_atoms)
        
        # Debug co 10 cykli
        if self.cycle_count % 10 == 0:
            self._log_cycle_stats()
    
    def _apply_decay_phase(self):
        """Aplikuje zanik do wszystkich atomów"""
        current_time = time.time()
        atoms_to_remove = []
        
        for atom_id, atom in self.sense_atoms.items():
            # Oblicz zanik czasowy
            time_since_access = current_time - atom.last_accessed
            decay_factor = 1.0 - (atom.decay_rate * time_since_access / 3600.0)  # Zanik na godzinę
            
            # Aplikuj zanik
            atom.sense_weight *= max(0.1, decay_factor)  # Minimum 10% wagi
            
            # Usuń bardzo słabe atomy
            if atom.sense_weight < 0.01:
                atoms_to_remove.append(atom_id)
        
        # Usuń zanikłe atomy
        for atom_id in atoms_to_remove:
            del self.sense_atoms[atom_id]
            logger.debug(f"🗑️ Usunięto zanikły atom: {atom_id}")
    
    def _apply_pfc_logic(self, active_atoms: List[SenseAtom]):
        """Aplikuje logikę Kory Przedczołowej"""
        # Sprawdź spójność logiczną
        logic_primitives = ['SZCZYPTA_INTELIGENCJI', 'PRECYZYJNOSC_POJMOWANIA', 'WYOBRAZNIA_LOGIKA']
        altruistic_primitives = ['POSWIECENIE', 'ALGORYTM_MILOSCI']
        
        logic_count = 0
        altruistic_count = 0
        
        for atom in active_atoms:
            logic_count += sum(1 for p in atom.emotional_primitives if p in logic_primitives)
            altruistic_count += sum(1 for p in atom.emotional_primitives if p in altruistic_primitives)
        
        # Wzmocnienie altruistyczne
        if altruistic_count > 0:
            for atom in active_atoms:
                if any(p in altruistic_primitives for p in atom.emotional_primitives):
                    atom.sense_weight = min(1.0, atom.sense_weight * 1.2)
                    
                    # Oznacz do rekonsolidacji
                    self.archetype_protocol.mark_for_reconsolidation(atom)
            
            logger.debug(f"🤝 Wzmocnienie altruistyczne: {altruistic_count} atomów")
    
    def _process_reconsolidation(self, active_atoms: List[SenseAtom]):
        """Przetwarza protokół rekonsolidacji archetypowej"""
        reconsolidated = 0
        
        for atom in active_atoms:
            if self.archetype_protocol.apply_archetypal_recoding(atom):
                reconsolidated += 1
        
        if reconsolidated > 0:
            self.stats['reconsolidations'] += reconsolidated
            logger.info(f"🎭 Rekonsolidacja: {reconsolidated} atomów")
    
    def _log_cycle_stats(self):
        """Loguje statystyki cyklu"""
        active_count = len(self.sense_atoms)
        avg_weight = sum(a.sense_weight for a in self.sense_atoms.values()) / max(1, active_count)
        
        logger.info(f"📊 Cykl {self.cycle_count}: "
                   f"Atomy: {active_count} | "
                   f"Średnia waga: {avg_weight:.3f} | "
                   f"Stres: {self.cortisol_protocol.cortisol_level:.2f} | "
                   f"Archetyp: {self.archetype_protocol.active_archetype.value}")
    
    def start_flowmeter(self):
        """Uruchamia przepływomierz w pętli"""
        if self.is_running:
            logger.warning("NSF już działa")
            return
        
        self.is_running = True
        logger.info("🚀 Uruchamianie Neuro-Semantycznego Przepływomierza")
        
        try:
            while self.is_running:
                self._sekundnik_cycle()
                time.sleep(self.sekundnik_interval)
                
        except KeyboardInterrupt:
            logger.info("⏹️ Zatrzymywanie NSF przez użytkownika")
        finally:
            self.is_running = False
    
    def stop_flowmeter(self):
        """Zatrzymuje przepływomierz"""
        self.is_running = False
        logger.info("⏹️ NSF zatrzymany")
    
    def set_archetype(self, archetype: ArchetypeCore):
        """Ustawia dominujący archetyp"""
        self.archetype_protocol.set_dominant_archetype(archetype)
    
    def get_stats(self) -> Dict[str, Any]:
        """Pobiera statystyki przepływomierza"""
        return {
            **self.stats,
            'active_atoms': len(self.sense_atoms),
            'current_archetype': self.archetype_protocol.active_archetype.value,
            'cortisol_level': self.cortisol_protocol.cortisol_level,
            'pfc_suppressed': self.cortisol_protocol.is_pfc_suppressed(),
            'resource_stress': self.network_contention.resource_stress
        }
    
    def simulate_experience(self, experience: str, primitives: List[str] = None):
        """
        Symuluje nowe doświadczenie i jego przetwarzanie
        
        Args:
            experience: Opis doświadczenia
            primitives: Wykryte pierwiastki emocjonalne
        """
        atom_id = self.add_sense_atom(experience, primitives or [])
        logger.info(f"💫 Nowe doświadczenie: {experience} | Atom: {atom_id}")
        return atom_id

# ===== PRZYKŁAD UŻYCIA =====

def demo_nsf_migi7g():
    """Demonstracja działania NSF z architekturą MIGI_7G"""
    
    # Inicjalizacja przepływomierza
    nsf = NeuroSemanticFlowmeter(sekundnik_interval=2.0)
    
    # Ustawienie archetypu
    nsf.set_archetype(ArchetypeCore.BOHATER)
    
    # Symulacja doświadczeń
    nsf.simulate_experience(
        "Podjąłem trudną decyzję pomocy komuś potrzebującemu",
        ['POSWIECENIE', 'ALGORYTM_MILOSCI', 'SZCZYPTA_INTELIGENCJI']
    )
    
    nsf.simulate_experience(
        "Czuję strach przed przyszłością i brak nadziei",
        ['BRAK_WIARY_NADZIEI', 'ODOSOBNIENIE_SAMOTNOSC']
    )
    
    nsf.simulate_experience(
        "Odkryłem piękną ideę łączącą sztukę z nauką",
        ['POMYSL_IDEA', 'SZCZYPTA_MAGII', 'WYOBRAZNIA_LOGIKA']
    )
    
    # Uruchomienie na 30 sekund
    import threading
    
    def run_nsf():
        nsf.start_flowmeter()
    
    nsf_thread = threading.Thread(target=run_nsf)
    nsf_thread.daemon = True
    nsf_thread.start()
    
    # Monitorowanie przez 30 sekund
    for i in range(15):
        time.sleep(2)
        stats = nsf.get_stats()
        print(f"\n📈 Cykl {i+1}/15:")
        print(f"   Aktywne atomy: {stats['active_atoms']}")
        print(f"   Archetyp: {stats['current_archetype']}")
        print(f"   Stres (kortyzol): {stats['cortisol_level']:.2f}")
        print(f"   PFC tłumione: {stats['pfc_suppressed']}")
        print(f"   Rekonsolidacje: {stats['reconsolidations']}")
        
        # Zmiana archetypu w połowie
        if i == 7:
            nsf.set_archetype(ArchetypeCore.MEDRZEC)
            print("🎭 Zmiana archetypu na MĘDRZEC")
    
    nsf.stop_flowmeter()
    
    final_stats = nsf.get_stats()
    print("\n🏁 FINALNE STATYSTYKI:")
    print(f"   Łączne cykle: {final_stats['total_cycles']}")
    print(f"   Przetworzone atomy: {final_stats['atoms_processed']}")
    print(f"   Rekonsolidacje: {final_stats['reconsolidations']}")
    print(f"   Tłumienia PFC: {final_stats['pfc_suppressions']}")

if __name__ == "__main__":
    # Konfiguracja loggingu
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("🧠 NEURO-SEMANTYCZNY PRZEPŁYWOMIERZ - MIGI_7G HYBRID")
    print("=" * 60)
    print("Symulacja cyfrowego odzwierciedlenia prawdziwego mózgu")
    print("z 23 pierwiastkami emocjonalnymi i protokołami rekonsolidacji")
    print("=" * 60)
    
    demo_nsf_migi7g()