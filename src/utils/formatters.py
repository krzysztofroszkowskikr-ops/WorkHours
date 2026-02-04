"""
Formatters - Formatowanie danych do wyświetlenia
"""

from datetime import datetime
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class Formatters:
    """Formatowanie danych dla UI"""
    
    @staticmethod
    def format_date(date_str: str, format_str: str = "%d.%m.%Y") -> str:
        """
        Formatuj datę
        
        Args:
            date_str: Data YYYY-MM-DD
            format_str: Format docelowy
            
        Returns:
            Sformatowana data
        """
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime(format_str)
        except ValueError:
            return date_str
    
    @staticmethod
    def format_date_verbose(date_str: str) -> str:
        """
        Formatuj datę werbalne (z dniem tygodnia)
        
        Args:
            date_str: Data YYYY-MM-DD
            
        Returns:
            Np. "Poniedziałek, 15 grudnia 2025"
        """
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            
            days_pl = [
                "Poniedziałek", "Wtorek", "Środa", "Czwartek",
                "Piątek", "Sobota", "Niedziela"
            ]
            
            months_pl = [
                "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
                "lipca", "sierpnia", "września", "października", "listopada", "grudnia"
            ]
            
            day_name = days_pl[dt.weekday()]
            month_name = months_pl[dt.month - 1]
            
            return f"{day_name}, {dt.day} {month_name} {dt.year}"
        except ValueError:
            return date_str
    
    @staticmethod
    def format_duration_hm(minutes: int) -> str:
        """
        Formatuj czas trwania na H:MM
        
        Args:
            minutes: Liczba minut
            
        Returns:
            Format H:MM (np. 8:30)
        """
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}:{mins:02d}"
    
    @staticmethod
    def format_duration_decimal(minutes: int, places: int = 2) -> str:
        """
        Formatuj czas trwania na dziesiętny
        
        Args:
            minutes: Liczba minut
            places: Liczba miejsc po przecinku
            
        Returns:
            Format dziesiętny (np. 8.50)
        """
        hours = minutes / 60
        return f"{hours:.{places}f}"
    
    @staticmethod
    def format_work_day_for_display(day_data: Dict) -> Dict:
        """
        Formatuj dzień pracy do wyświetlenia
        
        Args:
            day_data: Dane dnia
            
        Returns:
            Sformatowane dane
        """
        return {
            'date': Formatters.format_date(day_data.get('date', ''), "%A, %d %b"),
            'day_type': Formatters.format_day_type(day_data.get('day_type', 'work_day')),
            'start_time': day_data.get('start_time', '-'),
            'end_time': day_data.get('end_time', '-'),
            'work_hours': Formatters.format_duration_hm(day_data.get('work_minutes', 0)),
            'break_minutes': day_data.get('break_minutes', 0),
            'net_hours': Formatters.format_duration_hm(
                day_data.get('work_minutes', 0) - day_data.get('break_minutes', 0)
            ),
        }
    
    @staticmethod
    def format_day_type(day_type: str) -> str:
        """Formatuj typ dnia na polski"""
        mapping = {
            'work_day': 'Dzień pracujący',
            'sick_day': 'Dzień chorobowy',
            'vacation': 'Urlop',
            'day_off': 'Dzień wolny'
        }
        return mapping.get(day_type, day_type)
    
    @staticmethod
    def format_month_year(year: int, month: int) -> str:
        """Formatuj rok i miesiąc"""
        months = [
            "Stycznia", "Lutego", "Marca", "Kwietnia", "Maja", "Czerwca",
            "Lipca", "Sierpnia", "Września", "Października", "Listopada", "Grudnia"
        ]
        month_name = months[month - 1] if 1 <= month <= 12 else f"{month}"
        return f"{month_name} {year}"
    
    @staticmethod
    def format_currency(amount: float, currency: str = "PLN") -> str:
        """Formatuj walutę"""
        return f"{amount:.2f} {currency}"
    
    @staticmethod
    def format_percentage(value: float, total: float) -> str:
        """Formatuj procent"""
        if total == 0:
            return "0%"
        percentage = (value / total) * 100
        return f"{percentage:.1f}%"


__all__ = ['Formatters']
