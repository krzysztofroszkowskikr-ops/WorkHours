# TECHNICAL ARCHITECTURE DOCUMENT
## WorkHours Purple v1.0 - Complete Technical Specification

**Data**: 4 Luty 2026  
**Platform**: Android 16 (minSdkVersion: 26, targetSdkVersion: 35)  
**Developer**: 1 osoba (full-stack)  
**Timeline**: MVP → Full Feature Set

---

## 1. OVERVIEW ARCHITEKTURY

```
┌─────────────────────────────────────────────────────────────────┐
│                    LAYERS & ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  PRESENTATION LAYER (KivyMD)                             │   │
│  │  Screens, Widgets, Navigation, Animations               │   │
│  └────────────────┬─────────────────────────────────────────┘   │
│                   │ (ViewControllers/Presenters)                │
│  ┌────────────────▼─────────────────────────────────────────┐   │
│  │  BUSINESS LOGIC LAYER                                    │   │
│  │  - Services (Calc, PDF, Share, Reminders)               │   │
│  │  - Validators, Formatters                                │   │
│  │  - Theme Engine (A+B+Animations)                         │   │
│  └────────────────┬─────────────────────────────────────────┘   │
│                   │ (Repository Pattern)                        │
│  ┌────────────────▼─────────────────────────────────────────┐   │
│  │  DATA LAYER (SQLite + File System)                        │   │
│  │  - WorkEntry, Profile, Settings                          │   │
│  │  - Theme configs (JSON)                                  │   │
│  │  - Generated PDFs, Exports                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Design Pattern: **MVP + Repository + Service Locator**

```python
# Separation of concerns
main.py (AppEntry)
  ├── app.kv (layouts, basic bindings)
  ├── src/
  │   ├── models.py (data classes)
  │   ├── repository.py (data access abstraction)
  │   ├── services/ (business logic)
  │   │   ├── calc_service.py
  │   │   ├── pdf_service.py
  │   │   ├── reminder_service.py
  │   │   └── theme_service.py
  │   ├── ui/ (screens & widgets)
  │   │   ├── screens/
  │   │   ├── components/
  │   │   └── themes.py (theme definitions)
  │   └── utils/ (helpers)
  └── tests/
      ├── test_calc.py
      ├── test_validators.py
      └── test_pdf_generation.py
```

---

## 2. ARCHITEKTURA PROFILÓW UŻYTKOWNIKÓW

### Model wieloprofilowy (Isolated Data)

```
Database Structure:
┌─────────────────┐
│  profiles       │ (id, name, created_at)
├─────────────────┤
│  work_entries   │ ← profile_id (FK)
├─────────────────┤
│  settings       │ ← profile_id (FK)
└─────────────────┘
```

**Oznacza:**
- Każdy profil ma ODDZIELNE wpisy, ustawienia, motywy
- Przełączanie profilu = zmiana aktywnego kontekstu (session)
- Baza danych ONE dla wszystkich, ale isolated by profile_id

```python
# Pseudocode
class AppContext:
    active_profile_id: int
    active_profile: Profile
    
    def switch_profile(self, profile_id):
        self.active_profile_id = profile_id
        self.active_profile = repository.get_profile(profile_id)
        self.load_theme()  # Wczytaj motyw profilu
        self.refresh_ui()
        
    # Wszystkie operacje CRUD filtrują by active_profile_id
    def get_entries(self, month):
        return repository.get_entries(
            profile_id=self.active_profile_id,
            month=month
        )
```

---

## 3. SYSTEM MOTYWÓW (Kivy Animations + Opcja A + Opcja B)

### 3.1 Opcja A: Hardcoded Themes Dictionary

```python
# src/ui/themes.py
HARDCODED_THEMES = {
    1: {
        'name': 'Dark Purple Neon',
        'background': '#1A1428',
        'surface': '#2D1B69',
        'surface2': '#3E2D7D',
        'text': '#FFFFFF',
        'muted': '#B0B0B0',
        'primary': '#9C27B0',
        'accent': '#FF00FF',
        'success': '#4CAF50',
        'warning': '#FF9800',
        'error': '#F44336',
        'radius_card': '22dp',
        'radius_button': '18dp',
    },
    2: {
        'name': 'Dark Grape Premium',
        'background': '#1F0A3D',
        # ... pozostałe 9 wariantów
    },
    # ... id 3-10
}
```

### 3.2 Opcja B: Dynamic Color Generator

```python
# src/services/theme_service.py
from colorsys import hsv_to_rgb

def generate_theme_from_hue(base_hue, name="Custom"):
    """
    Generuje harmonijną paletę z jednego hue value.
    base_hue: 0-360 (HSV model)
    """
    def hsv_to_hex(h, s, v):
        r, g, b = hsv_to_rgb(h/360, s/100, v/100)
        return '#{:02x}{:02x}{:02x}'.format(
            int(r*255), int(g*255), int(b*255)
        )
    
    theme = {
        'name': name,
        'background': hsv_to_hex(base_hue, 40, 10),      # dark
        'surface': hsv_to_hex(base_hue, 50, 25),
        'surface2': hsv_to_hex(base_hue, 45, 35),
        'text': '#FFFFFF',
        'muted': '#B0B0B0',
        'primary': hsv_to_hex(base_hue, 100, 70),        # vibrant
        'accent': hsv_to_hex((base_hue+180)%360, 100, 100), # complementary
        'success': hsv_to_hex(120, 70, 60),
        'warning': hsv_to_hex(40, 100, 100),
        'error': hsv_to_hex(0, 80, 90),
    }
    return theme
```

### 3.3 Kivy Animations - Theme Transition

```python
# src/ui/animations.py
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout

class ThemeTransitionAnimator:
    """Animuje przejście między motywami"""
    
    @staticmethod
    def animate_theme_change(widget, old_theme, new_theme, duration=0.5):
        """
        Fade out, zmiana tematu, fade in
        """
        # Fade OUT
        anim_out = Animation(opacity=0, duration=duration/2)
        anim_out.bind(on_complete=lambda *args: (
            ThemeTransitionAnimator._apply_theme(widget, new_theme),
        ))
        
        # Fade IN
        anim_in = Animation(opacity=1, duration=duration/2)
        
        def on_fade_out(*args):
            anim_in.start(widget)
        
        anim_out.bind(on_complete=on_fade_out)
        anim_out.start(widget)
    
    @staticmethod
    def _apply_theme(widget, theme):
        """Nakłada nowy motyw na widżet"""
        widget.canvas.clear()
        with widget.canvas.before:
            Color(*ThemeTransitionAnimator.hex_to_rgba(theme['background']))
            Rectangle(size=widget.size, pos=widget.pos)
        widget.theme_data = theme
```

### 3.4 Użytkownik łączy A + B + Animations

```python
# src/services/theme_service.py
class ThemeService:
    def __init__(self):
        self.custom_themes = {}  # Generowane dinamicznie
        self.hardcoded_themes = HARDCODED_THEMES
        
    def get_theme(self, theme_id):
        """Zwraca motyw z cache'u lub hardcoded'a"""
        if theme_id in self.hardcoded_themes:
            return self.hardcoded_themes[theme_id]
        elif theme_id in self.custom_themes:
            return self.custom_themes[theme_id]
        raise ValueError(f"Theme {theme_id} not found")
    
    def create_custom_theme(self, theme_id, base_hue, name):
        """Generuje custom motyw (Opcja B)"""
        theme = generate_theme_from_hue(base_hue, name)
        self.custom_themes[theme_id] = theme
        # Zapisz do DB settings
        repository.save_custom_theme(theme_id, theme)
        return theme
    
    def apply_theme_with_animation(self, app, theme_id, duration=0.5):
        """Zmienia motyw z animacją"""
        new_theme = self.get_theme(theme_id)
        ThemeTransitionAnimator.animate_theme_change(
            app.root, 
            app.current_theme, 
            new_theme,
            duration=duration
        )
        app.current_theme = new_theme
        # Zapisz w DB
        repository.update_setting('theme_id', theme_id)
```

---

## 4. FLOW KALKULACJI GODZIN

### 4.1 Podstawowe równania

```
czas_brutto = czas_koniec - czas_start
czas_netto = czas_brutto - przerwa

Obsługa:
- Przejścia przez północ (22:00 - 06:00)
- Walidacja: koniec >= start (lub +24h)
- Walidacja: przerwa <= czas_brutto
- Dni "nie-praca" mają czas = 0
```

### 4.2 Obsługiwane przypadki edge'owe

| Przypadek | Logika | Funkcja |
|-----------|--------|---------|
| **22:00 - 06:00 (przejście)** | +1 dzień = 22→22 | `handle_midnight_crossing()` |
| **Przerwa > brutto** | Validation error | `validate_break()` |
| **Brak wpisu dzisiaj** | Wizualna flaga | `is_entry_missing()` |
| **Urlop/Chorobowe** | Czas = ignoruj obliczenia | `get_time_for_day_type()` |
| **Święto** | Czas = 0, brak wpisu | `is_holiday()` |
| **Częściowy dzień** | Proporcjonalna suma | Autorytarna w raporcie |

### 4.3 Pseudocode serwisu kalkulacji

```python
# src/services/calc_service.py
from datetime import datetime, timedelta

class CalcService:
    
    @staticmethod
    def calculate_work_time(
        start: str,      # "08:30"
        end: str,        # "17:00"
        break_minutes: int,
        day_type: str    # "work" | "vacation" | "sick" | "holiday" | "other"
    ) -> dict:
        """
        Returns: {
            'gross_minutes': int,
            'gross_formatted': "HH:MM",
            'net_minutes': int,
            'net_formatted': "HH:MM",
            'is_valid': bool,
            'errors': list
        }
        """
        errors = []
        
        # Parsuj czasy
        start_dt = datetime.strptime(start, "%H:%M")
        end_dt = datetime.strptime(end, "%H:%M")
        
        # Obsługa przejścia przez północ
        if end_dt <= start_dt:
            end_dt += timedelta(days=1)
        
        # Oblicz brutto
        gross = (end_dt - start_dt).total_seconds() // 60
        
        # Walidacja
        if gross <= 0:
            errors.append("Koniec musi być po starcie")
        if break_minutes > gross:
            errors.append(f"Przerwa ({break_minutes}min) > czas brutto ({gross}min)")
        
        # Oblicz netto
        net = max(0, gross - break_minutes)
        
        # Dla dni "nie-praca"
        if day_type != "work":
            return {
                'gross_minutes': 0,
                'gross_formatted': "0:00",
                'net_minutes': 0,
                'net_formatted': "0:00",
                'is_valid': True,
                'errors': [],
                'reason': f"Typ dnia: {day_type}"
            }
        
        return {
            'gross_minutes': int(gross),
            'gross_formatted': CalcService.minutes_to_hm(gross),
            'net_minutes': int(net),
            'net_formatted': CalcService.minutes_to_hm(net),
            'is_valid': len(errors) == 0,
            'errors': errors,
        }
    
    @staticmethod
    def minutes_to_hm(minutes: int) -> str:
        """Konwertuj minuty na "HH:MM" """
        h = minutes // 60
        m = minutes % 60
        return f"{h}:{m:02d}"
    
    @staticmethod
    def calculate_month_summary(entries: list) -> dict:
        """
        Podsumowanie całego miesiąca
        """
        total_net = 0
        total_gross = 0
        day_type_counts = {
            'work': 0,
            'vacation': 0,
            'sick': 0,
            'holiday': 0,
            'other': 0,
            'missing': 0  # brak wpisu
        }
        
        for entry in entries:
            if entry.day_type == 'work':
                total_net += entry.net_minutes
                total_gross += entry.gross_minutes
                day_type_counts['work'] += 1
            elif entry.day_type in ['vacation', 'sick', 'holiday', 'other']:
                day_type_counts[entry.day_type] += 1
            else:
                day_type_counts['missing'] += 1
        
        return {
            'total_net_minutes': total_net,
            'total_net_formatted': CalcService.minutes_to_hm(total_net),
            'total_gross_minutes': total_gross,
            'total_gross_formatted': CalcService.minutes_to_hm(total_gross),
            'day_counts': day_type_counts,
            'avg_daily_hours': total_gross / max(day_type_counts['work'], 1) if day_type_counts['work'] > 0 else 0,
        }
```

---

## 5. PERSISTENCE LAYER - MULTI-PROFILE CONTEXT

### 5.1 Singleton AppContext

```python
# src/app_context.py
class AppContext:
    """Global application state - singleton"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.active_profile_id: int = None
            self.active_profile: object = None
            self.theme_service: object = None
            self.db_connection: object = None
            self.initialized = True
    
    def initialize(self, db_path: str):
        """Inicjalizuj kontekst app"""
        self.db_connection = Database(db_path)
        self.theme_service = ThemeService()
        self._load_last_profile()
    
    def _load_last_profile(self):
        """Wczytaj ostatnio używany profil"""
        last_profile_id = self.db_connection.get_setting('last_profile_id')
        if last_profile_id:
            self.switch_profile(last_profile_id)
        else:
            # Stwórz default profile
            profile = self.db_connection.create_profile("Default User")
            self.switch_profile(profile['id'])
    
    def switch_profile(self, profile_id: int):
        """Przełącz na inny profil"""
        profile = self.db_connection.get_profile(profile_id)
        self.active_profile_id = profile_id
        self.active_profile = profile
        self.db_connection.update_setting('last_profile_id', profile_id)
        # Wczytaj motyw profilu
        theme_id = self.db_connection.get_setting(
            'theme_id',
            profile_id=profile_id
        ) or 1
        self.load_theme(theme_id)
    
    def load_theme(self, theme_id: int, animate=True):
        """Wczytaj motyw z animacją"""
        theme = self.theme_service.get_theme(theme_id)
        if animate and hasattr(self, 'app_instance'):
            self.theme_service.apply_theme_with_animation(
                self.app_instance,
                theme_id
            )
        return theme

# Globals
app_context = AppContext()
```

---

## 6. DATA ACCESS LAYER - Repository Pattern

```python
# src/repository.py
class WorkEntryRepository:
    """Abstrakcja dostępu do work_entries"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create_entry(
        self,
        profile_id: int,
        date: str,
        start_time: str,
        end_time: str,
        break_minutes: int,
        day_type: str,
        notes: str = ""
    ) -> dict:
        """Dodaj nowy wpis"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            INSERT INTO work_entries 
            (profile_id, date, start_time, end_time, break_minutes, day_type, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        """, (profile_id, date, start_time, end_time, break_minutes, day_type, notes))
        self.db.conn.commit()
        return {'id': cursor.lastrowid}
    
    def get_entry(self, profile_id: int, date: str) -> dict:
        """Pobrań wpis dla daty"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT * FROM work_entries
            WHERE profile_id = ? AND date = ?
        """, (profile_id, date))
        row = cursor.fetchone()
        return self._row_to_dict(row) if row else None
    
    def get_month_entries(self, profile_id: int, year: int, month: int) -> list:
        """Pobrać wszystkie wpisy za miesiąc"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT * FROM work_entries
            WHERE profile_id = ? AND strftime('%Y-%m', date) = ?
            ORDER BY date ASC
        """, (profile_id, f"{year:04d}-{month:02d}"))
        return [self._row_to_dict(row) for row in cursor.fetchall()]
    
    def update_entry(self, entry_id: int, **kwargs) -> bool:
        """Aktualizuj wpis"""
        allowed_fields = ['start_time', 'end_time', 'break_minutes', 'day_type', 'notes']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return False
        
        updates['updated_at'] = datetime.now().isoformat()
        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        cursor = self.db.conn.cursor()
        cursor.execute(f"""
            UPDATE work_entries SET {set_clause} WHERE id = ?
        """, list(updates.values()) + [entry_id])
        self.db.conn.commit()
        return cursor.rowcount > 0
    
    def delete_entry(self, entry_id: int) -> bool:
        """Usuń wpis"""
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM work_entries WHERE id = ?", (entry_id,))
        self.db.conn.commit()
        return cursor.rowcount > 0
    
    def _row_to_dict(self, row):
        """Konwertuj SQLite row do dict"""
        return {
            'id': row[0],
            'profile_id': row[1],
            'date': row[2],
            'start_time': row[3],
            'end_time': row[4],
            'break_minutes': row[5],
            'day_type': row[6],
            'notes': row[7],
            'created_at': row[8],
            'updated_at': row[9],
        }
```

---

## 7. BUSINESS LOGIC SERVICES

### 7.1 Service Locator Pattern

```python
# src/services/__init__.py
from .calc_service import CalcService
from .pdf_service import PDFService
from .reminder_service import ReminderService
from .theme_service import ThemeService

class ServiceLocator:
    """Rejestr serwisów - dependency injection"""
    _services = {}
    
    @classmethod
    def register(cls, name: str, service):
        cls._services[name] = service
    
    @classmethod
    def get(cls, name: str):
        if name not in cls._services:
            raise ValueError(f"Service {name} not registered")
        return cls._services[name]

# Inicjalizacja w main.py
def setup_services():
    ServiceLocator.register('calc', CalcService())
    ServiceLocator.register('pdf', PDFService())
    ServiceLocator.register('reminder', ReminderService())
    ServiceLocator.register('theme', ThemeService())

# Użycie
calc_service = ServiceLocator.get('calc')
result = calc_service.calculate_work_time(...)
```

---

## 8. PDF GENERATION SERVICE

```python
# src/services/pdf_service.py
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

class PDFService:
    
    def generate_monthly_report(
        self,
        profile: dict,
        employer: dict,
        entries: list,
        summary: dict,
        month: int,
        year: int,
        output_path: str
    ) -> str:
        """
        Generuje PDF raport dla miesiąca
        
        Returns: ścieżka do pliku PDF
        """
        from datetime import datetime
        
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Tytuł
        title = Paragraph(
            f"Raport godzin pracy - {datetime(year, month, 1).strftime('%B %Y')}",
            styles['Title']
        )
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Dane pracownika
        employee_data = [
            ['Pracownik:', profile['name']],
            ['Pracodawca:', employer['name']],
            ['Okres:', f"{month}/{year}"],
        ]
        employee_table = Table(employee_data, colWidths=[2*inch, 4*inch])
        story.append(employee_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Tabela wpisów
        table_data = [
            ['Data', 'Typ', 'Start', 'Koniec', 'Przerwa', 'Netto', 'Notatka']
        ]
        
        for entry in entries:
            if entry['day_type'] == 'work':
                table_data.append([
                    entry['date'],
                    entry['day_type'],
                    entry['start_time'],
                    entry['end_time'],
                    f"{entry['break_minutes']}min",
                    f"{entry['net_minutes']}min",
                    entry['notes'],
                ])
        
        entries_table = Table(table_data, colWidths=[1.2*inch]*7)
        entries_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(entries_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Podsumowanie
        summary_data = [
            ['Razem godzin netto:', summary['total_net_formatted']],
            ['Razem godzin brutto:', summary['total_gross_formatted']],
            ['Dni pracy:', summary['day_counts']['work']],
            ['Dni urlopu:', summary['day_counts']['vacation']],
            ['Dni chorobowe:', summary['day_counts']['sick']],
        ]
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        story.append(summary_table)
        
        # Renderuj PDF
        doc.build(story)
        return output_path
```

---

## 9. ANDROID NATIVE INTEGRATION

```python
# src/services/share_android.py
from kivy.core.window import Window
from android.intent import Intent
from android.content import Intent as ContentIntent
from android.net import Uri

class ShareService:
    """Integracja z Android Native API"""
    
    @staticmethod
    def share_pdf(pdf_path: str, mimetype: str = "application/pdf"):
        """Udostępnij PDF przez Android Intent"""
        try:
            PythonJavaClass = autoclass('org.kivy.android.PythonActivity')
            current_activity = PythonJavaClass.mActivity
            
            intent = Intent()
            intent.setAction(Intent.ACTION_SEND)
            intent.setType(mimetype)
            
            uri = Uri.fromFile(File(pdf_path))
            intent.putExtra(Intent.EXTRA_STREAM, uri)
            
            current_activity.startActivity(intent)
            return True
        except Exception as e:
            print(f"Share error: {e}")
            return False
    
    @staticmethod
    def open_file_picker(folder_path: str) -> str:
        """Otworz picker dla wybrania folderu zapisu"""
        # Alternativa: Intent do ACTION_OPEN_DOCUMENT_TREE
        return folder_path
```

---

## 10. PODSUMOWANIE ARCHITEKTURY

| Komponent | Wzorzec | Odpowiedzialność |
|-----------|---------|------------------|
| **AppContext** | Singleton | Globalny stan aplikacji, zarządzanie profilami |
| **Repository** | Repository Pattern | Abstrakcja dostępu do danych |
| **Services** | Service Locator | Logika biznesowa, kalkulacje, integracje |
| **UI Layers** | MVP | Presentacja, routing, state management |
| **Themes** | Strategy (A+B) | Motywów + Animations |
| **Database** | SQLite + Migrations | Persystencja multi-profile |

**Przewagi tej architektury:**
- ✅ Łatwe testowanie (loose coupling)
- ✅ Skalowalna (nowe serwisy bez zmian w core)
- ✅ Multi-profile z isolated data
- ✅ Łatwe dodawanie nowych motywów (A+B)
- ✅ Animacje integrowane w theme switching
- ✅ Gotowa do team development

---

**NEXT:** Database Schema + DDL + Migrations
