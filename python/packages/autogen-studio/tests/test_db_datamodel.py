from datetime import datetime, timezone
import pytest
from autogenstudio.datamodel.db import Session

def test_parse_datetime_with_datetime():
    """Test parse_datetime with a datetime object"""
    dt = datetime.now()
    result = Session.parse_datetime(dt)
    assert result == dt
    assert isinstance(result, datetime)

def test_parse_datetime_with_iso_string():
    """Test parse_datetime with an ISO format string"""
    iso_string = "2023-10-27T10:00:00"
    result = Session.parse_datetime(iso_string)
    assert result == datetime.fromisoformat(iso_string)
    assert isinstance(result, datetime)

def test_parse_datetime_with_z_string():
    """Test parse_datetime with an ISO string containing 'Z'"""
    z_string = "2023-10-27T10:00:00Z"
    result = Session.parse_datetime(z_string)
    expected = datetime.fromisoformat("2023-10-27T10:00:00+00:00")
    assert result == expected
    assert result.tzinfo == timezone.utc

def test_parse_datetime_with_offset_string():
    """Test parse_datetime with an ISO string containing an offset"""
    offset_string = "2023-10-27T10:00:00+02:00"
    result = Session.parse_datetime(offset_string)
    expected = datetime.fromisoformat(offset_string)
    assert result == expected
    assert result.utcoffset().total_seconds() == 2 * 3600

def test_parse_datetime_invalid_string():
    """Test parse_datetime with an invalid string (should raise ValueError)"""
    invalid_string = "not-a-date"
    with pytest.raises(ValueError):
        Session.parse_datetime(invalid_string)
