"""
WorkHours App - Testowa wersja bez złożonych kontrolek
Prosta, działająca aplikacja z Kivy + KivyMD minimum
"""

import logging
from pathlib import Path
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DashboardScreen(GridLayout):
    def __init__(self, app, **kwargs):
        super().__init__(cols=1, **kwargs)
        self.app = app
        self.add_widget(Label(text="🏢 Dashboard", size_hint_y=0.1, font_size='18sp', bold=True))
        self.add_widget(Label(text="Przegląd miesiąca\n[tu będą statystyki]", size_hint_y=0.8))
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        btn_add = Button(text='➕ Dodaj')
        btn_add.bind(on_press=lambda x: setattr(app.sm, 'current', 'entry'))
        btn_layout.add_widget(btn_add)
        btn_report = Button(text='📄 Raport')
        btn_report.bind(on_press=lambda x: setattr(app.sm, 'current', 'report'))
        btn_layout.add_widget(btn_report)
        self.add_widget(btn_layout)


class EntryScreen(GridLayout):
    def __init__(self, app, **kwargs):
        super().__init__(cols=1, **kwargs)
        self.app = app
        self.add_widget(Label(text="📝 Dodaj Wpis", size_hint_y=0.1, font_size='18sp', bold=True))
        self.add_widget(Label(text="Formularz dodawania wpisu\n[pola: data, start, koniec, typ]", size_hint_y=0.8))
        btn_back = Button(text='◀️ Wróć')
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'dashboard'))
        self.add_widget(btn_back)


class ReportScreen(GridLayout):
    def __init__(self, app, **kwargs):
        super().__init__(cols=1, **kwargs)
        self.app = app
        self.add_widget(Label(text="📄 Raporty", size_hint_y=0.1, font_size='18sp', bold=True))
        self.add_widget(Label(text="Generowanie raportów PDF\n[miejscem dla statystyk]", size_hint_y=0.8))
        btn_back = Button(text='◀️ Wróć')
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'dashboard'))
        self.add_widget(btn_back)


class SettingsScreen(GridLayout):
    def __init__(self, app, **kwargs):
        super().__init__(cols=1, **kwargs)
        self.app = app
        self.add_widget(Label(text="⚙️ Ustawienia", size_hint_y=0.1, font_size='18sp', bold=True))
        self.add_widget(Label(text="Profil, motyw, info\n[opcje]", size_hint_y=0.8))
        btn_back = Button(text='◀️ Wróć')
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'dashboard'))
        self.add_widget(btn_back)


class ProfileScreen(GridLayout):
    def __init__(self, app, **kwargs):
        super().__init__(cols=1, **kwargs)
        self.app = app
        self.add_widget(Label(text="👥 Profile", size_hint_y=0.1, font_size='18sp', bold=True))
        self.add_widget(Label(text="Zarządzanie profilami\n[lista, dodaj, usuń]", size_hint_y=0.8))
        btn_back = Button(text='◀️ Wróć')
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'settings'))
        self.add_widget(btn_back)


class ThemeScreen(GridLayout):
    def __init__(self, app, **kwargs):
        super().__init__(cols=1, **kwargs)
        self.app = app
        self.add_widget(Label(text="🎨 Motywy", size_hint_y=0.1, font_size='18sp', bold=True))
        self.add_widget(Label(text="Wybór kolorów aplikacji\n[10 opcji + custom]", size_hint_y=0.8))
        btn_back = Button(text='◀️ Wróć')
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'settings'))
        self.add_widget(btn_back)


class WorkHoursApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_context = None
        self.sm = None
    
    def build(self):
        logger.info("Inicjalizowanie WorkHours...")
        
        # Inicjalizuj backend
        from src.app_context import AppContext
        db_path = Path.home() / ".workhours" / "workhours_app.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.app_context = AppContext.get_instance(str(db_path))
        
        logger.info(f"Backend OK: {self.app_context.get_current_profile_name()}")
        
        # Główny layout
        main = BoxLayout(orientation='vertical')
        
        # Tytuł
        title = Label(text="🏢 WorkHours - Ewidencja Godzin", size_hint_y=0.08, font_size='16sp', bold=True)
        main.add_widget(title)
        
        # Screen Manager
        self.sm = ScreenManager()
        
        # Dodaj ekrany
        screens = [
            ('dashboard', DashboardScreen(self)),
            ('entry', EntryScreen(self)),
            ('report', ReportScreen(self)),
            ('settings', SettingsScreen(self)),
            ('profile', ProfileScreen(self)),
            ('theme', ThemeScreen(self)),
        ]
        
        for name, screen in screens:
            screen.name = name
            self.sm.add_widget(screen)
        
        self.sm.current = 'dashboard'
        main.add_widget(self.sm)
        
        # Menu dolne
        menu = BoxLayout(size_hint_y=0.1, spacing=2)
        for icon, screen_name in [('📊', 'dashboard'), ('📝', 'entry'), ('📄', 'report'), ('⚙️', 'settings')]:
            btn = Button(text=icon)
            btn.bind(on_press=lambda x, s=screen_name: setattr(self.sm, 'current', s))
            menu.add_widget(btn)
        
        main.add_widget(menu)
        
        logger.info("UI OK")
        return main
    
    def on_stop(self):
        logger.info("Zamykanie...")
        if self.app_context:
            self.app_context.shutdown()
        return True


if __name__ == '__main__':
    app = WorkHoursApp()
    app.run()
