                                            #   Airport Project Version 2.0
                                            #   Airport functions file
#   "Libraries" From our project!
########################################
from SRC.miscellaneus.config import sch_list                                            #sch_list is a schengen airport's list
from SRC.miscellaneus.security import TryFormat
########################################
#   External Libraries!
########################################
from matplotlib import pyplot as plt
import simplekml
########################################

                                            #   Airport Class   #
class Airport:
    def __init__(self, icao,lat, lon):
        self.icao = icao                #   Atr ICAO code
        self.lat = lat                  #   Atr Latitude
        self.lon = lon                  #   Atr Longitude
        self.schengen = False           #   Private Atr Schengen

                                            #   Format checker  #

                            #   Function to check if the airport it's schengen  #
def is_schengen_airport(icao):
    icao = icao[:2].upper()                                                     # Select first 2 letters and put it on Mayusc
    i = 0                                                                       # Counter
    found = False
    while i < len(sch_list) and not found:                                     # While the count is <= lenght and not found
        if icao == sch_list[i][:2]:                                              # Checks if the icao is on the schengen list
            found = True                                                        # If it's on the list, found = True and finish the while
        else:
            pass                                                                # If it's not, pass and try on the next line
        i += 1                                                                  # For trying the next line, sum up 1 to the counter
    if found:                                                                   # Once out the while, if found we assing the schengen atribute true
        return True
    else:                                                                       # If not found, we assing the shcengen atribute false
        return False                                                      #   If not, return False

                            #   Function to set an airport sch atr True  #
def set_schengen(airport):
    airport.schengen = is_schengen_airport(airport.icao)                      #   Change the sch atr of the airport obj

                                    #   Print Airports on screen  #
def print_airport(airport):
    print("ICAO: " + airport.icao,                                          #   Print all airport data's
          "Schengen: " + str(airport.schengen),
          "Coordenadas: " + str(airport.lat),
          " , " + str(airport.lon))

                            #   Load Airports from txt file (V0.0)  #
def load_airports(filename):
    try:
        file = open(filename, "r")                                          #   Open the txt airport file
    except FileNotFoundError:
        return []                                                           #   File not found: return empty list
    next(file)                                                              #   Ignore header line
    lines = file.readline()                                                 #   Read first data line
    airports = []                                                           #   Create airport list
    while lines != "":                                                      #   While line is not empty
        line_clean = lines.strip()                                          #   Remove leading/trailing whitespace
        if line_clean != "":                                                #   Skip blank lines
            elem = line_clean.split()                                       #   FIXED: split() handles any whitespace
            if len(elem) >= 3:                                              #   Only process well-formed lines
                try:
                    icao = elem[0]                                          #   ICAO code
                    lat_str = elem[1]                                       #   Latitude string e.g. N413456
                    lon_str = elem[2]                                       #   Longitude string e.g. W0823456
                    lat_digits = lat_str[1:7]                               #   Extract 6 digits after N/S
                    lat = int(lat_digits[0:2]) + int(lat_digits[2:4])/60 + int(lat_digits[4:6])/3600
                    lon_digits = lon_str[1:8]                               #   Extract 7 digits after E/W
                    lon = int(lon_digits[0:3]) + int(lon_digits[3:5])/60 + int(lon_digits[5:7])/3600
                    if lat_str[0] == 'S':                                   #   South → negative latitude
                        lat = -lat
                    if lon_str[0] == 'W':                                   #   West → negative longitude
                        lon = -lon
                    airport = Airport(icao, lat, lon)                       #   Create Airport object
                    TryFormat(airport)                                      #   Validate format
                    set_schengen(airport)                                   #   FIXED: set Schengen on load
                    airports.append(airport)                                #   Add to list
                except Exception:                                           #   Skip malformed lines silently
                    pass
        lines = file.readline()                                             #   Advance to next line
    file.close()                                                            #   Close the file
    return airports                                                         #   Return list of airports

                                #   Save sch airports in txt file!  #
def save_schengen_airports(airports, filename):
    file = open(filename, "w")                                              #   Write in the txt specific file
    i = 0                                                                   #   Counter
    while i < len(airports):                                                #   While the count is < len of airport list
        if is_schengen_airport(str(airports[i])):                                  #   Cheks if a specific airport is sch
            line = (airports[i].icao + "\t"                                 #   Creates the var line to write in file!
                    + str(airports[i].lat) + "\t"
                    + str(airports[i].lon) + "\n")
            file.write(line)                                                #   Write the airport information in the list

        else:                                                               #   If not
            pass                                                            #   Do Nothing :)
        i += 1
    file.close()                                                            #   Close the file!
    return airports

                                #   Add an Airport to the airports list  #
def add_airport(airports, airport):
    find = False                                                            #   Set a find variable in false
    i = 0                                                                   #   Counter to 0
    TryFormat(airport)
    print(airport.icao)
    while i < len(airports) and find == False:                              #   While not len and not find the airp check
        if str(airport.icao) == str(airports[i].icao):                                  #   It's the airport here?
            find = True                                                     #   If yes, STOP
        else: pass                                                          #   If not, pass
        i += 1                                                              #   Go next line
    if not find:                                                            #   If you don't find it, add the airport
        airports.append(airport)
    else: pass
    return airports

                                #   Remove an Airport from the airports list  #
def remove_airport(airports, icao):
    i = 0                                                                   #   Counter to 0
    while i < len(airports):                                                #   While not len
        if icao == str(airports[i].icao):                                     #   If Icao code is in the list
            airports.remove(airports[i])                                    #   Remove NO
            break                                                           #   STOP ALL, GO OUT
        else:
            pass
        i += 1
    return airports

                                #   Change!!!!!
def plot_airport(airports):
    sch_list = 0
    n_sch_list = 0
    i = 0
    while i < len(airports):
        if is_schengen_airport(str(airports[i].icao)):
            sch_list += 1
        else:
            n_sch_list += 1
        i += 1
    x = "Airports"
    y = [sch_list, n_sch_list]
    fig, ax = plt.subplots()
    ax.bar(x,y)
    # plt.ylabel("Airports")
    plt.show()

def map_airport(airports):
    try:
        kml = simplekml.Kml()
        i = 0
        while i < len(airports):
            pnt = kml.newpoint(name=str(airports[i].icao), coords=[(airports[i].lon, airports[i].lat)])
            if is_schengen_airport(str(airports[i].icao)):
                pnt.style.labelstyle.color = simplekml.Color.green
                # pnt.style.iconstyle.icon.href = "schengen-Photoroom.png"          PARA FUTURO
            else:
                pnt.style.labelstyle.color = simplekml.Color.red
            i += 1
        kml.save("airports_google_earth.kml")
        print("Map Airports Done")
    except Exception as e: return -1