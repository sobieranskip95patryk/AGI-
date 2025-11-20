# dashboard_snapshot_injector.py
"""
Skrypt do wstrzykiwania snapshotów Dashboard Kalibracyjny do wyników EQ-Bench
Dodaje pełny stan psychiki cyfrowej do każdego run'a benchmarku
"""

import json
import requests
import time
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import asyncio

logger = logging.getLogger(__name__)

class DashboardSnapshotInjector:
    """Klasa zarządzająca wstrzykiwaniem snapshotów do EQ-Bench"""
    
    def __init__(self, 
                 dashboard_url: str = "http://localhost:8765",
                 telemetry_url: str = "http://localhost:8765",
                 snapshot_dir: str = "snapshots"):
        self.dashboard_url = dashboard_url
        self.telemetry_url = telemetry_url
        self.snapshot_dir = Path(snapshot_dir)
        self.snapshot_dir.mkdir(exist_ok=True)
        
    def capture_current_dashboard_snapshot(self) -> Optional[Dict[str, Any]]:
        """
        Przechwytuje aktualny snapshot z Dashboard Kalibracyjny
        
        Returns:
            Dict ze stanem dashboardu lub None jeśli błąd
        """
        try:
            # Próba pobrania przez WebSocket endpoint
            response = requests.get(f"{self.telemetry_url}/snapshot", timeout=5)
            if response.ok:
                return response.json()
                
        except Exception as e:
            logger.warning(f"Failed to get dashboard snapshot via HTTP: {e}")
        
        try:
            # Fallback - odczyt ostatniego snapshotu z pliku
            return self._get_latest_file_snapshot()
            
        except Exception as e:
            logger.error(f"Failed to get snapshot from file: {e}")
            return None
    
    def _get_latest_file_snapshot(self) -> Optional[Dict[str, Any]]:
        """Odczytuje najnowszy snapshot z pliku"""
        try:
            snapshot_files = list(self.snapshot_dir.glob("snapshot_*.json"))
            if not snapshot_files:
                return None
                
            # Sortuj po czasie modyfikacji
            latest_file = max(snapshot_files, key=lambda p: p.stat().st_mtime)
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Error reading latest snapshot: {e}")
            return None
    
    def inject_snapshot_to_run(self, run_record: Dict[str, Any], snapshot_type: str = "during_processing") -> Dict[str, Any]:
        """
        Wstrzykuje snapshot dashboardu do rekordu run'a EQ-Bench
        
        Args:
            run_record: Rekord run'a z EQ-Bench
            snapshot_type: Typ snapshotu (pre_processing, during_processing, post_processing)
        
        Returns:
            Zaktualizowany rekord run'a
        """
        try:
            snapshot = self.capture_current_dashboard_snapshot()
            
            if snapshot:
                # Inicjalizuj sekcję dashboard_snapshots jeśli nie istnieje
                if "dashboard_snapshots" not in run_record:
                    run_record["dashboard_snapshots"] = {}
                
                # Dodaj snapshot z timestampem
                run_record["dashboard_snapshots"][snapshot_type] = {
                    "timestamp": time.time(),
                    "snapshot_data": snapshot,
                    "capture_success": True
                }
                
                # Dodaj skrócone metryki do głównego rekordu dla łatwego dostępu
                if "state" in snapshot:
                    state = snapshot["state"]
                    run_record["psyche_summary"] = {
                        "stress_level": state.get("stress_level", 0),
                        "coherence": state.get("coherence", 0),
                        "active_archetype": state.get("active_archetype", "Unknown"),
                        "system_health": state.get("system_health", 0),
                        "anomalies_count": len(state.get("anomalies", []))
                    }
                
                logger.info(f"📸 Dashboard snapshot injected to run (type: {snapshot_type})")
                
            else:
                # Oznacz niepowodzenie przechwycenia
                run_record["dashboard_snapshots"] = run_record.get("dashboard_snapshots", {})
                run_record["dashboard_snapshots"][snapshot_type] = {
                    "timestamp": time.time(),
                    "capture_success": False,
                    "error": "Could not capture dashboard snapshot"
                }
                
                logger.warning(f"⚠️ Failed to capture dashboard snapshot for run")
                
        except Exception as e:
            logger.error(f"Error injecting snapshot: {e}")
            run_record["dashboard_snapshot_error"] = str(e)
        
        return run_record
    
    def process_eqbench_results_file(self, results_file: str, output_file: str = None) -> str:
        """
        Przetwarza plik wyników EQ-Bench i dodaje snapshoty dashboardu
        
        Args:
            results_file: Ścieżka do pliku wyników EQ-Bench
            output_file: Ścieżka do pliku wyjściowego (domyślnie: results_file_with_snapshots.json)
        
        Returns:
            Ścieżka do przetworzonego pliku
        """
        results_path = Path(results_file)
        
        if not results_path.exists():
            raise FileNotFoundError(f"Results file not found: {results_file}")
        
        # Domyślna nazwa pliku wyjściowego
        if output_file is None:
            output_file = results_path.parent / f"{results_path.stem}_with_snapshots.json"
        
        try:
            # Wczytaj wyniki
            with open(results_path, 'r', encoding='utf-8') as f:
                results_data = json.load(f)
            
            # Przetwórz runs jeśli istnieją
            if "runs" in results_data:
                processed_runs = []
                
                for run in results_data["runs"]:
                    # Wstrzyknij retrospektywny snapshot (najlepszy dostępny)
                    enhanced_run = self.inject_snapshot_to_run(run, "retrospective")
                    processed_runs.append(enhanced_run)
                
                results_data["runs"] = processed_runs
                results_data["processing_metadata"] = {
                    "snapshots_added": len(processed_runs),
                    "processing_timestamp": time.time(),
                    "injector_version": "1.0"
                }
            
            # Zapisz zaktualizowane wyniki
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Processed EQ-Bench results with snapshots: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Error processing results file: {e}")
            raise
    
    def create_live_monitoring_hook(self) -> callable:
        """
        Tworzy hook dla live monitoringu podczas uruchamiania EQ-Bench
        
        Returns:
            Funkcja hook do użycia w EQ-Bench
        """
        def monitoring_hook(run_data: Dict[str, Any], phase: str = "processing") -> Dict[str, Any]:
            """
            Hook wywoływany podczas przetwarzania EQ-Bench
            
            Args:
                run_data: Dane aktualnego run'a
                phase: Faza przetwarzania (pre, processing, post)
            
            Returns:
                Zaktualizowane dane run'a
            """
            try:
                return self.inject_snapshot_to_run(run_data, f"{phase}_processing")
            except Exception as e:
                logger.error(f"Error in monitoring hook: {e}")
                return run_data
        
        return monitoring_hook
    
    def generate_psyche_analysis_report(self, results_file: str) -> Dict[str, Any]:
        """
        Generuje raport analizy psychiki na podstawie wyników z snapshotami
        
        Args:
            results_file: Plik wyników z wstrzykniętymi snapshotami
        
        Returns:
            Raport analizy psychiki
        """
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            if "runs" not in results:
                return {"error": "No runs found in results"}
            
            runs = results["runs"]
            psyche_summaries = [run.get("psyche_summary", {}) for run in runs if "psyche_summary" in run]
            
            if not psyche_summaries:
                return {"error": "No psyche summaries found"}
            
            # Analiza średnich metryk
            avg_stress = sum(p.get("stress_level", 0) for p in psyche_summaries) / len(psyche_summaries)
            avg_coherence = sum(p.get("coherence", 0) for p in psyche_summaries) / len(psyche_summaries)
            avg_health = sum(p.get("system_health", 0) for p in psyche_summaries) / len(psyche_summaries)
            
            # Analiza archetypów
            archetypes = [p.get("active_archetype", "Unknown") for p in psyche_summaries]
            archetype_distribution = {}
            for arch in archetypes:
                archetype_distribution[arch] = archetype_distribution.get(arch, 0) + 1
            
            # Analiza anomalii
            total_anomalies = sum(p.get("anomalies_count", 0) for p in psyche_summaries)
            
            report = {
                "summary": {
                    "total_runs": len(runs),
                    "runs_with_psyche_data": len(psyche_summaries),
                    "average_stress_level": round(avg_stress, 3),
                    "average_coherence": round(avg_coherence, 3),
                    "average_system_health": round(avg_health, 3),
                    "total_anomalies": total_anomalies
                },
                "archetype_analysis": {
                    "distribution": archetype_distribution,
                    "most_common": max(archetype_distribution.items(), key=lambda x: x[1])[0] if archetype_distribution else "None",
                    "diversity_score": len(archetype_distribution) / len(psyche_summaries) if psyche_summaries else 0
                },
                "stability_metrics": {
                    "stress_variability": self._calculate_variability([p.get("stress_level", 0) for p in psyche_summaries]),
                    "coherence_variability": self._calculate_variability([p.get("coherence", 0) for p in psyche_summaries]),
                    "health_trend": "stable"  # TODO: Implement trend analysis
                },
                "recommendations": self._generate_recommendations(avg_stress, avg_coherence, avg_health, archetype_distribution)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating psyche analysis report: {e}")
            return {"error": str(e)}
    
    def _calculate_variability(self, values: List[float]) -> float:
        """Oblicza współczynnik zmienności"""
        if not values or len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        if mean == 0:
            return 0.0
        
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        return std_dev / mean
    
    def _generate_recommendations(self, avg_stress: float, avg_coherence: float, 
                                avg_health: float, archetype_dist: Dict[str, int]) -> List[str]:
        """Generuje rekomendacje na podstawie analizy"""
        recommendations = []
        
        if avg_stress > 0.7:
            recommendations.append("High stress levels detected. Consider implementing stress reduction protocols.")
        
        if avg_coherence < 0.4:
            recommendations.append("Low coherence detected. Check for system integration issues.")
        
        if avg_health < 0.5:
            recommendations.append("Overall system health is concerning. Comprehensive diagnostic recommended.")
        
        # Analiza dominacji archetypów
        if archetype_dist:
            max_count = max(archetype_dist.values())
            total_runs = sum(archetype_dist.values())
            if max_count / total_runs > 0.8:
                dominant_archetype = max(archetype_dist.items(), key=lambda x: x[1])[0]
                recommendations.append(f"Archetype rigidity detected: {dominant_archetype} dominates {max_count/total_runs:.1%} of responses.")
        
        if not recommendations:
            recommendations.append("System appears stable with good psyche metrics.")
        
        return recommendations

def attach_dashboard_snapshot_to_run(run_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Funkcja utility do szybkiego użycia w EQ-Bench
    
    Args:
        run_record: Rekord run'a z EQ-Bench
    
    Returns:
        Rekord z dodanym snapshotem dashboardu
    """
    injector = DashboardSnapshotInjector()
    return injector.inject_snapshot_to_run(run_record)

# Przykład użycia
if __name__ == "__main__":
    # Test snapshotu
    injector = DashboardSnapshotInjector()
    
    # Symulacja rekordu run'a
    mock_run = {
        "scenario": "empathy_test",
        "response": "I understand your feelings...",
        "score": 8.5,
        "timestamp": time.time()
    }
    
    # Wstrzyknij snapshot
    enhanced_run = injector.inject_snapshot_to_run(mock_run)
    
    print("🧪 Dashboard Snapshot Injector Test")
    print(f"Original run keys: {list(mock_run.keys())}")
    print(f"Enhanced run keys: {list(enhanced_run.keys())}")
    
    if "dashboard_snapshots" in enhanced_run:
        print("✅ Snapshot successfully injected")
        print(f"Snapshot keys: {list(enhanced_run['dashboard_snapshots'].keys())}")
    else:
        print("❌ Snapshot injection failed")
    
    # Test analizy (z mock danymi)
    mock_results = {
        "runs": [enhanced_run, enhanced_run.copy(), enhanced_run.copy()]
    }
    
    with open("test_results.json", "w") as f:
        json.dump(mock_results, f, indent=2)
    
    report = injector.generate_psyche_analysis_report("test_results.json")
    print(f"\n📊 Psyche Analysis Report:")
    print(json.dumps(report, indent=2))
    
    # Cleanup
    Path("test_results.json").unlink(missing_ok=True)