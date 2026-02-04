# API DESIGN & CALCULATIONS SPECIFICATION
## WorkHours Purple v1.0

---

## 1. WORK TIME CALCULATION API

### 1.1 Core Calculation Function

```python
# src/services/calc_service.py

class CalcService:
    """Centralized work time calculations"""
    
    @staticmethod
    def calculate_work_time(
        start: str,           # "08:30"
        end: str,             # "17:00"
        break_minutes: int,   # 60
        day_type: str,        # "work" | "vacation" | "sick" | "holiday" | "other"
    ) -> dict:
        """
        Calculate work time for a single day
        
        Args:
            start: Start time in HH:MM format
            end: End time in HH:MM format
            break_minutes: Break duration in minutes
            day_type: Type of day (work/vacation/sick/holiday/other)
        
        Returns:
            {
                'gross_minutes': int,        # Total time (before break)
                'gross_formatted': str,      # "HH:MM"
                'net_minutes': int,          # Time after break
                'net_formatted': str,        # "HH:MM"
                'is_valid': bool,            # Validation status
                'errors': list,              # Validation error messages
                'reason': str,               # Why (for non-work days)
            }
        
        Examples:
            >>> CalcService.calculate_work_time('08:30', '17:00', 60, 'work')
            {
                'gross_minutes': 510,
                'gross_formatted': '8:30',
                'net_minutes': 450,
                'net_formatted': '7:30',
                'is_valid': True,
                'errors': [],
            }
            
            >>> CalcService.calculate_work_time('08:00', '17:00', 60, 'vacation')
            {
                'gross_minutes': 0,
                'gross_formatted': '0:00',
                'net_minutes': 0,
                'net_formatted': '0:00',
                'is_valid': True,
                'errors': [],
                'reason': 'Typ dnia: vacation (nie wlicza sie do sumy)',
            }
        """
        errors = []
        
        # Step 1: Validate input format
        if not CalcService._validate_time_format(start):
            errors.append(f"Invalid start time format: {start}")
        if not CalcService._validate_time_format(end):
            errors.append(f"Invalid end time format: {end}")
        
        if errors:
            return {
                'gross_minutes': 0,
                'gross_formatted': '0:00',
                'net_minutes': 0,
                'net_formatted': '0:00',
                'is_valid': False,
                'errors': errors,
            }
        
        # Step 2: Parse times to datetime objects
        from datetime import datetime, timedelta
        
        start_dt = datetime.strptime(start, "%H:%M")
        end_dt = datetime.strptime(end, "%H:%M")
        
        # Step 3: Handle midnight crossing (e.g., 22:00 - 06:00)
        if end_dt <= start_dt:
            end_dt += timedelta(days=1)
        
        # Step 4: Calculate gross time
        delta = end_dt - start_dt
        gross_minutes = int(delta.total_seconds() / 60)
        
        # Step 5: Validate time ranges
        if gross_minutes <= 0:
            errors.append("End time must be after start time")
        
        # Step 6: Validate break
        if break_minutes > gross_minutes:
            errors.append(
                f"Break ({break_minutes}min) exceeds gross time ({gross_minutes}min)"
            )
        
        # Step 7: For non-work days, return 0 hours
        if day_type != 'work':
            return {
                'gross_minutes': 0,
                'gross_formatted': '0:00',
                'net_minutes': 0,
                'net_formatted': '0:00',
                'is_valid': len(errors) == 0,
                'errors': errors,
                'reason': f'Typ dnia: {day_type}'
            }
        
        # Step 8: Calculate net time
        net_minutes = max(0, gross_minutes - break_minutes)
        
        return {
            'gross_minutes': gross_minutes,
            'gross_formatted': CalcService.minutes_to_hm(gross_minutes),
            'net_minutes': net_minutes,
            'net_formatted': CalcService.minutes_to_hm(net_minutes),
            'is_valid': len(errors) == 0,
            'errors': errors,
        }
    
    # ===== HELPER FUNCTIONS =====
    
    @staticmethod
    def _validate_time_format(time_str: str) -> bool:
        """Validate HH:MM format"""
        import re
        if not re.match(r'^\d{2}:\d{2}$', time_str):
            return False
        h, m = map(int, time_str.split(':'))
        return 0 <= h < 24 and 0 <= m < 60
    
    @staticmethod
    def minutes_to_hm(minutes: int) -> str:
        """Convert 510 minutes -> '8:30'"""
        h = minutes // 60
        m = minutes % 60
        return f"{h}:{m:02d}"
    
    @staticmethod
    def hm_to_minutes(time_str: str) -> int:
        """Convert '8:30' -> 510 minutes"""
        h, m = map(int, time_str.split(':'))
        return h * 60 + m
```

---

### 1.2 Monthly Summary Calculation

```python
class CalcService:
    
    @staticmethod
    def calculate_month_summary(entries: list) -> dict:
        """
        Calculate summary statistics for entire month
        
        Args:
            entries: list of WorkEntry objects
        
        Returns:
            {
                'total_net_minutes': int,
                'total_net_formatted': str,      # "168:30"
                'total_gross_minutes': int,
                'total_gross_formatted': str,
                'day_counts': {
                    'work': int,
                    'vacation': int,
                    'sick': int,
                    'holiday': int,
                    'other': int,
                    'missing': int,              # Days without entry
                },
                'avg_daily_hours': float,        # Average hours per work day
                'working_days': int,             # Expected work days
                'completeness': float,           # % of days with entries
            }
        
        Example:
            >>> entries = [entry1, entry2, ...]  # 30 entries for February
            >>> CalcService.calculate_month_summary(entries)
            {
                'total_net_minutes': 8640,       # 144 hours
                'total_net_formatted': '144:00',
                'total_gross_minutes': 8760,
                'total_gross_formatted': '146:00',
                'day_counts': {
                    'work': 20,
                    'vacation': 2,
                    'sick': 1,
                    'holiday': 1,
                    'other': 0,
                    'missing': 6,
                },
                'avg_daily_hours': 7.2,
                'working_days': 20,
                'completeness': 80.0,
            }
        """
        
        total_net = 0
        total_gross = 0
        day_type_counts = {
            'work': 0,
            'vacation': 0,
            'sick': 0,
            'holiday': 0,
            'other': 0,
            'missing': 0
        }
        
        # Count entries by type
        for entry in entries:
            if entry.day_type == 'work':
                # Calculate time for this day
                calc_result = CalcService.calculate_work_time(
                    entry.start_time,
                    entry.end_time,
                    entry.break_minutes,
                    entry.day_type
                )
                total_net += calc_result['net_minutes']
                total_gross += calc_result['gross_minutes']
                day_type_counts['work'] += 1
            
            elif entry.day_type in ['vacation', 'sick', 'holiday', 'other']:
                day_type_counts[entry.day_type] += 1
            
            else:
                day_type_counts['missing'] += 1
        
        # Calculate averages
        avg_daily_hours = (total_gross / 60) / max(day_type_counts['work'], 1)
        total_days = len(entries)
        days_with_entry = sum(1 for e in entries if e.day_type != 'missing')
        completeness = (days_with_entry / total_days * 100) if total_days > 0 else 0
        
        return {
            'total_net_minutes': total_net,
            'total_net_formatted': CalcService.minutes_to_hm(total_net),
            'total_gross_minutes': total_gross,
            'total_gross_formatted': CalcService.minutes_to_hm(total_gross),
            'day_counts': day_type_counts,
            'avg_daily_hours': avg_daily_hours,
            'working_days': day_type_counts['work'],
            'completeness': completeness,
        }
```

---

## 2. VALIDATION API

### 2.1 Validators Module

```python
# src/utils/validators.py

import re
from datetime import datetime

class Validators:
    """Input validation functions"""
    
    @staticmethod
    def validate_date(date_str: str) -> tuple[bool, str]:
        """
        Validate YYYY-MM-DD format
        
        Returns: (is_valid: bool, error_message: str)
        """
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return False, f"Invalid date format: {date_str} (expected YYYY-MM-DD)"
        
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            # Optional: validate date is not in future
            if dt > datetime.now():
                return False, "Cannot log future dates"
            return True, ""
        except ValueError as e:
            return False, f"Invalid date: {date_str}"
    
    @staticmethod
    def validate_time(time_str: str) -> tuple[bool, str]:
        """
        Validate HH:MM format
        
        Returns: (is_valid: bool, error_message: str)
        """
        if not re.match(r'^\d{2}:\d{2}$', time_str):
            return False, f"Invalid time format: {time_str} (expected HH:MM)"
        
        h, m = map(int, time_str.split(':'))
        if not (0 <= h < 24 and 0 <= m < 60):
            return False, f"Invalid time values: {time_str}"
        
        return True, ""
    
    @staticmethod
    def validate_break_minutes(break_min: int) -> tuple[bool, str]:
        """Validate break duration"""
        if not isinstance(break_min, int):
            return False, "Break must be integer minutes"
        if break_min < 0:
            return False, "Break cannot be negative"
        if break_min > 480:  # 8 hours
            return False, "Break cannot exceed 8 hours"
        return True, ""
    
    @staticmethod
    def validate_day_type(day_type: str) -> tuple[bool, str]:
        """Validate day type enum"""
        valid_types = ['work', 'vacation', 'sick', 'holiday', 'other']
        if day_type not in valid_types:
            return False, f"Invalid day type: {day_type}"
        return True, ""
    
    @staticmethod
    def validate_notes(notes: str) -> tuple[bool, str]:
        """Validate notes field"""
        if len(notes) > 500:
            return False, "Notes cannot exceed 500 characters"
        return True, ""
    
    @staticmethod
    def validate_work_entry(entry: dict) -> tuple[bool, list]:
        """
        Validate complete work entry
        
        Returns: (is_valid: bool, error_list: list)
        
        Example:
            >>> entry = {
            ...     'date': '2026-02-04',
            ...     'start_time': '08:00',
            ...     'end_time': '17:00',
            ...     'break_minutes': 60,
            ...     'day_type': 'work',
            ...     'notes': 'Regular day'
            ... }
            >>> Validators.validate_work_entry(entry)
            (True, [])
        """
        errors = []
        
        # Validate each field
        if 'date' in entry:
            valid, msg = Validators.validate_date(entry['date'])
            if not valid:
                errors.append(msg)
        
        if entry.get('day_type') == 'work':
            # For work days, time fields required
            if 'start_time' in entry:
                valid, msg = Validators.validate_time(entry['start_time'])
                if not valid:
                    errors.append(msg)
            else:
                errors.append("Start time required for work day")
            
            if 'end_time' in entry:
                valid, msg = Validators.validate_time(entry['end_time'])
                if not valid:
                    errors.append(msg)
            else:
                errors.append("End time required for work day")
        
        if 'break_minutes' in entry:
            valid, msg = Validators.validate_break_minutes(entry['break_minutes'])
            if not valid:
                errors.append(msg)
        
        if 'day_type' in entry:
            valid, msg = Validators.validate_day_type(entry['day_type'])
            if not valid:
                errors.append(msg)
        
        if 'notes' in entry:
            valid, msg = Validators.validate_notes(entry['notes'])
            if not valid:
                errors.append(msg)
        
        return len(errors) == 0, errors
```

---

## 3. FORMATTER API

### 3.1 Formatters Module

```python
# src/utils/formatters.py

class Formatters:
    """Output formatting functions"""
    
    @staticmethod
    def format_duration(minutes: int) -> str:
        """
        Format minutes as HH:MM
        
        Examples:
            >>> Formatters.format_duration(480)
            '8:00'
            >>> Formatters.format_duration(510)
            '8:30'
        """
        h = minutes // 60
        m = minutes % 60
        return f"{h}:{m:02d}"
    
    @staticmethod
    def format_decimal_hours(minutes: int, decimals: int = 2) -> str:
        """
        Format minutes as decimal hours
        
        Examples:
            >>> Formatters.format_decimal_hours(480)
            '8.00'
            >>> Formatters.format_decimal_hours(510)
            '8.50'
        """
        hours = minutes / 60
        return f"{hours:.{decimals}f}"
    
    @staticmethod
    def format_date_readable(date_str: str, locale: str = 'pl') -> str:
        """
        Format date as readable string
        
        Examples:
            >>> Formatters.format_date_readable('2026-02-04')
            '4 lutego 2026'
        """
        from datetime import datetime
        
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        
        months_pl = {
            1: 'stycznia', 2: 'lutego', 3: 'marca',
            4: 'kwietnia', 5: 'maja', 6: 'czerwca',
            7: 'lipca', 8: 'sierpnia', 9: 'września',
            10: 'października', 11: 'listopada', 12: 'grudnia'
        }
        
        if locale == 'pl':
            return f"{dt.day} {months_pl[dt.month]} {dt.year}"
        else:
            return dt.strftime('%d %B %Y')
    
    @staticmethod
    def format_month_header(year: int, month: int) -> str:
        """
        Format month as header
        
        Examples:
            >>> Formatters.format_month_header(2026, 2)
            'Luty 2026'
        """
        from datetime import datetime
        
        months_pl = {
            1: 'Styczeń', 2: 'Luty', 3: 'Marzec',
            4: 'Kwiecień', 5: 'Maj', 6: 'Czerwiec',
            7: 'Lipiec', 8: 'Sierpień', 9: 'Wrzesień',
            10: 'Październik', 11: 'Listopad', 12: 'Grudzień'
        }
        
        return f"{months_pl[month]} {year}"
    
    @staticmethod
    def format_json(data: dict, indent: int = 2) -> str:
        """Format dict as pretty JSON"""
        import json
        return json.dumps(data, indent=indent, ensure_ascii=False)
```

---

## 4. CALCULATION EDGE CASES

### 4.1 Midnight Crossing

```
Scenario: Employee works 22:00 - 06:00

Input:
  start: "22:00"
  end: "06:00"

Calculation:
  start_dt = datetime(2026, 2, 4, 22, 0)
  end_dt = datetime(2026, 2, 4, 6, 0)
  
  if end_dt <= start_dt:
    end_dt += timedelta(days=1)  # Now: 2026-02-05 06:00
  
  delta = 2026-02-05 06:00 - 2026-02-04 22:00 = 8 hours = 480 minutes

Result:
  gross_minutes: 480
  gross_formatted: "8:00"
  net_minutes: 420 (minus 60min break)
  net_formatted: "7:00"
```

### 4.2 Missing Entry

```
Scenario: User forgets to log a day

Current: Date without entry shows:
  - Visual indicator (empty card, red border)
  - Status in dashboard: "Brak wpisu"
  - In report: day not included in summary

Recommendation: Send reminder notification
```

### 4.3 Partial Month

```
Scenario: February 2026 (29 days, leap year)

Logged 20 work days:
  - 1 vacation day
  - 1 sick day
  - 1 holiday
  - 6 unlogged days

Summary shows:
  - Completeness: 23/29 = 79.3%
  - Working days: 20
  - Total hours: correctly summed only from logged days
```

---

## 5. API ERROR HANDLING

### 5.1 Error Responses

```python
class APIError(Exception):
    """Base API error"""
    def __init__(self, code: str, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}

class ValidationError(APIError):
    """Validation failed"""
    pass

class NotFoundError(APIError):
    """Resource not found"""
    pass

class CalculationError(APIError):
    """Calculation failed"""
    pass

# Usage:
def calculate_work_time(entry):
    try:
        # calculation
        pass
    except CalculationError as e:
        return {
            'error': {
                'code': e.code,
                'message': e.message,
                'details': e.details
            }
        }
```

---

## 6. API RESPONSE EXAMPLES

### 6.1 Calculate Single Day

```json
{
  "request": {
    "date": "2026-02-04",
    "start_time": "08:30",
    "end_time": "17:15",
    "break_minutes": 60,
    "day_type": "work"
  },
  "response": {
    "gross_minutes": 495,
    "gross_formatted": "8:15",
    "net_minutes": 435,
    "net_formatted": "7:15",
    "is_valid": true,
    "errors": []
  }
}
```

### 6.2 Monthly Summary

```json
{
  "request": {
    "profile_id": 1,
    "year": 2026,
    "month": 2
  },
  "response": {
    "total_net_minutes": 8640,
    "total_net_formatted": "144:00",
    "total_gross_minutes": 8760,
    "total_gross_formatted": "146:00",
    "day_counts": {
      "work": 20,
      "vacation": 2,
      "sick": 1,
      "holiday": 1,
      "other": 0,
      "missing": 5
    },
    "avg_daily_hours": 7.2,
    "working_days": 20,
    "completeness": 82.8
  }
}
```

---

## 7. CALCULATION PERFORMANCE

### 7.1 Performance Benchmarks

```
Operation              | Expected Time | Comments
─────────────────────────────────────────────────────
Single calculation    | < 1ms         | Negligible
Monthly summary       | < 5ms         | All 30 entries
PDF generation        | < 500ms       | ReportLab
Month data load       | < 10ms        | DB query
```

### 7.2 Optimization Notes

- Calculations are stateless (pure functions)
- No external API calls
- Minimal memory footprint
- All operations run on main thread (safe for SQLite)

---

**NEXT:** UI Components Library + Testing Strategy + Build Pipeline
