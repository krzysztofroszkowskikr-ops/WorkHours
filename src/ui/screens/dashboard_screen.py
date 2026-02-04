"""
DashboardScreen - Przegląd miesiąca i statystyki
"""

from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
import logging

logger = logging.getLogger(__name__)


class StatsCard(MDCard):
    """Karta ze statystyką"""
    
    def __init__(self, title: str, value: str, unit: str = "", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = '16dp'
        self.spacing = '8dp'
        self.size_hint_y = None
        self.height = '120dp'
        self.elevation = 2
        self.radius = '12dp'
        
        # Tytuł
        title_label = MDLabel(
            text=title,
            size_hint_y = None,
            height = '24dp',
            font_size = '14sp'
        )
        self.add_widget(title_label)
        
        # Wartość
        value_label = MDLabel(
            text=f"{value} {unit}",
            size_hint_y = None,
            height = '32dp',
            font_size = '28sp',
            bold = True
        )
        self.add_widget(value_label)


class DashboardScreen(Screen):
    """
    Ekran Dashboard
    
    Wyświetla:
    - Przegląd miesiąca (dni, godziny)
    - Statystyki
    - Ostatnie wpisy
    - Szybki dostęp do akcji
    """
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
        # Główny layout
        self.main_layout = MDBoxLayout(orientation='vertical', padding='16dp', spacing='12dp')
        self.add_widget(self.main_layout)
        
        # Załaduj UI
        self.load_ui()
    
    def load_ui(self):
        """Załaduj UI ekranu"""
        logger.info("Ładowanie Dashboard...")
        
        # Tytuł z miesiącem
        month_label = MDLabel(
            text=self._get_month_title(),
            size_hint_y = None,
            height = '40dp',
            font_size = '24sp',
            bold = True
        )
        self.main_layout.add_widget(month_label)
        
        # Pobierz dane
        from src.repository import WorkEntryRepository
        repo = WorkEntryRepository(self.app.app_context.database)
        entries = repo.get_month(
            self.app.app_context.get_current_profile_id(),
            self.current_year,
            self.current_month
        )
        
        # Oblicz statystyki
        results = []
        for entry in entries:
            result = self.app.app_context.calc_service.calculate_work_day(
                date=entry.date,
                start_time=entry.start_time if entry.start_time else None,
                end_time=entry.end_time if entry.end_time else None,
                break_minutes=entry.break_minutes,
                day_type=entry.day_type
            )
            if result.is_valid:
                results.append(result)
        
        summary = self.app.app_context.calc_service.calculate_month_summary(results)
        
        # Stats Grid
        stats_grid = MDGridLayout(
            cols=3,
            spacing='8dp',
            size_hint_y = None,
            height = '140dp'
        )
        
        stats_grid.add_widget(StatsCard("Całkowity czas", summary.total_work_hours_hm, "h"))
        stats_grid.add_widget(StatsCard("Dni pracujące", str(summary.work_days), ""))
        stats_grid.add_widget(StatsCard("Średnia/dzień", f"{summary.average_daily_hours}", "h"))
        
        self.main_layout.add_widget(stats_grid)
        
        # Szczegóły
        details_layout = MDBoxLayout(orientation='vertical', spacing='8dp', size_hint_y=None, height='200dp')
        
        details_label = MDLabel(
            text=f"Dni chorobowe: {summary.sick_days} | Urlopy: {summary.vacation_days} | Dni wolne: {summary.day_offs}",
            size_hint_y = None,
            height = '32dp',
            font_size = '14sp'
        )
        details_layout.add_widget(details_label)
        
        # Ostatnie wpisy
        entries_label = MDLabel(
            text="Ostatnie wpisy:",
            size_hint_y = None,
            height = '24dp',
            font_size = '16sp',
            bold = True
        )
        details_layout.add_widget(entries_label)
        
        # Lista ostatnich wpisów
        for entry in entries[-3:]:
            entry_text = f"{entry.date}: {entry.start_time}-{entry.end_time if entry.end_time else 'wolne'}"
            entry_label = MDLabel(
                text=entry_text,
                size_hint_y = None,
                height = '24dp',
                font_size = '12sp'
            )
            details_layout.add_widget(entry_label)
        
        self.main_layout.add_widget(details_layout)
        
        # Przyciski akcji
        actions_layout = MDBoxLayout(spacing='8dp', size_hint_y=None, height='56dp')
        
        add_entry_btn = MDRaisedButton(text="+ Dodaj wpis", size_hint_x=0.5)
        add_entry_btn.bind(on_release=lambda x: self.app.switch_screen('entry'))
        actions_layout.add_widget(add_entry_btn)
        
        view_report_btn = MDRaisedButton(text="📄 Raport", size_hint_x=0.5)
        view_report_btn.bind(on_release=lambda x: self.app.switch_screen('report'))
        actions_layout.add_widget(view_report_btn)
        
        self.main_layout.add_widget(actions_layout)
        
        # ScrollView dla reszty
        scroll = MDScrollView()
        scroll.add_widget(MDBoxLayout(size_hint_y=None, height='100dp'))
        self.main_layout.add_widget(scroll)
        
        logger.info("Dashboard załadowany")
    
    def _get_month_title(self) -> str:
        """Zwróć tytuł miesiąca"""
        months = [
            "Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
            "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"
        ]
        return f"{months[self.current_month-1]} {self.current_year}"
    
    def on_enter(self):
        """Odśwież ekran przy wejściu"""
        logger.info("Dashboard: on_enter")
        self.main_layout.clear_widgets()
        self.load_ui()


__all__ = ['DashboardScreen']
