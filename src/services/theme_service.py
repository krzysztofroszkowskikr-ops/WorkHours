"""
ThemeService - Serwis zarządzania motywami
Obsługuje: Opcja A (10 wbudowanych), Opcja B (HSV generator), Opcja C (animacje)
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import colorsys
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class ThemeColors:
    """Struktura kolorów motywu"""
    primary: str           # Kolor główny
    primary_variant: str   # Wariant główny
    secondary: str         # Kolor drugorzędny
    secondary_variant: str # Wariant drugorzędny
    surface: str           # Tło
    background: str        # Tło ogólne
    error: str             # Błąd
    on_primary: str        # Tekst na głównym
    on_secondary: str      # Tekst na drugorzędnym
    on_surface: str        # Tekst na powierzchni


class ThemeService:
    """
    Serwis do zarządzania motywami
    
    Obsługuje 3 opcje:
    - Opcja A: 10 wbudowanych motywów
    - Opcja B: Generator HSV dla własnych motywów
    - Opcja C: Animacje fade (0.5s przejście)
    """
    
    # ═══════════════════════════════════════════════════════════════════════
    # OPCJA A - WBUDOWANE MOTYWY (10 sztuk)
    # ═══════════════════════════════════════════════════════════════════════
    
    BUILTIN_THEMES = {
        1: {
            'name': 'Material Light',
            'primary': '#6200EE',
            'primary_variant': '#3700B3',
            'secondary': '#03DAC6',
            'secondary_variant': '#018786',
            'surface': '#FFFFFF',
            'background': '#FFFFFF',
            'error': '#B00020',
            'on_primary': '#FFFFFF',
            'on_secondary': '#000000',
            'on_surface': '#000000'
        },
        2: {
            'name': 'Material Dark',
            'primary': '#BB86FC',
            'primary_variant': '#3700B3',
            'secondary': '#03DAC6',
            'secondary_variant': '#03DAC6',
            'surface': '#121212',
            'background': '#121212',
            'error': '#CF6679',
            'on_primary': '#000000',
            'on_secondary': '#000000',
            'on_surface': '#FFFFFF'
        },
        3: {
            'name': 'Ocean Blue',
            'primary': '#006994',
            'primary_variant': '#004B6C',
            'secondary': '#34B0BE',
            'secondary_variant': '#00838F',
            'surface': '#FFFFFF',
            'background': '#F5F5F5',
            'error': '#D32F2F',
            'on_primary': '#FFFFFF',
            'on_secondary': '#000000',
            'on_surface': '#000000'
        },
        4: {
            'name': 'Forest Green',
            'primary': '#1B5E20',
            'primary_variant': '#003300',
            'secondary': '#66BB6A',
            'secondary_variant': '#2E7D32',
            'surface': '#FFFFFF',
            'background': '#F1F8E9',
            'error': '#D32F2F',
            'on_primary': '#FFFFFF',
            'on_secondary': '#000000',
            'on_surface': '#1B5E20'
        },
        5: {
            'name': 'Sunset Purple',
            'primary': '#6A1B9A',
            'primary_variant': '#4A148C',
            'secondary': '#F06292',
            'secondary_variant': '#C2185B',
            'surface': '#FFFFFF',
            'background': '#F3E5F5',
            'error': '#D32F2F',
            'on_primary': '#FFFFFF',
            'on_secondary': '#FFFFFF',
            'on_surface': '#4A148C'
        },
        6: {
            'name': 'Autumn Orange',
            'primary': '#E65100',
            'primary_variant': '#BF360C',
            'secondary': '#FF6F00',
            'secondary_variant': '#E65100',
            'surface': '#FFFFFF',
            'background': '#FFF3E0',
            'error': '#D32F2F',
            'on_primary': '#FFFFFF',
            'on_secondary': '#FFFFFF',
            'on_surface': '#E65100'
        },
        7: {
            'name': 'Slate Gray',
            'primary': '#455A64',
            'primary_variant': '#37474F',
            'secondary': '#78909C',
            'secondary_variant': '#607D8B',
            'surface': '#FFFFFF',
            'background': '#ECEFF1',
            'error': '#D32F2F',
            'on_primary': '#FFFFFF',
            'on_secondary': '#FFFFFF',
            'on_surface': '#37474F'
        },
        8: {
            'name': 'Deep Red',
            'primary': '#B71C1C',
            'primary_variant': '#7F0000',
            'secondary': '#E53935',
            'secondary_variant': '#C62828',
            'surface': '#FFFFFF',
            'background': '#FFEBEE',
            'error': '#B71C1C',
            'on_primary': '#FFFFFF',
            'on_secondary': '#FFFFFF',
            'on_surface': '#B71C1C'
        },
        9: {
            'name': 'Indigo Blue',
            'primary': '#283593',
            'primary_variant': '#1A237E',
            'secondary': '#5E35B1',
            'secondary_variant': '#512DA8',
            'surface': '#FFFFFF',
            'background': '#F3E5F5',
            'error': '#D32F2F',
            'on_primary': '#FFFFFF',
            'on_secondary': '#FFFFFF',
            'on_surface': '#1A237E'
        },
        10: {
            'name': 'Teal Modern',
            'primary': '#00897B',
            'primary_variant': '#004D40',
            'secondary': '#26C6DA',
            'secondary_variant': '#00838F',
            'surface': '#FFFFFF',
            'background': '#E0F2F1',
            'error': '#D32F2F',
            'on_primary': '#FFFFFF',
            'on_secondary': '#000000',
            'on_surface': '#004D40'
        }
    }
    
    @staticmethod
    def get_builtin_theme(theme_id: int) -> Optional[Dict]:
        """
        Pobierz wbudowany motyw (Opcja A)
        
        Args:
            theme_id: ID motywu (1-10)
            
        Returns:
            Słownik z kolorami lub None
        """
        if theme_id not in ThemeService.BUILTIN_THEMES:
            logger.warning(f"Motyw ID {theme_id} nie istnieje")
            return None
        
        return ThemeService.BUILTIN_THEMES[theme_id]
    
    @staticmethod
    def get_all_builtin_themes() -> Dict[int, Dict]:
        """Pobierz wszystkie wbudowane motywy"""
        return ThemeService.BUILTIN_THEMES.copy()
    
    # ═══════════════════════════════════════════════════════════════════════
    # OPCJA B - HSV GENERATOR (Niestandardowe motywy)
    # ═══════════════════════════════════════════════════════════════════════
    
    @staticmethod
    def hex_to_hsv(hex_color: str) -> Tuple[float, float, float]:
        """
        Konwertuj HEX na HSV
        
        Args:
            hex_color: Kolor w formacie #RRGGBB
            
        Returns:
            Tuple (H: 0-360, S: 0-100, V: 0-100)
        """
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return h * 360, s * 100, v * 100
    
    @staticmethod
    def hsv_to_hex(h: float, s: float, v: float) -> str:
        """
        Konwertuj HSV na HEX
        
        Args:
            h: Hue 0-360
            s: Saturation 0-100
            v: Value 0-100
            
        Returns:
            Kolor w formacie #RRGGBB
        """
        h = h / 360.0
        s = s / 100.0
        v = v / 100.0
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        
        return f"#{r:02X}{g:02X}{b:02X}"
    
    @staticmethod
    def generate_theme_from_primary(
        primary_hex: str,
        name: str = "Custom Theme"
    ) -> ThemeColors:
        """
        Wygeneruj kompletny motyw z pojedynczego koloru (Opcja B)
        
        Args:
            primary_hex: Kolor główny #RRGGBB
            name: Nazwa motywu
            
        Returns:
            ThemeColors z wygenerowanymi kolorami
        """
        # Konwertuj na HSV
        h, s, v = ThemeService.hex_to_hsv(primary_hex)
        
        # Wygeneruj warianty
        primary = primary_hex
        primary_variant = ThemeService.hsv_to_hex(h, s, v - 20)  # Ciemniej
        
        # Kolor drugorzędny (obok na kole)
        secondary_h = (h + 180) % 360  # Kolor komplementarny
        secondary = ThemeService.hsv_to_hex(secondary_h, s - 20, v)
        secondary_variant = ThemeService.hsv_to_hex(secondary_h, s, v - 15)
        
        # Kolory tła
        surface = "#FFFFFF"
        background = "#F5F5F5"
        error = "#D32F2F"
        
        # Kolory tekstowe
        on_primary = "#FFFFFF" if v > 50 else "#000000"
        on_secondary = "#FFFFFF" if v > 50 else "#000000"
        on_surface = "#000000"
        
        logger.info(f"Motyw '{name}' wygenerowany z koloru {primary}")
        
        return ThemeColors(
            primary=primary,
            primary_variant=primary_variant,
            secondary=secondary,
            secondary_variant=secondary_variant,
            surface=surface,
            background=background,
            error=error,
            on_primary=on_primary,
            on_secondary=on_secondary,
            on_surface=on_surface
        )
    
    @staticmethod
    def create_custom_theme_config(
        name: str,
        colors: ThemeColors
    ) -> Dict:
        """
        Utwórz konfigurację niestandardowego motywu
        
        Args:
            name: Nazwa motywu
            colors: Obiekt ThemeColors
            
        Returns:
            Słownik konfiguracji
        """
        return {
            'name': name,
            'primary': colors.primary,
            'primary_variant': colors.primary_variant,
            'secondary': colors.secondary,
            'secondary_variant': colors.secondary_variant,
            'surface': colors.surface,
            'background': colors.background,
            'error': colors.error,
            'on_primary': colors.on_primary,
            'on_secondary': colors.on_secondary,
            'on_surface': colors.on_surface
        }
    
    # ═══════════════════════════════════════════════════════════════════════
    # OPCJA C - ANIMACJE
    # ═══════════════════════════════════════════════════════════════════════
    
    @staticmethod
    def get_fade_animation_config() -> Dict:
        """
        Pobierz konfigurację animacji fade (Opcja C)
        
        Animacja: 0.25s fade out + 0.25s fade in = 0.5s total
        
        Returns:
            Słownik z konfiguracją
        """
        return {
            'name': 'Fade Transition',
            'type': 'fade',
            'fade_out_duration': 0.25,      # sekundy
            'fade_in_duration': 0.25,       # sekundy
            'total_duration': 0.5,          # sekundy
            'easing': 'out_quad'            # Kivy easing
        }
    
    @staticmethod
    def animate_theme_change(
        from_theme: Dict,
        to_theme: Dict,
        duration: float = 0.5
    ) -> Dict:
        """
        Przygotuj animację zmiany motywu
        
        Args:
            from_theme: Motyw początkowy
            to_theme: Motyw docelowy
            duration: Czas animacji (sekundy)
            
        Returns:
            Konfiguracja animacji
        """
        return {
            'animation_type': 'fade',
            'from_theme': from_theme,
            'to_theme': to_theme,
            'duration': duration,
            'steps': 10  # Liczba kroków animacji
        }


__all__ = ['ThemeService', 'ThemeColors']
