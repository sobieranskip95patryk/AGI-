#!/usr/bin/env python3
"""
⚙️ LOGIC ENGINE CONFIGURATION
Konfiguracja parametrów dla systemu rozumowania logicznego

Zawiera:
- Ustawienia wydajności
- Parametry algorytmów
- Limity zasobów
- Konfiguracja domeny wiedzy
"""

# Wydajność i zasoby
PERFORMANCE_CONFIG = {
    "max_inference_depth": 10,
    "max_reasoning_time": 30.0,  # sekundy
    "max_hypotheses": 10,
    "max_plan_steps": 50,
    "cache_size": 1000,
    "memory_limit_mb": 512
}

# Parametry algorytmów
ALGORITHM_CONFIG = {
    "deduction": {
        "forward_chaining_iterations": 10,
        "backward_chaining_depth": 5,
        "confidence_threshold": 0.1,
        "proof_chain_max_length": 20
    },
    "abduction": {
        "hypothesis_confidence_base": 0.3,
        "cost_weight": 0.2,
        "plausibility_weight": 0.3,
        "consistency_bonus": 0.1,
        "max_alternatives": 5
    },
    "htn_planning": {
        "max_decomposition_depth": 8,
        "resource_buffer_percent": 0.1,
        "priority_weight": 0.4,
        "cost_weight": 0.6
    }
}

# Domeny wiedzy
DOMAIN_CONFIG = {
    "system": {
        "priority": 1,
        "confidence_modifier": 1.0,
        "auto_learning": True
    },
    "cognition": {
        "priority": 2,
        "confidence_modifier": 0.9,
        "auto_learning": True
    },
    "general": {
        "priority": 3,
        "confidence_modifier": 0.8,
        "auto_learning": False
    },
    "external": {
        "priority": 4,
        "confidence_modifier": 0.7,
        "auto_learning": False
    }
}

# Logowanie i debugging
LOGGING_CONFIG = {
    "level": "INFO",
    "detailed_proofs": False,
    "performance_metrics": True,
    "cache_statistics": True,
    "error_reporting": True
}

# Integracja z innymi modułami MIGI 7G
INTEGRATION_CONFIG = {
    "social_vibration_interface": {
        "enabled": True,
        "confidence_sharing": True,
        "emotion_influence": 0.1
    },
    "hegemony_drive": {
        "enabled": True,
        "goal_priority_boost": 0.2,
        "resource_competition": True
    },
    "meta_metacognition": {
        "enabled": True,
        "self_reflection": True,
        "learning_feedback": True
    }
}

# Bezpieczeństwo i ograniczenia
SAFETY_CONFIG = {
    "max_concurrent_reasonings": 5,
    "infinite_loop_detection": True,
    "resource_monitoring": True,
    "fallback_timeout": 60.0,
    "emergency_shutdown_threshold": 0.95  # CPU/Memory usage
}

# Kombinuj wszystkie konfiguracje
LOGIC_ENGINE_CONFIG = {
    "performance": PERFORMANCE_CONFIG,
    "algorithms": ALGORITHM_CONFIG,
    "domains": DOMAIN_CONFIG,
    "logging": LOGGING_CONFIG,
    "integration": INTEGRATION_CONFIG,
    "safety": SAFETY_CONFIG,
    "version": "1.0.0",
    "last_updated": "2024-01-15"
}

def get_config(section: str = None):
    """Pobiera konfigurację dla danej sekcji lub całą konfigurację"""
    if section:
        return LOGIC_ENGINE_CONFIG.get(section, {})
    return LOGIC_ENGINE_CONFIG

def validate_config():
    """Waliduje konfigurację Logic Engine"""
    issues = []
    
    # Sprawdź wydajność
    perf = PERFORMANCE_CONFIG
    if perf["max_reasoning_time"] < 1.0:
        issues.append("max_reasoning_time too low")
    if perf["max_inference_depth"] < 3:
        issues.append("max_inference_depth too low")
    
    # Sprawdź algorytmy
    for algo, config in ALGORITHM_CONFIG.items():
        if "confidence_threshold" in config and config["confidence_threshold"] < 0:
            issues.append(f"{algo} confidence_threshold invalid")
    
    return {"valid": len(issues) == 0, "issues": issues}

if __name__ == "__main__":
    validation = validate_config()
    print(f"Configuration validation: {'PASS' if validation['valid'] else 'FAIL'}")
    if validation['issues']:
        print("Issues found:", validation['issues'])