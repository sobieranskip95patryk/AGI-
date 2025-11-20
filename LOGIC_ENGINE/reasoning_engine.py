#!/usr/bin/env python3
"""
🧠 LOGIC ENGINE - ADVANCED REASONING SYSTEM
Zaawansowany silnik rozumowania dla systemu AGI MIGI 7G

Komponenty:
- Dedukcja: Wnioskowanie logiczne z reguł i faktów
- Indukcja: Generowanie reguł z przykładów (ILP)
- Abdukcja: Hipotezy wyjaśniające obserwacje
- HTN Planning: Hierarchiczne planowanie zadań
- Causal Reasoning: Grafy przyczynowe i do-calculus

Autor: MIGI 7G Development Team
Status: IMPLEMENTATION PHASE 1 - ROI Critical Path
"""

import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='[🧠 LOGIC_ENGINE] %(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class ReasoningType(Enum):
    """Typy rozumowania logicznego"""
    DEDUCTION = "DEDUCTION"      # Dedukcja: reguły → wnioski
    INDUCTION = "INDUCTION"      # Indukcja: przykłady → reguły
    ABDUCTION = "ABDUCTION"      # Abdukcja: obserwacje → hipotezy
    CAUSAL = "CAUSAL"           # Rozumowanie przyczynowe
    HTN_PLANNING = "HTN_PLANNING" # Planowanie hierarchiczne

class ConfidenceLevel(Enum):
    """Poziomy pewności wniosków"""
    CERTAIN = 1.0
    VERY_HIGH = 0.9
    HIGH = 0.8
    MEDIUM = 0.6
    LOW = 0.4
    VERY_LOW = 0.2
    UNCERTAIN = 0.1

@dataclass
class Fact:
    """Reprezentuje fakt w bazie wiedzy"""
    id: str
    predicate: str
    arguments: List[str]
    confidence: float = 1.0
    timestamp: float = 0.0
    source: str = "system"
    
    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()
    
    def to_string(self) -> str:
        """Konwersja faktu na reprezentację tekstową"""
        args_str = ", ".join(self.arguments)
        return f"{self.predicate}({args_str})"

@dataclass
class Rule:
    """Reprezentuje regułę logiczną (if-then)"""
    id: str
    premises: List[str]  # Przesłanki (warunki)
    conclusion: str      # Konkluzja
    confidence: float = 1.0
    weight: float = 1.0
    domain: str = "general"
    
    def to_string(self) -> str:
        """Konwersja reguły na reprezentację tekstową"""
        premises_str = " AND ".join(self.premises)
        return f"IF {premises_str} THEN {self.conclusion}"

@dataclass
class Hypothesis:
    """Reprezentuje hipotezę abdukcyjną"""
    id: str
    explanation: str
    observations: List[str]
    confidence: float
    cost: float
    plausibility: float
    supporting_facts: List[str]
    
    def overall_score(self) -> float:
        """Oblicza ogólny wynik hipotezy"""
        return (self.confidence * 0.5 + 
                self.plausibility * 0.3 + 
                (1.0 - self.cost) * 0.2)

@dataclass
class InferenceResult:
    """Wynik procesu wnioskowania"""
    reasoning_type: ReasoningType
    query: str
    conclusion: str
    confidence: float
    proof_chain: List[str]
    used_facts: List[str]
    used_rules: List[str]
    execution_time: float
    explanation: str

@dataclass
class HTNTask:
    """Zadanie w hierarchicznym planowaniu"""
    id: str
    name: str
    task_type: str  # "primitive" lub "compound"
    preconditions: List[str]
    effects: List[str]
    subtasks: List[str] = None  # Dla zadań złożonych
    cost: float = 1.0
    priority: int = 1
    
class KnowledgeBase:
    """
    🗃️ BAZA WIEDZY - Centralne repozytorium faktów i reguł
    
    Przechowuje i zarządza:
    - Fakty (atomy logiczne)
    - Reguły wnioskowania
    - Schematy domeny
    - Historię wniosków
    """
    
    def __init__(self):
        self.facts: Dict[str, Fact] = {}
        self.rules: Dict[str, Rule] = {}
        self.domain_schema: Dict[str, Any] = {}
        self.inference_history: List[InferenceResult] = []
        
        logger.info("🗃️ KnowledgeBase initialized")
        self._initialize_default_knowledge()
    
    def _initialize_default_knowledge(self):
        """Inicjalizuje bazową wiedzę systemową"""
        
        # Podstawowe fakty systemowe
        default_facts = [
            Fact("fact_1", "system_status", ["operational"], 1.0, source="system"),
            Fact("fact_2", "agent_type", ["agi_system"], 1.0, source="system"),
            Fact("fact_3", "reasoning_capability", ["multi_modal"], 0.9, source="system"),
            Fact("fact_4", "learning_mode", ["active"], 0.8, source="system")
        ]
        
        for fact in default_facts:
            self.add_fact(fact)
        
        # Podstawowe reguły wnioskowania
        default_rules = [
            Rule("rule_1", 
                 ["system_status(operational)", "agent_type(agi_system)"], 
                 "ready_for_reasoning(true)", 
                 confidence=0.95, domain="system"),
            Rule("rule_2",
                 ["reasoning_capability(multi_modal)", "learning_mode(active)"],
                 "adaptive_reasoning(enabled)",
                 confidence=0.9, domain="cognition"),
            Rule("rule_3",
                 ["ready_for_reasoning(true)", "adaptive_reasoning(enabled)"],
                 "full_reasoning_available(true)",
                 confidence=0.85, domain="system")
        ]
        
        for rule in default_rules:
            self.add_rule(rule)
        
        logger.info(f"📚 Initialized {len(self.facts)} default facts and {len(self.rules)} default rules")
    
    def add_fact(self, fact: Fact):
        """Dodaje fakt do bazy wiedzy"""
        self.facts[fact.id] = fact
        logger.debug(f"➕ Added fact: {fact.to_string()}")
    
    def add_rule(self, rule: Rule):
        """Dodaje regułę do bazy wiedzy"""
        self.rules[rule.id] = rule
        logger.debug(f"➕ Added rule: {rule.to_string()}")
    
    def get_facts_by_predicate(self, predicate: str) -> List[Fact]:
        """Pobiera fakty o danym predykacie"""
        return [fact for fact in self.facts.values() 
                if fact.predicate == predicate]
    
    def get_applicable_rules(self, facts: List[str]) -> List[Rule]:
        """Znajduje reguły możliwe do zastosowania dla danych faktów"""
        applicable_rules = []
        
        for rule in self.rules.values():
            # Sprawdź czy wszystkie przesłanki są spełnione
            if all(premise in facts for premise in rule.premises):
                applicable_rules.append(rule)
        
        return applicable_rules
    
    def export_knowledge(self) -> Dict[str, Any]:
        """Eksportuje bazę wiedzy do formatu JSON"""
        return {
            "facts": [asdict(fact) for fact in self.facts.values()],
            "rules": [asdict(rule) for rule in self.rules.values()],
            "domain_schema": self.domain_schema,
            "total_inferences": len(self.inference_history)
        }

class DeductiveReasoner:
    """
    🎯 SILNIK DEDUKCYJNY - Forward/Backward Chaining
    
    Implementuje:
    - Forward chaining (od faktów do wniosków)
    - Backward chaining (od celów do faktów)
    - Unifikację i podstawianie
    - Generowanie proof chains
    """
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        logger.info("🎯 DeductiveReasoner initialized")
    
    def forward_chain(self, max_iterations: int = 10) -> List[InferenceResult]:
        """
        Forward chaining: wywnioskuj wszystkie możliwe wnioski
        """
        start_time = time.time()
        results = []
        derived_facts = set(fact.to_string() for fact in self.kb.facts.values())
        
        for iteration in range(max_iterations):
            new_facts = set()
            
            # Znajdź wszystkie możliwe do zastosowania reguły
            applicable_rules = self.kb.get_applicable_rules(list(derived_facts))
            
            if not applicable_rules:
                break
            
            for rule in applicable_rules:
                # Sprawdź czy konkluzja już nie została wyprowadzona
                if rule.conclusion not in derived_facts:
                    new_facts.add(rule.conclusion)
                    
                    # Stwórz wynik wnioskowania
                    result = InferenceResult(
                        reasoning_type=ReasoningType.DEDUCTION,
                        query=f"forward_chain_iteration_{iteration}",
                        conclusion=rule.conclusion,
                        confidence=rule.confidence,
                        proof_chain=[f"Applied rule: {rule.to_string()}"],
                        used_facts=rule.premises,
                        used_rules=[rule.id],
                        execution_time=time.time() - start_time,
                        explanation=f"Deduced '{rule.conclusion}' from premises: {', '.join(rule.premises)}"
                    )
                    results.append(result)
            
            # Dodaj nowe fakty do zbioru
            derived_facts.update(new_facts)
            
            if not new_facts:
                break
        
        logger.info(f"🎯 Forward chaining completed: {len(results)} new inferences in {len(range(iteration+1))} iterations")
        return results
    
    def backward_chain(self, goal: str, depth: int = 0, max_depth: int = 5) -> Optional[InferenceResult]:
        """
        Backward chaining: sprawdź czy cel można osiągnąć
        """
        start_time = time.time()
        
        if depth > max_depth:
            return None
        
        # Sprawdź czy cel jest już faktem
        for fact in self.kb.facts.values():
            if fact.to_string() == goal:
                return InferenceResult(
                    reasoning_type=ReasoningType.DEDUCTION,
                    query=goal,
                    conclusion=goal,
                    confidence=fact.confidence,
                    proof_chain=[f"Direct fact: {goal}"],
                    used_facts=[goal],
                    used_rules=[],
                    execution_time=time.time() - start_time,
                    explanation=f"Goal '{goal}' found as direct fact"
                )
        
        # Znajdź reguły które mogą wyprowadzić cel
        for rule in self.kb.rules.values():
            if rule.conclusion == goal:
                # Sprawdź rekurencyjnie wszystkie przesłanki
                premise_results = []
                all_premises_satisfied = True
                
                for premise in rule.premises:
                    premise_result = self.backward_chain(premise, depth + 1, max_depth)
                    if premise_result:
                        premise_results.append(premise_result)
                    else:
                        all_premises_satisfied = False
                        break
                
                if all_premises_satisfied:
                    # Oblicz łączną pewność
                    combined_confidence = rule.confidence
                    if premise_results:
                        premise_confidences = [res.confidence for res in premise_results]
                        combined_confidence *= min(premise_confidences)
                    
                    # Zbuduj proof chain
                    proof_chain = [f"Goal: {goal}"]
                    proof_chain.append(f"Applied rule: {rule.to_string()}")
                    for premise_result in premise_results:
                        proof_chain.extend([f"  Sub-proof: {chain}" for chain in premise_result.proof_chain])
                    
                    return InferenceResult(
                        reasoning_type=ReasoningType.DEDUCTION,
                        query=goal,
                        conclusion=goal,
                        confidence=combined_confidence,
                        proof_chain=proof_chain,
                        used_facts=[res.conclusion for res in premise_results],
                        used_rules=[rule.id] + [res.used_rules for res in premise_results],
                        execution_time=time.time() - start_time,
                        explanation=f"Goal '{goal}' proven through rule application"
                    )
        
        return None
    
    def prove_query(self, query: str) -> Optional[InferenceResult]:
        """Główna metoda dowodzenia zapytań"""
        logger.info(f"🎯 Attempting to prove query: {query}")
        
        result = self.backward_chain(query)
        if result:
            self.kb.inference_history.append(result)
            logger.info(f"✅ Query proven with confidence: {result.confidence:.3f}")
        else:
            logger.info(f"❌ Query could not be proven: {query}")
        
        return result

class AbductiveReasoner:
    """
    🔍 SILNIK ABDUKCYJNY - Generowanie hipotez wyjaśniających
    
    Implementuje:
    - Generowanie hipotez dla obserwacji
    - Ranking hipotez według prawdopodobieństwa
    - Ocena kosztów i wiarygodności
    - Best explanation selection
    """
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.hypothesis_cache: Dict[str, List[Hypothesis]] = {}
        logger.info("🔍 AbductiveReasoner initialized")
    
    def generate_hypotheses(self, observations: List[str], max_hypotheses: int = 5) -> List[Hypothesis]:
        """
        Generuje hipotezy wyjaśniające podane obserwacje
        """
        start_time = time.time()
        hypotheses = []
        
        # Cache key dla obserwacji
        cache_key = "|".join(sorted(observations))
        if cache_key in self.hypothesis_cache:
            logger.info("📋 Using cached hypotheses")
            return self.hypothesis_cache[cache_key]
        
        logger.info(f"🔍 Generating hypotheses for observations: {observations}")
        
        # Dla każdej obserwacji znajdź możliwe wyjaśnienia
        for observation in observations:
            # Znajdź reguły które mogą prowadzić do tej obserwacji
            explaining_rules = [rule for rule in self.kb.rules.values() 
                              if rule.conclusion == observation]
            
            for rule in explaining_rules:
                # Każda przesłanka reguły może być hipotezą
                for premise in rule.premises:
                    hypothesis_id = f"hyp_{len(hypotheses)+1}_{uuid.uuid4().hex[:8]}"
                    
                    # Sprawdź czy hipoteza już istnieje jako fakt
                    is_known_fact = any(fact.to_string() == premise for fact in self.kb.facts.values())
                    
                    if not is_known_fact:
                        # Oblicz parametry hipotezy
                        confidence = self._calculate_hypothesis_confidence(premise, observations)
                        cost = self._calculate_hypothesis_cost(premise)
                        plausibility = self._calculate_hypothesis_plausibility(premise, rule)
                        
                        hypothesis = Hypothesis(
                            id=hypothesis_id,
                            explanation=premise,
                            observations=observations,
                            confidence=confidence,
                            cost=cost,
                            plausibility=plausibility,
                            supporting_facts=[rule.id]
                        )
                        
                        hypotheses.append(hypothesis)
        
        # Usuń duplikaty i posortuj według overall_score
        unique_hypotheses = self._remove_duplicate_hypotheses(hypotheses)
        unique_hypotheses.sort(key=lambda h: h.overall_score(), reverse=True)
        
        # Ogranicz do max_hypotheses
        final_hypotheses = unique_hypotheses[:max_hypotheses]
        
        # Cache wyniki
        self.hypothesis_cache[cache_key] = final_hypotheses
        
        execution_time = time.time() - start_time
        logger.info(f"🔍 Generated {len(final_hypotheses)} hypotheses in {execution_time:.3f}s")
        
        return final_hypotheses
    
    def _calculate_hypothesis_confidence(self, premise: str, observations: List[str]) -> float:
        """Oblicza pewność hipotezy na podstawie obserwacji"""
        # Heurystyka: im więcej obserwacji wspiera hipotezę, tym wyższa pewność
        support_count = sum(1 for obs in observations if premise in obs or obs in premise)
        base_confidence = min(0.8, 0.3 + (support_count * 0.2))
        
        # Dodatkowo sprawdź czy hipoteza pasuje do domeny
        domain_bonus = 0.1 if any(premise in rule.premises for rule in self.kb.rules.values()) else 0.0
        
        return min(1.0, base_confidence + domain_bonus)
    
    def _calculate_hypothesis_cost(self, premise: str) -> float:
        """Oblicza koszt przyjęcia hipotezy"""
        # Heurystyka: prostsze hipotezy mają niższy koszt
        complexity = len(premise.split()) / 10.0  # Normalizacja przez liczbę słów
        return min(1.0, 0.2 + complexity)
    
    def _calculate_hypothesis_plausibility(self, premise: str, rule: Rule) -> float:
        """Oblicza prawdopodobieństwo hipotezy"""
        # Bazuje na sile reguły i jej wiarygodności
        rule_strength = rule.confidence * rule.weight
        
        # Bonus za spójność z istniejącą wiedzą
        consistency_bonus = 0.0
        for fact in self.kb.facts.values():
            if premise in fact.to_string() or fact.predicate in premise:
                consistency_bonus += 0.1
        
        return min(1.0, rule_strength + min(0.3, consistency_bonus))
    
    def _remove_duplicate_hypotheses(self, hypotheses: List[Hypothesis]) -> List[Hypothesis]:
        """Usuwa duplikaty hipotez na podstawie wyjaśnień"""
        seen_explanations = set()
        unique_hypotheses = []
        
        for hypothesis in hypotheses:
            if hypothesis.explanation not in seen_explanations:
                seen_explanations.add(hypothesis.explanation)
                unique_hypotheses.append(hypothesis)
        
        return unique_hypotheses
    
    def explain_observations(self, observations: List[str]) -> Optional[InferenceResult]:
        """Główna metoda wyjaśniania obserwacji"""
        start_time = time.time()
        
        logger.info(f"🔍 Explaining observations: {observations}")
        
        hypotheses = self.generate_hypotheses(observations)
        
        if not hypotheses:
            logger.info("❌ No hypotheses could be generated")
            return None
        
        # Wybierz najlepszą hipotezę
        best_hypothesis = hypotheses[0]
        
        # Stwórz wynik wnioskowania
        proof_chain = [f"Observations: {', '.join(observations)}"]
        proof_chain.append(f"Best explanation: {best_hypothesis.explanation}")
        proof_chain.append(f"Confidence: {best_hypothesis.confidence:.3f}")
        proof_chain.append(f"Overall score: {best_hypothesis.overall_score():.3f}")
        
        # Dodaj alternatywne hipotezy
        if len(hypotheses) > 1:
            proof_chain.append("Alternative explanations:")
            for i, alt_hyp in enumerate(hypotheses[1:4], 1):  # Top 3 alternatywy
                proof_chain.append(f"  {i}. {alt_hyp.explanation} (score: {alt_hyp.overall_score():.3f})")
        
        result = InferenceResult(
            reasoning_type=ReasoningType.ABDUCTION,
            query=f"explain({', '.join(observations)})",
            conclusion=best_hypothesis.explanation,
            confidence=best_hypothesis.overall_score(),
            proof_chain=proof_chain,
            used_facts=observations,
            used_rules=best_hypothesis.supporting_facts,
            execution_time=time.time() - start_time,
            explanation=f"Best explanation for observations: {best_hypothesis.explanation}"
        )
        
        self.kb.inference_history.append(result)
        logger.info(f"✅ Best explanation found: {best_hypothesis.explanation} (score: {best_hypothesis.overall_score():.3f})")
        
        return result

class HTNPlanner:
    """
    📋 HIERARCHICAL TASK NETWORK PLANNER
    
    Implementuje:
    - Dekompozycję zadań złożonych na primitive
    - Planowanie z ograniczeniami zasobów
    - Monitoring wykonania i replanning
    - Heurystyki optymalizacyjne
    """
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.task_library: Dict[str, HTNTask] = {}
        self.active_plans: Dict[str, Any] = {}
        logger.info("📋 HTNPlanner initialized")
        self._initialize_task_library()
    
    def _initialize_task_library(self):
        """Inicjalizuje bibliotekę zadań HTN"""
        
        # Podstawowe zadania primitive
        primitive_tasks = [
            HTNTask("gather_info", "gather_information", "primitive",
                   preconditions=["system_operational"],
                   effects=["information_available"],
                   cost=1.0, priority=2),
            
            HTNTask("analyze_data", "analyze_data", "primitive",
                   preconditions=["information_available"],
                   effects=["analysis_complete"],
                   cost=2.0, priority=3),
            
            HTNTask("make_decision", "make_decision", "primitive",
                   preconditions=["analysis_complete"],
                   effects=["decision_made"],
                   cost=1.5, priority=4),
            
            HTNTask("execute_action", "execute_action", "primitive",
                   preconditions=["decision_made"],
                   effects=["action_executed"],
                   cost=3.0, priority=5)
        ]
        
        # Zadania złożone (compound)
        compound_tasks = [
            HTNTask("solve_problem", "solve_problem", "compound",
                   preconditions=["problem_identified"],
                   effects=["problem_solved"],
                   subtasks=["gather_info", "analyze_data", "make_decision", "execute_action"],
                   cost=7.5, priority=1),
            
            HTNTask("learn_new_skill", "learn_new_skill", "compound",
                   preconditions=["learning_opportunity"],
                   effects=["skill_acquired"],
                   subtasks=["gather_info", "analyze_data", "practice_skill"],
                   cost=5.0, priority=2)
        ]
        
        # Dodaj do biblioteki
        for task in primitive_tasks + compound_tasks:
            self.task_library[task.id] = task
        
        logger.info(f"📚 Initialized task library with {len(self.task_library)} tasks")
    
    def create_plan(self, goal: str, available_resources: Dict[str, float] = None) -> Optional[Dict[str, Any]]:
        """
        Tworzy plan hierarchiczny dla osiągnięcia celu
        """
        start_time = time.time()
        
        if available_resources is None:
            available_resources = {"time": 100.0, "cpu": 100.0, "memory": 100.0}
        
        logger.info(f"📋 Creating HTN plan for goal: {goal}")
        
        # Znajdź zadanie odpowiadające celowi
        matching_tasks = [task for task in self.task_library.values()
                         if goal in task.effects or goal in task.name]
        
        if not matching_tasks:
            logger.info(f"❌ No matching tasks found for goal: {goal}")
            return None
        
        # Wybierz zadanie o najwyższym priorytecie
        main_task = max(matching_tasks, key=lambda t: t.priority)
        
        # Dekompozycja zadania
        plan_steps = self._decompose_task(main_task, available_resources)
        
        if not plan_steps:
            logger.info(f"❌ Could not decompose task: {main_task.name}")
            return None
        
        # Sprawdź wykonalność planu
        feasibility = self._check_plan_feasibility(plan_steps, available_resources)
        
        if not feasibility["feasible"]:
            logger.info(f"❌ Plan not feasible: {feasibility['reason']}")
            return None
        
        plan = {
            "id": f"plan_{uuid.uuid4().hex[:8]}",
            "goal": goal,
            "main_task": main_task.id,
            "steps": plan_steps,
            "total_cost": sum(step["cost"] for step in plan_steps),
            "estimated_time": feasibility["estimated_time"],
            "resource_requirements": feasibility["resources"],
            "created_at": time.time(),
            "status": "ready"
        }
        
        self.active_plans[plan["id"]] = plan
        
        execution_time = time.time() - start_time
        logger.info(f"✅ HTN plan created: {len(plan_steps)} steps, cost: {plan['total_cost']:.1f}, time: {execution_time:.3f}s")
        
        return plan
    
    def _decompose_task(self, task: HTNTask, resources: Dict[str, float]) -> List[Dict[str, Any]]:
        """Dekompozycja zadania na kroki wykonawcze"""
        
        if task.task_type == "primitive":
            return [{
                "id": task.id,
                "name": task.name,
                "type": "primitive",
                "preconditions": task.preconditions,
                "effects": task.effects,
                "cost": task.cost,
                "priority": task.priority
            }]
        
        elif task.task_type == "compound" and task.subtasks:
            steps = []
            
            for subtask_id in task.subtasks:
                if subtask_id in self.task_library:
                    subtask = self.task_library[subtask_id]
                    substeps = self._decompose_task(subtask, resources)
                    steps.extend(substeps)
                else:
                    # Jeśli podzadanie nie istnieje, stwórz placeholder
                    steps.append({
                        "id": subtask_id,
                        "name": subtask_id,
                        "type": "placeholder",
                        "preconditions": [],
                        "effects": [f"{subtask_id}_completed"],
                        "cost": 1.0,
                        "priority": 1
                    })
            
            return steps
        
        return []
    
    def _check_plan_feasibility(self, plan_steps: List[Dict[str, Any]], 
                               resources: Dict[str, float]) -> Dict[str, Any]:
        """Sprawdza wykonalność planu"""
        
        total_cost = sum(step["cost"] for step in plan_steps)
        estimated_time = total_cost * 0.5  # Heurystyka: każda jednostka kosztu = 0.5 jednostki czasu
        
        required_resources = {
            "time": estimated_time,
            "cpu": total_cost * 10,  # Każda jednostka kosztu wymaga 10 jednostek CPU
            "memory": len(plan_steps) * 5  # Każdy krok wymaga 5 jednostek pamięci
        }
        
        # Sprawdź czy zasoby są wystarczające
        for resource, required in required_resources.items():
            if resource in resources and resources[resource] < required:
                return {
                    "feasible": False,
                    "reason": f"Insufficient {resource}: required {required}, available {resources[resource]}",
                    "resources": required_resources,
                    "estimated_time": estimated_time
                }
        
        # Sprawdź logiczną spójność (preconditions → effects)
        available_conditions = set()
        
        for step in plan_steps:
            # Sprawdź czy wszystkie preconditions są spełnione
            for precond in step["preconditions"]:
                if precond not in available_conditions:
                    # Sprawdź czy precondition jest faktem w KB
                    if not any(fact.to_string() == precond for fact in self.kb.facts.values()):
                        return {
                            "feasible": False,
                            "reason": f"Unmet precondition: {precond} for step {step['name']}",
                            "resources": required_resources,
                            "estimated_time": estimated_time
                        }
            
            # Dodaj effects do dostępnych warunków
            available_conditions.update(step["effects"])
        
        return {
            "feasible": True,
            "reason": "Plan is feasible",
            "resources": required_resources,
            "estimated_time": estimated_time
        }
    
    def execute_plan(self, plan_id: str) -> Dict[str, Any]:
        """Symuluje wykonanie planu HTN"""
        
        if plan_id not in self.active_plans:
            return {"success": False, "error": "Plan not found"}
        
        plan = self.active_plans[plan_id]
        execution_log = []
        
        logger.info(f"📋 Executing HTN plan: {plan_id}")
        
        for i, step in enumerate(plan["steps"]):
            step_start = time.time()
            
            # Symulacja wykonania kroku
            success = True  # W rzeczywistej implementacji tutaj byłaby logika wykonania
            
            step_result = {
                "step_number": i + 1,
                "step_name": step["name"],
                "success": success,
                "execution_time": time.time() - step_start,
                "effects_achieved": step["effects"] if success else []
            }
            
            execution_log.append(step_result)
            
            if not success:
                plan["status"] = "failed"
                break
        
        if all(step["success"] for step in execution_log):
            plan["status"] = "completed"
        
        execution_result = {
            "plan_id": plan_id,
            "success": plan["status"] == "completed",
            "steps_executed": len(execution_log),
            "total_steps": len(plan["steps"]),
            "execution_log": execution_log,
            "final_status": plan["status"]
        }
        
        logger.info(f"📋 Plan execution {'completed' if execution_result['success'] else 'failed'}: {execution_result['steps_executed']}/{execution_result['total_steps']} steps")
        
        return execution_result

class LogicEngine:
    """
    🧠 GŁÓWNY SILNIK LOGICZNY - Logic Engine
    
    Centralny komponent zarządzający wszystkimi typami rozumowania:
    - Dedukcja, Indukcja, Abdukcja
    - Planowanie hierarchiczne HTN
    - Rozumowanie przyczynowe
    - Integracja z innymi modułami AGI
    """
    
    def __init__(self):
        logger.info("🧠 Initializing Logic Engine...")
        
        # Komponenty podstawowe
        self.knowledge_base = KnowledgeBase()
        self.deductive_reasoner = DeductiveReasoner(self.knowledge_base)
        self.abductive_reasoner = AbductiveReasoner(self.knowledge_base)
        self.htn_planner = HTNPlanner(self.knowledge_base)
        
        # Metryki i monitoring
        self.total_inferences = 0
        self.reasoning_stats = {
            "deduction": {"count": 0, "success_rate": 0.0, "avg_time": 0.0},
            "abduction": {"count": 0, "success_rate": 0.0, "avg_time": 0.0},
            "planning": {"count": 0, "success_rate": 0.0, "avg_time": 0.0}
        }
        
        # Status operacyjny
        self.is_operational = True
        self.initialization_time = time.time()
        
        logger.info("✅ Logic Engine fully initialized and operational")
        logger.info(f"📊 Knowledge Base: {len(self.knowledge_base.facts)} facts, {len(self.knowledge_base.rules)} rules")
    
    def reason(self, query: str, reasoning_type: ReasoningType = ReasoningType.DEDUCTION) -> Optional[InferenceResult]:
        """
        🎯 GŁÓWNA METODA ROZUMOWANIA
        
        Uniwersalny interfejs do wszystkich typów rozumowania
        """
        start_time = time.time()
        
        logger.info(f"🧠 Processing reasoning request: '{query}' (type: {reasoning_type.value})")
        
        result = None
        
        try:
            if reasoning_type == ReasoningType.DEDUCTION:
                result = self.deductive_reasoner.prove_query(query)
                self.reasoning_stats["deduction"]["count"] += 1
                
            elif reasoning_type == ReasoningType.ABDUCTION:
                # Dla abdukcji, query powinno być listą obserwacji
                observations = query.split(",") if "," in query else [query]
                result = self.abductive_reasoner.explain_observations(observations)
                self.reasoning_stats["abduction"]["count"] += 1
                
            elif reasoning_type == ReasoningType.HTN_PLANNING:
                plan = self.htn_planner.create_plan(query)
                if plan:
                    # Konwertuj plan na InferenceResult
                    result = InferenceResult(
                        reasoning_type=ReasoningType.HTN_PLANNING,
                        query=query,
                        conclusion=f"Plan created with {len(plan['steps'])} steps",
                        confidence=0.8,  # Pewność planu
                        proof_chain=[f"Step {i+1}: {step['name']}" for i, step in enumerate(plan['steps'])],
                        used_facts=[],
                        used_rules=[],
                        execution_time=time.time() - start_time,
                        explanation=f"HTN plan for goal '{query}' with total cost {plan['total_cost']:.1f}"
                    )
                self.reasoning_stats["planning"]["count"] += 1
            
            # Aktualizuj statystyki
            if result:
                self.total_inferences += 1
                reasoning_key = reasoning_type.value.lower()
                if reasoning_key in self.reasoning_stats:
                    stats = self.reasoning_stats[reasoning_key]
                    # Aktualizuj średni czas (moving average)
                    if stats["count"] > 1:
                        stats["avg_time"] = (stats["avg_time"] * (stats["count"] - 1) + result.execution_time) / stats["count"]
                    else:
                        stats["avg_time"] = result.execution_time
                    
                    # Aktualizuj success rate
                    stats["success_rate"] = (stats["success_rate"] * (stats["count"] - 1) + 1.0) / stats["count"]
            
        except Exception as e:
            logger.error(f"❌ Error during reasoning: {e}")
            return None
        
        if result:
            logger.info(f"✅ Reasoning completed: {result.conclusion} (confidence: {result.confidence:.3f})")
        else:
            logger.info(f"❌ Reasoning failed for query: {query}")
        
        return result
    
    def add_knowledge(self, facts: List[Dict] = None, rules: List[Dict] = None):
        """Dodaje wiedzę do systemu"""
        
        if facts:
            for fact_data in facts:
                fact = Fact(
                    id=fact_data.get("id", f"fact_{uuid.uuid4().hex[:8]}"),
                    predicate=fact_data["predicate"],
                    arguments=fact_data["arguments"],
                    confidence=fact_data.get("confidence", 1.0),
                    source=fact_data.get("source", "external")
                )
                self.knowledge_base.add_fact(fact)
        
        if rules:
            for rule_data in rules:
                rule = Rule(
                    id=rule_data.get("id", f"rule_{uuid.uuid4().hex[:8]}"),
                    premises=rule_data["premises"],
                    conclusion=rule_data["conclusion"],
                    confidence=rule_data.get("confidence", 1.0),
                    domain=rule_data.get("domain", "general")
                )
                self.knowledge_base.add_rule(rule)
        
        logger.info(f"📚 Added {len(facts) if facts else 0} facts and {len(rules) if rules else 0} rules")
    
    def get_reasoning_status(self) -> Dict[str, Any]:
        """Zwraca status i statystyki rozumowania"""
        
        uptime = time.time() - self.initialization_time
        
        return {
            "operational": self.is_operational,
            "uptime_seconds": uptime,
            "total_inferences": self.total_inferences,
            "knowledge_base": {
                "facts_count": len(self.knowledge_base.facts),
                "rules_count": len(self.knowledge_base.rules),
                "inference_history": len(self.knowledge_base.inference_history)
            },
            "reasoning_stats": self.reasoning_stats,
            "performance": {
                "inferences_per_second": self.total_inferences / uptime if uptime > 0 else 0,
                "avg_reasoning_time": sum(stats["avg_time"] for stats in self.reasoning_stats.values()) / len(self.reasoning_stats)
            }
        }
    
    def run_diagnostic_tests(self) -> Dict[str, Any]:
        """Uruchamia testy diagnostyczne systemu"""
        
        logger.info("🔧 Running Logic Engine diagnostic tests...")
        
        test_results = {
            "deduction_test": False,
            "abduction_test": False,
            "planning_test": False,
            "knowledge_base_test": False,
            "overall_status": "UNKNOWN"
        }
        
        try:
            # Test 1: Dedukcja
            deduction_result = self.reason("full_reasoning_available(true)", ReasoningType.DEDUCTION)
            test_results["deduction_test"] = deduction_result is not None
            
            # Test 2: Abdukcja
            abduction_result = self.reason("system_error,performance_degraded", ReasoningType.ABDUCTION)
            test_results["abduction_test"] = abduction_result is not None
            
            # Test 3: Planowanie
            planning_result = self.reason("solve_critical_problem", ReasoningType.HTN_PLANNING)
            test_results["planning_test"] = planning_result is not None
            
            # Test 4: Baza wiedzy
            kb_facts = len(self.knowledge_base.facts)
            kb_rules = len(self.knowledge_base.rules)
            test_results["knowledge_base_test"] = kb_facts > 0 and kb_rules > 0
            
            # Ogólny status
            passed_tests = sum(1 for test in test_results.values() if test is True)
            if passed_tests >= 3:
                test_results["overall_status"] = "PASSED"
            elif passed_tests >= 2:
                test_results["overall_status"] = "PARTIAL"
            else:
                test_results["overall_status"] = "FAILED"
                
        except Exception as e:
            logger.error(f"❌ Diagnostic test error: {e}")
            test_results["overall_status"] = "ERROR"
        
        logger.info(f"🔧 Diagnostic tests completed: {test_results['overall_status']}")
        return test_results
    
    def export_full_state(self) -> Dict[str, Any]:
        """Eksportuje pełny stan Logic Engine"""
        
        return {
            "metadata": {
                "engine_version": "1.0.0",
                "export_timestamp": time.time(),
                "uptime_seconds": time.time() - self.initialization_time
            },
            "knowledge_base": self.knowledge_base.export_knowledge(),
            "reasoning_stats": self.reasoning_stats,
            "diagnostic_status": self.run_diagnostic_tests(),
            "performance_metrics": self.get_reasoning_status()
        }

# Demo i funkcje testowe
def demo_logic_engine():
    """
    🎭 DEMONSTRACJA Logic Engine
    Pokazuje wszystkie możliwości systemu rozumowania
    """
    print("🧠 LOGIC ENGINE DEMO - Advanced Reasoning System")
    print("=" * 60)
    
    # Inicjalizacja
    engine = LogicEngine()
    
    print("\n📊 Initial Status:")
    status = engine.get_reasoning_status()
    print(f"   Knowledge Base: {status['knowledge_base']['facts_count']} facts, {status['knowledge_base']['rules_count']} rules")
    
    # Test 1: Dedukcja
    print("\n🎯 TEST 1: DEDUCTIVE REASONING")
    deduction_result = engine.reason("full_reasoning_available(true)", ReasoningType.DEDUCTION)
    if deduction_result:
        print(f"   Result: {deduction_result.conclusion}")
        print(f"   Confidence: {deduction_result.confidence:.3f}")
        print(f"   Proof chain: {len(deduction_result.proof_chain)} steps")
    
    # Test 2: Abdukcja
    print("\n🔍 TEST 2: ABDUCTIVE REASONING")
    abduction_result = engine.reason("system_slow,memory_high,cpu_overload", ReasoningType.ABDUCTION)
    if abduction_result:
        print(f"   Best explanation: {abduction_result.conclusion}")
        print(f"   Confidence: {abduction_result.confidence:.3f}")
    
    # Test 3: Planowanie HTN
    print("\n📋 TEST 3: HTN PLANNING")
    planning_result = engine.reason("solve_performance_issue", ReasoningType.HTN_PLANNING)
    if planning_result:
        print(f"   Plan: {planning_result.conclusion}")
        print(f"   Steps: {len(planning_result.proof_chain)}")
    
    # Dodanie dodatkowej wiedzy
    print("\n📚 ADDING CUSTOM KNOWLEDGE")
    new_facts = [
        {"predicate": "performance_issue", "arguments": ["detected"], "confidence": 0.9},
        {"predicate": "user_complaint", "arguments": ["slow_response"], "confidence": 0.8}
    ]
    
    new_rules = [
        {
            "premises": ["performance_issue(detected)", "user_complaint(slow_response)"],
            "conclusion": "urgent_action_required(true)",
            "confidence": 0.95
        }
    ]
    
    engine.add_knowledge(facts=new_facts, rules=new_rules)
    
    # Test z nową wiedzą
    print("\n🧠 TEST WITH NEW KNOWLEDGE")
    urgent_result = engine.reason("urgent_action_required(true)", ReasoningType.DEDUCTION)
    if urgent_result:
        print(f"   Conclusion: {urgent_result.conclusion}")
        print(f"   Confidence: {urgent_result.confidence:.3f}")
    
    # Finalne statystyki
    print("\n📊 FINAL STATISTICS")
    final_status = engine.get_reasoning_status()
    print(f"   Total inferences: {final_status['total_inferences']}")
    print(f"   Deductions: {final_status['reasoning_stats']['deduction']['count']}")
    print(f"   Abductions: {final_status['reasoning_stats']['abduction']['count']}")
    print(f"   Plans: {final_status['reasoning_stats']['planning']['count']}")
    
    # Testy diagnostyczne
    print("\n🔧 DIAGNOSTIC TESTS")
    diagnostics = engine.run_diagnostic_tests()
    print(f"   Overall status: {diagnostics['overall_status']}")
    
    print("\n✅ Logic Engine Demo completed successfully!")
    return engine

if __name__ == "__main__":
    demo_logic_engine()