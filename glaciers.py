import pathlib
from pathlib import Path
import matplotlib.pyplot as plt
import csv
import datetime
import utils
from utils import haversine_distance

location = ''
filepath1 = Path(location + 'sheet-A.csv')
filepath2 = Path(location + 'sheet-EE.csv')

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

        #Define type errors
        if not isinstance(glacier_id, str):
            raise TypeError("glacier id should be a string")
        
        if not isinstance(name, str):
            raise TypeError("name should be a string")
        
        if not isinstance(unit, str):
            raise TypeError("unit should be a string")
        

        #Raise value errors
        if len(self.glacier_id) != 5:
            raise ValueError("The Glacier ID should be a 5 digit string")
            
        if not -90.0 <= lat <= 90.0:
            raise ValueError("The latitude is not within the accepted range [-90, 90]")
            
        if not -180 <= lon <= 180:
            raise ValueError("The longitude is not within the accepted range [-180, 180]")
            
        if unit != '99':
            if unit.upper() != unit:
                raise ValueError("The unit should be in capital letters")

        if len(unit) != 2:
            raise ValueError("The unit should be a 2 string")

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
        """Plot the mass balance measurements againts the years"""
        
        #Define the variables
        x = self.years
        y = self.mass_balance
        glacier = self.name
        glacier_id = self.glacier_id
        
        #if there are not mass balance measurements for the glacier, return message
        if self.years == []:
            return 'No mass balance data for glacier ' + glacier + ' with id ' + glacier_id
        
        plt.plot(x, y)
        plt.xlabel("Years")
        plt.ylabel("Mass balance [mm.w.e]")
        plt.title('Mass balance measurement for ' + glacier + ' with ID ' + glacier_id)
        plt.savefig(output_path + 'mass_balance.png')
        
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
                if year > datetime.datetime.now().year:
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

    def find_nearest(self, lat, lon, n = 5):
        """Get the n glaciers closest to the given coordinates."""

        #Raise value errors
        if not -90.0 <= lat <= 90.0:
            raise ValueError("The latitude is not within the accepted range [-90, 90]")
            
        if not -180 <= lon <= 180:
            raise ValueError("The longitude is not within the accepted range [-180, 180]")

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
        list_names = []   #list of names given its code
        list_of_digits = [str(d) for d in str(code_pattern)]   #list of the code's digits 
        count = list_of_digits.count('?')   #number of times ? appears in the code
        
        #Case 1 = ? does not appear in the code
        if count == 0:
            for i in range(len(self.code)):
                if list_of_digits[0] == self.code[i][0] and list_of_digits[1] == self.code[i][1] and list_of_digits[2] == self.code[i][2]:
                    list_names.append(self.name[i])
                    
        #Case 2 = ? appears once in the code           
        elif count == 1:
            indices = []
            for i in range(len(list_of_digits)):
                if list_of_digits[i] != '?':
                    indices.append(i)
                    
            for i in range(len(self.code)):
                if list_of_digits[indices[0]] == self.code[i][indices[0]] and list_of_digits[indices[1]] == self.code[i][indices[1]]:
                    list_names.append(self.name[i])
                    
        #Case 3 = ? appears twice in the code              
        elif count == 2:
            indices = []
            for i in range(len(list_of_digits)):
                if list_of_digits[i] != '?':
                    indices.append(i)
                    
            for i in range(len(self.code)):
                if list_of_digits[indices[0]] == self.code[i][indices[0]]:
                    list_names.append(self.name[i])

        #Case 3 = we have a ??? code           
        else:
            list_names = self.name

        return list_names

    def sort_by_latest_mass_balance(self, n, reverse):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        last_mass_balance_measurement = []   #list of last mass balance measurement per glacier
        
        #get all the values to the list
        for i in range(len(self.glacier_classes)):
            if self.glacier_classes[i].mass_balance == []:
                continue
            else:
                last_mass_balance_measurement.append([i, self.glacier_classes[i].mass_balance[-1]])

        
        #sort the lists in increasing order
        last_mass_balance_measurement.sort(key=lambda tup: tup[1])
        
        list_of_classes = []
        for i in range(1, n+1):
            
            #retrieve the n classes with smallest change
            if reverse == True:
                list_of_classes.append(self.glacier_classes[last_mass_balance_measurement[i-1][0]])

            #retrieve the n classes with greatest change
            else:
                list_of_classes.append(self.glacier_classes[last_mass_balance_measurement[-i][0]])

        return list_of_classes

    def summary(self):
        number_glaciers = str(len(self.name))  #get the number of glaciers
        year = str(min(self.year))  #get the earliest year measurement
        mass_balances = []
        count = 0   #frequency of negative mass balance measurement
        total = 0   #total number of mass balanace measurements
        
        #iterate over all glaciers to get the frequency
        for i in range(len(self.glacier_classes)):
            if self.glacier_classes[i].mass_balance == []:
                continue
            else:
                if self.glacier_classes[i].mass_balance[-1] < 0:
                    count += 1
                    total += 1
                else:
                    total += 1
        
        #calculate the percentage
        percentage = str(int(((count / total)* 100)))
        
        return('This collection has ' + number_glaciers + ' glaciers',
                'The earliest measurement was in ' + year,
               percentage + '% of glaciers shrunk in their last measurement.')

    def plot_extremes(self, output_path):
        
        #get the glacier objects that shrunk and grew the most
        glacier_growth = self.sort_by_latest_mass_balance(1, reverse = False)
        glacier_shrunk = self.sort_by_latest_mass_balance(1, reverse = True)

        #Define the variables for the glacier that grew the most
        y1 = glacier_growth[0].mass_balance
        x1 = glacier_growth[0].years
        glacier1 = glacier_growth[0].name
        
        #Define the variables for the glacier that shrunk the most
        y2 = glacier_shrunk[0].mass_balance
        x2 = glacier_shrunk[0].years
        glacier2 = glacier_shrunk[0].name
        
        #plot everything
        plt.plot(x1, y1, label = glacier1 + ' is the glacier that grew the most')
        plt.plot(x2, y2, label = glacier2 + ' is the glacier that shrunk the most')
        plt.xlabel("Years")
        plt.ylabel("Mass balance [mm.w.e]")
        plt.title('Extreme glaciers in the collection')
        plt.legend()
        plt.savefig(output_path + 'plot_extremes.png')
