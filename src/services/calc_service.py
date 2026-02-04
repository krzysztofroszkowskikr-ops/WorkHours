"""
CalcService - Serwis obliczeń czasowych
Obsługuje: godziny pracy, przerwy, przekroczenia północy, dni nierobocze
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class WorkDayResult:
    """Wynik obliczeń dla dnia pracy"""
    date: str                        # YYYY-MM-DD
    work_minutes: int                # Całkowita liczba minut pracy
    work_hours_decimal: float        # Format dziesiętny (8.5)
    work_hours_hm: str               # Format H:MM (8:30)
    break_minutes: int               # Przerwy
    net_minutes: int                 # Minuty netto (work_minutes - break_minutes)
    net_hours_decimal: float         # Netto dziesiętny
    net_hours_hm: str                # Netto H:MM
    day_type: str                    # work_day, sick_day, vacation, day_off
    start_time: Optional[str]        # HH:MM
    end_time: Optional[str]          # HH:MM
    is_midnight_crossing: bool       # Czy wygodnie przekracza północ
    is_valid: bool                   # Czy wpis jest poprawny
    error_message: Optional[str]     # Wiadomość o błędzie


@dataclass
class MonthSummary:
    """Podsumowanie miesiąca"""
    year: int
    month: int
    work_days: int                   # Liczba dni pracujących
    sick_days: int
    vacation_days: int
    day_offs: int
    total_work_minutes: int
    total_work_hours_decimal: float
    total_work_hours_hm: str
    average_daily_hours: float
    days_with_entries: List[str]     # Lista dat z wpisami


class CalcService:
    """
    Serwis obliczeń czasu pracy
    
    Krytyczne funkcje:
    - Obliczanie czasu pracy z obsługą przekroczenia północy
    - Obsługa przerw
    - Kategoryzacja dni
    - Walidacja czasów
    - Podsumowania miesięczne
    """
    
    # Norma godzin pracy dziennie
    STANDARD_WORKING_HOURS = 8.0
    
    # Typy dni
    WORK_DAY = "work_day"
    SICK_DAY = "sick_day"
    VACATION = "vacation"
    DAY_OFF = "day_off"
    
    # Maksymalna i minimalna godzina dla jednego dnia (dla detecji)
    MIN_WORK_MINUTES = 15        # 15 minut
    MAX_WORK_MINUTES = 12 * 60   # 12 godzin
    
    @staticmethod
    def validate_time_format(time_str: str) -> bool:
        """
        Waliduj format czasu HH:MM
        
        Args:
            time_str: String do walidacji
            
        Returns:
            True jeśli format poprawny
        """
        try:
            if not isinstance(time_str, str):
                return False
            
            parts = time_str.split(':')
            if len(parts) != 2:
                return False
            
            hours = int(parts[0])
            minutes = int(parts[1])
            
            return 0 <= hours < 24 and 0 <= minutes < 60
        except (ValueError, AttributeError):
            return False
    
    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        """
        Waliduj format daty YYYY-MM-DD
        
        Args:
            date_str: String do walidacji
            
        Returns:
            True jeśli format poprawny i data válida
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def time_to_minutes(time_str: str) -> int:
        """
        Konwertuj czas HH:MM na minuty
        
        Args:
            time_str: Format HH:MM
            
        Returns:
            Liczba minut od północy
        """
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    @staticmethod
    def minutes_to_time(minutes: int) -> str:
        """
        Konwertuj minuty na format HH:MM
        
        Args:
            minutes: Liczba minut
            
        Returns:
            Format HH:MM
        """
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"
    
    @staticmethod
    def minutes_to_decimal_hours(minutes: int) -> float:
        """
        Konwertuj minuty na godziny dziesiętne
        
        Args:
            minutes: Liczba minut
            
        Returns:
            Godziny w formacie dziesiętnym (8.5)
        """
        return round(minutes / 60, 2)
    
    @staticmethod
    def minutes_to_hours_hm(minutes: int) -> str:
        """
        Konwertuj minuty na format H:MM
        
        Args:
            minutes: Liczba minut
            
        Returns:
            Format H:MM (np. 8:30)
        """
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}:{mins:02d}"
    
    @staticmethod
    def _calculate_work_minutes_with_midnight(
        start_time: str,
        end_time: str,
        date: str
    ) -> Tuple[int, bool]:
        """
        Oblicz minuty pracy z obsługą przekroczenia północy
        
        Specjalny przypadek:
        - Godziny: 22:00-06:00 (poprzedni dzień do następnego)
        - Tutaj dodajemy 1 dzień do end_time
        
        Args:
            start_time: Czas rozpoczęcia HH:MM
            end_time: Czas zakończenia HH:MM
            date: Data wpisu YYYY-MM-DD
            
        Returns:
            (work_minutes, is_midnight_crossing)
        """
        start_minutes = CalcService.time_to_minutes(start_time)
        end_minutes = CalcService.time_to_minutes(end_time)
        
        # Detekuj przekroczenie północy
        # Jeśli czas końca < czas startu, znaczy że zmieniła się doba
        is_midnight_crossing = end_minutes < start_minutes
        
        if is_midnight_crossing:
            # Koniec to następny dzień
            # Oblicz: (24h - start) + end
            work_minutes = (24 * 60 - start_minutes) + end_minutes
        else:
            # Normalnie
            work_minutes = end_minutes - start_minutes
        
        return work_minutes, is_midnight_crossing
    
    def calculate_work_day(
        self,
        date: str,
        start_time: Optional[str],
        end_time: Optional[str],
        break_minutes: int = 0,
        day_type: str = WORK_DAY,
        notes: str = ""
    ) -> WorkDayResult:
        """
        Oblicz szczegóły pracy dla dnia
        
        Args:
            date: Data YYYY-MM-DD
            start_time: Godzina rozpoczęcia (None dla dni wolnych)
            end_time: Godzina zakończenia (None dla dni wolnych)
            break_minutes: Liczba minut przerwy
            day_type: Typ dnia
            notes: Notatki
            
        Returns:
            WorkDayResult z wszystkimi obliczeniami
        """
        # Walidacja daty
        if not self.validate_date_format(date):
            return WorkDayResult(
                date=date,
                work_minutes=0,
                work_hours_decimal=0,
                work_hours_hm="0:00",
                break_minutes=0,
                net_minutes=0,
                net_hours_decimal=0,
                net_hours_hm="0:00",
                day_type=day_type,
                start_time=start_time,
                end_time=end_time,
                is_midnight_crossing=False,
                is_valid=False,
                error_message="Niepoprawny format daty"
            )
        
        # Dni wolne i urlopowe
        if day_type in [self.VACATION, self.DAY_OFF]:
            return WorkDayResult(
                date=date,
                work_minutes=0,
                work_hours_decimal=0,
                work_hours_hm="0:00",
                break_minutes=0,
                net_minutes=0,
                net_hours_decimal=0,
                net_hours_hm="0:00",
                day_type=day_type,
                start_time=None,
                end_time=None,
                is_midnight_crossing=False,
                is_valid=True,
                error_message=None
            )
        
        # Dni chorobowe
        if day_type == self.SICK_DAY:
            work_minutes = int(self.STANDARD_WORKING_HOURS * 60)
            return WorkDayResult(
                date=date,
                work_minutes=work_minutes,
                work_hours_decimal=self.minutes_to_decimal_hours(work_minutes),
                work_hours_hm=self.minutes_to_hours_hm(work_minutes),
                break_minutes=0,
                net_minutes=work_minutes,
                net_hours_decimal=self.minutes_to_decimal_hours(work_minutes),
                net_hours_hm=self.minutes_to_hours_hm(work_minutes),
                day_type=day_type,
                start_time=None,
                end_time=None,
                is_midnight_crossing=False,
                is_valid=True,
                error_message=None
            )
        
        # Dni pracujące - wymagaj godzin
        if not start_time or not end_time:
            return WorkDayResult(
                date=date,
                work_minutes=0,
                work_hours_decimal=0,
                work_hours_hm="0:00",
                break_minutes=0,
                net_minutes=0,
                net_hours_decimal=0,
                net_hours_hm="0:00",
                day_type=day_type,
                start_time=start_time,
                end_time=end_time,
                is_midnight_crossing=False,
                is_valid=False,
                error_message="Brakuje godzin dla dnia pracującego"
            )
        
        # Walidacja formatu czasu
        if not self.validate_time_format(start_time):
            return WorkDayResult(
                date=date,
                work_minutes=0,
                work_hours_decimal=0,
                work_hours_hm="0:00",
                break_minutes=0,
                net_minutes=0,
                net_hours_decimal=0,
                net_hours_hm="0:00",
                day_type=day_type,
                start_time=start_time,
                end_time=end_time,
                is_midnight_crossing=False,
                is_valid=False,
                error_message="Niepoprawny format czasu rozpoczęcia"
            )
        
        if not self.validate_time_format(end_time):
            return WorkDayResult(
                date=date,
                work_minutes=0,
                work_hours_decimal=0,
                work_hours_hm="0:00",
                break_minutes=0,
                net_minutes=0,
                net_hours_decimal=0,
                net_hours_hm="0:00",
                day_type=day_type,
                start_time=start_time,
                end_time=end_time,
                is_midnight_crossing=False,
                is_valid=False,
                error_message="Niepoprawny format czasu zakończenia"
            )
        
        # Oblicz minuty pracy
        work_minutes, is_midnight_crossing = self._calculate_work_minutes_with_midnight(
            start_time, end_time, date
        )
        
        # Walidacja zakresu
        if work_minutes < self.MIN_WORK_MINUTES:
            return WorkDayResult(
                date=date,
                work_minutes=0,
                work_hours_decimal=0,
                work_hours_hm="0:00",
                break_minutes=0,
                net_minutes=0,
                net_hours_decimal=0,
                net_hours_hm="0:00",
                day_type=day_type,
                start_time=start_time,
                end_time=end_time,
                is_midnight_crossing=is_midnight_crossing,
                is_valid=False,
                error_message=f"Zbyt mało czasu pracy (<15 minut)"
            )
        
        if work_minutes > self.MAX_WORK_MINUTES:
            return WorkDayResult(
                date=date,
                work_minutes=0,
                work_hours_decimal=0,
                work_hours_hm="0:00",
                break_minutes=0,
                net_minutes=0,
                net_hours_decimal=0,
                net_hours_hm="0:00",
                day_type=day_type,
                start_time=start_time,
                end_time=end_time,
                is_midnight_crossing=is_midnight_crossing,
                is_valid=False,
                error_message=f"Zbyt dużo czasu pracy (>12 godzin)"
            )
        
        # Walidacja przerwy
        if break_minutes < 0 or break_minutes >= work_minutes:
            return WorkDayResult(
                date=date,
                work_minutes=work_minutes,
                work_hours_decimal=self.minutes_to_decimal_hours(work_minutes),
                work_hours_hm=self.minutes_to_hours_hm(work_minutes),
                break_minutes=0,
                net_minutes=work_minutes,
                net_hours_decimal=self.minutes_to_decimal_hours(work_minutes),
                net_hours_hm=self.minutes_to_hours_hm(work_minutes),
                day_type=day_type,
                start_time=start_time,
                end_time=end_time,
                is_midnight_crossing=is_midnight_crossing,
                is_valid=False,
                error_message="Niepoprawna długość przerwy"
            )
        
        # Oblicz netto
        net_minutes = work_minutes - break_minutes
        
        return WorkDayResult(
            date=date,
            work_minutes=work_minutes,
            work_hours_decimal=self.minutes_to_decimal_hours(work_minutes),
            work_hours_hm=self.minutes_to_hours_hm(work_minutes),
            break_minutes=break_minutes,
            net_minutes=net_minutes,
            net_hours_decimal=self.minutes_to_decimal_hours(net_minutes),
            net_hours_hm=self.minutes_to_hours_hm(net_minutes),
            day_type=day_type,
            start_time=start_time,
            end_time=end_time,
            is_midnight_crossing=is_midnight_crossing,
            is_valid=True,
            error_message=None
        )
    
    def calculate_month_summary(
        self,
        work_days: List[WorkDayResult]
    ) -> MonthSummary:
        """
        Oblicz podsumowanie miesiąca
        
        Args:
            work_days: Lista wyników obliczeń dla dni
            
        Returns:
            Podsumowanie miesiąca
        """
        if not work_days:
            return MonthSummary(
                year=0,
                month=0,
                work_days=0,
                sick_days=0,
                vacation_days=0,
                day_offs=0,
                total_work_minutes=0,
                total_work_hours_decimal=0,
                total_work_hours_hm="0:00",
                average_daily_hours=0,
                days_with_entries=[]
            )
        
        # Ekstraktuj rok i miesiąc z pierwszego wpisu
        first_date = work_days[0].date
        year = int(first_date[:4])
        month = int(first_date[5:7])
        
        # Zlicz dni po typach
        work_day_count = sum(1 for d in work_days if d.day_type == self.WORK_DAY and d.is_valid)
        sick_day_count = sum(1 for d in work_days if d.day_type == self.SICK_DAY and d.is_valid)
        vacation_day_count = sum(1 for d in work_days if d.day_type == self.VACATION and d.is_valid)
        day_off_count = sum(1 for d in work_days if d.day_type == self.DAY_OFF and d.is_valid)
        
        # Sumuj minuty (tylko ważne wpisy)
        total_minutes = sum(d.net_minutes for d in work_days if d.is_valid)
        
        # Średnia dziennie (tylko dni pracujące z wpisami)
        days_with_work = sum(1 for d in work_days if d.is_valid and d.net_minutes > 0)
        average_hours = (total_minutes / 60 / days_with_work) if days_with_work > 0 else 0
        
        return MonthSummary(
            year=year,
            month=month,
            work_days=work_day_count,
            sick_days=sick_day_count,
            vacation_days=vacation_day_count,
            day_offs=day_off_count,
            total_work_minutes=total_minutes,
            total_work_hours_decimal=self.minutes_to_decimal_hours(total_minutes),
            total_work_hours_hm=self.minutes_to_hours_hm(total_minutes),
            average_daily_hours=round(average_hours, 2),
            days_with_entries=[d.date for d in work_days if d.is_valid]
        )
    
    def estimate_required_time(
        self,
        target_hours: float,
        daily_hours: float = STANDARD_WORKING_HOURS
    ) -> Tuple[int, float]:
        """
        Estymuj ile dni potrzeba aby osiągnąć target godzin
        
        Args:
            target_hours: Docelowa liczba godzin
            daily_hours: Godziny dziennie
            
        Returns:
            (liczba_dni, pozostałe_godziny)
        """
        total_minutes = int(target_hours * 60)
        daily_minutes = int(daily_hours * 60)
        
        if daily_minutes <= 0:
            return 0, target_hours
        
        days_needed = total_minutes // daily_minutes
        remaining_minutes = total_minutes % daily_minutes
        remaining_hours = self.minutes_to_decimal_hours(remaining_minutes)
        
        return days_needed, remaining_hours


__all__ = ['CalcService', 'WorkDayResult', 'MonthSummary']
