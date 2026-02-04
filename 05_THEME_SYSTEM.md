# THEME SYSTEM - COMPLETE IMPLEMENTATION
## WorkHours Purple v1.0 (Opcja A + Opcja B + Kivy Animations)

---

## 1. THEME SYSTEM OVERVIEW

```
Theme Selection Flow:

User opens Settings
    ↓
Selects Theme (Hardcoded 1-10 OR Custom 100+)
    ↓
ThemeService.apply_theme_with_animation()
    ├─ Fade Out (0.25s)
    ├─ Swap theme colors
    ├─ Fade In (0.25s)
    └─ Save to DB
    
Result: Smooth transition with no visual jarring
```

---

## 2. OPCJA A - HARDCODED THEMES (1-10)

### 2.1 Theme Definitions File

```python
# src/ui/themes/theme_definitions.py
"""
10 pre-designed color themes for WorkHours Purple
Each theme is carefully tuned for dark mode readability
"""

HARDCODED_THEMES = {
    1: {
        'id': 1,
        'name': 'Dark Purple Neon',
        'category': 'dark',
        'colors': {
            'background': '#1A1428',      # Deep purple-black
            'surface': '#2D1B69',         # Dark purple
            'surface2': '#3E2D7D',        # Medium purple
            'text': '#FFFFFF',            # White text
            'text_secondary': '#B0B0B0',  # Muted gray
            'primary': '#9C27B0',         # Vibrant purple
            'accent': '#FF00FF',          # Neon magenta
            'success': '#4CAF50',         # Green
            'warning': '#FF9800',         # Orange
            'error': '#F44336',           # Red
        },
        'shapes': {
            'radius_card': '22dp',
            'radius_button': '18dp',
            'radius_chip': '999dp',
        },
        'typography': {
            'font_size_title': '24sp',
            'font_size_heading': '18sp',
            'font_size_body': '14sp',
            'font_size_caption': '12sp',
        }
    },
    
    2: {
        'id': 2,
        'name': 'Dark Grape Premium',
        'category': 'dark',
        'colors': {
            'background': '#1F0A3D',
            'surface': '#3D1A5C',
            'surface2': '#4D2A7C',
            'text': '#FFFFFF',
            'text_secondary': '#C0C0C0',
            'primary': '#7B1FA2',
            'accent': '#FFD700',          # Gold accent
            'success': '#81C784',
            'warning': '#FFB74D',
            'error': '#EF5350',
        },
        'shapes': {
            'radius_card': '22dp',
            'radius_button': '18dp',
            'radius_chip': '999dp',
        },
        'typography': {
            'font_size_title': '24sp',
            'font_size_heading': '18sp',
            'font_size_body': '14sp',
            'font_size_caption': '12sp',
        }
    },
    
    3: {
        'id': 3,
        'name': 'Dark Electric Violet',
        'category': 'dark',
        'colors': {
            'background': '#0A0E27',
            'surface': '#1A1A4D',
            'surface2': '#2A2A6D',
            'text': '#FFFFFF',
            'text_secondary': '#A0A0C0',
            'primary': '#6200EE',         # Electric violet
            'accent': '#03DAC6',          # Cyan accent
            'success': '#03DAC6',
            'warning': '#CF6679',
            'error': '#CF6679',
        },
        'shapes': {
            'radius_card': '22dp',
            'radius_button': '18dp',
            'radius_chip': '999dp',
        },
        'typography': {
            'font_size_title': '24sp',
            'font_size_heading': '18sp',
            'font_size_body': '14sp',
            'font_size_caption': '12sp',
        }
    },
    
    4: {
        'id': 4,
        'name': 'Dark Plum + Gold',
        'category': 'dark',
        'colors': {
            'background': '#2D1B3D',
            'surface': '#3D2B4D',
            'surface2': '#4D3B5D',
            'text': '#FFFFFF',
            'text_secondary': '#D0C0D0',
            'primary': '#9C1D5C',         # Plum
            'accent': '#FFD54F',          # Gold
            'success': '#66BB6A',
            'warning': '#FFA726',
            'error': '#EF5350',
        },
        'shapes': {
            'radius_card': '22dp',
            'radius_button': '18dp',
            'radius_chip': '999dp',
        },
        'typography': {
            'font_size_title': '24sp',
            'font_size_heading': '18sp',
            'font_size_body': '14sp',
            'font_size_caption': '12sp',
        }
    },
    
    5: {
        'id': 5,
        'name': 'Light Clean Purple',
        'category': 'light',
        'colors': {
            'background': '#F5F5F5',      # Light gray
            'surface': '#FFFFFF',         # White
            'surface2': '#F0F0F0',        # Off-white
            'text': '#212121',            # Dark gray/black
            'text_secondary': '#757575',  # Medium gray
            'primary': '#9C27B0',
            'accent': '#E91E63',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'error': '#F44336',
        },
        'shapes': {
            'radius_card': '22dp',
            'radius_button': '18dp',
            'radius_chip': '999dp',
        },
        'typography': {
            'font_size_title': '24sp',
            'font_size_heading': '18sp',
            'font_size_body': '14sp',
            'font_size_caption': '12sp',
        }
    },
    
    6: {
        'id': 6,
        'name': 'Light Lavender Candy',
        'category': 'light',
        'colors': {
            'background': '#F3E5F5',      # Lavender
            'surface': '#FFFFFF',
            'surface2': '#F1E5F7',
            'text': '#2D1B4E',
            'text_secondary': '#6A4C8F',
            'primary': '#AB47BC',         # Medium purple
            'accent': '#FF1493',          # Deep pink
            'success': '#66BB6A',
            'warning': '#FFA726',
            'error': '#EF5350',
        },
        'shapes': {
            'radius_card': '22dp',
            'radius_button': '18dp',
            'radius_chip': '999dp',
        },
        'typography': {
            'font_size_title': '24sp',
            'font_size_heading': '18sp',
            'font_size_body': '14sp',
            'font_size_caption': '12sp',
        }
    },
    
    7: {
        'id': 7,
        'name': 'Midnight Indigo',
        'category': 'dark',
        'colors': {
            'background': '#0D0221',      # Almost black
            'surface': '#1A0033',
            'surface2': '#2D0052',
            'text': '#FFFFFF',
            'text_secondary': '#9090B0',
            'primary': '#5500BB',         # Indigo
            'accent': '#00FF88',          # Neon green
            'success': '#00FF88',
            'warning': '#FFBB00',
            'error': '#FF3333',
        },
        'shapes': {
            'radius_card': '22dp',
            'radius_button': '18dp',
            'radius_chip': '999dp',
        },
        'typography': {
            'font_size_title': '24sp',
            'font_size_heading': '18sp',
            'font_size_body': '14sp',
            'font_size_caption': '12sp',
        }
    },
    
    8: {
        'id': 8,
        'name': 'Graphite Purple',
        'category': 'dark',
        'colors': {
            'background': '#1E1E2E',      # Dark gray-blue
            'surface': '#2D2D44',
            'surface2': '#3C3C54',
            'text': '#FFFFFF',
            'text_secondary': '#A0A0B0',
            'primary': '#8040A8',
            'accent': '#B04080',          # Mauve
            'success': '#48A868',
            'warning': '#E0A040',
            'error': '#E04848',
        },
        'shapes': {
            'radius_card': '22dp',
            'radius_button': '18dp',
            'radius_chip': '999dp',
        },
        'typography': {
            'font_size_title': '24sp',
            'font_size_heading': '18sp',
            'font_size_body': '14sp',
            'font_size_caption': '12sp',
        }
    },
    
    9: {
        'id': 9,
        'name': 'Purple + Lime Pop',
        'category': 'dark',
        'colors': {
            'background': '#1A0A33',
            'surface': '#2D1A4D',
            'surface2': '#3D2A5D',
            'text': '#FFFFFF',
            'text_secondary': '#B0D090',
            'primary': '#9C27B0',
            'accent': '#CCFF00',          # Lime green
            'success': '#CCFF00',
            'warning': '#FF6B00',
            'error': '#FF2E2E',
        },
        'shapes': {
            'radius_card': '22dp',
            'radius_button': '18dp',
            'radius_chip': '999dp',
        },
        'typography': {
            'font_size_title': '24sp',
            'font_size_heading': '18sp',
            'font_size_body': '14sp',
            'font_size_caption': '12sp',
        }
    },
    
    10: {
        'id': 10,
        'name': 'Purple Sunset',
        'category': 'dark',
        'colors': {
            'background': '#2D1033',      # Deep purple
            'surface': '#4D1A4D',         # Darker purple
            'surface2': '#6D2A5D',        # Plum
            'text': '#FFFFFF',
            'text_secondary': '#F0C0E0',  # Light mauve
            'primary': '#D946E8',         # Hot pink-purple
            'accent': '#FF6B35',          # Orange
            'success': '#6BCB77',
            'warning': '#FFD93D',
            'error': '#FF6B6B',
        },
        'shapes': {
            'radius_card': '22dp',
            'radius_button': '18dp',
            'radius_chip': '999dp',
        },
        'typography': {
            'font_size_title': '24sp',
            'font_size_heading': '18sp',
            'font_size_body': '14sp',
            'font_size_caption': '12sp',
        }
    },
}

# Theme kategorii (for sorting in UI)
THEME_CATEGORIES = {
    'dark': 'Motywy ciemne',
    'light': 'Motywy jasne',
}

# Quick reference
THEME_NAMES = {theme['id']: theme['name'] for theme in HARDCODED_THEMES.values()}
```

---

## 3. OPCJA B - DYNAMIC THEME GENERATOR

### 3.1 Color Generation Algorithm

```python
# src/ui/themes/theme_generator.py
"""
Dynamic theme generation using HSV color model
Generates harmonious color palettes from a single hue value
"""

from colorsys import hsv_to_rgb, rgb_to_hsv

class ThemeGenerator:
    """Generate themes dynamically (Opcja B)"""
    
    @staticmethod
    def hsv_to_hex(h: float, s: float, v: float) -> str:
        """
        Convert HSV to hex color code
        h: 0-360 (hue)
        s: 0-100 (saturation)
        v: 0-100 (value/brightness)
        """
        r, g, b = hsv_to_rgb(h / 360, s / 100, v / 100)
        return '#{:02x}{:02x}{:02x}'.format(
            int(r * 255),
            int(g * 255),
            int(b * 255)
        )
    
    @staticmethod
    def generate_dark_theme(base_hue: float, name: str = "Custom") -> dict:
        """
        Generate complete dark theme from single hue
        
        Args:
            base_hue: 0-360 (HSV hue value)
            name: theme display name
        
        Returns:
            Theme dictionary (compatible with Opcja A format)
        """
        # HSV adjustments for dark theme harmony
        theme = {
            'id': None,  # Generated themes: 100+
            'name': name,
            'category': 'dark',
            'colors': {
                # Background: very low brightness, high saturation
                'background': ThemeGenerator.hsv_to_hex(base_hue, 40, 10),
                
                # Surface tiers: gradually lighter
                'surface': ThemeGenerator.hsv_to_hex(base_hue, 45, 20),
                'surface2': ThemeGenerator.hsv_to_hex(base_hue, 40, 30),
                
                # Text
                'text': '#FFFFFF',
                'text_secondary': '#B0B0B0',
                
                # Primary: full saturation, medium-high brightness
                'primary': ThemeGenerator.hsv_to_hex(base_hue, 100, 70),
                
                # Accent: complementary color (opposite hue)
                'accent': ThemeGenerator.hsv_to_hex((base_hue + 180) % 360, 100, 100),
                
                # Status colors (fixed, not hue-dependent)
                'success': ThemeGenerator.hsv_to_hex(120, 70, 60),
                'warning': ThemeGenerator.hsv_to_hex(40, 100, 100),
                'error': ThemeGenerator.hsv_to_hex(0, 80, 90),
            },
            'shapes': {
                'radius_card': '22dp',
                'radius_button': '18dp',
                'radius_chip': '999dp',
            },
            'typography': {
                'font_size_title': '24sp',
                'font_size_heading': '18sp',
                'font_size_body': '14sp',
                'font_size_caption': '12sp',
            }
        }
        return theme
    
    @staticmethod
    def generate_light_theme(base_hue: float, name: str = "Custom Light") -> dict:
        """Generate light theme with high brightness"""
        theme = {
            'id': None,
            'name': name,
            'category': 'light',
            'colors': {
                # Background & surfaces: very light
                'background': ThemeGenerator.hsv_to_hex(base_hue, 10, 95),
                'surface': '#FFFFFF',
                'surface2': ThemeGenerator.hsv_to_hex(base_hue, 10, 90),
                
                # Text: dark
                'text': '#212121',
                'text_secondary': '#757575',
                
                # Primary: vibrant
                'primary': ThemeGenerator.hsv_to_hex(base_hue, 100, 60),
                
                # Accent: complementary
                'accent': ThemeGenerator.hsv_to_hex((base_hue + 180) % 360, 100, 70),
                
                # Status colors
                'success': ThemeGenerator.hsv_to_hex(120, 70, 50),
                'warning': ThemeGenerator.hsv_to_hex(40, 90, 80),
                'error': ThemeGenerator.hsv_to_hex(0, 80, 70),
            },
            'shapes': {
                'radius_card': '22dp',
                'radius_button': '18dp',
                'radius_chip': '999dp',
            },
            'typography': {
                'font_size_title': '24sp',
                'font_size_heading': '18sp',
                'font_size_body': '14sp',
                'font_size_caption': '12sp',
            }
        }
        return theme

# Example usage:
# theme = ThemeGenerator.generate_dark_theme(base_hue=270, name="My Custom Purple")
# # Returns complete theme ready to apply
```

---

## 4. KIVY ANIMATIONS - THEME TRANSITIONS

### 4.1 Animation Service

```python
# src/ui/themes/animations.py
"""
Kivy animations for smooth theme transitions
"""

from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Canvas, Color, Rectangle

class ThemeTransitionAnimator:
    """Manages smooth theme transitions with animations"""
    
    @staticmethod
    def animate_theme_change(
        app_root_widget,
        old_theme: dict,
        new_theme: dict,
        duration: float = 0.5
    ):
        """
        Animate theme transition: fade out → change → fade in
        
        Args:
            app_root_widget: root widget of app
            old_theme: current theme dict
            new_theme: new theme dict
            duration: total animation time in seconds
        """
        
        # Phase 1: Fade OUT (50% of duration)
        fade_out_duration = duration * 0.5
        anim_out = Animation(opacity=0, duration=fade_out_duration)
        
        def on_fade_out_complete(*args):
            """Apply new theme during fade out"""
            ThemeTransitionAnimator._apply_theme_to_widget(
                app_root_widget,
                new_theme
            )
            # Phase 2: Fade IN
            fade_in_duration = duration * 0.5
            anim_in = Animation(opacity=1, duration=fade_in_duration)
            anim_in.start(app_root_widget)
        
        anim_out.bind(on_complete=on_fade_out_complete)
        anim_out.start(app_root_widget)
    
    @staticmethod
    def _apply_theme_to_widget(widget, theme: dict):
        """
        Recursively apply theme colors to widget and its children
        """
        # Update widget's canvas background
        widget.canvas.before.clear()
        with widget.canvas.before:
            # Draw background
            color_hex = theme['colors']['background']
            rgba = ThemeTransitionAnimator._hex_to_rgba(color_hex)
            Color(*rgba)
            Rectangle(size=widget.size, pos=widget.pos)
        
        # Store theme reference in widget for children
        widget.current_theme = theme
        
        # Recursively update children
        if hasattr(widget, 'children'):
            for child in widget.children:
                ThemeTransitionAnimator._apply_theme_to_widget(child, theme)
    
    @staticmethod
    def _hex_to_rgba(hex_color: str) -> tuple:
        """
        Convert hex color to RGBA tuple (0-1 range for Kivy)
        "#FF00FF" -> (1.0, 0.0, 1.0, 1.0)
        """
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b, 1.0)
    
    @staticmethod
    def animate_color_change(
        widget,
        color_hex_old: str,
        color_hex_new: str,
        duration: float = 0.3,
        on_complete=None
    ):
        """
        Animate single widget color change (e.g., button background)
        Uses opacity animation as proxy for color transition
        """
        anim = Animation(opacity=0.7, duration=duration*0.5)
        anim.bind(on_complete=lambda *args: (
            Animation(opacity=1, duration=duration*0.5).start(widget),
            on_complete() if on_complete else None
        ))
        anim.start(widget)
```

---

## 5. THEME SERVICE - INTEGRATION

### 5.1 ThemeService Main Class

```python
# src/services/theme_service.py
"""
Theme management service combining:
- Opcja A: Hardcoded themes
- Opcja B: Dynamic generation
- Animations: Kivy transitions
"""

import json
from src.ui.themes.theme_definitions import HARDCODED_THEMES
from src.ui.themes.theme_generator import ThemeGenerator
from src.ui.themes.animations import ThemeTransitionAnimator
from src.app_context import app_context

class ThemeService:
    """Central theme management"""
    
    def __init__(self, db_connection=None):
        self.db = db_connection
        self.hardcoded_themes = HARDCODED_THEMES
        self.custom_themes = {}  # theme_id -> theme dict
        self._load_custom_themes()
    
    def _load_custom_themes(self):
        """Load dynamically generated themes from DB"""
        if not self.db:
            return
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT theme_id, config_json FROM custom_themes")
        
        for row in cursor.fetchall():
            theme_id = row[0]
            config_json = row[1]
            try:
                theme_data = json.loads(config_json)
                theme_data['id'] = theme_id
                self.custom_themes[theme_id] = theme_data
            except json.JSONDecodeError:
                print(f"Failed to parse theme {theme_id}")
    
    def get_theme(self, theme_id: int) -> dict:
        """
        Get theme by ID
        1-10: Hardcoded
        100+: Custom generated
        """
        if theme_id in self.hardcoded_themes:
            return self.hardcoded_themes[theme_id]
        elif theme_id in self.custom_themes:
            return self.custom_themes[theme_id]
        else:
            # Fallback to default
            return self.hardcoded_themes[1]
    
    def get_all_available_themes(self) -> list:
        """Get list of all available themes"""
        themes = []
        
        # Add hardcoded
        for theme_id in sorted(self.hardcoded_themes.keys()):
            theme = self.hardcoded_themes[theme_id]
            themes.append({
                'id': theme_id,
                'name': theme['name'],
                'category': theme['category'],
                'type': 'hardcoded'
            })
        
        # Add custom
        for theme_id in sorted(self.custom_themes.keys()):
            theme = self.custom_themes[theme_id]
            themes.append({
                'id': theme_id,
                'name': theme['name'],
                'category': theme['category'],
                'type': 'custom'
            })
        
        return themes
    
    def apply_theme_with_animation(
        self,
        app_instance,
        theme_id: int,
        duration: float = 0.5
    ) -> bool:
        """
        Apply theme with Kivy animation
        
        Returns: True if successful
        """
        try:
            new_theme = self.get_theme(theme_id)
            old_theme = getattr(app_instance, 'current_theme', self.hardcoded_themes[1])
            
            # Trigger animation
            ThemeTransitionAnimator.animate_theme_change(
                app_instance.root,
                old_theme,
                new_theme,
                duration=duration
            )
            
            # Update app state
            app_instance.current_theme = new_theme
            
            # Save to DB
            if self.db:
                self.db.set_setting(
                    'theme_id',
                    theme_id,
                    'integer',
                    app_context.active_profile_id
                )
            
            return True
        
        except Exception as e:
            print(f"Theme application failed: {e}")
            return False
    
    def create_custom_theme(
        self,
        base_hue: float,
        is_dark: bool = True,
        name: str = None,
        profile_id: int = None
    ) -> dict:
        """
        Create new custom theme (Opcja B)
        
        Args:
            base_hue: 0-360 (HSV hue)
            is_dark: True for dark, False for light
            name: display name
            profile_id: which profile owns this theme
        
        Returns: theme dict
        """
        if name is None:
            name = f"Custom {'Dark' if is_dark else 'Light'} {int(base_hue)}°"
        
        # Generate theme
        if is_dark:
            theme = ThemeGenerator.generate_dark_theme(base_hue, name)
        else:
            theme = ThemeGenerator.generate_light_theme(base_hue, name)
        
        # Assign ID (100+)
        next_id = max([t['id'] for t in self.custom_themes.values()] + [99]) + 1
        theme['id'] = next_id
        
        # Store in memory
        self.custom_themes[next_id] = theme
        
        # Persist to DB
        if self.db and profile_id:
            self.db.conn.execute("""
                INSERT INTO custom_themes (profile_id, theme_id, name, config_json)
                VALUES (?, ?, ?, ?)
            """, (
                profile_id,
                next_id,
                name,
                json.dumps(theme)
            ))
            self.db.conn.commit()
        
        return theme
    
    def delete_custom_theme(self, theme_id: int) -> bool:
        """Delete custom theme"""
        if theme_id < 100:  # Can't delete hardcoded
            return False
        
        if theme_id in self.custom_themes:
            del self.custom_themes[theme_id]
        
        if self.db:
            self.db.conn.execute(
                "DELETE FROM custom_themes WHERE theme_id = ?",
                (theme_id,)
            )
            self.db.conn.commit()
        
        return True
```

---

## 6. UI INTEGRATION - SETTINGS SCREEN

### 6.1 Theme Selector Component

```python
# src/ui/components/theme_selector.py
"""
Theme selection UI component
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from src.services import ServiceLocator

class ThemeSelectorCard(MDCard):
    """Individual theme preview card"""
    
    def __init__(self, theme: dict, on_select_callback, **kwargs):
        super().__init__(**kwargs)
        self.theme = theme
        self.on_select = on_select_callback
        self.size_hint = (1, None)
        self.height = '80dp'
        
        # Build card with theme preview
        layout = BoxLayout(orientation='horizontal', padding='10dp', spacing='10dp')
        
        # Color preview circles
        color_preview = BoxLayout(size_hint_x=0.3)
        colors_to_show = [
            theme['colors']['primary'],
            theme['colors']['accent'],
            theme['colors']['background'],
        ]
        
        for color_hex in colors_to_show:
            preview_widget = MDCard(
                md_bg_color=self._hex_to_rgba(color_hex),
                size_hint=(1, 1),
                radius=[theme['shapes']['radius_card']],
            )
            color_preview.add_widget(preview_widget)
        
        layout.add_widget(color_preview)
        
        # Theme info
        info = BoxLayout(orientation='vertical', size_hint_x=0.5)
        info.add_widget(MDLabel(text=theme['name'], bold=True))
        info.add_widget(MDLabel(text=f"ID: {theme['id']}", size_hint_y=0.5))
        layout.add_widget(info)
        
        # Select button
        select_btn = MDRaisedButton(
            text='Wybierz',
            size_hint_x=0.2,
            on_press=self._on_press
        )
        layout.add_widget(select_btn)
        
        self.add_widget(layout)
    
    def _on_press(self, instance):
        self.on_select(self.theme['id'])
    
    @staticmethod
    def _hex_to_rgba(hex_color: str) -> tuple:
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b, 1.0)

class ThemeSelector(BoxLayout):
    """Theme selection view with grid of themes"""
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        self.theme_service = ServiceLocator.get('theme')
        
        # Scrollable theme grid
        scroll = ScrollView()
        theme_grid = GridLayout(cols=1, spacing='10dp', size_hint_y=None)
        theme_grid.bind(minimum_height=theme_grid.setter('height'))
        
        # Load all themes
        available_themes = self.theme_service.get_all_available_themes()
        
        for theme_info in available_themes:
            theme = self.theme_service.get_theme(theme_info['id'])
            card = ThemeSelectorCard(
                theme=theme,
                on_select_callback=self._on_theme_select
            )
            theme_grid.add_widget(card)
        
        scroll.add_widget(theme_grid)
        self.add_widget(scroll)
    
    def _on_theme_select(self, theme_id: int):
        """When user selects a theme"""
        # Get app instance
        from src.app_context import app_context
        
        # Apply with animation
        self.theme_service.apply_theme_with_animation(
            app_context.app_instance,
            theme_id,
            duration=0.5
        )
```

---

## 7. USAGE EXAMPLES

### 7.1 Basic Theme Application

```python
from src.services import ServiceLocator
from src.app_context import app_context

# Get theme service
theme_service = ServiceLocator.get('theme')

# Apply theme (Opcja A - hardcoded)
theme_service.apply_theme_with_animation(
    app_context.app_instance,
    theme_id=5,  # Light Clean Purple
    duration=0.5
)

# Create custom theme (Opcja B - generated)
custom_theme = theme_service.create_custom_theme(
    base_hue=270,  # Purple hue
    is_dark=True,
    name="My Purple",
    profile_id=app_context.active_profile_id
)

# Apply custom theme
theme_service.apply_theme_with_animation(
    app_context.app_instance,
    theme_id=custom_theme['id'],
    duration=0.5
)
```

### 7.2 Theme Persistence

```python
# Automatically saved when applied:
# - Settings DB stores 'theme_id' for active profile
# - Custom theme configs stored in custom_themes table
# - On app startup, last theme is restored
```

---

## 8. PODSUMOWANIE SYSTEMU MOTYWÓW

| Aspekt | Opcja A | Opcja B | Animacje |
|--------|---------|---------|----------|
| **Approach** | Hardcoded 10 themes | Dynamic generation | Kivy transitions |
| **Flexibility** | Fixed choices | Unlimited combinations | Smooth UX |
| **Dev Time** | Minimal (~2h) | Moderate (~4h) | Fast (~1h) |
| **Performance** | Excellent | Good | Excellent |
| **Maintenance** | Simple | Moderate | Simple |
| **User Control** | Limited | High | N/A |

**Rekomendacja:** Łączyć Opcję A + B dla balansu!
- Start z 10 hardcoded dla MVP
- Add custom generation w v1.1
- Animations zawsze (cheap win)

---

**NEXT:** API Design & Calculations
