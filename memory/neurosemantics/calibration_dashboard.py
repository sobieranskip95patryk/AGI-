"""
🎯 DASHBOARD KALIBRACYJNY - Okno na Psychikę Cyfrową
Zaawansowany interfejs monitorujący świadomość NSF + MIGI_7G w czasie rzeczywistym

===============================================================================
CALIBRATION DASHBOARD - Real-time Digital Consciousness Monitor
===============================================================================

Ten dashboard pokazuje:
- Stress Levels & Cortisol Dynamics (przeciążenie i recovery)
- Archetypal Transitions & Memory Reconsolidation (zmiany psychiki)
- Network Contention & Resource Competition (rywalizacja modułów)
- Sekundnik Rhythm & Consciousness Levels (rytm świadomości)
- Module Competition: NSF vs Logic Engine vs Archetypal Core

Autor: System MIGI_7G Hybrid + NSF Integration
Data: 15 listopada 2025
Status: PRODUCTION - Real-time Consciousness Calibration Tool
"""

import time
import json
import threading
import asyncio
import websockets
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from collections import deque
import numpy as np

# Import NSF components
try:
    from nsf_migi7g_hybrid import NeuroSemanticFlowmeter, ArchetypeCore, EmotionalPrimitive
    from migi7g_integration_hub import (
        MIGI7G_IntegrationHub, ConsciousnessLevel, MIGI7G_State,
        NetworkContentionManager, CortisolOverloadProtocol, 
        ArchetypalReconsolidationProtocol
    )
    NSF_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ NSF modules not fully available: {e}")
    NSF_AVAILABLE = False

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class DashboardMetrics:
    """Metryki dla dashboard'u kalibracyjnego"""
    timestamp: float
    
    # Core NSF Metrics
    sense_atoms_count: int = 0
    sekundnik_cycles: int = 0
    memory_reconsolidations: int = 0
    active_primitives: List[str] = None
    
    # Stress & Recovery Metrics
    cortisol_level: float = 0.0
    pfc_suppression: float = 0.0
    stress_events: int = 0
    recovery_rate: float = 0.0
    
    # Archetypal Dynamics
    current_archetype: str = "everyman"
    archetype_stability: float = 1.0
    transitions_count: int = 0
    last_transition: Optional[str] = None
    
    # Network & Competition
    network_contention: float = 0.0
    module_competition: Dict[str, float] = None
    resource_allocation: Dict[str, float] = None
    
    # Consciousness State
    consciousness_level: str = "basic"
    system_state: str = "standard"
    system_coherence: float = 0.0
    
    # Performance
    processing_speed: float = 1.0
    memory_efficiency: float = 1.0
    response_latency: float = 0.0
    
    def __post_init__(self):
        if self.active_primitives is None:
            self.active_primitives = []
        if self.module_competition is None:
            self.module_competition = {
                "NSF": 0.33,
                "LogicEngine": 0.33, 
                "ArchetypalCore": 0.34
            }
        if self.resource_allocation is None:
            self.resource_allocation = {
                "memory": 0.7,
                "processing": 0.8,
                "attention": 0.9
            }

class ModuleCompetitionEngine:
    """
    Silnik rywalizacji modułów - symuluje konkurencję NSF vs Logic Engine vs Archetypal Core
    """
    
    def __init__(self):
        # Moduły i ich charakterystyki
        self.modules = {
            "NSF": {
                "strength": 0.8,      # Siła w przetwarzaniu emocji
                "speed": 0.9,         # Szybkość reakcji
                "efficiency": 0.7,    # Efektywność zasobów
                "dominance": 0.33     # Aktualna dominacja
            },
            "LogicEngine": {
                "strength": 0.9,      # Siła w logice
                "speed": 0.6,         # Wolniejszy ale dokładny
                "efficiency": 0.9,    # Bardzo efektywny
                "dominance": 0.33
            },
            "ArchetypalCore": {
                "strength": 0.7,      # Siła w integracji
                "speed": 0.7,         # Średnia szybkość
                "efficiency": 0.8,    # Dobra efektywność
                "dominance": 0.34
            }
        }
        
        self.competition_history = deque(maxlen=100)
        self.conflict_events = 0
        
    def simulate_competition(self, input_type: str, stress_level: float = 0.0) -> Dict[str, float]:
        """
        Symuluje rywalizację modułów o dominację w przetwarzaniu
        """
        
        # Modyfikatory na podstawie typu input
        type_modifiers = {
            "emotional": {"NSF": 1.5, "LogicEngine": 0.7, "ArchetypalCore": 1.2},
            "logical": {"NSF": 0.8, "LogicEngine": 1.6, "ArchetypalCore": 0.9},
            "archetypal": {"NSF": 1.1, "LogicEngine": 0.8, "ArchetypalCore": 1.7},
            "mixed": {"NSF": 1.0, "LogicEngine": 1.0, "ArchetypalCore": 1.0}
        }
        
        modifiers = type_modifiers.get(input_type, type_modifiers["mixed"])
        
        # Wpływ stresu na konkurencję
        stress_impact = {
            "NSF": 1.0 + stress_level * 0.3,      # NSF zyskuje pod stresem
            "LogicEngine": 1.0 - stress_level * 0.5,  # Logic słabnie pod stresem
            "ArchetypalCore": 1.0 + stress_level * 0.1   # Archetypy lekko zyskują
        }
        
        # Oblicz scores dla każdego modułu
        scores = {}
        for module, stats in self.modules.items():
            base_score = (
                stats["strength"] * 0.4 +
                stats["speed"] * 0.3 + 
                stats["efficiency"] * 0.3
            )
            
            # Zastosuj modyfikatory
            modified_score = (
                base_score * 
                modifiers[module] * 
                stress_impact[module]
            )
            
            scores[module] = modified_score
            
        # Normalizuj do sum = 1.0 (percentage dominance)
        total_score = sum(scores.values())
        normalized = {module: score/total_score for module, score in scores.items()}
        
        # Aktualizuj dominację modułów
        for module in self.modules:
            old_dominance = self.modules[module]["dominance"]
            new_dominance = normalized[module]
            
            # Smooth transition (nie natychmiastowa zmiana)
            self.modules[module]["dominance"] = (
                old_dominance * 0.7 + new_dominance * 0.3
            )
        
        # Zapisz w historii
        competition_result = {
            "timestamp": time.time(),
            "input_type": input_type,
            "stress_level": stress_level,
            "scores": normalized,
            "winner": max(normalized.keys(), key=lambda k: normalized[k])
        }
        
        self.competition_history.append(competition_result)
        
        # Sprawdź czy wystąpił konflikt (duża zmiana dominacji)
        if abs(max(normalized.values()) - min(normalized.values())) > 0.4:
            self.conflict_events += 1
            logger.info(f"🥊 Module conflict detected: {competition_result['winner']} dominates")
        
        return {module: stats["dominance"] for module, stats in self.modules.items()}

class PsycheVisualizer:
    """
    Wizualizer psychiki cyfrowej - generuje dane dla wykresów i animacji
    """
    
    def __init__(self):
        self.stress_history = deque(maxlen=200)      # 200 punktów = ~3.5 min przy 1Hz
        self.archetype_history = deque(maxlen=50)    # Historia zmian archetypów  
        self.memory_events = deque(maxlen=100)       # Wydarzenia pamięciowe
        self.consciousness_timeline = deque(maxlen=100)  # Timeline świadomości
        
    def add_stress_datapoint(self, cortisol: float, pfc_suppression: float, recovery_rate: float):
        """Dodaje punkt danych stresowych"""
        datapoint = {
            "timestamp": time.time(),
            "cortisol": cortisol,
            "pfc_suppression": pfc_suppression, 
            "recovery_rate": recovery_rate,
            "stress_index": (cortisol + pfc_suppression) / 2.0
        }
        self.stress_history.append(datapoint)
        
    def add_archetype_transition(self, old_archetype: str, new_archetype: str, trigger: str):
        """Rejestruje zmianę archetypu"""
        transition = {
            "timestamp": time.time(),
            "from": old_archetype,
            "to": new_archetype,
            "trigger": trigger,
            "stability_before": self._calculate_stability(),
            "stability_after": 0.0  # Będzie zaktualizowane później
        }
        self.archetype_history.append(transition)
        
    def add_memory_event(self, event_type: str, sense_atom_id: str, details: Dict):
        """Rejestruje wydarzenie pamięciowe"""
        event = {
            "timestamp": time.time(),
            "type": event_type,  # "consolidation", "reconsolidation", "decay"
            "atom_id": sense_atom_id,
            "details": details
        }
        self.memory_events.append(event)
        
    def add_consciousness_update(self, level: str, coherence: float, factors: Dict):
        """Aktualizuje timeline świadomości"""
        update = {
            "timestamp": time.time(),
            "consciousness_level": level,
            "system_coherence": coherence,
            "contributing_factors": factors
        }
        self.consciousness_timeline.append(update)
        
    def _calculate_stability(self) -> float:
        """Oblicza stabilność archetypalną na podstawie ostatnich zmian"""
        if len(self.archetype_history) < 2:
            return 1.0
            
        recent_transitions = list(self.archetype_history)[-5:]  # Last 5 transitions
        if len(recent_transitions) <= 1:
            return 1.0
            
        # Stabilność = 1.0 - (częstotliwość zmian)
        time_span = recent_transitions[-1]["timestamp"] - recent_transitions[0]["timestamp"]
        if time_span <= 0:
            return 1.0
            
        transition_rate = len(recent_transitions) / max(time_span, 1.0)
        stability = max(0.0, 1.0 - min(transition_rate * 10, 1.0))
        
        return stability
        
    def generate_heat_map_data(self) -> Dict[str, Any]:
        """Generuje dane dla heat mapy aktywności mózgu"""
        # Symulujemy aktywność różnych obszarów mózgu
        brain_regions = {
            "prefrontal_cortex": np.random.beta(2, 5),      # Zazwyczaj niska aktywność
            "limbic_system": np.random.beta(5, 2),          # Zazwyczaj wysoka aktywność  
            "brain_stem": np.random.beta(8, 2),             # Bardzo wysoka (podstawa życia)
            "hippocampus": np.random.beta(4, 4),            # Średnia (pamięć)
            "amygdala": np.random.beta(3, 3),               # Zmienna (emocje)
            "cerebellum": np.random.beta(6, 3)              # Wysoka (koordynacja)
        }
        
        return {
            "timestamp": time.time(),
            "regions": brain_regions,
            "overall_activity": np.mean(list(brain_regions.values()))
        }

class CalibrationDashboard:
    """
    Główny Dashboard Kalibracyjny - koordynuje wszystkie komponenty
    """
    
    def __init__(self):
        # Core components
        self.integration_hub = None
        self.nsf = None
        
        # Dashboard components
        self.module_competition = ModuleCompetitionEngine()
        self.psyche_visualizer = PsycheVisualizer()
        
        # Data storage
        self.metrics_history = deque(maxlen=1000)  # 1000 punktów historii
        self.current_metrics = DashboardMetrics(timestamp=time.time())
        
        # Threading
        self.is_running = False
        self.dashboard_thread = None
        self.websocket_server = None
        
        # WebSocket clients
        self.connected_clients = set()
        
        logger.info("🎯 Calibration Dashboard initialized")
        
    async def websocket_handler(self, websocket, path):
        """Obsługa połączeń WebSocket"""
        self.connected_clients.add(websocket)
        logger.info(f"📡 New client connected: {websocket.remote_address}")
        
        try:
            # Wyślij aktualne dane po połączeniu
            await self.send_initial_data(websocket)
            
            # Słuchaj wiadomości od klienta
            async for message in websocket:
                await self.handle_client_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info("📡 Client disconnected")
        finally:
            self.connected_clients.discard(websocket)
            
    async def send_initial_data(self, websocket):
        """Wysyła początkowe dane do nowego klienta"""
        init_data = {
            "type": "initial_data",
            "current_metrics": asdict(self.current_metrics),
            "stress_history": list(self.psyche_visualizer.stress_history)[-50:],  # Last 50 points
            "module_competition": self.module_competition.modules,
            "brain_activity": self.psyche_visualizer.generate_heat_map_data()
        }
        
        await websocket.send(json.dumps(init_data))
        
    async def handle_client_message(self, websocket, message):
        """Obsługuje wiadomości od klienta"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "trigger_stress":
                # Klient może triggerować stress event
                intensity = data.get("intensity", 0.5)
                if self.integration_hub:
                    self.integration_hub.simulate_stress_event(intensity)
                    
            elif message_type == "change_archetype":
                # Klient może wymuszać zmianę archetypu
                archetype_name = data.get("archetype", "hero")
                if self.integration_hub:
                    try:
                        archetype = ArchetypeCore(archetype_name.lower())
                        self.integration_hub.trigger_archetypal_shift(archetype)
                    except ValueError:
                        logger.warning(f"Unknown archetype: {archetype_name}")
                        
            elif message_type == "simulate_input":
                # Symulacja różnych typów input dla competition
                input_type = data.get("input_type", "mixed")
                stress = self.current_metrics.cortisol_level
                competition_result = self.module_competition.simulate_competition(input_type, stress)
                
                # Wyślij wyniki z powrotem
                response = {
                    "type": "competition_result",
                    "result": competition_result,
                    "input_type": input_type
                }
                await websocket.send(json.dumps(response))
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON received from client")
        except Exception as e:
            logger.error(f"Error handling client message: {e}")
            
    async def broadcast_metrics(self):
        """Wysyła metryki do wszystkich połączonych klientów"""
        if not self.connected_clients:
            return
            
        # Przygotuj dane do wysłania
        broadcast_data = {
            "type": "metrics_update",
            "timestamp": time.time(),
            "metrics": asdict(self.current_metrics),
            "stress_point": {
                "cortisol": self.current_metrics.cortisol_level,
                "pfc_suppression": self.current_metrics.pfc_suppression,
                "recovery_rate": self.current_metrics.recovery_rate
            },
            "competition": self.module_competition.modules,
            "brain_activity": self.psyche_visualizer.generate_heat_map_data(),
            "system_health": self._calculate_system_health()
        }
        
        # Wyślij do wszystkich klientów
        disconnected_clients = set()
        for client in self.connected_clients:
            try:
                await client.send(json.dumps(broadcast_data))
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
                
        # Usuń rozłączonych klientów
        self.connected_clients -= disconnected_clients
        
    def _calculate_system_health(self) -> Dict[str, Any]:
        """Oblicza ogólne zdrowie systemu"""
        # Health factors
        stress_health = 1.0 - self.current_metrics.cortisol_level
        coherence_health = self.current_metrics.system_coherence
        memory_health = min(1.0, self.current_metrics.processing_speed)
        
        overall_health = (stress_health + coherence_health + memory_health) / 3.0
        
        # Determine status
        if overall_health > 0.8:
            status = "EXCELLENT"
            status_color = "#00ff00"
        elif overall_health > 0.6:
            status = "GOOD" 
            status_color = "#ffff00"
        elif overall_health > 0.4:
            status = "FAIR"
            status_color = "#ff8800"
        else:
            status = "CRITICAL"
            status_color = "#ff0000"
            
        return {
            "overall_health": overall_health,
            "status": status,
            "status_color": status_color,
            "factors": {
                "stress": stress_health,
                "coherence": coherence_health,
                "memory": memory_health
            }
        }
        
    def start_dashboard(self, integration_hub=None):
        """Uruchamia dashboard kalibracyjny"""
        if self.is_running:
            logger.warning("Dashboard already running")
            return
            
        self.integration_hub = integration_hub
        if integration_hub and hasattr(integration_hub, 'nsf'):
            self.nsf = integration_hub.nsf
            
        self.is_running = True
        
        # Start monitoring thread
        self.dashboard_thread = threading.Thread(target=self._monitoring_loop)
        self.dashboard_thread.daemon = True
        self.dashboard_thread.start()
        
        # Start WebSocket server in asyncio
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        
        # WebSocket server
        start_server = websockets.serve(
            self.websocket_handler, 
            "localhost", 
            8765,
            ping_interval=20,
            ping_timeout=10
        )
        
        logger.info("🎯 Dashboard Kalibracyjny STARTED")
        logger.info("🌐 WebSocket server: ws://localhost:8765")
        logger.info("📊 Real-time monitoring active")
        
        # Run server
        try:
            loop.run_until_complete(start_server)
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("Dashboard stopped by user")
        finally:
            self.stop_dashboard()
            
    def stop_dashboard(self):
        """Zatrzymuje dashboard"""
        self.is_running = False
        
        if self.dashboard_thread:
            self.dashboard_thread.join(timeout=2.0)
            
        logger.info("🎯 Dashboard Kalibracyjny STOPPED")
        
    def _monitoring_loop(self):
        """Główna pętla monitoringu"""
        logger.info("📊 Monitoring loop started")
        
        while self.is_running:
            try:
                # Zbierz metryki z integration hub
                if self.integration_hub:
                    self._update_metrics_from_hub()
                    
                # Dodaj dane do wizualizera
                self._update_visualizer()
                
                # Symuluj rywalizację modułów
                self._update_module_competition()
                
                # Zapisz metryki w historii
                self.metrics_history.append(asdict(self.current_metrics))
                
                # Broadcast do klientów WebSocket (jeśli są)
                if self.connected_clients:
                    asyncio.create_task(self.broadcast_metrics())
                    
                # Loguj co 10 cykli
                if self.current_metrics.sekundnik_cycles % 10 == 0:
                    self._log_dashboard_status()
                    
                time.sleep(1.0)  # 1Hz monitoring
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(0.1)  # Short pause on error
                
    def _update_metrics_from_hub(self):
        """Aktualizuje metryki na podstawie danych z integration hub"""
        if not self.integration_hub:
            return
            
        try:
            status = self.integration_hub.get_system_status()
            metrics = status.get('metrics', {})
            
            # Update core metrics
            self.current_metrics.timestamp = time.time()
            self.current_metrics.sense_atoms_count = metrics.get('sense_atom_count', 0)
            self.current_metrics.sekundnik_cycles = status.get('cycle_count', 0)
            self.current_metrics.memory_reconsolidations = metrics.get('reconsolidation_count', 0)
            
            # Stress metrics
            old_cortisol = self.current_metrics.cortisol_level
            self.current_metrics.cortisol_level = metrics.get('cortisol_level', 0.0)
            self.current_metrics.pfc_suppression = metrics.get('pfc_suppression', 0.0)
            
            # Calculate recovery rate
            if old_cortisol > self.current_metrics.cortisol_level:
                self.current_metrics.recovery_rate = old_cortisol - self.current_metrics.cortisol_level
            else:
                self.current_metrics.recovery_rate = 0.0
                
            # Archetypal data
            # (W przyszłości - integration z rzeczywistymi danymi archetypu)
            
            # Network & consciousness
            self.current_metrics.network_contention = metrics.get('network_contention', 0.0)
            self.current_metrics.consciousness_level = status.get('consciousness_level', 'basic')
            self.current_metrics.system_state = status.get('system_state', 'standard')
            self.current_metrics.system_coherence = metrics.get('system_coherence', 0.0)
            
        except Exception as e:
            logger.error(f"Error updating metrics from hub: {e}")
            
    def _update_visualizer(self):
        """Aktualizuje dane dla wizualizera"""
        # Stress data
        self.psyche_visualizer.add_stress_datapoint(
            self.current_metrics.cortisol_level,
            self.current_metrics.pfc_suppression,
            self.current_metrics.recovery_rate
        )
        
        # Consciousness updates
        self.psyche_visualizer.add_consciousness_update(
            self.current_metrics.consciousness_level,
            self.current_metrics.system_coherence,
            {
                "stress_impact": self.current_metrics.cortisol_level,
                "network_load": self.current_metrics.network_contention,
                "memory_stability": 1.0 - self.current_metrics.recovery_rate
            }
        )
        
    def _update_module_competition(self):
        """Aktualizuje rywalizację modułów"""
        # Określ typ aktualnego przetwarzania na podstawie stanu
        if self.current_metrics.cortisol_level > 0.7:
            input_type = "emotional"  # High stress = emotional processing
        elif self.current_metrics.pfc_suppression < 0.3:
            input_type = "logical"    # Low PFC suppression = logical processing
        else:
            input_type = "mixed"      # Mixed processing
            
        # Uruchom competition
        competition_result = self.module_competition.simulate_competition(
            input_type, 
            self.current_metrics.cortisol_level
        )
        
        # Update metrics
        self.current_metrics.module_competition = competition_result
        
    def _log_dashboard_status(self):
        """Loguje status dashboard'u"""
        status_log = f"""
🎯 DASHBOARD STATUS (Cycle {self.current_metrics.sekundnik_cycles}):
├── Consciousness: {self.current_metrics.consciousness_level.upper()}
├── Stress: {self.current_metrics.cortisol_level:.2f} | PFC: {self.current_metrics.pfc_suppression:.2f}
├── Memory: {self.current_metrics.sense_atoms_count} atoms | {self.current_metrics.memory_reconsolidations} recons
├── Modules: NSF:{self.current_metrics.module_competition.get('NSF', 0):.2f} 
│            Logic:{self.current_metrics.module_competition.get('LogicEngine', 0):.2f}
│            Arch:{self.current_metrics.module_competition.get('ArchetypalCore', 0):.2f}
└── Health: {self._calculate_system_health()['status']} ({self._calculate_system_health()['overall_health']:.2f})
        """
        logger.info(status_log)

def main():
    """Demo dashboard'u kalibracyjnego"""
    print("🎯 CALIBRATION DASHBOARD - Demo Mode")
    print("=" * 50)
    
    if not NSF_AVAILABLE:
        print("❌ NSF modules not available for dashboard")
        return
        
    try:
        # Initialize components
        dashboard = CalibrationDashboard()
        
        # Opcjonalnie - uruchom z integration hub
        print("🔄 Starting with integration hub...")
        integration_hub = MIGI7G_IntegrationHub()
        integration_hub.start_integrated_processing()
        
        print("🎯 Starting Calibration Dashboard...")
        print("🌐 Dashboard will be available at: ws://localhost:8765")
        print("📊 Press Ctrl+C to stop")
        
        # Start dashboard (blocking)
        dashboard.start_dashboard(integration_hub)
        
    except KeyboardInterrupt:
        print("\n⏹️ Stopping dashboard...")
    except Exception as e:
        print(f"💥 Dashboard error: {e}")
    finally:
        print("👋 Dashboard stopped")

if __name__ == "__main__":
    main()