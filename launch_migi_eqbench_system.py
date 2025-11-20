# launch_migi_eqbench_system.py
"""
Główny launcher dla pełnego systemu MIGI_7G + Dashboard Kalibracyjny + EQ-Bench 3
Uruchamia wszystkie komponenty w odpowiedniej kolejności
"""

import asyncio
import subprocess
import time
import logging
import signal
import sys
from pathlib import Path
from typing import List, Optional
import webbrowser
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migi_eqbench_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MIGIEQBenchSystemLauncher:
    """Główny launcher systemu MIGI + EQ-Bench"""
    
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.base_dir = Path(__file__).parent.parent
        self.running = False
        
        # Konfiguracja portów
        self.ports = {
            "telemetry_ws": 8765,
            "dashboard": 8080,
            "migi_api": 5000
        }
        
        # Ścieżki do komponentów
        self.components = {
            "telemetry_server": self.base_dir / "telemetry_ws.py",
            "migi_launcher": self.base_dir / "migi7g_launcher.py", 
            "dashboard": self.base_dir / "memory" / "neurosemantics" / "dashboard.html",
            "eq_adapter": self.base_dir / "eqbench_integration" / "migi_eqbench_adapter.py"
        }
        
    def check_dependencies(self) -> bool:
        """Sprawdza czy wszystkie wymagane pliki istnieją"""
        logger.info("🔍 Checking system dependencies...")
        
        missing_files = []
        for name, path in self.components.items():
            if not path.exists():
                missing_files.append(f"{name}: {path}")
        
        if missing_files:
            logger.error("❌ Missing required files:")
            for file in missing_files:
                logger.error(f"   - {file}")
            return False
        
        logger.info("✅ All dependencies found")
        return True
    
    def check_ports(self) -> bool:
        """Sprawdza czy porty są dostępne"""
        import socket
        
        logger.info("🔍 Checking port availability...")
        
        for name, port in self.ports.items():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex(('localhost', port))
                    if result == 0:
                        logger.warning(f"⚠️ Port {port} ({name}) is already in use")
                        return False
            except Exception as e:
                logger.error(f"❌ Error checking port {port}: {e}")
                return False
        
        logger.info("✅ All ports available")
        return True
    
    async def start_component(self, name: str, command: List[str], wait_for_ready: Optional[str] = None) -> subprocess.Popen:
        """
        Uruchamia pojedynczy komponent systemu
        
        Args:
            name: Nazwa komponentu
            command: Komenda do uruchomienia
            wait_for_ready: Tekst w stdout/stderr sygnalizujący gotowość komponentu
        
        Returns:
            Proces komponentu
        """
        logger.info(f"🚀 Starting {name}...")
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                cwd=self.base_dir
            )
            
            self.processes.append(process)
            
            # Czekaj na sygnał gotowości jeśli określony
            if wait_for_ready:
                await self._wait_for_ready_signal(process, wait_for_ready, timeout=30)
            else:
                await asyncio.sleep(2)  # Podstawowe opóźnienie
            
            logger.info(f"✅ {name} started successfully (PID: {process.pid})")
            return process
            
        except Exception as e:
            logger.error(f"❌ Failed to start {name}: {e}")
            raise
    
    async def _wait_for_ready_signal(self, process: subprocess.Popen, ready_signal: str, timeout: int = 30):
        """Czeka na sygnał gotowości z procesu"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if process.poll() is not None:
                logger.error(f"Process terminated unexpectedly (exit code: {process.returncode})")
                raise RuntimeError("Process terminated before ready signal")
            
            # Sprawdź stdout
            if process.stdout.readable():
                try:
                    line = process.stdout.readline()
                    if line and ready_signal in line:
                        logger.info(f"✅ Ready signal detected: {line.strip()}")
                        return
                except Exception:
                    pass
            
            await asyncio.sleep(0.5)
        
        logger.warning(f"⚠️ Timeout waiting for ready signal: {ready_signal}")
    
    async def start_system(self):
        """Uruchamia cały system MIGI + EQ-Bench"""
        logger.info("🎯 Starting MIGI EQ-Bench System...")
        logger.info("=" * 60)
        
        try:
            # 1. Sprawdzenie zależności
            if not self.check_dependencies():
                raise RuntimeError("Missing dependencies")
            
            if not self.check_ports():
                raise RuntimeError("Ports not available")
            
            # 2. Uruchomienie Telemetry WebSocket Server
            await self.start_component(
                "Telemetry WebSocket Server",
                [sys.executable, str(self.components["telemetry_server"])],
                "Telemetry server is running"
            )
            
            # 3. Uruchomienie MIGI Core
            await self.start_component(
                "MIGI Core System",
                [sys.executable, str(self.components["migi_launcher"])],
                "System MIGI 7G uruchomiony"
            )
            
            # 4. Otwórz Dashboard w przeglądarce
            dashboard_url = f"file://{self.components['dashboard'].absolute()}"
            logger.info(f"🌐 Opening Dashboard: {dashboard_url}")
            webbrowser.open(dashboard_url)
            
            # 5. Wyświetl instrukcje
            self._display_instructions()
            
            self.running = True
            logger.info("🎉 MIGI EQ-Bench System fully operational!")
            
        except Exception as e:
            logger.error(f"❌ System startup failed: {e}")
            await self.shutdown_system()
            raise
    
    def _display_instructions(self):
        """Wyświetla instrukcje użytkowania"""
        instructions = f"""
🧠 MIGI_7G + Dashboard Kalibracyjny + EQ-Bench 3 - SYSTEM READY!

📊 DASHBOARD KALIBRACYJNY
   URL: file://{self.components['dashboard'].absolute()}
   WebSocket: ws://localhost:{self.ports['telemetry_ws']}
   
🔬 EQ-BENCH TESTING
   Adapter: {self.components['eq_adapter']}
   
🎮 KONTROLKI EKSPERYMENTÓW:
   - Stress Spike 30s: Testuje reakcję na stres
   - Shift to Sage: Wymusza przejście do archetypu Mędrca
   - NSF Dominance: Test dominacji modułu NSF
   - Trauma Injection: Symuluje traumę emocjonalną
   - Coherence Test: Test utrzymania koherencji
   - Archetype Lock: Blokada przejść archetypowych
   
📈 RISK RADAR:
   - Masking Risk: Wykrywa fałszywą koherencję
   - Rigidity Risk: Wykrywa sztywność archetypową
   - Monoculture Risk: Wykrywa dominację modułów

🧪 PRZYKŁADY UŻYCIA:

1. Szybki test empatii:
   python -c "
   import asyncio
   from eqbench_integration.automated_eq_testing import run_quick_empathy_test
   print(asyncio.run(run_quick_empathy_test(5)))
   "

2. Porównanie archetypów:
   python -c "
   import asyncio
   from eqbench_integration.automated_eq_testing import run_archetype_comparison
   print(asyncio.run(run_archetype_comparison()))
   "

3. Test pojedynczego scenariusza:
   python -c "
   import asyncio
   from eqbench_integration.migi_eqbench_adapter import call_migi_model
   result = asyncio.run(call_migi_model('I lost my job and feel hopeless.'))
   print(f'Empathy: {{result[\"meta\"][\"empathy_indicators\"][\"empathy_score\"]:.2f}}')
   "

⚡ MONITOROWANIE:
   - Snapshoty: ./snapshots/
   - Logi systemu: ./migi_eqbench_system.log
   - Wyniki testów: ./eq_test_results/
   
🛑 ZATRZYMANIE SYSTEMU:
   Ctrl+C lub python launch_migi_eqbench_system.py --shutdown

{"="*60}
Press Ctrl+C to shutdown the system
{"="*60}
        """
        
        print(instructions)
    
    async def run_interactive_mode(self):
        """Uruchamia tryb interaktywny z monitorowaniem"""
        try:
            while self.running:
                await asyncio.sleep(1)
                
                # Sprawdź czy procesy jeszcze działają
                dead_processes = []
                for i, process in enumerate(self.processes):
                    if process.poll() is not None:
                        dead_processes.append(i)
                        logger.warning(f"⚠️ Process {process.pid} terminated (exit code: {process.returncode})")
                
                # Usuń martwe procesy
                for i in reversed(dead_processes):
                    self.processes.pop(i)
                
                # Jeśli wszystkie procesy zmarły, zakończ
                if not self.processes:
                    logger.error("❌ All processes terminated, shutting down")
                    break
                    
        except KeyboardInterrupt:
            logger.info("🛑 Shutdown requested by user")
        except Exception as e:
            logger.error(f"❌ Error in interactive mode: {e}")
        finally:
            await self.shutdown_system()
    
    async def shutdown_system(self):
        """Zamyka wszystkie komponenty systemu"""
        logger.info("🛑 Shutting down MIGI EQ-Bench System...")
        
        self.running = False
        
        # Zamknij wszystkie procesy
        for process in self.processes:
            try:
                logger.info(f"🛑 Terminating process {process.pid}")
                process.terminate()
                
                # Poczekaj na graceful shutdown
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning(f"⚠️ Force killing process {process.pid}")
                    process.kill()
                    process.wait()
                    
            except Exception as e:
                logger.error(f"❌ Error terminating process {process.pid}: {e}")
        
        self.processes.clear()
        logger.info("✅ System shutdown complete")
    
    async def run_eq_benchmark(self, scenarios_count: int = 10, output_file: str = None):
        """Uruchamia benchmark EQ-Bench"""
        logger.info(f"🧪 Starting EQ-Bench with {scenarios_count} scenarios")
        
        try:
            from eqbench_integration.automated_eq_testing import run_quick_empathy_test
            
            # Uruchom test
            results = await run_quick_empathy_test(scenarios_count)
            
            # Przygotuj raport
            report = {
                "timestamp": time.time(),
                "scenarios_count": scenarios_count,
                "average_empathy": results.average_empathy,
                "empathy_std": results.empathy_std,
                "success_rate": results.success_rate,
                "average_response_time": results.average_response_time,
                "detailed_results": {
                    "empathy_scores": results.empathy_scores,
                    "stress_responses": results.stress_responses,
                    "response_times": results.response_times
                }
            }
            
            # Zapisz wyniki
            if output_file is None:
                output_file = f"eq_benchmark_results_{int(time.time())}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            
            logger.info("✅ EQ-Bench completed!")
            logger.info(f"   Average empathy: {results.average_empathy:.3f} ± {results.empathy_std:.3f}")
            logger.info(f"   Success rate: {results.success_rate:.1%}")
            logger.info(f"   Results saved: {output_file}")
            
            return report
            
        except Exception as e:
            logger.error(f"❌ EQ-Bench failed: {e}")
            raise

def setup_signal_handlers(launcher):
    """Ustawia handlery sygnałów dla graceful shutdown"""
    def signal_handler(signum, frame):
        logger.info(f"📡 Received signal {signum}")
        asyncio.create_task(launcher.shutdown_system())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

async def main():
    """Główna funkcja launcher'a"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MIGI EQ-Bench System Launcher")
    parser.add_argument("--benchmark", type=int, metavar="N", 
                       help="Run EQ benchmark with N scenarios and exit")
    parser.add_argument("--output", type=str, 
                       help="Output file for benchmark results")
    parser.add_argument("--check-only", action="store_true",
                       help="Only check dependencies and exit")
    parser.add_argument("--shutdown", action="store_true",
                       help="Shutdown any running instances")
    
    args = parser.parse_args()
    
    launcher = MIGIEQBenchSystemLauncher()
    setup_signal_handlers(launcher)
    
    try:
        if args.check_only:
            # Tylko sprawdzenie zależności
            if launcher.check_dependencies() and launcher.check_ports():
                print("✅ System ready to launch")
                return 0
            else:
                print("❌ System not ready")
                return 1
        
        elif args.shutdown:
            # Shutdown existing instances (placeholder)
            logger.info("🛑 Shutdown requested")
            # TODO: Implement proper shutdown detection
            return 0
        
        elif args.benchmark:
            # Tylko benchmark
            await launcher.start_system()
            await asyncio.sleep(5)  # Czas na inicjalizację
            await launcher.run_eq_benchmark(args.benchmark, args.output)
            await launcher.shutdown_system()
            return 0
        
        else:
            # Pełny system
            await launcher.start_system()
            await launcher.run_interactive_mode()
            return 0
            
    except KeyboardInterrupt:
        logger.info("🛑 Interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"❌ System error: {e}")
        return 1

if __name__ == "__main__":
    # Uruchom system
    exit_code = asyncio.run(main())
    sys.exit(exit_code)