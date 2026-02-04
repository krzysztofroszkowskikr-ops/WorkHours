"""
Models - Definicje struktur danych aplikacji WorkHours
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Profile:
    """
    Model profilu użytkownika
    
    Atrybuty:
        id: Unikalny identyfikator profilu
        name: Nazwa profilu (unikalna)
        created_at: Timestamp utworzenia
        updated_at: Timestamp ostatniej aktualizacji
    """
    id: Optional[int] = None
    name: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()


@dataclass
class WorkEntry:
    """
    Model wpisu pracy
    
    Atrybuty:
        id: Unikalny identyfikator wpisu
        profile_id: ID profilu właściciela wpisu
        date: Data wpisu (YYYY-MM-DD)
        start_time: Godzina startu pracy (HH:MM)
        end_time: Godzina końca pracy (HH:MM)
        break_minutes: Długość przerwy w minutach
        day_type: Typ dnia (work_day, sick_day, vacation, day_off)
        notes: Opcjonalne notatki
        created_at: Timestamp utworzenia
        updated_at: Timestamp ostatniej aktualizacji
    """
    id: Optional[int] = None
    profile_id: int = 1
    date: str = ""
    start_time: str = ""
    end_time: str = ""
    break_minutes: int = 0
    day_type: str = "work_day"
    notes: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Konwertuj model do słownika"""
        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'break_minutes': self.break_minutes,
            'day_type': self.day_type,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


@dataclass
class Setting:
    """
    Model ustawienia profilu
    
    Atrybuty:
        id: Unikalny identyfikator
        profile_id: ID profilu
        key: Klucz ustawienia
        value: Wartość (string)
        type: Typ wartości (string, int, bool)
        created_at: Timestamp
        updated_at: Timestamp
    """
    id: Optional[int] = None
    profile_id: int = 1
    key: str = ""
    value: str = ""
    type: str = "string"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()


@dataclass
class CustomTheme:
    """
    Model niestandardowego motywu (Opcja B)
    
    Atrybuty:
        id: Unikalny identyfikator
        profile_id: ID profilu
        theme_id: ID motywu (100+)
        name: Nazwa motywu
        config_json: Konfiguracja w JSON (kolory, style)
        created_at: Timestamp
    """
    id: Optional[int] = None
    profile_id: int = 1
    theme_id: int = 100
    name: str = ""
    config_json: str = "{}"
    created_at: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


__all__ = ['Profile', 'WorkEntry', 'Setting', 'CustomTheme']
