# ILP/hypothesis_generator.py
"""
Hypothesis Generator - zaawansowane generowanie hipotez dla ILP
Używa heurystyk i beam search do efektywnego przeszukiwania przestrzeni hipotez
"""

from typing import List, Set, Generator
import heapq
from .ilp_engine import Rule, Atom, Predicate

class HypothesisSpace:
    def __init__(self, predicates: Set[Predicate], max_clause_length: int = 4):
        self.predicates = predicates
        self.max_clause_length = max_clause_length
        self.variable_names = ['X', 'Y', 'Z', 'W', 'V', 'U']
    
    def generate_candidates(self, target_predicate: str, beam_width: int = 100) -> List[Rule]:
        """Generuje kandydatów używając beam search"""
        candidates = []
        
        # Start with most general rules
        beam = [Rule(Atom(target_predicate, self.variable_names[:2]), [])]
        
        for depth in range(self.max_clause_length):
            new_beam = []
            
            for rule in beam:
                # Expand rule by adding body literals
                expansions = self._expand_rule(rule)
                new_beam.extend(expansions)
            
            # Keep only best candidates
            new_beam.sort(key=lambda r: self._heuristic_score(r), reverse=True)
            beam = new_beam[:beam_width]
            
            candidates.extend(beam)
        
        return candidates
    
    def _expand_rule(self, rule: Rule) -> List[Rule]:
        """Rozszerza regułę dodając jeden literal do ciała"""
        expansions = []
        
        # Get variables used in current rule
        used_vars = set()
        for atom in [rule.head] + rule.body:
            used_vars.update(atom.args)
        
        # Try adding each predicate to body
        for pred in self.predicates:
            if pred.name == rule.head.predicate:
                continue  # Avoid direct recursion
            
            # Generate argument combinations
            available_vars = list(used_vars) + [v for v in self.variable_names if v not in used_vars][:2]
            
            for i in range(min(len(available_vars), pred.arity)):
                args = available_vars[:pred.arity]
                new_atom = Atom(pred.name, args)
                new_rule = Rule(rule.head, rule.body + [new_atom])
                expansions.append(new_rule)
        
        return expansions
    
    def _heuristic_score(self, rule: Rule) -> float:
        """Heurystyczna ocena reguły"""
        # Prefer shorter rules initially
        length_penalty = len(rule.body) * 0.1
        
        # Prefer rules with more connected variables
        all_vars = set()
        for atom in [rule.head] + rule.body:
            all_vars.update(v for v in atom.args if v.isupper())
        
        connectivity_bonus = len(all_vars) * 0.2
        
        return connectivity_bonus - length_penalty

class AdvancedHypothesisGenerator:
    def __init__(self):
        self.mode_declarations = {}
        self.type_hierarchy = {}
    
    def add_mode_declaration(self, predicate: str, mode: str):
        """Dodaje deklarację modu dla predykatu (input/output)"""
        self.mode_declarations[predicate] = mode
    
    def generate_typed_hypotheses(self, target: str, types: dict) -> List[Rule]:
        """Generuje hipotezy z uwzględnieniem typów"""
        hypotheses = []
        
        # Use type information to constrain hypothesis generation
        if target in types:
            target_type = types[target]
            compatible_preds = [p for p, t in types.items() if self._type_compatible(t, target_type)]
            
            # Generate rules using only compatible predicates
            for pred in compatible_preds:
                rule = self._construct_typed_rule(target, pred, types)
                if rule:
                    hypotheses.append(rule)
        
        return hypotheses
    
    def _type_compatible(self, type1: str, type2: str) -> bool:
        """Sprawdza kompatybilność typów"""
        # Simple type compatibility check
        return type1 == type2 or type1 == 'any' or type2 == 'any'
    
    def _construct_typed_rule(self, head_pred: str, body_pred: str, types: dict) -> Rule:
        """Konstruuje regułę z uwzględnieniem typów"""
        # Simple typed rule construction
        head = Atom(head_pred, ['X'])
        body = [Atom(body_pred, ['X'])]
        return Rule(head, body)

class MetaLearningHypothesisGenerator:
    def __init__(self):
        self.successful_patterns = []
        self.pattern_scores = {}
    
    def learn_from_success(self, successful_rule: Rule, score: float):
        """Uczy się z udanych reguł"""
        pattern = self._extract_pattern(successful_rule)
        self.successful_patterns.append(pattern)
        self.pattern_scores[pattern] = score
    
    def generate_from_patterns(self, target_predicate: str) -> List[Rule]:
        """Generuje hipotezy bazując na nauczonych wzorcach"""
        hypotheses = []
        
        for pattern in self.successful_patterns:
            if pattern['target_type'] == 'binary':  # Example pattern matching
                # Generate similar rule structure
                rule = self._instantiate_pattern(pattern, target_predicate)
                if rule:
                    hypotheses.append(rule)
        
        return hypotheses
    
    def _extract_pattern(self, rule: Rule) -> dict:
        """Wydobywa wzorzec z reguły"""
        return {
            'target_type': 'binary' if len(rule.head.args) == 2 else 'unary',
            'body_length': len(rule.body),
            'predicates_used': [atom.predicate for atom in rule.body]
        }
    
    def _instantiate_pattern(self, pattern: dict, target_predicate: str) -> Rule:
        """Tworzy regułę na podstawie wzorca"""
        # Simple pattern instantiation
        if pattern['target_type'] == 'binary':
            head = Atom(target_predicate, ['X', 'Y'])
        else:
            head = Atom(target_predicate, ['X'])
        
        body = []
        for pred in pattern['predicates_used']:
            body.append(Atom(pred, ['X']))
        
        return Rule(head, body)