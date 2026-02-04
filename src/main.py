"""
WorkHours App - Entry point aplikacji
"""

import logging
from pathlib import Path
from src.app_context import AppContext
from src.repository import WorkEntryRepository, ProfileRepository
from src.services import CalcService
import sys

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def initialize_app() -> AppContext:
    """
    Inicjalizuj aplikację
    
    Returns:
        Instancja AppContext
    """
    logger.info("Inicjalizowanie aplikacji WorkHours...")
    
    # Ścieżka do bazy danych
    db_path = Path.home() / ".workhours" / "workhours_app.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Pobierz AppContext
    app_context = AppContext.get_instance(str(db_path))
    
    logger.info(f"Baza danych: {db_path}")
    logger.info(f"Obecny profil: {app_context.get_current_profile_name()}")
    
    return app_context


def main():
    """Główna funkcja aplikacji"""
    try:
        # Inicjalizuj
        app = initialize_app()
        
        # Demo: Pobierz obecny profil i wyświetl wpisy
        profile_id = app.get_current_profile_id()
        if profile_id:
            # Pobierz repozytorium
            repo = WorkEntryRepository(app.database)
            
            # Pobierz wpisy z ostatniego miesiąca
            from datetime import datetime
            today = datetime.now()
            
            logger.info(f"\n📊 Wpisy z {today.month:02d}/{today.year}:")
            entries = repo.get_month(profile_id, today.year, today.month)
            
            for entry in entries[:5]:  # Pokaż pierwsze 5
                logger.info(f"  {entry.date}: {entry.start_time}-{entry.end_time}")
            
            if len(entries) > 5:
                logger.info(f"  ... i {len(entries)-5} więcej")
        
        # Zamknij
        app.shutdown()
        logger.info("✅ Aplikacja zamknięta")
        
    except Exception as e:
        logger.error(f"❌ Błąd: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
