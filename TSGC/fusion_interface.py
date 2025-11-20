#!/usr/bin/env python3
"""
🔄 TSGC FUSION INTERFACE - Integration z ILP Engine & NSI Layer

Fusion Interface dla Phase 3.2 TSGC:
- Real-time processing pipeline TSGC → ILP Engine
- Integration z Neural-Symbolic Integration Layer
- Batch optimization dla performance
- Error handling i monitoring
- Production-ready deployment interface

Pipeline: TSGC Output → Symbolic Graph → ILP Rules → NSI Layer → Reasoning Results
"""

import torch
import torch.nn as nn
import logging
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass, field
import time
from collections import defaultdict, deque
import json

# Import TSGC components
from .transformer_encoder import TransformerEncoder
from .graph_mapper import GraphMapper, SymbolicNode
from .edge_constructor import EdgeConstructor, SymbolicEdge

# Import Phase 2 i Phase 3.1 components dla integration
try:
    from ILP.ilp_engine import ILPEngine, Atom, Rule
    ILP_AVAILABLE = True
except ImportError:
    ILP_AVAILABLE = False

try:
    from ILP.embedding_bridge import EmbeddingEnhancedILP
    EMBEDDING_ILP_AVAILABLE = True
except ImportError:
    EMBEDDING_ILP_AVAILABLE = False

try:
    from EMBEDDING.embedding_engine import EmbeddingEngine
    from EMBEDDING.vector_rule_mapping import VectorRuleMapping
    NSI_AVAILABLE = True
except ImportError:
    NSI_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class TSGCProcessingResult:
    """
    Rezultat przetwarzania TSGC Pipeline
    """
    sequence_id: str
    input_sequence: List[str]
    symbolic_nodes: List[SymbolicNode]
    symbolic_edges: List[SymbolicEdge]
    ilp_atoms: List[Any]  # ILP Atoms
    ilp_rules: List[Any]  # ILP Rules
    embeddings: Optional[torch.Tensor] = None
    processing_time: float = 0.0
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TSGCConfig:
    """
    Konfiguracja TSGC Fusion Interface
    """
    # Model parameters
    d_model: int = 512
    confidence_threshold: float = 0.5
    batch_size: int = 32
    max_sequence_length: int = 256
    
    # Processing parameters
    enable_real_time: bool = True
    enable_batching: bool = True
    cache_embeddings: bool = True
    max_cache_size: int = 1000
    
    # Integration parameters
    integrate_ilp: bool = True
    integrate_nsi: bool = True
    enable_rule_learning: bool = True
    
    # Performance parameters
    processing_timeout: float = 30.0
    max_concurrent_requests: int = 10
    enable_monitoring: bool = True

class TSGCPerformanceMonitor:
    """
    Performance Monitoring dla TSGC Pipeline
    """
    
    def __init__(self, window_size: int = 100):
        """
        Inicjalizuje Performance Monitor
        
        Args:
            window_size: Rozmiar sliding window dla metrics
        """
        self.window_size = window_size
        
        # Performance metrics
        self.processing_times = deque(maxlen=window_size)
        self.success_count = 0
        self.error_count = 0
        self.total_requests = 0
        
        # Component metrics
        self.transformer_times = deque(maxlen=window_size)
        self.graph_mapper_times = deque(maxlen=window_size)
        self.edge_constructor_times = deque(maxlen=window_size)
        self.ilp_integration_times = deque(maxlen=window_size)
        
        # Memory usage
        self.peak_memory_usage = 0.0
        self.average_memory_usage = 0.0
        
        logger.info(f"📊 TSGCPerformanceMonitor initialized with window_size={window_size}")
    
    def record_processing_time(self, component: str, processing_time: float):
        """Record processing time dla specific component"""
        if component == 'transformer':
            self.transformer_times.append(processing_time)
        elif component == 'graph_mapper':
            self.graph_mapper_times.append(processing_time)
        elif component == 'edge_constructor':
            self.edge_constructor_times.append(processing_time)
        elif component == 'ilp_integration':
            self.ilp_integration_times.append(processing_time)
        elif component == 'total':
            self.processing_times.append(processing_time)
    
    def record_request(self, success: bool):
        """Record request outcome"""
        self.total_requests += 1
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Pobiera current performance metrics
        
        Returns:
            Dict[str, Any]: Performance metrics
        """
        def compute_stats(times_deque):
            if not times_deque:
                return {'mean': 0.0, 'min': 0.0, 'max': 0.0, 'count': 0}
            times_list = list(times_deque)
            return {
                'mean': sum(times_list) / len(times_list),
                'min': min(times_list),
                'max': max(times_list),
                'count': len(times_list)
            }
        
        return {
            'total_requests': self.total_requests,
            'success_rate': self.success_count / max(1, self.total_requests),
            'error_rate': self.error_count / max(1, self.total_requests),
            'processing_times': compute_stats(self.processing_times),
            'component_times': {
                'transformer': compute_stats(self.transformer_times),
                'graph_mapper': compute_stats(self.graph_mapper_times),
                'edge_constructor': compute_stats(self.edge_constructor_times),
                'ilp_integration': compute_stats(self.ilp_integration_times)
            },
            'memory_usage': {
                'peak': self.peak_memory_usage,
                'average': self.average_memory_usage
            }
        }

class TSGCFusionInterface(nn.Module):
    """
    Core TSGC Fusion Interface - Complete Neural-Symbolic Pipeline
    
    Główny interface łączący wszystkie komponenty TSGC
    z Phase 2 reasoning engines i Phase 3.1 NSI layer.
    """
    
    def __init__(self, config: TSGCConfig):
        """
        Inicjalizuje TSGC Fusion Interface
        
        Args:
            config: Konfiguracja interface
        """
        super(TSGCFusionInterface, self).__init__()
        
        self.config = config
        
        # Core TSGC components
        self.transformer_encoder = TransformerEncoder(
            d_model=config.d_model,
            num_heads=8,
            num_layers=6,
            max_length=config.max_sequence_length
        )
        self.graph_mapper = GraphMapper(
            d_model=config.d_model,
            confidence_threshold=config.confidence_threshold
        )
        self.edge_constructor = EdgeConstructor(
            d_model=config.d_model,
            confidence_threshold=config.confidence_threshold
        )
        
        # Phase 2 & 3.1 integration components
        self.ilp_engine = None
        self.embedding_enhanced_ilp = None
        self.embedding_engine = None
        self.vector_rule_mapping = None
        
        # Initialize integrations
        self._initialize_integrations()
        
        # Performance monitoring
        self.monitor = TSGCPerformanceMonitor() if config.enable_monitoring else None
        
        # Processing queue dla batch processing
        self.processing_queue = deque()
        self.result_cache = {}
        
        # Statistics
        self.total_sequences_processed = 0
        self.successful_integrations = 0
        self.failed_integrations = 0
        
        logger.info(f"🔄 TSGCFusionInterface initialized with config: {config}")
    
    def _initialize_integrations(self):
        """Inicjalizuje integration components"""
        try:
            if ILP_AVAILABLE and self.config.integrate_ilp:
                self.ilp_engine = ILPEngine()
                logger.info("✅ ILP Engine integration enabled")
            
            if EMBEDDING_ILP_AVAILABLE and self.config.integrate_ilp:
                self.embedding_enhanced_ilp = EmbeddingEnhancedILP()
                logger.info("✅ Embedding Enhanced ILP integration enabled")
            
            if NSI_AVAILABLE and self.config.integrate_nsi:
                self.embedding_engine = EmbeddingEngine()
                self.vector_rule_mapping = VectorRuleMapping()
                logger.info("✅ Neural-Symbolic Integration enabled")
                
        except Exception as e:
            logger.warning(f"🚨 Integration initialization partially failed: {e}")
    
    def process_sequence(self, sequence: Union[str, List[str]], 
                        sequence_id: Optional[str] = None) -> TSGCProcessingResult:
        """
        Przetwarza single sequence przez complete TSGC pipeline
        
        Args:
            sequence: Input sequence (string lub list of tokens)
            sequence_id: Optional sequence identifier
            
        Returns:
            TSGCProcessingResult: Complete processing results
        """
        start_time = time.time()
        
        if sequence_id is None:
            sequence_id = f"seq_{int(time.time() * 1000)}"
        
        # Check cache
        if self.config.cache_embeddings and sequence_id in self.result_cache:
            cached_result = self.result_cache[sequence_id]
            logger.debug(f"🎯 Using cached result dla sequence {sequence_id}")
            return cached_result
        
        try:
            # Convert sequence to proper format
            if isinstance(sequence, str):
                tokens = sequence.split()
            else:
                tokens = sequence
            
            # 1. Transformer Encoding
            transformer_start = time.time()
            transformer_output = self.transformer_encoder.encode_sequences([tokens])
            hidden_states = transformer_output['hidden_states'][0]  # First batch
            transformer_time = time.time() - transformer_start
            
            if self.monitor:
                self.monitor.record_processing_time('transformer', transformer_time)
            
            # 2. Graph Mapping
            graph_mapper_start = time.time()
            graph_output = self.graph_mapper(hidden_states.unsqueeze(0))  # Add batch dim
            symbolic_nodes = graph_output['symbolic_nodes']
            graph_mapper_time = time.time() - graph_mapper_start
            
            if self.monitor:
                self.monitor.record_processing_time('graph_mapper', graph_mapper_time)
            
            # 3. Edge Construction
            edge_constructor_start = time.time()
            edge_output = self.edge_constructor(symbolic_nodes)
            symbolic_edges = edge_output['edges']
            edge_constructor_time = time.time() - edge_constructor_start
            
            if self.monitor:
                self.monitor.record_processing_time('edge_constructor', edge_constructor_time)
            
            # 4. ILP Integration
            ilp_start = time.time()
            ilp_atoms, ilp_rules = self._integrate_with_ilp(symbolic_nodes, symbolic_edges)
            ilp_time = time.time() - ilp_start
            
            if self.monitor:
                self.monitor.record_processing_time('ilp_integration', ilp_time)
            
            # 5. NSI Integration
            embeddings = None
            if self.config.integrate_nsi:
                embeddings = self._integrate_with_nsi(symbolic_nodes, ilp_rules)
            
            # Create result
            total_time = time.time() - start_time
            result = TSGCProcessingResult(
                sequence_id=sequence_id,
                input_sequence=tokens,
                symbolic_nodes=symbolic_nodes,
                symbolic_edges=symbolic_edges,
                ilp_atoms=ilp_atoms,
                ilp_rules=ilp_rules,
                embeddings=embeddings,
                processing_time=total_time,
                confidence_scores={
                    'average_node_confidence': sum(node.confidence for node in symbolic_nodes) / max(1, len(symbolic_nodes)),
                    'average_edge_confidence': sum(edge.confidence for edge in symbolic_edges) / max(1, len(symbolic_edges))
                },
                metadata={
                    'transformer_time': transformer_time,
                    'graph_mapper_time': graph_mapper_time,
                    'edge_constructor_time': edge_constructor_time,
                    'ilp_integration_time': ilp_time,
                    'num_nodes': len(symbolic_nodes),
                    'num_edges': len(symbolic_edges),
                    'num_atoms': len(ilp_atoms),
                    'num_rules': len(ilp_rules)
                }
            )
            
            # Cache result
            if self.config.cache_embeddings:
                if len(self.result_cache) >= self.config.max_cache_size:
                    # Remove oldest entry
                    oldest_key = next(iter(self.result_cache))
                    del self.result_cache[oldest_key]
                self.result_cache[sequence_id] = result
            
            # Update statistics
            self.total_sequences_processed += 1
            self.successful_integrations += 1
            
            if self.monitor:
                self.monitor.record_processing_time('total', total_time)
                self.monitor.record_request(True)
            
            logger.debug(f"✅ Processed sequence {sequence_id} in {total_time:.3f}s")
            return result
            
        except Exception as e:
            self.failed_integrations += 1
            if self.monitor:
                self.monitor.record_request(False)
            
            logger.error(f"🚨 Failed to process sequence {sequence_id}: {e}")
            
            # Return empty result
            return TSGCProcessingResult(
                sequence_id=sequence_id,
                input_sequence=tokens if 'tokens' in locals() else [],
                symbolic_nodes=[],
                symbolic_edges=[],
                ilp_atoms=[],
                ilp_rules=[],
                processing_time=time.time() - start_time,
                metadata={'error': str(e)}
            )
    
    def process_batch(self, sequences: List[Union[str, List[str]]], 
                     sequence_ids: Optional[List[str]] = None) -> List[TSGCProcessingResult]:
        """
        Przetwarza batch sequences dla efficiency
        
        Args:
            sequences: Lista input sequences
            sequence_ids: Optional lista sequence identifiers
            
        Returns:
            List[TSGCProcessingResult]: Batch processing results
        """
        if not self.config.enable_batching:
            # Fallback to individual processing
            results = []
            for i, seq in enumerate(sequences):
                seq_id = sequence_ids[i] if sequence_ids else None
                result = self.process_sequence(seq, seq_id)
                results.append(result)
            return results
        
        start_time = time.time()
        results = []
        
        try:
            # Process sequences in batches
            batch_size = min(self.config.batch_size, len(sequences))
            
            for i in range(0, len(sequences), batch_size):
                batch_end = min(i + batch_size, len(sequences))
                batch_sequences = sequences[i:batch_end]
                batch_ids = sequence_ids[i:batch_end] if sequence_ids else None
                
                # Convert to tokens
                batch_tokens = []
                for seq in batch_sequences:
                    if isinstance(seq, str):
                        batch_tokens.append(seq.split())
                    else:
                        batch_tokens.append(seq)
                
                # Batch transformer encoding
                transformer_output = self.transformer_encoder.encode_sequences(batch_tokens)
                
                # Process each sequence in batch
                for j, hidden_states in enumerate(transformer_output['hidden_states']):
                    seq_idx = i + j
                    seq_id = batch_ids[j] if batch_ids else f"batch_seq_{seq_idx}"
                    
                    # Individual graph mapping i edge construction
                    graph_output = self.graph_mapper(hidden_states.unsqueeze(0))
                    symbolic_nodes = graph_output['symbolic_nodes']
                    
                    edge_output = self.edge_constructor(symbolic_nodes)
                    symbolic_edges = edge_output['edges']
                    
                    # ILP integration
                    ilp_atoms, ilp_rules = self._integrate_with_ilp(symbolic_nodes, symbolic_edges)
                    
                    # NSI integration
                    embeddings = None
                    if self.config.integrate_nsi:
                        embeddings = self._integrate_with_nsi(symbolic_nodes, ilp_rules)
                    
                    # Create result
                    result = TSGCProcessingResult(
                        sequence_id=seq_id,
                        input_sequence=batch_tokens[j],
                        symbolic_nodes=symbolic_nodes,
                        symbolic_edges=symbolic_edges,
                        ilp_atoms=ilp_atoms,
                        ilp_rules=ilp_rules,
                        embeddings=embeddings,
                        processing_time=time.time() - start_time,
                        confidence_scores={
                            'average_node_confidence': sum(node.confidence for node in symbolic_nodes) / max(1, len(symbolic_nodes)),
                            'average_edge_confidence': sum(edge.confidence for edge in symbolic_edges) / max(1, len(symbolic_edges))
                        },
                        metadata={
                            'batch_processed': True,
                            'batch_size': len(batch_sequences),
                            'num_nodes': len(symbolic_nodes),
                            'num_edges': len(symbolic_edges)
                        }
                    )
                    
                    results.append(result)
            
            total_time = time.time() - start_time
            logger.info(f"📦 Processed batch of {len(sequences)} sequences in {total_time:.3f}s")
            
        except Exception as e:
            logger.error(f"🚨 Batch processing failed: {e}")
            
            # Fallback to individual processing
            results = []
            for i, seq in enumerate(sequences):
                seq_id = sequence_ids[i] if sequence_ids else None
                result = self.process_sequence(seq, seq_id)
                results.append(result)
        
        return results
    
    def _integrate_with_ilp(self, nodes: List[SymbolicNode], 
                           edges: List[SymbolicEdge]) -> Tuple[List[Any], List[Any]]:
        """
        Integration z ILP Engine
        
        Args:
            nodes: Symbolic nodes
            edges: Symbolic edges
            
        Returns:
            Tuple[List[Any], List[Any]]: (atoms, rules)
        """
        atoms = []
        rules = []
        
        try:
            if self.ilp_engine and ILP_AVAILABLE:
                # Convert nodes to atoms
                for node in nodes:
                    atom = Atom(node.predicate, node.arguments)
                    atoms.append(atom)
                
                # Convert edges to rules (simplified)
                for edge in edges:
                    if edge.confidence >= self.config.confidence_threshold:
                        # Create rule: source_predicate(args) -> target_predicate(args)
                        head = Atom(edge.target_node.predicate, edge.target_node.arguments)
                        body = [Atom(edge.source_node.predicate, edge.source_node.arguments)]
                        rule = Rule(head, body)
                        rules.append(rule)
            
            # Enhanced ILP with embeddings
            if self.embedding_enhanced_ilp and EMBEDDING_ILP_AVAILABLE:
                # Use embedding-enhanced learning
                node_embeddings = torch.stack([node.embedding for node in nodes])
                enhanced_rules = self.embedding_enhanced_ilp.learn_from_embeddings(
                    node_embeddings, max_rules=10
                )
                rules.extend(enhanced_rules)
            
        except Exception as e:
            logger.warning(f"🚨 ILP integration failed: {e}")
        
        return atoms, rules
    
    def _integrate_with_nsi(self, nodes: List[SymbolicNode], 
                           rules: List[Any]) -> Optional[torch.Tensor]:
        """
        Integration z Neural-Symbolic Integration Layer
        
        Args:
            nodes: Symbolic nodes
            rules: ILP rules
            
        Returns:
            Optional[torch.Tensor]: Enhanced embeddings
        """
        try:
            if self.embedding_engine and self.vector_rule_mapping and NSI_AVAILABLE:
                # Extract node texts dla embedding
                node_texts = [f"{node.predicate}({', '.join(node.arguments)})" 
                             for node in nodes]
                
                # Generate embeddings
                embeddings = self.embedding_engine.vectorize_batch(node_texts)
                
                # Map rules to vectors
                rule_texts = [str(rule) for rule in rules[:10]]  # Limit to 10 rules
                if rule_texts:
                    rule_mappings = self.vector_rule_mapping.map_rules_to_vectors(rule_texts)
                    
                    # Combine node embeddings with rule vectors
                    if embeddings is not None and len(rule_mappings) > 0:
                        # Simple averaging (can be enhanced)
                        rule_vectors = torch.stack([torch.from_numpy(vec) for vec in rule_mappings.values()])
                        avg_rule_vector = torch.mean(rule_vectors, dim=0)
                        
                        # Enhance node embeddings
                        enhanced_embeddings = embeddings + 0.1 * avg_rule_vector.unsqueeze(0)
                        return enhanced_embeddings
                
                return embeddings
                
        except Exception as e:
            logger.warning(f"🚨 NSI integration failed: {e}")
        
        return None
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Pobiera performance metrics
        
        Returns:
            Dict[str, Any]: Performance metrics
        """
        base_metrics = {
            'total_sequences_processed': self.total_sequences_processed,
            'successful_integrations': self.successful_integrations,
            'failed_integrations': self.failed_integrations,
            'success_rate': self.successful_integrations / max(1, self.total_sequences_processed),
            'cache_size': len(self.result_cache),
            'config': {
                'd_model': self.config.d_model,
                'confidence_threshold': self.config.confidence_threshold,
                'batch_size': self.config.batch_size,
                'enable_real_time': self.config.enable_real_time,
                'integrate_ilp': self.config.integrate_ilp,
                'integrate_nsi': self.config.integrate_nsi
            }
        }
        
        if self.monitor:
            monitor_metrics = self.monitor.get_metrics()
            base_metrics.update(monitor_metrics)
        
        return base_metrics
    
    def clear_cache(self):
        """Clears result cache"""
        self.result_cache.clear()
        logger.info("🧹 TSGC result cache cleared")
    
    def export_results_to_json(self, results: List[TSGCProcessingResult], 
                              filepath: str):
        """
        Eksportuje results do JSON file
        
        Args:
            results: Lista results do export
            filepath: Output file path
        """
        try:
            export_data = []
            
            for result in results:
                # Convert tensors to lists dla JSON serialization
                result_dict = {
                    'sequence_id': result.sequence_id,
                    'input_sequence': result.input_sequence,
                    'symbolic_nodes': [
                        {
                            'node_id': node.node_id,
                            'node_type': node.node_type,
                            'predicate': node.predicate,
                            'arguments': node.arguments,
                            'confidence': node.confidence,
                            'source_position': node.source_position
                        } for node in result.symbolic_nodes
                    ],
                    'symbolic_edges': [
                        {
                            'edge_id': edge.edge_id,
                            'edge_type': edge.edge_type.value,
                            'confidence': edge.confidence,
                            'weight': edge.weight,
                            'source_node_id': edge.source_node.node_id,
                            'target_node_id': edge.target_node.node_id
                        } for edge in result.symbolic_edges
                    ],
                    'processing_time': result.processing_time,
                    'confidence_scores': result.confidence_scores,
                    'metadata': result.metadata
                }
                
                export_data.append(result_dict)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📁 Exported {len(results)} results to {filepath}")
            
        except Exception as e:
            logger.error(f"🚨 Export failed: {e}")
    
    def __repr__(self) -> str:
        return f"TSGCFusionInterface(processed={self.total_sequences_processed}, success_rate={self.successful_integrations/max(1, self.total_sequences_processed):.2f})"