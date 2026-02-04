# KOMPLETNA DOKUMENTACJA PROJEKTOWA
## Aplikacja mobilna Android (Python) – Ewidencja godzin pracy + raport PDF

---

## 1. Informacje ogólne

**Nazwa robocza:** WorkHours Purple

**Platforma:** Android

**Technologia:** Python (Kivy + KivyMD)

**Model aplikacji:** Offline-first, lokalna baza danych (SQLite)

**Grupa docelowa:** Użytkownik indywidualny (osoba niechętna ręcznemu liczeniu godzin, zapominająca o wpisach)

**Cel aplikacji:**
- szybkie i bezbłędne rejestrowanie godzin pracy,
- automatyczne liczenie czasu,
- generowanie miesięcznego raportu dla pracodawcy,
- eksport i druk raportu (PDF),
- maksymalnie prosta obsługa.

---

## 2. Zakres funkcjonalny (pełny)

### 2.1 Funkcje podstawowe (MUST)
- dodawanie / edycja wpisu dziennego,
- typ dnia: praca / urlop / chorobowe / święto / inne,
- automatyczne wyliczanie czasu brutto i netto,
- miesięczne podsumowania,
- przypomnienia o wpisie,
- generowanie raportu miesięcznego,
- eksport do PDF,
- udostępnianie PDF (mail, komunikatory, drukowanie).

### 2.2 Funkcje rozszerzone (SHOULD)
- szablony godzin pracy,
- podgląd wyliczeń „na żywo",
- walidacja błędów (czas, przerwa),
- eksport CSV,
- dane pracownika i pracodawcy.

### 2.3 Funkcje opcjonalne (COULD)
- wiele profili pracy,
- nadgodziny i stawki,
- backup/eksport danych.

---

## 3. Architektura techniczna

### 3.1 Stack technologiczny
- Python 3.x
- Kivy
- KivyMD (UI / theming)
- SQLite (sqlite3)
- ReportLab (PDF)
- Plyer (powiadomienia)
- PyJNIus (udostępnianie plików Android)
- Buildozer (pakowanie APK)

### 3.2 Struktura projektu

```
workhours_app/
  main.py
  app.kv
  buildozer.spec
  requirements.txt
  src/
    db.py
    models.py
    services/
      calc.py
      pdf_export.py
      share_android.py
      reminders.py
    ui/
      screens.py
      themes.py
  assets/
    icons/
    fonts/
```

---

## 4. Model danych (SQLite)

### 4.1 Tabela: work_entries

| Pole | Typ | Opis |
|----|----|----|
| id | INTEGER PK | ID wpisu |
| date | TEXT | YYYY-MM-DD (unikalne) |
| start_time | TEXT | HH:MM |
| end_time | TEXT | HH:MM |
| break_minutes | INTEGER | Przerwa w minutach |
| day_type | TEXT | work / vacation / sick / holiday / other |
| notes | TEXT | Notatka |
| created_at | TEXT | ISO |
| updated_at | TEXT | ISO |

### 4.2 Tabela: settings

| key | value |
|---|---|
| theme_id | 1–10 |
| default_start | HH:MM |
| default_end | HH:MM |
| default_break | int |
| reminder_enabled | bool |
| reminder_time | HH:MM |
| employee_name | text |
| employer_name | text |

---

## 5. Logika obliczeń

- Czas brutto = koniec – start
- Czas netto = brutto – przerwa
- Obsługa przejścia przez północ
- Brak czasu dla dni innych niż „praca"
- Miesięczne sumy w minutach i HH:MM

Walidacje:
- koniec >= start (lub +24h),
- przerwa <= czas brutto,
- brak wpisu oznaczony wizualnie.

---

## 6. UX / IA – Ekrany aplikacji

### 6.1 Dashboard (Miesiąc)
- status „dziś wpisane / brak wpisu",
- suma godzin miesięcznych (duża liczba),
- lista dni (karty),
- szybki przycisk „Dodaj dziś".

### 6.2 Dodaj / Edytuj dzień
- wybór daty,
- chipy typu dnia,
- start / koniec / przerwa (tylko praca),
- podgląd netto/brutto,
- zapis jednym przyciskiem.

### 6.3 Raport
- dane pracownika/pracodawcy,
- tabela dni,
- podsumowania,
- generuj PDF / udostępnij.

### 6.4 Ustawienia
- szablony godzin,
- przypomnienia,
- wybór motywu,
- dane raportowe.

---

## 7. Design system (globalny)

### 7.1 Założenia
- zaokrąglone krawędzie,
- żywe kolory,
- fiolet jako główny akcent,
- dark i light mode,
- maksymalna czytelność.

### 7.2 Zaokrąglenia
- karty: 22dp
- przyciski: 18dp
- chipy: pill (999dp)

---

## 8. System motywów – 10 wariantów

Każdy wariant definiuje tokeny:
- background
- surface
- surface2
- text
- muted
- primary
- accent
- success / warning / error

### Lista wariantów
1. Dark Purple Neon
2. Dark Grape Premium
3. Dark Electric Violet
4. Dark Plum + Gold
5. Light Clean Purple
6. Light Lavender Candy
7. Midnight Indigo
8. Graphite Purple
9. Purple + Lime Pop
10. Purple Sunset

Motyw wybierany w ustawieniach, zapisywany jako `theme_id`.

---

## 9. Raport PDF – specyfikacja

### Zawartość
- tytuł + miesiąc,
- dane pracownika i pracodawcy,
- tabela dni:
  - data, typ, start, koniec, przerwa, netto, notatka,
- podsumowanie:
  - suma godzin,
  - liczba dni pracy/urlopu/chorobowego,
- stopka + miejsce na podpis.

### Technika
- generowanie lokalne (ReportLab),
- zapis do pliku,
- udostępnianie przez Android Intent,
- druk przez systemowy viewer PDF.

---

## 10. Przypomnienia

- dzienne powiadomienie (domyślnie 19:00),
- klik → ekran „Dodaj dziś",
- możliwość wyłączenia.

---

## 11. Build i dystrybucja

- Buildozer
- APK / AAB
- minimalne uprawnienia
- aplikacja offline

---

## 12. Roadmapa

### MVP 1.0
- wpisy dzienne
- dashboard
- PDF
- przypomnienia

### 1.1
- CSV
- szablony

### 1.2
- profile
- nadgodziny

---

## 13. Status dokumentu

Dokument kompletny, gotowy do przekazania zespołowi / AI technicznej.

Zakres zamknięty – implementacja bez decyzji projektowych.

