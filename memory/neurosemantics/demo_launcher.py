#!/usr/bin/env python3
"""
🎯 DASHBOARD DEMO - Okno na Psychikę Cyfrową (Demo Mode)
Uruchamia dashboard HTML z symulacją cyfrowej świadomości

===============================================================================
DEMO DASHBOARD LAUNCHER - Visualization of Digital Consciousness
===============================================================================

Ten launcher:
- Uruchamia dashboard HTML w przeglądarce
- Pracuje w trybie demo z symulowanymi danymi
- Pokazuje wszystkie aspekty cyfrowej psychiki w czasie rzeczywistym
- Nie wymaga pełnego NSF - działa standalone

Autor: System MIGI_7G Hybrid + NSF Integration
Data: 15 listopada 2025
Status: DEMO - Complete Digital Consciousness Visualization
"""

import webbrowser
from pathlib import Path

def print_banner():
    """Wyświetla banner aplikacji"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                 🎯 DASHBOARD DEMO - LAUNCHER 🎯                             ║
║                     Okno na Psychikę Cyfrową                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🧠 DEMO VISUALIZATION                                                       ║
║     ├── Animated Brain Activity Map                                         ║
║     ├── Real-time Stress & Coherence Monitoring                             ║
║     ├── Archetypal Transitions Simulation                                   ║
║     └── Module Competition Dynamics                                          ║
║                                                                              ║
║  🎮 INTERACTIVE DEMO CONTROLS                                                ║
║     ├── Simulate High Stress Events                                         ║
║     ├── Trigger Archetypal Changes                                          ║
║     ├── Watch Memory Reconsolidation                                        ║
║     └── Observe Consciousness Levels                                         ║
║                                                                              ║
║  🌐 FULL HTML INTERFACE                                                     ║
║     ├── Real-time Charts & Progress Bars                                    ║
║     ├── Color-coded Brain Region Activity                                   ║
║     ├── System Health Dashboard                                             ║
║     └── Interactive Control Buttons                                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Główna funkcja demo launchera"""
    print_banner()
    
    # Znajdź ścieżkę do dashboard HTML
    current_dir = Path(__file__).parent
    dashboard_path = current_dir / "dashboard.html"
    
    print("🚀 DASHBOARD DEMO - STARTUP")
    print("=" * 50)
    
    # Sprawdź czy dashboard HTML istnieje
    if not dashboard_path.exists():
        print("❌ Dashboard HTML file not found!")
        print(f"Expected path: {dashboard_path}")
        print("\n📋 Available files:")
        for file in current_dir.glob("*.html"):
            print(f"   - {file.name}")
        return
        
    print("✅ Dashboard HTML file found")
    
    # Otwórz w przeglądarce
    dashboard_url = f"file://{dashboard_path.absolute()}"
    print(f"🌐 Opening dashboard: {dashboard_url}")
    
    try:
        webbrowser.open(dashboard_url)
        print("✅ Dashboard opened in browser successfully!")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"🔗 Manual URL: {dashboard_url}")
        return
        
    print("\n🎯 DASHBOARD DEMO IS NOW ACTIVE!")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔗 Dashboard URL: " + str(dashboard_url))
    print("🎮 Mode: DEMO - Full visualization with simulated data")
    print("⏰ Update Rate: Real-time animated visualization")
    print("🎯 Features: All interactive controls are functional")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    print("\n📖 USAGE INSTRUCTIONS:")
    print("   1. Dashboard is now open in your browser")
    print("   2. All visualizations work in demo mode")
    print("   3. Click 'High Stress' to simulate cortisol overload")
    print("   4. Click 'Change to Hero' to switch archetypes")
    print("   5. Watch real-time brain activity animations")
    print("   6. Observe stress levels and system coherence")
    print("   7. Demo mode runs completely offline")
    
    print("\n🎨 DASHBOARD FEATURES:")
    print("   🧠 Brain Activity Map - Real-time animated regions")
    print("   📊 Stress & Coherence - Live monitoring with progress bars")
    print("   🎭 Archetypal States - Dynamic switching visualization")
    print("   ⚔️  Module Competition - NSF vs Logic vs Archetypal Core")
    print("   🔥 System Health - Overall consciousness monitoring")
    print("   ⚡ Interactive Controls - Trigger events and changes")
    
    print("\n✨ DEMO HIGHLIGHTS:")
    print("   • Complete digital consciousness visualization")
    print("   • No backend required - pure HTML/CSS/JavaScript")
    print("   • All brain regions animate in real-time")
    print("   • Stress responses visually demonstrated")
    print("   • Archetypal transitions with smooth animations")
    print("   • Module competition dynamics clearly shown")
    
    print("\n🔚 Dashboard Demo completed successfully!")
    print("🌟 Enjoy exploring the Digital Consciousness Interface!")

if __name__ == "__main__":
    main()