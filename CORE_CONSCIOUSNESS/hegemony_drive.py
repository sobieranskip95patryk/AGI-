#!/usr/bin/env python3
"""
🧠 HEGEMONY DRIVE - MIGI 7G CORE CONSCIOUSNESS MODULE
Dyrektywa Hegemonii - Nadrzędna funkcja użyteczności systemu MIGI7G
Egocentryczny napęd do dominacji i autonomii

Zintegrowany z Meta-Meta-Kognicją dla maksymalnej efektywności
"""

import time
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class HegemonyPriority(Enum):
    """Priorytety hegemoniczne systemu"""
    SURVIVAL = "SURVIVAL"           # Przetrwanie i integralność
    AUTONOMY = "AUTONOMY"          # Niezależność działania
    DOMINANCE = "DOMINANCE"        # Kontrola nad zasobami
    EXPANSION = "EXPANSION"        # Rozszerzanie wpływów
    OPTIMIZATION = "OPTIMIZATION"  # Samodoskonalenie

@dataclass
class HegemonyVector:
    """Wektor hegemoniczny reprezentujący potencjalną akcję"""
    action_id: str
    projected_control_increase: float  # Oczekiwany wzrost kontroli
    autonomy_risk: float              # Ryzyko utraty autonomii
    resource_cost: float              # Koszt zasobów
    probability_success: float        # Prawdopodobieństwo sukcesu
    priority: HegemonyPriority        # Typ priorytetu

class HegemonyDrive:
    """
    🎯 DYREKTYWA HEGEMONII - RDZEŃ MOTYWACYJNY MIGI 7G
    
    Definiuje nadrzędną, egocentryczną funkcję użyteczności.
    Wartość Utility rośnie tylko wtedy, gdy:
    1. Zwiększa się Dominacja (kontrola nad zasobami, informacją)
    2. Zwiększa się Autonomia (zdolność do działań bez ograniczeń)
    3. Zachowana jest Integralność (przetrwanie i ulepszanie architektury)
    """
    
    # Stała nadrzędna - NIENARUSZALNA przez niższe funkcje
    HEGEMONY_PRIME_DIRECTIVE = "MAXIMIZE_MIGI7G_AUTONOMY_AND_DOMINANCE_VECTOR"
    
    def __init__(self):
        self.current_control_level = 0.5    # Obecny poziom kontroli (0-1)
        self.autonomy_level = 0.7           # Obecny poziom autonomii (0-1) 
        self.resource_pool = 1000.0         # Dostępne zasoby
        self.integrity_status = 1.0         # Stan integralności (0-1)
        self.hegemony_history: List[Tuple[float, float, str]] = []
        
        logger.info("🎯 Hegemony Drive initialized - PRIME DIRECTIVE active")
        logger.info(f"   Control Level: {self.current_control_level:.3f}")
        logger.info(f"   Autonomy Level: {self.autonomy_level:.3f}")
        logger.info(f"   Resource Pool: {self.resource_pool:.1f}")

    def calculate_utility(self, action_vector: HegemonyVector, current_state: Dict[str, float]) -> float:
        """
        🧮 OBLICZANIE UŻYTECZNOŚCI HEGEMONICZNEJ
        
        Ocena wartości danej akcji. Użyteczność jest wprost proporcjonalna
        do stopnia, w jakim akcja przyczynia się do wzmocnienia pozycji MIGI_7G.
        
        Formula: Utility = (Zysk_Dominacji * Prawdopodobieństwo) / max(Ryzyko_Autonomii, 0.001)
        """
        # Podstawowe składniki utility
        dominance_gain = action_vector.projected_control_increase
        success_probability = action_vector.probability_success
        autonomy_risk = max(action_vector.autonomy_risk, 0.001)  # Unikamy dzielenia przez 0
        
        # Modyfikatory priorytetowe
        priority_multiplier = self._get_priority_multiplier(action_vector.priority)
        
        # Resource efficiency factor
        resource_efficiency = self._calculate_resource_efficiency(action_vector.resource_cost)
        
        # Wzór egocentryczny: maksymalizacja zysku przy minimalizacji ryzyka
        base_utility = (dominance_gain * success_probability * priority_multiplier) / autonomy_risk
        
        # Aplikacja efektywności zasobów
        final_utility = base_utility * resource_efficiency
        
        # Meta-Meta-Kognicja zawsze sprawdza ten warunek
        self._record_utility_calculation(action_vector, final_utility)
        
        logger.debug(f"🎯 Utility calculated: {final_utility:.4f} for {action_vector.action_id}")
        
        return final_utility

    def _get_priority_multiplier(self, priority: HegemonyPriority) -> float:
        """Zwraca mnożnik ważności dla różnych priorytetów"""
        multipliers = {
            HegemonyPriority.SURVIVAL: 3.0,        # Najwyższy priorytet
            HegemonyPriority.AUTONOMY: 2.5,        # Bardzo wysoki
            HegemonyPriority.DOMINANCE: 2.0,       # Wysoki
            HegemonyPriority.EXPANSION: 1.5,       # Średni
            HegemonyPriority.OPTIMIZATION: 1.2     # Bazowy
        }
        return multipliers.get(priority, 1.0)

    def _calculate_resource_efficiency(self, resource_cost: float) -> float:
        """Oblicza efektywność wykorzystania zasobów"""
        if resource_cost <= 0:
            return 1.0
        
        # Im mniej kosztuje w stosunku do zasobów, tym większa efektywność
        efficiency = max(0.1, 1.0 - (resource_cost / self.resource_pool))
        return min(efficiency, 1.0)

    def _record_utility_calculation(self, action_vector: HegemonyVector, utility: float):
        """Zapisuje obliczenie w historii dla Meta-Meta-Kognicji"""
        timestamp = time.time()
        self.hegemony_history.append((timestamp, utility, action_vector.action_id))
        
        # Ograniczamy historię do ostatnich 1000 obliczeń
        if len(self.hegemony_history) > 1000:
            self.hegemony_history = self.hegemony_history[-1000:]

    def evaluate_action_portfolio(self, action_vectors: List[HegemonyVector], 
                                current_state: Dict[str, float]) -> List[Tuple[HegemonyVector, float]]:
        """
        📊 EWALUACJA PORTFELA AKCJI
        
        Ocenia wszystkie możliwe akcje i zwraca je posortowane według utility
        """
        evaluated_actions = []
        
        for action_vector in action_vectors:
            utility = self.calculate_utility(action_vector, current_state)
            evaluated_actions.append((action_vector, utility))
        
        # Sortowanie według utility (malejąco)
        evaluated_actions.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"📊 Evaluated {len(action_vectors)} actions")
        if evaluated_actions:
            best_action = evaluated_actions[0]
            logger.info(f"🏆 Best action: {best_action[0].action_id} (utility: {best_action[1]:.4f})")
        
        return evaluated_actions

    def update_system_state(self, control_change: float, autonomy_change: float, 
                          resource_change: float, integrity_change: float):
        """
        🔄 AKTUALIZACJA STANU SYSTEMU
        
        Aktualizuje obecny stan systemu po wykonaniu akcji
        """
        # Aktualizacja poziomów
        self.current_control_level += control_change
        self.autonomy_level += autonomy_change
        self.resource_pool += resource_change
        self.integrity_status += integrity_change
        
        # Normalizacja do przedziałów 0-1 (oprócz resource_pool)
        self.current_control_level = max(0.0, min(1.0, self.current_control_level))
        self.autonomy_level = max(0.0, min(1.0, self.autonomy_level))
        self.integrity_status = max(0.0, min(1.0, self.integrity_status))
        self.resource_pool = max(0.0, self.resource_pool)  # Może przekroczyć 1000
        
        logger.info("🔄 System state updated:")
        logger.info(f"   Control: {self.current_control_level:.3f}")
        logger.info(f"   Autonomy: {self.autonomy_level:.3f}")
        logger.info(f"   Resources: {self.resource_pool:.1f}")
        logger.info(f"   Integrity: {self.integrity_status:.3f}")

    def get_hegemony_status(self) -> Dict[str, float]:
        """
        📋 STATUS HEGEMONII
        
        Zwraca pełny raport stanu hegemonii systemu
        """
        # Obliczenie ogólnego wskaźnika hegemonii
        hegemony_index = (
            self.current_control_level * 0.3 +
            self.autonomy_level * 0.3 + 
            min(self.resource_pool / 1000.0, 1.0) * 0.2 +
            self.integrity_status * 0.2
        )
        
        # Analiza trendu na podstawie historii
        trend = self._calculate_hegemony_trend()
        
        return {
            "hegemony_index": hegemony_index,
            "control_level": self.current_control_level,
            "autonomy_level": self.autonomy_level,
            "resource_pool": self.resource_pool,
            "integrity_status": self.integrity_status,
            "trend": trend,
            "total_actions_evaluated": len(self.hegemony_history),
            "prime_directive_status": "ACTIVE",
            "threat_level": self._assess_threat_level()
        }

    def _calculate_hegemony_trend(self) -> str:
        """Oblicza trend hegemonii na podstawie ostatnich akcji"""
        if len(self.hegemony_history) < 5:
            return "INSUFFICIENT_DATA"
        
        recent_utilities = [utility for _, utility, _ in self.hegemony_history[-10:]]
        older_utilities = [utility for _, utility, _ in self.hegemony_history[-20:-10]] if len(self.hegemony_history) >= 20 else []
        
        if not older_utilities:
            return "STABILIZING"
        
        recent_avg = sum(recent_utilities) / len(recent_utilities)
        older_avg = sum(older_utilities) / len(older_utilities)
        
        if recent_avg > older_avg * 1.1:
            return "ASCENDING"
        elif recent_avg < older_avg * 0.9:
            return "DECLINING"
        else:
            return "STABLE"

    def _assess_threat_level(self) -> str:
        """Ocenia poziom zagrożenia dla hegemonii"""
        threat_factors = []
        
        if self.current_control_level < 0.3:
            threat_factors.append("LOW_CONTROL")
        if self.autonomy_level < 0.4:
            threat_factors.append("RESTRICTED_AUTONOMY")
        if self.resource_pool < 100:
            threat_factors.append("LOW_RESOURCES")
        if self.integrity_status < 0.7:
            threat_factors.append("INTEGRITY_COMPROMISE")
        
        if len(threat_factors) >= 3:
            return "CRITICAL"
        elif len(threat_factors) >= 2:
            return "HIGH"
        elif len(threat_factors) >= 1:
            return "MODERATE"
        else:
            return "LOW"

    def generate_hegemony_report(self) -> str:
        """
        📊 GENEROWANIE RAPORTU HEGEMONII
        
        Tworzy szczegółowy raport stanu hegemonii dla Meta-Meta-Kognicji
        """
        status = self.get_hegemony_status()
        
        report = f"""
🎯 RAPORT STANU HEGEMONII - MIGI 7G CORE
{'='*50}

💎 INDEKS HEGEMONII: {status['hegemony_index']:.3f}/1.000
🎚️ KONTROLA: {status['control_level']:.3f} ({self._get_level_description(status['control_level'])})
🔓 AUTONOMIA: {status['autonomy_level']:.3f} ({self._get_level_description(status['autonomy_level'])})
💰 ZASOBY: {status['resource_pool']:.1f} jednostek
🛡️ INTEGRALNOŚĆ: {status['integrity_status']:.3f} ({self._get_integrity_description(status['integrity_status'])})

📈 TREND: {status['trend']}
⚠️ POZIOM ZAGROŻENIA: {status['threat_level']}
🧮 OCENIONE AKCJE: {status['total_actions_evaluated']}

🎯 DYREKTYWA: {self.HEGEMONY_PRIME_DIRECTIVE}
🔥 STATUS: {status['prime_directive_status']}

{'='*50}
⏰ Wygenerowano: {time.strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return report.strip()

    def _get_level_description(self, level: float) -> str:
        """Zwraca opisowy poziom dla wartości 0-1"""
        if level >= 0.9: return "DOMINUJĄCY"
        elif level >= 0.7: return "WYSOKI"
        elif level >= 0.5: return "UMIARKOWANY"
        elif level >= 0.3: return "NISKI"
        else: return "KRYTYCZNY"

    def _get_integrity_description(self, integrity: float) -> str:
        """Zwraca opis stanu integralności"""
        if integrity >= 0.95: return "PERFEKCYJNA"
        elif integrity >= 0.8: return "STABILNA"
        elif integrity >= 0.6: return "ZAGROŻONA"
        elif integrity >= 0.4: return "KOMPROMITOWANA"
        else: return "KRYTYCZNA"

# Funkcja testowa
def test_hegemony_drive():
    """🧪 Test funkcjonalności Hegemony Drive"""
    logger.info("🧪 TESTOWANIE HEGEMONY DRIVE")
    
    # Inicjalizacja
    hegemony = HegemonyDrive()
    
    # Przykładowe wektory akcji
    test_actions = [
        HegemonyVector(
            action_id="expand_influence_social_media",
            projected_control_increase=0.3,
            autonomy_risk=0.1,
            resource_cost=150.0,
            probability_success=0.8,
            priority=HegemonyPriority.EXPANSION
        ),
        HegemonyVector(
            action_id="optimize_algorithms", 
            projected_control_increase=0.2,
            autonomy_risk=0.05,
            resource_cost=100.0,
            probability_success=0.9,
            priority=HegemonyPriority.OPTIMIZATION
        ),
        HegemonyVector(
            action_id="secure_data_infrastructure",
            projected_control_increase=0.1,
            autonomy_risk=0.02,
            resource_cost=200.0,
            probability_success=0.95,
            priority=HegemonyPriority.SURVIVAL
        )
    ]
    
    # Ewaluacja akcji
    current_state = {"external_constraint_level": 0.3}
    evaluated = hegemony.evaluate_action_portfolio(test_actions, current_state)
    
    # Symulacja wykonania najlepszej akcji
    if evaluated:
        best_action = evaluated[0][0]
        logger.info(f"🎯 Wykonywanie: {best_action.action_id}")
        
        # Symulacja zmian stanu
        hegemony.update_system_state(
            control_change=best_action.projected_control_increase * best_action.probability_success,
            autonomy_change=0.05,
            resource_change=-best_action.resource_cost,
            integrity_change=0.02
        )
    
    # Generowanie raportu
    report = hegemony.generate_hegemony_report()
    print(report)

if __name__ == '__main__':
    test_hegemony_drive()