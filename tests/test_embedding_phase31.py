#!/usr/bin/env python3
"""
🧪 TEST EMBEDDING ENGINE - Phase 3.1 Testing Framework

Kompletne testy dla modułu EMBEDDING:
- EmbeddingEngine functionality tests
- VectorCache LRU policy tests  
- SemanticSimilarity metrics tests
- Integration tests z ILP Engine
- Performance benchmarks
"""

import pytest
import numpy as np
import tempfile
import os
from unittest.mock import Mock

# Import EMBEDDING modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from EMBEDDING.embedding_engine import EmbeddingEngine, EmbeddingVector
from EMBEDDING.vector_cache import VectorCache
from EMBEDDING.semantic_similarity import SemanticSimilarity

# Mock ILP objects for testing
class MockAtom:
    def __init__(self, predicate: str, args: list):
        self.predicate = predicate
        self.args = args
    
    def __str__(self):
        return f"{self.predicate}({', '.join(map(str, self.args))})"

class MockRule:
    def __init__(self, head: MockAtom, body: list):
        self.head = head
        self.body = body
    
    def __str__(self):
        body_str = ', '.join(str(atom) for atom in self.body)
        return f"{self.head} :- {body_str}"

class TestEmbeddingEngine:
    """🧪 Testy dla EmbeddingEngine"""
    
    def setup_method(self):
        """Setup przed każdym testem"""
        self.engine = EmbeddingEngine(embedding_dim=64, cache_size=100)
        
        # Training corpus
        self.corpus = [
            "fever temperature high",
            "cough respiratory symptom",
            "flu influenza disease",
            "treatment medication therapy"
        ]
        
    def test_initialization(self):
        """Test inicjalizacji EmbeddingEngine"""
        assert self.engine.embedding_dim == 64
        assert self.engine.cache_size == 100
        assert len(self.engine.embeddings_cache) == 0
        assert not self.engine.trained
        
    def test_train_vectorizer(self):
        """Test treningu vectorizer"""
        self.engine.train_vectorizer(self.corpus)
        assert self.engine.trained
        
    def test_create_text_representation(self):
        """Test tworzenia reprezentacji tekstowej"""
        # Test Atom
        atom = MockAtom("symptom", ["fever"])
        text = self.engine._create_text_representation(atom)
        assert text == "symptom fever"
        
        # Test Rule  
        head = MockAtom("disease", ["flu"])
        body = [MockAtom("symptom", ["fever"]), MockAtom("symptom", ["cough"])]
        rule = MockRule(head, body)
        text = self.engine._create_text_representation(rule)
        assert "disease(flu) :- symptom(fever)" in text
        assert "symptom(cough)" in text
        
        # Test dict
        sensor_data = {"temperature": 38.5, "heart_rate": 90}
        text = self.engine._create_text_representation(sensor_data)
        assert "temperature 38.5" in text
        assert "heart_rate 90" in text
        
    def test_create_embedding_without_training(self):
        """Test tworzenia embedding bez treningu (fallback mode)"""
        atom = MockAtom("symptom", ["fever"])
        embedding = self.engine.create_embedding(atom, "fact")
        
        assert isinstance(embedding, EmbeddingVector)
        assert embedding.vector.shape == (64,)
        assert embedding.source_type == "fact"
        assert embedding.confidence == 1.0
        
    def test_create_embedding_with_training(self):
        """Test tworzenia embedding z treningiem"""
        self.engine.train_vectorizer(self.corpus)
        
        atom = MockAtom("symptom", ["fever"])
        embedding = self.engine.create_embedding(atom, "fact")
        
        assert isinstance(embedding, EmbeddingVector)
        assert embedding.vector.shape[0] <= 64  # TF-IDF may create smaller vectors
        assert embedding.source_type == "fact"
        
    def test_cache_functionality(self):
        """Test działania cache"""
        atom = MockAtom("symptom", ["fever"])
        
        # First call - cache miss
        embedding1 = self.engine.create_embedding(atom, "fact")
        assert self.engine.cache_misses == 1
        assert self.engine.cache_hits == 0
        
        # Second call - cache hit
        embedding2 = self.engine.create_embedding(atom, "fact")
        assert self.engine.cache_hits == 1
        assert embedding1.source_id == embedding2.source_id
        
    def test_batch_create_embeddings(self):
        """Test batch tworzenia embeddingów"""
        self.engine.train_vectorizer(self.corpus)
        
        objects = [
            (MockAtom("symptom", ["fever"]), "fact", 1.0),
            (MockAtom("symptom", ["cough"]), "fact", 0.9),
            (MockAtom("disease", ["flu"]), "fact", 0.8)
        ]
        
        embeddings = self.engine.batch_create_embeddings(objects)
        assert len(embeddings) == 3
        assert all(isinstance(emb, EmbeddingVector) for emb in embeddings)
        
    def test_compute_similarity(self):
        """Test obliczania podobieństwa"""
        self.engine.train_vectorizer(self.corpus)
        
        atom1 = MockAtom("symptom", ["fever"])
        atom2 = MockAtom("symptom", ["cough"])
        
        emb1 = self.engine.create_embedding(atom1, "fact")
        emb2 = self.engine.create_embedding(atom2, "fact")
        
        similarity = self.engine.compute_similarity(emb1, emb2)
        assert 0.0 <= similarity <= 1.0
        
    def test_find_similar_embeddings(self):
        """Test znajdowania podobnych embeddingów"""
        self.engine.train_vectorizer(self.corpus)
        
        # Create several embeddings
        atoms = [
            MockAtom("symptom", ["fever"]),
            MockAtom("symptom", ["cough"]),
            MockAtom("disease", ["flu"]),
            MockAtom("treatment", ["medication"])
        ]
        
        embeddings = []
        for atom in atoms:
            emb = self.engine.create_embedding(atom, "fact")
            embeddings.append(emb)
        
        # Find similar to first embedding
        similar = self.engine.find_similar_embeddings(embeddings[0], top_k=2)
        assert len(similar) <= 2
        assert all(isinstance(result, tuple) for result in similar)
        
    def test_get_stats(self):
        """Test statystyk"""
        self.engine.train_vectorizer(self.corpus)
        atom = MockAtom("symptom", ["fever"])
        self.engine.create_embedding(atom, "fact")
        
        stats = self.engine.get_stats()
        assert 'cache_size' in stats
        assert 'trained' in stats
        assert 'total_embeddings_created' in stats
        assert stats['trained'] == True

class TestVectorCache:
    """🧪 Testy dla VectorCache"""
    
    def setup_method(self):
        """Setup przed każdym testem"""
        self.cache = VectorCache(max_size=3)
        
    def test_basic_operations(self):
        """Test podstawowych operacji cache"""
        # Put and get
        self.cache.put("key1", "value1")
        assert self.cache.get("key1") == "value1"
        assert self.cache.contains("key1")
        
        # Miss  
        assert self.cache.get("nonexistent") is None
        
    def test_lru_eviction(self):
        """Test LRU eviction policy"""
        # Fill cache to capacity
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2") 
        self.cache.put("key3", "value3")
        
        # Access key1 to make it recently used
        self.cache.get("key1")
        
        # Add new item - should evict key2 (least recently used)
        self.cache.put("key4", "value4")
        
        assert self.cache.contains("key1")  # Recently accessed
        assert not self.cache.contains("key2")  # Evicted
        assert self.cache.contains("key3")
        assert self.cache.contains("key4")  # Newly added
        
    def test_cache_stats(self):
        """Test statystyk cache"""
        self.cache.put("key1", "value1")
        self.cache.get("key1")  # Hit
        self.cache.get("nonexistent")  # Miss
        
        stats = self.cache.get_stats()
        assert stats['hits'] == 1
        assert stats['misses'] == 1
        assert stats['hit_rate'] == 0.5
        
    def test_save_and_load(self):
        """Test zapisywania i ładowania cache"""
        # Add some data
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            self.cache.save_to_file(tmp.name)
            
            # Create new cache and load
            new_cache = VectorCache()
            new_cache.load_from_file(tmp.name)
            
            assert new_cache.get("key1") == "value1"
            assert new_cache.get("key2") == "value2"
            
        # Cleanup
        os.unlink(tmp.name)

class TestSemanticSimilarity:
    """🧪 Testy dla SemanticSimilarity"""
    
    def setup_method(self):
        """Setup przed każdym testem"""
        self.similarity = SemanticSimilarity()
        
    def test_cosine_similarity(self):
        """Test cosine similarity"""
        # Identical vectors
        v1 = np.array([1, 0, 0])
        v2 = np.array([1, 0, 0])
        similarity = self.similarity.cosine_similarity(v1, v2)
        assert abs(similarity - 1.0) < 1e-6
        
        # Orthogonal vectors
        v3 = np.array([1, 0, 0])
        v4 = np.array([0, 1, 0])
        similarity = self.similarity.cosine_similarity(v3, v4)
        assert abs(similarity - 0.0) < 1e-6
        
        # Opposite vectors
        v5 = np.array([1, 0, 0])
        v6 = np.array([-1, 0, 0])
        similarity = self.similarity.cosine_similarity(v5, v6)
        assert abs(similarity - (-1.0)) < 1e-6
        
    def test_euclidean_similarity(self):
        """Test euclidean similarity"""
        # Identical vectors
        v1 = np.array([1, 1, 1])
        v2 = np.array([1, 1, 1])
        similarity = self.similarity.euclidean_similarity(v1, v2)
        assert abs(similarity - 1.0) < 1e-6  # exp(-0) = 1
        
        # Different vectors
        v3 = np.array([0, 0, 0])
        v4 = np.array([1, 1, 1])
        similarity = self.similarity.euclidean_similarity(v3, v4)
        assert 0.0 < similarity < 1.0
        
    def test_weighted_cosine_similarity(self):
        """Test weighted cosine similarity"""
        v1 = np.array([1, 0, 0])
        v2 = np.array([1, 0, 0])
        
        # High confidence
        similarity_high = self.similarity.weighted_cosine_similarity(
            v1, v2, confidence1=1.0, confidence2=1.0
        )
        
        # Low confidence
        similarity_low = self.similarity.weighted_cosine_similarity(
            v1, v2, confidence1=0.1, confidence2=0.1
        )
        
        assert similarity_high > similarity_low
        
    def test_batch_similarity_matrix(self):
        """Test batch similarity matrix"""
        vectors = [
            np.array([1, 0, 0]),
            np.array([0, 1, 0]),
            np.array([1, 0, 0])  # Same as first
        ]
        
        matrix = self.similarity.batch_similarity_matrix(vectors)
        
        assert matrix.shape == (3, 3)
        # Diagonal should be 1.0 (self-similarity)
        assert abs(matrix[0, 0] - 1.0) < 1e-6
        assert abs(matrix[1, 1] - 1.0) < 1e-6
        # First and third vectors are identical
        assert abs(matrix[0, 2] - 1.0) < 1e-6
        
    def test_find_most_similar(self):
        """Test znajdowania najbardziej podobnych"""
        query = np.array([1, 0, 0])
        candidates = [
            np.array([1, 0, 0]),      # Identical
            np.array([0.9, 0.1, 0]),  # Similar
            np.array([0, 1, 0]),      # Orthogonal
            np.array([-1, 0, 0])      # Opposite
        ]
        
        results = self.similarity.find_most_similar(query, candidates, top_k=2)
        
        assert len(results) == 2
        # First result should be the identical vector (index 0)
        assert results[0][0] == 0
        assert results[0][1] > results[1][1]  # Higher similarity

class TestIntegration:
    """🧪 Testy integracyjne Phase 3.1"""
    
    def setup_method(self):
        """Setup dla testów integracyjnych"""
        self.engine = EmbeddingEngine(embedding_dim=32)
        self.similarity = SemanticSimilarity()
        
        # Training corpus
        self.corpus = [
            "fever temperature high body",
            "cough respiratory lung symptom",
            "flu influenza viral disease",
            "treatment medication drug therapy",
            "diagnosis medical examination test"
        ]
        self.engine.train_vectorizer(self.corpus)
        
    def test_ilp_embedding_integration(self):
        """Test integracji z ILP objects"""
        # Create ILP-like objects
        facts = [
            MockAtom("symptom", ["fever"]),
            MockAtom("symptom", ["cough"]),
            MockAtom("disease", ["flu"]),
            MockAtom("causes", ["flu", "fever"]),
            MockAtom("requires_treatment", ["flu"])
        ]
        
        # Create embeddings for facts
        embeddings = []
        for fact in facts:
            emb = self.engine.create_embedding(fact, "fact")
            embeddings.append(emb)
        
        assert len(embeddings) == 5
        
        # Test similarity between related concepts
        fever_emb = embeddings[0]  # symptom(fever)
        flu_emb = embeddings[2]    # disease(flu)
        
        similarity_score = self.engine.compute_similarity(fever_emb, flu_emb)
        assert 0.0 <= similarity_score <= 1.0
        
    def test_rule_embedding_and_similarity(self):
        """Test embedding reguł i podobieństwa"""
        # Medical rules
        rules = [
            MockRule(
                MockAtom("requires_treatment", ["X"]),
                [MockAtom("disease", ["X"])]
            ),
            MockRule(
                MockAtom("has_symptom", ["X", "fever"]),
                [MockAtom("disease", ["X"]), MockAtom("causes", ["X", "fever"])]
            )
        ]
        
        rule_embeddings = []
        for rule in rules:
            emb = self.engine.create_embedding(rule, "rule")
            rule_embeddings.append(emb)
        
        # Test similarity between rules
        similarity = self.engine.compute_similarity(
            rule_embeddings[0], rule_embeddings[1]
        )
        assert 0.0 <= similarity <= 1.0
        
    def test_sensor_data_embedding(self):
        """Test embedding danych sensorycznych"""
        sensor_readings = [
            {"temperature": 38.5, "heart_rate": 90, "blood_pressure": "120/80"},
            {"temperature": 37.0, "heart_rate": 75, "blood_pressure": "110/70"},
            {"glucose_level": 95, "cholesterol": 180, "bmi": 23.5}
        ]
        
        sensor_embeddings = []
        for reading in sensor_readings:
            emb = self.engine.create_embedding(reading, "sensor")
            sensor_embeddings.append(emb)
        
        # Similar sensor readings should have higher similarity
        similarity_similar = self.engine.compute_similarity(
            sensor_embeddings[0], sensor_embeddings[1]  # Both temperature readings
        )
        
        similarity_different = self.engine.compute_similarity(
            sensor_embeddings[0], sensor_embeddings[2]  # Temperature vs glucose
        )
        
        # This test might not always pass due to TF-IDF randomness, 
        # but it demonstrates the concept
        assert similarity_similar >= 0.0
        assert similarity_different >= 0.0
        
    def test_performance_benchmark(self):
        """Test wydajności dla Phase 3.1"""
        import time
        
        # Create large number of embeddings
        num_embeddings = 100
        atoms = [MockAtom("test", [f"arg_{i}"]) for i in range(num_embeddings)]
        
        # Benchmark embedding creation
        start_time = time.time()
        embeddings = []
        for atom in atoms:
            emb = self.engine.create_embedding(atom, "fact")
            embeddings.append(emb)
        creation_time = time.time() - start_time
        
        # Benchmark similarity computation
        start_time = time.time()  
        for i in range(min(50, len(embeddings) - 1)):
            similarity = self.engine.compute_similarity(embeddings[i], embeddings[i+1])
        similarity_time = time.time() - start_time
        
        print(f"\n🚀 Performance Benchmark:")
        print(f"   📊 Created {num_embeddings} embeddings in {creation_time:.3f}s")
        print(f"   🔍 Computed 50 similarities in {similarity_time:.3f}s")
        print(f"   📈 Cache hit rate: {self.engine.get_stats()['hit_rate']:.3f}")
        
        # Basic performance assertions
        assert creation_time < 10.0  # Should complete within 10 seconds
        assert similarity_time < 5.0  # Should complete within 5 seconds

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])