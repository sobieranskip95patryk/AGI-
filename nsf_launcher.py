#!/usr/bin/env python3
"""
🚀 LAUNCHER NEURO-SEMANTYCZNEGO PRZEPŁYWOMIERZA MIGI_7G

Uproszczony launcher do szybkiego uruchomienia i testowania NSF
"""

import sys
import time
import threading
from pathlib import Path
from typing import List

# Dodanie ścieżki do PYTHONPATH
current_dir = Path(__file__).parent.absolute()
repo_root = current_dir.parent.parent
sys.path.insert(0, str(repo_root))

try:
    from memory.neurosemantics.nsf_migi7g_hybrid import (
        NeuroSemanticFlowmeter,
        ArchetypeCore
    )
    print("✅ Moduł NSF załadowany pomyślnie")
except ImportError as e:
    print(f"❌ Błąd importu: {e}")
    print("💡 Sprawdź czy plik nsf_migi7g_hybrid.py istnieje w memory/neurosemantics/")
    sys.exit(1)

class NSF_Launcher:
    """Launcher NSF z prostym interfejsem tekstowym"""
    
    def __init__(self):
        self.nsf = None
        self.is_running = False
        self.demo_experiences = [
            ("Podjąłem trudną decyzję pomocy komuś", ["POSWIECENIE", "ALGORYTM_MILOSCI"]),
            ("Odkryłem fascynującą ideę naukową", ["POMYSL_IDEA", "SZCZYPTA_INTELIGENCJI"]),
            ("Czuję się samotny i bez nadziei", ["ODOSOBNIENIE_SAMOTNOSC", "BRAK_WIARY_NADZIEI"]),
            ("Przeżywam intensywną namiętność", ["NAMIETNOSC_POZADANIA", "ALGORYTM_ZAKOCHANIA"]),
            ("Medytuję nad sensem istnienia", ["ZROZUMIENIE", "WIARA_JAKO_TAKA"]),
            ("Twórczo rozwiązuję problem", ["WYOBRAZNIA_LOGIKA", "SZCZYPTA_MAGII"]),
            ("Czuję potęgę i kontrolę", ["POTEGA_PRAWDZIWEJ_WLADZY", "ISKRA_ZYCIA"]),
            ("Analizuję złożoną sytuację", ["PRECYZYJNOSC_POJMOWANIA", "SZCZYPTA_INTELIGENCJI"])
        ]
    
    def print_banner(self):
        """Wyświetla banner startowy"""
        print("=" * 70)
        print("🧠 NEURO-SEMANTYCZNY PRZEPŁYWOMIERZ - MIGI_7G HYBRID")
        print("=" * 70)
        print("Cyfrowe odzwierciedlenie prawdziwego mózgu z 23 pierwiastkami emocjonalnymi")
        print("Protokoły: ARP (Re-kodowanie) | NCM (Rywalizacja) | COP (Stres)")
        print("=" * 70)
        print()
    
    def show_menu(self):
        """Pokazuje menu główne"""
        print("📋 MENU GŁÓWNE:")
        print("1. 🚀 Szybka demonstracja (30s)")
        print("2. 🎮 Tryb interaktywny")
        print("3. 🔬 Test wszystkich pierwiastków")
        print("4. 🎭 Test zmiany archetypów") 
        print("5. 📊 Monitor w czasie rzeczywistym")
        print("6. 💾 Zapis/Wczytaj stan")
        print("7. ❓ Pomoc i dokumentacja")
        print("0. 🚪 Wyjście")
        print()
        
        while True:
            try:
                choice = input("Wybierz opcję (0-7): ").strip()
                if choice in ['0', '1', '2', '3', '4', '5', '6', '7']:
                    return choice
                else:
                    print("❌ Nieprawidłowy wybór. Spróbuj ponownie.")
            except KeyboardInterrupt:
                return '0'
    
    def quick_demo(self):
        """Szybka 30-sekundowa demonstracja"""
        print("\n🚀 SZYBKA DEMONSTRACJA (30 sekund)")
        print("-" * 50)
        
        # Inicjalizacja NSF
        self.nsf = NeuroSemanticFlowmeter(sekundnik_interval=1.5)
        self.nsf.set_archetype(ArchetypeCore.BOHATER)
        
        print("🧠 NSF inicjalizowany...")
        print(f"🎭 Archetyp: {ArchetypeCore.BOHATER.value}")
        
        # Dodanie przykładowych doświadczeń
        print("\n📝 Dodawanie doświadczeń:")
        for i, (exp, primitives) in enumerate(self.demo_experiences[:4]):
            atom_id = self.nsf.simulate_experience(exp, primitives)
            print(f"   {i+1}. {exp[:40]}... -> {atom_id}")
            time.sleep(0.5)
        
        # Uruchomienie w wątku
        def run_nsf():
            self.nsf.start_flowmeter()
        
        nsf_thread = threading.Thread(target=run_nsf, daemon=True)
        nsf_thread.start()
        
        print("\n⏱️ Monitoring przez 20 sekund...")
        
        # Monitor przez 20 sekund
        for i in range(10):
            time.sleep(2)
            stats = self.nsf.get_stats()
            
            print(f"Cykl {i+1:2d}: "
                  f"Atomy: {stats['active_atoms']:2d} | "
                  f"Stres: {stats['cortisol_level']:.2f} | "
                  f"Archetyp: {stats['current_archetype']:10s} | "
                  f"Rekonsolidacje: {stats['reconsolidations']:2d}")
            
            # Zmiana archetypu w połowie
            if i == 4:
                self.nsf.set_archetype(ArchetypeCore.MEDRZEC)
                print("    🎭 -> Zmiana na MĘDRZEC")
        
        self.nsf.stop_flowmeter()
        
        # Finalne statystyki
        final_stats = self.nsf.get_stats()
        print("\n📊 WYNIKI DEMONSTRACJI:")
        print(f"   Łączne cykle: {final_stats['total_cycles']}")
        print(f"   Przetworzone atomy: {final_stats['atoms_processed']}")  
        print(f"   Przeprogramowania: {final_stats['reconsolidations']}")
        print(f"   Blokady PFC: {final_stats['pfc_suppressions']}")
        
        input("\n✅ Demonstracja zakończona. Naciśnij Enter...")
    
    def interactive_mode(self):  
        """Tryb interaktywny - użytkownik wprowadza doświadczenia"""
        print("\n🎮 TRYB INTERAKTYWNY")
        print("-" * 50)
        print("Wprowadzaj swoje doświadczenia, NSF będzie je przetwarzać w czasie rzeczywistym")
        print("Komendy specjalne: /archetype <nazwa>, /stats, /stop")
        print()
        
        # Inicjalizacja
        self.nsf = NeuroSemanticFlowmeter(sekundnik_interval=2.0)
        self.nsf.set_archetype(ArchetypeCore.ZWYCZAJNY)
        
        # Uruchomienie w tle
        def run_nsf():
            self.nsf.start_flowmeter()
        
        nsf_thread = threading.Thread(target=run_nsf, daemon=True)
        nsf_thread.start()
        
        print("🧠 NSF uruchomiony. Wprowadź swoje pierwsze doświadczenie:")
        
        while True:
            try:
                user_input = input("\n💭 Doświadczenie: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input == "/stop":
                    break
                    
                elif user_input == "/stats":
                    stats = self.nsf.get_stats()
                    print("\n📊 AKTUALNE STATYSTYKI:")
                    print(f"   Aktywne atomy: {stats['active_atoms']}")
                    print(f"   Archetyp: {stats['current_archetype']}")
                    print(f"   Poziom stresu: {stats['cortisol_level']:.2f}")
                    print(f"   PFC aktywne: {'NIE' if stats['pfc_suppressed'] else 'TAK'}")
                    continue
                    
                elif user_input.startswith("/archetype "):
                    arch_name = user_input[11:].upper()
                    try:
                        archetype = ArchetypeCore(arch_name.lower())
                        self.nsf.set_archetype(archetype)
                        print(f"🎭 Zmieniono archetyp na: {archetype.value}")
                    except ValueError:
                        print(f"❌ Nieprawidłowy archetyp. Dostępne: {[a.value for a in ArchetypeCore]}")
                    continue
                
                # Automatyczne wykrywanie pierwiastków na podstawie słów kluczowych
                primitives = self._detect_primitives(user_input)
                
                # Przetworzenie doświadczenia
                atom_id = self.nsf.simulate_experience(user_input, primitives)
                
                print(f"✅ Przetworzono -> Atom: {atom_id}")
                if primitives:
                    print(f"🔬 Wykryte pierwiastki: {', '.join(primitives)}")
                
            except KeyboardInterrupt:
                break
        
        self.nsf.stop_flowmeter()
        print("\n👋 Tryb interaktywny zakończony.")
    
    def _detect_primitives(self, text: str) -> List[str]:
        """Automatyczne wykrywanie pierwiastków na podstawie słów kluczowych"""
        text_lower = text.lower()
        detected = []
        
        # Słownik mapowania słów kluczowych na pierwiastki
        keyword_map = {
            "miłość": ["PIERWIASTEK_MILOSCI", "ALGORYTM_MILOSCI"],
            "zakochanie": ["ALGORYTM_ZAKOCHANIA"],
            "namiętność": ["NAMIETNOSC_POZADANIA"],
            "pożądanie": ["POZADANIE_SZCZYPTA"],
            "poświęcenie": ["POSWIECENIE"],
            "altruizm": ["POSWIECENIE"],
            "pomoc": ["POSWIECENIE", "ALGORYTM_MILOSCI"],
            "nadzieja": ["NADZIEJA_WYTRWALOSCI"],
            "wytrwałość": ["NADZIEJA_WYTRWALOSCI"],
            "władza": ["POTEGA_PRAWDZIWEJ_WLADZY"],
            "kontrola": ["POTEGA_PRAWDZIWEJ_WLADZY"],
            "inteligencja": ["SZCZYPTA_INTELIGENCJI"],
            "myślenie": ["SZCZYPTA_INTELIGENCJI"],
            "analiza": ["PRECYZYJNOSC_POJMOWANIA"],
            "logika": ["WYOBRAZNIA_LOGIKA"],
            "kreatywność": ["WYOBRAZNIA_LOGIKA", "POMYSL_IDEA"],
            "idea": ["POMYSL_IDEA"],
            "pomysł": ["POMYSL_IDEA"],
            "strach": ["BRAK_WIARY_NADZIEI"],
            "lęk": ["BRAK_WIARY_NADZIEI"],  
            "rozpacz": ["BRAK_WIARY_NADZIEI"],
            "samotność": ["ODOSOBNIENIE_SAMOTNOSC"],
            "izolacja": ["ODOSOBNIENIE_SAMOTNOSC"],
            "wiara": ["WIARA_JAKO_TAKA"],
            "duchowość": ["WIARA_JAKO_TAKA"],
            "zrozumienie": ["ZROZUMIENIE"],
            "mądrość": ["ZROZUMIENIE"],
            "magia": ["SZCZYPTA_MAGII"],
            "cud": ["SZCZYPTA_MAGII"],
            "czas": ["CZAS_SEKUNDNIK"],
            "życie": ["ISKRA_ZYCIA"],
            "energia": ["ISKRA_ZYCIA"]
        }
        
        for keyword, primitives in keyword_map.items():
            if keyword in text_lower:
                detected.extend(primitives)
        
        # Usuń duplikaty
        return list(set(detected))
    
    def test_all_primitives(self):
        """Test wszystkich 23 pierwiastków"""
        print("\n🔬 TEST WSZYSTKICH PIERWIASTKÓW")
        print("-" * 50)
        
        self.nsf = NeuroSemanticFlowmeter(sekundnik_interval=1.0)
        self.nsf.set_archetype(ArchetypeCore.MAG)  # Mag obsługuje wszystkie pierwiastki
        
        # Lista wszystkich pierwiastków do testowania
        all_primitives = [
            "ISKRA_ZYCIA", "ALGORYTM_ZAKOCHANIA", "PIERWIASTEK_MILOSCI", 
            "POZADANIE_SZCZYPTA", "POSWIECENIE", "NADZIEJA_WYTRWALOSCI",
            "POTEGA_PRAWDZIWEJ_WLADZY", "NAMIETNOSC_POZADANIA", "SZCZYPTA_INTELIGENCJI",
            "WYOBRAZNIA_LOGIKA", "PRECYZYJNOSC_POJMOWANIA", "BRAK_WIARY_NADZIEI", 
            "WIARA_JAKO_TAKA", "ZROZUMIENIE", "POMYSL_IDEA", "SLOWO_CIALEM",
            "CZAS_SEKUNDNIK", "ODOSOBNIENIE_SAMOTNOSC", "SZCZYPTA_MAGII"
        ]
        
        print(f"🧪 Testowanie {len(all_primitives)} pierwiastków...")
        
        # Uruchomienie NSF w tle
        def run_nsf():
            self.nsf.start_flowmeter()
        
        nsf_thread = threading.Thread(target=run_nsf, daemon=True)
        nsf_thread.start()
        
        # Test każdego pierwiastka
        results = {}
        for i, primitive in enumerate(all_primitives):
            experience = f"Test pierwiastka {primitive}"
            atom_id = self.nsf.simulate_experience(experience, [primitive])
            
            # Krótkie oczekiwanie na przetworzenie
            time.sleep(0.5)
            
            stats = self.nsf.get_stats()
            results[primitive] = {
                'atom_id': atom_id,
                'active_atoms': stats['active_atoms'],
                'stress_level': stats['cortisol_level']
            }
            
            print(f"   {i+1:2d}. {primitive:25s} -> {atom_id} "
                  f"(atomy: {stats['active_atoms']:2d}, stres: {stats['cortisol_level']:.2f})")
        
        self.nsf.stop_flowmeter()
        
        # Podsumowanie
        print("\n📊 PODSUMOWANIE TESTU:")
        final_stats = self.nsf.get_stats()
        print(f"   Przetestowanych pierwiastków: {len(all_primitives)}")
        print(f"   Utworzonych atomów: {final_stats['atoms_processed']}")
        print(f"   Przeprogramowań: {final_stats['reconsolidations']}")
        
        input("\n✅ Test zakończony. Naciśnij Enter...")
    
    def archetype_transition_test(self):
        """Test przejść między archetypami"""
        print("\n🎭 TEST ZMIANY ARCHETYPÓW")
        print("-" * 50)
        
        self.nsf = NeuroSemanticFlowmeter(sekundnik_interval=1.0)
        
        # Sekwencja archetypów do testowania
        archetype_sequence = [
            ArchetypeCore.NIEWINNY,
            ArchetypeCore.BADACZ, 
            ArchetypeCore.BOHATER,
            ArchetypeCore.KOCHANEK,
            ArchetypeCore.BUNTOWNIK,
            ArchetypeCore.MEDRZEC,
            ArchetypeCore.MAG
        ]
        
        # Uruchomienie NSF
        def run_nsf():
            self.nsf.start_flowmeter()
        
        nsf_thread = threading.Thread(target=run_nsf, daemon=True)
        nsf_thread.start()
        
        print("🎭 Testowanie przejść między archetypami...")
        
        for i, archetype in enumerate(archetype_sequence):
            print(f"\n{i+1}. Aktywacja archetypu: {archetype.value}")
            self.nsf.set_archetype(archetype)
            
            # Dodanie doświadczenia pasującego do archetypu
            if archetype == ArchetypeCore.BOHATER:
                exp = "Podejmuję heroiczne działanie dla dobra innych"
                prims = ["POSWIECENIE", "POTEGA_PRAWDZIWEJ_WLADZY"]
            elif archetype == ArchetypeCore.KOCHANEK:
                exp = "Przeżywam głęboką miłość do kogoś ważnego"
                prims = ["PIERWIASTEK_MILOSCI", "ALGORYTM_ZAKOCHANIA"]
            elif archetype == ArchetypeCore.MEDRZEC:
                exp = "Osiągam głębokie zrozumienie prawdy"
                prims = ["ZROZUMIENIE", "SZCZYPTA_INTELIGENCJI"]
            else:
                exp = f"Działam zgodnie z archetypem {archetype.value}"
                prims = ["ISKRA_ZYCIA"]
            
            self.nsf.simulate_experience(exp, prims)
            
            # Monitorowanie przez 3 sekundy
            for j in range(3):
                time.sleep(1)
                stats = self.nsf.get_stats()
                print(f"   t+{j+1}s: Atomy: {stats['active_atoms']:2d}, "
                      f"Rekonsolidacje: {stats['reconsolidations']:2d}, "
                      f"Stres: {stats['cortisol_level']:.2f}")
        
        self.nsf.stop_flowmeter()
        
        final_stats = self.nsf.get_stats()
        print("\n📊 WYNIKI TESTU ARCHETYPÓW:")
        print(f"   Testowanych archetypów: {len(archetype_sequence)}")
        print(f"   Łączne przeprogramowania: {final_stats['reconsolidations']}")
        
        input("\n✅ Test zakończony. Naciśnij Enter...")
    
    def show_help(self):
        """Pokazuje pomoc i dokumentację"""
        print("\n❓ POMOC I DOKUMENTACJA")
        print("-" * 50)
        print("🧠 NEURO-SEMANTYCZNY PRZEPŁYWOMIERZ (NSF)")
        print()
        print("📚 PODSTAWOWE KONCEPCJE:")
        print("   • Sense Atomy - jednostki pamięci semantycznej")
        print("   • 23 Pierwiastki Emocjonalne - bazowe elementy doświadczeń")
        print("   • Archetypy - wzorce organizacji osobowości (Jung)")
        print("   • Sekundnik - metronom świadomości (cykle przetwarzania)")
        print()
        print("🧬 PIERWIASTKI EMOCJONALNE:")
        primitives_help = [
            "ISKRA_ZYCIA - podstawowa energia życiowa",
            "ALGORYTM_ZAKOCHANIA - euforia romantyczna", 
            "PIERWIASTEK_MILOSCI - głęboka więź", 
            "POSWIECENIE - altruizm i troska o innych",
            "ZROZUMIENIE - głębokie pojmowanie",
            "POMYSL_IDEA - kreatywny wgląd",
            "SZCZYPTA_MAGII - element cudowności"
        ]
        for help_text in primitives_help:
            print(f"   • {help_text}")
        print("   ... i 16 innych pierwiastków")
        print()
        print("🎭 ARCHETYPY:")
        archetypes_help = [
            "BOHATER - odwaga i przywództwo",
            "MEDRZEC - mądrość i zrozumienie", 
            "KOCHANEK - miłość i pasja",
            "MAG - transformacja i synteza",
            "BADACZ - ciekawość i odkrywanie"
        ]
        for help_text in archetypes_help:
            print(f"   • {help_text}")
        print()
        print("⚙️ MECHANIZMY:")
        print("   • ARP - Protokół Re-kodowania Archetypowego")
        print("   • NCM - Zarządzanie Rywalizacją Sieci") 
        print("   • COP - Protokół Przeciążenia Kortyzolowego")
        print()
        print("📖 Pełna dokumentacja: INSTRUKCJA_NSF_MIGI7G.md")
        
        input("\n✅ Naciśnij Enter aby wrócić do menu...")
    
    def run(self):
        """Główna pętla programu"""
        self.print_banner()
        
        while True:
            choice = self.show_menu()
            
            if choice == '0':
                print("\n👋 Dzięki za użycie NSF MIGI_7G Hybrid!")
                break
            elif choice == '1':
                self.quick_demo()
            elif choice == '2':
                self.interactive_mode()
            elif choice == '3':
                self.test_all_primitives()
            elif choice == '4':
                self.archetype_transition_test()
            elif choice == '5':
                print("\n📊 Monitor w czasie rzeczywistym - w rozwoju")
                input("Naciśnij Enter...")
            elif choice == '6':
                print("\n💾 Zapis/Wczytaj stan - w rozwoju")
                input("Naciśnij Enter...")
            elif choice == '7':
                self.show_help()

if __name__ == "__main__":
    try:
        launcher = NSF_Launcher()
        launcher.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program przerwany przez użytkownika.")
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        import traceback
        traceback.print_exc()