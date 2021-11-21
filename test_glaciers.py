import pytest
import glaciers
from glaciers import Glacier, GlacierCollection

def test_error_messages():
    #define variables
    glacier_id = '17363'
    name = 'Any name'
    unit = 'FG'
    lat = 30
    lon = 39.87
    code = 638

    #create a glacier object with the variables
    example = Glacier(glacier_id, name, unit, lat, lon, code)

    #assert that it outputs the correct data
    assert example.glacier_id == glacier_id
    assert example.name == name
    assert example.unit == unit
    assert example.lat == lat
    assert example.lon == lon
    assert example.code == code

def test_add_mass_balance():
    raise NotImplementedError

def test_filter_code():
    raise NotImplementedError

def test_sort_latest():
    raise NotImplementedError