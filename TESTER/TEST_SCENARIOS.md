╔═══════════════════════════════════════════════════════════════════════════╗
║              WORKHOURSAPP - SCENARIUSZE TESTOWE (UX/UI/Funkcje)          ║
║                                                                           ║
║  Kompletne przypadki testowe do ręcznego testowania aplikacji            ║
║  jako użytkownik na urządzeniu rzeczywistym lub emulatorze               ║
║                                                                           ║
║  Data: 4 lutego 2026                                                     ║
║  Wersja: 1.0.0 (MVP)                                                     ║
╚═══════════════════════════════════════════════════════════════════════════╝

# SPIS SCENARIUSZY

1. [Scenariusze Podstawowe](#scenariusze-podstawowe)
2. [Scenariusze Dodawania Wpisów](#scenariusze-dodawania-wpisów)
3. [Scenariusze Edycji i Usuwania](#scenariusze-edycji-i-usuwania)
4. [Scenariusze Raportów](#scenariusze-raportów)
5. [Scenariusze Profili](#scenariusze-profili)
6. [Scenariusze Motywów](#scenariusze-motywów)
7. [Scenariusze Wydajności](#scenariusze-wydajności)
8. [Scenariusze Bezpieczeństwa](#scenariusze-bezpieczeństwa)
9. [Scenariusze Brzegowe](#scenariusze-brzegowe)
10. [Scenariusze Integracyjne](#scenariusze-integracyjne)

═══════════════════════════════════════════════════════════════════════════

# SCENARIUSZE PODSTAWOWE

## TC-001: Uruchomienie Aplikacji (First Launch)

**Kroki:**
```
1. Naciśnij ikonę aplikacji WorkHours na ekranie głównym
2. Czekaj na załadowanie (maksymalnie 3 sekundy)
3. Obserwuj ekran powitalny
```

**Oczekiwane Wyniki:**
```
✓ Aplikacja otwiera się bez błędów
✓ Wyświetlany jest ekran powitania
✓ Menu główne jest widoczne
✓ Wszystkie przyciski są responsywne
✓ Teksty są czytelne
```

**Kryteria Zdzenia:**
```
✗ Crash/zamrożenie
✗ Widoczne lagi lub opóźnienia
✗ Zniekształcone ikony/tekst
✗ Niewidoczne przyciski
```

---

## TC-002: Nawigacja Menu Głównego

**Kroki:**
```
1. Na ekranie głównym obserwuj dostępne karty:
   - ➕ Dodaj Wpis
   - 📋 Wpisy
   - 📊 Raport
   - 👤 Profile
   - 🎨 Motywy
   - 🗄️ Baza
2. Kliknij na każdą kartę
3. Sprawdź czy zawartość się zmienia
4. Wróć do każdej karty
```

**Oczekiwane Wyniki:**
```
✓ Wszystkie karty są dostępne
✓ Kliknięcie zmienia zawartość
✓ Przejścia są płynne (animacje)
✓ Dane się nie zmieniają przy przełączaniu
✓ Wszystkie przyciski mogą być naciśnięte
```

**Kryteria Zdzenia:**
```
✗ Brakujące karty
✗ Zawartość się nie zmienia
✗ Wielkie opóźnienia (>1s)
✗ Crash przy przełączaniu
```

═══════════════════════════════════════════════════════════════════════════

# SCENARIUSZE DODAWANIA WPISÓW

## TC-003: Dodaj Wpis - Standardowy Dzień Roboczy

**Kroki:**
```
1. Otwórz kartę "➕ Dodaj Wpis"
2. Wprowadź dane:
   - Data: 2026-02-04
   - Start: 09:00
   - Koniec: 17:00
   - Przerwa: 30 (minut)
   - Typ: work_day
   - Notatka: "Normalna jornada pracy"
3. Kliknij "💾 Zapisz Wpis"
4. Obserwuj komunikat
5. Przejdź do karty "📋 Wpisy"
```

**Oczekiwane Wyniki:**
```
✓ Wpis zostaje zapisany
✓ Wyświetlany jest komunikat potwierdzenia: "✓ Wpis zapisany!"
✓ Wyświetlana jest suma czasu: "Czas netto: 07:30 (7.50h)"
✓ Forma jest czyszczona automatycznie
✓ Wpis pojawia się w liście wpisów
✓ Znowu można dodać następny wpis
```

**Kryteria Zdzenia:**
```
✗ Wpis się nie zapisuje
✗ Brak komunikatu potwierdzenia
✗ Forma nie oczyszcza się
✗ Wpis nie pojawia się w liście
✗ Błędne obliczanie czasu
```

---

## TC-004: Dodaj Wpis - Przekroczenie Północy

**Kroki:**
```
1. Otwórz kartę "➕ Dodaj Wpis"
2. Wprowadź:
   - Data: 2026-02-03
   - Start: 22:00
   - Koniec: 06:00 (następnego dnia!)
   - Przerwa: 0
   - Typ: work_day
3. Kliknij "💾 Zapisz Wpis"
4. Sprawdź wynik
```

**Oczekiewane Wyniki:**
```
✓ System rozpoznaje przekroczenie północy
✓ Czas netto: 08:00 (8.00h) - prawidłowy
✓ Wpis zostaje zapisany bez błędu
✓ Komunikat: "✓ Wpis zapisany!"
```

**Kryteria Zdzenia:**
```
✗ Błędne obliczenie czasu
✗ Ujemny czas
✗ Błąd przy zapisie
✗ System mylnie traktuje jako błąd
```

---

## TC-005: Dodaj Wpis - Dzień Chorobowy

**Kroki:**
```
1. Otwórz kartę "➕ Dodaj Wpis"
2. Wprowadź:
   - Data: 2026-02-05
   - Start: --:-- (zostawić puste)
   - Koniec: --:-- (zostawić puste)
   - Typ: sick_day
3. Kliknij "💾 Zapisz Wpis"
4. Sprawdź raport
```

**Oczekiewane Wyniki:**
```
✓ System pozwala na puste pola godzin
✓ Wpis zostaje zapisany
✓ Czas netto: 00:00
✓ Raport pokazuje: "Dni chorobowe: 1"
✓ Nie liczy się do sumy czasu
```

**Kryteria Zdzenia:**
```
✗ Wymuszanie godzin dla boldays
✗ Błąd walidacji
✗ Przysłony do godzin pracy
```

---

## TC-006: Dodaj Wpis - Walidacja Błędów

**Kroki:**
```
1. Otwórz kartę "➕ Dodaj Wpis"
2. Test 1: Zła data
   - Data: 2026-13-45
   - Kliknij Zapisz
3. Test 2: Zła godzina
   - Data: 2026-02-04
   - Start: 25:99
   - Kliknij Zapisz
4. Test 3: Przerwa dłuższa niż praca
   - Data: 2026-02-04
   - Start: 09:00
   - Koniec: 10:00
   - Przerwa: 120
   - Kliknij Zapisz
```

**Oczekiewane Wyniki:**
```
✓ Błąd daty: "✗ Nieprawidłowy format daty (użyj YYYY-MM-DD)"
✓ Błąd godziny: "✗ Nieprawidłowy format czasu (użyj HH:MM)"
✓ Błąd przerwy: "✗ Przerwa nie może być dłuższa niż czas pracy"
✓ Wpis się nie zapisuje
✓ Forma nie jest czyszczona
```

**Kryteria Zdzenia:**
```
✗ Brak komunikatu błędu
✗ Wpis się zapisuje mimo błędu
✓ Niejasny komunikat błędu
```

═══════════════════════════════════════════════════════════════════════════

# SCENARIUSZE RAPORTÓW

## TC-007: Generowanie Raportu Miesięcznego

**Kroki:**
```
1. Dodaj kilka wpisów dla bieżącego miesiąca (TC-003)
2. Otwórz kartę "📊 Raport"
3. Ustaw:
   - Miesiąc: 02
   - Rok: 2026
4. Kliknij "📊 Generuj"
5. Obserwuj raport
```

**Oczekiewane Wyniki:**
```
✓ Raport się wyświetla
✓ Tytuł: "Raport za 02/2026"
✓ Wyświetlane są sumy (netto, brutto)
✓ Wyświetlana jest statystyka dni
✓ Pokazane są szczegóły wpisów
✓ Wszystkie liczby są prawidłowe
```

**Kryteria Zdzenia:**
```
✗ Raport się nie wyświetla
✗ Błędne sumy
✗ Brakujące dane
✗ Nieczytelny format
```

---

## TC-008: Generowanie PDF Raportu

**Kroki:**
```
1. Powtórz TC-007 (wygeneruj raport)
2. Kliknij "📄 Pobierz PDF"
3. Czekaj na generowanie (10-30 sekund)
4. Obserwuj komunikat
5. Przejdź do menedżera plików
6. Sprawdź folder: TESTER/reports/
7. Otwórz plik PDF
```

**Oczekiewane Wyniki:**
```
✓ Komunikat: "✓ PDF zapisany! [ścieżka]"
✓ Plik jest tworzony
✓ Nazwa: "Default_2026_02_report.pdf"
✓ Plik zawiera prawidłowe dane
✓ PDF można otworzyć
✓ Formatowanie jest czytelne
```

**Kryteria Zdzenia:**
```
✗ Błąd generowania
✗ Plik się nie tworzy
✗ PDF jest uszkodzony
✗ Brakujące dane w PDF
```

═══════════════════════════════════════════════════════════════════════════

# SCENARIUSZE PROFILI

## TC-009: Zarządzanie Profilami - Nowy Profil

**Kroki:**
```
1. Otwórz kartę "👤 Profile"
2. Wpisz: "Anna Kowalski"
3. Kliknij "➕ Nowy"
4. Obserwuj listę
```

**Oczekiewane Wyniki:**
```
✓ Nowy profil pojawia się na liście
✓ Wyświetlana nazwa: "👤 Anna Kowalski"
✓ Profil jest zaznaczony/aktywny
✓ Można kliknąć na profil
✓ Przełączenie do nowego profilu nie uszkadza starych danych
```

**Kryteria Zdzenia:**
```
✗ Profil się nie tworzy
✗ Błąd duplikacji (jeśli ta sama nazwa)
✗ Stare wpisy się skasują
✗ Profil niedostępny
```

---

## TC-010: Izolacja Danych Między Profilami

**Kroki:**
```
1. Masz profil "Default Tester" z wpisem (TC-003)
2. Stwórz nowy profil "Test Profile 2"
3. Przełącz do nowego profilu
4. Otwórz kartę "📋 Wpisy"
5. Obserwuj listę
6. Przełącz z powrotem na "Default Tester"
7. Sprawdź listę wpisów
```

**Oczekiewane Wyniki:**
```
✓ "Test Profile 2": Brak wpisów (pusta lista)
✓ "Default Tester": Wszystkie wpisy z TC-003 są tutaj
✓ Dane każdego profilu są całkowicie izolowane
✓ Przełączanie nie usuwa danych
```

**Kryteria Zdzenia:**
```
✗ Wpisy są współdzielone między profilami
✗ Dane się mieszają
✗ Usunięcie profilu kasuje dane innego
```

═══════════════════════════════════════════════════════════════════════════

# SCENARIUSZE MOTYWÓW

## TC-011: Zmiana Motywu - Opcja A (Hardcoded)

**Kroki:**
```
1. Otwórz kartę "🎨 Motywy"
2. Obserwuj listę dostępnych motywów (1-10)
3. Skopiuj ID motywu: "2"
4. Wklej do pola "ID motywu (1-10)"
5. Kliknij "🎨 Zastosuj"
6. Obserwuj zmianę kolorów
```

**Oczekiewane Wyniki:**
```
✓ Wyświetlana lista 10 motywów:
  1. Dark Purple Neon
  2. Dark Grape Premium
  3. Dark Electric Violet
  ... itd.
✓ Kolory zmieniają się (animacja fade)
✓ Motyw jest zapamiętywany
✓ Kolory są odświeżone na całej aplikacji
```

**Kryteria Zdzenia:**
```
✗ Motyw się nie zmienia
✗ Brakujące motywy
✗ Nieudana animacja
✗ Kolory nie odświeżają się wszędzie
```

---

## TC-012: Przejście Między Motywami z Animacją

**Kroki:**
```
1. Ustaw motyw #1 (Dark Purple Neon)
2. Czekaj 2 sekundy
3. Ustaw motyw #5 (Light Clean Purple)
4. Obserwuj przejście
```

**Oczekiewane Wyniki:**
```
✓ Płynna animacja fade:
  - Fade out (0.25s)
  - Zmiana koloru
  - Fade in (0.25s)
✓ Brak flashu/migotania
✓ Całkowity czas: ~0.5s
✓ Kolory ciemne → jasne
```

**Kryteria Zdzenia:**
```
✗ Błysk/migotanie
✗ Natychmiastowa zmiana bez animacji
✗ Animacja trwa >1s
✗ Glitche graficzne
```

═══════════════════════════════════════════════════════════════════════════

# SCENARIUSZE WYDAJNOŚCI

## TC-013: Wydajność przy 100 Wpisach

**Kroki:**
```
1. Pobierz script: TESTER/scripts/bulk_insert_entries.py
2. Uruchom: python bulk_insert_entries.py --count 100
3. Otwórz aplikację
4. Otwórz kartę "📋 Wpisy"
5. Obserwuj opóźnienia
6. Scroll w górę i dół
7. Genreruj raport
```

**Oczekiewane Wyniki:**
```
✓ Ładowanie listy: <1s
✓ Scrolling: płynny (60fps)
✓ Raport generuje się: <5s
✓ Brak crash'u
✓ Brak zawieszenia UI
```

**Kryteria Zdzenia:**
```
✗ Ładowanie >3s
✗ Lagi przy scrollingu
✗ Raport >10s
✗ Crash/OOM
```

---

## TC-014: Użycie Pamięci

**Kroki:**
```
1. Dodaj 50 wpisów
2. Otwórz Ustawienia Telefonu → Aplikacje → WorkHours
3. Obserwuj "Zużywana pamięć"
4. Przełączaj między kartami
5. Sprawdzaj pamięć co 30 sekund
6. Poczekaj 2 minuty bez działania
```

**Oczekiewane Wyniki:**
```
✓ Pamięć: 20-50 MB (zależy od urządzenia)
✓ Brak crescendoącego wzrostu
✓ Garbage collection pracuje
✓ Po 2 minutach: pamięć się zmniejsza
```

**Kryteria Zdzenia:**
```
✗ Pamięć >100 MB
✗ Ciągy wzrost bez limitu
✗ Leak pamięci
```

═══════════════════════════════════════════════════════════════════════════

# SCENARIUSZE BEZPIECZEŃSTWA

## TC-015: Izolacja Danych - Folder Prywatny

**Kroki:**
```
1. Dodaj sensytywne notatki: "Zarobki: 5000 PLN"
2. Podłącz telefon do PC
3. Otwórz menedżer plików na PC
4. Przejdź do: Android/data/
5. Spróbuj znaleźć folder aplikacji
6. Spróbuj odczytać pliki
```

**Oczekiewane Wyniki:**
```
✓ Folder aplikacji: Android/data/org.workhours/
✓ Dane są w: files/databases/
✓ Nie można czytać bez uprawnień root
✓ Bezpieczne przechowywanie
```

**Kryteria Zdzenia:**
```
✗ Dane w /sdcard/ (publicznie dostępne)
✗ Brak szyfrowania
✗ Mogą być odczytane bez uprawnień
```

---

## TC-016: Uprawnienia - Zapis PDF

**Kroki:**
```
1. Wygeneruj raport i PDF (TC-008)
2. Poczekaj na komunikat
3. Otwórz Menedżer Plików
4. Przejdź do: TESTER/reports/
5. Sprawdź czy plik istnieje
6. Spróbuj go otworzyć
```

**Oczekiewane Wyniki:**
```
✓ Plik jest tworzony w prawidłowej lokalizacji
✓ Uprawnienia są ustawione prawidłowo
✓ Można go otworzyć/przenieść
✓ Nie ma "Permission Denied"
```

**Kryteria Zdzenia:**
```
✗ Błąd uprawnień
✗ Plik nie zapisuje się
✗ Błąd dostępu
```

═══════════════════════════════════════════════════════════════════════════

# SCENARIUSZE BRZEGOWE (EDGE CASES)

## TC-017: Bardzo Długie Notatki

**Kroki:**
```
1. Dodaj wpis z notatką:
   - Długa notatka: 1000+ znaków
   - Zawiera znaki specjalne: @#$%^&*()
   - Zawiera Polskie znaki: ąćęłńóśźż
2. Zapisz
3. Sprawdź w liście wpisów
4. Sprawdź w raporcie
```

**Oczekiewane Wyniki:**
```
✓ Notatka się zapisuje
✓ Bez błędu Unicode
✓ Wszystkie znaki są zachowane
✓ W raporcie wyświetla się prawidłowo (obcięta lub z scrollem)
```

**Kryteria Zdzenia:**
```
✗ Crash
✗ Utrata znaków
✗ Nieczytelne znaki
✗ Przepełnienie layout'u
```

---

## TC-018: Granice Czasowe

**Kroki:**
```
1. Test 1: Minimum czasu pracy
   - Start: 00:00
   - Koniec: 00:01
   - Oczekiwane: 00:01 (1 minuta)

2. Test 2: Maximum czasu pracy
   - Start: 00:00
   - Koniec: 23:59
   - Oczekiwane: 23:59

3. Test 3: Zero czasu pracy
   - Start: 09:00
   - Koniec: 09:00
   - Oczekiwane: 00:00

4. Test 4: Cała noc (koło północy)
   - Start: 23:00
   - Koniec: 01:00
   - Oczekiwane: 02:00
```

**Oczekiewane Wyniki:**
```
✓ Wszystkie obliczenia prawidłowe
✓ Brak błędów
✓ Wszystkie wpisy się zapisują
```

**Kryteria Zdzenia:**
```
✗ Błędne obliczenia
✗ Ujemne czasy
✗ Crash
```

═══════════════════════════════════════════════════════════════════════════

# SCENARIUSZE INTEGRACYJNE

## TC-019: Pełny Cykl Użytkowania - Tydzień

**Kroki:**
```
Tydzień testowy: 3-7 lutego 2026

Poniedziałek (3.02):
  1. Dodaj: 09:00 - 17:00 (8h)
  2. Notatka: "Normalna praca"

Wtorek (4.02):
  1. Dodaj: 08:00 - 16:00 (7h, przerwa 30min)
  2. Notatka: "Wcześnie się skończyło"

Środa (5.02):
  1. Dni chorobowy

Czwartek (6.02):
  1. Dodaj: 09:00 - 18:00 (8h, przerwa 1h)
  2. Notatka: "Dłuższy dzień"

Piątek (7.02):
  1. Dodaj: 10:00 - 18:00 (7h, przerwa 30min)
  2. Notatka: "Przesunięte godziny"

Po każdym dniu:
  - Przejrzyj wpisy
  - Sprawdź raport
  - Zmień motyw

Na koniec:
  - Genjeruj raport dla całego tygodnia
  - Sprawdź PDF
```

**Oczekiewane Wyniki:**
```
✓ Wszystkie wpisy się zapisują
✓ Raport pokazuje: 30h pracy, 1 dzień chorobowy
✓ Średnia dzienna: 6h
✓ PDF zawiera wszystkie dane
✓ Brak błędów/crash'ów
✓ Aplikacja pracuje stabilnie przez cały tydzień
```

---

## TC-020: Import/Export Danych

**Kroki:**
```
1. Dodaj kilka wpisów
2. Otwórz kartę "🗄️ Baza"
3. Kliknij "💾 Eksportuj do JSON"
4. Czekaj na operację
5. Przejdź do Menedżera Plików
6. Otwórz: TESTER/export_data.json
7. Obserwuj strukturę JSON
```

**Oczekiewane Wyniki:**
```
✓ Plik JSON jest tworzony
✓ Zawiera strukturę:
  - profiles: []
  - entries: []
  - themes: []
✓ Wszystkie dane są zachowane
✓ JSON jest prawidłowy (otwarty editor JSON)
```

═══════════════════════════════════════════════════════════════════════════

# CHECKLIST TESTOWANIA

## Przed Publikacją Aplikacji

```
FUNKCJONALNOŚĆ
 □ Dodawanie wpisów (TC-003 do TC-006)
 □ Przeglądanie wpisów (TC-007)
 □ Generowanie raportów (TC-007, TC-008)
 □ Zarządzanie profilami (TC-009, TC-010)
 □ System motywów (TC-011, TC-012)
 □ Izolacja danych (TC-010)

WYDAJNOŚĆ
 □ 100 wpisów (TC-013)
 □ Użycie RAM (TC-014)
 □ Ładowanie <1s (TC-013)
 □ Scrolling płynny (TC-013)

BEZPIECZEŃSTWO
 □ Prywatne folder (TC-015)
 □ Uprawnienia (TC-016)
 □ Izolacja profilów (TC-010)

STABILNOŚĆ
 □ Pełny tydzień (TC-019)
 □ 50+ wpisów (TC-013)
 □ Powielone przełączanie (TC-011, TC-012)
 □ Brak crash'ów

WALIDACJA
 □ Wszystkie błędy testowe (TC-006)
 □ Brzegowe przypadki (TC-017, TC-018)
 □ Wejścia obcojęzyczne (TC-017)

UI/UX
 □ Responsywność (wszystkie TC)
 □ Czytelność (wszystkie TC)
 □ Animacje (TC-012)
 □ Kolory/Kontrast

DOKUMENTACJA
 □ Instrukcje są jasne
 □ Instalacja działa
 □ Troubleshooting jest pomocny
```

═══════════════════════════════════════════════════════════════════════════

# RAPORTOWANIE BŁĘDÓW

## Format Zgłoszenia Błędu

```
TYTUŁ: [Krótki opis problemu]

KROKI DO REPRODUKCJI:
1. [Krok 1]
2. [Krok 2]
3. [Krok 3]

OCZEKIWANE ZACHOWANIE:
[Co powinno się stać]

RZECZYWISTE ZACHOWANIE:
[Co się faktycznie stało]

SCREENSHOT/WIDEO:
[Zdjęcie lub nagranie ekranu]

ŚRODOWISKO:
- Urządzenie: [np. Samsung Galaxy S22 Pro]
- Android: [np. 16]
- Wersja aplikacji: [np. 1.0.0]
- Kroki dla raportu: [TC-XXX]

PRIORYTET:
□ Krytyczny (Crash, utrata danych)
□ Wysoki (Funkcja nie działa)
□ Średni (Drobne błędy)
□ Niski (Kosmetyka)
```

═══════════════════════════════════════════════════════════════════════════

**Powodzenia w testowaniu! Każdy test przyspiesza stabilizację aplikacji.**

Ostatnia aktualizacja: 4 lutego 2026
