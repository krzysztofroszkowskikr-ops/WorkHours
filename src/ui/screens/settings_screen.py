"""
SettingsScreen - Ustawienia aplikacji
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.scrollview import MDScrollView
import logging

logger = logging.getLogger(__name__)


class SettingsScreen(Screen):
    """
    Ekran ustawień aplikacji
    
    Opcje:
    - Wybór profilu
    - Wybór motywu
    - Informacje o aplikacji
    """
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        
        # Kontrolki
        self.profile_spinner = None
        self.theme_spinner = None
        
        # Załaduj UI
        self.load_ui()
    
    def load_ui(self):
        """Załaduj UI ekranu"""
        logger.info("Ładowanie Settings Screen...")
        
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
            text="Ustawienia",
            size_hint_y=None,
            height='40dp',
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)
        
        # PROFIL
        profile_label = MDLabel(
            text="Profil użytkownika",
            size_hint_y=None,
            height='24dp',
            font_size='16sp',
            bold=True
        )
        layout.add_widget(profile_label)
        
        profile_card = MDCard(padding='8dp', spacing='8dp', size_hint_y=None, height='56dp')
        profile_layout = MDBoxLayout(spacing='8dp')
        profile_layout.add_widget(MDLabel(text="Profil:", size_hint_x=0.3))
        
        # Pobierz dostępne profile
        from src.repository import ProfileRepository
        profile_repo = ProfileRepository(self.app.app_context.database)
        profiles = profile_repo.get_all() or []
        profile_names = [p.name for p in profiles] if profiles else ["brak"]
        current_profile_id = self.app.app_context.get_current_profile_id()
        current_profile = next((p for p in profiles if p.id == current_profile_id), None)
        
        self.profile_spinner = MDSpinner(
            text=current_profile.name if current_profile else "brak",
            values=profile_names,
            size_hint_x=0.7
        )
        self.profile_spinner.bind(text=self.on_profile_selected)
        profile_layout.add_widget(self.profile_spinner)
        profile_card.add_widget(profile_layout)
        layout.add_widget(profile_card)
        
        # MOTYW
        theme_label = MDLabel(
            text="Motyw",
            size_hint_y=None,
            height='24dp',
            font_size='16sp',
            bold=True
        )
        layout.add_widget(theme_label)
        
        theme_card = MDCard(padding='8dp', spacing='8dp', size_hint_y=None, height='56dp')
        theme_layout = MDBoxLayout(spacing='8dp')
        theme_layout.add_widget(MDLabel(text="Motyw:", size_hint_x=0.3))
        
        themes = [
            'Material Light',
            'Material Dark',
            'Ocean Blue',
            'Forest Green',
            'Sunset Purple',
            'Autumn Orange',
            'Slate Gray',
            'Deep Red',
            'Indigo Blue',
            'Teal Modern'
        ]
        
        self.theme_spinner = MDSpinner(
            text='Material Light',
            values=themes,
            size_hint_x=0.7
        )
        self.theme_spinner.bind(text=self.on_theme_selected)
        theme_layout.add_widget(self.theme_spinner)
        theme_card.add_widget(theme_layout)
        layout.add_widget(theme_card)
        
        # INFORMACJE
        info_label = MDLabel(
            text="Informacje",
            size_hint_y=None,
            height='24dp',
            font_size='16sp',
            bold=True
        )
        layout.add_widget(info_label)
        
        info_card = MDCard(
            padding='16dp',
            spacing='8dp',
            orientation='vertical',
            size_hint_y=None,
            height='140dp'
        )
        
        info_layout = MDBoxLayout(orientation='vertical', spacing='8dp')
        info_layout.add_widget(MDLabel(
            text="WorkHours Application",
            size_hint_y=None,
            height='24dp',
            bold=True
        ))
        info_layout.add_widget(MDLabel(
            text="Wersja: 1.0.0",
            size_hint_y=None,
            height='24dp'
        ))
        info_layout.add_widget(MDLabel(
            text="Aplikacja do ewidencji godzin pracy",
            size_hint_y=None,
            height='24dp'
        ))
        info_layout.add_widget(MDLabel(
            text="Python 3.11 + Kivy + KivyMD",
            size_hint_y=None,
            height='24dp',
            font_size='12sp'
        ))
        
        info_card.add_widget(info_layout)
        layout.add_widget(info_card)
        
        # PRZYCISK PROFILI (do zarządzania)
        manage_profile_btn = MDRaisedButton(
            text="👥 Zarządzaj profilami",
            size_hint_y=None,
            height='56dp'
        )
        manage_profile_btn.bind(on_release=lambda x: self.app.switch_screen('profile'))
        layout.add_widget(manage_profile_btn)
        
        # PRZYCISK MOTYWÓW (do wyboru zaawansowanego)
        manage_theme_btn = MDRaisedButton(
            text="🎨 Więcej motywów",
            size_hint_y=None,
            height='56dp'
        )
        manage_theme_btn.bind(on_release=lambda x: self.app.switch_screen('theme'))
        layout.add_widget(manage_theme_btn)
        
        # POWRÓT
        back_btn = MDRaisedButton(text="◀️ Wróć", size_hint_y=None, height='56dp')
        back_btn.bind(on_release=lambda x: self.app.switch_screen('dashboard'))
        layout.add_widget(back_btn)
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
        
        logger.info("Settings Screen załadowany")
    
    def on_profile_selected(self, spinner, text):
        """Obsłuż zmianę profilu"""
        try:
            from src.repository import ProfileRepository
            repo = ProfileRepository(self.app.app_context.database)
            profiles = repo.get_all() or []
            
            selected_profile = next((p for p in profiles if p.name == text), None)
            if selected_profile:
                self.app.app_context.set_current_profile_id(selected_profile.id)
                logger.info(f"Profil zmieniony na: {text}")
        except Exception as e:
            logger.error(f"Błąd zmiany profilu: {e}")
    
    def on_theme_selected(self, spinner, text):
        """Obsłuż zmianę motywu"""
        try:
            logger.info(f"Motyw zmieniony na: {text}")
            # Tutaj będzie integracja z ThemeService
        except Exception as e:
            logger.error(f"Błąd zmiany motywu: {e}")


__all__ = ['SettingsScreen']
