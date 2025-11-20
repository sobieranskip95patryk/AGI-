# BAYES/bayes_net.py
from typing import Dict, List, Tuple, Any

class Node:
    def __init__(self, name: str, parents: List[str], cpt: Dict[Tuple[Any,...], float]):
        """
        cpt: mapping from parent values tuple (in parent order) + self value -> P(self=True | parents)
        For binary nodes we store P(self=True | parents_tuple).
        Example: parents = ['A','B']
                 cpt = {
                   (True, True): 0.9,
                   (True, False): 0.6,
                   (False, True): 0.7,
                   (False, False): 0.01
                 }
        """
        self.name = name
        self.parents = list(parents)
        self.cpt = dict(cpt)

class BayesNet:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.children: Dict[str, List[str]] = {}

    def add_node(self, node: Node):
        if node.name in self.nodes:
            raise ValueError(f"Node {node.name} exists")
        self.nodes[node.name] = node
        for p in node.parents:
            self.children.setdefault(p, []).append(node.name)

    def topological_order(self) -> List[str]:
        # Kahn's algorithm
        indeg = {n:0 for n in self.nodes}
        for n in self.nodes.values():
            for p in n.parents:
                indeg[n.name] += 1
        queue = [n for n,d in indeg.items() if d==0]
        order=[]
        while queue:
            cur=queue.pop(0)
            order.append(cur)
            for ch in self.children.get(cur,[]):
                indeg[ch]-=1
                if indeg[ch]==0:
                    queue.append(ch)
        if len(order)!=len(self.nodes):
            raise ValueError("Graph has cycle or missing parents")
        return order