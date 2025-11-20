#!/usr/bin/env python3
"""
🧠 VECTOR CACHE - Optimized Embedding Storage

System cache dla embeddingów z zaawansowanymi funkcjami:
- LRU (Least Recently Used) eviction policy
- Persistent storage z pickle
- Compression dla oszczędności pamięci
- Statistics i monitoring
"""

import logging
from typing import Dict, Any, Optional
import time
from collections import OrderedDict
import pickle
import os
import gzip

logger = logging.getLogger(__name__)

class VectorCache:
    """
    🗄️ Zaawansowany cache system dla embeddingów
    
    Implementuje LRU eviction policy z persistent storage
    i compression dla optymalizacji pamięci.
    """
    
    def __init__(self, max_size: int = 10000, enable_compression: bool = True):
        """
        Inicjalizuje VectorCache
        
        Args:
            max_size: Maksymalny rozmiar cache
            enable_compression: Czy włączyć kompresję przy zapisie
        """
        self.max_size = max_size
        self.enable_compression = enable_compression
        
        # LRU cache using OrderedDict
        self.cache: OrderedDict = OrderedDict()
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.last_access_times: Dict[str, float] = {}
        
        logger.info(f"🗄️ VectorCache initialized: max_size={max_size}, compression={enable_compression}")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Pobiera wartość z cache
        
        Args:
            key: Klucz cache
            
        Returns:
            Optional[Any]: Wartość lub None jeśli nie ma w cache
        """
        if key in self.cache:
            # Move to end (most recently used)
            value = self.cache.pop(key)
            self.cache[key] = value
            self.last_access_times[key] = time.time()
            self.hits += 1
            return value
        else:
            self.misses += 1
            return None
    
    def put(self, key: str, value: Any) -> None:
        """
        Dodaje wartość do cache
        
        Args:
            key: Klucz cache
            value: Wartość do zapisania
        """
        current_time = time.time()
        
        if key in self.cache:
            # Update existing entry
            self.cache.pop(key)
        elif len(self.cache) >= self.max_size:
            # Evict least recently used
            oldest_key = next(iter(self.cache))
            self.cache.pop(oldest_key)
            self.last_access_times.pop(oldest_key, None)
            self.evictions += 1
            logger.debug(f"🗑️ Evicted LRU entry: {oldest_key}")
        
        # Add new entry (most recently used)
        self.cache[key] = value
        self.last_access_times[key] = current_time
    
    def contains(self, key: str) -> bool:
        """Sprawdza czy klucz istnieje w cache"""
        return key in self.cache
    
    def remove(self, key: str) -> bool:
        """
        Usuwa wpis z cache
        
        Args:
            key: Klucz do usunięcia
            
        Returns:
            bool: True jeśli usunięto, False jeśli nie było
        """
        if key in self.cache:
            self.cache.pop(key)
            self.last_access_times.pop(key, None)
            return True
        return False
    
    def clear(self) -> None:
        """Czyści cały cache"""
        cleared_count = len(self.cache)
        self.cache.clear()
        self.last_access_times.clear()
        logger.info(f"🗑️ Cache cleared: {cleared_count} entries removed")
    
    def size(self) -> int:
        """Zwraca aktualny rozmiar cache"""
        return len(self.cache)
    
    def keys(self):
        """Zwraca klucze cache"""
        return self.cache.keys()
    
    def values(self):
        """Zwraca wartości cache"""
        return self.cache.values()
    
    def items(self):
        """Zwraca pary (klucz, wartość) cache"""
        return self.cache.items()
    
    def get_hit_rate(self) -> float:
        """
        Oblicza hit rate cache
        
        Returns:
            float: Hit rate (0.0-1.0)
        """
        total_requests = self.hits + self.misses
        if total_requests == 0:
            return 0.0
        return self.hits / total_requests
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Pobiera statystyki cache
        
        Returns:
            Dict[str, Any]: Statystyki
        """
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'hit_rate': self.get_hit_rate(),
            'utilization': len(self.cache) / self.max_size,
            'compression_enabled': self.enable_compression
        }
    
    def save_to_file(self, filepath: str) -> None:
        """
        Zapisuje cache do pliku z opcjonalną kompresją
        
        Args:
            filepath: Ścieżka do pliku
        """
        try:
            cache_data = {
                'cache': dict(self.cache),  # Convert OrderedDict to dict
                'last_access_times': self.last_access_times,
                'stats': {
                    'hits': self.hits,
                    'misses': self.misses,
                    'evictions': self.evictions
                },
                'config': {
                    'max_size': self.max_size,
                    'compression_enabled': self.enable_compression
                }
            }
            
            if self.enable_compression:
                with gzip.open(filepath + '.gz', 'wb') as f:
                    pickle.dump(cache_data, f)
                logger.info(f"💾 Cache saved (compressed) to {filepath}.gz")
            else:
                with open(filepath, 'wb') as f:
                    pickle.dump(cache_data, f)
                logger.info(f"💾 Cache saved to {filepath}")
                
        except Exception as e:
            logger.error(f"🚨 Failed to save cache: {e}")
    
    def load_from_file(self, filepath: str) -> None:
        """
        Ładuje cache z pliku
        
        Args:
            filepath: Ścieżka do pliku
        """
        try:
            # Try compressed version first
            compressed_path = filepath + '.gz'
            if os.path.exists(compressed_path):
                with gzip.open(compressed_path, 'rb') as f:
                    cache_data = pickle.load(f)
                logger.info(f"💾 Cache loaded (compressed) from {compressed_path}")
            elif os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    cache_data = pickle.load(f)
                logger.info(f"💾 Cache loaded from {filepath}")
            else:
                logger.warning(f"🚨 Cache file not found: {filepath}")
                return
            
            # Restore cache data
            self.cache = OrderedDict(cache_data['cache'])
            self.last_access_times = cache_data.get('last_access_times', {})
            
            # Restore statistics
            stats = cache_data.get('stats', {})
            self.hits = stats.get('hits', 0)
            self.misses = stats.get('misses', 0)
            self.evictions = stats.get('evictions', 0)
            
            # Restore config
            config = cache_data.get('config', {})
            self.max_size = config.get('max_size', self.max_size)
            self.enable_compression = config.get('compression_enabled', self.enable_compression)
            
            logger.info(f"📊 Loaded {len(self.cache)} cache entries")
            
        except Exception as e:
            logger.error(f"🚨 Failed to load cache: {e}")
    
    def cleanup_old_entries(self, max_age_seconds: float = 3600) -> int:
        """
        Usuwa stare wpisy z cache
        
        Args:
            max_age_seconds: Maksymalny wiek wpisu w sekundach
            
        Returns:
            int: Liczba usuniętych wpisów
        """
        current_time = time.time()
        keys_to_remove = []
        
        for key, last_access in self.last_access_times.items():
            if current_time - last_access > max_age_seconds:
                keys_to_remove.append(key)
        
        removed_count = 0
        for key in keys_to_remove:
            if self.remove(key):
                removed_count += 1
        
        if removed_count > 0:
            logger.info(f"🧹 Cleaned up {removed_count} old cache entries")
        
        return removed_count
    
    def __repr__(self) -> str:
        return f"VectorCache(size={len(self.cache)}/{self.max_size}, hit_rate={self.get_hit_rate():.3f})"