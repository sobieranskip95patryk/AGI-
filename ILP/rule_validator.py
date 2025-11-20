# ILP/rule_validator.py
"""
Rule Validator - walidacja i ocena jakości nauczonych reguł
Integruje się z Logic Engine i Bayesian Engine do weryfikacji reguł
"""

from typing import List, Dict, Set, Tuple
from .ilp_engine import Rule, Atom

class RuleValidator:
    def __init__(self):
        self.validation_metrics = {}
        self.statistical_thresholds = {
            'min_precision': 0.7,
            'min_recall': 0.3,
            'min_f1': 0.5,
            'max_complexity': 5
        }
    
    def validate_rule_set(self, rules: List[Rule], 
                         positive_examples: Set[Atom], 
                         negative_examples: Set[Atom],
                         background_knowledge: Set[Atom]) -> Dict[str, float]:
        """Waliduje zestaw reguł względem przykładów"""
        
        total_metrics = {
            'precision': 0.0,
            'recall': 0.0,
            'f1_score': 0.0,
            'coverage': 0.0,
            'consistency': 0.0,
            'complexity': 0.0
        }
        
        if not rules:
            return total_metrics
        
        # Validate each rule individually
        rule_scores = []
        for rule in rules:
            metrics = self._validate_single_rule(rule, positive_examples, 
                                               negative_examples, background_knowledge)
            rule_scores.append(metrics)
        
        # Aggregate metrics
        for metric in total_metrics.keys():
            total_metrics[metric] = sum(score[metric] for score in rule_scores) / len(rule_scores)
        
        # Additional set-level metrics
        total_metrics['rule_count'] = len(rules)
        total_metrics['redundancy'] = self._calculate_redundancy(rules)
        total_metrics['completeness'] = self._calculate_completeness(rules, positive_examples)
        
        return total_metrics
    
    def _validate_single_rule(self, rule: Rule, 
                            positive_examples: Set[Atom],
                            negative_examples: Set[Atom],
                            background_knowledge: Set[Atom]) -> Dict[str, float]:
        """Waliduje pojedynczą regułę"""
        
        # Coverage analysis
        true_positives = self._count_covered_examples(rule, positive_examples, background_knowledge)
        false_positives = self._count_covered_examples(rule, negative_examples, background_knowledge)
        false_negatives = len(positive_examples) - true_positives
        
        # Calculate metrics
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        # Complexity metrics
        complexity = len(rule.body) + len(set(var for atom in [rule.head] + rule.body for var in atom.args if var.isupper()))
        
        # Consistency check
        consistency = 1.0 if false_positives == 0 else max(0.0, 1.0 - false_positives / len(negative_examples))
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'coverage': true_positives / len(positive_examples) if positive_examples else 0.0,
            'consistency': consistency,
            'complexity': complexity / 10.0  # Normalize complexity
        }
    
    def _count_covered_examples(self, rule: Rule, examples: Set[Atom], 
                              background_knowledge: Set[Atom]) -> int:
        """Liczy przykłady pokryte przez regułę"""
        covered = 0
        
        for example in examples:
            if self._rule_covers_example(rule, example, background_knowledge):
                covered += 1
        
        return covered
    
    def _rule_covers_example(self, rule: Rule, example: Atom, 
                           background_knowledge: Set[Atom]) -> bool:
        """Sprawdza czy reguła pokrywa przykład"""
        
        # Simple coverage check - head must unify with example
        if not self._unify(rule.head, example):
            return False
        
        # All body literals must be provable from background knowledge
        for body_atom in rule.body:
            if not self._can_prove_atom(body_atom, background_knowledge):
                return False
        
        return True
    
    def _unify(self, atom1: Atom, atom2: Atom) -> bool:
        """Prosta unifikacja atomów"""
        if atom1.predicate != atom2.predicate or len(atom1.args) != len(atom2.args):
            return False
        
        substitution = {}
        for arg1, arg2 in zip(atom1.args, atom2.args):
            if arg1.isupper():  # Variable
                if arg1 in substitution:
                    if substitution[arg1] != arg2:
                        return False
                else:
                    substitution[arg1] = arg2
            elif arg1 != arg2:  # Constants must match
                return False
        
        return True
    
    def _can_prove_atom(self, atom: Atom, background_knowledge: Set[Atom]) -> bool:
        """Sprawdza czy atom może być udowodniony z wiedzy podstawowej"""
        for bg_atom in background_knowledge:
            if self._unify(atom, bg_atom):
                return True
        return False
    
    def _calculate_redundancy(self, rules: List[Rule]) -> float:
        """Oblicza redundancję w zestawie reguł"""
        if len(rules) <= 1:
            return 0.0
        
        redundant_pairs = 0
        total_pairs = 0
        
        for i, rule1 in enumerate(rules):
            for j, rule2 in enumerate(rules[i+1:], i+1):
                total_pairs += 1
                if self._rules_redundant(rule1, rule2):
                    redundant_pairs += 1
        
        return redundant_pairs / total_pairs if total_pairs > 0 else 0.0
    
    def _rules_redundant(self, rule1: Rule, rule2: Rule) -> bool:
        """Sprawdza czy dwie reguły są redundantne"""
        # Simple redundancy check - same head predicate and similar body
        if rule1.head.predicate != rule2.head.predicate:
            return False
        
        # Check body similarity
        body1_preds = set(atom.predicate for atom in rule1.body)
        body2_preds = set(atom.predicate for atom in rule2.body)
        
        if len(body1_preds.intersection(body2_preds)) / max(len(body1_preds), len(body2_preds), 1) > 0.8:
            return True
        
        return False
    
    def _calculate_completeness(self, rules: List[Rule], positive_examples: Set[Atom]) -> float:
        """Oblicza kompletność zestawu reguł"""
        if not positive_examples:
            return 1.0
        
        covered_examples = set()
        
        for rule in rules:
            for example in positive_examples:
                if self._unify(rule.head, example):
                    covered_examples.add(example)
        
        return len(covered_examples) / len(positive_examples)
    
    def prune_rules(self, rules: List[Rule], 
                   positive_examples: Set[Atom],
                   negative_examples: Set[Atom],
                   background_knowledge: Set[Atom]) -> List[Rule]:
        """Przycinanie reguł - usuwa słabe i redundantne reguły"""
        
        # Score all rules
        scored_rules = []
        for rule in rules:
            metrics = self._validate_single_rule(rule, positive_examples, 
                                               negative_examples, background_knowledge)
            
            # Composite score
            score = (metrics['f1_score'] * 0.4 + 
                    metrics['precision'] * 0.3 + 
                    metrics['recall'] * 0.2 + 
                    (1 - metrics['complexity']) * 0.1)
            
            scored_rules.append((score, rule, metrics))
        
        # Sort by score
        scored_rules.sort(key=lambda x: x[0], reverse=True)
        
        # Filter by thresholds
        filtered_rules = []
        for score, rule, metrics in scored_rules:
            if (metrics['precision'] >= self.statistical_thresholds['min_precision'] and
                metrics['recall'] >= self.statistical_thresholds['min_recall'] and
                metrics['f1_score'] >= self.statistical_thresholds['min_f1'] and
                metrics['complexity'] <= self.statistical_thresholds['max_complexity']):
                filtered_rules.append(rule)
        
        # Remove redundant rules
        final_rules = []
        for rule in filtered_rules:
            is_redundant = False
            for existing_rule in final_rules:
                if self._rules_redundant(rule, existing_rule):
                    is_redundant = True
                    break
            if not is_redundant:
                final_rules.append(rule)
        
        return final_rules