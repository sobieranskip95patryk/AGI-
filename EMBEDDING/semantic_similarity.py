#!/usr/bin/env python3
"""
🧠 SEMANTIC SIMILARITY - Advanced Vector Comparisons

Zaawansowane obliczenia podobieństwa semantycznego dla embeddingów:
- Cosine similarity (podstawowe)
- Euclidean distance 
- Dot product similarity
- Weighted similarity z confidence scoring
- Batch similarity calculations
"""

import numpy as np
import logging
from typing import List, Tuple, Dict, Any
from scipy.spatial.distance import cosine, euclidean
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

logger = logging.getLogger(__name__)

class SemanticSimilarity:
    """
    🔍 Zaawansowane obliczenia podobieństwa semantycznego
    
    Implementuje różne metryki podobieństwa dla embeddingów
    z optymalizacją dla batch operations i confidence weighting.
    """
    
    def __init__(self, default_metric: str = 'cosine'):
        """
        Inicjalizuje SemanticSimilarity
        
        Args:
            default_metric: Domyślna metryka ('cosine', 'euclidean', 'dot')
        """
        self.default_metric = default_metric
        self.supported_metrics = ['cosine', 'euclidean', 'dot', 'weighted_cosine']
        
        # Statistics
        self.similarity_calls = 0
        self.batch_calls = 0
        
        if default_metric not in self.supported_metrics:
            logger.warning(f"🚨 Unknown metric '{default_metric}', using 'cosine'")
            self.default_metric = 'cosine'
        
        logger.info(f"🔍 SemanticSimilarity initialized: metric={self.default_metric}")
    
    def cosine_similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """
        Oblicza cosine similarity między dwoma wektorami
        
        Args:
            vector1: Pierwszy wektor
            vector2: Drugi wektor
            
        Returns:
            float: Cosine similarity (-1.0 do 1.0, wyższe = bardziej podobne)
        """
        # Handle zero vectors
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Cosine similarity = dot product / (norm1 * norm2)
        similarity = np.dot(vector1, vector2) / (norm1 * norm2)
        
        # Clamp to [-1, 1] range due to floating point precision
        return float(np.clip(similarity, -1.0, 1.0))
    
    def euclidean_similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """
        Oblicza similarity na bazie Euclidean distance
        
        Args:
            vector1: Pierwszy wektor
            vector2: Drugi wektor
            
        Returns:
            float: Similarity (0.0-1.0, wyższe = bardziej podobne)
        """
        distance = np.linalg.norm(vector1 - vector2)
        
        # Convert distance to similarity (0 distance = 1 similarity)
        # Using exponential decay: similarity = exp(-distance)
        similarity = np.exp(-distance)
        
        return float(similarity)
    
    def dot_product_similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """
        Oblicza normalized dot product similarity
        
        Args:
            vector1: Pierwszy wektor
            vector2: Drugi wektor
            
        Returns:
            float: Dot product similarity (normalized to 0.0-1.0)
        """
        dot_product = np.dot(vector1, vector2)
        
        # Normalize by vector magnitudes for fair comparison
        max_possible_dot = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        
        if max_possible_dot == 0:
            return 0.0
        
        # Normalize to [0, 1] range
        normalized_similarity = (dot_product + max_possible_dot) / (2 * max_possible_dot)
        
        return float(np.clip(normalized_similarity, 0.0, 1.0))
    
    def weighted_cosine_similarity(self, vector1: np.ndarray, vector2: np.ndarray,
                                  confidence1: float = 1.0, confidence2: float = 1.0) -> float:
        """
        Oblicza weighted cosine similarity z confidence scoring
        
        Args:
            vector1: Pierwszy wektor
            vector2: Drugi wektor  
            confidence1: Confidence pierwszego wektora (0.0-1.0)
            confidence2: Confidence drugiego wektora (0.0-1.0)
            
        Returns:
            float: Weighted similarity (0.0-1.0)
        """
        base_similarity = self.cosine_similarity(vector1, vector2)
        
        # Convert cosine similarity from [-1,1] to [0,1] range
        normalized_similarity = (base_similarity + 1) / 2
        
        # Weight by confidence scores
        confidence_weight = (confidence1 + confidence2) / 2
        weighted_similarity = normalized_similarity * confidence_weight
        
        return float(weighted_similarity)
    
    def compute_similarity(self, vector1: np.ndarray, vector2: np.ndarray,
                          metric: str = None, **kwargs) -> float:
        """
        Oblicza similarity używając wybranej metryki
        
        Args:
            vector1: Pierwszy wektor
            vector2: Drugi wektor
            metric: Metryka do użycia (None = default)
            **kwargs: Dodatkowe argumenty dla metryk
            
        Returns:
            float: Similarity score
        """
        if metric is None:
            metric = self.default_metric
        
        self.similarity_calls += 1
        
        if metric == 'cosine':
            return self.cosine_similarity(vector1, vector2)
        elif metric == 'euclidean':
            return self.euclidean_similarity(vector1, vector2)
        elif metric == 'dot':
            return self.dot_product_similarity(vector1, vector2)
        elif metric == 'weighted_cosine':
            confidence1 = kwargs.get('confidence1', 1.0)
            confidence2 = kwargs.get('confidence2', 1.0)
            return self.weighted_cosine_similarity(vector1, vector2, confidence1, confidence2)
        else:
            logger.warning(f"🚨 Unknown metric '{metric}', using cosine")
            return self.cosine_similarity(vector1, vector2)
    
    def batch_similarity_matrix(self, vectors: List[np.ndarray], 
                               metric: str = None) -> np.ndarray:
        """
        Oblicza macierz podobieństwa dla listy wektorów
        
        Args:
            vectors: Lista wektorów
            metric: Metryka do użycia
            
        Returns:
            np.ndarray: Macierz podobieństwa (n x n)
        """
        if metric is None:
            metric = self.default_metric
            
        self.batch_calls += 1
        n = len(vectors)
        
        if n == 0:
            return np.array([])
        
        # Stack vectors into matrix
        vector_matrix = np.vstack(vectors)
        
        if metric == 'cosine':
            # Use sklearn for efficient batch cosine similarity
            similarity_matrix = cosine_similarity(vector_matrix)
        elif metric == 'euclidean':
            # Convert euclidean distances to similarities
            distance_matrix = euclidean_distances(vector_matrix)
            similarity_matrix = np.exp(-distance_matrix)
        else:
            # Fallback: compute pairwise manually
            similarity_matrix = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    similarity_matrix[i, j] = self.compute_similarity(
                        vectors[i], vectors[j], metric
                    )
        
        logger.debug(f"📊 Computed {n}x{n} similarity matrix using {metric}")
        return similarity_matrix
    
    def find_most_similar(self, query_vector: np.ndarray, 
                         candidate_vectors: List[np.ndarray],
                         top_k: int = 5, metric: str = None,
                         min_similarity: float = 0.0) -> List[Tuple[int, float]]:
        """
        Znajduje najbardziej podobne wektory
        
        Args:
            query_vector: Wektor zapytania
            candidate_vectors: Lista kandydatów
            top_k: Liczba najlepszych wyników
            metric: Metryka podobieństwa
            min_similarity: Minimalny próg podobieństwa
            
        Returns:
            List[Tuple[int, float]]: Lista (index, similarity_score)
        """
        if len(candidate_vectors) == 0:
            return []
        
        similarities = []
        
        for i, candidate in enumerate(candidate_vectors):
            similarity = self.compute_similarity(query_vector, candidate, metric)
            
            if similarity >= min_similarity:
                similarities.append((i, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def cluster_by_similarity(self, vectors: List[np.ndarray], 
                             similarity_threshold: float = 0.8,
                             metric: str = None) -> List[List[int]]:
        """
        Grupuje wektory w klastry na podstawie podobieństwa
        
        Args:
            vectors: Lista wektorów
            similarity_threshold: Próg podobieństwa dla klastrów
            metric: Metryka podobieństwa
            
        Returns:
            List[List[int]]: Lista klastrów (każdy klaster to lista indeksów)
        """
        if len(vectors) == 0:
            return []
        
        # Compute similarity matrix
        similarity_matrix = self.batch_similarity_matrix(vectors, metric)
        
        # Simple clustering: group vectors above threshold
        n = len(vectors)
        visited = set()
        clusters = []
        
        for i in range(n):
            if i in visited:
                continue
                
            # Start new cluster
            cluster = [i]
            visited.add(i)
            
            # Find all similar vectors
            for j in range(i + 1, n):
                if j not in visited and similarity_matrix[i, j] >= similarity_threshold:
                    cluster.append(j)
                    visited.add(j)
            
            clusters.append(cluster)
        
        logger.info(f"🎯 Created {len(clusters)} clusters from {n} vectors")
        return clusters
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Pobiera statystyki działania
        
        Returns:
            Dict[str, Any]: Statystyki
        """
        return {
            'default_metric': self.default_metric,
            'supported_metrics': self.supported_metrics,
            'similarity_calls': self.similarity_calls,
            'batch_calls': self.batch_calls,
            'total_operations': self.similarity_calls + self.batch_calls
        }
    
    def __repr__(self) -> str:
        return f"SemanticSimilarity(metric={self.default_metric}, calls={self.similarity_calls})"