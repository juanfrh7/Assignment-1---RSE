import pathlib
from pathlib import Path
import matplotlib.pyplot as plt
import csv

class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):
        #initialise the data
        self.glacier_id = glacier_id
        self.name = name
        self.unit = unit
        self.lat = lat
        self.lon = lon
        self.code = code
        self.years = []
        self.mass_balance = []

    def add_mass_balance_measurement(self, year, mass_balance, boolean):
        raise NotImplementedError

    def plot_mass_balance(self, output_path):
        raise NotImplementedError

        
class GlacierCollection:

    def __init__(self, file_path):
        #initialize the data
        self.glacier_ids = []   #list of all the glacier ids
        self.glacier_classes = []   #list of all the glacier objects
        self.name = []   #list of all the glacier names
        self.latitude_list = []   #list of all the glacier latitudes
        self.longitude_list = []   #list of all the glacier longitudes
        self.code = []   #list of all the glacier codes
        self.units = []   #list of all the glacier units
        self.year = []   #list of all the glacier years
        self.mass_balance = []   #list of all the glacier mass_balances

    def read_mass_balance_data(self, file_path):
        raise NotImplementedError

    def find_nearest(self, lat, lon, n):
        """Get the n glaciers closest to the given coordinates."""
        raise NotImplementedError
    
    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        raise NotImplementedError

    def sort_by_latest_mass_balance(self, n, reverse):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        raise NotImplementedError

    def summary(self):
        raise NotImplementedError

    def plot_extremes(self, output_path):
        raise NotImplementedError
