#!/usr/bin/env python3
"""
🧠 LOGIC ENGINE MODULE - Advanced Reasoning System
Moduł zaawansowanego rozumowania logicznego dla systemu AGI MIGI 7G

Komponenty:
- LogicEngine: Główny silnik rozumowania
- KnowledgeBase: Baza wiedzy i faktów
- DeductiveReasoner: Rozumowanie dedukcyjne
- AbductiveReasoner: Rozumowanie abdukcyjne  
- HTNPlanner: Hierarchiczne planowanie zadań

Autor: MIGI 7G Development Team
Wersja: 1.0.0
Status: IMPLEMENTATION PHASE 1
"""

from .reasoning_engine import (
    LogicEngine,
    KnowledgeBase,
    DeductiveReasoner,
    AbductiveReasoner,
    HTNPlanner,
    ReasoningType,
    ConfidenceLevel,
    Fact,
    Rule,
    Hypothesis,
    InferenceResult,
    HTNTask
)

from .config import (
    LOGIC_ENGINE_CONFIG,
    get_config,
    validate_config
)

# Metadane modułu
__version__ = "1.0.0"
__author__ = "MIGI 7G Development Team"
__description__ = "Advanced Reasoning System for AGI"
__status__ = "Implementation Phase 1"

# Główne klasy eksportowane
__all__ = [
    # Główne komponenty
    "LogicEngine",
    "KnowledgeBase", 
    "DeductiveReasoner",
    "AbductiveReasoner",
    "HTNPlanner",
    
    # Typy i enumeracje
    "ReasoningType",
    "ConfidenceLevel",
    
    # Struktury danych
    "Fact",
    "Rule", 
    "Hypothesis",
    "InferenceResult",
    "HTNTask",
    
    # Konfiguracja
    "LOGIC_ENGINE_CONFIG",
    "get_config",
    "validate_config",
    
    # Metadane
    "__version__",
    "__author__",
    "__description__",
    "__status__"
]

# Inicjalizacja modułu
def initialize_logic_engine():
    """Inicjalizuje Logic Engine z domyślną konfiguracją"""
    engine = LogicEngine()
    return engine

# Szybki test integralności modułu
def module_health_check():
    """Przeprowadza podstawowy test modułu"""
    try:
        engine = initialize_logic_engine()
        status = engine.get_reasoning_status()
        diagnostics = engine.run_diagnostic_tests()
        
        return {
            "module_loaded": True,
            "engine_operational": status["operational"],
            "diagnostic_status": diagnostics["overall_status"],
            "knowledge_base_ready": status["knowledge_base"]["facts_count"] > 0,
            "version": __version__
        }
    except Exception as e:
        return {
            "module_loaded": False,
            "error": str(e),
            "version": __version__
        }

# Wyświetl informacje o module przy imporcie
if __name__ != "__main__":
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"🧠 Logic Engine Module v{__version__} loaded successfully")
    logger.info(f"📊 Available components: {len(__all__)} classes and functions")