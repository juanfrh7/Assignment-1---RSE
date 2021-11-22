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
    #create a collection
    collection = GlacierCollection(filepath1)
    collection.read_mass_balance_data(filepath2)

    #check when code is an integer
    assert collection.filter_by_code(638) == ['AGUA NEGRA', 'BROWN SUPERIOR', 'CONCONTA NORTE', 'LAGO DEL DESIERTO I', 
                                                'LAGO DEL DESIERTO II', 'LAGO DEL DESIERTO III', 'LOS AMARILLOS', 'POTRERILLOS', 
                                                'TORTOLAS', 'AMARILLO', 'NINGCHAN GLACIER NO.1', 'VESTRE MEMURUBREEN']

    #check when code is an string with no ?
    assert collection.filter_by_code('638') == ['AGUA NEGRA', 'BROWN SUPERIOR', 'CONCONTA NORTE', 'LAGO DEL DESIERTO I', 
                                                'LAGO DEL DESIERTO II', 'LAGO DEL DESIERTO III', 'LOS AMARILLOS', 'POTRERILLOS', 
                                                'TORTOLAS', 'AMARILLO', 'NINGCHAN GLACIER NO.1', 'VESTRE MEMURUBREEN']

    #check when code is an string with one ?
    assert collection.filter_by_code('6?8') == ['AGUA NEGRA', 'BROWN SUPERIOR', 'CANITO', 'CONCONTA NORTE', 'LAGO DEL DESIERTO I', 
                                                'LAGO DEL DESIERTO II', 'LAGO DEL DESIERTO III', 'LOS AMARILLOS', 'POTRERILLOS', 
                                                'TORTOLAS', 'ADLER', 'PERS, VADRET', 'AMARILLO', 'TRONQUITOS', 'NINGCHAN GLACIER NO.1', 
                                                'RULUNG', 'HALSJOKULL', 'BLAAISEN', 'VESTRE MEMURUBREEN']

    #check when code is an string with two ?
    assert collection.filter_by_code('6??') == ['GRAN CAMPO NEVADO (GCN)', 'DRANGAJOKULL ICE CAP', 'EIRIKSJOKULL', 'EYJAFJALLAJOKULL', 
                                                'HOFSJOKUL_EYSTRI', 'HOFSJOKULL ICE CAP', 'HRUTFELL', 'LANGJOKULL ICE CAP', 'MYRDALSJOKULL ICE CAP', 
                                                'ORAEFAJOKULL', 'SNAEFELLSJOKULL', 'THRANDARJOKULL', 'TINDFJALLAJOKULL', 'TORFAJOKULL', 
                                                'TUNGNAFELLSJOKULL', 'VATNAJOKULL', 'WESTERN VATNAJOKULL ICE CAP', 'MIDTRE FOLGEFONNA', 'NORDRE FOLGEFON', 
                                                'COROPUNA']
                                            
    #check when code is an string with three ?
    assert collection.filter_by_code('???') == collection.name

def test_sort_latest():
    #create a collection
    collection = GlacierCollection(filepath1)
    collection.read_mass_balance_data(filepath2)

    #check when reverse is true
    x = collection.sort_by_latest_mass_balance(1, reverse = True)
    assert x[0].name == 'ARTESONRAJU'

    #check when reverse is true
    x = collection.sort_by_latest_mass_balance(1, reverse = False)
    assert x[0].name == 'STORSTEINSFJELLBREEN'
    