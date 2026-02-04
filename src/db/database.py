"""
Database - Warstwa dostępu do danych SQLite
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Database:
    """
    Wrapper dla bazy danych SQLite
    
    Zarządza:
    - Połączeniami z bazą
    - Schematem bazy danych
    - Operacjami CRUD
    - Transakcjami
    """
    
    def __init__(self, db_path: str = "workhours_app.db"):
        """
        Inicjalizuj bazę danych
        
        Args:
            db_path: Ścieżka do pliku bazy danych
        """
        self.db_path = Path(db_path)
        self.connection: Optional[sqlite3.Connection] = None
        self.initialize()
    
    def initialize(self) -> None:
        """Inicjalizuj schemat bazy danych"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Tabela profili
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela wpisów pracy
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS work_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    start_time TEXT,
                    end_time TEXT,
                    break_minutes INTEGER DEFAULT 0,
                    day_type TEXT DEFAULT 'work_day',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
                    UNIQUE(profile_id, date)
                )
            """)
            
            # Tabela ustawień
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id INTEGER NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    type TEXT DEFAULT 'string',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
                    UNIQUE(profile_id, key)
                )
            """)
            
            # Tabela niestandardowych motywów
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS custom_themes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id INTEGER NOT NULL,
                    theme_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    config_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
                )
            """)
            
            # Indeksy dla wydajności
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_work_entries_profile_date
                ON work_entries(profile_id, date)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_work_entries_profile_month
                ON work_entries(profile_id, strftime('%Y-%m', date))
            """)
            
            # Domyślny profil
            cursor.execute("SELECT COUNT(*) FROM profiles")
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO profiles (name) VALUES (?)",
                    ("Default User",)
                )
                logger.info("Domyślny profil stworzony")
            
            conn.commit()
            logger.info(f"Baza danych zainicjalizowana: {self.db_path}")
            
        except Exception as e:
            logger.error(f"Błąd inicjalizacji bazy: {e}")
            conn.rollback()
            raise
    
    def get_connection(self) -> sqlite3.Connection:
        """Pobierz aktywne połączenie z bazą"""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self) -> None:
        """Zamknij połączenie z bazą"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Połączenie z bazą zamknięte")
    
    # ═══════════════════════════════════════════════════════════════════════
    # OPERACJE PROFILI
    # ═══════════════════════════════════════════════════════════════════════
    
    def create_profile(self, name: str) -> int:
        """
        Utwórz nowy profil
        
        Args:
            name: Nazwa profilu
            
        Returns:
            ID nowego profilu
            
        Raises:
            ValueError: Jeśli profil już istnieje
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO profiles (name) VALUES (?)",
                (name,)
            )
            conn.commit()
            profile_id = cursor.lastrowid
            logger.info(f"Profil '{name}' (ID: {profile_id}) stworzony")
            return profile_id
        except sqlite3.IntegrityError:
            logger.error(f"Profil '{name}' już istnieje")
            raise ValueError(f"Profil '{name}' już istnieje")
    
    def get_all_profiles(self) -> List[Dict]:
        """Pobierz wszystkie profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profiles ORDER BY created_at")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_profile(self, profile_id: int) -> Optional[Dict]:
        """Pobierz profil po ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def delete_profile(self, profile_id: int) -> bool:
        """Usuń profil (cascading delete)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
            conn.commit()
            logger.info(f"Profil ID {profile_id} usunięty")
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Błąd usuwania profilu: {e}")
            conn.rollback()
            raise
    
    # ═══════════════════════════════════════════════════════════════════════
    # OPERACJE WPISÓW PRACY
    # ═══════════════════════════════════════════════════════════════════════
    
    def insert_work_entry(self, entry: Dict) -> int:
        """
        Dodaj lub zaktualizuj wpis pracy (UPSERT)
        
        Args:
            entry: Słownik z danymi wpisu
            
        Returns:
            ID wpisu
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO work_entries
                (profile_id, date, start_time, end_time, break_minutes, day_type, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                entry['profile_id'],
                entry['date'],
                entry['start_time'],
                entry['end_time'],
                entry['break_minutes'],
                entry['day_type'],
                entry['notes']
            ))
            conn.commit()
            logger.info(f"Wpis {entry['date']} zapisany dla profilu {entry['profile_id']}")
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Błąd zapisywania wpisu: {e}")
            conn.rollback()
            raise
    
    def get_work_entry(self, profile_id: int, date: str) -> Optional[Dict]:
        """Pobierz wpis dla danego dnia"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM work_entries WHERE profile_id = ? AND date = ?",
            (profile_id, date)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_work_entries_month(self, profile_id: int, year: int, month: int) -> List[Dict]:
        """Pobierz wszystkie wpisy z miesiąca"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM work_entries
            WHERE profile_id = ? AND strftime('%Y-%m', date) = ?
            ORDER BY date
        """, (profile_id, f"{year:04d}-{month:02d}"))
        return [dict(row) for row in cursor.fetchall()]
    
    def delete_work_entry(self, profile_id: int, date: str) -> bool:
        """Usuń wpis"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM work_entries WHERE profile_id = ? AND date = ?",
            (profile_id, date)
        )
        conn.commit()
        return cursor.rowcount > 0
    
    # ═══════════════════════════════════════════════════════════════════════
    # OPERACJE USTAWIEŃ
    # ═══════════════════════════════════════════════════════════════════════
    
    def set_setting(self, profile_id: int, key: str, value: str, type_: str = "string") -> None:
        """Ustaw ustawienie (UPSERT)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO settings (profile_id, key, value, type)
                VALUES (?, ?, ?, ?)
            """, (profile_id, key, value, type_))
            conn.commit()
        except Exception as e:
            logger.error(f"Błąd ustawienia: {e}")
            conn.rollback()
            raise
    
    def get_setting(self, profile_id: int, key: str) -> Optional[str]:
        """Pobierz wartość ustawienia"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT value FROM settings WHERE profile_id = ? AND key = ?",
            (profile_id, key)
        )
        row = cursor.fetchone()
        return row[0] if row else None
    
    # ═══════════════════════════════════════════════════════════════════════
    # OPERACJE MOTYWÓW
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_custom_themes(self, profile_id: int) -> List[Dict]:
        """Pobierz niestandardowe motywy profilu"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM custom_themes WHERE profile_id = ? ORDER BY created_at",
            (profile_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def insert_custom_theme(self, profile_id: int, theme_id: int, name: str, config_json: str) -> int:
        """Dodaj niestandardowy motyw"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO custom_themes (profile_id, theme_id, name, config_json)
                VALUES (?, ?, ?, ?)
            """, (profile_id, theme_id, name, config_json))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Błąd dodawania motywu: {e}")
            conn.rollback()
            raise


__all__ = ['Database']
