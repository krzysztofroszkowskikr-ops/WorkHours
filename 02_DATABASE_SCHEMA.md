# DATABASE SCHEMA & MIGRATIONS
## WorkHours Purple v1.0

---

## 1. SCHEMA OVERVIEW

```
┌──────────────────────┐
│     profiles         │
├──────────────────────┤
│ id (PK)              │
│ name                 │
│ created_at           │
│ updated_at           │
└──────────────────────┘
          │
          ├─→ ┌──────────────────────┐
          │   │   work_entries       │
          │   ├──────────────────────┤
          │   │ id (PK)              │
          │   │ profile_id (FK)      │
          │   │ date (UNIQUE+idx)    │
          │   │ start_time           │
          │   │ end_time             │
          │   │ break_minutes        │
          │   │ day_type (idx)       │
          │   │ notes                │
          │   │ created_at           │
          │   │ updated_at           │
          │   └──────────────────────┘
          │
          ├─→ ┌──────────────────────┐
          │   │    settings          │
          │   ├──────────────────────┤
          │   │ id (PK)              │
          │   │ profile_id (FK)      │
          │   │ key (UNIQUE+idx)     │
          │   │ value                │
          │   │ type                 │
          │   └──────────────────────┘
          │
          └─→ ┌──────────────────────┐
              │  custom_themes       │
              ├──────────────────────┤
              │ id (PK)              │
              │ profile_id (FK)      │
              │ theme_id (UNIQUE)    │
              │ name                 │
              │ config_json          │
              │ created_at           │
              └──────────────────────┘
```

---

## 2. DDL - Create Table Statements

### 2.1 profiles

```sql
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    CHECK (length(name) >= 1 AND length(name) <= 100)
);

CREATE INDEX idx_profiles_name ON profiles(name);
```

**Logika:**
- `id`: auto-increment PK
- `name`: unikalna nazwa profilu (Anna, Jan, itp.)
- `created_at, updated_at`: auditowe timestampy
- CHECK: nazwa 1-100 znaków

---

### 2.2 work_entries

```sql
CREATE TABLE IF NOT EXISTS work_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    start_time TEXT,
    end_time TEXT,
    break_minutes INTEGER DEFAULT 0,
    day_type TEXT NOT NULL DEFAULT 'work',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    UNIQUE(profile_id, date),
    CHECK (day_type IN ('work', 'vacation', 'sick', 'holiday', 'other')),
    CHECK (break_minutes >= 0),
    CHECK (date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
);

CREATE INDEX idx_work_entries_profile_date ON work_entries(profile_id, date);
CREATE INDEX idx_work_entries_profile_month ON work_entries(profile_id, substr(date, 1, 7));
CREATE INDEX idx_work_entries_day_type ON work_entries(day_type);
```

**Logika:**
- `profile_id`: FK do profiles - każdy wpis przypisany do profilu
- `date`: YYYY-MM-DD format (UNIQUE per profile)
- `start_time, end_time`: HH:MM (nullable dla non-work dni)
- `break_minutes`: dominnie w minutach
- `day_type`: enum (work/vacation/sick/holiday/other)
- `notes`: opcjonalna notatka
- UNIQUE constraint: jeden wpis na dzień per profil
- Indeksy:
  - `(profile_id, date)`: szybkie zapytania dzienne
  - `(profile_id, substr(date, 1, 7))`: szybkie zapytania miesiączne
  - `day_type`: filtrowanie po typie

---

### 2.3 settings

```sql
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT DEFAULT 'string',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    UNIQUE(profile_id, key),
    CHECK (type IN ('string', 'integer', 'boolean', 'json'))
);

CREATE INDEX idx_settings_profile_key ON settings(profile_id, key);
```

**Logika:**
- Key-value store per profil
- `type`: hint do deserializacji (string/int/bool/json)
- Wspólne ustawienia (globalne) mogą mieć `profile_id = NULL`

---

### 2.4 custom_themes

```sql
CREATE TABLE IF NOT EXISTS custom_themes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    theme_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    config_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    UNIQUE(profile_id, theme_id),
    CHECK (theme_id >= 100)  -- Custom themes: 100+, Hardcoded: 1-10
);

CREATE INDEX idx_custom_themes_profile ON custom_themes(profile_id);
```

**Logika:**
- Przechowuje dynamicznie generowane motywy (Opcja B)
- `theme_id >= 100`: rozróżnienie od hardcoded (1-10)
- `config_json`: pełna paleta kolorów w JSON

**Przykład config_json:**
```json
{
  "name": "Custom Purple Hue 250",
  "background": "#1a0a3d",
  "surface": "#2d1b69",
  "surface2": "#3e2d7d",
  "text": "#ffffff",
  "muted": "#b0b0b0",
  "primary": "#9c27b0",
  "accent": "#ff00ff",
  "success": "#4caf50",
  "warning": "#ff9800",
  "error": "#f44336",
  "radius_card": "22dp",
  "radius_button": "18dp"
}
```

---

### 2.5 Holiday Master (Opcjonalnie - v1.2+)

```sql
CREATE TABLE IF NOT EXISTS holidays (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    is_national BOOLEAN DEFAULT 0,
    
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    CHECK (date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
);

CREATE INDEX idx_holidays_date ON holidays(date);
```

---

## 3. MIGRATION SYSTEM

### 3.1 Migration Runner

```python
# src/db/migrations.py
import sqlite3
from datetime import datetime

class MigrationRunner:
    """
    Zarządza migracjami bazy danych.
    Format: YYYYMMDD_HHmmss_description.sql
    """
    
    MIGRATIONS_DIR = 'src/db/migrations'
    MIGRATIONS_TABLE = '_migrations'
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.conn = db_connection.conn
    
    def init_migrations_table(self):
        """Stwórz tabelę śledzi migracji"""
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.MIGRATIONS_TABLE} (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                executed_at TEXT NOT NULL,
                duration_ms INTEGER
            )
        """)
        self.conn.commit()
    
    def get_executed_migrations(self) -> set:
        """Pobierz listę już wykonanych migracji"""
        cursor = self.conn.execute(
            f"SELECT name FROM {self.MIGRATIONS_TABLE}"
        )
        return {row[0] for row in cursor.fetchall()}
    
    def run_pending_migrations(self) -> dict:
        """Wykonaj wszystkie pending migracje"""
        import os
        
        self.init_migrations_table()
        executed = self.get_executed_migrations()
        
        migration_files = sorted(os.listdir(self.MIGRATIONS_DIR))
        results = {'executed': [], 'failed': []}
        
        for filename in migration_files:
            if not filename.endswith('.sql'):
                continue
            
            if filename in executed:
                print(f"✓ Migration already executed: {filename}")
                continue
            
            migration_path = os.path.join(self.MIGRATIONS_DIR, filename)
            
            try:
                with open(migration_path, 'r') as f:
                    sql_script = f.read()
                
                start_time = datetime.now()
                
                # Wykonaj migration
                for statement in sql_script.split(';'):
                    if statement.strip():
                        self.conn.execute(statement)
                
                duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
                
                # Zaloguj migration
                self.conn.execute(f"""
                    INSERT INTO {self.MIGRATIONS_TABLE} (name, executed_at, duration_ms)
                    VALUES (?, datetime('now'), ?)
                """, (filename, duration_ms))
                
                self.conn.commit()
                results['executed'].append(f"{filename} (+{duration_ms}ms)")
                print(f"✓ Migration executed: {filename}")
                
            except Exception as e:
                self.conn.rollback()
                results['failed'].append(f"{filename}: {str(e)}")
                print(f"✗ Migration failed: {filename}")
                print(f"  Error: {str(e)}")
        
        return results
```

---

### 3.2 Migration Files

#### 3.2.1 `20260204_000000_initial_schema.sql`

```sql
-- Initial schema: profiles, work_entries, settings

CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    CHECK (length(name) >= 1 AND length(name) <= 100)
);
CREATE INDEX idx_profiles_name ON profiles(name);

CREATE TABLE IF NOT EXISTS work_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    start_time TEXT,
    end_time TEXT,
    break_minutes INTEGER DEFAULT 0,
    day_type TEXT NOT NULL DEFAULT 'work',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    UNIQUE(profile_id, date),
    CHECK (day_type IN ('work', 'vacation', 'sick', 'holiday', 'other')),
    CHECK (break_minutes >= 0),
    CHECK (date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
);
CREATE INDEX idx_work_entries_profile_date ON work_entries(profile_id, date);
CREATE INDEX idx_work_entries_profile_month ON work_entries(profile_id, substr(date, 1, 7));
CREATE INDEX idx_work_entries_day_type ON work_entries(day_type);

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT DEFAULT 'string',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    UNIQUE(profile_id, key),
    CHECK (type IN ('string', 'integer', 'boolean', 'json'))
);
CREATE INDEX idx_settings_profile_key ON settings(profile_id, key);
```

#### 3.2.2 `20260205_000000_add_custom_themes.sql`

```sql
-- Add custom_themes table (Opcja B - dynamiczne generowanie)

CREATE TABLE IF NOT EXISTS custom_themes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    theme_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    config_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    UNIQUE(profile_id, theme_id),
    CHECK (theme_id >= 100)
);
CREATE INDEX idx_custom_themes_profile ON custom_themes(profile_id);
```

#### 3.2.3 `20260206_000000_default_profile_and_settings.sql`

```sql
-- Insert default profile and initial settings

INSERT INTO profiles (name) 
SELECT 'Default User' 
WHERE NOT EXISTS (SELECT 1 FROM profiles WHERE name = 'Default User');

INSERT OR IGNORE INTO settings (profile_id, key, value, type)
SELECT p.id, 'theme_id', '1', 'integer'
FROM profiles p
WHERE p.name = 'Default User';

INSERT OR IGNORE INTO settings (profile_id, key, value, type)
SELECT p.id, 'default_start', '08:00', 'string'
FROM profiles p;

INSERT OR IGNORE INTO settings (profile_id, key, value, type)
SELECT p.id, 'default_end', '17:00', 'string'
FROM profiles p;

INSERT OR IGNORE INTO settings (profile_id, key, value, type)
SELECT p.id, 'default_break', '60', 'integer'
FROM profiles p;

INSERT OR IGNORE INTO settings (profile_id, key, value, type)
SELECT p.id, 'reminder_enabled', 'true', 'boolean'
FROM profiles p;

INSERT OR IGNORE INTO settings (profile_id, key, value, type)
SELECT p.id, 'reminder_time', '19:00', 'string'
FROM profiles p;

INSERT OR IGNORE INTO settings (profile_id, key, value, type)
SELECT p.id, 'employee_name', 'Pracownik', 'string'
FROM profiles p;

INSERT OR IGNORE INTO settings (profile_id, key, value, type)
SELECT p.id, 'employer_name', 'Pracodawca', 'string'
FROM profiles p;
```

---

## 4. DATABASE WRAPPER & SETTINGS API

```python
# src/db/database.py
import sqlite3
from pathlib import Path
from .migrations import MigrationRunner

class Database:
    """Wrapper wokół SQLite"""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            isolation_level=None  # autocommit mode
        )
        self.conn.row_factory = sqlite3.Row
        
        # Enable foreign keys
        self.conn.execute("PRAGMA foreign_keys = ON")
    
    def initialize(self):
        """Inicjalizuj bazę (migracje + seed data)"""
        runner = MigrationRunner(self)
        results = runner.run_pending_migrations()
        print(f"Migrations: {len(results['executed'])} executed, {len(results['failed'])} failed")
        return results
    
    # ===== SETTINGS HELPERS =====
    
    def get_setting(self, key: str, profile_id: int = None, default=None):
        """Pobierz ustawienie"""
        cursor = self.conn.execute("""
            SELECT value, type FROM settings
            WHERE key = ? AND (profile_id = ? OR profile_id IS NULL)
            LIMIT 1
        """, (key, profile_id))
        row = cursor.fetchone()
        
        if not row:
            return default
        
        value, value_type = row
        return self._deserialize_setting(value, value_type)
    
    def set_setting(self, key: str, value, value_type: str = 'string', profile_id: int = None):
        """Zapisz/zaktualizuj ustawienie"""
        serialized = self._serialize_setting(value, value_type)
        self.conn.execute("""
            INSERT OR REPLACE INTO settings (profile_id, key, value, type)
            VALUES (?, ?, ?, ?)
        """, (profile_id, key, serialized, value_type))
    
    def _serialize_setting(self, value, value_type: str) -> str:
        """Serializuj wartość"""
        if value_type == 'boolean':
            return 'true' if value else 'false'
        elif value_type == 'integer':
            return str(int(value))
        elif value_type == 'json':
            import json
            return json.dumps(value)
        else:  # string
            return str(value)
    
    def _deserialize_setting(self, value: str, value_type: str):
        """Deserializuj wartość"""
        if value_type == 'boolean':
            return value.lower() in ('true', '1', 'yes')
        elif value_type == 'integer':
            return int(value)
        elif value_type == 'json':
            import json
            return json.loads(value)
        else:  # string
            return value
    
    # ===== PROFILE HELPERS =====
    
    def get_profile(self, profile_id: int) -> dict:
        """Pobierz profil"""
        cursor = self.conn.execute(
            "SELECT * FROM profiles WHERE id = ?",
            (profile_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_profiles(self) -> list:
        """Pobierz wszystkie profile"""
        cursor = self.conn.execute(
            "SELECT * FROM profiles ORDER BY name"
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def create_profile(self, name: str) -> dict:
        """Stwórz nowy profil"""
        cursor = self.conn.execute(
            "INSERT INTO profiles (name) VALUES (?)",
            (name,)
        )
        return self.get_profile(cursor.lastrowid)
    
    def update_profile(self, profile_id: int, name: str) -> bool:
        """Aktualizuj profil"""
        cursor = self.conn.execute(
            "UPDATE profiles SET name = ?, updated_at = datetime('now') WHERE id = ?",
            (name, profile_id)
        )
        return cursor.rowcount > 0
    
    def delete_profile(self, profile_id: int) -> bool:
        """Usuń profil (cascade delete)"""
        cursor = self.conn.execute(
            "DELETE FROM profiles WHERE id = ?",
            (profile_id,)
        )
        return cursor.rowcount > 0
    
    def close(self):
        """Zamknij połączenie"""
        self.conn.close()
```

---

## 5. BACKUP & EXPORT

### 5.1 Auto-Backup Strategy

```python
# src/db/backup.py
import shutil
from pathlib import Path
from datetime import datetime

class BackupManager:
    """Zarządza backupami bazy"""
    
    def __init__(self, db_path: str, backup_dir: str = None):
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir or self.db_path.parent / 'backups')
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, name: str = None) -> Path:
        """Stwórz backup"""
        if name is None:
            name = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        backup_path = self.backup_dir / f"workhours_{name}.db"
        shutil.copy2(self.db_path, backup_path)
        return backup_path
    
    def auto_backup_on_startup(self):
        """Auto-backup przy starcie (jeśli ostatni > 7 dni)"""
        import os
        
        if not self.backup_dir.exists():
            self.create_backup('startup')
            return
        
        backups = sorted(self.backup_dir.glob('workhours_*.db'))
        if not backups:
            self.create_backup('startup')
            return
        
        last_backup = backups[-1]
        age_seconds = (datetime.now() - datetime.fromtimestamp(
            os.path.getmtime(last_backup)
        )).total_seconds()
        
        if age_seconds > 7 * 24 * 60 * 60:  # 7 dni
            self.create_backup('startup')
```

---

## 6. PODSUMOWANIE BAZY DANYCH

| Tabela | Wiersze | Cel |
|--------|---------|-----|
| **profiles** | ~10 max | Przechowuje profile użytkowników |
| **work_entries** | ~1000 (30*12 profili) | Główne dane - wpisy dzienne |
| **settings** | ~100 (10*profili) | Konfiguracja per profil |
| **custom_themes** | ~50 (5*profili) | Dynamicznie generowane motywy |
| **_migrations** | ~10 | Tracking migracji |

**Indeksy:** 7 strategicznych indeksów dla szybkich zapytań

**Constraints:**
- Foreign Keys: ON DELETE CASCADE
- UNIQUE: profile_id+date dla work_entries
- CHECK: validacja day_type, dates, break_minutes

**Skalowanie:**
- Baza lokalna = wystarczająca dla 1 użytkownika
- Dla team mode (v2.0) → opcjonalny backend Py/Node

---

**NEXT:** Project Structure + Module Organization
