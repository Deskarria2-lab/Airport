                                        #   Aircraft functions file

#   "Libraries" From our project!
########################################
from SRC.Airportsfunctions.Airport import IsSchengenAirport
########################################
#   External Libraries!
########################################
import matplotlib.pyplot as plt
import math
########################################

class Aircraft:
    def __init__(self, id, airline, origin, arrival_time):
        self.id = id
        self.airline = airline
        self.origin = origin
        self.arrival_time = arrival_time

def LoadArrivals(filename):
    file = open(filename, "r")  # Load the txt airport file
    next(file)  # Ignore the first line
    lines = file.readline()  # Defines the var lines
    aircraft_list = []
    while lines != "":
        aircrafts = Aircraft("None", "None", 0, "None")
        elem = lines.strip("\t")
        elem = elem.split(" ")
        id = elem[0]
        origin = elem[1]
        arrival_time = elem[2]
        airline = elem[3]

        aircrafts.id = id
        aircrafts.airline = airline
        aircrafts.origin = origin
        aircrafts.arrival_time = arrival_time

        aircraft_list.append(aircrafts)
        lines = file.readline()
    file.close()
    return aircraft_list

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

def MapFlights (aircraft_list):                         #REVISAR
    if not aircraft_list:
        print("Error: No hay datos para graficar.")
        return

    if "LEBL" not in aircraft_list:
        print("Error: LEBL no esta en la base de datos de aeropuertos.")
        return
    dest_lat = aircraft_list["LEBL"].lat                #????'
    dest_lon = aircraft_list["LEBL"].lon

    try:
        with open ("trajectories.kml", "w") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>')
            file.write('<Style id="estilo_schengen"><LineStyle><color>ffff0000</color><width>2</width></LineStyle></Style>')
            file.write('<Style id="estilo_no_schengen"><LineStyle><color>ff0000ff</color><width>2</width></LineStyle></Style>')

            for avion in aircraft_list:
                origen = avion.origin
                if origen not in aircraft_list:
                    continue

                orig_lat = aircraft_list[origen].lat
                orig_lon = aircraft_list[origen].lon

                if IsSchengenAirport (origen):
                    estilo = "estilo_schengen"
                else:
                    estilo = "estilo_no_schengen"

                file.write(f'<Placemark><name>Vuelo: {origen} -> LEBL</name><styleUrl>#{estilo}</styleUrl><LineString><tessellate>1</tessellate><coordinates>{orig_lon},{orig_lat},0 {dest_lon},{dest_lat},0</coordinates></LineString></Placemark>')
            file.write('</Document></kml>')

    except Exception as e:
        print("Error al generar archivo KMl")

def LongDistanceArrivals (aircraft_list):                   #REHACER
    l_flights = []
    if not aircraft_list:
        print("Error: La lista de aviones esta vacía.")
        return l_flights
    if 'LEBL' not in aircraft_list:  #???
        print("Error: LEBL no esta en la base de datos.")
        return l_flights
    lat_dest = math.radians(aircraft_list["LEBL"].lat)
    lon_dest = math.radians(aircraft_list["LEBL"].lon)
    radio_tierra = 6371.0

    for aircraft in aircraft_list:
        origin = aircraft.origin

        if origin not in aircraft_list: continue

        lat_origen = math.radians(aircraft_list[origin].lat)
        lon_origen = math.radians(aircraft_list[origin].lon)

        delta_lat = abs(lat_dest - lat_origen)
        delta_lon = abs(lon_dest - lon_origen)

        a = (math.sin(delta_lat / 2)**2) + math.cos(lat_origen) * math.cos(lat_dest) * (math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia_km = radio_tierra * c
        if distancia_km > 2000:
            l_flights.append(aircraft)
        return l_flights
    return None

if __name__ == "__main__":
    # airport_list = LoadAirports('../Files/Airports.txt')
    # print(airport_list)
    aircraft_list = LoadArrivals('../../Files/Arrivals.txt')
    print(aircraft_list)
    PlotArrivals(aircraft_list)
    SaveFlights(aircraft_list, '../../Files/SaveFlights.txt')
    PlotAirlines(aircraft_list)
    PlotFlighType(aircraft_list)
    MapFlights(aircraft_list)
    LongDistanceArrivals(aircraft_list)