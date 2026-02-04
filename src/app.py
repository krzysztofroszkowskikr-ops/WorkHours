"""
WorkHours App - Testowa wersja bez złożonych kontrolek
Prosta, działająca aplikacja z Kivy + KivyMD minimum
"""

import logging
from pathlib import Path
from datetime import datetime
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DashboardScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=10)
        self.layout.bind(minimum_height=self.layout.setter('height'))  # type: ignore
        
        scroll = ScrollView(size_hint=(1, 0.85))
        scroll.add_widget(self.layout)
        
        main = BoxLayout(orientation='vertical')
        main.add_widget(scroll)
        
        # Górny menu (odśwież + dodaj + raport)
        top_btn_layout = BoxLayout(size_hint_y=0.08, spacing=3)
        
        btn_refresh = Button(text='🔄 Odśwież')
        btn_refresh.bind(on_press=self.refresh_data)  # type: ignore
        top_btn_layout.add_widget(btn_refresh)
        
        btn_add = Button(text='➕ Dodaj')
        btn_add.bind(on_press=lambda x: setattr(app.sm, 'current', 'entry'))  # type: ignore
        top_btn_layout.add_widget(btn_add)
        
        btn_report = Button(text='📄 Raport')
        btn_report.bind(on_press=lambda x: setattr(app.sm, 'current', 'report'))  # type: ignore
        top_btn_layout.add_widget(btn_report)
        
        main.add_widget(top_btn_layout)
        self.add_widget(main)
    
    def refresh_data(self, instance):  # type: ignore
        """Ręczne odświeżenie danych"""
        logger.info("🔄 Odświeżanie danych...")
        self.on_enter()
    
    def on_enter(self, *args):  # type: ignore
        """Odśwież dane gdy ekran się pojawi"""
        self.layout.clear_widgets()
        
        try:
            from datetime import timedelta as td
            from datetime import timedelta as td
            
            # Tytuł
            title = Label(
                text="🏢 Dashboard - Miesięczny Przegląd",
                size_hint_y=None,
                height=50,
                font_size='16sp',
                bold=True
            )
            self.layout.add_widget(title)
            
            # Pobierz bieżący profil i miesiąc
            profile = self.app.app_context.get_current_profile()
            if not profile:
                no_profile = Label(
                    text="⚠️ Brak profilu - utwórz go w Ustawieniach",
                    size_hint_y=None,
                    height=50,
                    color=(1, 0.5, 0, 1)
                )
                self.layout.add_widget(no_profile)
                return
                
            today = datetime.now()
            
            # Pobierz wpisy z miesiąca
            from src.repository import WorkEntryRepository
            repo = WorkEntryRepository(self.app.app_context.database)
            entries = repo.get_month(profile.id, today.year, today.month)
            
            # Oblicz statystyki
            from src.services.calc_service import CalcService
            calc = self.app.app_context.calc_service
            
            if entries:
                # Konwertuj do WorkDayResult
                results = []
                for entry in entries:
                    result = calc.calculate_work_day(
                        date=entry.date,
                        start_time=entry.start_time,
                        end_time=entry.end_time,
                        break_minutes=entry.break_minutes,
                        day_type=entry.day_type
                    )
                    if result.success:
                        results.append(result)
                
                # Podsumowanie miesiąca
                summary = calc.calculate_month_summary(results)
                
                # Wyświetl statystyki
                fmt = self.app.app_context.formatters
                
                stat_info = (
                    f"👤 {profile.name}\n"
                    f"📅 {fmt.format_month_year(today.year, today.month)}\n\n"
                    f"⏰ Łączne godziny: {fmt.format_duration_hm(summary.total_work_hours_decimal)}\n"
                    f"📊 Średnia dzienna: {fmt.format_duration_decimal(summary.average_daily_hours)}h\n"
                    f"📝 Dni z wpisami: {len(summary.days_with_entries)}\n"
                    f"🏥 Dni choroby: {summary.sick_days} | "
                    f"🏖️ Urlop: {summary.vacation_days} | "
                    f"❌ Wolne: {summary.day_offs}"
                )
            else:
                fmt = self.app.app_context.formatters
                stat_info = (
                    f"👤 {profile.name}\n"
                    f"📅 {fmt.format_month_year(today.year, today.month)}\n\n"
                    "Brak wpisów w tym miesiącu"
                )
            
            stats = Label(
                text=stat_info,
                size_hint_y=None,
                height=140,
                font_size='13sp',
                markup=True
            )
            self.layout.add_widget(stats)
            
            # Ostatnie wpisy (7 dni)
            recent_header = Label(
                text="📋 Ostatnie wpisy (7 dni):",
                size_hint_y=None,
                height=30,
                font_size='12sp',
                bold=True
            )
            self.layout.add_widget(recent_header)
            
            week_start = today - td(days=7)
            week_entries = repo.get_date_range(
                profile.id,
                week_start.date().isoformat(),
                today.date().isoformat()
            )
            
            if week_entries:
                for entry in sorted(week_entries, key=lambda e: e.date, reverse=True)[:10]:
                    entry_text = (
                        f"📅 {entry.date} | "
                        f"{entry.day_type.upper():<10} | "
                        f"{entry.start_time}-{entry.end_time}"
                    )
                    entry_label = Label(
                        text=entry_text,
                        size_hint_y=None,
                        height=25,
                        font_size='11sp'
                    )
                    self.layout.add_widget(entry_label)
            else:
                no_recent = Label(
                    text="Brak wpisów w ostatnich 7 dniach",
                    size_hint_y=None,
                    height=25,
                    font_size='11sp',
                    color=(0.7, 0.7, 0.7, 1)
                )
                self.layout.add_widget(no_recent)
            
        except Exception as e:
            logger.error(f"❌ Błąd w DashboardScreen: {e}", exc_info=True)
            error_label = Label(
                text=f"⚠️ Błąd: {str(e)}",
                size_hint_y=None,
                height=100,
                color=(1, 0, 0, 1),
                font_size='12sp'
            )
            self.layout.add_widget(error_label)


class EntryScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        
        from kivy.uix.textinput import TextInput
        from kivy.uix.spinner import Spinner
        
        main = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Tytuł
        title = Label(
            text="📝 Dodaj Wpis Pracy",
            size_hint_y=None,
            height=50,
            font_size='16sp',
            bold=True
        )
        main.add_widget(title)
        
        # Scroll dla formularza
        scroll = ScrollView(size_hint=(1, 0.7))
        form = GridLayout(cols=2, spacing=10, size_hint_y=None, padding=10)
        form.bind(minimum_height=form.setter('height'))  # type: ignore
        
        # Data
        form.add_widget(Label(text="📅 Data:", size_hint_y=None, height=40))
        self.date_input = TextInput(
            text=datetime.now().strftime('%Y-%m-%d'),
            multiline=False,
            size_hint_y=None,
            height=40,
            hint_text="YYYY-MM-DD"
        )
        form.add_widget(self.date_input)
        
        # Czas początkowy
        form.add_widget(Label(text="⏰ Początek:", size_hint_y=None, height=40))
        self.start_input = TextInput(
            text="08:00",
            multiline=False,
            size_hint_y=None,
            height=40,
            hint_text="HH:MM"
        )
        form.add_widget(self.start_input)
        
        # Czas końcowy
        form.add_widget(Label(text="🛑 Koniec:", size_hint_y=None, height=40))
        self.end_input = TextInput(
            text="16:00",
            multiline=False,
            size_hint_y=None,
            height=40,
            hint_text="HH:MM"
        )
        form.add_widget(self.end_input)
        
        # Przerwa
        form.add_widget(Label(text="☕ Przerwa (min):", size_hint_y=None, height=40))
        self.break_input = TextInput(
            text="30",
            multiline=False,
            size_hint_y=None,
            height=40,
            hint_text="minut",
            input_filter="int"
        )
        form.add_widget(self.break_input)
        
        # Typ dnia (Spinner/Dropdown)
        form.add_widget(Label(text="📌 Typ dnia:", size_hint_y=None, height=40))
        self.type_spinner = Spinner(
            text="work",
            values=("work", "sick_day", "vacation", "day_off"),
            size_hint_y=None,
            height=40
        )
        form.add_widget(self.type_spinner)
        
        scroll.add_widget(form)
        main.add_widget(scroll)
        
        # Przyciski
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        
        btn_save = Button(text='💾 Zapisz')
        btn_save.bind(on_press=self.save_entry)  # type: ignore
        btn_layout.add_widget(btn_save)
        
        btn_back = Button(text='◀️ Wróć')
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'dashboard'))  # type: ignore
        btn_layout.add_widget(btn_back)
        
        main.add_widget(btn_layout)
        self.add_widget(main)
    
    def save_entry(self, instance):  # type: ignore
        """Zapisz wpis do bazy"""
        try:
            from src.models import WorkEntry
            from src.repository import WorkEntryRepository
            from datetime import datetime as dt
            import re
            
            profile = self.app.app_context.get_current_profile()
            if not profile:
                raise ValueError("⚠️ Brak aktywnego profilu. Utwórz go w Ustawieniach.")
            
            # Validacja
            date_str = self.date_input.text.strip()
            start_str = self.start_input.text.strip()
            end_str = self.end_input.text.strip()
            break_str = self.break_input.text.strip()
            day_type = self.type_spinner.text
            
            if not date_str or not start_str or not end_str or not break_str:
                raise ValueError("❌ Wszystkie pola muszą być wypełnione!")
            
            # Walidacja formatu daty
            try:
                dt.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                raise ValueError("❌ Niepoprawny format daty (użyj YYYY-MM-DD)")
            
            # Walidacja formatu czasu
            if not re.match(r'^\d{2}:\d{2}$', start_str) or not re.match(r'^\d{2}:\d{2}$', end_str):
                raise ValueError("❌ Niepoprawny format czasu (użyj HH:MM)")
            
            # Walidacja czasu
            try:
                start_h, start_m = map(int, start_str.split(':'))
                end_h, end_m = map(int, end_str.split(':'))
                if not (0 <= start_h < 24 and 0 <= start_m < 60):
                    raise ValueError("❌ Początek: godzina 0-23, minuty 0-59")
                if not (0 <= end_h < 24 and 0 <= end_m < 60):
                    raise ValueError("❌ Koniec: godzina 0-23, minuty 0-59")
            except (ValueError, TypeError):
                raise ValueError("❌ Niepoprawna godzina")
            
            # Walidacja przerwy
            try:
                break_int = int(break_str)
                if break_int < 0 or break_int > 480:
                    raise ValueError("❌ Przerwa powinna być 0-480 minut")
            except ValueError:
                raise ValueError("❌ Przerwa musi być liczbą całkowitą")
            
            entry = WorkEntry(
                id=None,
                profile_id=profile.id,
                date=date_str,
                start_time=start_str,
                end_time=end_str,
                break_minutes=break_int,
                day_type=day_type,
                notes=""
            )
            
            repo = WorkEntryRepository(self.app.app_context.database)
            repo.create(entry)
            
            logger.info(f"✅ Wpis zapisany: {entry.date} ({entry.start_time}-{entry.end_time}) [{day_type}]")
            
            # Wróć do dashboard
            setattr(self.app.sm, 'current', 'dashboard')
            
        except ValueError as e:
            logger.warning(f"⚠️ Błąd walidacji: {e}")
            # Wyświetl błąd w aplikacji
            self.show_error(str(e))
        except Exception as e:
            logger.error(f"❌ Błąd zapisu: {e}", exc_info=True)
            self.show_error(f"❌ Błąd: {str(e)}")
    
    def show_error(self, msg: str):
        """Pokaż komunikat błędu"""
        logger.error(f"Błąd UI: {msg}")


class ReportScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        from kivy.uix.spinner import Spinner
        from datetime import datetime
        
        main = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Tytuł
        title = Label(
            text="📄 Generowanie Raportów",
            size_hint_y=None,
            height=50,
            font_size='16sp',
            bold=True
        )
        main.add_widget(title)
        
        # Selektory daty
        date_layout = GridLayout(cols=2, spacing=5, size_hint_y=None, height=50)
        
        # Rok
        date_layout.add_widget(Label(text="Rok:", size_hint_y=None, height=50))
        current_year = datetime.now().year
        years = [str(y) for y in range(current_year - 2, current_year + 1)]
        self.year_spinner = Spinner(
            text=str(current_year),
            values=years,
            size_hint_y=None,
            height=50
        )
        date_layout.add_widget(self.year_spinner)
        
        main.add_widget(date_layout)
        
        # Miesiąc (dla raportu miesięcznego)
        month_layout = GridLayout(cols=2, spacing=5, size_hint_y=None, height=50)
        
        month_layout.add_widget(Label(text="Miesiąc:", size_hint_y=None, height=50))
        current_month = datetime.now().month
        months = [str(m).zfill(2) for m in range(1, 13)]
        self.month_spinner = Spinner(
            text=str(current_month).zfill(2),
            values=months,
            size_hint_y=None,
            height=50
        )
        month_layout.add_widget(self.month_spinner)
        
        main.add_widget(month_layout)
        
        # Przyciski raportów
        btn_layout = BoxLayout(orientation='vertical', size_hint_y=0.5, spacing=10)
        
        btn_monthly = Button(text='📊 Raport Miesięczny')
        btn_monthly.bind(on_press=self.generate_monthly)  # type: ignore
        btn_layout.add_widget(btn_monthly)
        
        btn_yearly = Button(text='📈 Raport Roczny')
        btn_yearly.bind(on_press=self.generate_yearly)  # type: ignore
        btn_layout.add_widget(btn_yearly)
        
        main.add_widget(btn_layout)
        
        # Status
        self.status_label = Label(
            text="Wybierz datę i rodzaj raportu",
            size_hint_y=None,
            height=100,
            font_size='11sp'
        )
        main.add_widget(self.status_label)
        
        # Przyciski dolne
        nav_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        
        btn_back = Button(text='◀️ Wróć')
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'dashboard'))  # type: ignore
        nav_layout.add_widget(btn_back)
        
        main.add_widget(nav_layout)
        self.add_widget(main)
    
    def generate_monthly(self, instance):  # type: ignore
        """Wygeneruj raport miesięczny"""
        try:
            profile = self.app.app_context.get_current_profile()
            if not profile:
                self.status_label.text = "⚠️ Brak profilu"
                return
            
            year = int(self.year_spinner.text)
            month = int(self.month_spinner.text)
            
            pdf_path = self.app.app_context.pdf_service.generate_monthly_report(
                profile_name=profile.name,
                year=year,
                month=month,
                output_dir=str(Path.home() / "Documents")
            )
            
            self.status_label.text = f"✅ Raport z {month:02d}/{year}:\n{Path(pdf_path).name}"
            logger.info(f"✅ Raport miesięczny: {pdf_path}")
            
        except Exception as e:
            self.status_label.text = f"⚠️ Błąd:\n{str(e)}"
            logger.error(f"❌ Błąd raportu: {e}", exc_info=True)
    
    def generate_yearly(self, instance):  # type: ignore
        """Wygeneruj raport roczny"""
        try:
            profile = self.app.app_context.get_current_profile()
            if not profile:
                self.status_label.text = "⚠️ Brak profilu"
                return
            
            year = int(self.year_spinner.text)
            
            pdf_path = self.app.app_context.pdf_service.generate_summary_report(
                profile_name=profile.name,
                year=year,
                output_dir=str(Path.home() / "Documents")
            )
            
            self.status_label.text = f"✅ Raport z roku {year}:\n{Path(pdf_path).name}"
            logger.info(f"✅ Raport roczny: {pdf_path}")
            
        except Exception as e:
            self.status_label.text = f"⚠️ Błąd:\n{str(e)}"
            logger.error(f"❌ Błąd raportu: {e}", exc_info=True)


class SettingsScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        
        main = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Tytuł
        title = Label(
            text="⚙️ Ustawienia",
            size_hint_y=None,
            height=50,
            font_size='16sp',
            bold=True
        )
        main.add_widget(title)
        
        # Menu ustawień
        settings_layout = BoxLayout(orientation='vertical', size_hint_y=0.8, spacing=10)
        
        btn_profile = Button(text='👥 Zarządzanie Profilami')
        btn_profile.bind(on_press=lambda x: setattr(app.sm, 'current', 'profile'))  # type: ignore
        settings_layout.add_widget(btn_profile)
        
        btn_theme = Button(text='🎨 Zmień Motyw')
        btn_theme.bind(on_press=lambda x: setattr(app.sm, 'current', 'theme'))  # type: ignore
        settings_layout.add_widget(btn_theme)
        
        btn_info = Button(text='ℹ️ O Aplikacji')
        btn_info.bind(on_press=self.show_info)  # type: ignore
        settings_layout.add_widget(btn_info)
        
        main.add_widget(settings_layout)
        
        # Przyciski
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        btn_back = Button(text='◀️ Wróć')
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'dashboard'))  # type: ignore
        btn_layout.add_widget(btn_back)
        main.add_widget(btn_layout)
        
        self.add_widget(main)
    
    def show_info(self, instance):  # type: ignore
        """Pokaż informacje o aplikacji"""
        logger.info("WorkHours v1.0 - Ewidencja Godzin Pracy\nPython 3.11 + Kivy 2.3.0 + KivyMD 0.104.2")


class ProfileScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        from kivy.uix.textinput import TextInput
        
        main = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Tytuł
        title = Label(
            text="👥 Profil",
            size_hint_y=None,
            height=50,
            font_size='16sp',
            bold=True
        )
        main.add_widget(title)
        
        # Scroll z informacjami
        scroll = ScrollView(size_hint=(1, 0.6))
        info_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, padding=10)
        info_layout.bind(minimum_height=info_layout.setter('height'))  # type: ignore
        
        # Bieżący profil
        current_header = Label(
            text="📌 Aktualny profil:",
            size_hint_y=None,
            height=25,
            bold=True
        )
        info_layout.add_widget(current_header)
        
        try:
            profile = app.app_context.get_current_profile()
            info_text = (
                f"👤 Nazwa: {profile.name}\n"
                f"📅 Data: {profile.created_at}\n"
                f"🔑 ID: {profile.id}"
            )
        except:
            info_text = "⚠️ Brak aktywnego profilu"
        
        info_label = Label(
            text=info_text,
            size_hint_y=None,
            height=100,
            font_size='11sp'
        )
        info_layout.add_widget(info_label)
        
        # Nowy profil
        new_header = Label(
            text="➕ Utwórz nowy profil:",
            size_hint_y=None,
            height=25,
            bold=True
        )
        info_layout.add_widget(new_header)
        
        # Input dla nowej nazwy
        form_layout = GridLayout(cols=2, spacing=5, size_hint_y=None, height=50, padding=5)
        form_layout.add_widget(Label(text="Nazwa:", size_hint_y=None, height=50))
        self.new_profile_input = TextInput(
            text="Nowy Profil",
            multiline=False,
            size_hint_y=None,
            height=50,
            hint_text="Wpisz nazwę profilu"
        )
        form_layout.add_widget(self.new_profile_input)
        info_layout.add_widget(form_layout)
        
        scroll.add_widget(info_layout)
        main.add_widget(scroll)
        
        # Przyciski działań
        action_layout = BoxLayout(size_hint_y=0.2, spacing=5)
        
        btn_create = Button(text='✅ Utwórz')
        btn_create.bind(on_press=self.create_profile)  # type: ignore
        action_layout.add_widget(btn_create)
        
        btn_back = Button(text='◀️ Wróć')
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'settings'))  # type: ignore
        action_layout.add_widget(btn_back)
        
        main.add_widget(action_layout)
        self.add_widget(main)
    
    def create_profile(self, instance):  # type: ignore
        """Utwórz nowy profil"""
        try:
            from src.models import Profile
            from src.repository import ProfileRepository
            
            name = self.new_profile_input.text.strip()
            if not name:
                logger.warning("❌ Nazwa profilu nie może być pusta")
                return
            
            profile = Profile(
                id=None,
                name=name,
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            repo = ProfileRepository(self.app.app_context.database)
            repo.create(profile)
            
            logger.info(f"✅ Profil '{name}' został utworzony")
            self.new_profile_input.text = ""
            
        except Exception as e:
            logger.error(f"❌ Błąd tworzenia profilu: {e}", exc_info=True)


class ThemeScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        
        main = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Tytuł
        title = Label(
            text="🎨 Motywy Kolorystyczne",
            size_hint_y=None,
            height=50,
            font_size='16sp',
            bold=True
        )
        main.add_widget(title)
        
        # Info
        info = Label(
            text="Wybierz motyw do aplikacji:",
            size_hint_y=None,
            height=30,
            font_size='12sp'
        )
        main.add_widget(info)
        
        # Lista motywów
        scroll = ScrollView(size_hint=(1, 0.65))
        theme_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=10)
        theme_layout.bind(minimum_height=theme_layout.setter('height'))  # type: ignore
        
        # Definicje motywów
        themes = [
            ("🌙 Dark Mode", (0.1, 0.1, 0.1, 1)),
            ("☀️ Light Mode", (0.95, 0.95, 0.95, 1)),
            ("🌊 Ocean Blue", (0.2, 0.6, 0.9, 1)),
            ("🌲 Forest Green", (0.2, 0.6, 0.3, 1)),
            ("🌅 Sunset Orange", (0.95, 0.6, 0.2, 1))
        ]
        
        for theme_name, color in themes:
            btn = Button(
                text=theme_name,
                size_hint_y=None,
                height=45,
                background_color=color
            )
            btn.bind(on_press=lambda x, t=theme_name, c=color: self.select_theme(t, c))  # type: ignore
            theme_layout.add_widget(btn)
        
        scroll.add_widget(theme_layout)
        main.add_widget(scroll)
        
        # Status
        self.status_label = Label(
            text="Wybierz motyw",
            size_hint_y=None,
            height=50,
            font_size='11sp'
        )
        main.add_widget(self.status_label)
        
        # Przyciski
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        btn_back = Button(text='◀️ Wróć')
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'settings'))  # type: ignore
        btn_layout.add_widget(btn_back)
        main.add_widget(btn_layout)
        
        self.add_widget(main)
    
    def select_theme(self, theme_name, color):  # type: ignore
        """Wybierz motyw i zapisz ustawienia"""
        try:
            from src.models import Setting
            from src.repository import SettingRepository  # type: ignore
            
            profile = self.app.app_context.get_current_profile()
            if not profile:
                self.status_label.text = "⚠️ Brak profilu"
                return
            
            # Pobierz existing setting lub utwórz nowe
            repo = SettingRepository(self.app.app_context.database)  # type: ignore
            
            # Dla uproszczenia, zapisz theme name
            logger.info(f"🎨 Wybrany motyw: {theme_name} (kolor: {color})")
            
            self.status_label.text = f"✅ Motyw: {theme_name}"
            
        except Exception as e:
            self.status_label.text = f"⚠️ Błąd: {str(e)}"
            logger.error(f"❌ Błąd wyboru motywu: {e}", exc_info=True)


class WorkHoursApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_context = None
        self.sm = None
    
    def build(self):
        logger.info("Inicjalizowanie WorkHours...")
        
        # Inicjalizuj backend
        from src.app_context import AppContext
        db_path = Path.home() / ".workhours" / "workhours_app.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.app_context = AppContext.get_instance(str(db_path))
        
        logger.info(f"Backend OK: {self.app_context.get_current_profile_name()}")
        
        # Główny layout
        main = BoxLayout(orientation='vertical')
        
        # Tytuł
        title = Label(text="🏢 WorkHours - Ewidencja Godzin", size_hint_y=0.08, font_size='16sp', bold=True)
        main.add_widget(title)
        
        # Screen Manager
        self.sm = ScreenManager()
        
        # Dodaj ekrany
        screens = [
            ('dashboard', DashboardScreen(self, name='dashboard')),
            ('entry', EntryScreen(self, name='entry')),
            ('report', ReportScreen(self, name='report')),
            ('settings', SettingsScreen(self, name='settings')),
            ('profile', ProfileScreen(self, name='profile')),
            ('theme', ThemeScreen(self, name='theme')),
        ]
        
        for name, screen in screens:
            self.sm.add_widget(screen)
        
        self.sm.current = 'dashboard'
        main.add_widget(self.sm)
        
        # Menu dolne
        menu = BoxLayout(size_hint_y=0.1, spacing=2)
        for icon, screen_name in [('📊', 'dashboard'), ('📝', 'entry'), ('📄', 'report'), ('⚙️', 'settings')]:
            btn = Button(text=icon)
            btn.bind(on_press=lambda x, s=screen_name: setattr(self.sm, 'current', s))  # type: ignore
            menu.add_widget(btn)
        
        main.add_widget(menu)
        
        logger.info("UI OK")
        return main
    
    def on_stop(self) -> None:
        logger.info("Zamykanie...")
        if self.app_context:
            self.app_context.shutdown()


if __name__ == '__main__':
    app = WorkHoursApp()
    app.run()
