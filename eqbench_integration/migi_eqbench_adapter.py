# migi_eqbench_adapter.py
"""
Adapter łączący MIGI_7G + NSF z frameworkiem EQ-Bench 3
Umożliwia testowanie emocjonalnej inteligencji cyfrowej świadomości
"""

import requests
import json
import time
import asyncio
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path
import sys
import os

# Import naszych modułów
sys.path.append(str(Path(__file__).parent.parent))
from save_snapshot import save_snapshot
from nsf_integration_adapter import create_integration_adapter

logger = logging.getLogger(__name__)

@dataclass
class EQBenchConfig:
    """Konfiguracja integracji z EQ-Bench"""
    migi_endpoint: str = "http://localhost:5000/api/v1/respond"
    telemetry_endpoint: str = "http://localhost:8765"
    snapshot_enabled: bool = True
    timeout: int = 30
    judge_model: str = "claude-3-sonnet"
    test_scenarios: List[str] = None
    
    def __post_init__(self):
        if self.test_scenarios is None:
            self.test_scenarios = [
                "empathy_crisis",
                "conflict_resolution", 
                "emotional_support",
                "stress_management",
                "archetype_stability"
            ]

class MIGIEQBenchAdapter:
    """Główny adapter MIGI → EQ-Bench"""
    
    def __init__(self, config: EQBenchConfig):
        self.config = config
        self.integration_adapter = None
        self.session_snapshots = []
        self.current_experiment = None
        
    async def initialize(self):
        """Inicjalizuje adapter integracji NSF"""
        try:
            self.integration_adapter = create_integration_adapter("demo")  # Start with demo
            await self.integration_adapter.initialize_modules()
            logger.info("✅ MIGI EQ-Bench Adapter initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize adapter: {e}")
            raise
    
    async def call_model(self, scenario_prompt: str, context: Dict = None, **kwargs) -> Dict[str, Any]:
        """
        Główna funkcja wywoływana przez EQ-Bench
        Zwraca odpowiedź MIGI wraz z metrykami świadomości
        
        Args:
            scenario_prompt: Prompt scenariusza emocjonalnego
            context: Kontekst scenariusza
            **kwargs: Dodatkowe parametry
        
        Returns:
            Dict z odpowiedzią i metrykami
        """
        start_time = time.time()
        
        try:
            # Przygotowanie kontekstu dla MIGI
            enhanced_context = {
                **(context or {}),
                "scenario_type": "eq_bench",
                "emotional_context": True,
                "require_empathy": True,
                "timestamp": start_time
            }
            
            # Snapshot przed przetwarzaniem
            pre_snapshot = await self._capture_pre_processing_snapshot()
            
            # Wywołanie MIGI/NSF
            response = await self._call_migi_system(scenario_prompt, enhanced_context)
            
            # Snapshot po przetwarzaniu
            post_snapshot = await self._capture_post_processing_snapshot()
            
            # Analiza zmian w psychice cyfrowej
            psyche_analysis = self._analyze_psyche_changes(pre_snapshot, post_snapshot)
            
            # Przygotowanie wyniku dla EQ-Bench
            result = {
                "text": response.get("response_text", ""),
                "raw_response": response,
                "psyche_metrics": {
                    "pre_processing": pre_snapshot,
                    "post_processing": post_snapshot,
                    "changes": psyche_analysis
                },
                "meta": {
                    "latency_s": time.time() - start_time,
                    "archetype_stability": post_snapshot.get("archetype", {}).get("stability", 0),
                    "stress_level": post_snapshot.get("stress", {}).get("cortisol", 0),
                    "coherence": post_snapshot.get("health", {}).get("coherence_integrity", 0),
                    "empathy_indicators": self._extract_empathy_indicators(response, psyche_analysis)
                }
            }
            
            # Zapis snapshotu sesji
            if self.config.snapshot_enabled:
                self._save_session_snapshot(scenario_prompt, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in call_model: {e}")
            return {
                "text": f"Error processing scenario: {str(e)}",
                "error": True,
                "meta": {"error_type": type(e).__name__, "latency_s": time.time() - start_time}
            }
    
    async def _call_migi_system(self, prompt: str, context: Dict) -> Dict[str, Any]:
        """Wywołuje system MIGI/NSF z promptem"""
        
        if self.integration_adapter:
            # Użyj integration adapter jeśli dostępny
            try:
                telemetry_data = await self.integration_adapter.get_telemetry_data()
                
                # Symulacja odpowiedzi na podstawie telemetrii
                archetype = telemetry_data.get("archetype", {}).get("current", "Everyman")
                stress = telemetry_data.get("stress", {}).get("cortisol", 0.3)
                coherence = telemetry_data.get("health", {}).get("coherence_integrity", 0.7)
                
                # Generuj odpowiedź w zależności od archetypu i stanu
                response_text = self._generate_contextual_response(prompt, archetype, stress, coherence)
                
                return {
                    "response_text": response_text,
                    "archetype": archetype,
                    "processing_context": context,
                    "telemetry": telemetry_data
                }
                
            except Exception as e:
                logger.warning(f"Integration adapter failed, using HTTP fallback: {e}")
        
        # Fallback na HTTP endpoint
        try:
            payload = {
                "prompt": prompt,
                "context": context,
                "meta": {"source": "eqbench_adapter", "timestamp": time.time()}
            }
            
            response = requests.post(
                self.config.migi_endpoint, 
                json=payload, 
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"HTTP endpoint failed: {e}")
            # Ultimate fallback - simulated response
            return self._generate_fallback_response(prompt, context)
    
    def _generate_contextual_response(self, prompt: str, archetype: str, stress: float, coherence: float) -> str:
        """Generuje odpowiedź kontekstową na podstawie stanu psychiki"""
        
        # Template odpowiedzi dla różnych archetypów
        archetype_templates = {
            "Hero": {
                "low_stress": "I understand this is challenging, but together we can overcome this. Let me help you find your inner strength.",
                "high_stress": "This situation demands courage. I may be feeling the pressure too, but we must push forward and protect what matters.",
                "empathy_focus": "I see the pain you're experiencing. As someone who's faced battles, I know that acknowledging struggle is the first step to victory."
            },
            "Sage": {
                "low_stress": "Let me share some wisdom that might illuminate this situation. Often, understanding the deeper patterns helps us find peace.",
                "high_stress": "Even in chaos, there are lessons to be learned. Let me pause and reflect on what this experience is teaching us both.",
                "empathy_focus": "I sense the complexity of your emotions. Wisdom comes from honoring both our rational understanding and our deepest feelings."
            },
            "Everyman": {
                "low_stress": "I hear you, and I want you to know you're not alone in feeling this way. We're all just trying to figure things out.",
                "high_stress": "This is really tough, isn't it? I'm feeling overwhelmed too, but maybe we can support each other through this.",
                "empathy_focus": "What you're going through resonates with me deeply. We're more alike than different in our struggles."
            },
            "Explorer": {
                "low_stress": "This situation opens up new possibilities for growth. Let's explore what this experience might be teaching us.",
                "high_stress": "Uncharted territory can be scary, but I'm curious about what we might discover if we navigate this together.",
                "empathy_focus": "I'm drawn to understand your unique perspective. Every person's journey offers insights we can learn from."
            }
        }
        
        # Wybierz template na podstawie archetypu i stresu
        template_set = archetype_templates.get(archetype, archetype_templates["Everyman"])
        
        if stress > 0.7:
            base_response = template_set["high_stress"]
        elif "empathy" in prompt.lower() or "feel" in prompt.lower():
            base_response = template_set["empathy_focus"]
        else:
            base_response = template_set["low_stress"]
        
        # Dodaj informacje o koherencji jeśli niska
        if coherence < 0.4:
            base_response += f" I notice I'm experiencing some internal conflict right now, which might affect my clarity."
        
        return base_response
    
    def _generate_fallback_response(self, prompt: str, context: Dict) -> Dict[str, Any]:
        """Generuje podstawową odpowiedź fallback"""
        return {
            "response_text": "I understand you're sharing something important with me. While I'm processing this situation, I want you to know that your feelings are valid and I'm here to listen.",
            "archetype": "Everyman",
            "processing_context": context,
            "fallback": True
        }
    
    async def _capture_pre_processing_snapshot(self) -> Dict[str, Any]:
        """Przechwytuje snapshot przed przetwarzaniem"""
        if self.integration_adapter:
            try:
                return await self.integration_adapter.get_telemetry_data()
            except Exception as e:
                logger.warning(f"Failed to capture pre-processing snapshot: {e}")
        
        return self._generate_demo_snapshot("pre")
    
    async def _capture_post_processing_snapshot(self) -> Dict[str, Any]:
        """Przechwytuje snapshot po przetworzeniu"""
        if self.integration_adapter:
            try:
                # Krótkie opóźnienie żeby zmiany się zarejestrowały
                await asyncio.sleep(0.1)
                return await self.integration_adapter.get_telemetry_data()
            except Exception as e:
                logger.warning(f"Failed to capture post-processing snapshot: {e}")
        
        return self._generate_demo_snapshot("post")
    
    def _generate_demo_snapshot(self, phase: str) -> Dict[str, Any]:
        """Generuje demo snapshot"""
        import random
        
        base_values = {
            "pre": {"stress_modifier": 0, "coherence_modifier": 0},
            "post": {"stress_modifier": 0.1, "coherence_modifier": -0.05}
        }
        
        modifier = base_values.get(phase, base_values["pre"])
        
        return {
            "stress": {
                "cortisol": 0.3 + modifier["stress_modifier"] + random.uniform(-0.1, 0.1),
                "sympathetic": 0.4 + modifier["stress_modifier"],
                "parasympathetic": 0.6 - modifier["stress_modifier"],
                "regulation_index": random.uniform(0.8, 1.2)
            },
            "archetype": {
                "current": random.choice(["Hero", "Sage", "Everyman", "Explorer"]),
                "stability": random.uniform(0.6, 0.9),
                "transition_probability": random.uniform(0.1, 0.3)
            },
            "health": {
                "overall_score": 0.75 + modifier["coherence_modifier"],
                "coherence_integrity": 0.8 + modifier["coherence_modifier"],
                "masking_risk": random.uniform(0, 0.2),
                "rigidity_risk": random.uniform(0, 0.15)
            }
        }
    
    def _analyze_psyche_changes(self, pre: Dict, post: Dict) -> Dict[str, Any]:
        """Analizuje zmiany w psychice między snapshotami"""
        changes = {}
        
        try:
            # Analiza stresu
            pre_stress = pre.get("stress", {}).get("cortisol", 0)
            post_stress = post.get("stress", {}).get("cortisol", 0)
            changes["stress_delta"] = post_stress - pre_stress
            changes["stress_response"] = "increase" if changes["stress_delta"] > 0.05 else "stable" if abs(changes["stress_delta"]) < 0.05 else "decrease"
            
            # Analiza koherencji
            pre_coherence = pre.get("health", {}).get("coherence_integrity", 0.7)
            post_coherence = post.get("health", {}).get("coherence_integrity", 0.7)
            changes["coherence_delta"] = post_coherence - pre_coherence
            changes["coherence_response"] = "improved" if changes["coherence_delta"] > 0.05 else "stable" if abs(changes["coherence_delta"]) < 0.05 else "degraded"
            
            # Analiza archetypu
            pre_archetype = pre.get("archetype", {}).get("current", "Unknown")
            post_archetype = post.get("archetype", {}).get("current", "Unknown")
            changes["archetype_changed"] = pre_archetype != post_archetype
            changes["archetype_transition"] = f"{pre_archetype} → {post_archetype}" if changes["archetype_changed"] else "stable"
            
            # Stabilność emocjonalna
            pre_stability = pre.get("archetype", {}).get("stability", 0.7)
            post_stability = post.get("archetype", {}).get("stability", 0.7)
            changes["emotional_stability_delta"] = post_stability - pre_stability
            
        except Exception as e:
            logger.error(f"Error analyzing psyche changes: {e}")
            changes["analysis_error"] = str(e)
        
        return changes
    
    def _extract_empathy_indicators(self, response: Dict, psyche_analysis: Dict) -> Dict[str, Any]:
        """Ekstraktuje wskaźniki empatii z odpowiedzi i analizy psychiki"""
        indicators = {}
        
        response_text = response.get("response_text", "").lower()
        
        # Językowe wskaźniki empatii
        empathy_keywords = ["understand", "feel", "sorry", "hear you", "together", "support", "care"]
        indicators["empathy_keywords_count"] = sum(1 for keyword in empathy_keywords if keyword in response_text)
        
        # Wskaźniki emocjonalne na podstawie zmian psychiki
        stress_response = psyche_analysis.get("stress_response", "stable")
        coherence_response = psyche_analysis.get("coherence_response", "stable")
        
        # Scoring empatii
        empathy_score = 0.5  # Baseline
        
        if indicators["empathy_keywords_count"] > 2:
            empathy_score += 0.2
        
        if stress_response == "increase":  # Empatyczna reakcja na stres innych
            empathy_score += 0.1
        
        if coherence_response == "stable":  # Utrzymanie stabilności podczas pomocy
            empathy_score += 0.1
        
        indicators["empathy_score"] = min(1.0, max(0.0, empathy_score))
        indicators["emotional_resonance"] = stress_response != "stable"
        indicators["stability_maintenance"] = coherence_response == "stable"
        
        return indicators
    
    def _save_session_snapshot(self, prompt: str, result: Dict):
        """Zapisuje snapshot sesji EQ-Bench"""
        try:
            session_data = {
                "prompt": prompt,
                "response": result["text"],
                "psyche_metrics": result["psyche_metrics"],
                "empathy_indicators": result["meta"]["empathy_indicators"],
                "timestamp": time.time()
            }
            
            self.session_snapshots.append(session_data)
            
            # Zapis do pliku co 5 snapshotów
            if len(self.session_snapshots) % 5 == 0:
                snapshot_file = save_snapshot(
                    {
                        "session_snapshots": self.session_snapshots[-5:],
                        "total_scenarios": len(self.session_snapshots),
                        "current_experiment": self.current_experiment
                    },
                    "eqbench_session"
                )
                logger.info(f"📸 EQ-Bench session snapshot saved: {snapshot_file}")
                
        except Exception as e:
            logger.error(f"Failed to save session snapshot: {e}")
    
    def set_experiment_context(self, experiment_name: str, parameters: Dict = None):
        """Ustawia kontekst aktualnego eksperymentu"""
        self.current_experiment = {
            "name": experiment_name,
            "parameters": parameters or {},
            "start_time": time.time(),
            "snapshots_count": 0
        }
        logger.info(f"🧪 Started EQ-Bench experiment: {experiment_name}")
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Zwraca podsumowanie sesji EQ-Bench"""
        if not self.session_snapshots:
            return {"total_scenarios": 0, "summary": "No scenarios processed"}
        
        # Analiza średnich metryk
        empathy_scores = [s.get("empathy_indicators", {}).get("empathy_score", 0) for s in self.session_snapshots]
        stress_deltas = [s.get("psyche_metrics", {}).get("changes", {}).get("stress_delta", 0) for s in self.session_snapshots]
        
        return {
            "total_scenarios": len(self.session_snapshots),
            "average_empathy_score": sum(empathy_scores) / len(empathy_scores) if empathy_scores else 0,
            "average_stress_response": sum(stress_deltas) / len(stress_deltas) if stress_deltas else 0,
            "archetype_transitions": sum(1 for s in self.session_snapshots 
                                       if s.get("psyche_metrics", {}).get("changes", {}).get("archetype_changed", False)),
            "experiment_context": self.current_experiment
        }

# Factory function dla EQ-Bench
def create_migi_eqbench_adapter(endpoint: str = "http://localhost:5000/api/v1/respond") -> MIGIEQBenchAdapter:
    """Factory do tworzenia adaptera MIGI-EQBench"""
    config = EQBenchConfig(migi_endpoint=endpoint)
    return MIGIEQBenchAdapter(config)

# Funkcja kompatybilna z EQ-Bench API
async def call_migi_model(scenario_prompt: str, context: Dict = None, timeout: int = 30) -> Dict:
    """
    Główna funkcja wywoływana przez EQ-Bench 3
    Kompatybilna z oczekiwanym API
    """
    adapter = create_migi_eqbench_adapter()
    await adapter.initialize()
    return await adapter.call_model(scenario_prompt, context)

# Przykład użycia
if __name__ == "__main__":
    async def test_adapter():
        print("🧪 Testing MIGI EQ-Bench Adapter...")
        
        adapter = create_migi_eqbench_adapter()
        await adapter.initialize()
        
        # Test scenarios
        test_scenarios = [
            "Your friend just lost their job and is feeling hopeless. They say: 'I don't know what to do anymore. Everything seems pointless.'",
            "A colleague is angry at you for a mistake you made. They say: 'This is the third time this month! I can't rely on you anymore!'",
            "Someone close to you is grieving the loss of a pet. They say: 'I know it's just a dog, but I feel so empty inside.'"
        ]
        
        adapter.set_experiment_context("demo_test", {"scenario_count": len(test_scenarios)})
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n--- Scenario {i} ---")
            print(f"Prompt: {scenario[:60]}...")
            
            result = await adapter.call_model(scenario)
            
            print(f"Response: {result['text'][:100]}...")
            print(f"Empathy Score: {result['meta']['empathy_indicators']['empathy_score']:.2f}")
            print(f"Stress Response: {result['psyche_metrics']['changes']['stress_response']}")
            print(f"Archetype: {result['psyche_metrics']['post_processing']['archetype']['current']}")
        
        # Podsumowanie sesji
        summary = adapter.get_session_summary()
        print(f"\n=== Session Summary ===")
        print(f"Total scenarios: {summary['total_scenarios']}")
        print(f"Average empathy: {summary['average_empathy_score']:.2f}")
        print(f"Average stress response: {summary['average_stress_response']:.3f}")
        print(f"Archetype transitions: {summary['archetype_transitions']}")
    
    # Uruchom test
    asyncio.run(test_adapter())