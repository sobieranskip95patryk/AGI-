#!/usr/bin/env python3
"""
🧠 GRAPH MAPPER - Hidden States → Symbolic Nodes Conversion

Graph Mapping Layer dla Phase 3.2 TSGC:
- Konwersja Transformer hidden states na symbolic nodes
- Predicate classification i confidence scoring  
- Node type detection (entity, relation, action)
- Integration z ILP Engine symbology
- Batch processing dla efficiency

Pipeline: Hidden States → Node Classification → Predicate Extraction → Confidence Scoring
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import logging
from typing import Dict, List, Tuple, Any, Optional, NamedTuple
from dataclasses import dataclass
import numpy as np

# Import ILP components dla symbolic integration
try:
    from ILP.ilp_engine import Atom, Predicate
    ILP_AVAILABLE = True
except ImportError:
    ILP_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class SymbolicNode:
    """
    Reprezentacja symbolic node z metadanymi
    """
    node_id: str
    node_type: str  # 'entity', 'relation', 'action', 'property'
    predicate: str
    arguments: List[str]
    confidence: float
    embedding: torch.Tensor
    source_position: int  # Position in original sequence
    metadata: Dict[str, Any]

class NodeTypeClassifier(nn.Module):
    """
    Node Type Classifier (entity, relation, action, property)
    
    Klasyfikuje hidden states na różne typy symbolic nodes
    w oparciu o semantic content.
    """
    
    def __init__(self, d_model: int, num_node_types: int = 4):
        """
        Inicjalizuje Node Type Classifier
        
        Args:
            d_model: Wymiar hidden states
            num_node_types: Liczba typów nodes (default: 4)
        """
        super(NodeTypeClassifier, self).__init__()
        
        self.d_model = d_model
        self.num_node_types = num_node_types
        
        # Node type classification head
        self.classifier = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(d_model // 2, num_node_types)
        )
        
        # Node type labels
        self.node_type_labels = ['entity', 'relation', 'action', 'property']
        
    def forward(self, hidden_states: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Klasyfikuje hidden states na typy nodes
        
        Args:
            hidden_states: Hidden states [batch_size, seq_len, d_model]
            
        Returns:
            Dict[str, torch.Tensor]: Classification results
        """
        # Reshape dla classification
        batch_size, seq_len, d_model = hidden_states.shape
        flat_states = hidden_states.view(-1, d_model)  # [batch_size * seq_len, d_model]
        
        # Classify node types
        logits = self.classifier(flat_states)  # [batch_size * seq_len, num_node_types]
        probabilities = F.softmax(logits, dim=-1)
        
        # Reshape back
        logits = logits.view(batch_size, seq_len, self.num_node_types)
        probabilities = probabilities.view(batch_size, seq_len, self.num_node_types)
        
        return {
            'logits': logits,
            'probabilities': probabilities,
            'predicted_types': torch.argmax(probabilities, dim=-1)
        }

class PredicateExtractor(nn.Module):
    """
    Predicate Extractor z Vocabulary Mapping
    
    Mapuje hidden states na predicate names używając
    learned vocabulary i similarity matching.
    """
    
    def __init__(self, d_model: int, vocab_size: int = 1000):
        """
        Inicjalizuje Predicate Extractor
        
        Args:
            d_model: Wymiar hidden states
            vocab_size: Rozmiar predicate vocabulary
        """
        super(PredicateExtractor, self).__init__()
        
        self.d_model = d_model
        self.vocab_size = vocab_size
        
        # Predicate vocabulary embeddings
        self.predicate_embeddings = nn.Embedding(vocab_size, d_model)
        
        # Projection head dla mapping
        self.projection = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.Tanh(),
            nn.Linear(d_model, d_model)
        )
        
        # Default medical predicates dla initialization
        self.default_predicates = [
            'symptom', 'disease', 'treatment', 'causes', 'requires',
            'has_property', 'located_at', 'temporal_relation', 'causal_relation',
            'similar_to', 'part_of', 'instance_of', 'affects', 'prevents'
        ]
        
        # Initialize predicate vocabulary
        self._initialize_vocabulary()
        
    def _initialize_vocabulary(self):
        """Inicjalizuje vocabulary z default predicates"""
        self.predicate_to_id = {pred: i for i, pred in enumerate(self.default_predicates)}
        self.id_to_predicate = {i: pred for pred, i in self.predicate_to_id.items()}
        
        # Fill remaining vocabulary with generic predicates
        for i in range(len(self.default_predicates), min(self.vocab_size, 100)):
            generic_pred = f"pred_{i}"
            self.predicate_to_id[generic_pred] = i 
            self.id_to_predicate[i] = generic_pred
    
    def forward(self, hidden_states: torch.Tensor, 
                top_k: int = 5) -> Dict[str, torch.Tensor]:
        """
        Ekstraktuje predicates z hidden states
        
        Args:
            hidden_states: Hidden states [batch_size, seq_len, d_model]
            top_k: Liczba top predicates do return
            
        Returns:
            Dict[str, torch.Tensor]: Extracted predicates i scores
        """
        # Project hidden states
        projected = self.projection(hidden_states)  # [batch_size, seq_len, d_model]
        
        # Get all predicate embeddings
        all_pred_embeddings = self.predicate_embeddings.weight  # [vocab_size, d_model]
        
        # Compute similarity scores
        batch_size, seq_len, d_model = projected.shape
        projected_flat = projected.view(-1, d_model)  # [batch_size * seq_len, d_model]
        
        # Cosine similarity
        projected_norm = F.normalize(projected_flat, p=2, dim=1)
        pred_norm = F.normalize(all_pred_embeddings, p=2, dim=1) 
        
        similarity_scores = torch.mm(projected_norm, pred_norm.t())  # [batch_size * seq_len, vocab_size]
        similarity_scores = similarity_scores.view(batch_size, seq_len, self.vocab_size)
        
        # Get top-k predicates
        top_scores, top_indices = torch.topk(similarity_scores, top_k, dim=-1)
        
        return {
            'similarity_scores': similarity_scores,
            'top_scores': top_scores,
            'top_indices': top_indices
        }
    
    def get_predicate_names(self, indices: torch.Tensor) -> List[List[str]]:
        """
        Konwertuje predicate indices na names
        
        Args:
            indices: Tensor indices [batch_size, seq_len, top_k]
            
        Returns:
            List[List[str]]: Predicate names
        """
        batch_names = []
        
        for batch_idx in range(indices.shape[0]):
            seq_names = []
            for seq_idx in range(indices.shape[1]):
                token_names = []
                for k in range(indices.shape[2]):
                    pred_id = indices[batch_idx, seq_idx, k].item()
                    pred_name = self.id_to_predicate.get(pred_id, f"unk_{pred_id}")
                    token_names.append(pred_name)
                seq_names.append(token_names)
            batch_names.append(seq_names)
        
        return batch_names

class GraphMapper(nn.Module):
    """
    Core Graph Mapping Layer - Hidden States -> Symbolic Nodes
    
    Główny komponent konwertujący Transformer hidden states
    na structured symbolic nodes dla ILP reasoning.
    """
    
    def __init__(self, d_model: int, num_node_types: int = 4, 
                 vocab_size: int = 1000, confidence_threshold: float = 0.5):
        """
        Inicjalizuje Graph Mapper
        
        Args:
            d_model: Wymiar hidden states
            num_node_types: Liczba typów nodes
            vocab_size: Rozmiar predicate vocabulary
            confidence_threshold: Minimalny próg confidence
        """
        super(GraphMapper, self).__init__()
        
        self.d_model = d_model
        self.confidence_threshold = confidence_threshold
        
        # Core components
        self.node_classifier = NodeTypeClassifier(d_model, num_node_types)
        self.predicate_extractor = PredicateExtractor(d_model, vocab_size)
        
        # Confidence scorer
        self.confidence_scorer = nn.Sequential(
            nn.Linear(d_model, d_model // 4),
            nn.ReLU(),
            nn.Linear(d_model // 4, 1),
            nn.Sigmoid()
        )
        
        # Statistics
        self.total_nodes_generated = 0
        self.high_confidence_nodes = 0
        self.node_type_distribution = {
            'entity': 0, 'relation': 0, 'action': 0, 'property': 0
        }
        
        logger.info(f"🗺️ GraphMapper initialized: d_model={d_model}, threshold={confidence_threshold}")
    
    def forward(self, hidden_states: torch.Tensor, 
               attention_weights: Optional[torch.Tensor] = None) -> Dict[str, Any]:
        """
        Mapuje hidden states na symbolic nodes
        
        Args:
            hidden_states: Hidden states [batch_size, seq_len, d_model]
            attention_weights: Optional attention weights
            
        Returns:
            Dict[str, Any]: Mapped symbolic nodes i metadata
        """
        batch_size, seq_len, d_model = hidden_states.shape
        
        # 1. Classify node types
        node_classification = self.node_classifier(hidden_states)
        
        # 2. Extract predicates
        predicate_extraction = self.predicate_extractor(hidden_states, top_k=3)
        
        # 3. Score confidence
        confidence_scores = self.confidence_scorer(hidden_states).squeeze(-1)  # [batch_size, seq_len]
        
        # 4. Create symbolic nodes
        symbolic_nodes = self._create_symbolic_nodes(
            hidden_states,
            node_classification,
            predicate_extraction,
            confidence_scores
        )
        
        # Update statistics
        self._update_statistics(symbolic_nodes)
        
        return {
            'symbolic_nodes': symbolic_nodes,
            'node_classification': node_classification,
            'predicate_extraction': predicate_extraction,
            'confidence_scores': confidence_scores,
            'metadata': {
                'total_nodes': len(symbolic_nodes),
                'high_confidence_nodes': sum(1 for node in symbolic_nodes 
                                           if node.confidence >= self.confidence_threshold)
            }
        }
    
    def _create_symbolic_nodes(self, hidden_states: torch.Tensor,
                             node_classification: Dict[str, torch.Tensor],
                             predicate_extraction: Dict[str, torch.Tensor],
                             confidence_scores: torch.Tensor) -> List[SymbolicNode]:
        """
        Tworzy symbolic nodes z classification results
        
        Args:
            hidden_states: Original hidden states
            node_classification: Node type classification results
            predicate_extraction: Predicate extraction results
            confidence_scores: Confidence scores
            
        Returns:
            List[SymbolicNode]: Lista symbolic nodes
        """
        nodes = []
        batch_size, seq_len, d_model = hidden_states.shape
        
        # Get predicate names
        predicate_names = self.predicate_extractor.get_predicate_names(
            predicate_extraction['top_indices']
        )
        
        node_type_labels = self.node_classifier.node_type_labels
        
        for batch_idx in range(batch_size):
            for seq_idx in range(seq_len):
                # Get node type
                type_idx = node_classification['predicted_types'][batch_idx, seq_idx].item()
                node_type = node_type_labels[type_idx] if type_idx < len(node_type_labels) else 'unknown'
                
                # Get best predicate
                best_predicate = predicate_names[batch_idx][seq_idx][0]  # Top predicate
                
                # Get confidence
                confidence = confidence_scores[batch_idx, seq_idx].item()
                
                # Skip low confidence nodes
                if confidence < self.confidence_threshold:
                    continue
                
                # Create arguments based on node type
                if node_type == 'entity':
                    arguments = [f"entity_{batch_idx}_{seq_idx}"]
                elif node_type == 'relation':
                    arguments = [f"arg1_{batch_idx}_{seq_idx}", f"arg2_{batch_idx}_{seq_idx}"]
                else:
                    arguments = [f"arg_{batch_idx}_{seq_idx}"]
                
                # Create symbolic node
                node = SymbolicNode(
                    node_id=f"node_{batch_idx}_{seq_idx}",
                    node_type=node_type,
                    predicate=best_predicate,
                    arguments=arguments,
                    confidence=confidence,
                    embedding=hidden_states[batch_idx, seq_idx].clone().detach(),
                    source_position=seq_idx,
                    metadata={
                        'batch_idx': batch_idx,
                        'alternative_predicates': predicate_names[batch_idx][seq_idx][1:],
                        'type_probabilities': node_classification['probabilities'][batch_idx, seq_idx].tolist()
                    }
                )
                
                nodes.append(node)
        
        return nodes
    
    def nodes_to_atoms(self, nodes: List[SymbolicNode]) -> List:
        """
        Konwertuje symbolic nodes na ILP Atoms
        
        Args:
            nodes: Lista symbolic nodes
            
        Returns:
            List: Lista ILP Atoms (jeśli ILP available)
        """
        if not ILP_AVAILABLE:
            logger.warning("🚨 ILP not available - cannot convert to Atoms")
            return []
        
        atoms = []
        
        for node in nodes:
            try:
                atom = Atom(node.predicate, node.arguments)
                atoms.append(atom)
            except Exception as e:
                logger.warning(f"🚨 Failed to create Atom from node {node.node_id}: {e}")
        
        logger.info(f"🔄 Converted {len(atoms)} nodes to ILP Atoms")
        return atoms
    
    def filter_nodes_by_confidence(self, nodes: List[SymbolicNode], 
                                  min_confidence: float) -> List[SymbolicNode]:
        """
        Filtruje nodes według confidence threshold
        
        Args:
            nodes: Lista nodes do filtrowania
            min_confidence: Minimalny próg confidence
            
        Returns:
            List[SymbolicNode]: Filtered nodes
        """
        filtered = [node for node in nodes if node.confidence >= min_confidence]
        
        logger.debug(f"🔍 Filtered {len(filtered)}/{len(nodes)} nodes (confidence >= {min_confidence})")
        return filtered
    
    def cluster_nodes_by_similarity(self, nodes: List[SymbolicNode], 
                                   similarity_threshold: float = 0.8) -> Dict[int, List[SymbolicNode]]:
        """
        Klasteryzuje nodes według similarity embeddingów
        
        Args:
            nodes: Lista nodes do clustering
            similarity_threshold: Próg similarity
            
        Returns:
            Dict[int, List[SymbolicNode]]: Clusters nodes
        """
        if len(nodes) < 2:
            return {0: nodes}
        
        # Extract embeddings
        embeddings = torch.stack([node.embedding for node in nodes])
        
        # Compute similarity matrix
        embeddings_norm = F.normalize(embeddings, p=2, dim=1)
        similarity_matrix = torch.mm(embeddings_norm, embeddings_norm.t())
        
        # Simple clustering algorithm
        clusters = {}
        visited = set()
        cluster_id = 0
        
        for i in range(len(nodes)):
            if i in visited:
                continue
            
            # Start new cluster
            cluster = [nodes[i]]
            visited.add(i)
            
            # Find similar nodes
            for j in range(i + 1, len(nodes)):
                if j not in visited and similarity_matrix[i, j] >= similarity_threshold:
                    cluster.append(nodes[j])
                    visited.add(j)
            
            clusters[cluster_id] = cluster
            cluster_id += 1
        
        logger.info(f"🎯 Created {len(clusters)} clusters from {len(nodes)} nodes")
        return clusters
    
    def _update_statistics(self, nodes: List[SymbolicNode]):
        """Aktualizuje statystyki mapping"""
        self.total_nodes_generated += len(nodes)
        
        for node in nodes:
            if node.confidence >= self.confidence_threshold:
                self.high_confidence_nodes += 1
            
            if node.node_type in self.node_type_distribution:
                self.node_type_distribution[node.node_type] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Pobiera statystyki Graph Mapper
        
        Returns:
            Dict[str, Any]: Statystyki
        """
        total_classified = sum(self.node_type_distribution.values())
        
        return {
            'd_model': self.d_model,
            'confidence_threshold': self.confidence_threshold,
            'total_nodes_generated': self.total_nodes_generated,
            'high_confidence_nodes': self.high_confidence_nodes,
            'high_confidence_rate': self.high_confidence_nodes / max(1, self.total_nodes_generated),
            'node_type_distribution': self.node_type_distribution.copy(),
            'most_common_node_type': max(self.node_type_distribution, 
                                       key=self.node_type_distribution.get) if total_classified > 0 else 'none'
        }
    
    def __repr__(self) -> str:
        return f"GraphMapper(d_model={self.d_model}, nodes_generated={self.total_nodes_generated})"