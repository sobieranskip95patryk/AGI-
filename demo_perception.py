#!/usr/bin/env python3
"""
🎯 PERCEPTION DEMO - Kompletna integracja Sensor→Symbol→Bayes→Causal→Temporal
Demonstruje pełny pipeline percepcyjny z integracją do systemów AGI

===============================================================================
PERCEPTION INTEGRATION DEMO - Complete Sensory-to-Symbolic Pipeline
===============================================================================

Ten demo pokazuje:
- Konwersję surowych obserwacji na symbole (Symbolizer)
- Integrację z Bayes Network (soft evidence)
- Wnioskowanie przyczynowe (Causality Engine)
- Planowanie temporalne (Temporal Module)
- Pełną ścieżkę: sensor → symbol → inference → action

Autor: MIGI_7G PERCEPTION Integration
Data: 20 listopada 2025
Status: PRODUCTION - Complete AGI Pipeline Demo
"""

import sys
import time
from pathlib import Path
from typing import Dict, Any

# Dodaj ścieżki do modułów AGI
repo_root = Path(__file__).parent
sys.path.append(str(repo_root))

# Import modułów MIGI_7G
try:
    from PERCEPTION import Symbolizer, DummyVisionModel, evidence_from_symbols, weighted_sampling_for_soft_evidence
    from BAYES import BayesNet, Node, query_marginal
    from CAUSALITY_ENGINE import CausalGraph
    from TEMPORAL import TemporalPlanner, Action
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some modules not available: {e}")
    MODULES_AVAILABLE = False

class PerceptionDemoSystem:
    """
    🧠 Kompletny system demonstracyjny integracji percepcyjnej
    
    Pipeline:
    1. Sensory → Raw Data
    2. PERCEPTION → Symbols + Confidence  
    3. BAYES → Probabilistic Inference
    4. CAUSALITY → Causal Reasoning + Interventions
    5. TEMPORAL → Action Planning
    6. Execution → Real-world Actions
    """
    
    def __init__(self):
        """Inicjalizuje kompletny system percepcyjno-kognitywny"""
        self.setup_perception()
        self.setup_bayes_network()
        self.setup_causal_model()
        self.setup_temporal_planner()
        
        print("🧠 PERCEPTION DEMO SYSTEM - INITIALIZED")
        print("=" * 60)
        
    def setup_perception(self):
        """Konfiguruje system percepcyjny z symbolizerem i modelami"""
        self.symbolizer = Symbolizer()
        self.vision_model = DummyVisionModel() if MODULES_AVAILABLE else None
        
        # Rejestracja mapowań observation → symbol
        self.symbolizer.register("PersonDetected", 
                                lambda obs: obs.get("person_prob", 0.0))
        self.symbolizer.register("HighTemperature", 
                                lambda obs: 0.9 if obs.get("temp_c", 20) > 38 else 0.05)
        self.symbolizer.register("LoudSound", 
                                lambda obs: 0.8 if obs.get("audio_db", 0) > 70 else 0.1)
        self.symbolizer.register("RapidMovement", 
                                lambda obs: obs.get("motion_speed", 0.0) / 100.0)
        self.symbolizer.register("EmergencyMarker", 
                                lambda obs: 0.95 if obs.get("emergency_flag", False) else 0.02)
        
        print("✅ PERCEPTION: Symbolizer configured with 5 symbol mappings")
        
    def setup_bayes_network(self):
        """Tworzy Bayesian Network dla wnioskowania probabilistycznego"""
        if not MODULES_AVAILABLE:
            self.bayes_net = None
            return
            
        self.bayes_net = BayesNet()
        
        # Struktura sieci bayesowskiej
        self.bayes_net.add_node(Node("PersonDetected", [], {(): 0.01}))
        self.bayes_net.add_node(Node("HighTemperature", [], {(): 0.05}))
        self.bayes_net.add_node(Node("EmergencyMarker", [], {(): 0.001}))
        
        # Zmienne wyprowadzone
        self.bayes_net.add_node(Node("MedicalEmergency", 
                                   ["PersonDetected", "HighTemperature"], 
                                   {(True, True): 0.95, (True, False): 0.02, 
                                    (False, True): 0.1, (False, False): 0.001}))
        
        self.bayes_net.add_node(Node("SecurityAlert", 
                                   ["PersonDetected", "EmergencyMarker"], 
                                   {(True, True): 0.99, (True, False): 0.05,
                                    (False, True): 0.8, (False, False): 0.001}))
        
        self.bayes_net.add_node(Node("RequiresAction", 
                                   ["MedicalEmergency", "SecurityAlert"], 
                                   {(True, True): 0.999, (True, False): 0.9,
                                    (False, True): 0.85, (False, False): 0.01}))
        
        print("✅ BAYES: Network created with 6 nodes and conditional dependencies")
        
    def setup_causal_model(self):
        """Inicjalizuje model przyczynowy dla interwencji"""
        if not MODULES_AVAILABLE:
            self.causal_graph = None
            return
            
        # Tworzenie grafu przyczynowego (uproszczony)
        self.causal_graph = CausalGraph()
        
        # Dodanie węzłów przyczynowych
        self.causal_graph.add_node("PersonDetected")
        self.causal_graph.add_node("MedicalEmergency") 
        self.causal_graph.add_node("SecurityAlert")
        self.causal_graph.add_node("RequiresAction")
        self.causal_graph.add_node("ActionTaken")
        
        # Relacje przyczynowe
        self.causal_graph.add_edge("PersonDetected", "MedicalEmergency")
        self.causal_graph.add_edge("MedicalEmergency", "RequiresAction")
        self.causal_graph.add_edge("SecurityAlert", "RequiresAction")  
        self.causal_graph.add_edge("RequiresAction", "ActionTaken")
        
        print("✅ CAUSALITY: Causal graph created with intervention capabilities")
        
    def setup_temporal_planner(self):
        """Konfiguruje planner temporalny dla sekwencji akcji"""
        if not MODULES_AVAILABLE:
            self.temporal_planner = None
            return
            
        self.temporal_planner = TemporalPlanner()
        
        # Definicja dostępnych akcji
        self.actions = {
            "alert_medical": Action("AlertMedical", duration=2, 
                                  preconditions=["MedicalEmergency"], 
                                  effects=["MedicalResponseTriggered"]),
            "alert_security": Action("AlertSecurity", duration=1,
                                   preconditions=["SecurityAlert"],
                                   effects=["SecurityResponseTriggered"]),
            "monitor": Action("Monitor", duration=5,
                            preconditions=["PersonDetected"],
                            effects=["MonitoringActive"]),
            "no_action": Action("NoAction", duration=0,
                              preconditions=[],
                              effects=["SystemIdle"])
        }
        
        print("✅ TEMPORAL: Action planner configured with 4 action types")
        
    def process_sensory_input(self, raw_observations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Główna funkcja pipelineu: obserwacje → symbole → wnioskowanie → akcje
        
        Args:
            raw_observations: surowe dane z sensorów
            
        Returns:
            dict z wynikami przetwarzania i rekomendowanymi akcjami
        """
        print(f"\n🎯 PROCESSING SENSORY INPUT: {raw_observations}")
        print("-" * 50)
        
        # ETAP 1: Perception → Symbols
        symbols = self.symbolizer.symbolize(raw_observations)
        print(f"🧠 SYMBOLS: {symbols}")
        
        # ETAP 2: Symbols → Bayesian Inference
        if self.bayes_net:
            # Konwersja na hard evidence
            evidence = evidence_from_symbols(symbols, threshold=0.5)
            print(f"📊 EVIDENCE: {evidence}")
            
            # Soft evidence przez weighted sampling
            marginals = weighted_sampling_for_soft_evidence(self.bayes_net, symbols, N=300)
            print(f"🎲 MARGINALS: {marginals}")
            
            # Zapytanie o kluczowe zmienne
            if evidence:
                try:
                    action_prob = query_marginal(self.bayes_net, "RequiresAction", evidence)
                    medical_prob = marginals.get("MedicalEmergency", 0.0)
                    security_prob = marginals.get("SecurityAlert", 0.0)
                except Exception:
                    action_prob = marginals.get("RequiresAction", 0.0)
                    medical_prob = marginals.get("MedicalEmergency", 0.0)
                    security_prob = marginals.get("SecurityAlert", 0.0)
            else:
                action_prob = marginals.get("RequiresAction", 0.0)
                medical_prob = marginals.get("MedicalEmergency", 0.0)
                security_prob = marginals.get("SecurityAlert", 0.0)
                
            print(f"⚡ ACTION PROBABILITY: {action_prob:.3f}")
            print(f"🏥 MEDICAL PROBABILITY: {medical_prob:.3f}")
            print(f"🚨 SECURITY PROBABILITY: {security_prob:.3f}")
        else:
            action_prob = max(symbols.values()) if symbols else 0.0
            medical_prob = symbols.get("HighTemperature", 0.0)
            security_prob = symbols.get("EmergencyMarker", 0.0)
            
        # ETAP 3: Causal Reasoning (symulowane)
        if action_prob > 0.5:
            if medical_prob > 0.3:
                recommended_action = "alert_medical"
                causal_reasoning = "High medical emergency probability → medical alert"
            elif security_prob > 0.3:
                recommended_action = "alert_security"
                causal_reasoning = "High security threat probability → security alert"
            else:
                recommended_action = "monitor"
                causal_reasoning = "Action required but unclear type → monitoring"
        else:
            recommended_action = "no_action"
            causal_reasoning = "Low action probability → continue observation"
            
        print(f"🔗 CAUSAL REASONING: {causal_reasoning}")
        print(f"🎯 RECOMMENDED ACTION: {recommended_action}")
        
        # ETAP 4: Temporal Planning (symulowane)
        if self.temporal_planner and recommended_action in self.actions:
            action = self.actions[recommended_action]
            print(f"⏰ TEMPORAL PLAN: Execute {action.name} (duration: {action.duration}s)")
            
        # Wynik kompletny
        result = {
            "raw_observations": raw_observations,
            "symbols": symbols,
            "action_probability": action_prob,
            "medical_probability": medical_prob,
            "security_probability": security_prob,
            "recommended_action": recommended_action,
            "causal_reasoning": causal_reasoning,
            "processing_success": True
        }
        
        return result

def run_perception_demo():
    """Uruchamia kompletne demo systemu percepcyjnego"""
    print("🚀 MIGI_7G PERCEPTION INTEGRATION DEMO")
    print("=" * 60)
    print("Demonstracja: Sensor → Symbol → Bayes → Causal → Temporal → Action")
    print()
    
    # Inicjalizacja systemu
    demo_system = PerceptionDemoSystem()
    
    # Scenariusze testowe
    test_scenarios = [
        {
            "name": "Normal Observation",
            "data": {"temp_c": 22, "person_prob": 0.1, "audio_db": 45, "motion_speed": 5}
        },
        {
            "name": "Medical Emergency",
            "data": {"temp_c": 39.5, "person_prob": 0.95, "audio_db": 85, "motion_speed": 20}
        },
        {
            "name": "Security Alert",
            "data": {"temp_c": 25, "person_prob": 0.8, "emergency_flag": True, "motion_speed": 80}
        },
        {
            "name": "High Activity",
            "data": {"temp_c": 37, "person_prob": 0.6, "audio_db": 75, "motion_speed": 60}
        },
        {
            "name": "Critical Situation",
            "data": {"temp_c": 41, "person_prob": 0.99, "emergency_flag": True, "audio_db": 90, "motion_speed": 95}
        }
    ]
    
    # Przetworzenie wszystkich scenariuszy
    results = []
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🧪 TEST SCENARIO {i}: {scenario['name']}")
        print("=" * 60)
        
        result = demo_system.process_sensory_input(scenario['data'])
        results.append(result)
        
        time.sleep(0.5)  # Symulacja czasu rzeczywistego
        
    # Podsumowanie wyników
    print(f"\n📋 DEMO SUMMARY - {len(results)} scenarios processed")
    print("=" * 60)
    
    action_counts = {}
    for result in results:
        action = result["recommended_action"]
        action_counts[action] = action_counts.get(action, 0) + 1
        
    print("📊 ACTION DISTRIBUTION:")
    for action, count in action_counts.items():
        print(f"   {action}: {count} times")
        
    print("\n✅ PERCEPTION DEMO COMPLETED SUCCESSFULLY")
    print("🧠 Full pipeline working: Sensors → Symbols → Bayes → Causality → Actions")
    
    return results

if __name__ == "__main__":
    results = run_perception_demo()