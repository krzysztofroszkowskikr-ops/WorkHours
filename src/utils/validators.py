"""
Validators - Walidacja danych wejściowych
"""

from typing import List, Dict, Tuple
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)


class Validators:
    """
    Zestaw funkcji walidacyjnych dla aplikacji
    """
    
    @staticmethod
    def is_valid_profile_name(name: str) -> Tuple[bool, str]:
        """
        Waliduj nazwę profilu
        
        Args:
            name: Nazwa profilu
            
        Returns:
            (is_valid, message)
        """
        if not name:
            return False, "Nazwa profilu nie może być pusta"
        
        if not isinstance(name, str):
            return False, "Nazwa profilu musi być tekstem"
        
        if len(name) < 2:
            return False, "Nazwa profilu musi mieć co najmniej 2 znaki"
        
        if len(name) > 50:
            return False, "Nazwa profilu nie może mieć więcej niż 50 znaków"
        
        # Nie pozwól na znaki specjalne
        if not re.match(r'^[a-zA-Z0-9ąęćńółśżź\s\-_.\']+$', name):
            return False, "Nazwa zawiera niedozwolone znaki"
        
        return True, ""
    
    @staticmethod
    def is_valid_date(date_str: str) -> Tuple[bool, str]:
        """
        Waliduj datę w formacie YYYY-MM-DD
        
        Args:
            date_str: String z datą
            
        Returns:
            (is_valid, message)
        """
        if not date_str:
            return False, "Data nie może być pusta"
        
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Nie pozwól na przyszłe daty
            if dt.date() > datetime.now().date():
                return False, "Data nie może być w przyszłości"
            
            # Nie pozwól na zbyt stare daty
            if dt.year < 2020:
                return False, "Data jest zbyt stara"
            
            return True, ""
        except ValueError:
            return False, "Niepoprawny format daty (YYYY-MM-DD)"
    
    @staticmethod
    def is_valid_time(time_str: str) -> Tuple[bool, str]:
        """
        Waliduj czas w formacie HH:MM
        
        Args:
            time_str: String z czasem
            
        Returns:
            (is_valid, message)
        """
        if not time_str:
            return False, "Czas nie może być pusty"
        
        try:
            parts = time_str.split(':')
            if len(parts) != 2:
                return False, "Niepoprawny format czasu (HH:MM)"
            
            hours = int(parts[0])
            minutes = int(parts[1])
            
            if not (0 <= hours < 24):
                return False, "Godzina musi być w zakresie 0-23"
            
            if not (0 <= minutes < 60):
                return False, "Minuty muszą być w zakresie 0-59"
            
            return True, ""
        except (ValueError, AttributeError):
            return False, "Niepoprawny format czasu"
    
    @staticmethod
    def is_valid_time_range(
        start_time: str,
        end_time: str,
        allow_midnight_crossing: bool = True
    ) -> Tuple[bool, str]:
        """
        Waliduj zakres czasu
        
        Args:
            start_time: Czas rozpoczęcia HH:MM
            end_time: Czas zakończenia HH:MM
            allow_midnight_crossing: Czy pozwolić na przesunięcie na następny dzień
            
        Returns:
            (is_valid, message)
        """
        # Podstawowa walidacja
        is_valid, msg = Validators.is_valid_time(start_time)
        if not is_valid:
            return False, f"Start: {msg}"
        
        is_valid, msg = Validators.is_valid_time(end_time)
        if not is_valid:
            return False, f"Koniec: {msg}"
        
        start_mins = Validators.time_to_minutes(start_time)
        end_mins = Validators.time_to_minutes(end_time)
        
        # Jeśli czas końca < czasu startu, to przesunięcie na następny dzień
        is_midnight_crossing = end_mins < start_mins
        
        if is_midnight_crossing and not allow_midnight_crossing:
            return False, "Przesunięcie na następny dzień nie jest dozwolone"
        
        return True, ""
    
    @staticmethod
    def is_valid_break_minutes(
        break_minutes: int,
        total_work_minutes: int
    ) -> Tuple[bool, str]:
        """
        Waliduj liczbę minut przerwy
        
        Args:
            break_minutes: Liczba minut przerwy
            total_work_minutes: Całkowita liczba minut pracy
            
        Returns:
            (is_valid, message)
        """
        if break_minutes < 0:
            return False, "Przerwa nie może być ujemna"
        
        if break_minutes >= total_work_minutes:
            return False, "Przerwa nie może być równa lub większa niż czas pracy"
        
        # Maks. 2 godziny przerwy
        if break_minutes > 120:
            return False, "Przerwa nie może być dłuższa niż 2 godziny"
        
        return True, ""
    
    @staticmethod
    def is_valid_day_type(day_type: str) -> Tuple[bool, str]:
        """Waliduj typ dnia"""
        valid_types = {"work_day", "sick_day", "vacation", "day_off"}
        
        if day_type not in valid_types:
            return False, f"Niepoprawny typ dnia: {day_type}"
        
        return True, ""
    
    @staticmethod
    def time_to_minutes(time_str: str) -> int:
        """Konwertuj HH:MM na minuty"""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes


__all__ = ['Validators']
