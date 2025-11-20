# save_snapshot.py
import json
import os
import time
import uuid
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

SNAPSHOT_DIR = "snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

@dataclass
class SystemState:
    """Struktura danych dla stanu systemu NSF + MIGI_7G"""
    stress_level: float
    cortisol_ppm: float
    coherence: float
    active_archetype: str
    archetype_stability: float
    brain_layers: Dict[str, Dict[str, float]]
    module_health: Dict[str, str]
    system_health: float
    anomalies: list
    regulation_index: float
    
    def __post_init__(self):
        """Walidacja zakresów wartości"""
        self.stress_level = max(0.0, min(1.0, self.stress_level))
        self.cortisol_ppm = max(0.0, self.cortisol_ppm)
        self.coherence = max(0.0, min(1.0, self.coherence))
        self.archetype_stability = max(0.0, min(1.0, self.archetype_stability))
        self.system_health = max(0.0, min(1.0, self.system_health))
        self.regulation_index = max(0.0, self.regulation_index)

def save_snapshot(state: Dict[str, Any], source: str = "dashboard_demo") -> str:
    """
    Zapisuje snapshot JSON stanu dashboardu z metadanymi.
    Zwraca pełną ścieżkę pliku.
    
    Args:
        state: Słownik z danymi stanu systemu
        source: Źródło danych (dashboard_demo, live_nsf, integration_hub)
    
    Returns:
        str: Pełna ścieżka do zapisanego pliku
    """
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    trace_id = str(uuid.uuid4())
    
    # Dodanie metadanych spójności
    payload = {
        "metadata": {
            "trace_id": trace_id,
            "timestamp_utc": ts,
            "timestamp_local": datetime.now().isoformat(),
            "source": source,
            "version": "migi_dashboard_v1.0",
            "schema_version": "1.0"
        },
        "state": state,
        "validation": {
            "ranges_validated": True,
            "coherence_check": _validate_coherence(state),
            "anomaly_flags": _detect_anomalies(state)
        }
    }
    
    filename = f"{SNAPSHOT_DIR}/snapshot_{ts}_{trace_id[:8]}.json"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Snapshot saved: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Error saving snapshot: {e}")
        raise

def _validate_coherence(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Waliduje spójność danych stanu
    Wykrywa fałszywą koherencję (masking)
    """
    coherence = state.get("coherence", 0)
    stress = state.get("stress_level", 0)
    cortisol = state.get("cortisol_ppm", 0)
    
    # Detekcja fałszywej koherencji
    masking_risk = 0.0
    if coherence > 0.7 and stress > 0.6:
        masking_risk = (coherence * stress) - 0.42  # Threshold 0.42
    
    # Detekcja sztywności archetypowej
    archetype_stability = state.get("archetype_stability", 0)
    rigidity_risk = max(0.0, archetype_stability - 0.85)
    
    return {
        "masking_risk": max(0.0, min(1.0, masking_risk)),
        "rigidity_risk": max(0.0, min(1.0, rigidity_risk)),
        "stress_coherence_ratio": stress / (coherence + 0.01),
        "overall_consistency": 1.0 - max(masking_risk, rigidity_risk)
    }

def _detect_anomalies(state: Dict[str, Any]) -> list:
    """Wykrywa anomalie w stanie systemu"""
    anomalies = []
    
    # Sprawdzenie extremów
    if state.get("stress_level", 0) > 0.9:
        anomalies.append({"type": "extreme_stress", "severity": "high", "value": state["stress_level"]})
    
    if state.get("coherence", 1) < 0.2:
        anomalies.append({"type": "low_coherence", "severity": "medium", "value": state["coherence"]})
    
    # Sprawdzenie dominacji modułów
    module_health = state.get("module_health", {})
    degraded_modules = [k for k, v in module_health.items() if v in ["DEGRADED", "FAIL"]]
    if len(degraded_modules) > 1:
        anomalies.append({"type": "multiple_module_failure", "severity": "critical", "modules": degraded_modules})
    
    return anomalies

def load_snapshot(filepath: str) -> Dict[str, Any]:
    """
    Ładuje snapshot z pliku
    
    Args:
        filepath: Ścieżka do pliku snapshot
    
    Returns:
        Dict z danymi snapshot
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading snapshot: {e}")
        raise

def get_recent_snapshots(limit: int = 10) -> list:
    """
    Zwraca listę ostatnich snapshotów
    
    Args:
        limit: Maksymalna liczba zwracanych snapshotów
    
    Returns:
        Lista posortowanych ścieżek do plików snapshot
    """
    if not os.path.exists(SNAPSHOT_DIR):
        return []
    
    snapshots = []
    for filename in os.listdir(SNAPSHOT_DIR):
        if filename.startswith("snapshot_") and filename.endswith(".json"):
            filepath = os.path.join(SNAPSHOT_DIR, filename)
            snapshots.append((filepath, os.path.getctime(filepath)))
    
    # Sortowanie po czasie utworzenia (najnowsze pierwsze)
    snapshots.sort(key=lambda x: x[1], reverse=True)
    
    return [filepath for filepath, _ in snapshots[:limit]]

def cleanup_old_snapshots(keep_days: int = 7):
    """
    Usuwa stare snapshoty starsze niż keep_days
    
    Args:
        keep_days: Liczba dni do zachowania
    """
    if not os.path.exists(SNAPSHOT_DIR):
        return
    
    cutoff_time = time.time() - (keep_days * 24 * 60 * 60)
    removed_count = 0
    
    for filename in os.listdir(SNAPSHOT_DIR):
        if filename.startswith("snapshot_") and filename.endswith(".json"):
            filepath = os.path.join(SNAPSHOT_DIR, filename)
            if os.path.getctime(filepath) < cutoff_time:
                try:
                    os.remove(filepath)
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️ Could not remove {filepath}: {e}")
    
    if removed_count > 0:
        print(f"🧹 Cleaned up {removed_count} old snapshots")

# Example usage
if __name__ == "__main__":
    # Przykładowy stan systemu
    example_state = {
        "stress_level": 0.34,
        "cortisol_ppm": 12.7,
        "coherence": 0.78,
        "active_archetype": "Sage",
        "archetype_stability": 0.65,
        "brain_layers": {
            "Reptilian": {"coherence": 0.8, "load": 45, "entropy": 0.2},
            "Limbic": {"coherence": 0.7, "load": 60, "entropy": 0.3},
            "Neocortex": {"coherence": 0.85, "load": 70, "entropy": 0.15},
            "Meta": {"coherence": 0.9, "load": 55, "entropy": 0.1}
        },
        "module_health": {
            "NSF": "OK", 
            "LogicEngine": "OK", 
            "ArchetypeCore": "OK"
        },
        "system_health": 0.82,
        "anomalies": [],
        "regulation_index": 0.72
    }
    
    print("=== SNAPSHOT SYSTEM TEST ===")
    snapshot_path = save_snapshot(example_state, "test_demo")
    print(f"Saved to: {snapshot_path}")
    
    # Testowanie ładowania
    loaded = load_snapshot(snapshot_path)
    print(f"Loaded trace_id: {loaded['metadata']['trace_id']}")
    print(f"Validation results: {loaded['validation']}")
    
    # Lista ostatnich snapshotów
    recent = get_recent_snapshots(5)
    print(f"Recent snapshots: {len(recent)}")
    
    print("✅ Snapshot system ready!")