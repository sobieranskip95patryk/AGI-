# ILP/ilp_engine.py
"""
Inductive Logic Programming Engine - automatyczne generowanie reguł logicznych z obserwacji
Integruje się z Logic Engine, Causality Engine i Bayesian Engine
"""

from typing import Dict, List, Set, Tuple, Any, Optional
import itertools
from collections import defaultdict

class Predicate:
    def __init__(self, name: str, arity: int):
        self.name = name
        self.arity = arity
    
    def __str__(self):
        return f"{self.name}/{self.arity}"
    
    def __eq__(self, other):
        return isinstance(other, Predicate) and self.name == other.name and self.arity == other.arity
    
    def __hash__(self):
        return hash((self.name, self.arity))

class Atom:
    def __init__(self, predicate: str, args: List[str]):
        self.predicate = predicate
        self.args = args
    
    def __str__(self):
        return f"{self.predicate}({', '.join(self.args)})"
    
    def __eq__(self, other):
        return isinstance(other, Atom) and self.predicate == other.predicate and self.args == other.args
    
    def __hash__(self):
        return hash((self.predicate, tuple(self.args)))

class Rule:
    def __init__(self, head: Atom, body: List[Atom]):
        self.head = head
        self.body = body
        self.confidence = 0.0
    
    def __str__(self):
        if not self.body:
            return f"{self.head}."
        body_str = ", ".join(str(atom) for atom in self.body)
        return f"{self.head} :- {body_str}."

class ILPEngine:
    def __init__(self):
        self.background_knowledge: Set[Atom] = set()
        self.positive_examples: Set[Atom] = set()
        self.negative_examples: Set[Atom] = set()
        self.learned_rules: List[Rule] = []
        self.predicates: Set[Predicate] = set()
        
    def add_background_knowledge(self, facts: List[Atom]):
        """Dodaje wiedzę podstawową (background knowledge)"""
        for fact in facts:
            self.background_knowledge.add(fact)
            # Extract predicates
            pred = Predicate(fact.predicate, len(fact.args))
            self.predicates.add(pred)
    
    def add_positive_examples(self, examples: List[Atom]):
        """Dodaje pozytywne przykłady do uczenia"""
        for example in examples:
            self.positive_examples.add(example)
    
    def add_negative_examples(self, examples: List[Atom]):
        """Dodaje negatywne przykłady do uczenia"""
        for example in examples:
            self.negative_examples.add(example)
    
    def generate_hypotheses(self, max_body_length: int = 3) -> List[Rule]:
        """Generuje hipotezy reguł używając bottom-up approach"""
        hypotheses = []
        
        # For each positive example, try to generalize
        for pos_example in self.positive_examples:
            # Generate candidate rules with this example as head
            for body_length in range(0, max_body_length + 1):
                if body_length == 0:
                    # Fact rule
                    rule = Rule(pos_example, [])
                    if self._is_consistent(rule):
                        hypotheses.append(rule)
                else:
                    # Generate combinations of body atoms
                    candidate_bodies = self._generate_candidate_bodies(body_length, pos_example)
                    for body in candidate_bodies:
                        rule = Rule(pos_example, body)
                        if self._is_consistent(rule) and self._covers_positive(rule):
                            hypotheses.append(rule)
        
        return hypotheses
    
    def _generate_candidate_bodies(self, length: int, head: Atom) -> List[List[Atom]]:
        """Generuje kandydatów na ciało reguły"""
        candidates = []
        
        # Use variables from head and constants from background knowledge
        variables = set(head.args)
        constants = set()
        for fact in self.background_knowledge:
            constants.update(fact.args)
        
        # Generate atoms using available predicates
        possible_atoms = []
        for pred in self.predicates:
            if pred.name != head.predicate:  # Avoid recursive rules for now
                # Generate argument combinations
                all_terms = list(variables) + list(constants)
                for args_combo in itertools.combinations_with_replacement(all_terms, pred.arity):
                    atom = Atom(pred.name, list(args_combo))
                    possible_atoms.append(atom)
        
        # Generate combinations of atoms for body
        for atoms_combo in itertools.combinations(possible_atoms, length):
            candidates.append(list(atoms_combo))
        
        return candidates[:50]  # Limit to prevent explosion
    
    def _is_consistent(self, rule: Rule) -> bool:
        """Sprawdza czy reguła jest spójna z przykładami negatywnymi"""
        # Simple consistency check - rule shouldn't prove negative examples
        for neg_example in self.negative_examples:
            if self._unifies(rule.head, neg_example):
                # Check if body can be satisfied
                if self._can_prove_body(rule.body, neg_example):
                    return False
        return True
    
    def _covers_positive(self, rule: Rule) -> bool:
        """Sprawdza czy reguła pokrywa jakiś pozytywny przykład"""
        for pos_example in self.positive_examples:
            if self._unifies(rule.head, pos_example):
                if self._can_prove_body(rule.body, pos_example):
                    return True
        return False
    
    def _unifies(self, atom1: Atom, atom2: Atom) -> bool:
        """Prosta unifikacja atomów"""
        if atom1.predicate != atom2.predicate:
            return False
        if len(atom1.args) != len(atom2.args):
            return False
        
        # Simple syntactic unification
        substitution = {}
        for arg1, arg2 in zip(atom1.args, atom2.args):
            if arg1.isupper() and arg2.isupper():  # Both variables
                continue
            elif arg1.isupper():  # arg1 is variable
                if arg1 in substitution and substitution[arg1] != arg2:
                    return False
                substitution[arg1] = arg2
            elif arg2.isupper():  # arg2 is variable
                if arg2 in substitution and substitution[arg2] != arg1:
                    return False
                substitution[arg2] = arg1
            else:  # Both constants
                if arg1 != arg2:
                    return False
        return True
    
    def _can_prove_body(self, body: List[Atom], example: Atom) -> bool:
        """Sprawdza czy ciało reguły może być udowodnione"""
        if not body:
            return True
        
        # Simple check - see if all body atoms are in background knowledge
        for body_atom in body:
            found = False
            for bg_fact in self.background_knowledge:
                if self._unifies(body_atom, bg_fact):
                    found = True
                    break
            if not found:
                return False
        return True
    
    def learn_rules(self, max_rules: int = 10) -> List[Rule]:
        """Główna metoda uczenia reguł"""
        hypotheses = self.generate_hypotheses()
        
        # Score and rank hypotheses
        scored_rules = []
        for rule in hypotheses:
            score = self._score_rule(rule)
            rule.confidence = score
            scored_rules.append((score, rule))
        
        # Sort by score and return top rules
        scored_rules.sort(key=lambda x: x[0], reverse=True)
        
        self.learned_rules = [rule for score, rule in scored_rules[:max_rules]]
        return self.learned_rules
    
    def _score_rule(self, rule: Rule) -> float:
        """Ocenia jakość reguły"""
        positive_coverage = 0
        negative_coverage = 0
        
        # Count positive examples covered
        for pos_example in self.positive_examples:
            if self._unifies(rule.head, pos_example) and self._can_prove_body(rule.body, pos_example):
                positive_coverage += 1
        
        # Count negative examples covered (should be 0)
        for neg_example in self.negative_examples:
            if self._unifies(rule.head, neg_example) and self._can_prove_body(rule.body, neg_example):
                negative_coverage += 1
        
        # Simple scoring: precision-like measure
        if positive_coverage + negative_coverage == 0:
            return 0.0
        
        precision = positive_coverage / (positive_coverage + negative_coverage)
        recall = positive_coverage / len(self.positive_examples) if self.positive_examples else 0
        
        # F1-like score
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)
    
    def get_learned_rules_summary(self) -> Dict[str, Any]:
        """Zwraca podsumowanie nauczonych reguł"""
        return {
            "total_rules": len(self.learned_rules),
            "average_confidence": sum(rule.confidence for rule in self.learned_rules) / len(self.learned_rules) if self.learned_rules else 0,
            "rules": [{"rule": str(rule), "confidence": rule.confidence} for rule in self.learned_rules]
        }