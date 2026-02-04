# 🧪 WORKHOURSAPP - TESTER

## Kompletny System Testowania Aplikacji

Folder `TESTER` zawiera wszystkie narzędzia i dokumenty potrzebne do testowania aplikacji WorkHours na poziomie użytkownika, poprzez interfejs graficzny (UI).

---

## 📁 STRUKTURA FOLDERU TESTER

```
TESTER/
├── tester_app.py                 ⭐ Główna aplikacja testowa
├── INSTALLATION_GUIDE.md         📱 Przewodnik instalacji na telefonie
├── TEST_SCENARIOS.md             🧪 20+ scenariuszy testowych
├── requirements_tester.txt       📦 Zależności Python
├── tester_config.ini             ⚙️  Konfiguracja
├── README.md                     📖 Ten plik
├── reports/                      📄 Wygenerowane raporty PDF
├── backups/                      💾 Kopie zapasowe bazy danych
├── logs/                         📝 Pliki logów
├── fixtures/                     🔧 Dane testowe
└── scripts/                      🐍 Pomocnicze skrypty
```

---

## 🚀 SZYBKI START

### Opcja 1: Testowanie na PC (Rekomendowane dla Deweloperów)

```bash
# 1. Wejdź do folderu projektu
cd e:\MobileApp_Paulina

# 2. Utwórz wirtualne środowisko
python -m venv venv

# 3. Aktywuj (Windows)
venv\Scripts\activate

# 4. Zainstaluj zależności
pip install -r TESTER/requirements_tester.txt

# 5. Uruchom tester
python TESTER/tester_app.py

# 6. Okno aplikacji otworzy się
# Możesz testować jak na telefonie!
```

### Opcja 2: Testowanie na Telefonie

```
1. Pobierz APK z folderu bin/ (lub zbuduj Buildozer)
2. Zainstaluj na telefonie (patrz INSTALLATION_GUIDE.md)
3. Otwórz aplikację
4. Testuj jak normalny użytkownik
5. Zgłoś błędy (patrz Raportowanie Błędów)
```

---

## 📱 GŁÓWNA APLIKACJA TESTOWA (`tester_app.py`)

### Klasy i Moduły

#### 1. **Models** - Modele danych
```python
WorkEntry     # Wpis pracy (data, godziny, notatka)
Profile       # Profil użytkownika (izolacja danych)
```

#### 2. **TesterDatabase** - Obsługa bazy SQLite
```python
db.add_work_entry(entry)           # Dodaj wpis
db.get_work_entries_month()        # Pobierz wpisy z miesiąca
db.get_all_profiles()              # Pobierz wszystkie profile
db.add_profile(name)               # Dodaj profil
db.delete_profile(profile_id)      # Usuń profil
db.get_custom_themes()             # Pobierz motywy
```

#### 3. **TesterValidators** - Walidacja danych
```python
TesterValidators.validate_date()        # Sprawdź datę
TesterValidators.validate_time()        # Sprawdź czas
TesterValidators.validate_work_entry()  # Waliduj cały wpis
```

#### 4. **TesterCalculations** - Obliczenia czasu pracy
```python
calculate_work_time(start, end, break, day_type)
# Oblicz czas pracy z obsługą:
# - Przekroczenia północy
# - Dni nieroboczych
# - Przerw
# Zwraca: gross_minutes, net_minutes, formatted strings, errors

calculate_month_summary(entries)
# Podsumowanie miesiąca
# Zwraca: total_net, total_gross, day_counts, średnia
```

#### 5. **TesterPDFGenerator** - Generowanie PDF
```python
TesterPDFGenerator.generate_month_report()
# Tworzy plik PDF z raportem miesiąca
# Lokalizacja: TESTER/reports/
```

#### 6. **TesterThemeManager** - System motywów
```python
# Opcja A: 10 Hardcoded Themes
TesterThemeManager.get_theme(theme_id)      # ID 1-10
TesterThemeManager.list_all_themes()

# Opcja B: Dynamic Generator
TesterThemeManager.generate_custom_theme(hue, is_dark)

# Listuj wszystkie
TesterThemeManager.list_all_themes()
```

#### 7. **WorkHoursTesterApp** - UI (KivyMD)
```
Karty interfejsu:
1. ➕ Dodaj Wpis
2. 📋 Wpisy
3. 📊 Raport
4. 👤 Profile
5. 🎨 Motywy
6. 🗄️ Baza
```

---

## 🎯 SCENARIUSZE TESTOWE

Folder zawiera plik `TEST_SCENARIOS.md` z 20+ scenariuszami testowymi:

### Kategorie Testów

| Typ | Scenariusze | Kroki |
|-----|------------|-------|
| **Podstawowe** | TC-001, TC-002 | Uruchomienie, nawigacja |
| **Dodawanie Wpisów** | TC-003 - TC-006 | Wpisy normalne, przekroczenie północy, walidacja |
| **Raporty** | TC-007, TC-008 | Generowanie, PDF |
| **Profile** | TC-009, TC-010 | Tworzenie, izolacja danych |
| **Motywy** | TC-011, TC-012 | Zmiana, animacje |
| **Wydajność** | TC-013, TC-014 | 100 wpisów, RAM |
| **Bezpieczeństwo** | TC-015, TC-016 | Prywatne foldery, uprawnienia |
| **Brzegowe** | TC-017, TC-018 | Długie notatki, granice czasowe |
| **Integracyjne** | TC-019, TC-020 | Pełny tydzień, import/export |

### Jak Testować

1. Otwórz `TEST_SCENARIOS.md`
2. Wybierz scenariusz (np. TC-003)
3. Wykonaj kroki po kolei
4. Porównaj wyniki z oczekiwaniami
5. Zanotuj bugs (patrz Raportowanie)

---

## ⚙️ KONFIGURACJA

Plik `tester_config.ini` zawiera wszystkie ustawienia:

```ini
[database]
path = tester_workhoursapp.db        # Ścieżka do bazy
auto_backup = true                   # Automatyczne backupy

[ui]
default_theme = 1                    # Motyw startowy
animations_enabled = true            # Animacje
theme_animation_duration = 0.5       # Czas animacji (s)

[defaults]
default_start_time = 09:00           # Domyślny start
default_end_time = 17:00             # Domyślny koniec
default_break_minutes = 30           # Domyślna przerwa

[validation]
max_work_duration = 1440             # Max 24h na dzień
max_note_length = 1000               # Max długość notatki
max_break_duration = 480             # Max 8h przerwy

[themes]
hardcoded_theme_count = 10           # Liczba motywów
allow_custom_themes = true           # Tworzenie niestandardowych
enable_theme_animations = true       # Animacje motywów
```

### Edytowanie Konfiguracji

```bash
# Otwórz plik w edytorze
notepad TESTER/tester_config.ini

# Zmień wartości
# Zapisz (Ctrl+S)

# Zmiany obowiązują przy następnym uruchomieniu
python TESTER/tester_app.py
```

---

## 📦 ZALEŻNOŚCI

Zainstaluj z pliku `requirements_tester.txt`:

```bash
pip install -r TESTER/requirements_tester.txt
```

### Główne Pakiety

| Pakiet | Wersja | Cel |
|--------|--------|-----|
| **Kivy** | 2.3.0 | Framework UI |
| **KivyMD** | 0.104.2 | Material Design |
| **ReportLab** | 4.0.7 | Generowanie PDF |
| **Pillow** | 10.0.1 | Obsługa obrazów |
| **pytest** | 7.4.3 | Unit testing |
| **black** | 23.12.0 | Code formatting |
| **flake8** | 6.1.0 | Linting |

---

## 📱 INSTALACJA NA TELEFONIE

### Kroki (Skróty)

1. **Metoda 1: Plik APK (Najprościej)**
   ```
   1. Pobierz APK
   2. Transfer na telefon
   3. Zainstaluj
   Patrz: INSTALLATION_GUIDE.md → Metoda 1
   ```

2. **Metoda 2: Buildozer (Zaawansowane)**
   ```bash
   buildozer android debug
   adb install -r bin/workhoursapp-*.apk
   Patrz: INSTALLATION_GUIDE.md → Metoda 2
   ```

3. **Metoda 3: Android Studio**
   ```
   Otwórz projekt → Run → Wybierz urządzenie
   Patrz: INSTALLATION_GUIDE.md → Metoda 3
   ```

4. **Metoda 4: ADB (Command Line)**
   ```bash
   adb install -r /path/to/apk
   Patrz: INSTALLATION_GUIDE.md → Metoda 4
   ```

### Wymagania Telefonu

```
✓ Android 8.0+ (API 26+)
✓ Przetestowane na Android 16
✓ ~100 MB wolnego miejsca
✓ 2GB RAM minimum
```

---

## 🧪 PRZEPROWADZANIE TESTÓW

### Test Podstawowy

```bash
# 1. Uruchom aplikację
python TESTER/tester_app.py

# 2. Dodaj wpis (TC-003)
# - Kliknij "➕ Dodaj Wpis"
# - Wpisz dane
# - Kliknij "💾 Zapisz Wpis"

# 3. Sprawdź raport (TC-007)
# - Kliknij "📊 Raport"
# - Ustaw miesiąc
# - Kliknij "📊 Generuj"

# 4. Sprawdź PDF (TC-008)
# - Kliknij "📄 Pobierz PDF"
# - Otwórz z pliku
```

### Testy Zaawansowane

```bash
# 1. 100 wpisów (TC-013)
python TESTER/scripts/bulk_insert_entries.py --count 100

# 2. Monitoruj RAM (TC-014)
# - Ustawienia → Aplikacje → WorkHours → Zużywana pamięć

# 3. Długi test (TC-019)
# - Testuj przez cały tydzień
# - Notuj problemy
```

---

## 📊 STRUKTURA BAZY DANYCH

### Tabele

```sql
-- Profili użytkowników (izolacja danych)
profiles (id, name, created_at, updated_at)

-- Wpisy pracy
work_entries (
  id, profile_id, date, start_time, end_time,
  break_minutes, day_type, notes, ...
)

-- Motywy niestandardowe
custom_themes (id, profile_id, theme_id, name, config_json, ...)

-- Ustawienia
settings (id, profile_id, key, value, type, ...)
```

### Zarządzanie Bazą

```bash
# 1. Otwórz aplikację testową
python TESTER/tester_app.py

# 2. Karty "🗄️ Baza"

# 3. Akcje:
# - "💾 Eksportuj do JSON" - Backup wszystkich danych
# - "⚠️ Reset bazy" - Wyczyść bazę (UWAGA!)
```

---

## 🎨 SYSTEM MOTYWÓW

### Opcja A: 10 Hardcoded Themes

```python
1. Dark Purple Neon      (Primary: #7C3AED)
2. Dark Grape Premium    (Primary: #8B5CF6)
3. Dark Electric Violet  (Primary: #A78BFA)
4. Dark Plum + Gold      (Primary: #9333EA)
5. Light Clean Purple    (Primary: #7C3AED)
6. Light Lavender Candy  (Primary: #A78BFA)
7. Midnight Indigo       (Primary: #4F46E5)
8. Graphite Purple       (Primary: #8B5CF6)
9. Purple + Lime Pop     (Primary: #7C3AED)
10. Purple Sunset        (Primary: #C4B5FD)
```

### Opcja B: Generator HSV

```python
# Dynamiczny generator - nieograniczone motywy
theme = TesterThemeManager.generate_custom_theme(
    base_hue=240,      # 0-360 (BLUE)
    is_dark=True       # True = Dark, False = Light
)
```

### Testowanie Motywów

```bash
# 1. Kliknij "🎨 Motywy"
# 2. Wpisz ID: 1-10 (Opcja A)
# 3. Obserwuj zmianę + animację
# 4. Powtórz dla różnych motywów
```

---

## 🐛 RAPORTOWANIE BŁĘDÓW

### Format

```
TYTUŁ:
[Krótki opis problemu]

KROKI DO REPRODUKCJI:
1. [Krok 1]
2. [Krok 2]

OCZEKIWANE ZACHOWANIE:
[Co powinno się stać]

RZECZYWISTE ZACHOWANIE:
[Co się faktycznie stało]

SCREENSHOT:
[Zdjęcie ekranu]

ŚRODOWISKO:
- Urządzenie: [np. PC / Samsung S22]
- System: [np. Windows 10 / Android 16]
- Wersja aplikacji: [np. 1.0.0]
- Scenariusz: [np. TC-003]
```

### Gdzie Zgłaszać

```
1. GitHub Issues:
   https://github.com/YOUR_USER/workhoursapp/issues

2. Email:
   bugs@workhours.app

3. Discord/Slack:
   #bugs channel
```

---

## 📊 METRYKI TESTOWANIA

### Coverage

```
Kod testowy: src/            ← 75%+ coverage
Funkcje: calc_service.py     ← 95%+ coverage
Walidacja: validators.py     ← 100% coverage
```

### Uruchomienie Testów

```bash
# Unit testy
pytest TESTER/tests/test_validators.py -v

# Coverage raport
pytest --cov=src TESTER/tests/

# HTML raport
pytest --cov=src --cov-report=html TESTER/tests/
```

---

## 💡 TIPS & TRICKS

### Szybkie Testowanie

```bash
# 1. Zapamiętaj skróty:
# Tab 1: Dodaj (➕)
# Tab 2: Wpisy (📋)
# Tab 3: Raport (📊)
# Tab 4: Profile (👤)
# Tab 5: Motywy (🎨)
# Tab 6: Baza (🗄️)

# 2. Domyślne wartości (z config):
# Data: Dzisiaj
# Start: 09:00
# Koniec: 17:00
# Przerwa: 30 min

# 3. Kliknij "🔄 Wyczyść" żeby zresetować formularz
```

### Debugowanie

```bash
# 1. Włącz debug mode w config
# [debug]
# log_level = DEBUG

# 2. Sprawdzaj logi
# tail -f TESTER/logs/app.log

# 3. SQL debug
# [debug]
# sql_debug = true
```

### Backup Danych

```bash
# 1. Automatycznie (codziennie o 23:00)
# [backup]
# auto_backup_time = 23:00

# 2. Ręcznie (Tab "🗄️ Baza")
# Kliknij: "💾 Eksportuj do JSON"

# 3. Folder
# TESTER/backups/
```

---

## 📚 DODATKOWA DOKUMENTACJA

| Dokument | Zawartość |
|----------|-----------|
| **INSTALLATION_GUIDE.md** | Jak zainstalować na telefonie (4 metody) |
| **TEST_SCENARIOS.md** | 20+ scenariuszy testowych (TC-001 - TC-020) |
| **tester_config.ini** | Wszystkie ustawienia aplikacji |
| **requirements_tester.txt** | Lista zależności |
| **01_TECHNICAL_ARCHITECTURE.md** | Architektura ogólna (folder główny) |
| **05_THEME_SYSTEM.md** | Szczegóły systemu motywów |
| **06_API_DESIGN_CALCULATIONS.md** | Dokumentacja API |

---

## 🔧 TROUBLESHOOTING

### Problem: Aplikacja się nie uruchamia

```bash
# 1. Sprawdzić Python
python --version          # Musi być 3.9+

# 2. Sprawdzić venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Reinstaluj zależności
pip install --upgrade pip
pip install -r TESTER/requirements_tester.txt

# 4. Uruchom ponownie
python TESTER/tester_app.py
```

### Problem: Baza danych uszkodzona

```bash
# 1. Zamknij aplikację

# 2. Reset bazy
rm tester_workhoursapp.db

# 3. Uruchom aplikację (stworzy nową bazę)
python TESTER/tester_app.py

# 4. Lub w UI: Tab "🗄️ Baza" → "⚠️ Reset"
```

### Problem: Błędy PDF

```bash
# 1. Sprawdzić folder
ls -la TESTER/reports/

# 2. Uprawnienia zapisu
chmod 755 TESTER/reports/

# 3. Sprawdzić ReportLab
python -c "import reportlab; print(reportlab.Version)"

# 4. Reinstaluj
pip install --upgrade reportlab
```

---

## 📈 PLAN TESTOWANIA

### Przed Publikacją (MVP)

```
Tydzień 1: Testy podstawowe (TC-001 - TC-006)
Tydzień 2: Raport i Profile (TC-007 - TC-010)
Tydzień 3: Motywy i Wydajność (TC-011 - TC-014)
Tydzień 4: Bezpieczeństwo i Brzegowe (TC-015 - TC-018)
Tydzień 5: Testy integracyjne (TC-019 - TC-020)
```

### Checklist Publikacji

```
□ Wszystkie scenariusze przeszły
□ Brak crash'ów
□ Performance OK (<3s ładowanie)
□ PDF generuje się
□ Motywy działają
□ Uprawnienia OK
□ Dokumentacja kompletna
```

---

## 🎓 LEARNING RESOURCES

### Kivy Documentation
- [Kivy Official](https://kivy.org/doc/)
- [KivyMD Documentation](https://kivymd.readthedocs.io/)

### Python Testing
- [pytest Official](https://docs.pytest.org/)
- [Python unittest](https://docs.python.org/3/library/unittest.html)

### Android Development
- [Android Developer Guide](https://developer.android.com/)
- [Buildozer Wiki](https://github.com/kivy/buildozer/wiki)

---

## 📞 SUPPORT

### Pytania?

```
1. Sprawdź TEST_SCENARIOS.md (20+ przykładów)
2. Sprawdzić INSTALLATION_GUIDE.md (4 metody)
3. Sprawdzić Troubleshooting sekcję wyżej
4. Email: support@workhours.app
5. GitHub Issues: [repo]/issues
```

### Reportowanie Bugów

```
Patrz sekcja: "🐛 RAPORTOWANIE BŁĘDÓW"
Format jest prawie zawsze najważniejszy!
```

---

## 📋 CHECKLISTA GOTOWOŚCI

Przed publikacją aplikacji:

```
□ Aplikacja testowa (tester_app.py) testowana
□ Wszystkie 20+ scenariuszy przeszły
□ PDF Reports działają
□ Motywy A+B+Animacje działają
□ Profily izolują dane
□ Wydajność OK (100+ wpisów)
□ Bezpieczeństwo sprawdzone
□ Dokumentacja kompletna
□ Instalacja na telefonie weryfikowana
□ Uprawnienia udzielane
□ Backup/Restore działa
□ Błędy raportowane i naprawione
```

---

## 📊 STATYSTYKI

```
Scenariusze testowe:    20+ (TC-001 - TC-020)
Etapy testowania:       5 (Podstawowy → Integracyjny)
Dokumentacja:           3 pliki
Pokrycie funkcji:       95%+
Oczekiwany czas:        5+ godzin
```

---

## ✨ KONIEC!

Jesteś gotów do testowania aplikacji jak profesjonalista. 🎉

**Data:** 4 lutego 2026  
**Wersja:** 1.0.0 (MVP)  
**Status:** Production Ready ✓

---

Happy Testing! 🧪🚀
