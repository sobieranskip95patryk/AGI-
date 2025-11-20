#!/usr/bin/env python3
"""
🧠 VECTOR-RULE MAPPING - Bidirectional Neural-Symbolic Bridge

Bidirectional mapping między ILP rules/predicates a embedding vectors:
- Rule → Vector transformation
- Vector → Rule reconstruction  
- Semantic similarity scoring
- Batch processing capabilities
- Rule similarity clustering
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Any, Optional, Set
from collections import defaultdict
import pickle
import json

# Import components
from ILP.ilp_engine import Atom, Rule, Predicate

try:
    from EMBEDDING.embedding_engine import EmbeddingEngine, EmbeddingVector
    from EMBEDDING.semantic_similarity import SemanticSimilarity
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False

logger = logging.getLogger(__name__)

class VectorRuleMapping:
    """
    🔄 Bidirectional mapping między symbolicznymi regułami a wektorami
    
    Umożliwia konwersję w obu kierunkach:
    - Rule/Predicate → EmbeddingVector (neural encoding)
    - EmbeddingVector → Rule/Predicate (symbolic decoding)
    """
    
    def __init__(self, embedding_dim: int = 128):
        """
        Inicjalizuje Vector-Rule Mapping system
        
        Args:
            embedding_dim: Wymiar przestrzeni embeddingów
        """
        self.embedding_dim = embedding_dim
        
        # Core mapping dictionaries
        self.rule_to_vector: Dict[str, EmbeddingVector] = {}
        self.vector_to_rule: Dict[str, Rule] = {}
        self.predicate_to_vector: Dict[str, EmbeddingVector] = {}
        self.vector_to_predicate: Dict[str, Predicate] = {}
        
        # Similarity clusters
        self.rule_clusters: Dict[int, List[str]] = {}
        self.predicate_clusters: Dict[int, List[str]] = {}
        
        # Embedding components
        if EMBEDDING_AVAILABLE:
            self.embedding_engine = EmbeddingEngine(embedding_dim=embedding_dim)
            self.similarity_engine = SemanticSimilarity(default_metric='cosine')
        else:
            self.embedding_engine = None
            self.similarity_engine = None
            logger.warning("🚨 EMBEDDING module not available")
        
        # Statistics
        self.mappings_created = 0
        self.successful_reconstructions = 0
        self.failed_reconstructions = 0
        
        logger.info(f"🔄 VectorRuleMapping initialized: dim={embedding_dim}")
    
    def map_rule_to_vector(self, rule: Rule, confidence: float = 1.0) -> Optional[EmbeddingVector]:
        """
        Mapuje regułę logiczną na wektor embedding
        
        Args:
            rule: Reguła do zmapowania
            confidence: Poziom pewności (0.0-1.0)
            
        Returns:
            Optional[EmbeddingVector]: Wektor embedding lub None
        """
        if not self.embedding_engine:
            return None
        
        rule_key = str(rule)
        
        # Check if already mapped
        if rule_key in self.rule_to_vector:
            return self.rule_to_vector[rule_key]
        
        # Create embedding
        embedding = self.embedding_engine.create_embedding(rule, "rule", confidence)
        
        # Store bidirectional mapping
        self.rule_to_vector[rule_key] = embedding
        self.vector_to_rule[embedding.source_id] = rule
        
        self.mappings_created += 1
        
        logger.debug(f"🔄 Mapped rule to vector: {rule_key[:50]}...")
        return embedding
    
    def map_predicate_to_vector(self, predicate: Predicate, confidence: float = 1.0) -> Optional[EmbeddingVector]:
        """
        Mapuje predykat na wektor embedding
        
        Args:
            predicate: Predykat do zmapowania
            confidence: Poziom pewności
            
        Returns:
            Optional[EmbeddingVector]: Wektor embedding lub None
        """
        if not self.embedding_engine:
            return None
        
        pred_key = str(predicate)
        
        if pred_key in self.predicate_to_vector:
            return self.predicate_to_vector[pred_key]
        
        # Create atom representation for embedding
        atom = Atom(predicate.name, [f"X{i}" for i in range(predicate.arity)])
        embedding = self.embedding_engine.create_embedding(atom, "predicate", confidence)
        
        # Store bidirectional mapping
        self.predicate_to_vector[pred_key] = embedding
        self.vector_to_predicate[embedding.source_id] = predicate
        
        self.mappings_created += 1
        
        logger.debug(f"🔄 Mapped predicate to vector: {pred_key}")
        return embedding
    
    def reconstruct_rule_from_vector(self, vector: EmbeddingVector, 
                                   similarity_threshold: float = 0.8) -> Optional[Rule]:
        """
        Rekonstruuje regułę z wektora embedding
        
        Args:
            vector: Wektor embedding
            similarity_threshold: Próg podobieństwa dla rekonstrukcji
            
        Returns:
            Optional[Rule]: Zrekonstruowana reguła lub None
        """
        if not self.similarity_engine:
            self.failed_reconstructions += 1
            return None
        
        # Direct lookup first
        if vector.source_id in self.vector_to_rule:
            self.successful_reconstructions += 1
            return self.vector_to_rule[vector.source_id]
        
        # Find most similar existing rule
        best_rule = None
        best_similarity = 0.0
        
        for rule_embedding in self.rule_to_vector.values():
            similarity = self.similarity_engine.compute_similarity(
                vector.vector, rule_embedding.vector
            )
            
            if similarity > best_similarity and similarity >= similarity_threshold:
                best_similarity = similarity
                best_rule = self.vector_to_rule.get(rule_embedding.source_id)
        
        if best_rule:
            self.successful_reconstructions += 1
            logger.debug(f"🔄 Reconstructed rule with similarity {best_similarity:.3f}")
        else:
            self.failed_reconstructions += 1
            logger.debug("🚨 Failed to reconstruct rule - no similar rule found")
        
        return best_rule
    
    def reconstruct_predicate_from_vector(self, vector: EmbeddingVector,
                                        similarity_threshold: float = 0.8) -> Optional[Predicate]:
        """
        Rekonstruuje predykat z wektora embedding
        
        Args:
            vector: Wektor embedding
            similarity_threshold: Próg podobieństwa
            
        Returns:
            Optional[Predicate]: Zrekonstruowany predykat lub None
        """
        if not self.similarity_engine:
            return None
        
        # Direct lookup
        if vector.source_id in self.vector_to_predicate:
            return self.vector_to_predicate[vector.source_id]
        
        # Find most similar predicate
        best_predicate = None
        best_similarity = 0.0
        
        for pred_embedding in self.predicate_to_vector.values():
            similarity = self.similarity_engine.compute_similarity(
                vector.vector, pred_embedding.vector
            )
            
            if similarity > best_similarity and similarity >= similarity_threshold:
                best_similarity = similarity
                best_predicate = self.vector_to_predicate.get(pred_embedding.source_id)
        
        return best_predicate
    
    def batch_map_rules(self, rules: List[Rule], confidences: Optional[List[float]] = None) -> List[EmbeddingVector]:
        """
        Mapuje wiele reguł na wektory w trybie batch
        
        Args:
            rules: Lista reguł
            confidences: Opcjonalne confidence scores
            
        Returns:
            List[EmbeddingVector]: Lista wektorów embedding
        """
        if confidences is None:
            confidences = [1.0] * len(rules)
        
        embeddings = []
        
        for i, rule in enumerate(rules):
            confidence = confidences[i] if i < len(confidences) else 1.0
            embedding = self.map_rule_to_vector(rule, confidence)
            if embedding:
                embeddings.append(embedding)
        
        logger.info(f"🔄 Batch mapped {len(embeddings)} rules to vectors")
        return embeddings
    
    def compute_rule_similarity(self, rule1: Rule, rule2: Rule) -> float:
        """
        Oblicza podobieństwo między regułami używając embeddingów
        
        Args:
            rule1: Pierwsza reguła
            rule2: Druga reguła
            
        Returns:
            float: Similarity score (0.0-1.0)
        """
        if not self.similarity_engine:
            return 0.0
        
        # Get or create embeddings
        emb1 = self.map_rule_to_vector(rule1)
        emb2 = self.map_rule_to_vector(rule2)
        
        if not emb1 or not emb2:
            return 0.0
        
        return self.similarity_engine.compute_similarity(emb1.vector, emb2.vector)
    
    def cluster_rules_by_similarity(self, similarity_threshold: float = 0.7) -> Dict[int, List[str]]:
        """
        Klasteryzuje reguły na podstawie podobieństwa embeddingów
        
        Args:
            similarity_threshold: Próg podobieństwa dla klastrów
            
        Returns:
            Dict[int, List[str]]: Mapa cluster_id -> lista rule_keys
        """
        if not self.similarity_engine or len(self.rule_to_vector) < 2:
            return {}
        
        rule_keys = list(self.rule_to_vector.keys())
        rule_vectors = [self.rule_to_vector[key].vector for key in rule_keys]
        
        # Use similarity engine clustering
        clusters_indices = self.similarity_engine.cluster_by_similarity(
            rule_vectors, similarity_threshold
        )
        
        # Convert indices to rule keys
        clusters = {}
        for cluster_id, indices in enumerate(clusters_indices):
            clusters[cluster_id] = [rule_keys[i] for i in indices]
        
        self.rule_clusters = clusters
        
        logger.info(f"🎯 Created {len(clusters)} rule clusters")
        return clusters
    
    def find_similar_rules(self, query_rule: Rule, top_k: int = 5, 
                          min_similarity: float = 0.5) -> List[Tuple[Rule, float]]:
        """
        Znajduje reguły podobne do zapytania
        
        Args:
            query_rule: Reguła zapytania
            top_k: Liczba najlepszych wyników
            min_similarity: Minimalny próg podobieństwa
            
        Returns:
            List[Tuple[Rule, float]]: Lista (reguła, similarity_score)
        """
        query_embedding = self.map_rule_to_vector(query_rule)
        if not query_embedding or not self.similarity_engine:
            return []
        
        similarities = []
        
        for rule_key, rule_embedding in self.rule_to_vector.items():
            if rule_key == str(query_rule):
                continue  # Skip self
            
            similarity = self.similarity_engine.compute_similarity(
                query_embedding.vector, rule_embedding.vector
            )
            
            if similarity >= min_similarity:
                rule = self.vector_to_rule.get(rule_embedding.source_id)
                if rule:
                    similarities.append((rule, similarity))
        
        # Sort by similarity and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def get_rule_embedding_space_summary(self) -> Dict[str, Any]:
        """
        Podsumowanie przestrzeni embeddingów reguł
        
        Returns:
            Dict[str, Any]: Statystyki embedding space
        """
        if not self.rule_to_vector:
            return {'empty': True}
        
        # Collect all rule vectors
        vectors = [emb.vector for emb in self.rule_to_vector.values()]
        vector_matrix = np.vstack(vectors)
        
        # Calculate statistics
        mean_vector = np.mean(vector_matrix, axis=0)
        std_vector = np.std(vector_matrix, axis=0)
        
        # Pairwise similarities
        similarities = []
        if self.similarity_engine and len(vectors) > 1:
            similarity_matrix = self.similarity_engine.batch_similarity_matrix(vectors)
            # Get upper triangle (excluding diagonal)
            upper_indices = np.triu_indices_from(similarity_matrix, k=1)
            similarities = similarity_matrix[upper_indices].tolist()
        
        summary = {
            'total_rules': len(self.rule_to_vector),
            'embedding_dim': self.embedding_dim,
            'mean_vector_norm': float(np.linalg.norm(mean_vector)),
            'std_vector_norm': float(np.linalg.norm(std_vector)),
            'num_clusters': len(self.rule_clusters),
            'avg_pairwise_similarity': float(np.mean(similarities)) if similarities else 0.0,
            'similarity_std': float(np.std(similarities)) if similarities else 0.0,
            'min_similarity': float(np.min(similarities)) if similarities else 0.0,
            'max_similarity': float(np.max(similarities)) if similarities else 0.0
        }
        
        return summary
    
    def save_mappings(self, filepath: str) -> None:
        """
        Zapisuje mappings do pliku
        
        Args:
            filepath: Ścieżka do pliku
        """
        try:
            # Prepare data for serialization
            data = {
                'rule_to_vector': {k: v.__dict__ for k, v in self.rule_to_vector.items()},
                'vector_to_rule': {k: str(v) for k, v in self.vector_to_rule.items()},
                'predicate_to_vector': {k: v.__dict__ for k, v in self.predicate_to_vector.items()},
                'vector_to_predicate': {k: str(v) for k, v in self.vector_to_predicate.items()},
                'rule_clusters': self.rule_clusters,
                'stats': {
                    'mappings_created': self.mappings_created,
                    'successful_reconstructions': self.successful_reconstructions,
                    'failed_reconstructions': self.failed_reconstructions
                },
                'config': {
                    'embedding_dim': self.embedding_dim
                }
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"💾 Mappings saved to {filepath}")
            
        except Exception as e:
            logger.error(f"🚨 Failed to save mappings: {e}")
    
    def load_mappings(self, filepath: str) -> None:
        """
        Ładuje mappings z pliku
        
        Args:
            filepath: Ścieżka do pliku
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Restore basic mappings (simplified version)
            # Note: Full restoration would require proper object reconstruction
            self.rule_clusters = data.get('rule_clusters', {})
            
            # Restore statistics
            stats = data.get('stats', {})
            self.mappings_created = stats.get('mappings_created', 0)
            self.successful_reconstructions = stats.get('successful_reconstructions', 0)
            self.failed_reconstructions = stats.get('failed_reconstructions', 0)
            
            logger.info(f"💾 Mappings loaded from {filepath}")
            logger.warning("🚨 Note: Full object restoration not implemented - recreate embeddings")
            
        except Exception as e:
            logger.error(f"🚨 Failed to load mappings: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Pobiera statystyki mapping system
        
        Returns:
            Dict[str, Any]: Statystyki
        """
        reconstruction_rate = 0.0
        total_attempts = self.successful_reconstructions + self.failed_reconstructions
        if total_attempts > 0:
            reconstruction_rate = self.successful_reconstructions / total_attempts
        
        return {
            'embedding_available': EMBEDDING_AVAILABLE,
            'embedding_dim': self.embedding_dim,
            'mappings_created': self.mappings_created,
            'total_rules_mapped': len(self.rule_to_vector),
            'total_predicates_mapped': len(self.predicate_to_vector),
            'rule_clusters': len(self.rule_clusters),
            'successful_reconstructions': self.successful_reconstructions,
            'failed_reconstructions': self.failed_reconstructions,
            'reconstruction_success_rate': reconstruction_rate
        }
    
    def __repr__(self) -> str:
        return f"VectorRuleMapping(rules={len(self.rule_to_vector)}, predicates={len(self.predicate_to_vector)})"