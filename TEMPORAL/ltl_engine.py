# TEMPORAL/ltl_engine.py
"""
Prosty LTL engine: parse + evaluate on finite traces.
Nie jest to pełna implementacja LTL — to lekki, rozszerzalny moduł
do walidacji sekwencji zdarzeń i integrowania z Planner/HTN.
"""

from typing import List, Dict, Any, Iterable

class LTLError(Exception):
    pass

class LTLEngine:
    def __init__(self):
        # tu można dodać cache, zoptymalizowane struktury
        self._cache = {}

    def parse(self, formula: str) -> str:
        """
        Placeholder parser — w tym etapie przechowujemy formułę jako string.
        Przykład formuł: "G(req -> F(resp))", "F(success)", "G(!error)"
        """
        if not formula or not isinstance(formula, str):
            raise LTLError("Invalid LTL formula")
        # prosty normalizer
        return formula.strip()

    def evaluate_on_trace(self, formula: str, trace: Iterable[Dict[str, Any]]) -> bool:
        """
        Evaluate a (parsed) LTL formula on a finite trace.
        trace: iterable of states, each state is dict of atomic propositions -> bool
        NOTE: This is a lightweight evaluator supporting:
          - F(p) (eventually p)
          - G(p) (always p)
          - p -> q
          - !p (not), & (and), | (or)
        For complex usage replace with full LTL library.
        """
        f = self.parse(formula)
        states = list(trace)
        if not states:
            return False

        # Hand-rolled simple checks:
        # handle basic F(...) and G(...)
        if f.startswith("F(") and f.endswith(")"):
            atom = f[2:-1].strip()
            return any(self._eval_atom(atom, s) for s in states)
        if f.startswith("G(") and f.endswith(")"):
            atom = f[2:-1].strip()
            return all(self._eval_atom(atom, s) for s in states)

        # implication pattern a -> b (very naive split)  
        if "->" in f:
            left, right = f.split("->", 1)
            left = left.strip()
            right = right.strip()
            # For temporal implication: if left appears anywhere, right must appear somewhere after
            left_found = False
            right_found = False
            
            for s in states:
                if self._eval_atom(left, s):
                    left_found = True
                if self._eval_atom(right, s):
                    right_found = True
            
            # If left never appears, implication is vacuously true
            # If left appears, right must also appear in the trace
            return not left_found or right_found

        # single atom
        return all(self._eval_atom(f, s) for s in states)

    def _eval_atom(self, atom: str, state: Dict[str, Any]) -> bool:
        atom = atom.strip()
        # boolean operators
        if atom.startswith('!'):
            return not self._eval_atom(atom[1:].strip(), state)
        if '&' in atom:
            parts = [p.strip() for p in atom.split('&')]
            return all(self._eval_atom(p, state) for p in parts)
        if '|' in atom:
            parts = [p.strip() for p in atom.split('|')]
            return any(self._eval_atom(p, state) for p in parts)
        # direct proposition lookup
        return bool(state.get(atom, False))