"""
Migrations - System kontroli wersji bazy danych
"""

import sqlite3
from pathlib import Path
from typing import List, Tuple
import logging
import re

logger = logging.getLogger(__name__)


class MigrationRunner:
    """
    Zarządza migracjami bazy danych
    
    - Detektuje pliki migracji SQL
    - Śledzi zastosowane migracje
    - Uruchamia nowe migracje w porządku
    """
    
    def __init__(self, db_path: str, migrations_dir: str = "src/db/migrations"):
        """
        Inicjalizuj runner migracji
        
        Args:
            db_path: Ścieżka do bazy danych
            migrations_dir: Folder zawierający pliki migracji
        """
        self.db_path = Path(db_path)
        self.migrations_dir = Path(migrations_dir)
        self.connection: sqlite3.Connection = None
        self._init_migrations_table()
    
    def _init_migrations_table(self) -> None:
        """Utwórz tabelę do śledzenia migracji"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version TEXT PRIMARY KEY,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        logger.info("Tabela migracji zainicjalizowana")
    
    def get_applied_migrations(self) -> List[str]:
        """Pobierz listę zastosowanych migracji"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT version FROM schema_migrations ORDER BY version")
        versions = [row[0] for row in cursor.fetchall()]
        conn.close()
        return versions
    
    def get_pending_migrations(self) -> List[Tuple[str, Path]]:
        """
        Pobierz listę niezastosowanych migracji
        
        Returns:
            Lista (version, path) migracji do uruchomienia
        """
        if not self.migrations_dir.exists():
            logger.warning(f"Folder migracji nie istnieje: {self.migrations_dir}")
            return []
        
        # Pobierz wszystkie pliki SQL
        migration_files = sorted(self.migrations_dir.glob("*.sql"))
        
        # Pobierz zastosowane
        applied = set(self.get_applied_migrations())
        
        # Filtruj niezastosowane
        pending = []
        for file_path in migration_files:
            version = self._extract_version(file_path.name)
            if version and version not in applied:
                pending.append((version, file_path))
        
        return pending
    
    def _extract_version(self, filename: str) -> str:
        """Wyodrębni wersję z nazwy pliku"""
        match = re.match(r'(\d{8}_\d{6})', filename)
        return match.group(1) if match else None
    
    def run_pending_migrations(self) -> int:
        """
        Uruchom wszystkie niezastosowane migracje
        
        Returns:
            Liczba uruchomionych migracji
        """
        pending = self.get_pending_migrations()
        
        if not pending:
            logger.info("Brak nowych migracji do uruchomienia")
            return 0
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        count = 0
        for version, file_path in pending:
            try:
                logger.info(f"Uruchamiam migrację: {file_path.name}")
                
                # Przeczytaj plik SQL
                sql_content = file_path.read_text(encoding='utf-8')
                
                # Uruchom instrukcje
                cursor.executescript(sql_content)
                
                # Zaznacz jako zastosowaną
                cursor.execute(
                    "INSERT INTO schema_migrations (version) VALUES (?)",
                    (version,)
                )
                conn.commit()
                
                logger.info(f"✓ Migracja zastosowana: {version}")
                count += 1
                
            except Exception as e:
                logger.error(f"✗ Błąd migracji {version}: {e}")
                conn.rollback()
                raise
        
        conn.close()
        logger.info(f"Zastosowano {count} migracji")
        return count
    
    def get_status(self) -> str:
        """Zwróć status migracji"""
        applied = self.get_applied_migrations()
        pending = self.get_pending_migrations()
        
        status = f"\nStatus migracji:\n"
        status += f"Zastosowane: {len(applied)}\n"
        
        if applied:
            for version in applied:
                status += f"  ✓ {version}\n"
        
        status += f"\nNiezastosowane: {len(pending)}\n"
        if pending:
            for version, path in pending:
                status += f"  • {version} ({path.name})\n"
        
        return status


__all__ = ['MigrationRunner']
