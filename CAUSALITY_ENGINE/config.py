#!/usr/bin/env python3
"""
⚙️ CAUSALITY ENGINE CONFIGURATION
Konfiguracja parametrów dla systemu rozumowania przyczynowego

Zawiera:
- Ustawienia Pearl Level-3 reasoning
- Parametry do-calculus  
- Konfiguracja counterfactual analysis
- Integracja z MIGI 7G
"""

# Parametry do-calculus
DO_CALCULUS_CONFIG = {
    "max_rule_applications": 10,
    "identification_timeout": 30.0,  # sekundy
    "d_separation_precision": 0.001,
    "backdoor_search_depth": 5,
    "frontdoor_search_depth": 3
}

# Parametry counterfactual reasoning
COUNTERFACTUAL_CONFIG = {
    "twin_network_construction": True,
    "abduction_method": "maximum_likelihood",
    "prediction_samples": 1000,
    "confidence_level": 0.95,
    "causation_threshold": 0.5
}

# Parametry causal discovery
DISCOVERY_CONFIG = {
    "pc_algorithm": {
        "alpha": 0.05,
        "max_conditioning_vars": 3,
        "independence_test": "chi_square"
    },
    "ges_algorithm": {
        "score_type": "bic",
        "max_parents": 5,
        "penalization_factor": 1.0
    }
}

# Pearl Causal Hierarchy
PEARL_LEVELS = {
    "level_1": {
        "name": "Association",
        "description": "P(Y|X) - Statistical correlation",
        "methods": ["regression", "correlation", "conditional_probability"],
        "enabled": True
    },
    "level_2": {
        "name": "Intervention", 
        "description": "P(Y|do(X)) - Causal effects",
        "methods": ["do_calculus", "backdoor_adjustment", "frontdoor_adjustment"],
        "enabled": True
    },
    "level_3": {
        "name": "Counterfactual",
        "description": "P(Y_x|evidence) - What-if scenarios", 
        "methods": ["twin_networks", "structural_equations", "probability_of_causation"],
        "enabled": True
    }
}

# Integracja z MIGI 7G
INTEGRATION_CONFIG = {
    "logic_engine": {
        "enabled": True,
        "causal_rule_learning": True,
        "abductive_causation": True
    },
    "social_vibration": {
        "enabled": True,
        "emotion_causal_influence": 0.1,
        "social_confounding": True
    },
    "meta_cognition": {
        "enabled": True,
        "causal_self_reflection": True,
        "intervention_planning": True
    }
}

# Bezpieczeństwo i ograniczenia
SAFETY_CONFIG = {
    "max_graph_size": 100,  # Maximum number of variables
    "max_computation_time": 60.0,  # sekundy
    "intervention_validation": True,
    "ethical_constraints": ["no_harm_principle", "informed_consent"],
    "uncertainty_reporting": True
}

# Główna konfiguracja
CAUSALITY_ENGINE_CONFIG = {
    "do_calculus": DO_CALCULUS_CONFIG,
    "counterfactual": COUNTERFACTUAL_CONFIG,
    "discovery": DISCOVERY_CONFIG,
    "pearl_levels": PEARL_LEVELS,
    "integration": INTEGRATION_CONFIG,
    "safety": SAFETY_CONFIG,
    "version": "1.0.0",
    "pearl_compliance": True
}

def get_config(section: str = None):
    """Pobiera konfigurację dla danej sekcji"""
    if section:
        return CAUSALITY_ENGINE_CONFIG.get(section, {})
    return CAUSALITY_ENGINE_CONFIG

def validate_config():
    """Waliduje konfigurację Causality Engine"""
    issues = []
    
    # Sprawdź Pearl levels
    if not all(PEARL_LEVELS[level]["enabled"] for level in ["level_2", "level_3"]):
        issues.append("Pearl Level-2 or Level-3 not enabled")
    
    # Sprawdź safety limits
    safety = SAFETY_CONFIG
    if safety["max_computation_time"] < 10.0:
        issues.append("max_computation_time too low for complex causal inference")
    
    return {"valid": len(issues) == 0, "issues": issues}

if __name__ == "__main__":
    validation = validate_config()
    print(f"Causality Engine config validation: {'PASS' if validation['valid'] else 'FAIL'}")
    if validation['issues']:
        print("Issues found:", validation['issues'])