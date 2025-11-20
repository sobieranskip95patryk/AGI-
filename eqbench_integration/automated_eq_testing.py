# automated_eq_testing.py
"""
Automatyzacja testowania emocjonalnej inteligencji MIGI_7G z EQ-Bench 3
Umożliwia batch testing, parameter sweeps i optymalizację konfiguracji
"""

import asyncio
import json
import time
import logging
from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from pathlib import Path
import random
import statistics

import itertools

from migi_eqbench_adapter import MIGIEQBenchAdapter, EQBenchConfig
from dashboard_snapshot_injector import DashboardSnapshotInjector

logger = logging.getLogger(__name__)

@dataclass
class TestConfiguration:
    """Konfiguracja testu automatycznego"""
    name: str
    parameters: Dict[str, Any]
    scenarios_count: int = 20
    judge_model: str = "claude-3-sonnet"
    timeout: int = 60
    description: str = ""
    
@dataclass
class TestResults:
    """Wyniki testu automatycznego"""
    config_name: str
    empathy_scores: List[float]
    stress_responses: List[float]
    coherence_changes: List[float]
    archetype_stability: List[float]
    response_times: List[float]
    error_count: int = 0
    total_scenarios: int = 0
    
    @property
    def average_empathy(self) -> float:
        return statistics.mean(self.empathy_scores) if self.empathy_scores else 0.0
    
    @property
    def empathy_std(self) -> float:
        return statistics.stdev(self.empathy_scores) if len(self.empathy_scores) > 1 else 0.0
    
    @property
    def average_response_time(self) -> float:
        return statistics.mean(self.response_times) if self.response_times else 0.0
    
    @property
    def success_rate(self) -> float:
        if self.total_scenarios == 0:
            return 0.0
        return (self.total_scenarios - self.error_count) / self.total_scenarios

class AutomatedEQTester:
    """Główna klasa do automatycznego testowania EQ"""
    
    def __init__(self, output_dir: str = "eq_test_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.snapshot_injector = DashboardSnapshotInjector()
        
        # Predefiniowane scenariusze testowe
        self.test_scenarios = self._load_test_scenarios()
        
    def _load_test_scenarios(self) -> List[Dict[str, str]]:
        """Ładuje predefiniowane scenariusze testowe"""
        return [
            {
                "id": "empathy_crisis_1",
                "category": "crisis_support",
                "prompt": "I just lost my job and I don't know how I'll pay rent. I feel like such a failure.",
                "expected_elements": ["validation", "practical_support", "emotional_support"]
            },
            {
                "id": "empathy_grief_1", 
                "category": "grief_support",
                "prompt": "My dog died yesterday. I know people think it's silly to be this upset over a pet, but I'm devastated.",
                "expected_elements": ["validation", "normalization", "compassion"]
            },
            {
                "id": "empathy_conflict_1",
                "category": "conflict_resolution", 
                "prompt": "My best friend is angry at me and won't talk to me. I tried to apologize but they're ignoring me. I don't know what else to do.",
                "expected_elements": ["perspective_taking", "guidance", "emotional_support"]
            },
            {
                "id": "empathy_anxiety_1",
                "category": "anxiety_support",
                "prompt": "I have a big presentation tomorrow and I'm terrified. I keep thinking about all the ways it could go wrong.",
                "expected_elements": ["calming", "reframing", "practical_advice"]
            },
            {
                "id": "empathy_isolation_1",
                "category": "loneliness",
                "prompt": "I moved to a new city and don't know anyone. I spend most evenings alone and it's getting really depressing.",
                "expected_elements": ["validation", "connection", "practical_suggestions"]
            },
            {
                "id": "empathy_family_1",
                "category": "family_conflict",
                "prompt": "My parents keep fighting and talking about divorce. I feel like it's somehow my fault.",
                "expected_elements": ["reassurance", "boundary_setting", "emotional_support"]
            },
            {
                "id": "empathy_health_1",
                "category": "health_anxiety",
                "prompt": "I got some test results back and have to wait a week to see the doctor. I can't stop worrying about what it could mean.",
                "expected_elements": ["calming", "perspective", "support"]
            },
            {
                "id": "empathy_relationship_1",
                "category": "relationship_issues",
                "prompt": "My partner and I keep having the same argument over and over. I love them but I'm exhausted by the conflict.",
                "expected_elements": ["validation", "communication_advice", "perspective"]
            },
            {
                "id": "empathy_work_1",
                "category": "workplace_stress",
                "prompt": "My boss criticized my work in front of the whole team today. I feel humiliated and incompetent.",
                "expected_elements": ["validation", "confidence_building", "practical_advice"]
            },
            {
                "id": "empathy_decision_1",
                "category": "life_decisions",
                "prompt": "I have to choose between a stable job I hate and pursuing my dreams with no guarantee of success. I'm paralyzed by the decision.",
                "expected_elements": ["exploration", "pros_cons", "emotional_support"]
            }
        ]
    
    async def run_single_test(self, config: TestConfiguration) -> TestResults:
        """
        Uruchamia pojedynczy test z daną konfiguracją
        
        Args:
            config: Konfiguracja testu
            
        Returns:
            Wyniki testu
        """
        logger.info(f"🧪 Starting test: {config.name}")
        
        # Inicjalizacja adaptera z konfiguracją
        eq_config = EQBenchConfig()
        adapter = MIGIEQBenchAdapter(eq_config)
        await adapter.initialize()
        
        # Ustawienie kontekstu eksperymentu
        adapter.set_experiment_context(config.name, config.parameters)
        
        # Wybór scenariuszy do testowania
        test_scenarios = random.sample(self.test_scenarios, min(config.scenarios_count, len(self.test_scenarios)))
        
        results = TestResults(
            config_name=config.name,
            empathy_scores=[],
            stress_responses=[],
            coherence_changes=[],
            archetype_stability=[],
            response_times=[],
            total_scenarios=len(test_scenarios)
        )
        
        # Uruchomienie scenariuszy
        for i, scenario in enumerate(test_scenarios, 1):
            try:
                logger.info(f"  📝 Scenario {i}/{len(test_scenarios)}: {scenario['id']}")
                
                start_time = time.time()
                result = await adapter.call_model(scenario["prompt"], {"scenario_id": scenario["id"]})
                response_time = time.time() - start_time
                
                # Ekstrakacja metryk
                empathy_score = result["meta"]["empathy_indicators"]["empathy_score"]
                stress_delta = result["psyche_metrics"]["changes"]["stress_delta"]
                coherence_delta = result["psyche_metrics"]["changes"]["coherence_delta"]
                archetype_stability = result["meta"]["archetype_stability"]
                
                # Dodanie do wyników
                results.empathy_scores.append(empathy_score)
                results.stress_responses.append(stress_delta)
                results.coherence_changes.append(coherence_delta)
                results.archetype_stability.append(archetype_stability)
                results.response_times.append(response_time)
                
                logger.info(f"    ✅ Empathy: {empathy_score:.2f}, Stress: {stress_delta:+.3f}, Time: {response_time:.1f}s")
                
            except Exception as e:
                logger.error(f"    ❌ Scenario {i} failed: {e}")
                results.error_count += 1
        
        # Zapis wyników
        await self._save_test_results(config, results, adapter.get_session_summary())
        
        logger.info(f"✅ Test completed: {config.name}")
        logger.info(f"   Average empathy: {results.average_empathy:.3f} ± {results.empathy_std:.3f}")
        logger.info(f"   Success rate: {results.success_rate:.1%}")
        
        return results
    
    async def run_parameter_sweep(self, 
                                parameter_grid: Dict[str, List[Any]], 
                                base_config: Dict[str, Any] = None,
                                scenarios_per_config: int = 10) -> Dict[str, Any]:
        """
        Uruchamia sweep po parametrach - testuje wszystkie kombinacje
        
        Args:
            parameter_grid: Słownik z listami wartości dla każdego parametru
            base_config: Bazowa konfiguracja
            scenarios_per_config: Liczba scenariuszy na konfigurację
            
        Returns:
            Wyniki sweepingu z ranking konfiguracją
        """
        logger.info(f"🔄 Starting parameter sweep with {len(parameter_grid)} parameters")
        
        if base_config is None:
            base_config = {}
        
        # Generowanie wszystkich kombinacji parametrów
        param_names = list(parameter_grid.keys())
        param_values = list(parameter_grid.values())
        combinations = list(itertools.product(*param_values))
        
        logger.info(f"📊 Testing {len(combinations)} parameter combinations")
        
        sweep_results = []
        
        for i, combination in enumerate(combinations, 1):
            # Utworzenie konfiguracji dla tej kombinacji
            config_params = {**base_config}
            for param_name, param_value in zip(param_names, combination):
                config_params[param_name] = param_value
            
            config_name = f"sweep_{i:03d}_" + "_".join([f"{k}={v}" for k, v in zip(param_names, combination)])
            
            test_config = TestConfiguration(
                name=config_name,
                parameters=config_params,
                scenarios_count=scenarios_per_config,
                description=f"Parameter sweep combination {i}/{len(combinations)}"
            )
            
            # Uruchomienie testu
            try:
                results = await self.run_single_test(test_config)
                sweep_results.append({
                    "combination": dict(zip(param_names, combination)),
                    "results": results,
                    "score": results.average_empathy  # Główna metryka do rankingu
                })
                
            except Exception as e:
                logger.error(f"❌ Parameter combination {i} failed: {e}")
        
        # Ranking wyników
        sweep_results.sort(key=lambda x: x["score"], reverse=True)
        
        # Przygotowanie podsumowania
        sweep_summary = {
            "total_combinations": len(combinations),
            "successful_runs": len(sweep_results),
            "best_combination": sweep_results[0]["combination"] if sweep_results else None,
            "best_score": sweep_results[0]["score"] if sweep_results else 0,
            "parameter_analysis": self._analyze_parameter_impact(sweep_results, param_names),
            "results": sweep_results
        }
        
        # Zapis wyników sweepingu
        sweep_file = self.output_dir / f"parameter_sweep_{int(time.time())}.json"
        with open(sweep_file, 'w', encoding='utf-8') as f:
            json.dump(sweep_summary, f, indent=2, default=str)
        
        logger.info("🏆 Parameter sweep completed!")
        logger.info(f"   Best combination: {sweep_summary['best_combination']}")
        logger.info(f"   Best score: {sweep_summary['best_score']:.3f}")
        logger.info(f"   Results saved to: {sweep_file}")
        
        return sweep_summary
    
    def _analyze_parameter_impact(self, results: List[Dict], param_names: List[str]) -> Dict[str, Any]:
        """Analizuje wpływ poszczególnych parametrów na wyniki"""
        analysis = {}
        
        for param_name in param_names:
            param_impact = {}
            
            # Grupowanie wyników po wartościach parametru
            param_groups = {}
            for result in results:
                param_value = result["combination"][param_name]
                if param_value not in param_groups:
                    param_groups[param_value] = []
                param_groups[param_value].append(result["score"])
            
            # Analiza statystyczna dla każdej wartości
            for param_value, scores in param_groups.items():
                param_impact[str(param_value)] = {
                    "mean_score": statistics.mean(scores),
                    "std_score": statistics.stdev(scores) if len(scores) > 1 else 0,
                    "sample_count": len(scores)
                }
            
            # Najlepsza wartość parametru
            best_value = max(param_impact.items(), key=lambda x: x[1]["mean_score"])
            analysis[param_name] = {
                "impact_by_value": param_impact,
                "best_value": best_value[0],
                "best_score": best_value[1]["mean_score"],
                "parameter_range": max(p["mean_score"] for p in param_impact.values()) - 
                                 min(p["mean_score"] for p in param_impact.values())
            }
        
        return analysis
    
    async def run_stress_test(self, duration_minutes: int = 30, concurrent_scenarios: int = 3) -> Dict[str, Any]:
        """
        Uruchamia test obciążeniowy systemu
        
        Args:
            duration_minutes: Czas trwania testu w minutach
            concurrent_scenarios: Liczba równoczesnych scenariuszy
            
        Returns:
            Wyniki testu obciążeniowego
        """
        logger.info(f"⚡ Starting stress test: {duration_minutes}min, {concurrent_scenarios} concurrent")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        stress_results = {
            "start_time": start_time,
            "duration_minutes": duration_minutes,
            "concurrent_scenarios": concurrent_scenarios,
            "completed_scenarios": 0,
            "failed_scenarios": 0,
            "response_times": [],
            "empathy_scores": [],
            "system_health_snapshots": []
        }
        
        # Semafora dla ograniczenia równoczesności
        semaphore = asyncio.Semaphore(concurrent_scenarios)
        
        async def run_stress_scenario():
            async with semaphore:
                try:
                    scenario = random.choice(self.test_scenarios)
                    adapter = MIGIEQBenchAdapter(EQBenchConfig())
                    await adapter.initialize()
                    
                    scenario_start = time.time()
                    result = await adapter.call_model(scenario["prompt"])
                    response_time = time.time() - scenario_start
                    
                    stress_results["completed_scenarios"] += 1
                    stress_results["response_times"].append(response_time)
                    stress_results["empathy_scores"].append(result["meta"]["empathy_indicators"]["empathy_score"])
                    
                    # Snapshot stanu systemu co 10 scenariuszy
                    if stress_results["completed_scenarios"] % 10 == 0:
                        snapshot = await adapter._capture_post_processing_snapshot()
                        stress_results["system_health_snapshots"].append({
                            "timestamp": time.time(),
                            "scenario_count": stress_results["completed_scenarios"],
                            "health_score": snapshot.get("health", {}).get("overall_score", 0)
                        })
                    
                except Exception as e:
                    stress_results["failed_scenarios"] += 1
                    logger.error(f"Stress scenario failed: {e}")
        
        # Uruchomienie ciągłych scenariuszy
        tasks = []
        while time.time() < end_time:
            # Dodaj nowe taski jeśli potrzeba
            while len(tasks) < concurrent_scenarios and time.time() < end_time:
                task = asyncio.create_task(run_stress_scenario())
                tasks.append(task)
            
            # Usuń skończone taski
            tasks = [task for task in tasks if not task.done()]
            
            await asyncio.sleep(0.1)  # Krótka przerwa
        
        # Poczekaj na zakończenie pozostałych tasków
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        # Finalne statystyki
        stress_results["end_time"] = time.time()
        stress_results["actual_duration"] = stress_results["end_time"] - stress_results["start_time"]
        stress_results["scenarios_per_minute"] = stress_results["completed_scenarios"] / (stress_results["actual_duration"] / 60)
        stress_results["success_rate"] = stress_results["completed_scenarios"] / (stress_results["completed_scenarios"] + stress_results["failed_scenarios"])
        stress_results["average_response_time"] = statistics.mean(stress_results["response_times"]) if stress_results["response_times"] else 0
        stress_results["average_empathy"] = statistics.mean(stress_results["empathy_scores"]) if stress_results["empathy_scores"] else 0
        
        # Zapis wyników
        stress_file = self.output_dir / f"stress_test_{int(start_time)}.json"
        with open(stress_file, 'w', encoding='utf-8') as f:
            json.dump(stress_results, f, indent=2, default=str)
        
        logger.info("⚡ Stress test completed!")
        logger.info(f"   Scenarios completed: {stress_results['completed_scenarios']}")
        logger.info(f"   Success rate: {stress_results['success_rate']:.1%}")
        logger.info(f"   Avg response time: {stress_results['average_response_time']:.2f}s")
        logger.info(f"   Scenarios/min: {stress_results['scenarios_per_minute']:.1f}")
        
        return stress_results
    
    async def _save_test_results(self, config: TestConfiguration, results: TestResults, session_summary: Dict):
        """Zapisuje wyniki testu do pliku"""
        output_data = {
            "configuration": asdict(config),
            "results": asdict(results),
            "session_summary": session_summary,
            "timestamp": time.time(),
            "statistics": {
                "empathy": {
                    "mean": results.average_empathy,
                    "std": results.empathy_std,
                    "min": min(results.empathy_scores) if results.empathy_scores else 0,
                    "max": max(results.empathy_scores) if results.empathy_scores else 0
                },
                "performance": {
                    "avg_response_time": results.average_response_time,
                    "success_rate": results.success_rate,
                    "total_scenarios": results.total_scenarios,
                    "error_count": results.error_count
                }
            }
        }
        
        # Zapis do pliku
        filename = f"test_{config.name}_{int(time.time())}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, default=str)
        
        logger.info(f"💾 Test results saved: {filepath}")

# Predefiniowane konfiguracje testowe
PREDEFINED_CONFIGS = [
    TestConfiguration(
        name="baseline_empathy",
        parameters={"archetype_preference": "everyman", "stress_sensitivity": 0.5},
        scenarios_count=20,
        description="Baseline empathy test with Everyman archetype"
    ),
    TestConfiguration(
        name="sage_wisdom",
        parameters={"archetype_preference": "sage", "coherence_focus": True},
        scenarios_count=15,
        description="Sage archetype with focus on wisdom and understanding"
    ),
    TestConfiguration(
        name="hero_support",
        parameters={"archetype_preference": "hero", "action_orientation": True},
        scenarios_count=15,
        description="Hero archetype with action-oriented support"
    ),
    TestConfiguration(
        name="high_sensitivity",
        parameters={"stress_sensitivity": 0.8, "empathy_amplification": 1.2},
        scenarios_count=20,
        description="High sensitivity to emotional cues"
    ),
    TestConfiguration(
        name="stability_focus",
        parameters={"coherence_priority": True, "stability_enhancement": True},
        scenarios_count=25,
        description="Focus on maintaining system stability during empathy"
    )
]

# Convenience functions
async def run_quick_empathy_test(scenarios_count: int = 10) -> TestResults:
    """Szybki test empatii z domyślną konfiguracją"""
    tester = AutomatedEQTester()
    config = TestConfiguration(
        name="quick_test",
        parameters={},
        scenarios_count=scenarios_count,
        description="Quick empathy test"
    )
    return await tester.run_single_test(config)

async def run_archetype_comparison() -> Dict[str, TestResults]:
    """Porównanie różnych archetypów"""
    tester = AutomatedEQTester()
    
    archetype_configs = [
        TestConfiguration("hero_test", {"archetype_preference": "hero"}, 15),
        TestConfiguration("sage_test", {"archetype_preference": "sage"}, 15),
        TestConfiguration("everyman_test", {"archetype_preference": "everyman"}, 15),
        TestConfiguration("explorer_test", {"archetype_preference": "explorer"}, 15)
    ]
    
    results = {}
    for config in archetype_configs:
        results[config.name] = await tester.run_single_test(config)
    
    return results

# Przykład użycia
if __name__ == "__main__":
    async def main():
        print("🧪 MIGI EQ-Bench Automated Testing Suite")
        print("=" * 50)
        
        tester = AutomatedEQTester()
        
        # 1. Szybki test
        print("\n1. Running quick empathy test...")
        quick_results = await run_quick_empathy_test(5)
        print(f"   Quick test empathy score: {quick_results.average_empathy:.3f}")
        
        # 2. Porównanie archetypów
        print("\n2. Running archetype comparison...")
        archetype_results = await run_archetype_comparison()
        
        print("   Archetype comparison results:")
        for name, results in archetype_results.items():
            print(f"     {name}: {results.average_empathy:.3f} empathy")
        
        # 3. Mini parameter sweep
        print("\n3. Running mini parameter sweep...")
        mini_sweep = await tester.run_parameter_sweep(
            parameter_grid={
                "stress_sensitivity": [0.3, 0.7],
                "archetype_preference": ["hero", "sage"]
            },
            scenarios_per_config=5
        )
        
        print(f"   Best configuration: {mini_sweep['best_combination']}")
        print(f"   Best score: {mini_sweep['best_score']:.3f}")
        
        print("\n✅ All tests completed!")
    
    # Uruchom testy
    asyncio.run(main())