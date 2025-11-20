#!/usr/bin/env python3
"""
🧠 ILP-EMBEDDING BRIDGE - Neural-Symbolic Integration API

Rozszerzenie ILP Engine o funkcjonalności embeddingów:
- learn_from_embeddings() API dla uczenia z wektorów
- Beam search w embedding space
- Confidence scoring z Bayesian integration
- Bidirectional mapping rules ↔ embeddings
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Any, Optional
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Import ILP components
from ILP.ilp_engine import Atom, Rule, ILPEngine
from ILP.hypothesis_generator import AdvancedHypothesisGenerator

# Import Embedding components (będzie dostępne po integracji)
try:
    from EMBEDDING.embedding_engine import EmbeddingEngine, EmbeddingVector
    from EMBEDDING.semantic_similarity import SemanticSimilarity
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False

logger = logging.getLogger(__name__)

class EmbeddingEnhancedILP:
    """
    🧠 ILP Engine rozszerzony o Neural-Symbolic Integration
    
    Łączy symboliczne uczenie reguł ILP z embedding space reasoning
    dla zaawansowanej Neural-Symbolic Fusion.
    """
    
    def __init__(self, embedding_dim: int = 128):
        """
        Inicjalizuje Enhanced ILP z embedding capabilities
        
        Args:
            embedding_dim: Wymiar przestrzeni embeddingów
        """
        self.embedding_dim = embedding_dim
        
        # Core ILP components
        self.ilp_engine = ILPEngine()
        self.hypothesis_generator = AdvancedHypothesisGenerator()
        
        # Embedding components (jeśli dostępne)
        if EMBEDDING_AVAILABLE:
            self.embedding_engine = EmbeddingEngine(embedding_dim=embedding_dim)
            self.similarity_engine = SemanticSimilarity(default_metric='cosine')
        else:
            self.embedding_engine = None
            self.similarity_engine = None
            logger.warning("🚨 EMBEDDING module not available - falling back to pure ILP")
        
        # Rule-embedding mappings
        self.rule_embeddings: Dict[str, EmbeddingVector] = {}
        self.embedding_rules: Dict[str, Rule] = {}
        
        # Learning statistics
        self.rules_learned_from_embeddings = 0
        self.embedding_confidence_scores: Dict[str, float] = {}
        
        logger.info(f"🧠 EmbeddingEnhancedILP initialized: dim={embedding_dim}")
    
    def add_background_knowledge(self, facts: List[Atom]) -> None:
        """
        Dodaje background knowledge i tworzy embeddingi
        
        Args:
            facts: Lista faktów jako background knowledge
        """
        # Add to standard ILP
        self.ilp_engine.add_background_knowledge(facts)
        
        # Create embeddings if available
        if self.embedding_engine:
            self._create_fact_embeddings(facts)
        
        logger.info(f"📚 Added {len(facts)} facts to background knowledge")
    
    def add_positive_examples(self, examples: List[Atom]) -> None:
        """
        Dodaje positive examples i tworzy embeddingi
        
        Args:
            examples: Lista positive examples
        """
        self.ilp_engine.add_positive_examples(examples)
        
        if self.embedding_engine:
            self._create_fact_embeddings(examples)
        
        logger.info(f"✅ Added {len(examples)} positive examples")
    
    def _create_fact_embeddings(self, facts: List[Atom]) -> None:
        """
        Tworzy embeddingi dla faktów
        
        Args:
            facts: Lista faktów do embedding
        """
        if not self.embedding_engine:
            return
        
        for fact in facts:
            embedding = self.embedding_engine.create_embedding(fact, "fact")
            # Store mapping for later use
            fact_key = str(fact)
            self.rule_embeddings[fact_key] = embedding
    
    def learn_from_embeddings(self, embedding_vectors: List[np.ndarray], 
                            labels: Optional[List[str]] = None,
                            min_confidence: float = 0.7) -> List[Rule]:
        """
        🧠 Główna funkcja uczenia reguł z embeddingów
        
        Args:
            embedding_vectors: Lista wektorów embedding
            labels: Opcjonalne labele dla wektorów
            min_confidence: Minimalny próg confidence
            
        Returns:
            List[Rule]: Lista nauczonych reguł
        """
        if not self.embedding_engine:
            logger.warning("🚨 Cannot learn from embeddings - EMBEDDING module not available")
            return []
        
        logger.info(f"🧠 Learning rules from {len(embedding_vectors)} embeddings...")
        
        # 1. Cluster embeddings to find patterns
        clusters = self._cluster_embeddings(embedding_vectors, labels)
        
        # 2. Generate rule hypotheses from clusters
        hypotheses = self._generate_hypotheses_from_clusters(clusters)
        
        # 3. Validate rules using embedding similarity
        validated_rules = self._validate_rules_with_embeddings(hypotheses, min_confidence)
        
        # 4. Add to ILP knowledge base
        for rule in validated_rules:
            self._add_rule_to_knowledge_base(rule)
        
        self.rules_learned_from_embeddings += len(validated_rules)
        
        logger.info(f"✅ Learned {len(validated_rules)} rules from embeddings")
        return validated_rules
    
    def _cluster_embeddings(self, vectors: List[np.ndarray], 
                           labels: Optional[List[str]] = None) -> Dict[int, List[int]]:
        """
        Klasteryzuje embeddingi dla znalezienia wzorców
        
        Args:
            vectors: Lista wektorów
            labels: Opcjonalne labele
            
        Returns:
            Dict[int, List[int]]: Mapa klaster_id -> lista indeksów
        """
        if len(vectors) < 2:
            return {0: list(range(len(vectors)))}
        
        # Stack vectors into matrix
        X = np.vstack(vectors)
        
        # Find optimal number of clusters using silhouette score
        best_n_clusters = 2
        best_score = -1
        
        for n_clusters in range(2, min(len(vectors), 10)):
            try:
                kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                cluster_labels = kmeans.fit_predict(X)
                score = silhouette_score(X, cluster_labels)
                
                if score > best_score:
                    best_score = score
                    best_n_clusters = n_clusters
            except:
                break
        
        # Final clustering
        kmeans = KMeans(n_clusters=best_n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(X)
        
        # Group indices by cluster
        clusters = {}
        for idx, cluster_id in enumerate(cluster_labels):
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(idx)
        
        logger.debug(f"🎯 Created {len(clusters)} clusters from {len(vectors)} vectors")
        return clusters
    
    def _generate_hypotheses_from_clusters(self, clusters: Dict[int, List[int]]) -> List[Rule]:
        """
        Generuje hipotezy reguł z klastrów
        
        Args:
            clusters: Mapa klaster_id -> lista indeksów
            
        Returns:
            List[Rule]: Lista hipotez reguł
        """
        hypotheses = []
        
        for cluster_id, indices in clusters.items():
            if len(indices) < 2:  # Skip clusters with single element
                continue
            
            # Generate generic rule for cluster
            # For now, create simple clustering-based rules
            cluster_predicate = f"cluster_{cluster_id}"
            
            for idx in indices:
                # Create rule: cluster_X(item_Y) :- similar_embedding(item_Y, cluster_X)
                head = Atom(cluster_predicate, [f"item_{idx}"])
                body = [Atom("similar_embedding", [f"item_{idx}", cluster_predicate])]
                
                rule = Rule(head, body)
                rule.confidence = len(indices) / sum(len(cluster) for cluster in clusters.values())
                
                hypotheses.append(rule)
        
        logger.debug(f"📊 Generated {len(hypotheses)} hypotheses from clusters")
        return hypotheses
    
    def _validate_rules_with_embeddings(self, hypotheses: List[Rule], 
                                      min_confidence: float) -> List[Rule]:
        """
        Waliduje reguły używając podobieństwa embeddingów
        
        Args:
            hypotheses: Lista hipotez reguł
            min_confidence: Minimalny próg confidence
            
        Returns:
            List[Rule]: Lista zwalidowanych reguł
        """
        validated = []
        
        for rule in hypotheses:
            # Create embedding for rule
            rule_embedding = self.embedding_engine.create_embedding(rule, "rule")
            
            # Calculate embedding-based confidence
            embedding_confidence = self._calculate_embedding_confidence(rule, rule_embedding)
            
            # Combine with rule confidence
            combined_confidence = (rule.confidence + embedding_confidence) / 2
            
            if combined_confidence >= min_confidence:
                rule.confidence = combined_confidence
                validated.append(rule)
                
                # Store rule-embedding mapping
                rule_key = str(rule)
                self.rule_embeddings[rule_key] = rule_embedding
                self.embedding_rules[rule_embedding.source_id] = rule
                self.embedding_confidence_scores[rule_key] = embedding_confidence
        
        logger.debug(f"✅ Validated {len(validated)}/{len(hypotheses)} rules")
        return validated
    
    def _calculate_embedding_confidence(self, rule: Rule, rule_embedding: EmbeddingVector) -> float:
        """
        Oblicza confidence reguły na podstawie embeddingów
        
        Args:
            rule: Reguła do oceny
            rule_embedding: Embedding reguły
            
        Returns:
            float: Confidence score (0.0-1.0)
        """
        if not self.similarity_engine or len(self.rule_embeddings) == 0:
            return 0.5  # Default neutral confidence
        
        # Find similar rules in embedding space
        similarities = []
        for existing_embedding in self.rule_embeddings.values():
            if existing_embedding.source_id != rule_embedding.source_id:
                similarity = self.similarity_engine.compute_similarity(
                    rule_embedding.vector, existing_embedding.vector
                )
                similarities.append(similarity)
        
        if not similarities:
            return 0.5
        
        # Confidence based on average similarity to existing rules
        avg_similarity = sum(similarities) / len(similarities)
        
        # Transform similarity to confidence (higher similarity = higher confidence)
        confidence = min(1.0, max(0.0, avg_similarity))
        
        return confidence
    
    def _add_rule_to_knowledge_base(self, rule: Rule) -> None:
        """
        Dodaje regułę do bazy wiedzy ILP
        
        Args:
            rule: Reguła do dodania
        """
        # Add rule atoms to background knowledge if needed
        all_atoms = [rule.head] + rule.body
        self.ilp_engine.add_background_knowledge(all_atoms)
        
        logger.debug(f"📚 Added rule to knowledge base: {rule}")
    
    def beam_search_embedding_space(self, query_embedding: EmbeddingVector, 
                                  beam_width: int = 5,
                                  max_expansions: int = 100) -> List[Tuple[Rule, float]]:
        """
        🔍 Beam search w embedding space dla generowania reguł
        
        Args:
            query_embedding: Embedding zapytania
            beam_width: Szerokość beam search
            max_expansions: Maksymalna liczba ekspansji
            
        Returns:
            List[Tuple[Rule, float]]: Lista (reguła, score)
        """
        if not self.similarity_engine:
            logger.warning("🚨 Cannot perform beam search - similarity engine not available")
            return []
        
        logger.info(f"🔍 Starting beam search: beam_width={beam_width}")
        
        # Start with most similar existing rules
        candidates = []
        
        for rule_key, rule_embedding in self.rule_embeddings.items():
            similarity = self.similarity_engine.compute_similarity(
                query_embedding.vector, rule_embedding.vector
            )
            
            if rule_key in self.embedding_rules:
                rule = self.embedding_rules[rule_embedding.source_id]
                candidates.append((rule, similarity))
        
        # Sort by similarity and keep top beam_width
        candidates.sort(key=lambda x: x[1], reverse=True)
        beam = candidates[:beam_width]
        
        # Expand beam (simplified version)
        for expansion in range(max_expansions):
            if not beam:
                break
            
            # Generate variations of best candidates
            new_candidates = []
            
            for rule, score in beam[:beam_width//2]:  # Expand top half
                variations = self._generate_rule_variations(rule)
                
                for variation in variations:
                    var_embedding = self.embedding_engine.create_embedding(variation, "rule")
                    var_similarity = self.similarity_engine.compute_similarity(
                        query_embedding.vector, var_embedding.vector
                    )
                    new_candidates.append((variation, var_similarity))
            
            # Merge and re-rank
            all_candidates = beam + new_candidates
            all_candidates.sort(key=lambda x: x[1], reverse=True)
            beam = all_candidates[:beam_width]
            
            if expansion % 10 == 0:
                logger.debug(f"🔍 Beam search expansion {expansion}: best_score={beam[0][1]:.3f}")
        
        logger.info(f"✅ Beam search completed: {len(beam)} candidates")
        return beam
    
    def _generate_rule_variations(self, rule: Rule) -> List[Rule]:
        """
        Generuje warianty reguły dla beam search
        
        Args:
            rule: Reguła bazowa
            
        Returns:
            List[Rule]: Lista wariantów
        """
        variations = []
        
        # Variation 1: Remove one body atom (if possible)
        if len(rule.body) > 1:
            for i in range(len(rule.body)):
                new_body = rule.body[:i] + rule.body[i+1:]
                variation = Rule(rule.head, new_body)
                variation.confidence = rule.confidence * 0.9  # Slightly lower confidence
                variations.append(variation)
        
        # Variation 2: Add generic body atom (simplified)
        generic_atoms = [
            Atom("related", ["X", "Y"]),
            Atom("similar", ["X", "Y"]),
            Atom("type", ["X", "generic"])
        ]
        
        for generic_atom in generic_atoms:
            new_body = rule.body + [generic_atom]
            variation = Rule(rule.head, new_body)
            variation.confidence = rule.confidence * 0.8  # Lower confidence for more complex rules
            variations.append(variation)
        
        return variations[:5]  # Limit variations
    
    def find_embedding_based_rules(self, target_predicate: str, 
                                 min_similarity: float = 0.8) -> List[Tuple[Rule, float]]:
        """
        Znajduje reguły na podstawie podobieństwa embeddingów do predykatu
        
        Args:
            target_predicate: Predykat docelowy
            min_similarity: Minimalny próg podobieństwa
            
        Returns:
            List[Tuple[Rule, float]]: Lista (reguła, similarity_score)
        """
        if not self.embedding_engine:
            return []
        
        # Create embedding for target predicate
        target_atom = Atom(target_predicate, ["X"])
        target_embedding = self.embedding_engine.create_embedding(target_atom, "predicate")
        
        # Find similar rules
        similar_rules = []
        
        for rule_key, rule_embedding in self.rule_embeddings.items():
            similarity = self.similarity_engine.compute_similarity(
                target_embedding.vector, rule_embedding.vector
            )
            
            if similarity >= min_similarity and rule_embedding.source_id in self.embedding_rules:
                rule = self.embedding_rules[rule_embedding.source_id]
                similar_rules.append((rule, similarity))
        
        # Sort by similarity
        similar_rules.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"🔍 Found {len(similar_rules)} similar rules for '{target_predicate}'")
        return similar_rules
    
    def get_embedding_stats(self) -> Dict[str, Any]:
        """
        Pobiera statystyki embeddings integration
        
        Returns:
            Dict[str, Any]: Statystyki
        """
        stats = {
            'embedding_available': EMBEDDING_AVAILABLE,
            'embedding_dim': self.embedding_dim,
            'rules_learned_from_embeddings': self.rules_learned_from_embeddings,
            'total_rule_embeddings': len(self.rule_embeddings),
            'avg_embedding_confidence': 0.0
        }
        
        if self.embedding_confidence_scores:
            stats['avg_embedding_confidence'] = sum(self.embedding_confidence_scores.values()) / len(self.embedding_confidence_scores)
        
        if self.embedding_engine:
            engine_stats = self.embedding_engine.get_stats()
            stats.update({
                'embedding_cache_size': engine_stats['cache_size'],
                'embedding_hit_rate': engine_stats['hit_rate'],
                'total_embeddings_created': engine_stats['total_embeddings_created']
            })
        
        return stats
    
    def __repr__(self) -> str:
        return f"EmbeddingEnhancedILP(dim={self.embedding_dim}, rules_learned={self.rules_learned_from_embeddings})"