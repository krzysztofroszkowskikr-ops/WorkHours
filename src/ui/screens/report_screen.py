"""
ReportScreen - Generowanie raportów PDF
"""

from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.scrollview import MDScrollView
import logging
import os

logger = logging.getLogger(__name__)


class ReportScreen(Screen):
    """
    Ekran generowania raportów PDF
    
    Funkcje:
    - Wybór miesiąca
    - Generowanie raportu miesięcznego
    - Generowanie raportu rocznego
    - Wyświetlenie ścieżki do pliku
    """
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        
        # Kontrolki
        self.month_spinner = None
        self.year_spinner = None
        self.report_path_label = None
        
        # Załaduj UI
        self.load_ui()
    
    def load_ui(self):
        """Załaduj UI ekranu"""
        logger.info("Ładowanie Report Screen...")
        
        # Scroll view
        scroll = MDScrollView()
        
        # Główny layout
        layout = MDBoxLayout(
            orientation='vertical',
            padding='16dp',
            spacing='12dp',
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))
        
        # Tytuł
        title = MDLabel(
            text="Generuj raporty",
            size_hint_y=None,
            height='40dp',
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)
        
        # WYBÓR MIESIĄCA
        month_card = MDCard(padding='8dp', spacing='8dp', size_hint_y=None, height='56dp')
        month_layout = MDBoxLayout(spacing='8dp')
        month_layout.add_widget(MDLabel(text="Miesiąc:", size_hint_x=0.3))
        
        months = [f"{i:02d}" for i in range(1, 13)]
        self.month_spinner = MDSpinner(
            text=f"{datetime.now().month:02d}",
            values=months,
            size_hint_x=0.7
        )
        month_layout.add_widget(self.month_spinner)
        month_card.add_widget(month_layout)
        layout.add_widget(month_card)
        
        # WYBÓR ROKU
        year_card = MDCard(padding='8dp', spacing='8dp', size_hint_y=None, height='56dp')
        year_layout = MDBoxLayout(spacing='8dp')
        year_layout.add_widget(MDLabel(text="Rok:", size_hint_x=0.3))
        
        current_year = datetime.now().year
        years = [str(y) for y in range(current_year - 5, current_year + 1)]
        self.year_spinner = MDSpinner(
            text=str(current_year),
            values=years,
            size_hint_x=0.7
        )
        year_layout.add_widget(self.year_spinner)
        year_card.add_widget(year_layout)
        layout.add_widget(year_card)
        
        # INFO CARD
        info_card = MDCard(
            padding='16dp',
            spacing='8dp',
            orientation='vertical',
            size_hint_y=None,
            height='120dp'
        )
        
        info_layout = MDBoxLayout(orientation='vertical', spacing='8dp')
        info_layout.add_widget(MDLabel(
            text="Raporty mają format PDF",
            size_hint_y=None,
            height='24dp'
        ))
        info_layout.add_widget(MDLabel(
            text="Zawierają statystyki pracy,",
            size_hint_y=None,
            height='24dp'
        ))
        info_layout.add_widget(MDLabel(
            text="urlopy, choroby, dni wolne",
            size_hint_y=None,
            height='24dp'
        ))
        
        self.report_path_label = MDLabel(
            text="Plik: -",
            size_hint_y=None,
            height='24dp',
            font_size='12sp'
        )
        info_layout.add_widget(self.report_path_label)
        
        info_card.add_widget(info_layout)
        layout.add_widget(info_card)
        
        # PRZYCISKI
        buttons_layout = MDBoxLayout(spacing='8dp', orientation='vertical', size_hint_y=None, height='112dp')
        
        monthly_btn = MDRaisedButton(text="📄 Raport miesięczny", size_hint_y=0.5)
        monthly_btn.bind(on_release=self.generate_monthly_report)
        buttons_layout.add_widget(monthly_btn)
        
        yearly_btn = MDRaisedButton(text="📊 Raport roczny", size_hint_y=0.5)
        yearly_btn.bind(on_release=self.generate_yearly_report)
        buttons_layout.add_widget(yearly_btn)
        
        layout.add_widget(buttons_layout)
        
        # POWRÓT
        back_btn = MDRaisedButton(text="◀️ Wróć", size_hint_y=None, height='56dp')
        back_btn.bind(on_release=lambda x: self.app.switch_screen('dashboard'))
        layout.add_widget(back_btn)
        
        # Dodaj do scroll
        scroll.add_widget(layout)
        self.add_widget(scroll)
        
        logger.info("Report Screen załadowany")
    
    def generate_monthly_report(self, instance):
        """Generuj raport miesięczny"""
        try:
            month = int(self.month_spinner.text)
            year = int(self.year_spinner.text)
            
            from src.services.pdf_service import PDFService
            from src.repository import WorkEntryRepository
            
            # Pobierz wpisy
            repo = WorkEntryRepository(self.app.app_context.database)
            profile_id = self.app.app_context.get_current_profile_id()
            
            # Filtruj wpisy
            all_entries = repo.get_all() or []
            month_entries = [
                e for e in all_entries
                if e.profile_id == profile_id and 
                   e.date.startswith(f"{year:04d}-{month:02d}")
            ]
            
            # Generuj PDF
            pdf_service = PDFService()
            output_dir = os.path.expanduser("~/.workhours/reports")
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"report_{year:04d}_{month:02d}.pdf"
            filepath = os.path.join(output_dir, filename)
            
            pdf_service.generate_monthly_report(
                month_entries,
                month,
                year,
                self.app.app_context.formatters,
                self.app.app_context.calc_service,
                filepath
            )
            
            self.report_path_label.text = f"Plik: {filepath}"
            logger.info(f"Raport generowany: {filepath}")
            
        except Exception as e:
            logger.error(f"Błąd generowania raportu: {e}")
            self.report_path_label.text = f"Błąd: {str(e)}"
    
    def generate_yearly_report(self, instance):
        """Generuj raport roczny"""
        try:
            year = int(self.year_spinner.text)
            
            from src.services.pdf_service import PDFService
            from src.repository import WorkEntryRepository
            
            # Pobierz wszystkie wpisy z roku
            repo = WorkEntryRepository(self.app.app_context.database)
            profile_id = self.app.app_context.get_current_profile_id()
            
            all_entries = repo.get_all() or []
            year_entries = [
                e for e in all_entries
                if e.profile_id == profile_id and 
                   e.date.startswith(f"{year:04d}")
            ]
            
            # Generuj PDF
            pdf_service = PDFService()
            output_dir = os.path.expanduser("~/.workhours/reports")
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"report_{year:04d}.pdf"
            filepath = os.path.join(output_dir, filename)
            
            pdf_service.generate_summary_report(
                year_entries,
                year,
                self.app.app_context.formatters,
                self.app.app_context.calc_service,
                filepath
            )
            
            self.report_path_label.text = f"Plik: {filepath}"
            logger.info(f"Raport roczny generowany: {filepath}")
            
        except Exception as e:
            logger.error(f"Błąd generowania raportu: {e}")
            self.report_path_label.text = f"Błąd: {str(e)}"


__all__ = ['ReportScreen']
