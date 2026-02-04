# PROJECT STRUCTURE & MODULE ORGANIZATION
## WorkHours Purple v1.0

---

## 1. COMPLETE PROJECT TREE

```
workhours_app/
├── main.py                          # Entry point
├── app.kv                           # Global KivyMD layouts
├── buildozer.spec                   # Android build configuration
├── requirements.txt                 # Python dependencies
├── pytest.ini                       # Testing configuration
├── .gitignore                       # Git ignore patterns
│
├── src/
│   ├── __init__.py
│   ├── app_context.py              # Singleton app context
│   ├── app.py                       # KivyMD App class
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py             # SQLite wrapper + settings API
│   │   ├── migrations.py           # Migration runner
│   │   ├── backup.py               # Backup manager
│   │   └── migrations/
│   │       ├── 20260204_000000_initial_schema.sql
│   │       ├── 20260205_000000_add_custom_themes.sql
│   │       └── 20260206_000000_default_profile_and_settings.sql
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── work_entry.py           # WorkEntry dataclass
│   │   ├── profile.py              # Profile dataclass
│   │   └── settings.py             # Settings model
│   │
│   ├── repository/
│   │   ├── __init__.py
│   │   ├── base_repository.py      # Abstract base class
│   │   ├── work_entry_repository.py
│   │   ├── profile_repository.py
│   │   └── settings_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── service_locator.py      # Dependency injection
│   │   ├── calc_service.py         # Obliczenia godzin
│   │   ├── pdf_service.py          # Generowanie PDF
│   │   ├── reminder_service.py     # Powiadomienia
│   │   ├── theme_service.py        # Zarządzanie motywami (A+B+anim)
│   │   └── share_service.py        # Integracja Android
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py           # Validatory (daty, czasy)
│   │   ├── formatters.py           # Formatownie (HH:MM, JSON)
│   │   ├── constants.py            # Globalne stałe
│   │   └── logger.py               # Logging utility
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── screens/
│   │   │   ├── __init__.py
│   │   │   ├── base_screen.py      # Base class dla screens
│   │   │   ├── dashboard_screen.py # Miesiąc overview
│   │   │   ├── entry_screen.py     # Dodaj/Edytuj wpis
│   │   │   ├── report_screen.py    # Raport PDF
│   │   │   ├── settings_screen.py  # Ustawienia
│   │   │   └── profile_screen.py   # Zarządzanie profilami
│   │   │
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── day_card.py         # Card dla jednego dnia
│   │   │   ├── time_picker.py      # Custom time picker
│   │   │   ├── day_type_chips.py   # Chipy (work/vacation/itd)
│   │   │   ├── month_selector.py   # Selektor miesiąca
│   │   │   └── custom_widgets.py   # Inne reusable widgets
│   │   │
│   │   ├── themes/
│   │   │   ├── __init__.py
│   │   │   ├── theme_definitions.py # Opcja A (hardcoded)
│   │   │   ├── theme_loader.py     # Loader dla themes
│   │   │   └── animations.py       # Kivy animations
│   │   │
│   │   └── styles.kv               # Global KivyMD styles
│   │
│   └── assets/
│       ├── icons/
│       │   ├── app_icon.png        # 512x512
│       │   ├── notification.png
│       │   └── [inne ikony]
│       │
│       └── fonts/
│           └── [custom fonts]
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   ├── test_calc_service.py        # Unit testy obliczeń
│   ├── test_validators.py          # Unit testy validatorów
│   ├── test_pdf_generation.py      # Integration testy PDF
│   ├── test_database.py            # Database layer testy
│   ├── test_theme_service.py       # Theme engine testy
│   └── fixtures/
│       ├── sample_entries.json     # Sample test data
│       └── sample_profiles.json
│
├── docs/
│   ├── API.md                      # API documentation
│   ├── THEME_SYSTEM.md             # Theme system guide
│   ├── DATABASE.md                 # Database documentation
│   ├── SETUP_DEV.md                # Developer setup
│   └── DEPLOYMENT.md               # Build & deployment
│
├── android/
│   └── buildozer/
│       └── [buildozer output]
│
└── .github/
    └── workflows/
        ├── build.yml               # CI/CD build APK
        └── tests.yml               # Run tests
```

---

## 2. MODULE DESCRIPTIONS & RESPONSIBILITIES

### 2.1 Entry Point: `main.py`

```python
"""
main.py - WorkHours Purple Application Entry Point
"""

from kivy.app import App
from src.app import WorkHoursApp
from src.app_context import app_context
from src.services import ServiceLocator

if __name__ == '__main__':
    # Initialize
    app_context.initialize(db_path='user_data/workhours.db')
    
    # Register services
    ServiceLocator.setup_all()
    
    # Run app
    app = WorkHoursApp()
    app.run()
```

---

### 2.2 Core Application: `src/app.py`

```python
"""
src/app.py - Main KivyMD Application Class
"""

from kivy.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.app import MDApp
from src.ui.screens import DashboardScreen, EntryScreen, ReportScreen, SettingsScreen, ProfileScreen
from src.app_context import app_context

class WorkHoursApp(MDApp):
    def build(self):
        self.title = "WorkHours Purple"
        self.theme_cls.theme_style = "Dark"
        
        # Setup screens
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(EntryScreen(name='entry'))
        sm.add_widget(ReportScreen(name='report'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(ProfileScreen(name='profile'))
        
        app_context.app_instance = self
        self.root = sm
        
        return self.root
```

---

### 2.3 Models: `src/models/`

```python
# src/models/work_entry.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class WorkEntry:
    id: Optional[int] = None
    profile_id: int = None
    date: str = None  # YYYY-MM-DD
    start_time: Optional[str] = None  # HH:MM
    end_time: Optional[str] = None
    break_minutes: int = 0
    day_type: str = 'work'  # work/vacation/sick/holiday/other
    notes: str = ''
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    # Computed properties (nie w DB)
    net_minutes: Optional[int] = None
    gross_minutes: Optional[int] = None
    
    def is_work_day(self) -> bool:
        return self.day_type == 'work'
    
    def is_complete(self) -> bool:
        """Check if all required fields filled for work day"""
        if not self.is_work_day():
            return True
        return all([self.date, self.start_time, self.end_time])

# src/models/profile.py
@dataclass
class Profile:
    id: Optional[int] = None
    name: str = ''
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

# src/models/settings.py
@dataclass
class Setting:
    id: Optional[int] = None
    profile_id: int = None
    key: str = ''
    value: str = ''
    type: str = 'string'  # string/integer/boolean/json
```

---

### 2.4 Repository Pattern: `src/repository/`

```python
# src/repository/base_repository.py
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    """Abstract base for all repositories"""
    
    def __init__(self, db):
        self.db = db
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id):
        pass

# src/repository/work_entry_repository.py
from src.models import WorkEntry
from src.utils.validators import validate_date, validate_time

class WorkEntryRepository(BaseRepository):
    
    def create(self, entry: WorkEntry) -> int:
        """Returns: entry_id"""
        # Validate
        validate_date(entry.date)
        if entry.is_work_day():
            validate_time(entry.start_time)
            validate_time(entry.end_time)
        
        cursor = self.db.conn.cursor()
        cursor.execute("""
            INSERT INTO work_entries 
            (profile_id, date, start_time, end_time, break_minutes, day_type, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            entry.profile_id, entry.date, entry.start_time, entry.end_time,
            entry.break_minutes, entry.day_type, entry.notes
        ))
        self.db.conn.commit()
        return cursor.lastrowid
    
    def get_by_id(self, entry_id: int) -> WorkEntry:
        """Get single entry by ID"""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM work_entries WHERE id = ?", (entry_id,))
        row = cursor.fetchone()
        return self._map_to_entity(row) if row else None
    
    def get_by_date(self, profile_id: int, date: str) -> WorkEntry:
        """Get entry for specific date"""
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT * FROM work_entries WHERE profile_id = ? AND date = ?",
            (profile_id, date)
        )
        row = cursor.fetchone()
        return self._map_to_entity(row) if row else None
    
    def get_month(self, profile_id: int, year: int, month: int) -> list:
        """Get all entries for month"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT * FROM work_entries
            WHERE profile_id = ? AND strftime('%Y-%m', date) = ?
            ORDER BY date ASC
        """, (profile_id, f"{year:04d}-{month:02d}"))
        return [self._map_to_entity(row) for row in cursor.fetchall()]
    
    def update(self, entry: WorkEntry) -> bool:
        """Update entry"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            UPDATE work_entries 
            SET start_time = ?, end_time = ?, break_minutes = ?, day_type = ?, notes = ?,
                updated_at = datetime('now')
            WHERE id = ?
        """, (entry.start_time, entry.end_time, entry.break_minutes, 
              entry.day_type, entry.notes, entry.id))
        self.db.conn.commit()
        return cursor.rowcount > 0
    
    def delete(self, entry_id: int) -> bool:
        """Delete entry"""
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM work_entries WHERE id = ?", (entry_id,))
        self.db.conn.commit()
        return cursor.rowcount > 0
    
    def _map_to_entity(self, row) -> WorkEntry:
        """Map DB row to WorkEntry"""
        return WorkEntry(
            id=row[0], profile_id=row[1], date=row[2],
            start_time=row[3], end_time=row[4], break_minutes=row[5],
            day_type=row[6], notes=row[7], created_at=row[8], updated_at=row[9]
        )
```

---

### 2.5 Services: `src/services/`

```python
# src/services/service_locator.py
class ServiceLocator:
    """Dependency injection container"""
    _services = {}
    
    @classmethod
    def register(cls, name: str, service):
        cls._services[name] = service
    
    @classmethod
    def get(cls, name: str):
        if name not in cls._services:
            raise ValueError(f"Service '{name}' not registered")
        return cls._services[name]
    
    @classmethod
    def setup_all(cls):
        """Setup all services - call once at app startup"""
        from src.db.database import Database
        from src.repository.work_entry_repository import WorkEntryRepository
        from src.services.calc_service import CalcService
        from src.services.pdf_service import PDFService
        from src.services.reminder_service import ReminderService
        from src.services.theme_service import ThemeService
        from src.services.share_service import ShareService
        from src.app_context import app_context
        
        # Register repositories
        cls.register('work_entry_repo', WorkEntryRepository(app_context.db_connection))
        
        # Register services
        cls.register('calc', CalcService())
        cls.register('pdf', PDFService())
        cls.register('reminder', ReminderService())
        cls.register('theme', ThemeService())
        cls.register('share', ShareService())

# Usage:
# service = ServiceLocator.get('calc')
# result = service.calculate_work_time(...)
```

---

### 2.6 UI Screens: `src/ui/screens/`

```python
# src/ui/screens/base_screen.py
from kivymd.uix.screen import MDScreen

class BaseScreen(MDScreen):
    """Base class for all app screens"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_context = None
    
    def on_enter(self):
        """Called when screen is displayed"""
        from src.app_context import app_context
        self.app_context = app_context
        self.refresh()
    
    def refresh(self):
        """Override in subclasses"""
        pass

# src/ui/screens/dashboard_screen.py
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from src.ui.components import DayCard
from src.services import ServiceLocator

class DashboardScreen(BaseScreen):
    """Main screen - month overview"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.month_entries = []
    
    def on_enter(self):
        super().on_enter()
    
    def refresh(self):
        """Refresh dashboard data"""
        from datetime import datetime
        from src.app_context import app_context
        from src.repository.work_entry_repository import WorkEntryRepository
        
        now = datetime.now()
        repo = WorkEntryRepository(app_context.db_connection)
        self.month_entries = repo.get_month(
            app_context.active_profile_id,
            now.year,
            now.month
        )
        
        # Calculate summary
        calc_service = ServiceLocator.get('calc')
        summary = calc_service.calculate_month_summary(self.month_entries)
        
        # Update UI (stub)
        self.update_ui(summary)
    
    def update_ui(self, summary):
        """Update UI with data"""
        # Build layout with day cards
        pass
```

---

### 2.7 Utils: `src/utils/`

```python
# src/utils/validators.py
import re
from datetime import datetime

def validate_date(date_str: str) -> bool:
    """Validate YYYY-MM-DD format"""
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        raise ValueError(f"Invalid date format: {date_str}")
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        raise ValueError(f"Invalid date: {date_str}")

def validate_time(time_str: str) -> bool:
    """Validate HH:MM format"""
    if not re.match(r'^\d{2}:\d{2}$', time_str):
        raise ValueError(f"Invalid time format: {time_str}")
    h, m = map(int, time_str.split(':'))
    if not (0 <= h < 24 and 0 <= m < 60):
        raise ValueError(f"Invalid time values: {time_str}")
    return True

# src/utils/formatters.py
def minutes_to_hm(minutes: int) -> str:
    """Convert 480 -> "8:00" """
    h = minutes // 60
    m = minutes % 60
    return f"{h}:{m:02d}"

def hm_to_minutes(time_str: str) -> int:
    """Convert "8:30" -> 510"""
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

# src/utils/constants.py
DAY_TYPES = {
    'work': 'Praca',
    'vacation': 'Urlop',
    'sick': 'Chorobowe',
    'holiday': 'Święto',
    'other': 'Inne'
}

DEFAULT_WORK_START = '08:00'
DEFAULT_WORK_END = '17:00'
DEFAULT_BREAK_MINUTES = 60
```

---

## 3. DEPENDENCY GRAPH

```
main.py
  └── AppContext (Singleton)
      └── Database (SQLite)
          └── Repositories
              └── Services
                  ├── CalcService
                  ├── PDFService
                  ├── ReminderService
                  ├── ThemeService
                  └── ShareService
          └── Migrations
              └── SQL scripts
  
  └── App (KivyMD)
      └── Screens
          ├── DashboardScreen
          ├── EntryScreen
          ├── ReportScreen
          ├── SettingsScreen
          └── ProfileScreen
          
      └── UI Components
          ├── DayCard
          ├── TimePicker
          ├── DayTypeChips
          └── MonthSelector
      
      └── Theme Engine
          ├── ThemeService
          ├── ThemeDefinitions (Opcja A)
          ├── ThemeGenerator (Opcja B)
          └── Animations (Kivy)
```

---

## 4. LOADING SEQUENCE (Startup)

```
1. main.py starts
   ├── app_context.initialize()
   │   ├── Database.connect()
   │   ├── MigrationRunner.run_pending()
   │   └── Load last profile
   │
   ├── ServiceLocator.setup_all()
   │   ├── Register repositories
   │   └── Register services
   │
   └── WorkHoursApp.run()
       ├── build()
       ├── Load theme for active profile
       ├── Display DashboardScreen
       └── Start reminder service
```

---

## 5. CODING STANDARDS

### Directory Structure Rules:
- **Python modules**: snake_case (work_entry.py, calc_service.py)
- **Classes**: PascalCase (WorkEntry, CalcService)
- **Functions**: snake_case (calculate_work_time)
- **Constants**: UPPER_SNAKE_CASE (DEFAULT_BREAK_MINUTES)

### Import Organization:
```python
# 1. Standard library
import os
import sqlite3
from datetime import datetime
from pathlib import Path

# 2. Third party
from kivy.uix.widget import Widget
from kivymd.app import MDApp

# 3. Local
from src.models import WorkEntry
from src.services import ServiceLocator
```

### Module Docstrings:
```python
"""
src/services/calc_service.py - Calculation Service

Provides work time calculation, validation, and monthly summaries.
Handles edge cases: midnight crossing, break validation, etc.
"""
```

---

## 6. DEVELOPMENT CHECKLIST

- [ ] Create base folder structure
- [ ] Setup database migrations
- [ ] Implement Repository layer
- [ ] Build Service layer
- [ ] Create UI screens
- [ ] Setup theme system (A+B+animations)
- [ ] Add PDF generation
- [ ] Configure reminders
- [ ] Write unit tests
- [ ] Build & test APK
- [ ] Prepare documentation

---

**NEXT:** Dependencies Matrix & Requirements.txt
