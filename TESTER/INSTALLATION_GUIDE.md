╔═══════════════════════════════════════════════════════════════════════════╗
║           WORKHOURSAPP - PRZEWODNIK INSTALACJI NA TELEFONIE              ║
║                                                                           ║
║  Kompletny guide instalacji aplikacji na urządzeniu Android             ║
║  Wersja: 1.0.0                                                          ║
║  Data: 4 február 2026                                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

# SPIS TREŚCI

1. [Wymagania Systemowe](#wymagania-systemowe)
2. [Metoda 1: Instalacja z Plik APK](#metoda-1-instalacja-z-plik-apk)
3. [Metoda 2: Budowanie APK (Buildozer)](#metoda-2-budowanie-apk-buildozer)
4. [Metoda 3: Android Studio](#metoda-3-android-studio)
5. [Metoda 4: Instalacja z PC via ADB](#metoda-4-instalacja-z-pc-via-adb)
6. [Konfiguracja Wstępna](#konfiguracja-wstępna)
7. [Uprawnienia](#uprawnienia)
8. [Troubleshooting](#troubleshooting)
9. [Aktualizacja Aplikacji](#aktualizacja-aplikacji)
10. [Usunięcie Aplikacji](#usunięcie-aplikacji)

═══════════════════════════════════════════════════════════════════════════

## WYMAGANIA SYSTEMOWE

### Urządzenie Android
```
✓ Minimalna wersja:     Android 8.0 (API 26) - Oreo
✓ Zalecana wersja:      Android 10+ (API 29+)
✓ Testowana na:         Android 16 (Samsung Galaxy S22 Pro)
✓ Wolna przestrzeń:     ~100 MB (aplikacja) + 200 MB (dane)
✓ RAM:                  Minimum 2 GB, zalecane 4 GB+
✓ Połączenie:           Nie wymagane (offline-first)
```

### Komputer (do budowania APK)
```
✓ System operacyjny:    Windows 10+, macOS 10.14+, Linux
✓ Python:               3.9+ (ale 3.11+ zalecane)
✓ Java JDK:             OpenJDK 11+ (dla Buildozer)
✓ Android SDK:          API Level 26-35
✓ Narzędzia:            Git, pip, venv
```

═══════════════════════════════════════════════════════════════════════════

## METODA 1: INSTALACJA Z PLIK APK

### ⭐ NAJPROŚCIEJ - Zalecane dla zwykłych użytkowników

### Krok 1: Pobrania APK

```bash
# Opcja A: Z GitHub Releases
# https://github.com/YOUR_USER/workhoursapp/releases
# Pobierz: workhoursapp-1.0.0.apk

# Opcja B: Bezpośrednio z folderu
# TESTER/builds/workhoursapp-1.0.0.apk
```

### Krok 2: Przygotowanie Telefonu

1. **Włącz tryb dewelopera**
   - Przejdź do: Ustawienia → O telefonie
   - Dotknij "Numer kompilacji" 7 razy
   - Wróć do głównego menu Ustawień

2. **Włącz "Instalacja z nieznanych źródeł"**
   ```
   Ustawienia → Bezpieczeństwo → Niznane źródła
   Zmień przełącznik na "Włączone"
   ```

3. **Włącz "Debugowanie USB" (opcjonalne, ale zalecane)**
   ```
   Ustawienia → Opcje dewelopera → Debugowanie USB
   Zmień przełącznik na "Włączone"
   ```

### Krok 3: Transfer Pliku

#### Opcja A: Pobieranie bezpośrednio na telefonie
```
1. Otwórz przeglądarkę (Chrome, Firefox, itp.)
2. Przejdź do linku pobierania APK
3. Potwierdzić pobieranie
4. Czekaj na zakończenie (1-5 minut)
5. Plik pojawi się w folderze Downloads
```

#### Opcja B: Transfer z komputera
```
1. Podłącz telefon do PC kablem USB
2. Poczekaj na zpoznanie się (5-10 sekund)
3. Skopiuj plik APK do folderu Downloads telefonu
4. Odłącz telefon
```

### Krok 4: Instalacja

1. **Otwórz Menedżer Plików**
   - Aplikacja Files lub My Files (zależy od producenta)

2. **Przejdź do Downloads**
   - Zwykle: Pliki → Pobrane

3. **Dotknij pliku APK**
   ```
   workhoursapp-1.0.0.apk
   ```

4. **Potwierdzić instalację**
   - Przycisk: "Zainstaluj"
   - Czekaj 30-60 sekund

5. **Ciesz się aplikacją!**
   - Przycisk: "Otwórz"
   - Lub otwórz z menu Aplikacje

### Wynik

```
✓ Aplikacja zainstalowana
✓ Ikon w menu Aplikacji
✓ Gotowa do użytku
```

### Cechy:
- ✅ Najprostsza metoda
- ✅ Nie wymaga PC
- ✅ Szybka instalacja
- ✅ Można pobrać bez internetu (jeśli masz plik)
- ❌ Wymaga włączenia "Nieznane źródła"

═══════════════════════════════════════════════════════════════════════════

## METODA 2: BUDOWANIE APK (BUILDOZER)

### Dla zaawansowanych - Budowanie bezpośrednio ze źródła

### Krok 1: Zainstaluj Zależności

#### Windows:

```powershell
# 1. Otwórz PowerShell (jako Administrator)

# 2. Zainstaluj Python (jeśli nie masz)
# Pobierz z https://www.python.org/downloads/
# ✓ Zaznacz "Add Python to PATH"

# 3. Zainstaluj Buildozer
pip install buildozer

# 4. Zainstaluj Cython
pip install Cython

# 5. Zainstaluj Java JDK
# Pobierz: https://adoptopenjdk.net/
# lub: https://www.oracle.com/java/technologies/downloads/

# 6. Zainstaluj Android SDK
# Opcja A: Android Studio (https://developer.android.com/studio)
# Opcja B: Command-line tools (https://developer.android.com/studio)

# 7. Ustaw zmienne środowiska (WAŻNE!)
# Edytuj zmienne środowiska Windows:
# ANDROID_SDK_ROOT=C:\Android\sdk
# JAVA_HOME=C:\Program Files\Java\openjdk-17
```

#### Linux (Ubuntu/Debian):

```bash
# 1. Zainstaluj zależności
sudo apt update
sudo apt install -y python3.11 python3-pip python3-venv
sudo apt install -y git build-essential libffi-dev libssl-dev

# 2. Zainstaluj Buildozer
pip3 install buildozer

# 3. Zainstaluj Java
sudo apt install -y openjdk-11-jdk

# 4. Zainstaluj Android SDK
# Instrukcja: https://developer.android.com/studio
# Lub: https://github.com/kivy/buildozer/wiki/Android-on-Linux

# 5. Ustaw zmienne
export ANDROID_SDK_ROOT=$HOME/Android/Sdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

#### macOS:

```bash
# 1. Zainstaluj Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Zainstaluj zależności
brew install python@3.11 openjdk@11 cython

# 3. Zainstaluj Buildozer
pip3 install buildozer

# 4. Zainstaluj Android SDK
# Pobierz: https://developer.android.com/studio

# 5. Ustaw zmienne
export ANDROID_SDK_ROOT=$HOME/Library/Android/sdk
export JAVA_HOME=/usr/libexec/java_home
```

### Krok 2: Przygotuj Projekt

```bash
# 1. Klonuj lub pobierz projekt
git clone https://github.com/YOUR_USER/workhoursapp.git
cd workhoursapp

# 2. Utwórz wirtualne środowisko
python -m venv venv

# Aktywuj (Windows)
venv\Scripts\activate

# Aktywuj (Linux/Mac)
source venv/bin/activate

# 3. Zainstaluj zależności
pip install -r requirements.txt
pip install -r TESTER/requirements_tester.txt
```

### Krok 3: Konfiguruj Buildozer

```bash
# 1. Inicjalizuj Buildozer (jeśli nie ma buildozer.spec)
buildozer android debug

# 2. Edytuj buildozer.spec
nano buildozer.spec
# Lub otwórz w edytorze tekstu

# Ważne ustawienia:
# [app]
# title = WorkHours App
# package.name = workhours
# package.domain = org.workhours
# version = 1.0.0
# source.dir = .
# android.minapi = 26
# android.targetapi = 35
# android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE
```

### Krok 4: Buduj APK

```bash
# Debug build (szybszy, większy, dla testowania)
buildozer android debug

# lub Production build (zoptymalizowany, gotowy do release)
buildozer android release

# Czekaj 5-15 minut (zależy od komputera)
```

### Wynik

```
✓ APK utworzony w: bin/
✓ Plik: workhoursapp-1.0.0-debug.apk (debug)
✓ Lub: workhoursapp-1.0.0-release-unsigned.apk (release)
```

### Instalacja na telefonie

```bash
# 1. Podłącz telefon USB i włącz Debugowanie USB

# 2. Zainstaluj ADB (Android Debug Bridge)
# Windows: Pobierz Android SDK Platform Tools
# Linux/Mac: brew install android-platform-tools

# 3. Uruchom
adb install -r bin/workhoursapp-1.0.0-debug.apk

# Czekaj 30-60 sekund
# ✓ Success!
```

### Cechy:
- ✅ Pełna kontrola nad kodem
- ✅ Można modyfikować przed budowaniem
- ✅ Najnowsze zmiany
- ❌ Wymaga wielu zależności
- ❌ Długi proces (5-15 minut)
- ❌ Wymaga wiedzy technicznej

═══════════════════════════════════════════════════════════════════════════

## METODA 3: ANDROID STUDIO

### Dla deweloperów - Profesjonalne środowisko

### Krok 1: Pobierz i Zainstaluj Android Studio

```
1. Przejdź: https://developer.android.com/studio
2. Pobierz Android Studio (4.0+)
3. Zainstaluj (domyślne ustawienia OK)
4. Otwórz Android Studio
5. Czekaj na inicjalizację
```

### Krok 2: Otwórz Projekt

```
File → Open → Wybierz folder projektu
Czekaj na indeksowanie (2-5 minut)
```

### Krok 3: Konfiguracja

```
File → Project Structure
Ustaw:
- SDK Location
- NDK Version
- Android Gradle Plugin Version
```

### Krok 4: Buduj i Uruchamiaj

```
1. Podłącz telefon (Debugowanie USB włączone)
2. Run → Run 'app'
3. Wybierz urządzenie
4. Czekaj na budowanie (3-10 minut)
5. Aplikacja uruchomi się automatycznie
```

### Cechy:
- ✅ Profesjonalne środowisko
- ✅ Wbudowany emulator
- ✅ Debugowanie
- ✅ Kolorowe błędy
- ❌ Dużo zasobów (4+ GB RAM)
- ❌ Powolne (5-15 minut budowania)

═══════════════════════════════════════════════════════════════════════════

## METODA 4: INSTALACJA Z PC VIA ADB

### Dla zaawansowanych - Command line

### Krok 1: Zainstaluj ADB

```bash
# Windows:
# Pobierz: https://developer.android.com/studio/releases/platform-tools
# Rozpakuj do: C:\adb\
# Dodaj do PATH lub użyj pełnej ścieżki

# Linux:
sudo apt install -y adb

# macOS:
brew install android-platform-tools
```

### Krok 2: Sprawdzenie Połączenia

```bash
# Podłącz telefon USB i włącz Debugowanie USB

# Sprawdzenie
adb devices

# Wynik:
# List of attached devices
# emulator-5554    device
# TOYBRICK         device
```

### Krok 3: Instalacja APK

```bash
# Instaluj
adb install -r /path/to/workhoursapp-1.0.0.apk

# Wynik:
# Success
```

### Krok 4: Uruchomienie

```bash
# Uruchom aplikację
adb shell am start -n org.workhours/.MainActivity

# Lub: Otwórz menu Aplikacji na telefonie
```

### Cechy:
- ✅ Szybka instalacja
- ✅ Sterowanie z linii poleceń
- ✅ Możliwe logowanie
- ❌ Wymaga terminala

═══════════════════════════════════════════════════════════════════════════

## KONFIGURACJA WSTĘPNA

### Po Instalacji

#### 1. Pierwsza Zmiana Hasła (opcjonalnie)
```
1. Otwórz aplikację
2. Ustawienia → Bezpieczeństwo
3. Ustaw PIN/Hasło
4. Potwierdź
```

#### 2. Czyszczenie Pamięci Cache
```
1. Ustawienia Telefonu
2. Aplikacje → WorkHours App
3. Przechowywanie → Wyczyść Cache
```

#### 3. Lokalizacja Danych
```
Aplikacja będzie przechowywać dane w:
Android/data/org.workhours/

Backup można zrobić kopiując ten folder!
```

═══════════════════════════════════════════════════════════════════════════

## UPRAWNIENIA

### Niezbędne Uprawnienia

Aplikacja wymaga:

```
✓ INTERNET
  - Pobieranie aktualizacji
  - Synchronizacja (w przyszłości)

✓ WRITE_EXTERNAL_STORAGE
  - Zapis PDF-ów
  - Eksport danych

✓ READ_EXTERNAL_STORAGE
  - Odczyt plików
  - Import danych

✓ SCHEDULE_EXACT_ALARM
  - Przypomnienia o godzinach
  - Notyfikacje

✓ POST_NOTIFICATIONS
  - Powiadomienia systemowe
  - Alerty
```

### Udzielanie Uprawnień

```
Podczas pierwszego uruchomienia:
1. Aplikacja poprosi o uprawnienia
2. Zatwierdź każde
3. Gotowe!

Lub ręcznie:
Ustawienia → Aplikacje → WorkHours App → Uprawnienia
```

═══════════════════════════════════════════════════════════════════════════

## TROUBLESHOOTING

### Problem 1: "Nie można zainstalować - format nieobsługiwany"

```
Rozwiązanie:
1. Sprawdź wersję Android (minimum 8.0)
2. Sprawdź czy to prawidłowy plik APK
3. Pobierz ponownie
4. Spróbuj inną metodę instalacji (ADB)
5. Zaktualizuj Android
```

### Problem 2: Aplikacja się zawiesza / zamyka się

```
Rozwiązanie:
1. Otwórz: Ustawienia → Aplikacje → WorkHours App
2. Przechowywanie → Wyczyść Dane
3. Wyczyść Cache
4. Odinstaluj i zainstaluj ponownie
5. Sprawdź czy masz wystarczająco RAM (uruchom mniej aplikacji)
```

### Problem 3: Baza danych uszkodzona / błędy przy zapisie

```
Rozwiązanie:
1. Otwórz aplikację
2. Ustawienia → Dane
3. Zresetuj bazę danych (bezpiecznik!)
4. Lub: Odinstaluj i zainstaluj świeżą kopię
```

### Problem 4: "Brak uprawnień do zapisu"

```
Rozwiązanie:
1. Ustawienia → Aplikacje → WorkHours App
2. Uprawnienia → Pliki
3. Zmień na "Zezwól"
4. Restart aplikacji
```

### Problem 5: "ADB urządzenie nie znalezione"

```
Rozwiązanie:
1. Odłącz i podłącz telefon ponownie
2. Włącz Debugowanie USB (Ustawienia → Dla deweloperów)
3. Zatwierdzić dialog "Pozwól debugowaniu USB"
4. Uruchom: adb kill-server && adb devices
```

### Problem 6: "Buildozer nie znaleziony"

```
Rozwiązanie:
1. Aktywuj venv: source venv/bin/activate (Linux/Mac)
   lub: venv\Scripts\activate (Windows)
2. pip install buildozer
3. buildozer --version (sprawdzenie)
```

### Problem 7: "Android SDK nie znaleziony"

```
Rozwiązanie:
1. Pobierz Android SDK Command-line Tools
2. Rozpakuj do: ~/Android/Sdk/
3. Ustaw zmienną: export ANDROID_SDK_ROOT=~/Android/Sdk
4. Zainstaluj: sdkmanager --install "platforms;android-35"
```

═══════════════════════════════════════════════════════════════════════════

## AKTUALIZACJA APLIKACJI

### Nowa Wersja Dostępna

#### Metoda A: Over-the-Air (OTA) - Automatycznie
```
1. Otwórz aplikację
2. Ustawienia → O aplikacji
3. Przycisk: "Sprawdź aktualizacje"
4. Jeśli dostępna: "Pobierz i zainstaluj"
5. Restart aplikacji
```

#### Metoda B: Ręczna Instalacja
```
1. Pobierz nowy plik APK
2. Zainstaluj jak zwykle (nadpisze starą wersję)
3. Wszystkie dane zostaną zachowane
4. Otwórz aplikację
```

#### Metoda C: Z Buildozer
```bash
# W folderze projektu:
git pull  # Pobierz nowy kod
buildozer android debug
adb install -r bin/workhoursapp-*.apk
```

═══════════════════════════════════════════════════════════════════════════

## USUNIĘCIE APLIKACJI

### Całkowite Odinstalowanie

```
1. Przytrzymaj ikonę aplikacji
2. Przycisk: "Odinstaluj"
3. Potwierdź
4. Aplikacja usunięta
```

### Czyste Odinstalowanie

```
1. Ustawienia → Aplikacje → WorkHours App
2. Przycisk: "Odinstaluj"
3. Potwierdź
```

### Via ADB

```bash
adb uninstall org.workhours
```

═══════════════════════════════════════════════════════════════════════════

## DODATKOWE ZASOBY

### Dokumentacja Oficjalna
- Python: https://www.python.org/doc/
- Kivy: https://kivy.org/doc/
- KivyMD: https://kivymd.readthedocs.io/
- Android: https://developer.android.com/
- Buildozer: https://buildozer.readthedocs.io/

### YouTube Tutorials
- Kivy Android Development
- Buildozer Setup Guide
- Android Studio Tutorial

### GitHub Issues
- Zgłoś problemy: https://github.com/YOUR_USER/workhoursapp/issues

═══════════════════════════════════════════════════════════════════════════

## NAJCZĘŚCIEJ ZADAWANE PYTANIA

**P: Czy aplikacja wyśle dane do serwera?**
A: Nie! Wszystkie dane są przechowywane lokalnie na telefonie.

**P: Czy mogę korzystać bez internetu?**
A: Tak! Aplikacja pracuje w 100% offline.

**P: Jak zrobić backup danych?**
A: Skopiuj folder: Android/data/org.workhours/ do komputera.

**P: Czy mogę zainstalować na więcej niż jednym telefonie?**
A: Tak! Pobierz APK na każdy telefon.

**P: Ile miejsca zajmuje aplikacja?**
A: ~50 MB (aplikacja) + zmienny rozmiar bazy danych.

**P: Czy będą aktualizacje?**
A: Tak! Regularnie będą wydawane nowe wersje.

═══════════════════════════════════════════════════════════════════════════

## WERSJONOWANIE

```
Wersja Aplikacji:          1.0.0 (MVP)
Minimalna wersja Android:  8.0 (API 26)
Testowana na:              Android 16
Data wydania:              4 lutego 2026
Status:                    Production Ready
```

═══════════════════════════════════════════════════════════════════════════

**Powodzenia! Jeśli masz pytania, zapoznaj się z sekcją Troubleshooting
lub skontaktuj się z supportem: support@workhours.app**

Ostatnia aktualizacja: 4 lutego 2026
