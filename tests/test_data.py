"""
🧪 TSGC Test Data - Sample Medical Sequences

Test data dla TSGC Phase 3.2 validation:
- Medical domain sequences
- Temporal relationships
- Causal patterns
- Expected symbolic outputs
"""

MEDICAL_TEST_SEQUENCES = [
    {
        "id": "seq_001",
        "sequence": ["patient", "has", "fever", "and", "cough"],
        "expected_nodes": [
            {"type": "entity", "predicate": "patient", "confidence": 0.9},
            {"type": "property", "predicate": "fever", "confidence": 0.8},
            {"type": "property", "predicate": "cough", "confidence": 0.8}
        ],
        "expected_edges": [
            {"type": "has_property", "source": "patient", "target": "fever"},
            {"type": "has_property", "source": "patient", "target": "cough"}
        ]
    },
    {
        "id": "seq_002", 
        "sequence": ["temperature", "is", "high", "indicating", "infection"],
        "expected_nodes": [
            {"type": "entity", "predicate": "temperature", "confidence": 0.7},
            {"type": "property", "predicate": "high", "confidence": 0.8},
            {"type": "entity", "predicate": "infection", "confidence": 0.9}
        ],
        "expected_edges": [
            {"type": "indicates", "source": "high_temperature", "target": "infection"}
        ]
    },
    {
        "id": "seq_003",
        "sequence": ["doctor", "prescribes", "antibiotics", "for", "treatment"],
        "expected_nodes": [
            {"type": "entity", "predicate": "doctor", "confidence": 0.9},
            {"type": "action", "predicate": "prescribes", "confidence": 0.9},
            {"type": "entity", "predicate": "antibiotics", "confidence": 0.8},
            {"type": "entity", "predicate": "treatment", "confidence": 0.8}
        ],
        "expected_edges": [
            {"type": "agent", "source": "prescribes", "target": "doctor"},
            {"type": "object", "source": "prescribes", "target": "antibiotics"},
            {"type": "purpose", "source": "prescribes", "target": "treatment"}
        ]
    }
]

TEMPORAL_TEST_SEQUENCES = [
    {
        "id": "temporal_001",
        "sequence": ["patient", "took", "medication", "before", "symptoms", "improved"],
        "expected_temporal_edges": [
            {"type": "before", "source": "took_medication", "target": "symptoms_improved"}
        ]
    },
    {
        "id": "temporal_002", 
        "sequence": ["after", "surgery", "patient", "showed", "recovery"],
        "expected_temporal_edges": [
            {"type": "after", "source": "surgery", "target": "showed_recovery"}
        ]
    }
]

CAUSAL_TEST_SEQUENCES = [
    {
        "id": "causal_001",
        "sequence": ["virus", "causes", "infection", "which", "leads", "to", "fever"],
        "expected_causal_edges": [
            {"type": "causes", "source": "virus", "target": "infection"},
            {"type": "causes", "source": "infection", "target": "fever"}
        ]
    },
    {
        "id": "causal_002",
        "sequence": ["medication", "prevents", "disease", "progression"],
        "expected_causal_edges": [
            {"type": "prevents", "source": "medication", "target": "disease_progression"}
        ]
    }
]

PERFORMANCE_TEST_DATA = {
    "latency_targets": {
        "single_sequence": 0.05,  # 50ms
        "batch_8": 0.2,          # 200ms dla 8 sequences
        "batch_32": 0.5          # 500ms dla 32 sequences
    },
    "confidence_targets": {
        "node_confidence": 0.7,
        "edge_confidence": 0.6,
        "overall_confidence": 0.75
    },
    "throughput_targets": {
        "sequences_per_second": 500,
        "batch_processing": 100
    }
}

ERROR_TEST_CASES = [
    {
        "id": "error_001",
        "sequence": [],  # Empty sequence
        "expected_behavior": "graceful_fallback"
    },
    {
        "id": "error_002", 
        "sequence": None,  # None input
        "expected_behavior": "graceful_fallback"
    },
    {
        "id": "error_003",
        "sequence": ["unknown", "tokens", "that", "never", "seen", "before"],
        "expected_behavior": "low_confidence_processing"
    }
]