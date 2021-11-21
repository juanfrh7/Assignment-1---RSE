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
    """Add the mass balance measurements depending if its partial or total measurements"""
        
        #if the year is recorded, we check if the previous value is partial or total measurement
        if year in self.years:
            index = self.years.index(year)
            
            #if its a total measurement, we dont append
            if self.mass_balance[index] == True:
                return
            
            #if its a partial measurement, we check if the new value is partial or total measurement
            else:
                
                #if it's total, we ignore it assuming it appears at the end
                if boolean == True:
                    return

                #if it's partial, we add it to the previous value
                else:
                    self.mass_balance[index] = self.mass_balance[index] + mass_balance
                    
        #if year is not recorded, we append the new values
        else:
            self.years.append(year)
            self.mass_balance.append(mass_balance)

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

        #load the data from sheet A
        with open(file_path, encoding = "utf8") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter = ',')
            for row in csv_reader:
                id_glacier = str(row['WGMS_ID'])
                name = str(row['NAME'])
                unit = str(row['POLITICAL_UNIT'])
                lat = float(row['LATITUDE'])
                lon = float(row['LONGITUDE'])
                prim_class = str(row['PRIM_CLASSIFIC'])
                form = str(row['FORM'])
                frontal_chars = str(row['FRONTAL_CHARS'])
                code = prim_class + form + frontal_chars
                    
                #append values to a list
                self.name.append(name)
                self.glacier_ids.append(id_glacier)
                self.latitude_list.append(lat)
                self.longitude_list.append(lon)
                self.code.append(code)
                self.units.append(unit)
                self.glacier_classes.append(Glacier(id_glacier, name, unit, lat, lon, code))

    def read_mass_balance_data(self, file_path):
        """Load the data from sheet EE""" 

        #load the data
        with open(file_path, encoding = "utf8") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter = ',')
            for row in csv_reader:
                glacier_id = str(row['WGMS_ID'])
                year = int(row['YEAR'])
                bound = str(row['LOWER_BOUND'])
                mass_balance = row['ANNUAL_BALANCE']
                
                if not isinstance(year, int):
                    raise TypeError("year should be an integer")
                    
                #if year is in the future, raise error
                if year > 2022:
                    raise ValueError("The year is in the future")
        
                #do not take into account empty mass balance measurements
                if mass_balance == '':
                    continue
                    
                #append data to list
                self.year.append(year)
                self.mass_balance.append(float(mass_balance))

                boolean = False
                if bound == '9999':
                    boolean = True
                       
                #append mass balance measurement to each glacier object
                if glacier_id in self.glacier_ids:
                    index1 = self.glacier_ids.index(glacier_id)
                    self.glacier_classes[index1].add_mass_balance_measurement(year, float(mass_balance), boolean)

    def find_nearest(self, lat, lon, n):
        """Get the n glaciers closest to the given coordinates."""
        
        distances = []   #list of all the distances to the given coordinates
        
        for i in range(len(self.latitude_list)):
            #calculate the distance using the haversine distance function
            distance = haversine_distance(lat, lon, self.latitude_list[i], self.longitude_list[i])
            distances.append((self.name[i], distance))

        #sort the list of distances
        distances.sort(key=lambda tup: tup[1])
        
        neighbors = []   #list of closest neighbours
        
        #append the n closest neighbors to the list
        for i in range(n):
            neighbors.append(distances[i][0])

        return neighbors
    
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
