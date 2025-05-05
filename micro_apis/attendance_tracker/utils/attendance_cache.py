from datetime import date, datetime
from typing import Dict, List, Optional

# In-memory cache for attendance records
_attendance_cache: Dict[str, List[Dict]] = {}

def get_cached_attendance(date_str: str) -> Optional[List[Dict]]:
    """Retrieve cached attendance records for a specific date"""
    return _attendance_cache.get(date_str)

def cache_attendance(date_str: str, records: List[Dict]) -> None:
    """Cache attendance records for a specific date"""
    _attendance_cache[date_str] = records

def clear_cache() -> None:
    """Clear the entire attendance cache"""
    _attendance_cache.clear()

def format_date(dt: date) -> str:
    """Format a date object to YYYY-MM-DD string"""
    return dt.strftime("%Y-%m-%d")

def parse_date(date_str: str) -> date:
    """Parse a date string in YYYY-MM-DD format"""
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def get_today_str() -> str:
    """Get today's date as a string"""
    return format_date(date.today())
