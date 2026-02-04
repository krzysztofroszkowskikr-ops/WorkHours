# Phase 3.4 - Google Play Deployment Guide

## Overview

Przewodnik do publikacji aplikacji WorkHours na Google Play Store.

**Status**: ⏳ Przygotowanie do wdrożenia

---

## Wymagania

- ✅ APK zbudowany i przetestowany (Phase 3.3)
- ✅ Google Play Developer Account ($25 jednorazowo)
- ✅ Podpisany release APK
- ✅ App screenshots i description
- ✅ Privacy Policy

---

## Krok 1: Przygotowanie Release APK

### 1.1 Utworzenie Keystore

```bash
# Wygeneruj klucz do podpisywania (tylko raz!)
keytool -genkey -v -keystore workhours-release.jks -keyalg RSA -keysize 2048 -validity 36500

# Wymagane informacje:
# - Keystore password: (zapamiętaj!)
# - Key password: (może być taki sam)
# - Common Name: Your Name
# - Organizational Unit: Your Company
# - Organization: Your Company
# - City/Locality: Your City
# - State/Province: Your State
# - Country Code: PL (lub 2-znakowy kod kraju)
```

**Wynik**: `workhours-release.jks` (trzymaj w bezpiecznym miejscu!)

### 1.2 Konfiguracja Buildozer

Dodaj do `buildozer.spec` sekcji `[app:android]`:

```ini
# Android signing
android.release_artifact = aab
android.accept_sdk_license = True
android.logcat_filters = *:S python:D
android.gradle_dependencies = 

# Keystore signing (jeśli chcesz podpisywać w buildozer)
android.keystore = 1
android.keystore_path = workhours-release.jks
android.keystore_alias = workhours
```

### 1.3 Build Release APK

```bash
# Build release (bez podpisu w buildozer)
python build_apk.py --type release

# Lub ręcznie z buildozer:
buildozer android release
```

**Wyjście**: `bin/workhours-1.0.0-release.apk`

### 1.4 Podpis APK (ręcznie)

```bash
# Jeśli APK nie jest podpisany:
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore workhours-release.jks \
  bin/workhours-1.0.0-release.apk workhours

# Zweryfikuj podpis:
jarsigner -verify -verbose -certs bin/workhours-1.0.0-release.apk
```

**Spodziewane wyjście**:
```
jar verified.
```

---

## Krok 2: Google Play Console Setup

### 2.1 Utworzenie Konta Developer

1. Przejdź do [Google Play Console](https://play.google.com/console)
2. Zaloguj się na konto Google
3. Zaakceptuj warunki
4. Zapłać $25 (jednorazowo)

### 2.2 Utworzenie Aplikacji

1. W Google Play Console kliknij **Create app**
2. **App name**: WorkHours
3. **Default language**: English (lub Polski)
4. **Type**: Free or Paid (zalecam: Free)
5. Kliknij **Create**

### 2.3 Uzupełnij Dane Aplikacji

**1. App Access**
- Default: Users (wszyscy mogą)

**2. Content Rating**
- Questionnaire → Google Play Content Rating form
- Zawiera: time tracking, user profiles
- Główna kategoria: Productivity

**3. App Content**
- Targeting: Select target audience
- Minimum age: 13+
- Contains ads: No
- Accessibility: Support accessibility features

**4. Pricing & Distribution**
- Countries: Select all (lub wybrane)
- Device categories: Phones, Tablets

---

## Krok 3: Przygotowanie Materiałów

### 3.1 Screenshots

Musisz mieć 2-8 screenshotów na każdym rozmiarze ekranu:

**Phone (5.1 inch - 5.5 inch)**
- Wymiary: 1080 x 1920 px
- Wymagane: minimum 2

**Tablet (7 inch - 10 inch)**
- Wymiary: 1600 x 2560 px
- Wymagane: minimum 2 (opcjonalnie)

### 3.2 App Icon

- **Wymiary**: 512 x 512 px
- **Format**: PNG (bez przezroczystości)
- **Bezpieczna strefa**: 48 px od krawędzi

### 3.3 Feature Graphic

- **Wymiary**: 1024 x 500 px
- **Format**: PNG lub JPG
- **Zawartość**: Logo + tekst "Work Hours Tracking"

### 3.4 Description

**Short Description** (50 znaków):
```
Track your work hours easily
```

**Full Description** (4000 znaków):
```
WorkHours - Simple and efficient work time tracking application.

Features:
• Track daily work hours
• Support for different work types (work, sick leave, vacation, day off)
• Monthly and yearly reports
• PDF export
• Customizable themes
• Offline support

Perfect for freelancers, remote workers, and time-conscious professionals.
```

### 3.5 Privacy Policy

Utwórz plik `privacy_policy.html` z treścią:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Privacy Policy - WorkHours</title>
</head>
<body>
    <h1>Privacy Policy - WorkHours</h1>
    
    <h2>Data Collection</h2>
    <p>WorkHours stores data locally on your device:</p>
    <ul>
        <li>Work hours entries (local database)</li>
        <li>User profile information</li>
        <li>App preferences and settings</li>
    </ul>
    
    <h2>Data Storage</h2>
    <p>All data is stored locally on your device. No data is sent to external servers.</p>
    
    <h2>Permissions</h2>
    <p>The app requires the following permissions:</p>
    <ul>
        <li>INTERNET: Optional, for future cloud sync</li>
        <li>READ/WRITE_EXTERNAL_STORAGE: For file export</li>
        <li>ACCESS_FINE_LOCATION: For location-based features (future)</li>
    </ul>
    
    <h2>Contact</h2>
    <p>For privacy concerns, contact: your-email@example.com</p>
</body>
</html>
```

Umieść na serwerze i podaj URL w Google Play Console.

---

## Krok 4: Upload na Google Play

### 4.1 Przygotowanie do Uploadu

1. **App releases** → **Testing** → **Internal testing**
2. **Create release**
3. **Browse files** → Wybierz `workhours-1.0.0-release.apk`
4. **Release notes** (PL):
   ```
   Pierwsza publiczna wersja!
   
   Nowe cechy:
   • Śledzenie godzin pracy
   • Różne typy dni (praca, urlop, zwolnienie, wolne)
   • Raporty miesięczne i roczne
   • Eksport do PDF
   • Motywy barw
   ```

### 4.2 App Listing

1. **App listing** (lewa menu)
2. Uzupełnij wszystkie pola:

| Pole | Wartość |
|------|---------|
| Title | WorkHours |
| Short description | Track your work hours easily |
| Full description | (Patrz punkt 3.4) |
| Screenshots (phone) | 2-8 screenshotów |
| Feature graphic | 1024x500 banner |
| Icon | 512x512 PNG |
| Promotional text | (opcjonalnie) |

### 4.3 Content Rating

1. **Content rating questionnaire**
2. Zaznacz odpowiednie kategorie:
   - Apps that save data: YES
   - Contact information: YES (user profile)
   - User-generated content: NO
3. Submit
4. Czekaj na wynik (zwykle kilka minut)

### 4.4 Pricing & Distribution

1. **Pricing**
   - Free or Paid: **Free**
   
2. **Distribution**
   - Countries: Wybierz **All countries and regions**

### 4.5 Privacy Policy

1. **App content** → **Privacy policy**
2. Wklej URL do Twojej privacy policy

---

## Krok 5: Testowanie (Internal Testing)

### 5.1 Internal Testing Release

1. **Testing** → **Internal testing**
2. **Create release** → Upload APK
3. **Testers**: Dodaj testerów (maile Google)
4. Prześlij im link do testowania
5. **Zbierz feedback** przez minimum 24 godziny

### 5.2 Staged Rollout (Optional)

Jeśli chcesz testować na %:
1. **Staged rollout** (zamiast Production)
2. **Start with**: 10%
3. **Monitor**: Crashlytics, ANR rate
4. Jeśli OK → Zwiększ do 100%

---

## Krok 6: Submission na Production

### 6.1 Finalna Kontrola

1. Sprawdź czy wszystko jest uzupełnione:
   - ✅ App listing (title, description, screenshots)
   - ✅ Content rating
   - ✅ Privacy policy
   - ✅ Pricing & distribution
   - ✅ Release APK podpisany

2. **Review** → Kliknij na każdą sekcję aby zatwierdzić

3. **Save** i **Submit for review**

### 6.2 Process Recenzji

- **Typowy czas**: 30 minut - 24 godziny
- **Automatyczna kontrola**: Malware, compatibility
- **Manualna kontrola**: Content, compliance
- **Notyfikacja**: Email na konto Google Play

### 6.3 Po Zatwierdzeniu

1. **Track release**: Obserwaj install count
2. **Monitor reviews**: Odpowiadaj na komentarze
3. **Analytics**: Sprawdzaj App Analytics
4. **Update planning**: Zbierz feedback na następną wersję

---

## Aktualizacje Aplikacji

### Procedura Update

1. Zaktualizuj `buildozer.spec`:
   ```ini
   version = 1.0.1  # Zwiększ numer wersji
   ```

2. Zbuduj nowy release APK:
   ```bash
   python build_apk.py --type release --clean
   ```

3. Podpisz APK (jeśli ręcznie):
   ```bash
   jarsigner -keystore workhours-release.jks bin/workhours-1.0.1-release.apk workhours
   ```

4. W Google Play Console:
   - **App releases** → **Production** → **Create release**
   - Upload nowy APK
   - Release notes (co się zmieniło)
   - Submit

---

## Bezpieczeństwo Keystore

⚠️ **WAŻNE**: Ochrona klucza do podpisywania

```bash
# Backup keystore (w bezpiecznym miejscu!)
cp workhours-release.jks /backup/workhours-release.jks

# Ustaw uprawnienia (Linux/Mac)
chmod 600 workhours-release.jks

# Nigdy nie commituj do Git!
echo "workhours-release.jks" >> .gitignore
```

---

## Monitoring & Support

### Google Play Analytics

1. **Google Play Console** → **Analytics**
2. Monitoruj:
   - Install count
   - Uninstall rate
   - Crash rate
   - ANR (Application Not Responding)

### User Reviews

1. **Ratings & reviews** section
2. Odpowiadaj na review'y:
   - Podziękuj za pozytywne
   - Rozwiąż problemy z negatywnymi
   - Update app jeśli jest dużo crash'y

### Next Version Planning

Na podstawie feedback'u:
- ✅ Poprawiaj bugs
- ✅ DodawajRequestedFeatures
- ✅ Ulepszaj UI/UX
- ✅ Optimizuj performance

---

## Timeline

| Krok | Czas |
|------|------|
| Przygotowanie keystore | 10 min |
| Build release APK | 10 min |
| Przygotowanie materiałów | 1-2 hours |
| Setup Google Play account | 30 min |
| Wgranie do testowania | 10 min |
| Internal testing | 24 hours |
| Submission | 5 min |
| Review Google Play | 30 min - 24 hours |
| **TOTAL** | **~30 hours** |

---

## Wsparcie

- [Google Play Console Help](https://support.google.com/googleplay/android-developer)
- [App signing requirements](https://developer.android.com/studio/publish/app-signing)
- [Buildozer release documentation](https://buildozer.readthedocs.io/)

---

## Następne Kroki

Po publicznym wdrożeniu:

1. **Market feedback collection**
2. **Version 1.1 planning** (user requests)
3. **Features pipeline**:
   - Cloud sync
   - Multiple languages
   - Widget
   - Notifications
   - Calendar integration

---

*Dokumentacja Phase 3.4 - Google Play Deployment*
*Last updated: 2026-02-04*
