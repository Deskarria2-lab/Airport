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
def IsSchengenAirport(icao):
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
def SetSchengen(airport):
    airport.schengen = IsSchengenAirport(airport.icao)                      #   Change the sch atr of the airport obj

                                    #   Print Airports on screen  #
def PrintAirport(airport):
    print("ICAO: " + airport.icao,                                          #   Print all airport data's
          "Schengen: " + str(airport.schengen),
          "Coordenadas: " + str(airport.lat),
          " , " + str(airport.lon))

                            #   Load Airports from txt file (V0.0)  #
def LoadAirports(filename):   #PARA REVISAR!!!! BASTANTE POCHO!!!!
    file = open(filename, "r")                                              #   Load the txt airport file
    next(file)                                                              #   Ignore the first line
    lines = file.readline()                                                 #   Defines the var lines
    airports = []                                                           #   Create Airport list
    while lines != "":                                                      #   while line is not empty
        airport = Airport("None", 0, 0)
        elem = lines.strip("\t")                                            #   Var elem that strips a line
        elem = elem.split(" ")                                              #   Strip empty space, vector 3 value
        icao = elem[0]                                                      #   ICAO is elem 1 of vect elem
        lat = elem[1][1:7]                                                  #   Lat is elem 2, starts in 1 and end's in 7
        lat = int(lat[0:2]) + int(lat[2:4])/60 + int(lat[4:6])/3600         #   Calculate lat
        lon = elem[2][1:8]                                                  #   Lon is elem 3, starts in 1 and end's in 7
        lon = int(lon[1:3]) + int(lon[3:5])/60 + int(lon[5:7])/3600         #   Calculate lon
        if elem[1][0] == 'S':                                               #   If lat is in South
            lat = -lat                                                      #   Negate it, oposite direction!
        if elem[2][0] == 'W':                                               #   If lon is in West
            lon = -lon                                                      #   Negate it, oposite direction!
        airport.icao = icao
        airport.lat = lat
        airport.lon = lon
        TryFormat(airport)
        airports.append(airport)                                            #   Append the data in airports list
        lines = file.readline()                                             #   Next Line to reed
    file.close()                                                            #   Close the file
    return airports                                                      #   Return's a vect airports with all data

                                #   Save sch airports in txt file!  #
def SaveSchengenAirports(airports, filename):
    file = open(filename, "w")                                              #   Write in the txt specific file
    i = 0                                                                   #   Counter
    while i < len(airports):                                                #   While the count is < len of airport list
        if IsSchengenAirport(str(airports[i])):                                  #   Cheks if a specific airport is sch
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
def AddAirport(airports, airport):
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
def RemoveAirport(airports, icao):
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
def PlotAirport(airports):
    sch_list = 0
    n_sch_list = 0
    i = 0
    while i < len(airports):
        if IsSchengenAirport(str(airports[i].icao)):
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

def MapAirport(airports):
    kml = simplekml.Kml()
    i = 0
    while i < len(airports):
        pnt = kml.newpoint(name=str(airports[i].icao), coords=[(airports[i].lon, airports[i].lat)])
        if IsSchengenAirport(str(airports[i].icao)):
            pnt.style.labelstyle.color = simplekml.Color.green
            # pnt.style.iconstyle.icon.href = "schengen-Photoroom.png"          PARA FUTURO
        else:
            pnt.style.labelstyle.color = simplekml.Color.red
        i += 1
    kml.save("airports_google_earth.kml")
    print("Map Airports Done")