"""
WorkEntryRepository - Warstwa dostępu do danych wpisów pracy
"""

from typing import List, Optional, Dict
from datetime import datetime, timedelta
from src.db import Database
from src.models import WorkEntry
import logging

logger = logging.getLogger(__name__)


class WorkEntryRepository:
    """
    Repozytorium do obsługi wpisów pracy
    
    Zapewnia:
    - CRUD operacje
    - Zapytania po dacie, miesiącu
    - Konwersję między modelami i bazą
    """
    
    def __init__(self, database: Database):
        """
        Inicjalizuj repozytorium
        
        Args:
            database: Instancja bazy danych
        """
        self.db = database
    
    def create(self, work_entry: WorkEntry) -> int:
        """
        Utwórz nowy wpis pracy
        
        Args:
            work_entry: Obiekt WorkEntry
            
        Returns:
            ID utworzonego wpisu
            
        Raises:
            ValueError: Jeśli wpis jest niepoprawny
        """
        if work_entry.profile_id is None:
            raise ValueError("profile_id jest wymagany")
        
        entry_dict = work_entry.to_dict()
        return self.db.insert_work_entry(entry_dict)
    
    def get_by_date(self, profile_id: int, date: str) -> Optional[WorkEntry]:
        """
        Pobierz wpis dla konkretnej daty
        
        Args:
            profile_id: ID profilu
            date: Data YYYY-MM-DD
            
        Returns:
            WorkEntry lub None jeśli nie znaleziono
        """
        row = self.db.get_work_entry(profile_id, date)
        if row:
            return self._row_to_model(row)
        return None
    
    def get_month(self, profile_id: int, year: int, month: int) -> List[WorkEntry]:
        """
        Pobierz wszystkie wpisy z danego miesiąca
        
        Args:
            profile_id: ID profilu
            year: Rok YYYY
            month: Miesiąc 1-12
            
        Returns:
            Lista WorkEntry dla miesiąca
        """
        rows = self.db.get_work_entries_month(profile_id, year, month)
        return [self._row_to_model(row) for row in rows]
    
    def get_week(self, profile_id: int, start_date: str) -> List[WorkEntry]:
        """
        Pobierz wpisy dla tygodnia
        
        Args:
            profile_id: ID profilu
            start_date: Początek tygodnia YYYY-MM-DD
            
        Returns:
            Lista WorkEntry dla tygodnia
        """
        entries = []
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        
        for i in range(7):
            date_str = current_date.strftime("%Y-%m-%d")
            entry = self.get_by_date(profile_id, date_str)
            if entry:
                entries.append(entry)
            current_date += timedelta(days=1)
        
        return entries
    
    def get_date_range(
        self,
        profile_id: int,
        start_date: str,
        end_date: str
    ) -> List[WorkEntry]:
        """
        Pobierz wpisy w zakresie dat
        
        Args:
            profile_id: ID profilu
            start_date: Początkowa data YYYY-MM-DD
            end_date: Końcowa data YYYY-MM-DD
            
        Returns:
            Lista WorkEntry
        """
        entries = []
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current_date <= end_date_obj:
            date_str = current_date.strftime("%Y-%m-%d")
            entry = self.get_by_date(profile_id, date_str)
            if entry:
                entries.append(entry)
            current_date += timedelta(days=1)
        
        return entries
    
    def update(self, work_entry: WorkEntry) -> bool:
        """
        Zaktualizuj wpis pracy
        
        Args:
            work_entry: Obiekt WorkEntry
            
        Returns:
            True jeśli update się powiódł
        """
        entry_dict = work_entry.to_dict()
        self.db.insert_work_entry(entry_dict)  # UPSERT
        return True
    
    def delete(self, profile_id: int, date: str) -> bool:
        """
        Usuń wpis
        
        Args:
            profile_id: ID profilu
            date: Data YYYY-MM-DD
            
        Returns:
            True jeśli usuwanie się powiodło
        """
        return self.db.delete_work_entry(profile_id, date)
    
    def delete_month(self, profile_id: int, year: int, month: int) -> int:
        """
        Usuń wszystkie wpisy z miesiąca
        
        Args:
            profile_id: ID profilu
            year: Rok
            month: Miesiąc
            
        Returns:
            Liczba usuniętych wpisów
        """
        entries = self.get_month(profile_id, year, month)
        count = 0
        
        for entry in entries:
            if self.delete(profile_id, entry.date):
                count += 1
        
        logger.info(f"Usunięto {count} wpisów z {month:02d}/{year}")
        return count
    
    def exists(self, profile_id: int, date: str) -> bool:
        """Sprawdź czy wpis istnieje"""
        return self.get_by_date(profile_id, date) is not None
    
    def count_month(self, profile_id: int, year: int, month: int) -> int:
        """Zlicz wpisy w miesiącu"""
        return len(self.get_month(profile_id, year, month))
    
    def _row_to_model(self, row: Dict) -> WorkEntry:
        """Konwertuj rząd bazy do modelu WorkEntry"""
        return WorkEntry(
            id=row['id'],
            profile_id=row['profile_id'],
            date=row['date'],
            start_time=row['start_time'],
            end_time=row['end_time'],
            break_minutes=row['break_minutes'],
            day_type=row['day_type'],
            notes=row['notes'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )


__all__ = ['WorkEntryRepository']
