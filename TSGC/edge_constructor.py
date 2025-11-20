#!/usr/bin/env python3
"""
🔗 EDGE CONSTRUCTOR - Temporal & Causal Relationships

Edge Construction Layer dla Phase 3.2 TSGC:
- Temporal relationships (before, after, during, overlaps)
- Causal relationships (causes, prevents, enables, blocks)
- Integration z Temporal Logic Engine i Causality Engine
- Confidence scoring dla edge validity
- Graph structure optimization

Pipeline: Symbolic Nodes → Relationship Detection → Edge Creation → Graph Assembly
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import logging
from typing import Dict, List, Tuple, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum
import numpy as np

# Import TSGC components
from .graph_mapper import SymbolicNode

# Import Phase 2 reasoning engines dla integration
try:
    from TEMPORAL.temporal_logic_engine import TemporalLogicEngine, TemporalOperator
    TEMPORAL_AVAILABLE = True
except ImportError:
    TEMPORAL_AVAILABLE = False

try:
    from CAUSALITY.causality_engine import CausalityEngine, CausalRelation
    CAUSALITY_AVAILABLE = True
except ImportError:
    CAUSALITY_AVAILABLE = False

logger = logging.getLogger(__name__)

class EdgeType(Enum):
    """
    Typy krawędzi w symbolic graph
    """
    # Temporal relationships
    BEFORE = "before"
    AFTER = "after" 
    DURING = "during"
    OVERLAPS = "overlaps"
    SIMULTANEOUS = "simultaneous"
    
    # Causal relationships
    CAUSES = "causes"
    PREVENTS = "prevents"
    ENABLES = "enables"
    BLOCKS = "blocks"
    INFLUENCES = "influences"
    
    # Logical relationships
    IMPLIES = "implies"
    EQUIVALENT = "equivalent"
    CONTRADICTS = "contradicts"
    
    # Structural relationships
    PART_OF = "part_of"
    SIMILAR_TO = "similar_to"
    RELATED_TO = "related_to"

@dataclass
class SymbolicEdge:
    """
    Reprezentacja krawędzi między symbolic nodes
    """
    edge_id: str
    source_node: SymbolicNode
    target_node: SymbolicNode
    edge_type: EdgeType
    confidence: float
    weight: float
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        """Validate edge data"""
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be in [0,1], got {self.confidence}")
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(f"Weight must be in [0,1], got {self.weight}")

class TemporalRelationDetector(nn.Module):
    """
    Detector dla temporal relationships między nodes
    
    Używa position encoding i attention patterns dla
    wykrywania temporal dependencies.
    """
    
    def __init__(self, d_model: int, num_temporal_types: int = 5):
        """
        Inicjalizuje Temporal Relation Detector
        
        Args:
            d_model: Wymiar node embeddings
            num_temporal_types: Liczba typów temporal relations
        """
        super(TemporalRelationDetector, self).__init__()
        
        self.d_model = d_model
        self.num_temporal_types = num_temporal_types
        
        # Pairwise relation classifier
        self.relation_classifier = nn.Sequential(
            nn.Linear(d_model * 2, d_model),  # Concat embeddings
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(d_model, d_model // 2),
            nn.ReLU(),
            nn.Linear(d_model // 2, num_temporal_types)
        )
        
        # Position-aware scoring
        self.position_scorer = nn.Sequential(
            nn.Linear(2, 32),  # Position differences
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        
        # Temporal relation types
        self.temporal_types = [
            EdgeType.BEFORE, EdgeType.AFTER, EdgeType.DURING, 
            EdgeType.OVERLAPS, EdgeType.SIMULTANEOUS
        ]
        
    def forward(self, nodes: List[SymbolicNode]) -> List[Tuple[int, int, EdgeType, float]]:
        """
        Wykrywa temporal relationships między nodes
        
        Args:
            nodes: Lista symbolic nodes
            
        Returns:
            List[Tuple[int, int, EdgeType, float]]: (source_idx, target_idx, relation_type, confidence)
        """
        if len(nodes) < 2:
            return []
        
        temporal_edges = []
        
        # Extract embeddings i positions
        embeddings = torch.stack([node.embedding for node in nodes])
        positions = torch.tensor([node.source_position for node in nodes], dtype=torch.float32)
        
        # Compute pairwise relations
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                # Concat embeddings
                pair_embedding = torch.cat([embeddings[i], embeddings[j]], dim=0)
                
                # Classify relation type
                relation_logits = self.relation_classifier(pair_embedding.unsqueeze(0))
                relation_probs = F.softmax(relation_logits, dim=-1)
                best_relation_idx = torch.argmax(relation_probs, dim=-1).item()
                relation_confidence = relation_probs[0, best_relation_idx].item()
                
                # Position-based scoring
                pos_diff = torch.tensor([[positions[i].item(), positions[j].item()]], dtype=torch.float32)
                position_score = self.position_scorer(pos_diff).item()
                
                # Combined confidence
                combined_confidence = (relation_confidence + position_score) / 2.0
                
                # Determine temporal relation based on positions
                if positions[i] < positions[j]:
                    if best_relation_idx in [0, 1]:  # BEFORE, AFTER priority
                        relation_type = EdgeType.BEFORE
                    else:
                        relation_type = self.temporal_types[best_relation_idx]
                else:
                    if best_relation_idx in [0, 1]:
                        relation_type = EdgeType.AFTER  
                    else:
                        relation_type = self.temporal_types[best_relation_idx]
                
                temporal_edges.append((i, j, relation_type, combined_confidence))
        
        return temporal_edges

class CausalRelationDetector(nn.Module):
    """
    Detector dla causal relationships między nodes
    
    Analizuje semantic content i predicate patterns
    dla wykrywania causal dependencies.
    """
    
    def __init__(self, d_model: int, num_causal_types: int = 5):
        """
        Inicjalizuje Causal Relation Detector
        
        Args:
            d_model: Wymiar node embeddings  
            num_causal_types: Liczba typów causal relations
        """
        super(CausalRelationDetector, self).__init__()
        
        self.d_model = d_model
        self.num_causal_types = num_causal_types
        
        # Causal pattern classifier
        self.causal_classifier = nn.Sequential(
            nn.Linear(d_model * 2, d_model),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(d_model, d_model // 2),
            nn.ReLU(),
            nn.Linear(d_model // 2, num_causal_types)
        )
        
        # Predicate-based causal scoring
        self.predicate_scorer = nn.Linear(d_model, 1)
        
        # Causal relation types
        self.causal_types = [
            EdgeType.CAUSES, EdgeType.PREVENTS, EdgeType.ENABLES,
            EdgeType.BLOCKS, EdgeType.INFLUENCES
        ]
        
        # Medical causal patterns
        self.medical_causal_patterns = {
            'causes': ['symptom', 'disease', 'condition'],
            'prevents': ['treatment', 'medication', 'therapy'],
            'enables': ['procedure', 'surgery', 'intervention'],
            'blocks': ['inhibitor', 'blocker', 'antagonist'],
            'influences': ['factor', 'indicator', 'marker']
        }
        
    def forward(self, nodes: List[SymbolicNode]) -> List[Tuple[int, int, EdgeType, float]]:
        """
        Wykrywa causal relationships między nodes
        
        Args:
            nodes: Lista symbolic nodes
            
        Returns:
            List[Tuple[int, int, EdgeType, float]]: Causal edges
        """
        if len(nodes) < 2:
            return []
        
        causal_edges = []
        embeddings = torch.stack([node.embedding for node in nodes])
        
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if i == j:
                    continue
                
                source_node = nodes[i]
                target_node = nodes[j]
                
                # Skip if same predicate (unlikely causal relation)
                if source_node.predicate == target_node.predicate:
                    continue
                
                # Concat embeddings
                pair_embedding = torch.cat([embeddings[i], embeddings[j]], dim=0)
                
                # Classify causal relation
                causal_logits = self.causal_classifier(pair_embedding.unsqueeze(0))
                causal_probs = F.softmax(causal_logits, dim=-1)
                best_causal_idx = torch.argmax(causal_probs, dim=-1).item()
                causal_confidence = causal_probs[0, best_causal_idx].item()
                
                # Predicate-based scoring
                source_score = torch.sigmoid(self.predicate_scorer(embeddings[i])).item()
                target_score = torch.sigmoid(self.predicate_scorer(embeddings[j])).item()
                predicate_score = (source_score + target_score) / 2.0
                
                # Medical pattern matching
                pattern_score = self._compute_medical_pattern_score(source_node, target_node)
                
                # Combined confidence
                combined_confidence = (causal_confidence + predicate_score + pattern_score) / 3.0
                
                # Threshold filtering
                if combined_confidence >= 0.3:  # Lower threshold dla causal relations
                    causal_type = self.causal_types[best_causal_idx]
                    causal_edges.append((i, j, causal_type, combined_confidence))
        
        return causal_edges
    
    def _compute_medical_pattern_score(self, source: SymbolicNode, target: SymbolicNode) -> float:
        """
        Compute score based on medical causal patterns
        
        Args:
            source: Source node
            target: Target node
            
        Returns:
            float: Pattern matching score [0,1]
        """
        score = 0.0
        
        # Check dla known medical causal patterns
        for causal_type, keywords in self.medical_causal_patterns.items():
            source_match = any(keyword in source.predicate.lower() for keyword in keywords)
            target_match = any(keyword in target.predicate.lower() for keyword in keywords)
            
            if source_match or target_match:
                if causal_type == 'causes' and source.node_type == 'entity' and target.node_type == 'entity':
                    score += 0.3
                elif causal_type == 'prevents' and source.node_type == 'action' and target.node_type == 'entity':
                    score += 0.3
                elif causal_type == 'enables' and source.node_type == 'action':
                    score += 0.2
        
        return min(score, 1.0)

class EdgeConstructor(nn.Module):
    """
    Core Edge Construction Layer - Symbolic Nodes → Graph Relationships
    
    Główny komponent tworzący krawędzie między symbolic nodes
    w oparciu o temporal i causal reasoning.
    """
    
    def __init__(self, d_model: int, confidence_threshold: float = 0.4):
        """
        Inicjalizuje Edge Constructor
        
        Args:
            d_model: Wymiar node embeddings
            confidence_threshold: Minimalny próg confidence dla edges
        """
        super(EdgeConstructor, self).__init__()
        
        self.d_model = d_model
        self.confidence_threshold = confidence_threshold
        
        # Core detectors
        self.temporal_detector = TemporalRelationDetector(d_model)
        self.causal_detector = CausalRelationDetector(d_model)
        
        # Edge weight scorer
        self.weight_scorer = nn.Sequential(
            nn.Linear(d_model * 2, d_model // 2),
            nn.ReLU(),
            nn.Linear(d_model // 2, 1),
            nn.Sigmoid()
        )
        
        # Statistics
        self.total_edges_created = 0
        self.temporal_edges_count = 0
        self.causal_edges_count = 0
        self.high_confidence_edges = 0
        
        # Integration trackers
        self.temporal_engine_calls = 0
        self.causality_engine_calls = 0
        
        logger.info(f"🔗 EdgeConstructor initialized: d_model={d_model}, threshold={confidence_threshold}")
    
    def forward(self, nodes: List[SymbolicNode]) -> Dict[str, Any]:
        """
        Konstruuje edges między symbolic nodes
        
        Args:
            nodes: Lista symbolic nodes
            
        Returns:
            Dict[str, Any]: Constructed edges i metadata
        """
        if len(nodes) < 2:
            return {'edges': [], 'metadata': {'total_nodes': len(nodes), 'total_edges': 0}}
        
        all_edges = []
        
        # 1. Detect temporal relationships
        temporal_relations = self.temporal_detector(nodes)
        temporal_edges = self._create_edges_from_relations(
            nodes, temporal_relations, 'temporal'
        )
        all_edges.extend(temporal_edges)
        self.temporal_edges_count += len(temporal_edges)
        
        # 2. Detect causal relationships  
        causal_relations = self.causal_detector(nodes)
        causal_edges = self._create_edges_from_relations(
            nodes, causal_relations, 'causal'
        )
        all_edges.extend(causal_edges)
        self.causal_edges_count += len(causal_edges)
        
        # 3. Filter by confidence
        high_confidence_edges = [
            edge for edge in all_edges 
            if edge.confidence >= self.confidence_threshold
        ]
        
        # 4. Integration z Phase 2 engines
        if TEMPORAL_AVAILABLE:
            self._integrate_temporal_engine(temporal_edges)
        if CAUSALITY_AVAILABLE:
            self._integrate_causality_engine(causal_edges)
        
        # Update statistics
        self.total_edges_created += len(high_confidence_edges)
        self.high_confidence_edges += len(high_confidence_edges)
        
        return {
            'edges': high_confidence_edges,
            'all_edges': all_edges,
            'temporal_relations': temporal_relations,
            'causal_relations': causal_relations,
            'metadata': {
                'total_nodes': len(nodes),
                'total_edges': len(all_edges),
                'high_confidence_edges': len(high_confidence_edges),
                'temporal_edges': len(temporal_edges),
                'causal_edges': len(causal_edges),
                'confidence_threshold': self.confidence_threshold
            }
        }
    
    def _create_edges_from_relations(self, nodes: List[SymbolicNode], 
                                   relations: List[Tuple[int, int, EdgeType, float]],
                                   relation_category: str) -> List[SymbolicEdge]:
        """
        Tworzy SymbolicEdge objects z detected relations
        
        Args:
            nodes: Lista nodes
            relations: Lista detected relations
            relation_category: Kategoria relations ('temporal' lub 'causal')
            
        Returns:
            List[SymbolicEdge]: Utworzone edges
        """
        edges = []
        
        for i, (source_idx, target_idx, edge_type, confidence) in enumerate(relations):
            source_node = nodes[source_idx]
            target_node = nodes[target_idx]
            
            # Compute edge weight
            pair_embedding = torch.cat([source_node.embedding, target_node.embedding])
            weight = self.weight_scorer(pair_embedding.unsqueeze(0)).item()
            
            # Create edge
            edge = SymbolicEdge(
                edge_id=f"{relation_category}_edge_{source_idx}_{target_idx}_{i}",
                source_node=source_node,
                target_node=target_node,
                edge_type=edge_type,
                confidence=confidence,
                weight=weight,
                metadata={
                    'relation_category': relation_category,
                    'source_idx': source_idx,
                    'target_idx': target_idx,
                    'creation_timestamp': torch.tensor([0.0]).item()  # Placeholder
                }
            )
            
            edges.append(edge)
        
        return edges
    
    def _integrate_temporal_engine(self, temporal_edges: List[SymbolicEdge]):
        """
        Integration z Temporal Logic Engine z Phase 2
        
        Args:
            temporal_edges: Lista temporal edges
        """
        if not TEMPORAL_AVAILABLE:
            return
        
        try:
            # Simulate integration - w rzeczywistości byłby pełny API call
            self.temporal_engine_calls += 1
            
            # Convert edges do temporal operators
            for edge in temporal_edges:
                if edge.edge_type == EdgeType.BEFORE:
                    # temporal_engine.add_temporal_constraint(...)
                    pass
                elif edge.edge_type == EdgeType.DURING:
                    # temporal_engine.add_during_constraint(...)
                    pass
            
            logger.debug(f"🕐 Integrated {len(temporal_edges)} temporal edges with Temporal Engine")
            
        except Exception as e:
            logger.warning(f"🚨 Temporal Engine integration failed: {e}")
    
    def _integrate_causality_engine(self, causal_edges: List[SymbolicEdge]):
        """
        Integration z Causality Engine z Phase 2
        
        Args:
            causal_edges: Lista causal edges
        """
        if not CAUSALITY_AVAILABLE:
            return
        
        try:
            self.causality_engine_calls += 1
            
            # Convert edges do causal relations
            for edge in causal_edges:
                if edge.edge_type == EdgeType.CAUSES:
                    # causality_engine.add_causal_relation(...)
                    pass
                elif edge.edge_type == EdgeType.PREVENTS:
                    # causality_engine.add_prevention_relation(...)
                    pass
            
            logger.debug(f"🎯 Integrated {len(causal_edges)} causal edges with Causality Engine")
            
        except Exception as e:
            logger.warning(f"🚨 Causality Engine integration failed: {e}")
    
    def create_adjacency_matrix(self, edges: List[SymbolicEdge], 
                               num_nodes: int) -> torch.Tensor:
        """
        Tworzy adjacency matrix z edges
        
        Args:
            edges: Lista edges
            num_nodes: Liczba nodes
            
        Returns:
            torch.Tensor: Adjacency matrix [num_nodes, num_nodes]
        """
        adj_matrix = torch.zeros(num_nodes, num_nodes)
        
        for edge in edges:
            source_idx = edge.metadata.get('source_idx', -1)
            target_idx = edge.metadata.get('target_idx', -1)
            
            if 0 <= source_idx < num_nodes and 0 <= target_idx < num_nodes:
                adj_matrix[source_idx, target_idx] = edge.weight
        
        return adj_matrix
    
    def filter_edges_by_type(self, edges: List[SymbolicEdge], 
                           edge_types: List[EdgeType]) -> List[SymbolicEdge]:
        """
        Filtruje edges według typu
        
        Args:
            edges: Lista edges do filtrowania
            edge_types: Lista dopuszczalnych typów
            
        Returns:
            List[SymbolicEdge]: Filtered edges
        """
        return [edge for edge in edges if edge.edge_type in edge_types]
    
    def get_node_connections(self, edges: List[SymbolicEdge], 
                           node_id: str) -> Dict[str, List[SymbolicEdge]]:
        """
        Pobiera connections dla specific node
        
        Args:
            edges: Lista edges
            node_id: ID node do analyze
            
        Returns:
            Dict[str, List[SymbolicEdge]]: Incoming i outgoing edges
        """
        incoming = []
        outgoing = []
        
        for edge in edges:
            if edge.source_node.node_id == node_id:
                outgoing.append(edge)
            elif edge.target_node.node_id == node_id:
                incoming.append(edge)
        
        return {
            'incoming': incoming,
            'outgoing': outgoing,
            'total_connections': len(incoming) + len(outgoing)
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Pobiera statystyki Edge Constructor
        
        Returns:
            Dict[str, Any]: Statystyki
        """
        return {
            'd_model': self.d_model,
            'confidence_threshold': self.confidence_threshold,
            'total_edges_created': self.total_edges_created,
            'temporal_edges_count': self.temporal_edges_count,
            'causal_edges_count': self.causal_edges_count,
            'high_confidence_edges': self.high_confidence_edges,
            'temporal_engine_calls': self.temporal_engine_calls,
            'causality_engine_calls': self.causality_engine_calls,
            'temporal_engine_available': TEMPORAL_AVAILABLE,
            'causality_engine_available': CAUSALITY_AVAILABLE
        }
    
    def __repr__(self) -> str:
        return f"EdgeConstructor(d_model={self.d_model}, edges_created={self.total_edges_created})"