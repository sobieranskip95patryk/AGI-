# telemetry_ws.py
"""
WebSocket Telemetry Server dla Dashboard Kalibracyjny NSF + MIGI_7G
Udostępnia real-time stream metryk świadomości cyfrowej
"""

import asyncio
import json
import time
import uuid
import websockets
import random
import math
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from save_snapshot import save_snapshot

# Konfiguracja
PORT = 8765
HOST = "0.0.0.0"
UPDATE_INTERVAL = 0.25  # 250ms dla płynnej animacji

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BrainLayer:
    name: str
    coherence: float
    load: int
    entropy: float
    activation: float = 0.0

@dataclass
class StressMetrics:
    cortisol: float
    sympathetic: float
    parasympathetic: float
    regulation_index: float

@dataclass
class ArchetypeState:
    current: str
    stability: float
    transition_probability: float
    previous: Optional[str] = None
    transition_time: Optional[float] = None

@dataclass
class ModuleStatus:
    name: str
    influence: float
    error_rate: float
    health: str
    response_time: float = 0.0

@dataclass
class SystemHealth:
    overall_score: float
    anomalies: List[Dict[str, Any]]
    coherence_integrity: float
    masking_risk: float
    rigidity_risk: float

class TelemetryGenerator:
    """Generator metryk dla symulacji lub rzeczywistych danych NSF"""
    
    def __init__(self, mode="demo"):
        self.mode = mode  # "demo", "stub", "live"
        self.time_offset = time.time()
        self.stress_phase = 0
        self.archetype_timer = 0
        self.current_archetype = "Everyman"
        self.available_archetypes = ["Hero", "Sage", "Everyman", "Explorer", "Innocent", "Rebel", "Magician"]
        
        # Kalibracja metryk
        self.stress_baseline = 0.3
        self.coherence_baseline = 0.7
        self.module_competition_cycle = 0
        
        # Śledzenie anomalii
        self.anomaly_history = []
        self.last_spike_time = 0
        
    def noise(self, mean: float, spread: float) -> float:
        """Generuje szum gaussian"""
        return mean + (random.random() * 2 - 1) * spread
    
    def clamp(self, value: float, min_val: float, max_val: float) -> float:
        """Ogranicza wartość do zakresu"""
        return max(min_val, min(max_val, value))
    
    def generate_brain_layers(self, t: float) -> List[BrainLayer]:
        """Generuje dane warstw mózgu z realistycznymi interakcjami"""
        layers = []
        
        # Reptilian - podstawowe funkcje, stabilny
        reptilian_coherence = self.clamp(self.noise(0.8, 0.1), 0.0, 1.0)
        reptilian_load = int(self.clamp(self.noise(40, 10), 0, 100))
        reptilian_entropy = self.clamp(self.noise(0.2, 0.05), 0.0, 1.0)
        
        # Limbic - emocje, reaguje na stres
        stress_impact = math.sin(self.stress_phase) * 0.3
        limbic_coherence = self.clamp(self.noise(0.6 - stress_impact, 0.15), 0.0, 1.0)
        limbic_load = int(self.clamp(self.noise(60 + stress_impact * 30, 15), 0, 100))
        limbic_entropy = self.clamp(self.noise(0.35 + stress_impact * 0.2, 0.1), 0.0, 1.0)
        
        # Neocortex - logika, stabilizuje się pod presją
        neocortex_coherence = self.clamp(self.noise(0.75 + stress_impact * 0.1, 0.12), 0.0, 1.0)
        neocortex_load = int(self.clamp(self.noise(70 + stress_impact * 20, 12), 0, 100))
        neocortex_entropy = self.clamp(self.noise(0.25 - stress_impact * 0.1, 0.08), 0.0, 1.0)
        
        # Meta - świadomość, najwyższy poziom
        meta_coherence = self.clamp(self.noise(0.85 - stress_impact * 0.05, 0.1), 0.0, 1.0)
        meta_load = int(self.clamp(self.noise(55 + stress_impact * 15, 10), 0, 100))
        meta_entropy = self.clamp(self.noise(0.15 + stress_impact * 0.05, 0.05), 0.0, 1.0)
        
        layers = [
            BrainLayer("Reptilian", reptilian_coherence, reptilian_load, reptilian_entropy),
            BrainLayer("Limbic", limbic_coherence, limbic_load, limbic_entropy),
            BrainLayer("Neocortex", neocortex_coherence, neocortex_load, neocortex_entropy),
            BrainLayer("Meta", meta_coherence, meta_load, meta_entropy)
        ]
        
        return layers
    
    def generate_stress_metrics(self, t: float) -> StressMetrics:
        """Generuje realistyczne metryki stresu"""
        base_stress = math.sin(self.stress_phase) * 0.2 + self.stress_baseline
        
        cortisol = self.clamp(self.noise(base_stress, 0.15), 0.0, 1.0)
        sympathetic = self.clamp(self.noise(base_stress + 0.1, 0.2), 0.0, 1.0)
        parasympathetic = self.clamp(self.noise(0.6 - base_stress * 0.5, 0.15), 0.0, 1.0)
        
        # Indeks regulacji - parasympathetic vs sympathetic
        regulation_index = parasympathetic / (sympathetic + 0.01)
        
        return StressMetrics(cortisol, sympathetic, parasympathetic, regulation_index)
    
    def generate_archetype_state(self, t: float) -> ArchetypeState:
        """Generuje stan archetypu z przejściami"""
        self.archetype_timer += UPDATE_INTERVAL
        
        # Przejście co 15-30 sekund
        if self.archetype_timer > random.uniform(15, 30):
            previous = self.current_archetype
            self.current_archetype = random.choice(
                [arch for arch in self.available_archetypes if arch != self.current_archetype]
            )
            self.archetype_timer = 0
            transition_time = time.time()
            logger.info(f"🔄 Archetype transition: {previous} → {self.current_archetype}")
        else:
            previous = None
            transition_time = None
        
        # Stabilność zależy od czasu od ostatniego przejścia
        stability = min(1.0, self.archetype_timer / 10.0)
        transition_probability = max(0.0, (self.archetype_timer - 10) / 20.0)
        
        return ArchetypeState(
            self.current_archetype,
            stability,
            transition_probability,
            previous,
            transition_time
        )
    
    def generate_module_status(self, t: float) -> List[ModuleStatus]:
        """Generuje status modułów z konkurencją"""
        self.module_competition_cycle += UPDATE_INTERVAL
        
        # Cykliczna konkurencja modułów
        cycle_phase = self.module_competition_cycle / 20.0  # 20s cykl
        
        nsf_influence = self.clamp(self.noise(0.4 + math.sin(cycle_phase) * 0.2, 0.1), 0.0, 1.0)
        logic_influence = self.clamp(self.noise(0.35 + math.cos(cycle_phase + 1) * 0.2, 0.1), 0.0, 1.0)
        archetype_influence = self.clamp(self.noise(0.25 + math.sin(cycle_phase + 2) * 0.15, 0.1), 0.0, 1.0)
        
        # Normalizacja do sumy ≤ 1
        total_influence = nsf_influence + logic_influence + archetype_influence
        if total_influence > 1.0:
            nsf_influence /= total_influence
            logic_influence /= total_influence
            archetype_influence /= total_influence
        
        modules = [
            ModuleStatus("NSF", nsf_influence, self.clamp(self.noise(0.05, 0.03), 0.0, 1.0), "OK"),
            ModuleStatus("LogicEngine", logic_influence, self.clamp(self.noise(0.04, 0.02), 0.0, 1.0), "OK"),
            ModuleStatus("ArchetypalCore", archetype_influence, self.clamp(self.noise(0.03, 0.02), 0.0, 1.0), "OK")
        ]
        
        # Symulacja degradacji
        for module in modules:
            if module.error_rate > 0.08:
                module.health = "DEGRADED"
            elif module.error_rate > 0.12:
                module.health = "FAIL"
        
        return modules
    
    def detect_system_anomalies(self, stress: StressMetrics, layers: List[BrainLayer], 
                               archetype: ArchetypeState) -> List[Dict[str, Any]]:
        """Wykrywa anomalie w systemie"""
        anomalies = []
        current_time = time.time()
        
        # Spike stresu
        if stress.cortisol > 0.8 and (current_time - self.last_spike_time) > 30:
            anomalies.append({
                "type": "stress_spike",
                "severity": "high",
                "value": stress.cortisol,
                "timestamp": current_time
            })
            self.last_spike_time = current_time
        
        # Niska koherencja
        avg_coherence = sum(layer.coherence for layer in layers) / len(layers)
        if avg_coherence < 0.3:
            anomalies.append({
                "type": "low_coherence",
                "severity": "medium",
                "value": avg_coherence,
                "timestamp": current_time
            })
        
        # Sztywność archetypowa
        if archetype.stability > 0.9 and archetype.transition_probability < 0.05:
            anomalies.append({
                "type": "archetype_rigidity",
                "severity": "medium",
                "archetype": archetype.current,
                "timestamp": current_time
            })
        
        return anomalies
    
    def calculate_system_health(self, stress: StressMetrics, layers: List[BrainLayer],
                               modules: List[ModuleStatus], anomalies: List[Dict]) -> SystemHealth:
        """Oblicza ogólne zdrowie systemu"""
        
        # Średnia koherencja warstw
        avg_coherence = sum(layer.coherence for layer in layers) / len(layers)
        
        # Współczynnik modułów
        healthy_modules = sum(1 for m in modules if m.health == "OK")
        module_factor = healthy_modules / len(modules)
        
        # Wykrywanie fałszywej koherencji (masking)
        masking_risk = 0.0
        if avg_coherence > 0.7 and stress.cortisol > 0.6:
            masking_risk = (avg_coherence * stress.cortisol) - 0.42
        
        # Wykrywanie sztywności
        rigidity_risk = 0.0  # Będzie obliczane na podstawie archetypu
        
        # Ogólny wynik zdrowia
        overall_score = (
            0.4 * avg_coherence +
            0.3 * (1.0 - stress.cortisol) +
            0.2 * module_factor +
            0.1 * stress.regulation_index
        ) - 0.2 * masking_risk
        
        overall_score = self.clamp(overall_score, 0.0, 1.0)
        
        return SystemHealth(
            overall_score,
            anomalies,
            avg_coherence,
            max(0.0, masking_risk),
            rigidity_risk
        )
    
    def generate_telemetry_packet(self) -> Dict[str, Any]:
        """Generuje kompletny pakiet telemetrii"""
        current_time = time.time()
        t = current_time - self.time_offset
        
        # Aktualizacja fazy stresu
        self.stress_phase += UPDATE_INTERVAL * 0.1
        
        # Generowanie danych
        layers = self.generate_brain_layers(t)
        stress = self.generate_stress_metrics(t)
        archetype = self.generate_archetype_state(t)
        modules = self.generate_module_status(t)
        anomalies = self.detect_system_anomalies(stress, layers, archetype)
        health = self.calculate_system_health(stress, layers, modules, anomalies)
        
        # Konwersja do słowników
        packet = {
            "metadata": {
                "trace_id": str(uuid.uuid4()),
                "timestamp": current_time,
                "timestamp_iso": datetime.now().isoformat(),
                "mode": self.mode,
                "version": "1.0"
            },
            "brain_layers": [asdict(layer) for layer in layers],
            "stress": asdict(stress),
            "archetype": asdict(archetype),
            "modules": [asdict(module) for module in modules],
            "health": asdict(health)
        }
        
        return packet

class TelemetryServer:
    """WebSocket server dla telemetrii"""
    
    def __init__(self, port=PORT, host=HOST):
        self.port = port
        self.host = host
        self.generator = TelemetryGenerator("demo")
        self.clients = set()
        self.running = False
        self.snapshot_interval = 10.0  # Snapshot co 10 sekund
        self.last_snapshot = time.time()
        
    async def register_client(self, websocket):
        """Rejestruje nowego klienta"""
        self.clients.add(websocket)
        client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"🔌 Client connected: {client_id} (total: {len(self.clients)})")
        
    async def unregister_client(self, websocket):
        """Wyrejestruje klienta"""
        self.clients.discard(websocket)
        logger.info(f"🔌 Client disconnected (total: {len(self.clients)})")
        
    async def broadcast_telemetry(self, packet: Dict[str, Any]):
        """Wysyła telemetrię do wszystkich klientów"""
        if not self.clients:
            return
            
        message = json.dumps(packet)
        disconnected = set()
        
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
            except Exception as e:
                logger.error(f"Error sending to client: {e}")
                disconnected.add(client)
        
        # Usuń rozłączonych klientów
        for client in disconnected:
            await self.unregister_client(client)
    
    async def save_periodic_snapshot(self, packet: Dict[str, Any]):
        """Zapisuje okresoweSnapShoty"""
        current_time = time.time()
        if current_time - self.last_snapshot >= self.snapshot_interval:
            try:
                # Przygotowanie stanu do snapshotu
                state = {
                    "stress_level": packet["stress"]["cortisol"],
                    "cortisol_ppm": packet["stress"]["cortisol"] * 20,  # Skalowanie
                    "coherence": packet["health"]["coherence_integrity"],
                    "active_archetype": packet["archetype"]["current"],
                    "archetype_stability": packet["archetype"]["stability"],
                    "brain_layers": {
                        layer["name"]: {
                            "coherence": layer["coherence"],
                            "load": layer["load"],
                            "entropy": layer["entropy"]
                        } for layer in packet["brain_layers"]
                    },
                    "module_health": {
                        module["name"]: module["health"] for module in packet["modules"]
                    },
                    "system_health": packet["health"]["overall_score"],
                    "anomalies": packet["health"]["anomalies"],
                    "regulation_index": packet["stress"]["regulation_index"]
                }
                
                snapshot_path = save_snapshot(state, "telemetry_server")
                logger.info(f"📸 Snapshot saved: {snapshot_path}")
                self.last_snapshot = current_time
                
            except Exception as e:
                logger.error(f"Error saving snapshot: {e}")
    
    async def telemetry_producer(self, websocket, path):
        """Handler dla połączeń WebSocket"""
        await self.register_client(websocket)
        
        try:
            # Wysyłaj telemetrię dopóki klient jest połączony
            while True:
                packet = self.generator.generate_telemetry_packet()
                await self.broadcast_telemetry(packet)
                await self.save_periodic_snapshot(packet)
                await asyncio.sleep(UPDATE_INTERVAL)
                
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            logger.error(f"Error in telemetry producer: {e}")
        finally:
            await self.unregister_client(websocket)
    
    async def start_server(self):
        """Uruchamia serwer WebSocket"""
        self.running = True
        logger.info(f"🚀 Starting Telemetry WebSocket Server on {self.host}:{self.port}")
        logger.info(f"📊 Mode: {self.generator.mode}, Update interval: {UPDATE_INTERVAL}s")
        
        async with websockets.serve(self.telemetry_producer, self.host, self.port):
            logger.info("✅ Telemetry server is running...")
            logger.info("Connect your dashboard to: ws://localhost:8765")
            await asyncio.Future()  # Run forever
    
    def stop_server(self):
        """Zatrzymuje serwer"""
        self.running = False
        logger.info("🛑 Telemetry server stopped")

# Główna funkcja
async def main():
    server = TelemetryServer()
    try:
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🧠 NSF + MIGI_7G Telemetry WebSocket Server")
    print("=" * 60)
    print(f"Port: {PORT}")
    print(f"Update rate: {UPDATE_INTERVAL}s ({1/UPDATE_INTERVAL:.1f} Hz)")
    print("=" * 60)
    print("Ctrl+C to stop")
    print("=" * 60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")