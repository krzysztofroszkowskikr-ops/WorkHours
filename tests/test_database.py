"""
Test Database - Testy integracyjne bazy danych
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from src.db import Database


@pytest.fixture
def temp_db():
    """Utwórz tymczasową bazę danych"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        yield db, db_path
        db.close()


class TestDatabaseInitialization:
    """Testy inicjalizacji bazy danych"""
    
    def test_database_creates_tables(self, temp_db):
        """Test czy baza tworzy tabele"""
        db, db_path = temp_db
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Sprawdź czy tabele istnieją
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert 'profiles' in tables
        assert 'work_entries' in tables
        assert 'settings' in tables
        assert 'custom_themes' in tables
        
        conn.close()
    
    def test_database_creates_default_profile(self, temp_db):
        """Test czy baza tworzy domyślny profil"""
        db, db_path = temp_db
        
        profiles = db.get_all_profiles()
        assert len(profiles) > 0
        assert profiles[0]['name'] == 'Default User'


class TestDatabaseProfiles:
    """Testy operacji na profilach"""
    
    def test_create_profile(self, temp_db):
        """Test tworzenia profilu"""
        db, db_path = temp_db
        
        profile_id = db.create_profile("Test User")
        assert isinstance(profile_id, int)
        assert profile_id > 0
        
        profile = db.get_profile(profile_id)
        assert profile is not None
        assert profile['name'] == "Test User"
    
    def test_duplicate_profile_raises_error(self, temp_db):
        """Test czy zduplikowana nazwa profilu podnosi błąd"""
        db, db_path = temp_db
        
        db.create_profile("Duplicate")
        
        with pytest.raises(ValueError):
            db.create_profile("Duplicate")
    
    def test_get_all_profiles(self, temp_db):
        """Test pobierania wszystkich profili"""
        db, db_path = temp_db
        
        db.create_profile("User 1")
        db.create_profile("User 2")
        
        profiles = db.get_all_profiles()
        assert len(profiles) >= 3  # Default + 2 nowe
    
    def test_delete_profile(self, temp_db):
        """Test usuwania profilu"""
        db, db_path = temp_db
        
        profile_id = db.create_profile("To Delete")
        result = db.delete_profile(profile_id)
        
        assert result is True
        assert db.get_profile(profile_id) is None


class TestDatabaseWorkEntries:
    """Testy operacji na wpisach pracy"""
    
    @pytest.fixture
    def profile_with_entries(self, temp_db):
        """Utwórz profil i dodaj wpisy"""
        db, db_path = temp_db
        profile_id = db.create_profile("Test Profile")
        return db, db_path, profile_id
    
    def test_insert_work_entry(self, profile_with_entries):
        """Test dodawania wpisu pracy"""
        db, db_path, profile_id = profile_with_entries
        
        entry = {
            'profile_id': profile_id,
            'date': '2025-01-15',
            'start_time': '09:00',
            'end_time': '17:00',
            'break_minutes': 30,
            'day_type': 'work_day',
            'notes': 'Test entry'
        }
        
        entry_id = db.insert_work_entry(entry)
        assert isinstance(entry_id, int)
        assert entry_id > 0
    
    def test_get_work_entry(self, profile_with_entries):
        """Test pobierania wpisu pracy"""
        db, db_path, profile_id = profile_with_entries
        
        entry = {
            'profile_id': profile_id,
            'date': '2025-01-15',
            'start_time': '09:00',
            'end_time': '17:00',
            'break_minutes': 30,
            'day_type': 'work_day',
            'notes': 'Test'
        }
        
        db.insert_work_entry(entry)
        
        retrieved = db.get_work_entry(profile_id, '2025-01-15')
        assert retrieved is not None
        assert retrieved['date'] == '2025-01-15'
        assert retrieved['start_time'] == '09:00'
    
    def test_get_work_entries_month(self, profile_with_entries):
        """Test pobierania wpisów z miesiąca"""
        db, db_path, profile_id = profile_with_entries
        
        # Dodaj kilka wpisów
        for day in range(1, 6):
            entry = {
                'profile_id': profile_id,
                'date': f'2025-01-{day:02d}',
                'start_time': '09:00',
                'end_time': '17:00',
                'break_minutes': 0,
                'day_type': 'work_day',
                'notes': ''
            }
            db.insert_work_entry(entry)
        
        entries = db.get_work_entries_month(profile_id, 2025, 1)
        assert len(entries) == 5
    
    def test_delete_work_entry(self, profile_with_entries):
        """Test usuwania wpisu"""
        db, db_path, profile_id = profile_with_entries
        
        entry = {
            'profile_id': profile_id,
            'date': '2025-01-15',
            'start_time': '09:00',
            'end_time': '17:00',
            'break_minutes': 0,
            'day_type': 'work_day',
            'notes': ''
        }
        
        db.insert_work_entry(entry)
        result = db.delete_work_entry(profile_id, '2025-01-15')
        
        assert result is True
        assert db.get_work_entry(profile_id, '2025-01-15') is None
    
    def test_upsert_work_entry(self, profile_with_entries):
        """Test aktualizacji wpisu (UPSERT)"""
        db, db_path, profile_id = profile_with_entries
        
        # Pierwszy wpis
        entry = {
            'profile_id': profile_id,
            'date': '2025-01-15',
            'start_time': '09:00',
            'end_time': '17:00',
            'break_minutes': 0,
            'day_type': 'work_day',
            'notes': 'Original'
        }
        
        db.insert_work_entry(entry)
        
        # Zaktualizuj
        entry['end_time'] = '18:00'
        entry['notes'] = 'Updated'
        db.insert_work_entry(entry)
        
        retrieved = db.get_work_entry(profile_id, '2025-01-15')
        assert retrieved['end_time'] == '18:00'
        assert retrieved['notes'] == 'Updated'


class TestDatabaseSettings:
    """Testy operacji na ustawieniach"""
    
    @pytest.fixture
    def profile_with_settings(self, temp_db):
        """Utwórz profil"""
        db, db_path = temp_db
        profile_id = db.create_profile("Settings Test")
        return db, db_path, profile_id
    
    def test_set_and_get_setting(self, profile_with_settings):
        """Test ustawiania i pobierania ustawienia"""
        db, db_path, profile_id = profile_with_settings
        
        db.set_setting(profile_id, "theme", "dark", "string")
        value = db.get_setting(profile_id, "theme")
        
        assert value == "dark"
    
    def test_update_setting(self, profile_with_settings):
        """Test aktualizacji ustawienia"""
        db, db_path, profile_id = profile_with_settings
        
        db.set_setting(profile_id, "theme", "light")
        db.set_setting(profile_id, "theme", "dark")
        
        value = db.get_setting(profile_id, "theme")
        assert value == "dark"


class TestDatabaseCustomThemes:
    """Testy operacji na niestandardowych motywach"""
    
    @pytest.fixture
    def profile_with_themes(self, temp_db):
        """Utwórz profil"""
        db, db_path = temp_db
        profile_id = db.create_profile("Themes Test")
        return db, db_path, profile_id
    
    def test_insert_custom_theme(self, profile_with_themes):
        """Test dodawania niestandardowego motywu"""
        db, db_path, profile_id = profile_with_themes
        
        theme_id = db.insert_custom_theme(
            profile_id=profile_id,
            theme_id=100,
            name="My Theme",
            config_json='{"primary": "#FF0000"}'
        )
        
        assert isinstance(theme_id, int)
        assert theme_id > 0
    
    def test_get_custom_themes(self, profile_with_themes):
        """Test pobierania niestandardowych motywów"""
        db, db_path, profile_id = profile_with_themes
        
        db.insert_custom_theme(profile_id, 100, "Theme 1", '{}')
        db.insert_custom_theme(profile_id, 101, "Theme 2", '{}')
        
        themes = db.get_custom_themes(profile_id)
        assert len(themes) == 2


class TestDatabaseCascadeDelete:
    """Testy usuwania kaskadowego"""
    
    def test_delete_profile_cascades_to_entries(self, temp_db):
        """Test czy usunięcie profilu usuwa jego wpisy"""
        db, db_path = temp_db
        
        profile_id = db.create_profile("To Delete")
        
        entry = {
            'profile_id': profile_id,
            'date': '2025-01-15',
            'start_time': '09:00',
            'end_time': '17:00',
            'break_minutes': 0,
            'day_type': 'work_day',
            'notes': ''
        }
        
        db.insert_work_entry(entry)
        
        # Sprawdź czy wpis istnieje
        retrieved = db.get_work_entry(profile_id, '2025-01-15')
        assert retrieved is not None
        
        # Usuń profil
        db.delete_profile(profile_id)
        
        # Sprawdź czy wpis również został usunięty
        retrieved = db.get_work_entry(profile_id, '2025-01-15')
        assert retrieved is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
