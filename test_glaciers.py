import pytest
import glaciers
from glaciers import Glacier, GlacierCollection

location = ''
filepath1 = Path(location + 'sheet-A.csv')
filepath2 = Path(location + 'sheet-EE.csv')

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
    #create a collection
    collection = GlacierCollection(filepath1)
    collection.read_mass_balance_data(filepath2)

    #check for the glacier Agua Negra which has partial and total measurements for 2018 and 2019
    assert collection.glacier_classes[0].mass_balance == [-793.0, -418.0, 332.0, -7886.0, -2397.0, -13331.0]

def test_filter_code():
    raise NotImplementedError

def test_sort_latest():
    raise NotImplementedError