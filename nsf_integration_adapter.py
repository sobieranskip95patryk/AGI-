# nsf_integration_adapter.py
"""
Adapter do integracji Dashboard Kalibracyjny z rzeczywistymi modułami NSF + MIGI_7G
Obsługuje fallback: demo → stub → live NSF
"""

import json
import time
import logging
import asyncio
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from dataclasses import dataclass
import importlib.util
import sys

# Import schemy walidacji
SCHEMA_PATH = Path(__file__).parent / "schemas" / "metrics.json"

logger = logging.getLogger(__name__)

@dataclass
class IntegrationConfig:
    """Konfiguracja integracji z modułami NSF"""
    mode: str = "demo"  # demo, stub, live
    nsf_module_path: Optional[str] = None
    logic_engine_path: Optional[str] = None
    archetype_core_path: Optional[str] = None
    fallback_on_error: bool = True
    health_check_interval: float = 5.0
    max_retries: int = 3

class NSFIntegrationAdapter:
    """Główny adapter do integracji z modułami NSF"""
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.mode = config.mode
        self.modules = {}
        self.last_health_check = 0
        self.error_counts = {}
        self.fallback_mode = False
        
        # Ładowanie schemy walidacji
        self.schema = self._load_schema()
        
    def _load_schema(self) -> Dict[str, Any]:
        """Ładuje schemat JSON dla walidacji"""
        try:
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load schema: {e}")
            return {}
    
    def _validate_metrics(self, data: Dict[str, Any]) -> bool:
        """Waliduje dane według schematu JSON"""
        try:
            # Podstawowa walidacja struktury
            required_fields = ["metadata", "brain_layers", "stress", "archetype", "modules", "health"]
            for field in required_fields:
                if field not in data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Walidacja zakresów
            if not (0 <= data["stress"]["cortisol"] <= 1):
                logger.error(f"Cortisol out of range: {data['stress']['cortisol']}")
                return False
                
            if not (0 <= data["health"]["overall_score"] <= 1):
                logger.error(f"Health score out of range: {data['health']['overall_score']}")
                return False
            
            # Walidacja brain_layers
            if len(data["brain_layers"]) != 4:
                logger.error(f"Expected 4 brain layers, got {len(data['brain_layers'])}")
                return False
            
            expected_layers = {"Reptilian", "Limbic", "Neocortex", "Meta"}
            actual_layers = {layer["name"] for layer in data["brain_layers"]}
            if actual_layers != expected_layers:
                logger.error(f"Invalid brain layers: {actual_layers}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
    
    async def initialize_modules(self):
        """Inicjalizuje moduły zgodnie z trybem"""
        logger.info(f"🚀 Initializing NSF integration in {self.mode} mode")
        
        if self.mode == "demo":
            await self._init_demo_mode()
        elif self.mode == "stub":
            await self._init_stub_mode()
        elif self.mode == "live":
            await self._init_live_mode()
        else:
            logger.error(f"Unknown mode: {self.mode}")
            self.mode = "demo"
            await self._init_demo_mode()
    
    async def _init_demo_mode(self):
        """Inicjalizacja trybu demo (symulowane dane)"""
        logger.info("📊 Demo mode: Using simulated data")
        self.modules = {
            "NSF": DemoNSFModule(),
            "LogicEngine": DemoLogicEngineModule(),
            "ArchetypalCore": DemoArchetypeModule()
        }
    
    async def _init_stub_mode(self):
        """Inicjalizacja trybu stub (częściowe dane rzeczywiste)"""
        logger.info("🔌 Stub mode: Using partial real data with fallbacks")
        
        # Próba załadowania rzeczywistych modułów z fallback na stub
        self.modules = {}
        
        # NSF Module
        try:
            nsf_module = self._try_load_module("NSF", self.config.nsf_module_path)
            self.modules["NSF"] = nsf_module or StubNSFModule()
        except Exception as e:
            logger.warning(f"NSF module failed, using stub: {e}")
            self.modules["NSF"] = StubNSFModule()
        
        # Logic Engine
        try:
            logic_module = self._try_load_module("LogicEngine", self.config.logic_engine_path)
            self.modules["LogicEngine"] = logic_module or StubLogicEngineModule()
        except Exception as e:
            logger.warning(f"Logic Engine failed, using stub: {e}")
            self.modules["LogicEngine"] = StubLogicEngineModule()
        
        # Archetypal Core
        try:
            archetype_module = self._try_load_module("ArchetypalCore", self.config.archetype_core_path)
            self.modules["ArchetypalCore"] = archetype_module or StubArchetypeModule()
        except Exception as e:
            logger.warning(f"Archetype Core failed, using stub: {e}")
            self.modules["ArchetypalCore"] = StubArchetypeModule()
    
    async def _init_live_mode(self):
        """Inicjalizacja trybu live (pełne dane rzeczywiste)"""
        logger.info("🔥 Live mode: Using real NSF modules")
        
        try:
            # Próba załadowania wszystkich rzeczywistych modułów
            nsf_module = self._try_load_real_nsf()
            logic_module = self._try_load_real_logic_engine()
            archetype_module = self._try_load_real_archetype_core()
            
            if not all([nsf_module, logic_module, archetype_module]):
                if self.config.fallback_on_error:
                    logger.warning("⚠️ Some modules failed, falling back to stub mode")
                    self.mode = "stub"
                    await self._init_stub_mode()
                    return
                else:
                    raise Exception("Required modules failed to load")
            
            self.modules = {
                "NSF": nsf_module,
                "LogicEngine": logic_module,
                "ArchetypalCore": archetype_module
            }
            
        except Exception as e:
            logger.error(f"Live mode initialization failed: {e}")
            if self.config.fallback_on_error:
                logger.info("🔄 Falling back to demo mode")
                self.mode = "demo"
                await self._init_demo_mode()
            else:
                raise
    
    def _try_load_module(self, module_name: str, module_path: Optional[str]):
        """Próbuje załadować moduł z podanej ścieżki"""
        if not module_path:
            return None
            
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return getattr(module, f"{module_name}Module", None)
        except Exception as e:
            logger.error(f"Failed to load {module_name} from {module_path}: {e}")
            
        return None
    
    def _try_load_real_nsf(self):
        """Próbuje załadować rzeczywisty moduł NSF"""
        try:
            # Próba importu z CORE_CONSCIOUSNESS
            sys.path.append(str(Path(__file__).parent / "CORE_CONSCIOUSNESS"))
            from nsf_core import NSFCore
            return NSFCore()
        except ImportError:
            logger.warning("Real NSF module not available")
            return None
        except Exception as e:
            logger.error(f"Error loading real NSF: {e}")
            return None
    
    def _try_load_real_logic_engine(self):
        """Próbuje załadować rzeczywisty Logic Engine"""
        try:
            sys.path.append(str(Path(__file__).parent / "LOGIC_ENGINE"))
            from logic_core import LogicEngineCore
            return LogicEngineCore()
        except ImportError:
            logger.warning("Real Logic Engine not available")
            return None
        except Exception as e:
            logger.error(f"Error loading real Logic Engine: {e}")
            return None
    
    def _try_load_real_archetype_core(self):
        """Próbuje załadować rzeczywisty Archetypal Core"""
        try:
            sys.path.append(str(Path(__file__).parent))
            from memory.structures.AbsolutMemoryCore import ArchetypalCore
            return ArchetypalCore()
        except ImportError:
            logger.warning("Real Archetypal Core not available")
            return None
        except Exception as e:
            logger.error(f"Error loading real Archetypal Core: {e}")
            return None
    
    async def get_telemetry_data(self) -> Dict[str, Any]:
        """Pobiera dane telemetryczne z aktywnych modułów"""
        try:
            # Health check co X sekund
            await self._periodic_health_check()
            
            # Zbieranie danych z modułów
            brain_data = await self._collect_brain_layer_data()
            stress_data = await self._collect_stress_data()
            archetype_data = await self._collect_archetype_data()
            module_data = await self._collect_module_status_data()
            health_data = await self._calculate_system_health(brain_data, stress_data, module_data)
            
            # Budowanie pakietu telemetrii
            telemetry_packet = {
                "metadata": {
                    "trace_id": self._generate_trace_id(),
                    "timestamp": time.time(),
                    "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "mode": self.mode,
                    "version": "1.0"
                },
                "brain_layers": brain_data,
                "stress": stress_data,
                "archetype": archetype_data,
                "modules": module_data,
                "health": health_data
            }
            
            # Walidacja przed zwróceniem
            if not self._validate_metrics(telemetry_packet):
                logger.error("Telemetry data validation failed")
                if self.config.fallback_on_error:
                    return await self._get_fallback_data()
                else:
                    raise ValueError("Invalid telemetry data")
            
            return telemetry_packet
            
        except Exception as e:
            logger.error(f"Error collecting telemetry: {e}")
            if self.config.fallback_on_error:
                return await self._get_fallback_data()
            else:
                raise
    
    async def _periodic_health_check(self):
        """Okresowe sprawdzanie zdrowia modułów"""
        current_time = time.time()
        if (current_time - self.last_health_check) < self.config.health_check_interval:
            return
        
        logger.debug("🔍 Performing module health check...")
        
        for name, module in self.modules.items():
            try:
                health = await self._check_module_health(module)
                if health != "OK":
                    self.error_counts[name] = self.error_counts.get(name, 0) + 1
                    logger.warning(f"Module {name} health: {health}")
                else:
                    self.error_counts[name] = 0
                    
            except Exception as e:
                logger.error(f"Health check failed for {name}: {e}")
                self.error_counts[name] = self.error_counts.get(name, 0) + 1
        
        self.last_health_check = current_time
    
    async def _check_module_health(self, module) -> str:
        """Sprawdza zdrowie pojedynczego modułu"""
        try:
            if hasattr(module, 'health_check'):
                return await module.health_check()
            elif hasattr(module, 'is_healthy'):
                return "OK" if await module.is_healthy() else "DEGRADED"
            else:
                return "OK"  # Assume OK if no health check method
        except Exception:
            return "FAIL"
    
    async def _collect_brain_layer_data(self) -> List[Dict[str, Any]]:
        """Zbiera dane warstw mózgu"""
        layers = []
        layer_names = ["Reptilian", "Limbic", "Neocortex", "Meta"]
        
        for name in layer_names:
            try:
                if "NSF" in self.modules:
                    layer_data = await self.modules["NSF"].get_brain_layer_state(name)
                else:
                    layer_data = self._get_demo_layer_data(name)
                
                layers.append({
                    "name": name,
                    "coherence": layer_data.get("coherence", 0.7),
                    "load": layer_data.get("load", 50),
                    "entropy": layer_data.get("entropy", 0.3),
                    "activation": layer_data.get("activation", 0.5)
                })
                
            except Exception as e:
                logger.error(f"Error collecting {name} layer data: {e}")
                layers.append(self._get_demo_layer_data(name))
        
        return layers
    
    async def _collect_stress_data(self) -> Dict[str, float]:
        """Zbiera dane o stresie"""
        try:
            if "NSF" in self.modules:
                return await self.modules["NSF"].get_stress_metrics()
            else:
                return self._get_demo_stress_data()
        except Exception as e:
            logger.error(f"Error collecting stress data: {e}")
            return self._get_demo_stress_data()
    
    async def _collect_archetype_data(self) -> Dict[str, Any]:
        """Zbiera dane o archetypie"""
        try:
            if "ArchetypalCore" in self.modules:
                return await self.modules["ArchetypalCore"].get_current_state()
            else:
                return self._get_demo_archetype_data()
        except Exception as e:
            logger.error(f"Error collecting archetype data: {e}")
            return self._get_demo_archetype_data()
    
    async def _collect_module_status_data(self) -> List[Dict[str, Any]]:
        """Zbiera dane statusu modułów"""
        module_status = []
        
        for name, module in self.modules.items():
            try:
                if hasattr(module, 'get_status'):
                    status = await module.get_status()
                else:
                    status = {
                        "influence": 0.33,
                        "error_rate": 0.05,
                        "health": "OK",
                        "response_time": 0.1
                    }
                
                module_status.append({
                    "name": name,
                    "influence": status.get("influence", 0.33),
                    "error_rate": status.get("error_rate", 0.05),
                    "health": status.get("health", "OK"),
                    "response_time": status.get("response_time", 0.1)
                })
                
            except Exception as e:
                logger.error(f"Error collecting {name} status: {e}")
                module_status.append({
                    "name": name,
                    "influence": 0.1,
                    "error_rate": 0.2,
                    "health": "DEGRADED",
                    "response_time": 1.0
                })
        
        return module_status
    
    async def _calculate_system_health(self, brain_data, stress_data, module_data) -> Dict[str, Any]:
        """Oblicza ogólne zdrowie systemu"""
        try:
            # Średnia koherencja
            avg_coherence = sum(layer["coherence"] for layer in brain_data) / len(brain_data)
            
            # Współczynnik zdrowia modułów
            healthy_modules = sum(1 for m in module_data if m["health"] == "OK")
            module_health_factor = healthy_modules / len(module_data)
            
            # Wykrywanie anomalii
            anomalies = []
            masking_risk = 0.0
            rigidity_risk = 0.0
            
            # Fałszywa koherencja
            if avg_coherence > 0.7 and stress_data["cortisol"] > 0.6:
                masking_risk = (avg_coherence * stress_data["cortisol"]) - 0.42
                anomalies.append({
                    "type": "masking_detected",
                    "severity": "medium",
                    "timestamp": time.time(),
                    "value": masking_risk
                })
            
            # Ogólny wynik zdrowia
            overall_score = (
                0.4 * avg_coherence +
                0.3 * (1.0 - stress_data["cortisol"]) +
                0.2 * module_health_factor +
                0.1 * stress_data["regulation_index"]
            ) - 0.2 * max(0, masking_risk)
            
            overall_score = max(0.0, min(1.0, overall_score))
            
            return {
                "overall_score": overall_score,
                "anomalies": anomalies,
                "coherence_integrity": avg_coherence,
                "masking_risk": max(0.0, masking_risk),
                "rigidity_risk": rigidity_risk
            }
            
        except Exception as e:
            logger.error(f"Error calculating system health: {e}")
            return {
                "overall_score": 0.5,
                "anomalies": [{"type": "calculation_error", "severity": "high", "timestamp": time.time()}],
                "coherence_integrity": 0.5,
                "masking_risk": 0.0,
                "rigidity_risk": 0.0
            }
    
    def _generate_trace_id(self) -> str:
        """Generuje UUID dla śledzenia"""
        import uuid
        return str(uuid.uuid4())
    
    # Demo data generators (fallback)
    def _get_demo_layer_data(self, layer_name: str) -> Dict[str, float]:
        """Generuje demo dane dla warstwy mózgu"""
        import random
        base_values = {
            "Reptilian": {"coherence": 0.8, "load": 40, "entropy": 0.2},
            "Limbic": {"coherence": 0.6, "load": 60, "entropy": 0.35},
            "Neocortex": {"coherence": 0.75, "load": 70, "entropy": 0.25},
            "Meta": {"coherence": 0.85, "load": 55, "entropy": 0.15}
        }
        
        base = base_values.get(layer_name, {"coherence": 0.7, "load": 50, "entropy": 0.3})
        return {
            "coherence": max(0, min(1, base["coherence"] + random.uniform(-0.1, 0.1))),
            "load": max(0, min(100, base["load"] + random.randint(-10, 10))),
            "entropy": max(0, min(1, base["entropy"] + random.uniform(-0.05, 0.05))),
            "activation": random.uniform(0.3, 0.8)
        }
    
    def _get_demo_stress_data(self) -> Dict[str, float]:
        """Generuje demo dane stresu"""
        import random
        cortisol = random.uniform(0.2, 0.7)
        sympathetic = random.uniform(0.3, 0.8)
        parasympathetic = random.uniform(0.4, 0.7)
        
        return {
            "cortisol": cortisol,
            "sympathetic": sympathetic,
            "parasympathetic": parasympathetic,
            "regulation_index": parasympathetic / (sympathetic + 0.01)
        }
    
    def _get_demo_archetype_data(self) -> Dict[str, Any]:
        """Generuje demo dane archetypu"""
        import random
        archetypes = ["Hero", "Sage", "Everyman", "Explorer"]
        return {
            "current": random.choice(archetypes),
            "stability": random.uniform(0.5, 0.9),
            "transition_probability": random.uniform(0.1, 0.3),
            "previous": None,
            "transition_time": None
        }
    
    async def _get_fallback_data(self) -> Dict[str, Any]:
        """Generuje podstawowe dane fallback"""
        from telemetry_ws import TelemetryGenerator
        generator = TelemetryGenerator("demo")
        return generator.generate_telemetry_packet()

# Klasy stub modułów
class DemoNSFModule:
    """Demo implementacja modułu NSF"""
    async def get_brain_layer_state(self, layer_name: str) -> Dict[str, float]:
        import random
        return {
            "coherence": random.uniform(0.5, 0.9),
            "load": random.randint(30, 80),
            "entropy": random.uniform(0.1, 0.4),
            "activation": random.uniform(0.3, 0.8)
        }
    
    async def get_stress_metrics(self) -> Dict[str, float]:
        import random
        return {
            "cortisol": random.uniform(0.2, 0.6),
            "sympathetic": random.uniform(0.3, 0.7),
            "parasympathetic": random.uniform(0.4, 0.8),
            "regulation_index": random.uniform(0.5, 1.5)
        }
    
    async def health_check(self) -> str:
        return "OK"

class DemoLogicEngineModule:
    """Demo implementacja Logic Engine"""
    async def get_status(self) -> Dict[str, Any]:
        import random
        return {
            "influence": random.uniform(0.2, 0.5),
            "error_rate": random.uniform(0.02, 0.08),
            "health": "OK",
            "response_time": random.uniform(0.05, 0.2)
        }

class DemoArchetypeModule:
    """Demo implementacja Archetypal Core"""
    def __init__(self):
        self.current_archetype = "Everyman"
        self.last_change = time.time()
    
    async def get_current_state(self) -> Dict[str, Any]:
        import random
        
        # Symulacja przejść archetypowych
        if (time.time() - self.last_change) > 20:  # Co 20 sekund
            archetypes = ["Hero", "Sage", "Everyman", "Explorer"]
            self.current_archetype = random.choice(archetypes)
            self.last_change = time.time()
        
        return {
            "current": self.current_archetype,
            "stability": random.uniform(0.6, 0.9),
            "transition_probability": random.uniform(0.1, 0.3),
            "previous": None,
            "transition_time": None
        }

# Stub modules (częściowe dane rzeczywiste)
class StubNSFModule(DemoNSFModule):
    """Stub NSF z częściowymi danymi rzeczywistymi"""
    pass

class StubLogicEngineModule(DemoLogicEngineModule):
    """Stub Logic Engine z częściowymi danymi rzeczywistymi"""
    pass

class StubArchetypeModule(DemoArchetypeModule):
    """Stub Archetypal Core z częściowymi danymi rzeczywistymi"""
    pass

# Factory function
def create_integration_adapter(mode: str = "demo") -> NSFIntegrationAdapter:
    """Factory do tworzenia adaptera integracji"""
    config = IntegrationConfig(
        mode=mode,
        fallback_on_error=True,
        health_check_interval=5.0
    )
    
    return NSFIntegrationAdapter(config)

# Przykład użycia
if __name__ == "__main__":
    async def test_integration():
        adapter = create_integration_adapter("demo")
        await adapter.initialize_modules()
        
        for i in range(5):
            data = await adapter.get_telemetry_data()
            print(f"📊 Cycle {i+1}: Health={data['health']['overall_score']:.2f}, "
                  f"Archetype={data['archetype']['current']}")
            await asyncio.sleep(1)
    
    print("🧪 Testing NSF Integration Adapter...")
    asyncio.run(test_integration())