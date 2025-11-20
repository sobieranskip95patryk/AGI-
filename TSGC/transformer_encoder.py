#!/usr/bin/env python3
"""
🧠 TRANSFORMER ENCODER - Core Sequence Processing

Transformer Encoder dla Phase 3.2 TSGC:
- Multi-head self-attention mechanism
- Positional encoding dla sequence order
- Feed-forward layers z residual connections
- Batch processing i real-time inference
- PyTorch backend z ONNX export capability

Konwersja: Input sequences → Hidden states → Symbolic reasoning
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import logging
from typing import Dict, List, Tuple, Any, Optional
import math

logger = logging.getLogger(__name__)

class PositionalEncoding(nn.Module):
    """
    🎯 Positional Encoding dla Transformer
    
    Dodaje informację o pozycji w sekwencji używając
    sin/cos functions o różnych częstotliwościach.
    """
    
    def __init__(self, d_model: int, max_len: int = 5000):
        """
        Inicjalizuje Positional Encoding
        
        Args:
            d_model: Wymiar modelu (embedding size)
            max_len: Maksymalna długość sekwencji
        """
        super(PositionalEncoding, self).__init__()
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                           (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        
        self.register_buffer('pe', pe)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Dodaje positional encoding do input embeddings
        
        Args:
            x: Input tensor [seq_len, batch_size, d_model]
            
        Returns:
            torch.Tensor: Tensor z positional encoding
        """
        return x + self.pe[:x.size(0), :]

class MultiHeadAttention(nn.Module):
    """
    🔍 Multi-Head Self-Attention Mechanism
    
    Implementuje scaled dot-product attention z multiple heads
    dla parallel attention computation.
    """
    
    def __init__(self, d_model: int, num_heads: int = 8, dropout: float = 0.1):
        """
        Inicjalizuje Multi-Head Attention
        
        Args:
            d_model: Wymiar modelu
            num_heads: Liczba attention heads
            dropout: Dropout rate
        """
        super(MultiHeadAttention, self).__init__()
        
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.w_o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
        
    def scaled_dot_product_attention(self, Q: torch.Tensor, K: torch.Tensor, 
                                   V: torch.Tensor, mask: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Oblicza scaled dot-product attention
        
        Args:
            Q: Query tensor
            K: Key tensor  
            V: Value tensor
            mask: Optional attention mask
            
        Returns:
            Tuple[torch.Tensor, torch.Tensor]: Output i attention weights
        """
        d_k = Q.size(-1)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        
        output = torch.matmul(attention_weights, V)
        return output, attention_weights
    
    def forward(self, query: torch.Tensor, key: torch.Tensor, 
               value: torch.Tensor, mask: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass przez Multi-Head Attention
        
        Args:
            query: Query tensor [batch_size, seq_len, d_model]
            key: Key tensor
            value: Value tensor
            mask: Optional attention mask
            
        Returns:
            Tuple[torch.Tensor, torch.Tensor]: Output i attention weights
        """
        batch_size = query.size(0)
        
        # Linear transformations and reshape
        Q = self.w_q(query).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.w_k(key).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.w_v(value).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # Apply attention
        attention_output, attention_weights = self.scaled_dot_product_attention(Q, K, V, mask)
        
        # Concatenate heads
        attention_output = attention_output.transpose(1, 2).contiguous().view(
            batch_size, -1, self.d_model
        )
        
        # Final linear transformation
        output = self.w_o(attention_output)
        
        return output, attention_weights

class FeedForward(nn.Module):
    """
    🍞 Feed-Forward Network
    
    Position-wise feed-forward network z ReLU activation
    i residual connections.
    """
    
    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        """
        Inicjalizuje Feed-Forward Network
        
        Args:
            d_model: Wymiar modelu
            d_ff: Wymiar hidden layer
            dropout: Dropout rate
        """
        super(FeedForward, self).__init__()
        
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass przez feed-forward network
        
        Args:
            x: Input tensor
            
        Returns:
            torch.Tensor: Output tensor
        """
        return self.linear2(self.dropout(F.relu(self.linear1(x))))

class TransformerEncoderLayer(nn.Module):
    """
    🏗️ Single Transformer Encoder Layer
    
    Składa się z multi-head attention i feed-forward network
    z residual connections i layer normalization.
    """
    
    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float = 0.1):
        """
        Inicjalizuje Transformer Encoder Layer
        
        Args:
            d_model: Wymiar modelu
            num_heads: Liczba attention heads
            d_ff: Wymiar feed-forward network
            dropout: Dropout rate
        """
        super(TransformerEncoderLayer, self).__init__()
        
        self.multi_head_attention = MultiHeadAttention(d_model, num_heads, dropout)
        self.feed_forward = FeedForward(d_model, d_ff, dropout)
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass przez encoder layer
        
        Args:
            x: Input tensor [batch_size, seq_len, d_model]
            mask: Optional attention mask
            
        Returns:
            Tuple[torch.Tensor, torch.Tensor]: Output i attention weights
        """
        # Multi-head attention z residual connection
        attention_output, attention_weights = self.multi_head_attention(x, x, x, mask)
        x = self.norm1(x + self.dropout(attention_output))
        
        # Feed-forward z residual connection
        ff_output = self.feed_forward(x)
        x = self.norm2(x + self.dropout(ff_output))
        
        return x, attention_weights

class TransformerEncoder(nn.Module):
    """
    🧠 Core Transformer Encoder dla TSGC
    
    Multi-layer transformer encoder dla konwersji sequences
    na rich hidden representations dla symbolic reasoning.
    """
    
    def __init__(self, 
                 vocab_size: int = 10000, 
                 d_model: int = 512, 
                 num_heads: int = 8,
                 num_layers: int = 6, 
                 d_ff: int = 2048, 
                 max_len: int = 5000,
                 dropout: float = 0.1):
        """
        Inicjalizuje Transformer Encoder
        
        Args:
            vocab_size: Rozmiar vocabulary
            d_model: Wymiar modelu/embeddings
            num_heads: Liczba attention heads
            num_layers: Liczba encoder layers
            d_ff: Wymiar feed-forward network
            max_len: Maksymalna długość sekwencji
            dropout: Dropout rate
        """
        super(TransformerEncoder, self).__init__()
        
        self.d_model = d_model
        self.num_layers = num_layers
        
        # Embedding layers
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.positional_encoding = PositionalEncoding(d_model, max_len)
        
        # Transformer encoder layers
        self.layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        
        self.dropout = nn.Dropout(dropout)
        
        # Statistics
        self.total_sequences_processed = 0
        self.avg_attention_entropy = 0.0
        
        logger.info(f"🧠 TransformerEncoder initialized: d_model={d_model}, layers={num_layers}, heads={num_heads}")
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> Dict[str, torch.Tensor]:
        """
        Forward pass przez transformer encoder
        
        Args:
            x: Input token indices [batch_size, seq_len]
            mask: Optional attention mask
            
        Returns:
            Dict[str, torch.Tensor]: Output dictionary containing:
                - hidden_states: Final hidden representations
                - all_hidden_states: Hidden states from all layers
                - attention_weights: All attention weights
        """
        # Input embedding i positional encoding
        x = self.embedding(x) * math.sqrt(self.d_model)
        x = self.positional_encoding(x.transpose(0, 1)).transpose(0, 1)
        x = self.dropout(x)
        
        # Collect outputs from all layers
        all_hidden_states = []
        all_attention_weights = []
        
        # Pass through encoder layers
        for layer in self.layers:
            x, attention_weights = layer(x, mask)
            all_hidden_states.append(x)
            all_attention_weights.append(attention_weights)
        
        # Update statistics
        self.total_sequences_processed += x.size(0)
        
        # Calculate attention entropy (measure of attention distribution)
        if all_attention_weights:
            last_attention = all_attention_weights[-1]  # Use last layer attention
            attention_probs = F.softmax(last_attention, dim=-1)
            entropy = -torch.sum(attention_probs * torch.log(attention_probs + 1e-8), dim=-1)
            self.avg_attention_entropy = torch.mean(entropy).item()
        
        return {
            'hidden_states': x,  # Final hidden states [batch_size, seq_len, d_model]
            'all_hidden_states': torch.stack(all_hidden_states),  # All layers
            'attention_weights': torch.stack(all_attention_weights),  # All attention weights
            'pooled_output': torch.mean(x, dim=1)  # Pooled representation [batch_size, d_model]
        }
    
    def encode_sequences(self, sequences: List[List[int]], max_length: Optional[int] = None) -> Dict[str, torch.Tensor]:
        """
        Encodes lista sequences do hidden representations
        
        Args:
            sequences: Lista sequences jako token indices
            max_length: Optional max length dla padding
            
        Returns:
            Dict[str, torch.Tensor]: Encoded representations
        """
        if max_length is None:
            max_length = max(len(seq) for seq in sequences)
        
        # Pad sequences
        padded_sequences = []
        attention_masks = []
        
        for seq in sequences:
            if len(seq) > max_length:
                seq = seq[:max_length]
            
            # Pad with zeros
            padded_seq = seq + [0] * (max_length - len(seq))
            attention_mask = [1] * len(seq) + [0] * (max_length - len(seq))
            
            padded_sequences.append(padded_seq)
            attention_masks.append(attention_mask)
        
        # Convert to tensors
        input_ids = torch.tensor(padded_sequences)
        attention_mask = torch.tensor(attention_masks)
        
        # Forward pass
        with torch.no_grad():
            outputs = self.forward(input_ids, attention_mask)
        
        logger.debug(f"📊 Encoded {len(sequences)} sequences to hidden states")
        return outputs
    
    def get_symbolic_features(self, hidden_states: torch.Tensor, 
                            sequence_lengths: Optional[List[int]] = None) -> Dict[str, torch.Tensor]:
        """
        Ekstraktuje features użyteczne dla symbolic reasoning
        
        Args:
            hidden_states: Hidden states tensor [batch_size, seq_len, d_model]
            sequence_lengths: Opcjonalne rzeczywiste długości sequences
            
        Returns:
            Dict[str, torch.Tensor]: Symbolic features
        """
        batch_size, seq_len, d_model = hidden_states.shape
        
        features = {}
        
        # 1. Sequence-level pooling
        features['mean_pooling'] = torch.mean(hidden_states, dim=1)  # [batch_size, d_model]
        features['max_pooling'] = torch.max(hidden_states, dim=1)[0]  # [batch_size, d_model]
        
        # 2. Position-aware features
        # First token (often represents sequence-level info)
        features['first_token'] = hidden_states[:, 0, :]  # [batch_size, d_model]
        
        # Last token (dla sequences o różnych długościach)
        if sequence_lengths:
            last_token_features = []
            for i, length in enumerate(sequence_lengths):
                last_idx = min(length - 1, seq_len - 1)
                last_token_features.append(hidden_states[i, last_idx, :])
            features['last_token'] = torch.stack(last_token_features)
        else:
            features['last_token'] = hidden_states[:, -1, :]  # [batch_size, d_model]
        
        # 3. Attention-weighted features (z ostatniej warstwy)
        # Simplified - użyjemy mean pooling jako approximation
        features['attention_weighted'] = features['mean_pooling']
        
        return features
    
    def save_model(self, filepath: str) -> None:
        """
        Zapisuje model do pliku
        
        Args:
            filepath: Ścieżka do pliku
        """
        try:
            torch.save({
                'model_state_dict': self.state_dict(),
                'config': {
                    'vocab_size': self.embedding.num_embeddings,
                    'd_model': self.d_model,
                    'num_layers': self.num_layers
                },
                'stats': {
                    'total_sequences_processed': self.total_sequences_processed,
                    'avg_attention_entropy': self.avg_attention_entropy
                }
            }, filepath)
            
            logger.info(f"💾 TransformerEncoder saved to {filepath}")
            
        except Exception as e:
            logger.error(f"🚨 Failed to save model: {e}")
    
    def load_model(self, filepath: str) -> None:
        """
        Ładuje model z pliku
        
        Args:
            filepath: Ścieżka do pliku
        """
        try:
            checkpoint = torch.load(filepath, map_location='cpu')
            self.load_state_dict(checkpoint['model_state_dict'])
            
            # Restore statistics
            stats = checkpoint.get('stats', {})
            self.total_sequences_processed = stats.get('total_sequences_processed', 0)
            self.avg_attention_entropy = stats.get('avg_attention_entropy', 0.0)
            
            logger.info(f"💾 TransformerEncoder loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"🚨 Failed to load model: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Pobiera statystyki modelu
        
        Returns:
            Dict[str, Any]: Statystyki
        """
        return {
            'd_model': self.d_model,
            'num_layers': self.num_layers,
            'total_parameters': sum(p.numel() for p in self.parameters()),
            'trainable_parameters': sum(p.numel() for p in self.parameters() if p.requires_grad),
            'total_sequences_processed': self.total_sequences_processed,
            'avg_attention_entropy': self.avg_attention_entropy
        }
    
    def __repr__(self) -> str:
        return f"TransformerEncoder(d_model={self.d_model}, layers={self.num_layers}, processed={self.total_sequences_processed})"