# BAYES/inference.py
from typing import Dict, Any, List
from .bayes_net import BayesNet
import random

def enum_all(variables: List[str], bn: BayesNet, evidence: Dict[str, bool]) -> float:
    if not variables:
        return 1.0
    Y = variables[0]
    rest = variables[1:]
    if Y in evidence:
        prob = prob_of(Y, evidence[Y], bn, evidence)
        return prob * enum_all(rest, bn, evidence)
    else:
        # sum over Y = True/False
        total = 0.0
        for y_val in (True, False):
            evidence2 = dict(evidence)
            evidence2[Y] = y_val
            total += prob_of(Y, y_val, bn, evidence2) * enum_all(rest, bn, evidence2)
        return total

def prob_of(var: str, value: bool, bn: BayesNet, evidence: Dict[str, bool]) -> float:
    node = bn.nodes[var]
    parent_vals = tuple(evidence[p] for p in node.parents)
    p_true = node.cpt.get(parent_vals, 0.0)
    return p_true if value else (1.0 - p_true)

def query_marginal(bn: BayesNet, query: str, evidence: Dict[str, bool]) -> float:
    # P(query=True | evidence)
    vars_order = bn.topological_order()
    Q = query
    numerator_e = dict(evidence)
    numerator_e[Q] = True
    numerator = enum_all(vars_order, bn, numerator_e)
    denom = enum_all(vars_order, bn, dict(evidence))
    if denom == 0:
        return 0.0
    return numerator / denom

def prior_sample(bn: BayesNet) -> Dict[str, bool]:
    sample = {}
    for var in bn.topological_order():
        node = bn.nodes[var]
        parent_vals = tuple(sample[p] for p in node.parents)
        p_true = node.cpt.get(parent_vals, 0.0)
        sample[var] = random.random() < p_true
    return sample

def rejection_sampling(bn: BayesNet, query: str, evidence: Dict[str,bool], N:int=1000) -> float:
    count_q_and_e = 0
    count_e = 0
    for _ in range(N):
        s = prior_sample(bn)
        match = all(s[k]==v for k,v in evidence.items())
        if match:
            count_e += 1
            if s[query]:
                count_q_and_e += 1
    if count_e == 0:
        return 0.0
    return count_q_and_e / count_e