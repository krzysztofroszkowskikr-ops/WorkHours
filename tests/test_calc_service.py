"""
Test CalcService - Testy jednostkowe dla logiki obliczeń czasowych
"""

import pytest
from datetime import datetime, timedelta
from src.services.calc_service import CalcService, WorkDayResult, MonthSummary


class TestCalcServiceValidation:
    """Testy walidacji formatu"""
    
    def test_validate_time_format_valid(self):
        """Testy poprawnych formatów czasu"""
        assert CalcService.validate_time_format("09:00") is True
        assert CalcService.validate_time_format("23:59") is True
        assert CalcService.validate_time_format("00:00") is True
    
    def test_validate_time_format_invalid(self):
        """Testy niepoprawnych formatów czasu"""
        assert CalcService.validate_time_format("24:00") is False
        assert CalcService.validate_time_format("09:60") is False
        assert CalcService.validate_time_format("9:00") is False
        assert CalcService.validate_time_format("09-00") is False
        assert CalcService.validate_time_format("") is False
        assert CalcService.validate_time_format(None) is False
    
    def test_validate_date_format_valid(self):
        """Testy poprawnych formatów daty"""
        today = datetime.now().date().isoformat()
        assert CalcService.validate_date_format(today) is True
        assert CalcService.validate_date_format("2025-01-01") is True
        assert CalcService.validate_date_format("2024-12-31") is True
    
    def test_validate_date_format_invalid(self):
        """Testy niepoprawnych formatów daty"""
        assert CalcService.validate_date_format("01-01-2025") is False
        assert CalcService.validate_date_format("2025-13-01") is False
        assert CalcService.validate_date_format("2025-01-32") is False
        assert CalcService.validate_date_format("") is False


class TestCalcServiceConversions:
    """Testy konwersji czasu"""
    
    def test_time_to_minutes(self):
        """Testy konwersji czasu na minuty"""
        assert CalcService.time_to_minutes("00:00") == 0
        assert CalcService.time_to_minutes("01:00") == 60
        assert CalcService.time_to_minutes("08:30") == 510
        assert CalcService.time_to_minutes("23:59") == 1439
    
    def test_minutes_to_time(self):
        """Testy konwersji minut na czas"""
        assert CalcService.minutes_to_time(0) == "00:00"
        assert CalcService.minutes_to_time(60) == "01:00"
        assert CalcService.minutes_to_time(510) == "08:30"
        assert CalcService.minutes_to_time(1439) == "23:59"
    
    def test_minutes_to_decimal_hours(self):
        """Testy konwersji minut na godziny dziesiętne"""
        assert CalcService.minutes_to_decimal_hours(0) == 0.0
        assert CalcService.minutes_to_decimal_hours(60) == 1.0
        assert CalcService.minutes_to_decimal_hours(480) == 8.0
        assert CalcService.minutes_to_decimal_hours(510) == 8.5
        assert CalcService.minutes_to_decimal_hours(540) == 9.0
    
    def test_minutes_to_hours_hm(self):
        """Testy konwersji minut na format H:MM"""
        assert CalcService.minutes_to_hours_hm(0) == "0:00"
        assert CalcService.minutes_to_hours_hm(60) == "1:00"
        assert CalcService.minutes_to_hours_hm(480) == "8:00"
        assert CalcService.minutes_to_hours_hm(510) == "8:30"


class TestCalcServiceWorkday:
    """Testy obliczeń dla poszczególnych dni"""
    
    @pytest.fixture
    def service(self):
        return CalcService()
    
    def test_normal_workday(self, service):
        """Test normalnego dnia pracy 9:00-17:00"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time="09:00",
            end_time="17:00",
            break_minutes=0,
            day_type="work_day"
        )
        
        assert result.is_valid is True
        assert result.work_minutes == 480  # 8 godzin
        assert result.work_hours_decimal == 8.0
        assert result.net_minutes == 480
    
    def test_workday_with_break(self, service):
        """Test dnia pracy z przerwą"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time="09:00",
            end_time="17:30",
            break_minutes=30,
            day_type="work_day"
        )
        
        assert result.is_valid is True
        assert result.work_minutes == 510  # 8.5 godzin
        assert result.break_minutes == 30
        assert result.net_minutes == 480
    
    def test_midnight_crossing(self, service):
        """Test przekroczenia północy (22:00-06:00)"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time="22:00",
            end_time="06:00",
            break_minutes=0,
            day_type="work_day"
        )
        
        assert result.is_valid is True
        assert result.is_midnight_crossing is True
        assert result.work_minutes == 480  # 8 godzin
        assert result.net_minutes == 480
    
    def test_midnight_crossing_with_break(self, service):
        """Test przekroczenia północy z przerwą"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time="22:00",
            end_time="07:00",
            break_minutes=60,
            day_type="work_day"
        )
        
        assert result.is_valid is True
        assert result.is_midnight_crossing is True
        assert result.work_minutes == 540  # 9 godzin
        assert result.break_minutes == 60
        assert result.net_minutes == 480  # 8 godzin netto
    
    def test_sick_day(self, service):
        """Test dnia chorobowego"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time=None,
            end_time=None,
            day_type="sick_day"
        )
        
        assert result.is_valid is True
        assert result.day_type == "sick_day"
        assert result.net_minutes == 480  # Norma dniowa
    
    def test_vacation(self, service):
        """Test urlopu"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time=None,
            end_time=None,
            day_type="vacation"
        )
        
        assert result.is_valid is True
        assert result.net_minutes == 0
    
    def test_day_off(self, service):
        """Test dnia wolnego"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time=None,
            end_time=None,
            day_type="day_off"
        )
        
        assert result.is_valid is True
        assert result.net_minutes == 0
    
    def test_invalid_time_too_short(self, service):
        """Test zbyt krótkiej pracy (<15 minut)"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time="09:00",
            end_time="09:10",
            day_type="work_day"
        )
        
        assert result.is_valid is False
        assert "zbyt mało" in result.error_message.lower()
    
    def test_invalid_time_too_long(self, service):
        """Test zbyt długiej pracy (>12 godzin)"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time="09:00",
            end_time="22:00",
            day_type="work_day"
        )
        
        assert result.is_valid is False
        assert "zbyt dużo" in result.error_message.lower()
    
    def test_invalid_break_exceeds_work(self, service):
        """Test przerwy dłuższej niż czas pracy"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time="09:00",
            end_time="17:00",
            break_minutes=500,
            day_type="work_day"
        )
        
        assert result.is_valid is False
    
    def test_invalid_date_future(self, service):
        """Test przyszłej daty"""
        future_date = (datetime.now() + timedelta(days=10)).date().isoformat()
        result = service.calculate_work_day(
            date=future_date,
            start_time="09:00",
            end_time="17:00",
            day_type="work_day"
        )
        
        assert result.is_valid is False
    
    def test_missing_times_for_workday(self, service):
        """Test brakujących czasów dla dnia pracującego"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time=None,
            end_time=None,
            day_type="work_day"
        )
        
        assert result.is_valid is False
        assert "brakuje" in result.error_message.lower()


class TestCalcServiceMonthlySummary:
    """Testy podsumowań miesięcznych"""
    
    @pytest.fixture
    def service(self):
        return CalcService()
    
    def test_empty_month(self, service):
        """Test pustego miesiąca"""
        summary = service.calculate_month_summary([])
        
        assert summary.year == 0
        assert summary.month == 0
        assert summary.total_work_minutes == 0
    
    def test_single_workday(self, service):
        """Test miesiąca z jednym dniem pracy"""
        result = service.calculate_work_day(
            date="2025-01-15",
            start_time="09:00",
            end_time="17:00",
            break_minutes=0,
            day_type="work_day"
        )
        
        summary = service.calculate_month_summary([result])
        
        assert summary.year == 2025
        assert summary.month == 1
        assert summary.work_days == 1
        assert summary.total_work_minutes == 480
    
    def test_mixed_work_types(self, service):
        """Test miesiąca z różnymi typami dni"""
        days = [
            service.calculate_work_day("2025-01-01", "09:00", "17:00", 0, "work_day"),
            service.calculate_work_day("2025-01-02", None, None, 0, "sick_day"),
            service.calculate_work_day("2025-01-03", None, None, 0, "vacation"),
            service.calculate_work_day("2025-01-04", None, None, 0, "day_off"),
        ]
        
        summary = service.calculate_month_summary(days)
        
        assert summary.work_days == 1
        assert summary.sick_days == 1
        assert summary.vacation_days == 1
        assert summary.day_offs == 1
        assert summary.total_work_minutes == 480


class TestCalcServiceEstimation:
    """Testy estymacji"""
    
    @pytest.fixture
    def service(self):
        return CalcService()
    
    def test_estimate_required_time(self, service):
        """Test estymacji wymaganego czasu"""
        days, hours = service.estimate_required_time(
            target_hours=40,
            daily_hours=8
        )
        
        assert days == 5
        assert hours == 0.0
    
    def test_estimate_with_remainder(self, service):
        """Test estymacji z resztą"""
        days, hours = service.estimate_required_time(
            target_hours=42,
            daily_hours=8
        )
        
        assert days == 5
        assert hours == 2.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
