# PERCEPTION/symbolizer.py
"""
Symbolizer: konwertuje output modeli percepcyjnych (NN, detectors) na symbole i soft-evidence
dla systemów bayesowskich/logic/causal/temporal.

API:
- symbolize(observations: Dict[str, Any]) -> Dict[str, float]
  zwraca mapę symbol -> confidence (p in [0,1])
"""

from typing import Dict, Any, Callable, List, Tuple

class Symbolizer:
    def __init__(self, mapping: Dict[str, Callable[[Any], float]] = None):
        """
        mapping: dict symbol_name -> function(obs) -> confidence in [0,1]
        Example: "HasFever": lambda obs: obs.get('temp_c',0) > 38.0 ? 0.9 : 0.1
        """
        self.mapping = mapping or {}

    def register(self, symbol: str, fn: Callable[[Dict[str,Any]], float]) -> None:
        self.mapping[symbol] = fn

    def symbolize(self, observations: Dict[str, Any]) -> Dict[str, float]:
        results = {}
        for sym, fn in self.mapping.items():
            try:
                v = float(fn(observations))
                # clamp
                v = max(0.0, min(1.0, v))
            except Exception:
                v = 0.0
            results[sym] = v
        return results

    def top_symbols(self, observations: Dict[str,Any], thresh: float=0.5, k:int=10) -> List[Tuple[str,float]]:
        syms = self.symbolize(observations)
        filtered = [(s,p) for s,p in syms.items() if p>=thresh]
        filtered.sort(key=lambda x: x[1], reverse=True)
        return filtered[:k]