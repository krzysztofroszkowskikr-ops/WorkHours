"""
ThemeScreen - Wybór i kustomizacja motywów
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.popup import MDPopup
from kivymd.color_definitions import colors
import logging

logger = logging.getLogger(__name__)


class ThemeScreen(Screen):
    """
    Ekran wyboru i kustomizacji motywów
    
    Funkcje:
    - Wyświetlenie 10 wbudowanych motywów
    - Generator własnych motywów (HSV)
    - Podgląd motywu
    - Zapisanie wybranego motywu
    """
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        
        # Wbudowane motywy
        self.themes = {
            'Material Light': {'primary': '#2196F3', 'accent': '#FFC107'},
            'Material Dark': {'primary': '#1F1F1F', 'accent': '#FFC107'},
            'Ocean Blue': {'primary': '#006994', 'accent': '#00BCD4'},
            'Forest Green': {'primary': '#1B5E20', 'accent': '#4CAF50'},
            'Sunset Purple': {'primary': '#7B1FA2', 'accent': '#FF5722'},
            'Autumn Orange': {'primary': '#E65100', 'accent': '#FF9800'},
            'Slate Gray': {'primary': '#37474F', 'accent': '#78909C'},
            'Deep Red': {'primary': '#B71C1C', 'accent': '#F44336'},
            'Indigo Blue': {'primary': '#3F51B5', 'accent': '#2196F3'},
            'Teal Modern': {'primary': '#00695C', 'accent': '#009688'}
        }
        
        # Załaduj UI
        self.load_ui()
    
    def load_ui(self):
        """Załaduj UI ekranu"""
        logger.info("Ładowanie Theme Screen...")
        
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
            text="Motywy aplikacji",
            size_hint_y=None,
            height='40dp',
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)
        
        # WBUDOWANE MOTYWY
        builtin_label = MDLabel(
            text="Wbudowane motywy",
            size_hint_y=None,
            height='24dp',
            font_size='16sp',
            bold=True
        )
        layout.add_widget(builtin_label)
        
        # Grid motywów (2 kolumny)
        theme_grid = MDGridLayout(
            cols=2,
            spacing='8dp',
            size_hint_y=None,
            padding='8dp'
        )
        theme_grid.bind(minimum_height=theme_grid.setter('height'))
        
        for theme_name, colors_dict in self.themes.items():
            theme_card = MDCard(
                padding='8dp',
                spacing='8dp',
                orientation='vertical',
                size_hint_y=None,
                height='120dp'
            )
            
            # Nazwa
            theme_card.add_widget(MDLabel(
                text=theme_name,
                size_hint_y=0.3,
                bold=True
            ))
            
            # Kolory
            color_layout = MDBoxLayout(
                spacing='4dp',
                size_hint_y=0.4
            )
            
            primary_color_box = MDCard(
                size_hint_x=0.5,
                canvas_color=self._hex_to_rgb(colors_dict['primary'])
            )
            color_layout.add_widget(primary_color_box)
            
            accent_color_box = MDCard(
                size_hint_x=0.5,
                canvas_color=self._hex_to_rgb(colors_dict['accent'])
            )
            color_layout.add_widget(accent_color_box)
            
            theme_card.add_widget(color_layout)
            
            # Przycisk
            select_btn = MDRaisedButton(
                text="Wybierz",
                size_hint_y=0.3
            )
            select_btn.bind(on_release=lambda x, tn=theme_name, cd=colors_dict: 
                self.select_theme(tn, cd))
            theme_card.add_widget(select_btn)
            
            theme_grid.add_widget(theme_card)
        
        layout.add_widget(theme_grid)
        
        # GENERATOR WŁASNYCH MOTYWÓW
        custom_label = MDLabel(
            text="Vlastní motyw (HSV generátor)",
            size_hint_y=None,
            height='24dp',
            font_size='16sp',
            bold=True
        )
        layout.add_widget(custom_label)
        
        custom_card = MDCard(
            padding='12dp',
            spacing='8dp',
            orientation='vertical',
            size_hint_y=None,
            height='100dp'
        )
        
        custom_layout = MDBoxLayout(orientation='vertical', spacing='8dp')
        custom_layout.add_widget(MDLabel(
            text="Generuj własny motyw z wybranym kolorem",
            size_hint_y=0.5
        ))
        
        generator_btn = MDRaisedButton(
            text="🎨 Generator motywu",
            size_hint_y=0.5
        )
        generator_btn.bind(on_release=self.show_generator)
        custom_layout.add_widget(generator_btn)
        
        custom_card.add_widget(custom_layout)
        layout.add_widget(custom_card)
        
        # INFORMACJE
        info_card = MDCard(
            padding='12dp',
            spacing='8dp',
            orientation='vertical',
            size_hint_y=None,
            height='100dp'
        )
        
        info_layout = MDBoxLayout(orientation='vertical', spacing='4dp')
        info_layout.add_widget(MDLabel(
            text="ℹ️ Informacje",
            bold=True,
            size_hint_y=None,
            height='24dp'
        ))
        info_layout.add_widget(MDLabel(
            text="Kolory Primary i Accent",
            size_hint_y=None,
            height='24dp',
            font_size='12sp'
        ))
        info_layout.add_widget(MDLabel(
            text="Zmiany zostaną zastosowane natychmiast",
            size_hint_y=None,
            height='24dp',
            font_size='12sp'
        ))
        
        info_card.add_widget(info_layout)
        layout.add_widget(info_card)
        
        # POWRÓT
        back_btn = MDRaisedButton(text="◀️ Wróć", size_hint_y=None, height='56dp')
        back_btn.bind(on_release=lambda x: self.app.switch_screen('settings'))
        layout.add_widget(back_btn)
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
        
        logger.info("Theme Screen załadowany")
    
    def select_theme(self, theme_name, colors_dict):
        """Wybierz motyw"""
        try:
            logger.info(f"Motyw wybrany: {theme_name}")
            # TODO: Integracja z ThemeService
            logger.info(f"Primary: {colors_dict['primary']}, Accent: {colors_dict['accent']}")
        except Exception as e:
            logger.error(f"Błąd wyboru motywu: {e}")
    
    def show_generator(self, instance):
        """Pokaż generator motywów"""
        try:
            content = MDBoxLayout(orientation='vertical', padding='16dp', spacing='12dp')
            
            content.add_widget(MDLabel(text="Generator motywu (HSV)", bold=True))
            content.add_widget(MDLabel(
                text="Funkcja: Generuj motyw z wybranym kolorem bazowym"
            ))
            
            generator_btn = MDRaisedButton(text="Generuj motyw HSV")
            content.add_widget(generator_btn)
            
            close_btn = MDRaisedButton(text="Zamknij")
            content.add_widget(close_btn)
            
            popup = MDPopup(
                title="Generator motywu",
                content=content,
                size_hint=(0.9, 0.6)
            )
            
            close_btn.bind(on_release=popup.dismiss)
            popup.open()
            
        except Exception as e:
            logger.error(f"Błąd generatora motywu: {e}")
    
    @staticmethod
    def _hex_to_rgb(hex_color):
        """Konwertuj hex na RGB (0-1)"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4)) + (1,)


__all__ = ['ThemeScreen']
