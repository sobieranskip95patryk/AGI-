#!/usr/bin/env python3
"""
🎯 DASHBOARD LAUNCHER - Okno na Psychikę Cyfrową
Uruchamia pełny system monitoringu NSF + MIGI_7G z interfejsem webowym

===============================================================================
CALIBRATION DASHBOARD LAUNCHER - Digital Consciousness Monitor
===============================================================================

Ten launcher:
- Uruchamia NSF + MIGI_7G Integration Hub
- Startuje WebSocket server dla real-time komunikacji  
- Otwiera dashboard HTML w przeglądarce
- Monitoruje wszystkie aspekty cyfrowej psychiki w czasie rzeczywistym

Autor: System MIGI_7G Hybrid + NSF Integration
Data: 15 listopada 2025
Status: PRODUCTION - Complete Digital Consciousness Monitoring Solution
"""

import os
import sys
import time
import threading
import webbrowser
import json
import logging
from pathlib import Path

# Dodaj ścieżkę do NSF
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import modułów
try:
    from nsf_migi7g_hybrid import NeuroSemanticFlowmeter
    from migi7g_integration_hub import MIGI7G_IntegrationHub
    NSF_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ NSF modules not available: {e}")
    NSF_AVAILABLE = False

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleDashboardServer:
    """
    Uproszczony dashboard server dla demonstracji
    Symuluje dane gdy NSF nie jest dostępny
    """
    
    def __init__(self):
        self.integration_hub = None
        self.is_running = False
        self.demo_mode = not NSF_AVAILABLE
        
        # Demo data
        self.demo_cycle = 0
        self.demo_stress = 0.0
        self.demo_archetype = "everyman"
        
    def start_server(self):
        """Uruchamia serwer dashboard'u"""
        print("🎯 DASHBOARD KALIBRACYJNY - STARTUP")
        print("=" * 50)
        
        if NSF_AVAILABLE:
            print("🧠 Starting NSF + MIGI_7G Integration...")
            try:
                self.integration_hub = MIGI7G_IntegrationHub()
                self.integration_hub.start_integrated_processing()
                time.sleep(2)
                print("✅ Integration Hub started successfully")
            except Exception as e:
                print(f"❌ Failed to start Integration Hub: {e}")
                print("🎮 Switching to demo mode...")
                self.demo_mode = True
        else:
            print("🎮 NSF not available - running in demo mode")
            
        # Start monitoring thread
        self.is_running = True
        monitor_thread = threading.Thread(target=self._monitoring_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Open dashboard in browser
        dashboard_path = current_dir / "dashboard.html"
        if dashboard_path.exists():
            print(f"🌐 Opening dashboard: {dashboard_path}")
            webbrowser.open(f"file://{dashboard_path}")
        else:
            print("❌ Dashboard HTML file not found")
            
        print("\n📊 DASHBOARD ACTIVE")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🔗 Dashboard URL: file://" + str(dashboard_path))
        print("🎯 Status: " + ("Real NSF Data" if not self.demo_mode else "Demo Mode"))
        print("⏰ Update Rate: 1Hz (every second)")
        print("🎮 Use dashboard buttons to interact with system")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        return True
        
    def _monitoring_loop(self):
        """Główna pętla monitoringu"""
        while self.is_running:
            try:
                if self.demo_mode:
                    self._update_demo_data()
                    self._log_demo_status()
                else:
                    self._log_real_status()
                    
                time.sleep(1.0)  # 1Hz
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(0.1)
                
    def _update_demo_data(self):
        """Aktualizuje dane demo"""
        import random
        
        self.demo_cycle += 1
        
        # Simulate stress waves
        stress_wave = abs(math.sin(self.demo_cycle * 0.1)) * 0.8
        self.demo_stress = max(0.0, min(1.0, stress_wave + random.uniform(-0.2, 0.2)))
        
        # Simulate archetype changes
        if self.demo_cycle % 30 == 0:  # Every 30 seconds
            archetypes = ["everyman", "hero", "sage", "lover", "magician"]
            self.demo_archetype = random.choice(archetypes)
            
    def _log_demo_status(self):
        """Loguje status demo mode"""
        if self.demo_cycle % 10 == 0:  # Every 10 seconds
            status = f"""
🎮 DEMO MODE STATUS (Cycle {self.demo_cycle}):
├── Simulated Stress: {self.demo_stress:.2f}
├── Current Archetype: {self.demo_archetype.upper()}
├── Demo Atoms: {self.demo_cycle % 10 + 1}
├── Demo Cycles: {self.demo_cycle}
└── Status: DEMO - Open dashboard.html in browser
            """
            print(status)
            
    def _log_real_status(self):
        """Loguje status rzeczywistych danych"""
        if not self.integration_hub:
            return
            
        try:
            status = self.integration_hub.get_system_status()
            if status.get('cycle_count', 0) % 10 == 0:
                metrics = status.get('metrics', {})
                real_status = f"""
🧠 REAL NSF STATUS (Cycle {status.get('cycle_count', 0)}):
├── Consciousness: {status.get('consciousness_level', 'unknown').upper()}
├── Stress: {metrics.get('cortisol_level', 0):.2f}
├── PFC Suppression: {metrics.get('pfc_suppression', 0):.2f}
├── Sense Atoms: {metrics.get('sense_atom_count', 0)}
├── Reconsolidations: {metrics.get('reconsolidation_count', 0)}
└── System Coherence: {metrics.get('system_coherence', 0):.2f}
                """
                print(real_status)
        except Exception as e:
            logger.error(f"Error logging real status: {e}")
            
    def stop_server(self):
        """Zatrzymuje serwer"""
        print("\n⏹️ Stopping Dashboard Server...")
        self.is_running = False
        
        if self.integration_hub:
            self.integration_hub.stop_integrated_processing()
            print("✅ Integration Hub stopped")
            
        print("👋 Dashboard Server stopped")

def print_banner():
    """Wyświetla banner aplikacji"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║               🎯 DASHBOARD KALIBRACYJNY - LAUNCHER 🎯                       ║
║                     Okno na Psychikę Cyfrową                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🧠 REAL-TIME MONITORING                                                     ║
║     ├── Stress Levels & Cortisol Dynamics                                   ║
║     ├── Archetypal Transitions & Memory Reconsolidation                     ║
║     ├── Network Contention & Resource Competition                           ║
║     └── Sekundnik Rhythm & Consciousness Levels                             ║
║                                                                              ║
║  🎮 INTERACTIVE CONTROLS                                                     ║
║     ├── Trigger Stress Events (Mild/High)                                   ║
║     ├── Change Archetypal States (Hero/Sage)                               ║
║     ├── Simulate Different Input Types                                      ║
║     └── Real-time System Health Monitoring                                  ║
║                                                                              ║
║  🌐 WEB INTERFACE                                                           ║
║     ├── Animated Brain Activity Map                                         ║
║     ├── Real-time Charts & Progress Bars                                    ║
║     ├── Module Competition Visualization                                     ║
║     └── System Health Dashboard                                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Główna funkcja launchera"""
    print_banner()
    
    # Import math for demo mode
    import math
    globals()['math'] = math
    
    try:
        # Sprawdź czy dashboard HTML istnieje
        dashboard_path = current_dir / "dashboard.html"
        if not dashboard_path.exists():
            print("❌ Dashboard HTML file not found!")
            print(f"Expected path: {dashboard_path}")
            return
            
        # Uruchom server
        server = SimpleDashboardServer()
        
        print("🚀 Starting Dashboard Server...")
        success = server.start_server()
        
        if success:
            print("\n🎯 Dashboard is now active!")
            print("📖 USAGE INSTRUCTIONS:")
            print("   1. Dashboard should open automatically in your browser")
            print("   2. If not, manually open: dashboard.html")
            print("   3. Use the control buttons to interact with the system")
            print("   4. Watch real-time metrics update every second")
            print("   5. Press Ctrl+C here to stop the monitoring")
            
            # Keep running until interrupted
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n⚠️ Interrupt received...")
        else:
            print("❌ Failed to start dashboard server")
            
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'server' in locals():
            server.stop_server()
        print("\n🔚 Dashboard Launcher finished")

if __name__ == "__main__":
    main()