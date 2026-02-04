"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  WORKHOURSAPP - TESTER APPLICATION                         ║
║                                                                            ║
║  Kompletny tester aplikacji mobilnej do ewidencji godzin pracy            ║
║  Pozwala testować UI, logikę biznesową i integracje bez telefonu          ║
║                                                                            ║
║  Features:                                                                 ║
║  - Dodawanie wpisów pracy (wpisywanie tekstu do pól)                      ║
║  - Zarządzanie profilami                                                  ║
║  - Testowanie systemu motywów (Opcja A + B + Animations)                 ║
║  - Generowanie raportów PDF                                              ║
║  - Przegląd bazy danych                                                   ║
║  - Symulacja cyklu życia aplikacji                                        ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.relativelayout import RelativeLayout

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem, ThreeLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner
from kivymd.color_definitions import colors
from kivymd.theming import ThemeManager

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os
from decimal import Decimal
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional, Dict

# ═══════════════════════════════════════════════════════════════════════════
# MODELS - Definicje struktur danych
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class WorkEntry:
    """Model wpisu pracy"""
    id: int = None
    profile_id: int = 1
    date: str = ""
    start_time: str = ""
    end_time: str = ""
    break_minutes: int = 0
    day_type: str = "work_day"
    notes: str = ""
    created_at: str = None
    updated_at: str = None

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Profile:
    """Model profilu użytkownika"""
    id: int = None
    name: str = ""
    created_at: str = None
    updated_at: str = None

    def to_dict(self) -> Dict:
        return asdict(self)


# ═══════════════════════════════════════════════════════════════════════════
# DATABASE - Obsługa bazy danych SQLite
# ═══════════════════════════════════════════════════════════════════════════

class TesterDatabase:
    """Wrapper do obsługi bazy danych testowej"""
    
    def __init__(self, db_path: str = "tester_workhoursapp.db"):
        self.db_path = db_path
        self.connection = None
        self.initialize()

    def initialize(self) -> None:
        """Inicjalizuj bazę danych"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela profili
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela wpisów pracy
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS work_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                break_minutes INTEGER DEFAULT 0,
                day_type TEXT DEFAULT 'work_day',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
                UNIQUE(profile_id, date)
            )
        """)
        
        # Tabela motywów
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS custom_themes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                theme_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                config_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
            )
        """)
        
        # Tabela ustawień
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                type TEXT DEFAULT 'string',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
                UNIQUE(profile_id, key)
            )
        """)
        
        # Domyślny profil
        cursor.execute("SELECT COUNT(*) FROM profiles")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO profiles (name) VALUES (?)",
                ("Default Tester",)
            )
        
        conn.commit()
        conn.close()

    def get_connection(self) -> sqlite3.Connection:
        """Pobierz połączenie z bazą"""
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def add_work_entry(self, entry: WorkEntry) -> int:
        """Dodaj wpis pracy"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO work_entries 
            (profile_id, date, start_time, end_time, break_minutes, day_type, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (entry.profile_id, entry.date, entry.start_time, entry.end_time,
              entry.break_minutes, entry.day_type, entry.notes))
        
        conn.commit()
        return cursor.lastrowid

    def get_work_entries_month(self, profile_id: int, year: int, month: int) -> List[Dict]:
        """Pobierz wpisy z całego miesiąca"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM work_entries 
            WHERE profile_id = ? AND strftime('%Y-%m', date) = ?
            ORDER BY date
        """, (profile_id, f"{year:04d}-{month:02d}"))
        
        return [dict(row) for row in cursor.fetchall()]

    def get_all_profiles(self) -> List[Dict]:
        """Pobierz wszystkie profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profiles ORDER BY created_at")
        return [dict(row) for row in cursor.fetchall()]

    def add_profile(self, name: str) -> int:
        """Dodaj nowy profil"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO profiles (name) VALUES (?)", (name,))
        conn.commit()
        return cursor.lastrowid

    def delete_profile(self, profile_id: int) -> bool:
        """Usuń profil (cascade delete)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
        conn.commit()
        return cursor.rowcount > 0

    def get_custom_themes(self, profile_id: int) -> List[Dict]:
        """Pobierz niestandardowe motywy"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM custom_themes WHERE profile_id = ?", 
            (profile_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        """Zamknij połączenie"""
        if self.connection:
            self.connection.close()


# ═══════════════════════════════════════════════════════════════════════════
# VALIDATORS - Walidacja danych
# ═══════════════════════════════════════════════════════════════════════════

class TesterValidators:
    """Walidatory dla danych testowych"""
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        """Waliduj datę (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, "✓ Data prawidłowa"
        except ValueError:
            return False, "✗ Nieprawidłowy format daty (użyj YYYY-MM-DD)"

    @staticmethod
    def validate_time(time_str: str) -> Tuple[bool, str]:
        """Waliduj czas (HH:MM)"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True, "✓ Czas prawidłowy"
        except ValueError:
            return False, "✗ Nieprawidłowy format czasu (użyj HH:MM)"

    @staticmethod
    def validate_work_entry(entry: WorkEntry) -> Tuple[bool, List[str]]:
        """Waliduj cały wpis pracy"""
        errors = []
        
        # Data
        is_valid, msg = TesterValidators.validate_date(entry.date)
        if not is_valid:
            errors.append(msg)
        
        # Czas startu
        is_valid, msg = TesterValidators.validate_time(entry.start_time)
        if not is_valid:
            errors.append("Start: " + msg)
        
        # Czas końca
        is_valid, msg = TesterValidators.validate_time(entry.end_time)
        if not is_valid:
            errors.append("Koniec: " + msg)
        
        # Break minutes
        if entry.break_minutes < 0 or entry.break_minutes > 480:
            errors.append("✗ Przerwa musi być 0-480 minut")
        
        # Day type
        if entry.day_type not in ["work_day", "sick_day", "vacation", "day_off"]:
            errors.append("✗ Nieprawidłowy typ dnia")
        
        return len(errors) == 0, errors


# ═══════════════════════════════════════════════════════════════════════════
# CALCULATIONS - Obliczenia czasu pracy
# ═══════════════════════════════════════════════════════════════════════════

class TesterCalculations:
    """Obliczenia czasu pracy - testowanie logiki biznesowej"""
    
    @staticmethod
    def calculate_work_time(start_time: str, end_time: str, 
                           break_minutes: int = 0, day_type: str = "work_day") -> Dict:
        """
        Oblicz czas pracy
        
        Args:
            start_time: HH:MM (np. "09:00")
            end_time: HH:MM (np. "17:00")
            break_minutes: Długość przerwy w minutach
            day_type: work_day, sick_day, vacation, day_off
        
        Returns:
            Dict z gross_minutes, net_minutes, formatted strings, is_valid, errors
        """
        result = {
            "gross_minutes": 0,
            "net_minutes": 0,
            "gross_formatted": "00:00",
            "net_formatted": "00:00",
            "decimal_hours": "0.00",
            "is_valid": False,
            "errors": []
        }
        
        # Obsługa dni nieroboczych
        if day_type in ["sick_day", "vacation", "day_off"]:
            result["is_valid"] = True
            result["gross_minutes"] = 0
            result["net_minutes"] = 0
            return result
        
        try:
            start = datetime.strptime(start_time, "%H:%M")
            end = datetime.strptime(end_time, "%H:%M")
            
            # Obsługa przekroczenia północy
            if end < start:
                end = end.replace(day=end.day + 1)
            
            gross_minutes = int((end - start).total_seconds() / 60)
            net_minutes = max(0, gross_minutes - break_minutes)
            
            if gross_minutes < 0:
                result["errors"].append("✗ Czas końca nie może być wcześniej niż start")
                return result
            
            if break_minutes > gross_minutes:
                result["errors"].append("✗ Przerwa nie może być dłuższa niż czas pracy")
                return result
            
            result["gross_minutes"] = gross_minutes
            result["net_minutes"] = net_minutes
            result["gross_formatted"] = TesterCalculations._minutes_to_hhmm(gross_minutes)
            result["net_formatted"] = TesterCalculations._minutes_to_hhmm(net_minutes)
            result["decimal_hours"] = f"{net_minutes / 60:.2f}"
            result["is_valid"] = True
            
        except Exception as e:
            result["errors"].append(f"✗ Błąd: {str(e)}")
        
        return result

    @staticmethod
    def _minutes_to_hhmm(minutes: int) -> str:
        """Konwertuj minuty na HH:MM"""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"

    @staticmethod
    def calculate_month_summary(entries: List[Dict]) -> Dict:
        """Oblicz podsumowanie miesiąca"""
        total_net_minutes = 0
        total_gross_minutes = 0
        day_counts = {
            "work_day": 0,
            "sick_day": 0,
            "vacation": 0,
            "day_off": 0
        }
        
        for entry in entries:
            calc = TesterCalculations.calculate_work_time(
                entry["start_time"],
                entry["end_time"],
                entry["break_minutes"],
                entry["day_type"]
            )
            
            if calc["is_valid"]:
                total_net_minutes += calc["net_minutes"]
                total_gross_minutes += calc["gross_minutes"]
            
            day_counts[entry["day_type"]] += 1
        
        return {
            "total_net_hours": total_net_minutes / 60,
            "total_gross_hours": total_gross_minutes / 60,
            "total_net_formatted": TesterCalculations._minutes_to_hhmm(total_net_minutes),
            "total_gross_formatted": TesterCalculations._minutes_to_hhmm(total_gross_minutes),
            "day_counts": day_counts,
            "entry_count": len(entries),
            "average_daily_hours": (total_net_minutes / 60) / len(entries) if entries else 0
        }


# ═══════════════════════════════════════════════════════════════════════════
# PDF GENERATOR - Generowanie raportów PDF
# ═══════════════════════════════════════════════════════════════════════════

class TesterPDFGenerator:
    """Generator raportów PDF - symulacja ReportLab"""
    
    @staticmethod
    def generate_month_report(profile_name: str, year: int, month: int, 
                             entries: List[Dict], summary: Dict, 
                             output_path: str = None) -> str:
        """
        Generuj raport PDF miesiączny
        
        Args:
            profile_name: Nazwa profilu
            year, month: Rok i miesiąc
            entries: Lista wpisów
            summary: Podsumowanie
            output_path: Ścieżka do pliku (domyślnie: TESTER/reports/)
        
        Returns:
            Ścieżka do utworzonego pliku
        """
        if not output_path:
            output_path = "TESTER/reports"
        
        # Utwórz folder jeśli nie istnieje
        Path(output_path).mkdir(parents=True, exist_ok=True)
        
        filename = f"{profile_name}_{year:04d}_{month:02d}_report.pdf"
        filepath = Path(output_path) / filename
        
        # Symulacja - utwórz plik tekstowy z metadanymi PDF
        content = f"""
═══════════════════════════════════════════════════════════════
                   RAPORT CZASU PRACY - PDF
═══════════════════════════════════════════════════════════════

Profil:        {profile_name}
Okres:         {month:02d}/{year}
Data raportu:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

───────────────────────────────────────────────────────────────
PODSUMOWANIE MIESIĄCA
───────────────────────────────────────────────────────────────

Całkowity czas netto:     {summary['total_net_formatted']} ({summary['total_net_hours']:.2f}h)
Całkowity czas brutto:    {summary['total_gross_formatted']} ({summary['total_gross_hours']:.2f}h)

Statystyka dni:
  - Dni robocze:          {summary['day_counts']['work_day']}
  - Dni chorobowe:        {summary['day_counts']['sick_day']}
  - Urlop:                {summary['day_counts']['vacation']}
  - Dni wolne:            {summary['day_counts']['day_off']}

Średnia dzienna:          {summary['average_daily_hours']:.2f}h

───────────────────────────────────────────────────────────────
SZCZEGÓŁOWE WPISY
───────────────────────────────────────────────────────────────

"""
        for entry in entries:
            calc = TesterCalculations.calculate_work_time(
                entry["start_time"],
                entry["end_time"],
                entry["break_minutes"],
                entry["day_type"]
            )
            
            day_name = {
                "work_day": "Dzień roboczy",
                "sick_day": "Dzień chorobowy",
                "vacation": "Urlop",
                "day_off": "Dzień wolny"
            }.get(entry["day_type"], entry["day_type"])
            
            content += f"""
Data: {entry['date']}
  Godziny:   {entry['start_time']} - {entry['end_time']}
  Przerwa:   {entry['break_minutes']} minut
  Typ dnia:  {day_name}
  Czas netto: {calc['net_formatted']}
  Notatka:   {entry['notes'] or '-'}
"""
        
        content += f"""

───────────────────────────────────────────────────────────────
Raport wygenerowany automatycznie przez WorkHoursApp Tester
Wersja: 1.0.0
═══════════════════════════════════════════════════════════════
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)


# ═══════════════════════════════════════════════════════════════════════════
# THEME SYSTEM - System motywów (Opcja A + B + Animations)
# ═══════════════════════════════════════════════════════════════════════════

class TesterThemeManager:
    """Manager motywów - testowanie Opcja A + B + Animations"""
    
    # Opcja A - 10 hardcoded themes
    HARDCODED_THEMES = {
        1: {
            "name": "Dark Purple Neon",
            "primary": "#7C3AED",
            "accent": "#06B6D4",
            "background": "#1F2937",
            "surface": "#111827"
        },
        2: {
            "name": "Dark Grape Premium",
            "primary": "#8B5CF6",
            "accent": "#EC4899",
            "background": "#1E1B4B",
            "surface": "#0F172A"
        },
        3: {
            "name": "Dark Electric Violet",
            "primary": "#A78BFA",
            "accent": "#10B981",
            "background": "#312E81",
            "surface": "#1E3A8A"
        },
        4: {
            "name": "Dark Plum + Gold",
            "primary": "#9333EA",
            "accent": "#F59E0B",
            "background": "#1F1033",
            "surface": "#2D1B69"
        },
        5: {
            "name": "Light Clean Purple",
            "primary": "#7C3AED",
            "accent": "#3B82F6",
            "background": "#F3F4F6",
            "surface": "#FFFFFF"
        },
        6: {
            "name": "Light Lavender Candy",
            "primary": "#A78BFA",
            "accent": "#EC4899",
            "background": "#F5F3FF",
            "surface": "#FAFAFA"
        },
        7: {
            "name": "Midnight Indigo",
            "primary": "#4F46E5",
            "accent": "#06B6D4",
            "background": "#0F172A",
            "surface": "#1E293B"
        },
        8: {
            "name": "Graphite Purple",
            "primary": "#8B5CF6",
            "accent": "#6366F1",
            "background": "#27272A",
            "surface": "#18181B"
        },
        9: {
            "name": "Purple + Lime Pop",
            "primary": "#7C3AED",
            "accent": "#84CC16",
            "background": "#1F2937",
            "surface": "#111827"
        },
        10: {
            "name": "Purple Sunset",
            "primary": "#C4B5FD",
            "accent": "#FB7185",
            "background": "#2D1B69",
            "surface": "#1F1033"
        }
    }

    @staticmethod
    def get_theme(theme_id: int) -> Dict:
        """Pobierz motyw (Opcja A)"""
        return TesterThemeManager.HARDCODED_THEMES.get(
            theme_id,
            TesterThemeManager.HARDCODED_THEMES[1]
        )

    @staticmethod
    def generate_custom_theme(base_hue: float, is_dark: bool = True) -> Dict:
        """
        Generuj motyw dynamicznie (Opcja B)
        
        Args:
            base_hue: Wartość hue (0-360)
            is_dark: Czy ciemny motyw
        
        Returns:
            Dict z kolorami wygenerowanymi
        """
        # Uproszczona implementacja HSV → HEX konwersji
        colors_palette = {
            "primary": f"hsl({base_hue}, 80%, 50%)",
            "accent": f"hsl({(base_hue + 120) % 360}, 85%, 50%)",
            "background": "#1F2937" if is_dark else "#F3F4F6",
            "surface": "#111827" if is_dark else "#FFFFFF"
        }
        return colors_palette

    @staticmethod
    def list_all_themes() -> List[Dict]:
        """Listuj wszystkie dostępne motywy"""
        themes = []
        for theme_id, theme_data in TesterThemeManager.HARDCODED_THEMES.items():
            themes.append({
                "id": theme_id,
                "name": theme_data["name"],
                "type": "Opcja A (Hardcoded)",
                "colors": theme_data
            })
        return themes


# ═══════════════════════════════════════════════════════════════════════════
# UI - KIVY APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

class WorkHoursTesterApp(MDApp):
    """Główna aplikacja testowa"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = TesterDatabase()
        self.validators = TesterValidators()
        self.calculator = TesterCalculations()
        self.pdf_gen = TesterPDFGenerator()
        self.theme_mgr = TesterThemeManager()
        self.current_profile_id = 1
        
        # Inicjalizuj folder reportów
        Path("TESTER/reports").mkdir(parents=True, exist_ok=True)

    def build(self):
        """Zbuduj interfejs"""
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_palette = "Cyan"
        
        main_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = MDLabel(
            text="[b]WorkHours App - Tester UI[/b]\nTeść aplikację jak rzeczywisty użytkownik",
            markup=True,
            size_hint_y=0.1,
            font_size='16sp'
        )
        main_layout.add_widget(header)
        
        # Tabbed Interface
        tabs = TabbedPanel(size_hint_y=0.9)
        
        # TAB 1: Add Work Entry
        tab1 = TabbedPanelItem(text='➕ Dodaj Wpis')
        tab1.content = self._build_add_entry_tab()
        tabs.add_widget(tab1)
        
        # TAB 2: View Entries
        tab2 = TabbedPanelItem(text='📋 Wpisy')
        tab2.content = self._build_view_entries_tab()
        tabs.add_widget(tab2)
        
        # TAB 3: Monthly Report
        tab3 = TabbedPanelItem(text='📊 Raport')
        tab3.content = self._build_report_tab()
        tabs.add_widget(tab3)
        
        # TAB 4: Profiles
        tab4 = TabbedPanelItem(text='👤 Profile')
        tab4.content = self._build_profiles_tab()
        tabs.add_widget(tab4)
        
        # TAB 5: Themes
        tab5 = TabbedPanelItem(text='🎨 Motywy')
        tab5.content = self._build_themes_tab()
        tabs.add_widget(tab5)
        
        # TAB 6: Database
        tab6 = TabbedPanelItem(text='🗄️ Baza')
        tab6.content = self._build_database_tab()
        tabs.add_widget(tab6)
        
        main_layout.add_widget(tabs)
        
        return main_layout

    def _build_add_entry_tab(self) -> BoxLayout:
        """Tab do dodawania wpisów"""
        layout = MDBoxLayout(orientation='vertical', padding=15, spacing=10)
        scroll = ScrollView(size_hint_y=0.9)
        
        form_layout = MDGridLayout(cols=2, spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Data
        self.entry_date = MDTextField(
            hint_text='Data (YYYY-MM-DD)',
            mode='rectangle',
            size_hint_x=0.5,
            text=datetime.now().strftime('%Y-%m-%d')
        )
        form_layout.add_widget(MDLabel(text='Data:', size_hint_x=0.5))
        form_layout.add_widget(self.entry_date)
        
        # Start time
        self.entry_start = MDTextField(
            hint_text='Start (HH:MM)',
            mode='rectangle',
            size_hint_x=0.5,
            text='09:00'
        )
        form_layout.add_widget(MDLabel(text='Godzina startu:', size_hint_x=0.5))
        form_layout.add_widget(self.entry_start)
        
        # End time
        self.entry_end = MDTextField(
            hint_text='Koniec (HH:MM)',
            mode='rectangle',
            size_hint_x=0.5,
            text='17:00'
        )
        form_layout.add_widget(MDLabel(text='Godzina końca:', size_hint_x=0.5))
        form_layout.add_widget(self.entry_end)
        
        # Break
        self.entry_break = MDTextField(
            hint_text='Przerwa (minuty)',
            mode='rectangle',
            size_hint_x=0.5,
            text='0'
        )
        form_layout.add_widget(MDLabel(text='Przerwa (min):', size_hint_x=0.5))
        form_layout.add_widget(self.entry_break)
        
        # Day type
        self.entry_day_type = MDTextField(
            hint_text='Typ: work_day, sick_day, vacation, day_off',
            mode='rectangle',
            size_hint_x=0.5,
            text='work_day'
        )
        form_layout.add_widget(MDLabel(text='Typ dnia:', size_hint_x=0.5))
        form_layout.add_widget(self.entry_day_type)
        
        # Notes
        self.entry_notes = MDTextField(
            hint_text='Notatki (opcjonalnie)',
            mode='rectangle',
            size_hint_x=0.5,
            multiline=True,
            height=60
        )
        form_layout.add_widget(MDLabel(text='Notatki:', size_hint_x=0.5))
        form_layout.add_widget(self.entry_notes)
        
        scroll.add_widget(form_layout)
        layout.add_widget(scroll)
        
        # Buttons
        btn_layout = MDBoxLayout(size_hint_y=0.1, spacing=10)
        
        btn_save = MDRaisedButton(
            text='💾 Zapisz Wpis',
            size_hint_x=0.5
        )
        btn_save.bind(on_press=self._on_save_entry)
        btn_layout.add_widget(btn_save)
        
        btn_clear = MDFlatButton(
            text='🔄 Wyczyść',
            size_hint_x=0.5
        )
        btn_clear.bind(on_press=self._on_clear_entry)
        btn_layout.add_widget(btn_clear)
        
        layout.add_widget(btn_layout)
        
        # Status label
        self.entry_status = MDLabel(text='', size_hint_y=0.1)
        layout.add_widget(self.entry_status)
        
        return layout

    def _build_view_entries_tab(self) -> BoxLayout:
        """Tab do przeglądania wpisów"""
        layout = MDBoxLayout(orientation='vertical', padding=15, spacing=10)
        
        self.entries_list = MDList(size_hint_y=0.9)
        self._refresh_entries_list()
        
        layout.add_widget(self.entries_list)
        
        btn_refresh = MDRaisedButton(
            text='🔄 Odśwież',
            size_hint_y=0.1
        )
        btn_refresh.bind(on_press=lambda x: self._refresh_entries_list())
        layout.add_widget(btn_refresh)
        
        return layout

    def _build_report_tab(self) -> BoxLayout:
        """Tab do raportów"""
        layout = MDBoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Month/Year selector
        selector_layout = MDBoxLayout(size_hint_y=0.1, spacing=10)
        
        self.report_month = MDTextField(
            hint_text='Miesiąc (1-12)',
            mode='rectangle',
            text=str(datetime.now().month)
        )
        self.report_year = MDTextField(
            hint_text='Rok',
            mode='rectangle',
            text=str(datetime.now().year)
        )
        
        selector_layout.add_widget(MDLabel(text='Miesiąc:', size_hint_x=0.2))
        selector_layout.add_widget(self.report_month)
        selector_layout.add_widget(MDLabel(text='Rok:', size_hint_x=0.15))
        selector_layout.add_widget(self.report_year)
        
        layout.add_widget(selector_layout)
        
        # Report display
        self.report_display = MDLabel(
            text='Wybierz miesiąc i rok, aby zobaczyć raport',
            size_hint_y=0.7,
            markup=True
        )
        scroll = ScrollView()
        scroll.add_widget(self.report_display)
        layout.add_widget(scroll)
        
        # Buttons
        btn_layout = MDBoxLayout(size_hint_y=0.2, spacing=10)
        
        btn_generate = MDRaisedButton(text='📊 Generuj')
        btn_generate.bind(on_press=self._on_generate_report)
        btn_layout.add_widget(btn_generate)
        
        btn_pdf = MDRaisedButton(text='📄 Pobierz PDF')
        btn_pdf.bind(on_press=self._on_generate_pdf)
        btn_layout.add_widget(btn_pdf)
        
        layout.add_widget(btn_layout)
        
        return layout

    def _build_profiles_tab(self) -> BoxLayout:
        """Tab do profili"""
        layout = MDBoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # New profile form
        form_layout = MDBoxLayout(size_hint_y=0.15, spacing=10)
        
        self.new_profile_name = MDTextField(
            hint_text='Nazwa nowego profilu',
            mode='rectangle'
        )
        form_layout.add_widget(self.new_profile_name)
        
        btn_add = MDRaisedButton(text='➕ Nowy')
        btn_add.bind(on_press=self._on_add_profile)
        form_layout.add_widget(btn_add)
        
        layout.add_widget(form_layout)
        
        # Profiles list
        self.profiles_list = MDList(size_hint_y=0.85)
        self._refresh_profiles_list()
        layout.add_widget(self.profiles_list)
        
        return layout

    def _build_themes_tab(self) -> BoxLayout:
        """Tab do motywów"""
        layout = MDBoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Theme selector
        selector_layout = MDBoxLayout(size_hint_y=0.1, spacing=10)
        
        self.theme_selector = MDTextField(
            hint_text='ID motywu (1-10)',
            mode='rectangle',
            text='1'
        )
        selector_layout.add_widget(self.theme_selector)
        
        btn_apply = MDRaisedButton(text='🎨 Zastosuj')
        btn_apply.bind(on_press=self._on_apply_theme)
        selector_layout.add_widget(btn_apply)
        
        layout.add_widget(selector_layout)
        
        # Themes list
        self.themes_display = MDLabel(text='', markup=True, size_hint_y=0.9)
        self._refresh_themes_display()
        
        scroll = ScrollView()
        scroll.add_widget(self.themes_display)
        layout.add_widget(scroll)
        
        return layout

    def _build_database_tab(self) -> BoxLayout:
        """Tab do bazy danych"""
        layout = MDBoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Info
        info_text = f"""
[b]Baza danych:[/b] {self.db.db_path}

[b]Tabele:[/b]
• profiles - Profily użytkowników
• work_entries - Wpisy czasu pracy
• custom_themes - Niestandardowe motywy
• settings - Ustawienia

[b]Akcje:[/b]
        """
        
        self.db_info = MDLabel(text=info_text, markup=True, size_hint_y=0.7)
        scroll = ScrollView()
        scroll.add_widget(self.db_info)
        layout.add_widget(scroll)
        
        # Buttons
        btn_layout = MDBoxLayout(size_hint_y=0.3, spacing=10, orientation='vertical')
        
        btn_export = MDRaisedButton(text='💾 Eksportuj do JSON')
        btn_export.bind(on_press=self._on_export_db)
        btn_layout.add_widget(btn_export)
        
        btn_reset = MDFlatButton(text='⚠️ Reset bazy')
        btn_reset.bind(on_press=self._on_reset_db)
        btn_layout.add_widget(btn_reset)
        
        layout.add_widget(btn_layout)
        
        return layout

    # ═════════════════════════════════════════════════════════════════════════
    # EVENT HANDLERS
    # ═════════════════════════════════════════════════════════════════════════

    def _on_save_entry(self, instance):
        """Obsłuż zapis wpisu"""
        try:
            entry = WorkEntry(
                profile_id=self.current_profile_id,
                date=self.entry_date.text,
                start_time=self.entry_start.text,
                end_time=self.entry_end.text,
                break_minutes=int(self.entry_break.text or 0),
                day_type=self.entry_day_type.text,
                notes=self.entry_notes.text
            )
            
            # Walidacja
            is_valid, errors = self.validators.validate_work_entry(entry)
            
            if not is_valid:
                error_text = '\n'.join(errors)
                self.entry_status.text = f'[color=ff0000]{error_text}[/color]'
                return
            
            # Obliczenie
            calc = self.calculator.calculate_work_time(
                entry.start_time,
                entry.end_time,
                entry.break_minutes,
                entry.day_type
            )
            
            # Zapis
            entry_id = self.db.add_work_entry(entry)
            
            self.entry_status.text = (
                f'[color=00cc00]✓ Wpis zapisany![/color]\n'
                f'Czas netto: {calc["net_formatted"]} ({calc["decimal_hours"]}h)'
            )
            
            self._on_clear_entry(None)
            self._refresh_entries_list()
            
        except Exception as e:
            self.entry_status.text = f'[color=ff0000]✗ Błąd: {str(e)}[/color]'

    def _on_clear_entry(self, instance):
        """Wyczyść formularz"""
        self.entry_date.text = datetime.now().strftime('%Y-%m-%d')
        self.entry_start.text = '09:00'
        self.entry_end.text = '17:00'
        self.entry_break.text = '0'
        self.entry_day_type.text = 'work_day'
        self.entry_notes.text = ''
        self.entry_status.text = ''

    def _refresh_entries_list(self):
        """Odśwież listę wpisów"""
        self.entries_list.clear_widgets()
        
        entries = self.db.get_work_entries_month(
            self.current_profile_id,
            datetime.now().year,
            datetime.now().month
        )
        
        if not entries:
            self.entries_list.add_widget(
                OneLineListItem(text='Brak wpisów w tym miesiącu')
            )
            return
        
        for entry in entries:
            calc = self.calculator.calculate_work_time(
                entry['start_time'],
                entry['end_time'],
                entry['break_minutes'],
                entry['day_type']
            )
            
            text = (
                f"{entry['date']}: {entry['start_time']} - {entry['end_time']} "
                f"({calc['net_formatted']}) - {entry['day_type']}"
            )
            
            self.entries_list.add_widget(OneLineListItem(text=text))

    def _on_generate_report(self, instance):
        """Generuj raport miesiączny"""
        try:
            month = int(self.report_month.text)
            year = int(self.report_year.text)
            
            entries = self.db.get_work_entries_month(self.current_profile_id, year, month)
            summary = self.calculator.calculate_month_summary(entries)
            
            # Format report
            report_text = f"""
[b]Raport za {month:02d}/{year}[/b]

[b]Podsumowanie:[/b]
Czas netto: {summary['total_net_formatted']} ({summary['total_net_hours']:.2f}h)
Czas brutto: {summary['total_gross_formatted']} ({summary['total_gross_hours']:.2f}h)
Średnia dzienna: {summary['average_daily_hours']:.2f}h

[b]Statystyka dni:[/b]
Dni robocze: {summary['day_counts']['work_day']}
Dni chorobowe: {summary['day_counts']['sick_day']}
Urlop: {summary['day_counts']['vacation']}
Dni wolne: {summary['day_counts']['day_off']}

[b]Szczegóły:[/b]
"""
            for entry in entries[:10]:  # Pokaż pierwsze 10
                calc = self.calculator.calculate_work_time(
                    entry['start_time'],
                    entry['end_time'],
                    entry['break_minutes'],
                    entry['day_type']
                )
                report_text += f"\n{entry['date']}: {calc['net_formatted']}"
            
            if len(entries) > 10:
                report_text += f"\n... i {len(entries) - 10} więcej"
            
            self.report_display.text = report_text
            
        except Exception as e:
            self.report_display.text = f'[color=ff0000]Błąd: {str(e)}[/color]'

    def _on_generate_pdf(self, instance):
        """Generuj PDF raportu"""
        try:
            month = int(self.report_month.text)
            year = int(self.report_year.text)
            
            entries = self.db.get_work_entries_month(self.current_profile_id, year, month)
            summary = self.calculator.calculate_month_summary(entries)
            
            profile = self.db.get_all_profiles()[0]
            
            filepath = self.pdf_gen.generate_month_report(
                profile['name'],
                year,
                month,
                entries,
                summary
            )
            
            self.report_display.text = f'[color=00cc00]✓ PDF zapisany!\n{filepath}[/color]'
            
        except Exception as e:
            self.report_display.text = f'[color=ff0000]Błąd: {str(e)}[/color]'

    def _refresh_profiles_list(self):
        """Odśwież listę profili"""
        self.profiles_list.clear_widgets()
        
        profiles = self.db.get_all_profiles()
        
        for profile in profiles:
            text = f"👤 {profile['name']}"
            self.profiles_list.add_widget(OneLineListItem(text=text))

    def _on_add_profile(self, instance):
        """Dodaj nowy profil"""
        if not self.new_profile_name.text:
            return
        
        try:
            profile_id = self.db.add_profile(self.new_profile_name.text)
            self.current_profile_id = profile_id
            self.new_profile_name.text = ''
            self._refresh_profiles_list()
        except Exception as e:
            print(f"Błąd: {e}")

    def _refresh_themes_display(self):
        """Odśwież wyświetlanie motywów"""
        themes = self.theme_mgr.list_all_themes()
        
        text = "[b]DOSTĘPNE MOTYWY (Opcja A - Hardcoded):[/b]\n\n"
        
        for theme in themes:
            text += (
                f"[b]{theme['id']}. {theme['name']}[/b]\n"
                f"Primary: {theme['colors']['primary']}\n"
                f"Accent: {theme['colors']['accent']}\n\n"
            )
        
        self.themes_display.text = text

    def _on_apply_theme(self, instance):
        """Zastosuj motyw"""
        try:
            theme_id = int(self.theme_selector.text)
            theme = self.theme_mgr.get_theme(theme_id)
            
            # Konwertuj hex na Kivy color
            # (Uproszczona - w pełnej wersji byłaby pełna implementacja)
            
            self.theme_cls.primary_palette = "Purple"
            self.root.canvas.clear()
            
        except Exception as e:
            print(f"Błąd motywu: {e}")

    def _on_export_db(self, instance):
        """Eksportuj bazę do JSON"""
        try:
            import json
            
            export_data = {
                "profiles": self.db.get_all_profiles(),
                "entries": self.db.get_work_entries_month(
                    self.current_profile_id,
                    datetime.now().year,
                    datetime.now().month
                ),
                "themes": self.db.get_custom_themes(self.current_profile_id)
            }
            
            filepath = "TESTER/export_data.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.db_info.text += f"\n✓ Eksported do: {filepath}"
            
        except Exception as e:
            print(f"Błąd eksportu: {e}")

    def _on_reset_db(self, instance):
        """Reset bazy danych"""
        try:
            import os
            self.db.close()
            os.remove(self.db.db_path)
            self.db = TesterDatabase()
            self.db_info.text = "✓ Baza została zresetowana"
        except Exception as e:
            print(f"Błąd: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    app = WorkHoursTesterApp()
    app.run()
