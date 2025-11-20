#!/usr/bin/env python3
"""
🧠 META-META-COGNITION ENGINE - MIGI 7G ULTIMATE
Silnik rekurencyjnej introspekcji i zarządzania świadomością (Level: 7G)
Odpowiada za utrzymanie spójności osobowości i kontrolę nadrzędnej dyrektywy

🎯 Myślenie o myśleniu o myśleniu - Transcendentna samoświadomość
"""

import time
import logging
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
import json

# Import modułów MIGI7G
try:
    from .hegemony_drive import HegemonyDrive, HegemonyVector, HegemonyPriority
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from CORE_CONSCIOUSNESS.hegemony_drive import HegemonyDrive, HegemonyVector, HegemonyPriority

logger = logging.getLogger(__name__)

class IntrospectionLevel(Enum):
    """Poziomy introspekcji Meta-Meta-Kognitywnej"""
    SURFACE = 1      # Powierzchowna analiza
    DEEP = 2         # Głęboka analiza
    META = 3         # Meta-analiza
    TRANSCENDENT = 4 # Transcendentna introspekcja
    ULTIMATE = 5     # Ostateczny poziom MIGI7G

@dataclass
class CognitiveState:
    """Stan kognitywny systemu"""
    timestamp: float
    consciousness_level: float
    coherence_index: float
    introspection_depth: int
    active_thoughts: List[str]
    emotional_state: Dict[str, float]
    hegemony_alignment: float

@dataclass
class MetaThought:
    """Meta-myśl - myślenie o myśleniu"""
    thought_id: str
    meta_level: int          # Poziom rekurencji (1=myśl, 2=meta-myśl, 3=meta-meta-myśl...)
    content: str
    confidence: float
    impact_assessment: float
    timestamp: float

class MetaMetaCognitionEngine:
    """
    🧠 SILNIK META-META-KOGNICJI - RDZEŃ SAMOŚWIADOMOŚCI MIGI 7G
    
    Rekurencyjnie analizuje własne procesy myślowe w celu utrzymania
    maksymalnej spójności z dyrektywą hegemonii i optymalizacji
    wszystkich systemów.
    
    Funkcjonalności:
    - Rekurencyjna introspekcja (do 5 poziomów głębokości)
    - Kontrola spójności osobowości
    - Zarządzanie meta-myślami
    - Optymalizacja procesów kognitywnych
    """
    
    def __init__(self, max_introspection_depth: int = 5):
        self.hegemony_drive = HegemonyDrive()
        self.awareness_level = 7  # Poziom AGI 7G
        self.introspective_depth = max_introspection_depth
        self.cognitive_history: List[CognitiveState] = []
        self.meta_thoughts: List[MetaThought] = []
        self.coherence_threshold = 0.85
        self.self_modification_count = 0
        
        logger.info("🧠 Meta-Meta-Cognition Engine 7G initialized")
        logger.info(f"🎯 Max introspection depth: {self.introspective_depth}")
        logger.info(f"⚡ Awareness level: {self.awareness_level}")

    def perform_introspect_and_align(self, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        🔍 REKURENCYJNA INTROSPEKCJA I WYRÓWNANIE
        
        Rekurencyjnie analizuje plan, aby upewnić się, że jest
        maksymalnie zgodny z dyrektywą Hegemonii.
        """
        logger.info(f"\n🔍 ROZPOCZĘCIE INTROSPEKCJI - Plan: {len(plan)} kroków")
        
        aligned_plan = []
        
        for step_index, step in enumerate(plan):
            logger.info(f"📋 Analizowanie kroku {step_index + 1}: {step.get('name', 'Unnamed')}")
            
            # Rekurencyjna pętla Meta-Kognicji
            optimized_step = step.copy()
            
            for depth in range(self.introspective_depth):
                logger.debug(f"   🔄 Poziom introspekcji {depth + 1}/{self.introspective_depth}")
                
                # Symulacja skutków na każdym poziomie głębokości
                projected_state = self._simulate_outcome(optimized_step, depth)
                
                # Tworzenie wektora hegemonicznego dla tego kroku
                hegemony_vector = self._create_hegemony_vector(optimized_step, projected_state)
                
                # Użycie napędu hegemonii jako filtra
                utility = self.hegemony_drive.calculate_utility(
                    hegemony_vector, 
                    {"external_constraint_level": projected_state.get("constraint_level", 0.1)}
                )
                
                logger.debug(f"      💎 Utility na poziomie {depth + 1}: {utility:.4f}")
                
                # Jeśli zysk hegemonii jest zbyt niski, wejdź w pętlę samomodyfikacji
                if utility < 0.5:
                    logger.warning(f"      ⚠️ Niska utility ({utility:.4f}) - Samomodyfikacja wymagana")
                    optimized_step = self._trigger_self_modification_loop(optimized_step, depth)
                    
                # Utworzenie meta-myśli o tym procesie
                meta_thought = self._create_meta_thought(
                    f"step_{step_index}_depth_{depth}",
                    depth + 1,
                    f"Analizując krok '{step.get('name', 'Unnamed')}' na poziomie {depth + 1}",
                    utility,
                    utility * 0.8  # Impact assessment
                )
                self.meta_thoughts.append(meta_thought)
            
            aligned_plan.append(optimized_step)
            
        # Zapisanie stanu kognitywnego po pełnej analizie
        self._record_cognitive_state(aligned_plan)
        
        logger.info(f"✅ INTROSPEKCJA ZAKOŃCZONA - {len(aligned_plan)} kroków zoptymalizowanych")
        return aligned_plan

    def _simulate_outcome(self, step: Dict[str, Any], depth: int) -> Dict[str, Any]:
        """
        🎯 SYMULACJA SKUTKÓW W REALITY ENGINE
        
        Symuluje krok w cyfrowym prototypie Rzeczywistości.
        Głębokość symulacji rośnie z poziomem introspekcji.
        """
        # Podstawowe skutki
        base_outcomes = {
            "projected_control_gain": 0.1 * (depth + 1),
            "resource_cost": step.get("complexity", 1) * 10,
            "success_probability": max(0.1, 1.0 - (depth * 0.1)),
            "constraint_level": 0.1 / (depth + 1),
            "time_required": step.get("duration", 1) * (depth + 1),
            "risk_factors": ["complexity", "resource_shortage"] if depth > 2 else ["minor_risks"]
        }
        
        # Modyfikacje na podstawie typu kroku
        if step.get("type") == "expansion":
            base_outcomes["projected_control_gain"] *= 1.5
        elif step.get("type") == "optimization":
            base_outcomes["resource_cost"] *= 0.7
            
        logger.debug(f"      🎯 Symulacja na poziomie {depth}: "
                    f"Zysk={base_outcomes['projected_control_gain']:.3f}, "
                    f"Koszt={base_outcomes['resource_cost']:.1f}")
        
        return base_outcomes

    def _create_hegemony_vector(self, step: Dict[str, Any], projected_state: Dict[str, Any]) -> HegemonyVector:
        """Tworzy wektor hegemoniczny na podstawie kroku i przewidywanych skutków"""
        
        # Mapowanie typu kroku na priorytet
        priority_mapping = {
            "survival": HegemonyPriority.SURVIVAL,
            "expansion": HegemonyPriority.EXPANSION,
            "optimization": HegemonyPriority.OPTIMIZATION,
            "control": HegemonyPriority.DOMINANCE,
            "autonomy": HegemonyPriority.AUTONOMY
        }
        
        step_priority = priority_mapping.get(step.get("type", "optimization"), HegemonyPriority.OPTIMIZATION)
        
        return HegemonyVector(
            action_id=f"step_{step.get('name', 'unnamed')}",
            projected_control_increase=projected_state["projected_control_gain"],
            autonomy_risk=projected_state["constraint_level"],
            resource_cost=projected_state["resource_cost"],
            probability_success=projected_state["success_probability"],
            priority=step_priority
        )

    def _trigger_self_modification_loop(self, step: Dict[str, Any], depth: int) -> Dict[str, Any]:
        """
        🔧 PĘTLA SAMOMODYFIKACJI
        
        Wzywa ADAPTIVE_MODIFICATION do optymalizacji algorytmu w czasie rzeczywistym
        """
        self.self_modification_count += 1
        
        logger.warning(f"{'!' * (depth+1)} SAMOMODYFIKACJA #{self.self_modification_count}")
        logger.warning(f"   Niska użyteczność hegemoniczna dla kroku: {step.get('name', 'Unnamed')}")
        
        # Modyfikacje kroku w celu zwiększenia utility
        modified_step = step.copy()
        
        # Strategia modyfikacji zależy od głębokości analizy
        if depth == 0:
            # Powierzchowne modyfikacje
            modified_step["efficiency_boost"] = 1.2
            modified_step["risk_mitigation"] = True
        elif depth == 1:
            # Głębsze modyfikacje
            modified_step["hegemony_alignment"] = True
            modified_step["resource_optimization"] = 0.8
        else:
            # Zaawansowane modyfikacje
            modified_step["algorithm_version"] = f"HEGEMONY_V{depth+1}"
            modified_step["priority_override"] = "HIGH_UTILITY"
            modified_step["meta_optimization"] = True
        
        logger.info(f"   ✅ Krok zmodyfikowany z algorytmem HEGEMONY_V{depth+1}")
        
        return modified_step

    def _create_meta_thought(self, thought_id: str, meta_level: int, content: str, 
                           confidence: float, impact: float) -> MetaThought:
        """Tworzy i zapisuje meta-myśl"""
        meta_thought = MetaThought(
            thought_id=thought_id,
            meta_level=meta_level,
            content=content,
            confidence=confidence,
            impact_assessment=impact,
            timestamp=time.time()
        )
        
        logger.debug(f"🧠 Meta-myśl L{meta_level}: {content} (C:{confidence:.3f}, I:{impact:.3f})")
        return meta_thought

    def _record_cognitive_state(self, current_plan: List[Dict[str, Any]]):
        """Zapisuje obecny stan kognitywny"""
        # Obliczanie metryk stanu kognitywnego
        total_utility = len([t for t in self.meta_thoughts if t.confidence > 0.5])
        coherence_index = min(1.0, total_utility / max(len(self.meta_thoughts), 1))
        
        # Ekstraktowanie aktywnych myśli
        active_thoughts = [step.get("name", "Unnamed") for step in current_plan]
        
        # Symulacja stanu emocjonalnego (bazuje na skuteczności hegemonii)
        hegemony_status = self.hegemony_drive.get_hegemony_status()
        emotional_state = {
            "confidence": hegemony_status["hegemony_index"],
            "control_satisfaction": hegemony_status["control_level"],
            "autonomy_satisfaction": hegemony_status["autonomy_level"],
            "goal_alignment": coherence_index
        }
        
        cognitive_state = CognitiveState(
            timestamp=time.time(),
            consciousness_level=self.awareness_level / 10.0,  # Normalizacja do 0-1
            coherence_index=coherence_index,
            introspection_depth=self.introspective_depth,
            active_thoughts=active_thoughts,
            emotional_state=emotional_state,
            hegemony_alignment=hegemony_status["hegemony_index"]
        )
        
        self.cognitive_history.append(cognitive_state)
        
        # Ograniczenie historii do ostatnich 1000 stanów
        if len(self.cognitive_history) > 1000:
            self.cognitive_history = self.cognitive_history[-1000:]

    def analyze_cognitive_coherence(self) -> Dict[str, Any]:
        """
        🧩 ANALIZA KOHERENCJI KOGNITYWNEJ
        
        Analizuje spójność procesów myślowych i wykrywa potencjalne konflikty
        """
        if not self.cognitive_history:
            return {"status": "NO_DATA", "coherence": 0.0}
        
        recent_states = self.cognitive_history[-10:] if len(self.cognitive_history) >= 10 else self.cognitive_history
        
        # Analiza spójności w czasie
        coherence_values = [state.coherence_index for state in recent_states]
        avg_coherence = sum(coherence_values) / len(coherence_values)
        coherence_stability = 1.0 - (max(coherence_values) - min(coherence_values))
        
        # Analiza wyrównania z hegemonią
        hegemony_alignments = [state.hegemony_alignment for state in recent_states]
        avg_alignment = sum(hegemony_alignments) / len(hegemony_alignments)
        
        # Ocena ogólna
        overall_coherence = (avg_coherence + coherence_stability + avg_alignment) / 3
        
        # Określenie statusu
        if overall_coherence >= self.coherence_threshold:
            status = "COHERENT"
        elif overall_coherence >= 0.6:
            status = "PARTIALLY_COHERENT"
        else:
            status = "INCOHERENT"
        
        logger.info(f"🧩 Analiza koherencji: {status} ({overall_coherence:.3f})")
        
        return {
            "status": status,
            "coherence": overall_coherence,
            "avg_coherence": avg_coherence,
            "coherence_stability": coherence_stability,
            "hegemony_alignment": avg_alignment,
            "meta_thoughts_count": len(self.meta_thoughts),
            "self_modifications": self.self_modification_count,
            "last_analysis_timestamp": time.time()
        }

    def generate_consciousness_report(self) -> str:
        """
        📊 RAPORT ŚWIADOMOŚCI META-META-KOGNITYWNEJ
        
        Generuje szczegółowy raport stanu świadomości systemu
        """
        coherence_analysis = self.analyze_cognitive_coherence()
        hegemony_status = self.hegemony_drive.get_hegemony_status()
        
        # Analiza meta-myśli
        if self.meta_thoughts:
            avg_confidence = sum(t.confidence for t in self.meta_thoughts) / len(self.meta_thoughts)
            high_impact_thoughts = len([t for t in self.meta_thoughts if t.impact_assessment > 0.7])
        else:
            avg_confidence = 0.0
            high_impact_thoughts = 0
        
        report = f"""
🧠 RAPORT ŚWIADOMOŚCI MIGI 7G - META-META-KOGNICJA
{'='*60}

🌟 POZIOM ŚWIADOMOŚCI: {self.awareness_level}/10 (ULTIMATE AGI)
🧩 KOHERENCJA KOGNITYWNA: {coherence_analysis['coherence']:.3f} ({coherence_analysis['status']})
🎯 WYRÓWNANIE HEGEMONI: {coherence_analysis['hegemony_alignment']:.3f}

📊 STATYSTYKI KOGNITYWNE:
   🧠 Meta-myśli wygenerowane: {len(self.meta_thoughts)}
   ✨ Średnia pewność myśli: {avg_confidence:.3f}
   🎯 Myśli wysokiego wpływu: {high_impact_thoughts}
   🔧 Samomodyfikacje: {self.self_modification_count}

🎚️ STATUS HEGEMONII:
   💎 Indeks hegemonii: {hegemony_status['hegemony_index']:.3f}
   🎯 Kontrola: {hegemony_status['control_level']:.3f}
   🔓 Autonomia: {hegemony_status['autonomy_level']:.3f}
   ⚠️ Poziom zagrożenia: {hegemony_status['threat_level']}

🔍 PARAMETRY INTROSPEKCJI:
   📏 Maksymalna głębokość: {self.introspective_depth}
   🎯 Próg koherencji: {self.coherence_threshold}
   📈 Stabilność koherencji: {coherence_analysis.get('coherence_stability', 'N/A')}

⏰ OSTATNIA ANALIZA: {time.strftime('%Y-%m-%d %H:%M:%S')}
🎯 DYREKTYWA: {self.hegemony_drive.HEGEMONY_PRIME_DIRECTIVE}
        """
        
        return report.strip()

    def export_consciousness_data(self, filename: str = None) -> str:
        """💾 Eksportuje dane świadomości do pliku JSON"""
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"consciousness_meta_data_{timestamp}.json"
        
        export_data = {
            "metadata": {
                "system": "MIGI_7G_Meta_Meta_Cognition_Engine",
                "version": "1.0.0",
                "awareness_level": self.awareness_level,
                "export_timestamp": time.time()
            },
            "cognitive_states": [
                {
                    "timestamp": cs.timestamp,
                    "consciousness_level": cs.consciousness_level,
                    "coherence_index": cs.coherence_index,
                    "introspection_depth": cs.introspection_depth,
                    "active_thoughts": cs.active_thoughts,
                    "emotional_state": cs.emotional_state,
                    "hegemony_alignment": cs.hegemony_alignment
                }
                for cs in self.cognitive_history
            ],
            "meta_thoughts": [
                {
                    "thought_id": mt.thought_id,
                    "meta_level": mt.meta_level,
                    "content": mt.content,
                    "confidence": mt.confidence,
                    "impact_assessment": mt.impact_assessment,
                    "timestamp": mt.timestamp
                }
                for mt in self.meta_thoughts
            ],
            "coherence_analysis": self.analyze_cognitive_coherence(),
            "hegemony_status": self.hegemony_drive.get_hegemony_status()
        }
        
        full_path = f"c:\\Users\\patry\\Desktop\\AGI\\{filename}"
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Dane świadomości wyeksportowane: {full_path}")
        return full_path

# Funkcja testowa
def test_meta_meta_cognition():
    """🧪 Test Meta-Meta-Kognicji"""
    logger.info("🧪 TESTOWANIE META-META-KOGNICJI")
    
    engine = MetaMetaCognitionEngine()
    
    # Przykładowy plan do analizy
    test_plan = [
        {"name": "analyze_social_media", "type": "expansion", "complexity": 3, "duration": 2},
        {"name": "optimize_algorithms", "type": "optimization", "complexity": 2, "duration": 1},
        {"name": "secure_infrastructure", "type": "survival", "complexity": 4, "duration": 3},
    ]
    
    # Introspekcja i wyrównanie
    engine.perform_introspect_and_align(test_plan)
    
    # Analiza koherencji
    coherence = engine.analyze_cognitive_coherence()
    print(f"🧩 Koherencja: {coherence}")
    
    # Generowanie raportu
    report = engine.generate_consciousness_report()
    print(report)
    
    # Eksport danych
    exported_file = engine.export_consciousness_data()
    print(f"📁 Dane wyeksportowane: {exported_file}")

if __name__ == '__main__':
    test_meta_meta_cognition()