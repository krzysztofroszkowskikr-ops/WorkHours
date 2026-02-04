"""
Test Validators - Testy walidatorów
"""

import pytest
from src.utils.validators import Validators


class TestValidatorsProfileName:
    """Testy walidacji nazw profili"""
    
    def test_valid_profile_names(self):
        """Testy poprawnych nazw"""
        assert Validators.is_valid_profile_name("John Doe")[0] is True
        assert Validators.is_valid_profile_name("Adam")[0] is True
        assert Validators.is_valid_profile_name("Maria-123")[0] is True
        assert Validators.is_valid_profile_name("Paweł O'Connor")[0] is True
    
    def test_invalid_profile_names(self):
        """Testy niepoprawnych nazw"""
        is_valid, msg = Validators.is_valid_profile_name("")
        assert is_valid is False
        
        is_valid, msg = Validators.is_valid_profile_name("A")
        assert is_valid is False
        
        is_valid, msg = Validators.is_valid_profile_name("A" * 51)
        assert is_valid is False
        
        is_valid, msg = Validators.is_valid_profile_name("John@Doe#")
        assert is_valid is False


class TestValidatorsDate:
    """Testy walidacji dat"""
    
    def test_valid_dates(self):
        """Testy poprawnych dat"""
        is_valid, msg = Validators.is_valid_date("2025-01-15")
        assert is_valid is True
        
        is_valid, msg = Validators.is_valid_date("2020-01-01")
        assert is_valid is True
    
    def test_invalid_dates(self):
        """Testy niepoprawnych dat"""
        is_valid, msg = Validators.is_valid_date("01-15-2025")
        assert is_valid is False
        
        is_valid, msg = Validators.is_valid_date("2025-13-01")
        assert is_valid is False
        
        is_valid, msg = Validators.is_valid_date("2019-12-31")
        assert is_valid is False


class TestValidatorsTime:
    """Testy walidacji czasu"""
    
    def test_valid_times(self):
        """Testy poprawnych czasów"""
        is_valid, msg = Validators.is_valid_time("09:00")
        assert is_valid is True
        
        is_valid, msg = Validators.is_valid_time("23:59")
        assert is_valid is True
        
        is_valid, msg = Validators.is_valid_time("00:00")
        assert is_valid is True
    
    def test_invalid_times(self):
        """Testy niepoprawnych czasów"""
        is_valid, msg = Validators.is_valid_time("24:00")
        assert is_valid is False
        
        is_valid, msg = Validators.is_valid_time("09:60")
        assert is_valid is False
        
        is_valid, msg = Validators.is_valid_time("9:00")
        assert is_valid is False


class TestValidatorsTimeRange:
    """Testy walidacji zakresu czasu"""
    
    def test_valid_time_range(self):
        """Testy poprawnych zakresów"""
        is_valid, msg = Validators.is_valid_time_range("09:00", "17:00")
        assert is_valid is True
        
        is_valid, msg = Validators.is_valid_time_range("22:00", "06:00", allow_midnight_crossing=True)
        assert is_valid is True
    
    def test_invalid_time_range(self):
        """Testy niepoprawnych zakresów"""
        is_valid, msg = Validators.is_valid_time_range("24:00", "17:00")
        assert is_valid is False
        
        is_valid, msg = Validators.is_valid_time_range("22:00", "06:00", allow_midnight_crossing=False)
        assert is_valid is False


class TestValidatorsBreak:
    """Testy walidacji przerw"""
    
    def test_valid_breaks(self):
        """Testy poprawnych przerw"""
        is_valid, msg = Validators.is_valid_break_minutes(30, 480)
        assert is_valid is True
        
        is_valid, msg = Validators.is_valid_break_minutes(0, 480)
        assert is_valid is True
    
    def test_invalid_breaks(self):
        """Testy niepoprawnych przerw"""
        is_valid, msg = Validators.is_valid_break_minutes(-1, 480)
        assert is_valid is False
        
        is_valid, msg = Validators.is_valid_break_minutes(480, 480)
        assert is_valid is False
        
        is_valid, msg = Validators.is_valid_break_minutes(150, 480)
        assert is_valid is False


class TestValidatorsDayType:
    """Testy walidacji typów dni"""
    
    def test_valid_day_types(self):
        """Testy poprawnych typów dni"""
        is_valid, msg = Validators.is_valid_day_type("work_day")
        assert is_valid is True
        
        is_valid, msg = Validators.is_valid_day_type("sick_day")
        assert is_valid is True
        
        is_valid, msg = Validators.is_valid_day_type("vacation")
        assert is_valid is True
        
        is_valid, msg = Validators.is_valid_day_type("day_off")
        assert is_valid is True
    
    def test_invalid_day_types(self):
        """Testy niepoprawnych typów dni"""
        is_valid, msg = Validators.is_valid_day_type("unknown_day")
        assert is_valid is False
        
        is_valid, msg = Validators.is_valid_day_type("WORK_DAY")
        assert is_valid is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
