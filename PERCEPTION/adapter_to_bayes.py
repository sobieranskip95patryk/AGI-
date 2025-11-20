# PERCEPTION/adapter_to_bayes.py
"""
Adapter: zamienia symbole z confidence w 'soft evidence' dla BayesNet.
Implementujemy prostą transformację: symbol confidence -> likelihood ratio / virtual evidence.
For our Bayes module (which expects hard evidence), we produce hard evidence via thresholding
or use sampling (weighted samples) to approximate soft evidence.
"""

from typing import Dict, Any
from BAYES import BayesNet, prior_sample
import random

def evidence_from_symbols(symbol_conf: Dict[str,float], threshold: float=0.5) -> Dict[str,bool]:
    # simple thresholding -> hard evidence
    return {s: (p >= threshold) for s,p in symbol_conf.items()}

def weighted_sampling_for_soft_evidence(bn: BayesNet, symbol_conf: Dict[str,float], N:int=500):
    """
    Create weighted estimate of marginals given soft evidences.
    Approach: sample from prior, weight by likelihood of observed symbols given sample.
    Assumes each symbol corresponds to a variable in BN and P(symbol|var) ~ symbol_conf if var=True else (1-symbol_conf)
    This is a simplistic approximation — replace with likelihood models in production.
    """
    counts = {v:0.0 for v in bn.nodes}
    weights_sum = 0.0
    for _ in range(N):
        s = prior_sample(bn)
        weight = 1.0
        for sym, conf in symbol_conf.items():
            if sym not in s:
                continue
            p_obs_given_true = conf
            p_obs_given_false = 1.0 - conf
            weight *= p_obs_given_true if s[sym] else p_obs_given_false
        weights_sum += weight
        for var, val in s.items():
            counts[var] += weight if val else 0.0
    if weights_sum == 0:
        return {k:0.0 for k in counts}
    return {k: counts[k]/weights_sum for k in counts}