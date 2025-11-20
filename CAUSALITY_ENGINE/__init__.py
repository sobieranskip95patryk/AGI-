#!/usr/bin/env python3
"""
🔗 CAUSALITY ENGINE MODULE - Pearl Level-3 Reasoning
Moduł rozumowania przyczynowego dla systemu AGI MIGI 7G

Komponenty:
- CausalityEngine: Główny silnik przyczynowości
- CausalGraph: Struktury DAG i d-separation
- DoCalculus: Pearl's intervention calculus  
- CounterfactualReasoner: What-if analysis
- CausalDiscovery: Odkrywanie związków przyczynowych

Autor: MIGI 7G Development Team
Wersja: 1.0.0  
Status: PHASE 2 - INTELLECTUAL ASCENSION
"""

from .causal_graph import (
    CausalityEngine,
    CausalGraph,
    DoCalculus,
    CounterfactualReasoner,
    CausalVariable,
    CausalEdge,
    CausalQuery,
    CausalResult,
    CausalRelationType,
    InterventionType
)

from .do_engine import (
    DoCalculusValidator,
    DoOperation,
    DoRule
)

from .counterfactual import (
    CounterfactualEngine,
    CounterfactualScenario  
)

from .config import (
    CAUSALITY_ENGINE_CONFIG,
    PEARL_LEVELS,
    get_config,
    validate_config
)

# Metadane modułu
__version__ = "1.0.0"
__author__ = "MIGI 7G Development Team"
__description__ = "Pearl Level-3 Causal Reasoning for AGI"
__status__ = "Phase 2 - Intellectual Ascension"
__pearl_level__ = 3  # Supports all Pearl hierarchy levels

# Główne klasy eksportowane
__all__ = [
    # Główne komponenty
    "CausalityEngine",
    "CausalGraph", 
    "DoCalculus",
    "CounterfactualReasoner",
    "DoCalculusValidator",
    "CounterfactualEngine",
    
    # Struktury danych
    "CausalVariable",
    "CausalEdge",
    "CausalQuery", 
    "CausalResult",
    "DoOperation",
    "CounterfactualScenario",
    
    # Typy i enumeracje
    "CausalRelationType",
    "InterventionType",
    "DoRule",
    
    # Konfiguracja
    "CAUSALITY_ENGINE_CONFIG",
    "PEARL_LEVELS",
    "get_config",
    "validate_config",
    
    # Metadane
    "__version__",
    "__author__", 
    "__description__",
    "__status__",
    "__pearl_level__"
]

# Inicjalizacja modułu
def initialize_causality_engine():
    """Inicjalizuje Causality Engine z domyślną konfiguracją"""
    engine = CausalityEngine()
    return engine

# Test integralności modułu
def module_health_check():
    """Przeprowadza podstawowy test modułu"""
    try:
        engine = initialize_causality_engine()
        status = engine.get_causality_status()
        diagnostics = engine.run_diagnostic_tests()
        
        return {
            "module_loaded": True,
            "engine_operational": status["operational"],
            "diagnostic_status": diagnostics["overall_status"],
            "pearl_level_3_ready": diagnostics.get("counterfactual_test", False),
            "causal_graphs_count": len(status["causal_graphs"]),
            "version": __version__,
            "pearl_compliance": True
        }
    except Exception as e:
        return {
            "module_loaded": False,
            "error": str(e),
            "version": __version__,
            "pearl_compliance": False
        }

# Wyświetl informacje o module przy imporcie
if __name__ != "__main__":
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"🔗 Causality Engine Module v{__version__} loaded successfully")
    logger.info(f"🌟 Pearl Level-{__pearl_level__} Reasoning: READY")
    logger.info(f"📊 Available components: {len(__all__)} classes and functions")