"""
ProfileRepository - Warstwa dostępu do danych profili
"""

from typing import List, Optional, Dict
from src.db import Database
from src.models import Profile
import logging

logger = logging.getLogger(__name__)


class ProfileRepository:
    """
    Repozytorium do obsługi profili użytkowników
    
    Zapewnia:
    - CRUD operacje
    - Zarządzanie profilami
    - Konwersję między modelami i bazą
    """
    
    def __init__(self, database: Database):
        """
        Inicjalizuj repozytorium
        
        Args:
            database: Instancja bazy danych
        """
        self.db = database
    
    def create(self, profile: Profile) -> int:
        """
        Utwórz nowy profil
        
        Args:
            profile: Obiekt Profile
            
        Returns:
            ID utworzonego profilu
            
        Raises:
            ValueError: Jeśli profil jest niepoprawny
        """
        if not profile.name:
            raise ValueError("Nazwa profilu jest wymagana")
        
        return self.db.create_profile(profile.name)
    
    def get_by_id(self, profile_id: int) -> Optional[Profile]:
        """
        Pobierz profil po ID
        
        Args:
            profile_id: ID profilu
            
        Returns:
            Profile lub None jeśli nie znaleziono
        """
        row = self.db.get_profile(profile_id)
        if row:
            return self._row_to_model(row)
        return None
    
    def get_all(self) -> List[Profile]:
        """
        Pobierz wszystkie profile
        
        Returns:
            Lista Profile
        """
        rows = self.db.get_all_profiles()
        return [self._row_to_model(row) for row in rows]
    
    def delete(self, profile_id: int) -> bool:
        """
        Usuń profil (cascading delete)
        
        Args:
            profile_id: ID profilu
            
        Returns:
            True jeśli usuwanie się powiodło
        """
        result = self.db.delete_profile(profile_id)
        if result:
            logger.info(f"Profil ID {profile_id} usunięty")
        return result
    
    def exists(self, profile_id: int) -> bool:
        """Sprawdź czy profil istnieje"""
        return self.get_by_id(profile_id) is not None
    
    def count(self) -> int:
        """Zlicz wszystkie profile"""
        return len(self.get_all())
    
    def _row_to_model(self, row: Dict) -> Profile:
        """Konwertuj rząd bazy do modelu Profile"""
        return Profile(
            id=row['id'],
            name=row['name'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )


__all__ = ['ProfileRepository']
