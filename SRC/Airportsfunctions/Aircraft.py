from SRC.Airportsfunctions.Airport import *  #   Aircraft functions file

#   "Libraries" From our project!
########################################
from SRC.Airportsfunctions.Airport import *
########################################
#   External Libraries!
########################################
import matplotlib.pyplot as plt
import math
########################################

####################################################    Aircraft Class  ####################################################################
class Aircraft:
    def __init__(self, id, airline, origin, arrival_time):
        self.id = id                                                    #   ID del Avion
        self.airline = airline                                          #   Aerolinea Asociada
        self.origin = origin                                            #   Origen del Avion
        self.arrival_time = arrival_time                                #   Hora de llegada

####################################################    Load Arrivals   #######################################################################
def LoadArrivals(filename):
    file = open(filename, "r")                                                                  #   Carga el archivo .txt
    next(file)                                                                                  #   Ignore the first line
    lines = file.readline()                                                                     #   Defines the var lines
    aircraft_list = []                                                                          #   Creamos la lista de Aviones
    while lines != "":                                                                          #   Mientras no hayan lineas vacias
        aircrafts = Aircraft("None", "None", 0, "None")
        elem = lines.strip("\t")                                                                #
        elem = elem.split(" ")                                                                  #
        id = elem[0]                                                                            #
        origin = elem[1]                                                                        #
        arrival_time = elem[2]                                                                  #
        airline = elem[3]                                                                       #

        aircrafts.id = id                                                                       #
        aircrafts.airline = airline                                                             #
        aircrafts.origin = origin                                                               #
        aircrafts.arrival_time = arrival_time                                                   #

        aircraft_list.append(aircrafts)                                                         #
        lines = file.readline()                                                                 #
    file.close()                                                                                #   Cierra el programa
    return aircraft_list                                                                        #   Devuelve la lista de Aviones

def PlotArrivals(aircraft_list):
    if len(aircraft_list) == 0:
        print("Error: La lista de vuelos está vacía.")
        return
    h_cont = [0] * 24
    i=0
    while i < len(aircraft_list):
        aircraft = aircraft_list[i]
        partes_hora = aircraft.arrival_time.split(':')
        hora_entera = int(partes_hora[0])
        if 0 <= hora_entera < 24:
            h_cont[hora_entera] += 1
        i += 1

    horas = list(range(24))
    plt.bar(horas, h_cont, color='blue')
    plt.title("Frecuencia de Aterrizajes por Hora")
    plt.xlabel("Hora")
    plt.ylabel("Número de aviones")
    plt.xticks(horas)
    plt.show()

def SaveFlights(aircraft_list, filename):                               #Casi good
    if len(aircraft_list) == 0:
        print("ERROR: La lista de aviones está vacía. No se puede crear el archivo.")
        return -1 # Devolvemos un código de error (por ejemplo -1)
    try:
        with open(filename, "w") as f:
            f.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE2\n")
            i = 0
            while i < len(aircraft_list):
                aircraft = aircraft_list[i]
                id_aircraft = aircraft.id if aircraft.id else "-"
                origin = aircraft.origin if aircraft.origin else "-"
                arrival = aircraft.arrival_time if aircraft.arrival_time else "-"
                airline = aircraft.airline if aircraft.airline else "-"
                line = f"{id_aircraft} {origin} {arrival} {airline}\n"
                f.write(line)
                i += 1
        print(f"Archivo '{filename}' guardado correctamente.")
        return 0  # Éxito
    except FileNotFoundError: print("Error")

def PlotAirlines (aircraft_list):
    if not aircraft_list:
        print ("Error: No hay datos para graficar.")
        return

    airlines_list = {}
    for avion in aircraft_list:
        airline = avion.airline

        if airline in airlines_list:
            airlines_list[airline] += 1
        else:
            airlines_list[airline] = 1

    eje_x = list(airlines_list.keys())
    eje_y = list(airlines_list.values())

    plt.bar(eje_x, eje_y, color='blue', edgecolor='black')
    plt.title('Frecuencia de vuelos por aerolinea')
    plt.xlabel('Aerolinea (ICAO)')
    plt.ylabel('Numero de vuelos')
    plt.show()

def PlotFlighType (aircraft_list):
    if not aircraft_list:
        print("Error: No hay datos para graficar.")
        return
    flights_sch = 0
    flights_nsch = 0

    for avion in aircraft_list:
        if IsSchengenAirport (avion.origin):
            flights_sch += 1
        else:
            flights_nsch += 1
    categoria_x = ["Vuelos totales a LEBL"]

    plt.bar(categoria_x, [flights_sch], label ="Schengen", color='blue')
    plt.bar(categoria_x, [flights_nsch], bottom = [flights_sch], label ="No Schengen", color='red')
    plt.title('Proporcion Schengen vs No Schengen')
    plt.ylabel('Numero de llegadas')
    plt.legend()
    plt.show()

def MapFlights(aircrafts):

    f = open("mis_vuelos.kml", "w") # Creo el archivo

    # Cabecera KML, escribo el inicio
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')

    #Recorrer la lista de aviones
    i = 0

    while i < len(airport_list):
        flight = aircrafts[i]  # Cogemos el avión actual

        f.write('<Placemark>\n')
        f.write(f'<name>Vuelo {flight.id}</name>\n')
        f.write('<LineString>\n')
        f.write('<coordinates>\n')
        # Escribimos: Longitud, Latitud del origen y luego del destino
        f.write(f'{airport_list[i].lon},{airport_list[i].lat},0\n')
        f.write(f'{'2.085'},{'41.2971'},0\n')
        f.write('</coordinates>\n')
        f.write('</LineString>\n')
        f.write('</Placemark>\n')

        i = i + 1 # Pasamos al siguiente avión

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()

def Haversine(lat1, lon1, lat2, lon2):
    r = 6371 #Radio Tierra
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c

def LongDistanceArrivals(aircrafts):
    # Coordenadas de Barcelona (LEBL)
    lebl_lat = 41.297445
    lebl_lon = 2.0832941
    lista_especial = [] # Lista para guardar los aviones de más de 2000km
    i = 0

    while i < len(aircrafts):
        codigo_origen = aircrafts[i].origin

        # Buscamos el objeto aeropuerto que coincide con el origen del vuelo
        j = 0
        encontrado = False
        while j < len(airport_list) and not encontrado:
            if airport_list[j].icao == codigo_origen:
                # Si lo encontramos, calculamos la distancia
                dist = Haversine(airport_list[j].lat, airport_list[j].lon, lebl_lat, lebl_lon)

                # Si la distancia es mayor a 2000 km, lo añadimos a la lista
                if dist > 2000:
                    lista_especial.append(aircrafts[i])
                encontrado = True  # Para saber que ya hemos procesado este avión
            j = j + 1
        i = i + 1

    return lista_especial

if __name__ == "__main__":

    airport_list = LoadAirports('../../Files/Airports.txt')
    print(airport_list)
    aircraft_list = LoadArrivals('../../Files/Arrivals.txt')
    print(aircraft_list)

    PlotArrivals(aircraft_list)
    SaveFlights(aircraft_list, '../../Files/SaveFlights.txt')
    PlotAirlines(aircraft_list)
    PlotFlighType(aircraft_list)

    MapFlights(aircraft_list)
    print(LongDistanceArrivals(aircraft_list))