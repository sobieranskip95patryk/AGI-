#!/usr/bin/env python3
"""
🧠 EMBEDDING ENGINE - Core Neural-Symbolic Integration

Główny silnik embeddingów dla MIGI 7G Neural-Symbolic Integration.
Tworzy wektorowe reprezentacje dla:
- Faktów logicznych (Atom objects)
- Reguł ILP (Rule objects) 
- Danych sensorycznych (Perception data)
- Predykatów i ich argumentów

Funkcjonalności:
- Embedding generation & caching
- Semantic similarity calculations
- Batch processing dla wydajności
- Integration z ILP Engine
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Any, Optional, Union
import hashlib
import json
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

logger = logging.getLogger(__name__)

@dataclass
class EmbeddingVector:
    """Reprezentacja wektora embedding z metadanymi"""
    vector: np.ndarray
    source_type: str  # 'fact', 'rule', 'predicate', 'sensor'
    source_id: str
    confidence: float = 1.0
    timestamp: float = 0.0
    metadata: Dict[str, Any] = None

class EmbeddingEngine:
    """
    🧠 Core Embedding Engine for Neural-Symbolic Integration
    
    Główny silnik do tworzenia i zarządzania embeddingami w systemie MIGI 7G.
    Łączy simboliczne reprezentacje z wektorowymi dla AGI reasoning.
    """
    
    def __init__(self, embedding_dim: int = 128, cache_size: int = 10000):
        """
        Inicjalizuje Embedding Engine
        
        Args:
            embedding_dim: Wymiar wektorów embedding (default: 128)
            cache_size: Maksymalny rozmiar cache (default: 10000)
        """
        self.embedding_dim = embedding_dim
        self.cache_size = cache_size
        
        # Core components
        self.vectorizer = TfidfVectorizer(max_features=embedding_dim, ngram_range=(1, 2))
        self.embeddings_cache: Dict[str, EmbeddingVector] = {}
        self.trained = False
        
        # Statistics
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_embeddings_created = 0
        
        logger.info(f"🧠 EmbeddingEngine initialized: dim={embedding_dim}, cache={cache_size}")
    
    def _create_text_representation(self, obj: Any) -> str:
        """
        Tworzy tekstową reprezentację objektu dla embeddingu
        
        Args:
            obj: Obiekt do konwersji (Atom, Rule, sensor data, etc.)
            
        Returns:
            str: Tekstowa reprezentacja
        """
        if hasattr(obj, 'predicate') and hasattr(obj, 'args'):
            # ILP Atom object
            args_str = ' '.join(str(arg) for arg in obj.args)
            return f"{obj.predicate} {args_str}"
            
        elif hasattr(obj, 'head') and hasattr(obj, 'body'):
            # ILP Rule object
            body_str = ' '.join(str(atom) for atom in obj.body)
            return f"{obj.head} :- {body_str}"
            
        elif isinstance(obj, dict):
            # Sensor data or generic dict
            items = []
            for key, value in obj.items():
                items.append(f"{key} {value}")
            return ' '.join(items)
            
        elif isinstance(obj, (list, tuple)):
            # List/tuple of objects
            return ' '.join(str(item) for item in obj)
            
        else:
            # Generic object
            return str(obj)
    
    def _get_cache_key(self, obj: Any, source_type: str) -> str:
        """
        Generuje klucz cache dla objektu
        
        Args:
            obj: Obiekt do hashowania
            source_type: Typ źródła ('fact', 'rule', 'predicate', 'sensor')
            
        Returns:
            str: Klucz cache
        """
        text_repr = self._create_text_representation(obj)
        content = f"{source_type}:{text_repr}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def train_vectorizer(self, corpus: List[str]) -> None:
        """
        Trenuje vectorizer na korpusie tekstów
        
        Args:
            corpus: Lista tekstów do treningu
        """
        if len(corpus) == 0:
            logger.warning("🚨 Empty corpus provided for training")
            return
            
        logger.info(f"🎯 Training vectorizer on {len(corpus)} documents...")
        self.vectorizer.fit(corpus)
        self.trained = True
        logger.info("✅ Vectorizer training completed")
    
    def create_embedding(self, obj: Any, source_type: str, 
                        confidence: float = 1.0) -> EmbeddingVector:
        """
        Tworzy embedding dla objektu
        
        Args:
            obj: Obiekt do embedding (Atom, Rule, sensor data, etc.)
            source_type: Typ źródła ('fact', 'rule', 'predicate', 'sensor')
            confidence: Poziom pewności (0.0-1.0)
            
        Returns:
            EmbeddingVector: Wygenerowany embedding
        """
        # Check cache first
        cache_key = self._get_cache_key(obj, source_type)
        
        if cache_key in self.embeddings_cache:
            self.cache_hits += 1
            return self.embeddings_cache[cache_key]
        
        self.cache_misses += 1
        
        # Create text representation
        text_repr = self._create_text_representation(obj)
        
        # Generate embedding vector
        if self.trained:
            # Use trained TF-IDF vectorizer
            tfidf_vector = self.vectorizer.transform([text_repr]).toarray()[0]
        else:
            # Fallback: simple hash-based embedding
            logger.warning("🚨 Vectorizer not trained, using hash-based embedding")
            hash_val = hash(text_repr)
            # Create pseudo-random vector based on hash
            np.random.seed(hash_val % (2**32))
            tfidf_vector = np.random.normal(0, 1, self.embedding_dim)
            tfidf_vector = tfidf_vector / np.linalg.norm(tfidf_vector)  # Normalize
        
        # Create EmbeddingVector object
        embedding = EmbeddingVector(
            vector=tfidf_vector,
            source_type=source_type,
            source_id=cache_key,
            confidence=confidence,
            timestamp=float(np.datetime64('now').astype('datetime64[s]').astype(int)),
            metadata={'text_repr': text_repr}
        )
        
        # Add to cache (with size limit)
        if len(self.embeddings_cache) >= self.cache_size:
            # Remove oldest embedding (simple FIFO)
            oldest_key = next(iter(self.embeddings_cache))
            del self.embeddings_cache[oldest_key]
            
        self.embeddings_cache[cache_key] = embedding
        self.total_embeddings_created += 1
        
        logger.debug(f"📊 Created embedding: {source_type} -> {text_repr[:50]}...")
        
        return embedding
    
    def batch_create_embeddings(self, objects: List[Tuple[Any, str, float]]) -> List[EmbeddingVector]:
        """
        Tworzy embeddingi w batch dla wydajności
        
        Args:
            objects: Lista tupli (obj, source_type, confidence)
            
        Returns:
            List[EmbeddingVector]: Lista wygenerowanych embeddingów
        """
        logger.info(f"🔄 Batch creating {len(objects)} embeddings...")
        
        embeddings = []
        for obj, source_type, confidence in objects:
            embedding = self.create_embedding(obj, source_type, confidence)
            embeddings.append(embedding)
        
        logger.info(f"✅ Batch created {len(embeddings)} embeddings")
        return embeddings
    
    def compute_similarity(self, embedding1: EmbeddingVector, 
                          embedding2: EmbeddingVector) -> float:
        """
        Oblicza podobieństwo cosine między dwoma embeddingami
        
        Args:
            embedding1: Pierwszy embedding
            embedding2: Drugi embedding
            
        Returns:
            float: Podobieństwo cosine (0.0-1.0)
        """
        similarity = cosine_similarity(
            embedding1.vector.reshape(1, -1),
            embedding2.vector.reshape(1, -1)
        )[0][0]
        
        return float(similarity)
    
    def find_similar_embeddings(self, query_embedding: EmbeddingVector, 
                               top_k: int = 5, 
                               min_similarity: float = 0.1) -> List[Tuple[EmbeddingVector, float]]:
        """
        Znajduje podobne embeddingi w cache
        
        Args:
            query_embedding: Embedding zapytania
            top_k: Liczba najlepszych wyników
            min_similarity: Minimalny próg podobieństwa
            
        Returns:
            List[Tuple[EmbeddingVector, float]]: Lista (embedding, similarity_score)
        """
        similarities = []
        
        for cached_embedding in self.embeddings_cache.values():
            if cached_embedding.source_id == query_embedding.source_id:
                continue  # Skip self
                
            similarity = self.compute_similarity(query_embedding, cached_embedding)
            
            if similarity >= min_similarity:
                similarities.append((cached_embedding, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def get_embeddings_by_type(self, source_type: str) -> List[EmbeddingVector]:
        """
        Pobiera wszystkie embeddingi określonego typu
        
        Args:
            source_type: Typ źródła ('fact', 'rule', 'predicate', 'sensor')
            
        Returns:
            List[EmbeddingVector]: Lista embeddingów danego typu
        """
        return [emb for emb in self.embeddings_cache.values() 
                if emb.source_type == source_type]
    
    def save_cache(self, filepath: str) -> None:
        """
        Zapisuje cache embeddingów do pliku
        
        Args:
            filepath: Ścieżka do pliku
        """
        try:
            cache_data = {
                'embeddings': self.embeddings_cache,
                'vectorizer': self.vectorizer,
                'trained': self.trained,
                'stats': {
                    'cache_hits': self.cache_hits,
                    'cache_misses': self.cache_misses,
                    'total_created': self.total_embeddings_created
                }
            }
            
            with open(filepath, 'wb') as f:
                pickle.dump(cache_data, f)
                
            logger.info(f"💾 Embedding cache saved to {filepath}")
            
        except Exception as e:
            logger.error(f"🚨 Failed to save cache: {e}")
    
    def load_cache(self, filepath: str) -> None:
        """
        Ładuje cache embeddingów z pliku
        
        Args:
            filepath: Ścieżka do pliku
        """
        try:
            if not os.path.exists(filepath):
                logger.warning(f"🚨 Cache file not found: {filepath}")
                return
                
            with open(filepath, 'rb') as f:
                cache_data = pickle.load(f)
            
            self.embeddings_cache = cache_data['embeddings']
            self.vectorizer = cache_data['vectorizer']
            self.trained = cache_data['trained']
            
            stats = cache_data.get('stats', {})
            self.cache_hits = stats.get('cache_hits', 0)
            self.cache_misses = stats.get('cache_misses', 0)
            self.total_embeddings_created = stats.get('total_created', 0)
            
            logger.info(f"💾 Embedding cache loaded from {filepath}")
            logger.info(f"📊 Loaded {len(self.embeddings_cache)} embeddings")
            
        except Exception as e:
            logger.error(f"🚨 Failed to load cache: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Pobiera statystyki działania silnika
        
        Returns:
            Dict[str, Any]: Statystyki
        """
        return {
            'cache_size': len(self.embeddings_cache),
            'max_cache_size': self.cache_size,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate': self.cache_hits / max(1, self.cache_hits + self.cache_misses),
            'total_embeddings_created': self.total_embeddings_created,
            'trained': self.trained,
            'embedding_dim': self.embedding_dim,
            'types_in_cache': list(set(emb.source_type for emb in self.embeddings_cache.values()))
        }
    
    def clear_cache(self) -> None:
        """Czyści cache embeddingów"""
        self.embeddings_cache.clear()
        logger.info("🗑️ Embedding cache cleared")
    
    def __repr__(self) -> str:
        return f"EmbeddingEngine(dim={self.embedding_dim}, cached={len(self.embeddings_cache)})"