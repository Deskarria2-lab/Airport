                                            #   Airport Project Version 1.0
                                            #   Airport functions file
#   "Libraries" From our project!
########################################
from config import sch_list as sch_list                                     #sch_list is a schengen airport's list
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
def TryFormat(airport):
    #   ICAO Validation Format, if it's not and string || it's too short or longer to be a ICAO code
    if not(isinstance(airport.icao, str) and len(airport.icao) == 4):        #   Checks if it's and str
        raise Exception("Invalid icao format, needs to be a string!")
    elif not(len(airport.icao) == 4):                                       #   Checks if it's len 4
        raise Exception("Invalid icao format, needs to be a string with len 4!")
    #   If it's all right, check's the lat and lon value
    else:
        try:
            #   Excep in the case that you put in lat/lon a Boolean value!
            if isinstance(airport.lat, bool) or isinstance(airport.lon, bool):
                raise ValueError("Latitude and Longitude must be numbers, not boolean")
            else:
                airport.lat = float(airport.lat)                            # Pass the format to float
                airport.lon = float(airport.lon)                            # Pass the format to a float
            #In case that you can't pass to float type, give and advice and stop the process!
        except (ValueError, TypeError):
            raise ValueError("Invalid lat/lon Format, needs to be a number!")
    return True                                                             #   If it's all right return a True

                            #   Function to check if the airport it's schengen  #
def IsSchengenAirport(icao):
    icao = icao[:2].upper()                                                 #   Get the two first terms of ICAO and make it UPPER
    if icao in sch_list:                                                    #   Compare ICAO to the Schengen contr list
        return True                                                         #   If it's sch, return True
    else:
        return False                                                        #   If not, return False

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
        airports.append([icao, lat, lon])                                   #   Append the data in airports list
        lines = file.readline()                                             #   Next Line to reed
    file.close()                                                            #   Close the file
    return airports                                                         #   Return's a vect airports with all data

                                #   Save sch airports in txt file!  #
def SaveSchengenAirports(airports, filename):
    file = open(filename, "w")                                              #   Write in the txt specific file
    i = 0                                                                   #   Counter
    while i < len(airports):                                                #   While the count is < len of airport list
        if IsSchengenAirport(airports[i][0]):                               #   Cheks if a specific airport is sch
            line = (airports[i][0] + "\t"                                   #   Creates the var line to write in file!
                    + str(airports[i][1]) + "\t"
                    + str(airports[i][2]) + "\n")
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
    print(airport.icao)
    while i < len(airports) and find == False:                              #   While not len and not find the airp check
        if str(airport.icao) == airports[i][0]:                                  #   It's the airport here?
            find = True                                                     #   If yes, STOP
        else: pass                                                          #   If not, pass
        i += 1                                                              #   Go next line
    if not find:                                                            #   If you don't find it, add the airport
        airports.append([airport.icao, airport.lat, airport.lon])
    else: pass
    return airports

                                #   Remove an Airport from the airports list  #
def RemoveAirport(airports, icao):
    i = 0                                                                   #   Counter to 0
    print(airports[0][0])
    while i < len(airports):                                                #   While not len
        if icao == str(airports[i][0]):                                     #   If Icao code is in the list
            airports.remove(airports[i])                                    #   Remove
            break                                                           #   STOP ALL, GO OUT
        else:
            pass
        i += 1
    return airports

def PlotAirport(airports):
    sch_list = 0
    n_sch_list = 0
    i = 0
    while i < len(airports):
        if IsSchengenAirport(airports[i][0]):
            sch_list += 1
        else:
            n_sch_list += 1
        i += 1
    x = ["Schengen", "Not Schengen", "All Airports"]
    y = [sch_list, n_sch_list, i]
    fig, ax = plt.subplots()
    ax.bar(x=x, height=y)
    plt.ylabel("Airports")
    plt.show()
def MapAirport(airports):
    kml = simplekml.Kml()
    i = 0
    while i < len(airports):
        pnt = kml.newpoint(name=airports[i][0], coords=[(airports[i][2], airports[i][1])])
        if IsSchengenAirport(airports[i][0]):
            pnt.style.labelstyle.color = simplekml.Color.green
        else:
            pnt.style.labelstyle.color = simplekml.Color.red
        i += 1
    kml.save("airports_google_earth.kml")