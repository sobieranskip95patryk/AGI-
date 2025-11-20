"""
🧠 TSGC - Transformer → Symbolic Graph Converter

Phase 3.2 Neural-Symbolic Integration:
- Transformer Encoder dla sequence → hidden states
- Graph Mapping Layer hidden states → symbolic nodes  
- Edge Constructor dla temporal & causal relations
- Fusion Interface z ILP Engine i NSI Layer

Eksportowane klasy:
- TransformerEncoder: Core transformer dla sequence processing
- GraphMapper: Konwersja hidden states → symbolic nodes
- EdgeConstructor: Tworzenie relacji temporal/causal
- TSGCFusionInterface: Interface z NSI Layer
"""

from .transformer_encoder import (
    TransformerEncoder,
    MultiHeadAttention, 
    PositionalEncoding,
    FeedForward,
    TransformerEncoderLayer
)
from .graph_mapper import (
    GraphMapper,
    NodeTypeClassifier,
    PredicateExtractor,
    SymbolicNode
)
from .edge_constructor import (
    EdgeConstructor,
    TemporalRelationDetector,
    CausalRelationDetector,
    SymbolicEdge,
    EdgeType
)
from .fusion_interface import (
    TSGCFusionInterface,
    TSGCConfig,
    TSGCProcessingResult,
    TSGCPerformanceMonitor
)

__all__ = [
    'TransformerEncoder',
    'MultiHeadAttention', 
    'PositionalEncoding',
    'FeedForward',
    'TransformerEncoderLayer',
    'GraphMapper',
    'NodeTypeClassifier', 
    'PredicateExtractor',
    'SymbolicNode',
    'EdgeConstructor',
    'TemporalRelationDetector',
    'CausalRelationDetector',
    'SymbolicEdge',
    'EdgeType',
    'TSGCFusionInterface',
    'TSGCConfig',
    'TSGCProcessingResult',
    'TSGCPerformanceMonitor'
]
__version__ = '1.0.0'