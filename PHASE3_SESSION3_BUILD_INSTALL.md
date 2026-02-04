# Phase 3.3 - Android Build & Installation Guide

## Overview

Masz teraz kompletny zestaw skryptów do zbudowania i zainstalowania aplikacji WorkHours na urządzeniu Android.

**Status**: 🟢 Gotowy do budowania APK

## Workflow

```
1. Konfiguracja SDK/NDK     (configure_android_paths.py)
2. Weryfikacja środowiska   (verify_android_env.py)
3. Budowanie APK            (build_apk.py)
4. Instalacja na urządzeniu (install_apk.py)
```

---

## Krok 1: Konfiguracja Ścieżek SDK/NDK

### Jeśli jeszcze nie masz zainstalowanych narzędzi:

Przejdź do [PHASE3_SESSION2_ANDROID_SETUP.md](PHASE3_SESSION2_ANDROID_SETUP.md) i zainstaluj:
- ✅ JDK 8+
- ✅ Android SDK
- ✅ Android NDK r25b

### Jeśli masz już zainstalowane narzędzia:

```bash
# Automatyczne wykrycie ścieżek
python configure_android_paths.py --auto

# Lub ręczna konfiguracja
python configure_android_paths.py \
  --sdk "C:\Users\YourUser\AppData\Local\Android\Sdk" \
  --ndk "C:\Android\ndk\android-ndk-r25b"
```

**Wynik**: 
- ✅ `android_sdk_path` zaktualizowana w `buildozer.spec`
- ✅ `android_ndk_path` zaktualizowana w `buildozer.spec`

---

## Krok 2: Weryfikacja Środowiska

Sprawdź czy wszystko jest prawidłowo zainstalowane:

```bash
python verify_android_env.py
```

**Spodziewany wynik**:
```
[1/5] Checking Java (JDK)... ✅
[2/5] Checking Android SDK... ✅
[3/5] Checking Android NDK... ✅
[4/5] Checking Buildozer... ✅
[5/5] Checking Disk Space... ✅

Passed: 5/5
🎉 All checks passed! Ready to build APK.
```

**Jeśli są błędy**: Sprawdź komunikat błędu i napraw problem zanim przejdziesz dalej.

---

## Krok 3: Budowanie APK

### Build Debug (na testowanie)

```bash
python build_apk.py --type debug
```

**Czas budowania**: ~5-15 minut (na pierwszym uruchomieniu może być dłużej)

**Wyjście**: 
```
✅ APK build successful!
📦 APK Location: bin/workhours-1.0.0-debug.apk
   Size: 85.3MB
```

### Build Release (do Google Play)

```bash
python build_apk.py --type release
```

⚠️ Wymaga podpisania certyfikatem - zobacz [Phase 3.4](PHASE3_SESSION4_GOOGLE_PLAY.md)

### Czyszczenie przed buildem

```bash
python build_apk.py --type debug --clean
```

---

## Krok 4: Instalacja na Urządzeniu

### Przygotowanie urządzenia

1. **Podłączyć** telefon do komputera kablem USB
2. **Włączyć** mode developer:
   - Settings → About Phone
   - Kliknięcie Build Number 7 razy
   - Settings → Developer Options
3. **Włączyć** USB Debugging:
   - Developer Options → USB Debugging → ON
4. **Autoryzować** połączenie na telefonie

### Instalacja aplikacji

```bash
# Automatyczne wykrycie i instalacja
python install_apk.py

# Lub wskazać konkretne urządzenie
python install_apk.py --device emulator-5554

# Lub wskazać konkretny APK
python install_apk.py --apk bin/workhours-1.0.0-debug.apk
```

**Spodziewany wynik**:
```
✅ Found adb
✅ Found 1 device(s):
   1. emulator-5554 (selected)
📦 Installing APK: bin/workhours-1.0.0-debug.apk
✅ APK installed successfully!
🎉 Ready to use! Launch 'WorkHours' app on your device.
```

### Uruchomienie aplikacji

1. Na urządzeniu otwórz **App Drawer**
2. Znajdź i kliknij **WorkHours**
3. Gotowe! 🎉

---

## Rozwiązywanie Problemów

### Problem: "adb not found"

```bash
# Rozwiązanie: Android SDK path nie jest w PATH
# Dodaj do PATH: C:\Users\YourUser\AppData\Local\Android\Sdk\platform-tools
```

### Problem: "No connected devices"

```bash
# Sprawdź czy telefon jest podłączony:
adb devices

# Jeśli to emulator: uruchom emulator przed instalacją
```

### Problem: "Device not authorized"

```bash
# Autoryzuj na telefonie: Settings → USB Debugging → Allow
# Lub zresetuj:
adb kill-server
adb start-server
adb devices
```

### Problem: "Insufficient space on device"

Musisz mieć co najmniej 200MB wolnego miejsca na telefonie

### Problem: "Build failed"

1. Sprawdź czy wszystkie kroki w `verify_android_env.py` przeszły ✅
2. Wyczyść build: `python build_apk.py --clean --type debug`
3. Spróbuj ponownie

---

## Dodatkowe Komendy

### Listowanie podłączonych urządzeń

```bash
adb devices -l
```

### Uninstallacja aplikacji

```bash
adb uninstall org.workhours
```

### Logowanie z aplikacji

```bash
adb logcat | findstr WorkHours
```

### Resetowanie urządzenia

```bash
adb kill-server
adb start-server
```

---

## Następne Kroki

Po pomyślnej instalacji i testowaniu:

1. **Phase 3.3**: ✅ Build & Installation (aktualny)
2. **Phase 3.4**: Google Play Release
   - Podpisanie release APK
   - Google Play Console setup
   - App listing i submission
   - Deployment

Przejdź do: [PHASE3_SESSION4_GOOGLE_PLAY.md](PHASE3_SESSION4_GOOGLE_PLAY.md)

---

## Skróty

| Zadanie | Komenda |
|---------|---------|
| Konfiguracja | `python configure_android_paths.py --auto` |
| Weryfikacja | `python verify_android_env.py` |
| Build debug | `python build_apk.py --type debug` |
| Build release | `python build_apk.py --type release` |
| Instalacja | `python install_apk.py` |
| Lista urządzeń | `adb devices -l` |

---

## Status

| Faza | Status | Czas |
|------|--------|------|
| 3.1: Buildozer Setup | ✅ COMPLETE | 30 min |
| 3.2: Android SDK/NDK | ✅ COMPLETE | 1-2 hours |
| 3.3: Build & Install | 🔄 IN PROGRESS | 30 min |
| 3.4: Google Play | ⏳ NOT STARTED | 1-2 hours |

---

## Metryki Projektu

- **Total backend**: 2,260+ lines
- **Total frontend**: 2,530+ lines
- **Build config**: buildozer.spec (105 lines)
- **Helper scripts**: 4 Python scripts (600+ lines)
- **Documentation**: 5 markdown files (2,000+ lines)

**APK Size**: ~85-100 MB (debug), ~50-60 MB (release)

---

## Wsparcie

Jeśli napotkasz problemy:

1. Sprawdź komunikaty błędu w zbudowanym wyjściu
2. Przejrzyj "Rozwiązywanie Problemów" powyżej
3. Sprawdź [official Buildozer docs](https://buildozer.readthedocs.io/)
4. Sprawdź [Android Developer Guide](https://developer.android.com/guide)

---

*Dokumentacja Phase 3.3 - Android Build & Installation*
*Last updated: 2026-02-04*
