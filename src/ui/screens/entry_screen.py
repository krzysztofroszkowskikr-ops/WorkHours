"""
EntryScreen - Dodawanie i edytowanie wpisów pracy
"""

from datetime import datetime, timedelta
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.datepicker import MDDatePicker
from kivymd.uix.popup import MDPopup
import logging

logger = logging.getLogger(__name__)


class EntryScreen(Screen):
    """
    Ekran dodawania/edytowania wpisu pracy
    
    Pola:
    - Data (datepicker)
    - Godzina rozpoczęcia
    - Godzina zakończenia
    - Przerwa (minuty)
    - Typ dnia
    - Notatki
    """
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        
        # Pola formularza
        self.date_field = None
        self.start_time_field = None
        self.end_time_field = None
        self.break_field = None
        self.day_type_spinner = None
        self.notes_field = None
        
        # Załaduj UI
        self.load_ui()
    
    def load_ui(self):
        """Załaduj UI ekranu"""
        logger.info("Ładowanie Entry Screen...")
        
        # Scroll view dla formularza
        scroll = MDScrollView()
        
        # Główny layout
        form_layout = MDBoxLayout(
            orientation='vertical',
            padding='16dp',
            spacing='12dp',
            size_hint_y=None
        )
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Tytuł
        title = MDLabel(
            text="Dodaj wpis pracy",
            size_hint_y = None,
            height = '40dp',
            font_size = '24sp',
            bold = True
        )
        form_layout.add_widget(title)
        
        # DATA
        date_card = MDCard(padding='8dp', spacing='8dp', size_hint_y=None, height='56dp')
        date_layout = MDBoxLayout(spacing='8dp')
        date_layout.add_widget(MDLabel(text="Data:", size_hint_x=0.3))
        
        self.date_field = MDTextField(
            hint_text="YYYY-MM-DD",
            mode="rectangle",
            text=datetime.now().strftime("%Y-%m-%d")
        )
        date_layout.add_widget(self.date_field)
        
        date_btn = MDRaisedButton(text="📅", size_hint_x=0.1, size_hint_y=1)
        date_btn.bind(on_release=self.show_datepicker)
        date_layout.add_widget(date_btn)
        
        date_card.add_widget(date_layout)
        form_layout.add_widget(date_card)
        
        # CZAS STARTU
        start_card = MDCard(padding='8dp', spacing='8dp', size_hint_y=None, height='56dp')
        start_layout = MDBoxLayout(spacing='8dp')
        start_layout.add_widget(MDLabel(text="Start:", size_hint_x=0.3))
        
        self.start_time_field = MDTextField(
            hint_text="HH:MM",
            mode="rectangle"
        )
        start_layout.add_widget(self.start_time_field)
        start_card.add_widget(start_layout)
        form_layout.add_widget(start_card)
        
        # CZAS KONCA
        end_card = MDCard(padding='8dp', spacing='8dp', size_hint_y=None, height='56dp')
        end_layout = MDBoxLayout(spacing='8dp')
        end_layout.add_widget(MDLabel(text="Koniec:", size_hint_x=0.3))
        
        self.end_time_field = MDTextField(
            hint_text="HH:MM",
            mode="rectangle"
        )
        end_layout.add_widget(self.end_time_field)
        end_card.add_widget(end_layout)
        form_layout.add_widget(end_card)
        
        # PRZERWA
        break_card = MDCard(padding='8dp', spacing='8dp', size_hint_y=None, height='56dp')
        break_layout = MDBoxLayout(spacing='8dp')
        break_layout.add_widget(MDLabel(text="Przerwa (min):", size_hint_x=0.3))
        
        self.break_field = MDTextField(
            hint_text="0",
            mode="rectangle",
            text="30"
        )
        break_layout.add_widget(self.break_field)
        break_card.add_widget(break_layout)
        form_layout.add_widget(break_card)
        
        # TYP DNIA
        type_card = MDCard(padding='8dp', spacing='8dp', size_hint_y=None, height='56dp')
        type_layout = MDBoxLayout(spacing='8dp')
        type_layout.add_widget(MDLabel(text="Typ dnia:", size_hint_x=0.3))
        
        self.day_type_spinner = MDSpinner(
            text='work_day',
            values=('work_day', 'sick_day', 'vacation', 'day_off'),
            size_hint_x=1
        )
        type_layout.add_widget(self.day_type_spinner)
        type_card.add_widget(type_layout)
        form_layout.add_widget(type_card)
        
        # NOTATKI
        notes_label = MDLabel(
            text="Notatki:",
            size_hint_y = None,
            height = '24dp'
        )
        form_layout.add_widget(notes_label)
        
        self.notes_field = MDTextField(
            hint_text="Opcjonalne notatki",
            mode="rectangle",
            multiline=True,
            size_hint_y = None,
            height = '100dp'
        )
        form_layout.add_widget(self.notes_field)
        
        # PRZYCISKI
        buttons_layout = MDBoxLayout(spacing='8dp', size_hint_y=None, height='56dp')
        
        save_btn = MDRaisedButton(text="💾 Zapisz", size_hint_x=0.5)
        save_btn.bind(on_release=self.save_entry)
        buttons_layout.add_widget(save_btn)
        
        cancel_btn = MDRaisedButton(text="❌ Anuluj", size_hint_x=0.5)
        cancel_btn.bind(on_release=lambda x: self.app.switch_screen('dashboard'))
        buttons_layout.add_widget(cancel_btn)
        
        form_layout.add_widget(buttons_layout)
        
        # Dodaj do scroll view
        scroll.add_widget(form_layout)
        self.add_widget(scroll)
        
        logger.info("Entry Screen załadowany")
    
    def show_datepicker(self, instance):
        """Pokaż datepicker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()
    
    def on_date_selected(self, instance, value, date_range):
        """Obsłuż wybranie daty"""
        self.date_field.text = str(value)
    
    def save_entry(self, instance):
        """Zapisz wpis"""
        from src.models import WorkEntry
        from src.repository import WorkEntryRepository
        
        try:
            # Pobierz wartości
            date = self.date_field.text
            start_time = self.start_time_field.text if self.start_time_field.text else None
            end_time = self.end_time_field.text if self.end_time_field.text else None
            break_min = int(self.break_field.text or 0)
            day_type = self.day_type_spinner.text
            notes = self.notes_field.text
            
            # Waliduj
            is_valid, msg = self.app.app_context.validators.is_valid_date(date)
            if not is_valid:
                logger.error(f"Błąd daty: {msg}")
                return
            
            if start_time and not self.app.app_context.validators.is_valid_time(start_time)[0]:
                logger.error("Błąd godziny startu")
                return
            
            if end_time and not self.app.app_context.validators.is_valid_time(end_time)[0]:
                logger.error("Błąd godziny końca")
                return
            
            # Utwórz wpis
            entry = WorkEntry(
                id=None,
                profile_id=self.app.app_context.get_current_profile_id(),
                date=date,
                start_time=start_time or "",
                end_time=end_time or "",
                break_minutes=break_min,
                day_type=day_type,
                notes=notes,
                created_at=None,
                updated_at=None
            )
            
            # Zapisz
            repo = WorkEntryRepository(self.app.app_context.database)
            repo.create(entry)
            
            logger.info(f"Wpis zapisany: {date}")
            
            # Powróć do dashboard
            self.app.switch_screen('dashboard')
            
        except Exception as e:
            logger.error(f"Błąd zapisywania wpisu: {e}")


__all__ = ['EntryScreen']
