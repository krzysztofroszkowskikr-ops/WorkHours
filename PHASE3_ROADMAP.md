# Phase 3 Roadmap - Android Build & Deployment

## 🚀 Overview

Phase 3 polega na konwersji aplikacji Kivy z pracy na PC do działającego APK-a na Androidzie.

**Status**: ⏳ IN PLANNING  
**Estymowana Długość**: 2-3 sesje  
**Złożoność**: Wysoka (nowe narzędzia, konfiguracja)  

---

## 📋 Fazy Phase 3

### Phase 3.1: Buildozer Setup ⏳

#### 3.1.1 - Instalacja Buildozer
```bash
# Zainstaluj buildozer
pip install buildozer

# Weryfikuj instalację
buildozer --version
```

#### 3.1.2 - Przygotowanie buildozer.spec
```bash
# Stwórz bazowy spec
buildozer init

# Edytuj buildozer.spec:
[app]
title = WorkHours
package.name = workhours
package.domain = org.workhours

[buildozer]
# Android SDK/NDK paths
android_sdk_path = /path/to/android-sdk
android_ndk_path = /path/to/android-ndk

# Wersja Android
android_api = 30
android_minapi = 21
android_ndk_version = 25.1.8937393
```

#### 3.1.3 - Wymagane Komponenty
- [ ] Android SDK (API 21-30)
- [ ] Android NDK (r25.1.8937393)
- [ ] Java Development Kit (JDK 8+)
- [ ] Ant build tool

**Oczekiwany czas**: 1-2 godziny

---

### Phase 3.2: Plyer Integration ⏳

#### 3.2.1 - Storage Access
```python
from plyer import storagepath

# Dostęp do Documents folder
docs_path = storagepath.get_documents_dir()
```

#### 3.2.2 - Notyfikacje
```python
from plyer import notification

notification.notify(
    title="WorkHours",
    message="Wpis zapisany",
    timeout=5
)
```

#### 3.2.3 - Permissions w AndroidManifest.xml
```xml
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.INTERNET" />
```

**Oczekiwany czas**: 30 minut

---

### Phase 3.3: APK Generation ⏳

#### 3.3.1 - Debug Build
```bash
buildozer android debug
```

#### 3.3.2 - Release Build
```bash
buildozer android release
```

#### 3.3.3 - Keystore Creation
```bash
keytool -genkey -alias workhours -keyalg RSA -keysize 2048 \
  -keystore workhours.keystore -validity 10000
```

**Oczekiwany czas**: 45 minut (pierwszy build może być długi)

---

### Phase 3.4: Testing ⏳

#### 3.4.1 - Device Testing
- [ ] Zainstaluj APK na testowym urządzeniu
- [ ] Test wszystkich ekranów
- [ ] Test formularza wpisów
- [ ] Test raportów PDF
- [ ] Test bazy danych
- [ ] Test obsługi błędów

#### 3.4.2 - Performance Testing
- [ ] Pomiar czasu startup
- [ ] Sprawdzenie pamięci
- [ ] Sprawdzenie baterii
- [ ] Sprawdzenie połączenia WiFi

#### 3.4.3 - Compatibility Testing
- [ ] Android 5.0+ (API 21+)
- [ ] Różne rozdzielczości ekranu
- [ ] Orientacja pionowa/pozioma
- [ ] Urządzenia tablet i phone

**Oczekiwany czas**: 2-3 godziny

---

### Phase 3.5: Google Play Submission ⏳

#### 3.5.1 - Play Store Setup
- [ ] Utwórz Google Play Developer account ($25)
- [ ] Utwórz aplikację na Play Console
- [ ] Przygotuj ikony (192x192, 512x512)
- [ ] Przygotuj screenshoty (min. 2)

#### 3.5.2 - App Listing
- [ ] Opis aplikacji
- [ ] Screenshots (min. 2, max 8)
- [ ] Kategoria aplikacji
- [ ] Content rating questionnaire
- [ ] Privacy policy

#### 3.5.3 - Upload APK
- [ ] Generate release build
- [ ] Sign release APK
- [ ] Upload do Play Store
- [ ] Ustaw cena (free)
- [ ] Deploy

**Oczekiwany czas**: 1-2 godziny

---

## 🛠️ Technical Checklist

### Pre-Build Requirements
- [ ] Python 3.11.6 zainstalowany
- [ ] Kivy 2.3.0 zainstalowany
- [ ] Buildozer zainstalowany
- [ ] Android SDK zainstalowany
- [ ] Android NDK zainstalowany
- [ ] JDK zainstalowany
- [ ] Ant zainstalowany

### Code Requirements
- [ ] Wszystkie importy działają
- [ ] Brak błędów typu
- [ ] Brak syntax errors
- [ ] 230+ testów przechodzi
- [ ] Obsługa błędów kompletna
- [ ] Logging skonfigurowany

### Android Requirements
- [ ] buildozer.spec skonfigurowany
- [ ] Permissions w AndroidManifest.xml
- [ ] Icony w res/drawable/ (ldpi, mdpi, hdpi, xhdpi)
- [ ] Strings w res/values/strings.xml
- [ ] Plyer zintegrowany

### Distribution Requirements
- [ ] Release keystore wygenerowany
- [ ] APK podpisany
- [ ] Wersja zadbana
- [ ] Play Store account aktywny
- [ ] App listing kompletne
- [ ] Screenshots przygotowane

---

## 📊 Expected Results

### Debug Build (~5-10 min)
```
buildozer android debug
# Output: bin/workhours-0.1-debug.apk (50-80 MB)
```

### Release Build (~10-15 min)
```
buildozer android release
# Output: bin/workhours-0.1-release-unsigned.apk (45-70 MB)
```

### Signed Release (~1 min)
```
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore workhours.keystore \
  bin/workhours-0.1-release-unsigned.apk alias_name
# Output: bin/workhours-0.1-release.apk (ready for Play Store)
```

---

## 🎯 Success Criteria

### ✅ Phase 3.1 Success
- [ ] buildozer --version works
- [ ] buildozer.spec created
- [ ] Android SDK path configured
- [ ] Android NDK path configured

### ✅ Phase 3.2 Success
- [ ] Plyer imported w aplikacji
- [ ] Permissions w manifest
- [ ] Storage access works
- [ ] Notyfikacje działają

### ✅ Phase 3.3 Success
- [ ] Debug APK generated
- [ ] Release APK generated
- [ ] APK signed
- [ ] APK size < 100 MB

### ✅ Phase 3.4 Success
- [ ] App instaluje się na device
- [ ] Dashboard ekran działa
- [ ] Entry form działa
- [ ] PDF generation działa
- [ ] Baza danych działa
- [ ] Bez crashów

### ✅ Phase 3.5 Success
- [ ] Play Store listing created
- [ ] App approved by Google
- [ ] App available for download
- [ ] User reviews positive

---

## ⚠️ Known Challenges

### 1. Buildozer Setup
**Problem**: Buildozer setup może być długi (SDK/NDK ~1GB+)  
**Rozwiązanie**: Zainstaluj offline, lub użyj VirtualBox z Android Studio

### 2. APK Size
**Problem**: APK może być 80-100MB (Kivy + Python runtime)  
**Rozwiązanie**: Możliwe to jest - to jest normalne dla Kivy apps

### 3. Performance
**Problem**: Kivy może być wolniejszy na starszych deviceach  
**Rozwiązanie**: Optimize database queries, use Cython for hotspots

### 4. Android Permissions
**Problem**: Storage access wymaga runtime permissions na Android 6+  
**Rozwiązanie**: Use Plyer do request permissions

### 5. Play Store Policies
**Problem**: App musi spełniać Google Play policy  
**Rozwiązanie**: Privacy policy, no malware, etc.

---

## 🔮 Post-Launch

### Monitoring
- [ ] Crash reporting (Firebase Crashlytics)
- [ ] User analytics (Firebase Analytics)
- [ ] App reviews monitoring
- [ ] Bug tracking

### Updates
- [ ] Bug fixes
- [ ] Feature additions
- [ ] Performance optimization
- [ ] Security updates

### Marketing
- [ ] App store optimization (ASO)
- [ ] Social media promotion
- [ ] Beta testing (Play Console)
- [ ] User feedback incorporation

---

## 📚 Resources

### Documentation
- [Buildozer Docs](https://buildozer.readthedocs.io/)
- [Plyer Docs](https://plyer.readthedocs.io/)
- [Kivy on Android](https://kivy.org/doc/stable/guide/android.html)
- [Google Play Console Docs](https://support.google.com/googleplay/android-developer)

### Tools
- Buildozer: `pip install buildozer`
- Android Studio: [download](https://developer.android.com/studio)
- jarsigner: comes with JDK
- apktool: optional, for APK inspection

### Community
- Kivy Discord: https://discord.gg/kivy
- Buildozer Issues: https://github.com/kivy/buildozer/issues
- Stack Overflow: tag [kivy] or [buildozer]

---

## 🏁 Next Steps

When ready for Phase 3:

1. **Type**: `kontynuuj budować Android`
2. **Start**: Buildozer installation & configuration
3. **Follow**: This roadmap step-by-step
4. **Build**: Debug → Release → Signed APK
5. **Test**: On multiple devices
6. **Deploy**: To Google Play Store

---

**Ready for Phase 3?** Type "kontynuuj budować Android" to continue!

**Estimated Total Time**: 4-6 hours (first time)  
**Difficulty**: Medium-High  
**Success Rate**: 85%+ (with proper setup)

---

Ostatnia aktualizacja: 2024-02-04
Przygotowanie: Phase 3 Ready ✅

