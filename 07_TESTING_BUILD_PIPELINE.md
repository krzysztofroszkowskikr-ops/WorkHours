# TESTING STRATEGY & BUILD PIPELINE
## WorkHours Purple v1.0

---

## 1. TESTING PYRAMID

```
                    ▲
                   /█\
                  / █ \        E2E (Acceptance Tests)
                 /  █  \       - Full app workflows
                /   █   \      - Android device
               /────█────\
              /█████████████\
             / █ █ █ █ █ █ █ \  Integration Tests
            /  █ █ █ █ █ █ █  \ - Database + Services
           /───█─█─█─█─█─█─█───\
          /████████████████████\
         / Unit Tests            \ - Pure logic
        /  - Validators           \ - Functions
       /   - Formatters           \ - APIs
      /    - CalcService          \
     /─────────────────────────────\
    
Pyramid Principle:
- Many unit tests (cheap, fast)
- Fewer integration tests (moderate)
- Few E2E tests (expensive, slow)
```

---

## 2. UNIT TESTS

### 2.1 Calculation Tests

```python
# tests/test_calc_service.py

import pytest
from src.services.calc_service import CalcService

class TestWorkTimeCalculation:
    """Test suite for CalcService.calculate_work_time()"""
    
    def test_basic_8_hour_day(self):
        """Test standard 8-hour workday"""
        result = CalcService.calculate_work_time(
            '08:00', '17:00', 60, 'work'
        )
        assert result['gross_minutes'] == 540  # 9 hours
        assert result['net_minutes'] == 480    # 8 hours (after 1h break)
        assert result['is_valid'] is True
        assert len(result['errors']) == 0
    
    def test_midnight_crossing(self):
        """Test work across midnight"""
        result = CalcService.calculate_work_time(
            '22:00', '06:00', 0, 'work'
        )
        assert result['gross_minutes'] == 480  # 8 hours
        assert result['net_minutes'] == 480
        assert result['is_valid'] is True
    
    def test_no_break(self):
        """Test full hours with no break"""
        result = CalcService.calculate_work_time(
            '09:00', '17:00', 0, 'work'
        )
        assert result['gross_minutes'] == 480
        assert result['net_minutes'] == 480
        assert result['is_valid'] is True
    
    def test_long_break(self):
        """Test with longer break"""
        result = CalcService.calculate_work_time(
            '07:00', '16:30', 120, 'work'  # 2 hour break
        )
        assert result['gross_minutes'] == 570  # 9.5 hours
        assert result['net_minutes'] == 450    # 7.5 hours
        assert result['is_valid'] is True
    
    def test_break_exceeds_time(self):
        """Test validation: break > gross time"""
        result = CalcService.calculate_work_time(
            '08:00', '17:00', 600, 'work'  # 10 hour break > 9 hour day
        )
        assert result['is_valid'] is False
        assert "exceeds" in result['errors'][0]
    
    def test_end_before_start(self):
        """Test validation: end < start"""
        result = CalcService.calculate_work_time(
            '17:00', '08:00', 60, 'work'
        )
        assert result['is_valid'] is True  # Assumes next day
        assert result['gross_minutes'] == 540  # Next day calculation
    
    def test_vacation_day_zero_hours(self):
        """Test vacation day returns 0 hours"""
        result = CalcService.calculate_work_time(
            '08:00', '17:00', 60, 'vacation'
        )
        assert result['gross_minutes'] == 0
        assert result['net_minutes'] == 0
        assert result['is_valid'] is True
        assert 'vacation' in result['reason']
    
    def test_invalid_time_format(self):
        """Test validation: bad time format"""
        result = CalcService.calculate_work_time(
            '8:00', '17:00', 60, 'work'  # Missing leading 0
        )
        assert result['is_valid'] is False
        assert any('format' in e for e in result['errors'])
    
    @pytest.mark.parametrize('day_type', ['work', 'vacation', 'sick', 'holiday', 'other'])
    def test_all_day_types(self, day_type):
        """Test all valid day types"""
        result = CalcService.calculate_work_time(
            '08:00', '17:00', 60, day_type
        )
        assert result['is_valid'] is True

class TestMonthSummary:
    """Test suite for CalcService.calculate_month_summary()"""
    
    def test_empty_month(self):
        """Test summary with no entries"""
        result = CalcService.calculate_month_summary([])
        assert result['total_net_minutes'] == 0
        assert result['working_days'] == 0
        assert result['completeness'] == 0
    
    def test_full_month_all_work(self):
        """Test full month of work days"""
        # Create 20 mock entries
        entries = self._create_mock_entries(20, 'work')
        result = CalcService.calculate_month_summary(entries)
        assert result['working_days'] == 20
        assert result['day_counts']['work'] == 20
        assert result['total_net_minutes'] > 0
    
    def test_mixed_day_types(self):
        """Test month with various day types"""
        entries = (
            self._create_mock_entries(20, 'work') +
            self._create_mock_entries(2, 'vacation') +
            self._create_mock_entries(1, 'sick') +
            self._create_mock_entries(1, 'holiday')
        )
        result = CalcService.calculate_month_summary(entries)
        assert result['day_counts']['work'] == 20
        assert result['day_counts']['vacation'] == 2
        assert result['day_counts']['sick'] == 1
        assert result['day_counts']['holiday'] == 1
    
    def test_completeness_calculation(self):
        """Test completeness percentage"""
        entries = self._create_mock_entries(20, 'work')
        # Simulate 20 logged out of 30 days
        result = CalcService.calculate_month_summary(entries)
        completeness = result['completeness']
        assert 0 <= completeness <= 100
    
    @staticmethod
    def _create_mock_entries(count, day_type):
        """Helper: create mock WorkEntry objects"""
        from src.models import WorkEntry
        return [
            WorkEntry(
                id=i,
                profile_id=1,
                date=f'2026-02-{i+1:02d}',
                start_time='08:00' if day_type == 'work' else None,
                end_time='17:00' if day_type == 'work' else None,
                break_minutes=60 if day_type == 'work' else 0,
                day_type=day_type,
            )
            for i in range(count)
        ]
```

### 2.2 Validation Tests

```python
# tests/test_validators.py

import pytest
from src.utils.validators import Validators

class TestDateValidation:
    """Test suite for date validation"""
    
    def test_valid_date_format(self):
        valid, msg = Validators.validate_date('2026-02-04')
        assert valid is True
        assert msg == ""
    
    def test_invalid_date_format(self):
        valid, msg = Validators.validate_date('2026/02/04')
        assert valid is False
        assert 'format' in msg
    
    def test_invalid_date_values(self):
        valid, msg = Validators.validate_date('2026-13-01')  # Month 13
        assert valid is False
    
    def test_future_date_rejected(self):
        """Test that future dates are rejected"""
        from datetime import datetime, timedelta
        future = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        valid, msg = Validators.validate_date(future)
        assert valid is False

class TestTimeValidation:
    """Test suite for time validation"""
    
    def test_valid_time(self):
        valid, msg = Validators.validate_time('08:30')
        assert valid is True
    
    def test_invalid_format(self):
        valid, msg = Validators.validate_time('8:30')  # Missing leading 0
        assert valid is False
    
    def test_invalid_hours(self):
        valid, msg = Validators.validate_time('25:00')
        assert valid is False
    
    def test_invalid_minutes(self):
        valid, msg = Validators.validate_time('12:60')
        assert valid is False

class TestWorkEntryValidation:
    """Test complete work entry validation"""
    
    def test_valid_work_entry(self):
        entry = {
            'date': '2026-02-04',
            'start_time': '08:00',
            'end_time': '17:00',
            'break_minutes': 60,
            'day_type': 'work',
            'notes': 'Regular day'
        }
        valid, errors = Validators.validate_work_entry(entry)
        assert valid is True
        assert len(errors) == 0
    
    def test_missing_required_fields(self):
        entry = {
            'date': '2026-02-04',
            'day_type': 'work',
            # Missing start_time, end_time
        }
        valid, errors = Validators.validate_work_entry(entry)
        assert valid is False
        assert len(errors) > 0
```

---

## 3. INTEGRATION TESTS

### 3.1 Database Integration Tests

```python
# tests/test_database.py

import pytest
import tempfile
import os
from src.db.database import Database
from src.db.migrations import MigrationRunner
from src.repository.work_entry_repository import WorkEntryRepository
from src.models import WorkEntry

@pytest.fixture
def db():
    """Create temporary test database"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'test.db')
        db = Database(db_path)
        db.initialize()
        yield db
        db.close()

class TestDatabaseIntegration:
    """Test database operations"""
    
    def test_database_initialization(self, db):
        """Test database creates schema"""
        # Check tables exist
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='profiles'
        """)
        assert cursor.fetchone() is not None
    
    def test_migrations_run(self, db):
        """Test migrations execute"""
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT name FROM _migrations
        """)
        migrations = cursor.fetchall()
        assert len(migrations) > 0
    
    def test_create_and_retrieve_profile(self, db):
        """Test profile CRUD"""
        # Create
        profile = db.create_profile("Test User")
        assert profile['name'] == "Test User"
        
        # Retrieve
        retrieved = db.get_profile(profile['id'])
        assert retrieved['name'] == "Test User"
    
    def test_work_entry_repository(self, db):
        """Test work entry operations"""
        repo = WorkEntryRepository(db)
        
        # Create profile first
        profile = db.create_profile("Worker")
        
        # Create entry
        entry = WorkEntry(
            profile_id=profile['id'],
            date='2026-02-04',
            start_time='08:00',
            end_time='17:00',
            break_minutes=60,
            day_type='work'
        )
        entry_id = repo.create(entry)
        assert entry_id is not None
        
        # Retrieve
        retrieved = repo.get_by_id(entry_id)
        assert retrieved.date == '2026-02-04'
        assert retrieved.start_time == '08:00'
        
        # Update
        entry.notes = "Updated"
        assert repo.update(entry) is True
        
        # Delete
        assert repo.delete(entry_id) is True
        assert repo.get_by_id(entry_id) is None

class TestDatabaseMultiProfile:
    """Test multi-profile isolation"""
    
    def test_profile_isolation(self, db):
        """Test that profiles are isolated"""
        # Create two profiles
        profile1 = db.create_profile("User 1")
        profile2 = db.create_profile("User 2")
        
        repo = WorkEntryRepository(db)
        
        # Add entry for profile 1
        entry1 = WorkEntry(
            profile_id=profile1['id'],
            date='2026-02-04',
            start_time='08:00',
            end_time='17:00',
            break_minutes=60,
            day_type='work'
        )
        repo.create(entry1)
        
        # Retrieve for profile 1
        entries_p1 = repo.get_month(profile1['id'], 2026, 2)
        assert len(entries_p1) == 1
        
        # Retrieve for profile 2
        entries_p2 = repo.get_month(profile2['id'], 2026, 2)
        assert len(entries_p2) == 0
```

---

## 4. E2E / ACCEPTANCE TESTS

### 4.1 User Journey Tests

```python
# tests/test_user_journeys.py

@pytest.mark.e2e
class TestUserJourneys:
    """Test complete user workflows"""
    
    def test_create_and_log_workday(self):
        """User creates profile and logs a workday"""
        # 1. Open app
        # 2. Create profile "Anna"
        # 3. Navigate to dashboard
        # 4. Click "Add today"
        # 5. Fill: 08:00 - 17:00, break 60min
        # 6. Save
        # 7. Verify entry appears
        pass
    
    def test_generate_monthly_report(self):
        """User generates monthly PDF report"""
        # 1. Create profile & log entries
        # 2. Navigate to Report
        # 3. Click "Generate PDF"
        # 4. Verify PDF is saved to /Downloads
        # 5. Verify PDF contains correct data
        pass
    
    def test_theme_switching(self):
        """User switches between themes"""
        # 1. Open Settings
        # 2. Select theme #5 (Light)
        # 3. Verify smooth animation
        # 4. Verify colors changed
        # 5. Close app & reopen
        # 6. Verify theme persisted
        pass
```

---

## 5. TESTING CONFIGURATION

### 5.1 pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    -p no:warnings

markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests (skip with -m "not slow")
```

### 5.2 conftest.py

```python
# tests/conftest.py

import pytest
from src.app_context import app_context

@pytest.fixture(scope="session", autouse=True)
def setup_app_context():
    """Setup app context for all tests"""
    # Initialize with test database
    import tempfile
    tmpdir = tempfile.mkdtemp()
    app_context.initialize(f'{tmpdir}/test.db')
    yield
    app_context.db_connection.close()

@pytest.fixture
def mock_profile():
    """Create mock profile"""
    from src.models import Profile
    return Profile(id=1, name='Test User')

@pytest.fixture
def mock_entry():
    """Create mock work entry"""
    from src.models import WorkEntry
    return WorkEntry(
        id=1,
        profile_id=1,
        date='2026-02-04',
        start_time='08:00',
        end_time='17:00',
        break_minutes=60,
        day_type='work'
    )
```

---

## 6. RUN TESTS

```bash
# Run all tests
pytest

# Run only unit tests
pytest -m unit

# Run specific test
pytest tests/test_calc_service.py::TestWorkTimeCalculation::test_basic_8_hour_day

# Run with coverage
pytest --cov=src --cov-report=html

# Run and show print statements
pytest -s

# Run and stop on first failure
pytest -x
```

---

## 7. BUILD PIPELINE

### 7.1 Buildozer Configuration (buildozer.spec)

```ini
[app]
# Basic metadata
title = WorkHours Purple
package.name = workhours
package.domain = org.workhours
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Version and icons
version = 1.0.0
icon.filename = assets/icons/app_icon.png
presplash.filename = assets/icons/presplash.png

# Permissions
permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,POST_NOTIFICATIONS,SCHEDULE_EXACT_ALARM

# Requirements
requirements = python3,kivy,kivymd,reportlab,plyer,pyjnius,pillow,python-dateutil

# Android configuration
android.api = 35
android.minapi = 26
android.ndk = 25b
android.accept_sdk_license = True

# Gradle build options
android.gradle_dependencies = 
android.ant_targets = 

[buildozer]
log_level = 2
warn_on_root = 1
```

### 7.2 Build Commands

```bash
# Install buildozer (one-time)
pip install buildozer

# Build debug APK
buildozer android debug

# Build release APK (requires keystore)
buildozer android release

# Deploy to device
buildozer android debug deploy run

# Clean build
buildozer android clean
buildozer android clean_build_dir

# Check setup
buildozer android dumpenv
```

### 7.3 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/build.yml
name: Build APK

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build-apk:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '11'
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install buildozer
        run: pip install buildozer cython
      
      - name: Build APK
        run: buildozer android debug
      
      - name: Upload APK artifact
        uses: actions/upload-artifact@v3
        with:
          name: workhours-debug
          path: bin/*.apk
```

---

## 8. TESTING SUMMARY

| Type | Count | Time | Coverage |
|------|-------|------|----------|
| **Unit Tests** | 40+ | < 5s | 85%+ |
| **Integration Tests** | 15+ | < 10s | 60%+ |
| **E2E Tests** | 5+ | 1-2min | Key flows |
| **Total** | 60+ | 2-3min | 75%+ |

**Target:** ✅ 75%+ code coverage before release

---

**NEXT:** Developer Setup Guide + Final Summary
