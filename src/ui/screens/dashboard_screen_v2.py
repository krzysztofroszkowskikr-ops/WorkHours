"""
DashboardScreen - Panel główny
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DashboardScreen(Screen):
    """Dashboard ekran z przeglądem miesiąca"""
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
    
    def on_enter(self):
        """Załaduj zawartość przy wejściu"""
        self.clear_widgets()
        self.load_ui()
    
    def load_ui(self):
        """Załaduj dashboard"""
        logger.info("Dashboard: loading UI")
        
        # Główny layout
        main = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Tytuł
        now = datetime.now()
        title = Label(
            text=f"🏢 WorkHours - {now.strftime('%B %Y')}",
            size_hint_y=0.1,
            font_size='18sp',
            bold=True
        )
        main.add_widget(title)
        
        # Statystyki
        stats = GridLayout(cols=3, spacing=10, size_hint_y=0.2)
        stats.add_widget(Label(text="⏱️\nGodziny\n-", font_size='12sp'))
        stats.add_widget(Label(text="📅\nDni\n-", font_size='12sp'))
        stats.add_widget(Label(text="📊\nŚrednia\n-", font_size='12sp'))
        main.add_widget(stats)
        
        # Szczegóły
        details = Label(
            text="Szczegóły miesiąca:\n"
                 "🤒 Choroby: -\n"
                 "🏖️ Urlopy: -\n"
                 "📆 Dni wolne: -\n"
                 "📝 Wpisów: -",
            size_hint_y=0.3,
            font_size='11sp'
        )
        main.add_widget(details)
        
        # Ostatnie wpisy
        recent = Label(
            text="Ostatnie wpisy:\n-",
            size_hint_y=0.2,
            font_size='11sp'
        )
        main.add_widget(recent)
        
        # Przyciski
        actions = BoxLayout(size_hint_y=0.2, spacing=5)
        add_btn = Button(text='➕ Dodaj')
        add_btn.bind(on_press=lambda x: self.app.switch_screen('entry'))
        actions.add_widget(add_btn)
        
        report_btn = Button(text='📄 Raport')
        report_btn.bind(on_press=lambda x: self.app.switch_screen('report'))
        actions.add_widget(report_btn)
        
        main.add_widget(actions)
        
        self.add_widget(main)


__all__ = ['DashboardScreen']
