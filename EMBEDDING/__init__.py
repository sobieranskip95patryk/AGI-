"""
🧠 EMBEDDING ENGINE - Neural-Symbolic Integration Phase 3.1

Moduł Embedding Engine dla systemu MIGI 7G:
- Wektorowe reprezentacje faktów, predykatów i danych sensorycznych
- Bridge między simbolicznymi regułami ILP a przestrzenią embeddingów
- Semantyczne podobieństwo i operacje na wektorach

Eksportowane klasy:
- EmbeddingEngine: Core engine dla operacji embedding
- VectorCache: Cache system dla embeddingów
- SemanticSimilarity: Obliczanie podobieństwa semantycznego
"""

from .embedding_engine import EmbeddingEngine
from .vector_cache import VectorCache  
from .semantic_similarity import SemanticSimilarity
from .vector_rule_mapping import VectorRuleMapping

__all__ = ['EmbeddingEngine', 'VectorCache', 'SemanticSimilarity', 'VectorRuleMapping']
__version__ = '1.0.0'