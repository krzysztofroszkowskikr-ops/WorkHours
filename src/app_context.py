"""
AppContext - Singleton aplikacji
Centralne miejsce dla wszystkich serwisów i konfiguracji
"""

from typing import Optional
from src.db import Database
from src.services.calc_service import CalcService
from src.utils.validators import Validators
from src.utils.formatters import Formatters
import logging

logger = logging.getLogger(__name__)


class AppContext:
    """
    Singleton AppContext
    
    Zawiera:
    - Instancję bazy danych
    - Serwisy (CalcService, etc.)
    - Obecny profil użytkownika
    - Konfigurację aplikacji
    """
    
    _instance: Optional['AppContext'] = None
    
    def __init__(self, db_path: str = "workhours_app.db"):
        """
        Inicjalizuj AppContext
        
        Args:
            db_path: Ścieżka do bazy danych
        """
        self.database = Database(db_path)
        self.calc_service = CalcService()
        self.validators = Validators()
        self.formatters = Formatters()
        
        # Obecny profil (domyślnie pierwszy)
        self.current_profile_id: Optional[int] = None
        self._load_default_profile()
        
        logger.info("AppContext zainicjalizowany")
    
    @classmethod
    def get_instance(cls, db_path: str = "workhours_app.db") -> 'AppContext':
        """
        Pobierz singleton instancję AppContext
        
        Args:
            db_path: Ścieżka do bazy danych
            
        Returns:
            Instancja AppContext
        """
        if cls._instance is None:
            cls._instance = cls(db_path)
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """Zresetuj singleton (dla testów)"""
        if cls._instance:
            cls._instance.database.close()
            cls._instance = None
    
    def _load_default_profile(self) -> None:
        """Załaduj domyślny profil"""
        profiles = self.database.get_all_profiles()
        if profiles:
            self.current_profile_id = profiles[0]['id']
            logger.info(f"Załadowano profil: {profiles[0]['name']} (ID: {self.current_profile_id})")
    
    def set_current_profile(self, profile_id: int) -> bool:
        """
        Ustaw obecny profil
        
        Args:
            profile_id: ID profilu do ustawienia
            
        Returns:
            True jeśli profil istnieje
        """
        profile = self.database.get_profile(profile_id)
        if profile:
            self.current_profile_id = profile_id
            logger.info(f"Profil zmieniony na: {profile['name']}")
            return True
        
        logger.error(f"Profil ID {profile_id} nie istnieje")
        return False
    
    def get_current_profile_id(self) -> Optional[int]:
        """Pobierz ID obecnego profilu"""
        return self.current_profile_id
    
    def get_current_profile_name(self) -> str:
        """Pobierz nazwę obecnego profilu"""
        if self.current_profile_id:
            profile = self.database.get_profile(self.current_profile_id)
            return profile['name'] if profile else "Unknown"
        return "Unknown"
    
    def shutdown(self) -> None:
        """Zamknij AppContext i zasoby"""
        logger.info("Zamykanie AppContext...")
        if self.database:
            self.database.close()
        AppContext._instance = None


__all__ = ['AppContext']
