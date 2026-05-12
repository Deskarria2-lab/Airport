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

####################################################    PlotA Arrivals  ###########################################################

def PlotArrivals(aircraft_list):
    if len(aircraft_list) == 0:                                                                 #   Comprobamos si no tenemos datos cargados en lista
        print("Error: La lista de vuelos está vacía.")                                          #   Muestras el Error
        return
    h_cont = [0] * 24                                                                           #   Creamos lista de 24 unidades / 1 h -> 1 u
    i=0                                                                                         #   Inicializamos contador en 0
    while i < len(aircraft_list):                                                               #   Cuando el contador es mas pequeño que lista
        aircraft = aircraft_list[i]                                                             #   Por comodidad simplificamos el elemento i de la lista aeropuerto
        partes_hora = aircraft.arrival_time.split(':')                                          #   Del atributo tiempo de llegada  separamos hora y minuto
        hora_entera = int(partes_hora[0])                                                       #   Seleccionas la hora

        if 0 <= hora_entera < 24:                                                               #   Seguridad redundante, comprobar que la hora es coherente
            h_cont[hora_entera] += 1                                                            #   Añades 1 a h_cont en la posicion de la hora especifica

        i += 1                                                                                  #   Miramos la hora del siguiente avion

    horas = list(range(24))                                                                     #   Creamos 24 espacios para el eje x
    plt.bar(horas, h_cont, color='blue')                                                        #   Diagrama de barras h_cont(horas)
    plt.title("Frecuencia de Aterrizajes por Hora")                                             #   Titulo de la grafica
    plt.xlabel("Hora")                                                                          #   Titulo eje X
    plt.ylabel("Número de aviones")                                                             #   Titulo eje Y
    plt.xticks(horas)
    plt.show()

####################################################    Save Flights    ##################################################################

def SaveFlights(aircraft_list, filename):                               #Casi good
    if len(aircraft_list) == 0:                                                                 #   Compruebas si la lista aircraft esta vacia
        print(                                                                                  #   Muestras error en pantalla
            "ERROR: La lista de aviones está vacía."
            " No se puede crear el archivo."
        )
        return -1                                                                               #   Devolvemos un código de error (por ejemplo -1)
    
    try:                                                                                        #   Intenta hacer lo siguiente:                                                                                            
        with open(filename, "w") as f:                                                          #       -   Abrir el archivo
            f.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE2\n")                                       #       -   Escribe título de fichero
            i = 0                                                                               #       -   Contador a 0
            
            while i < len(aircraft_list):
                aircraft = aircraft_list[i]                                                     #       -   Variable para el obj 
                id_aircraft = aircraft.id if aircraft.id else "-"                               #       -   si aircraft.id != None guarda la variable id_aircraft con aircraft.id, sino "-"
                origin = aircraft.origin if aircraft.origin else "-"                            #       -   si aircraft.origin != None guarda la variable origin con aircraft.origin, sino "-"
                arrival = aircraft.arrival_time if aircraft.arrival_time else "-"               #       -   si aircraft.arrival_time != None guarda la variable arrival con aircraft.arrival_time, sino "-"
                airline = aircraft.airline if aircraft.airline else "-"                         #       -   si aircraft.airline != None guarda la variable airline con aircraft.airline, sino "-"
                line = f"{id_aircraft} {origin} {arrival} {airline}\n"                          #       -   La línea a escribir es la union de toda esta informacion
                f.write(line)                                                                   #       -   Escribe la línea en el archivo
                i += 1                                                                          #       -   Incrementa 1 en el contador

        print(f"Archivo '{filename}' guardado correctamente.")                                  #       -   Avisa que ya esta guardado de forma exitosa
        return 0                                                                                #       -   Éxito
    except FileNotFoundError: print("Error")                                                    #   En caso de no encontrar el archivo en question, manda error

####################################################    Plot Airlines   ####################################################################

def PlotAirlines (aircraft_list):
    if not aircraft_list:                                                                       #   Si no hay elementos en la lista
        print ("Error: No hay datos para graficar.")                                            #   Informar que no puedes graficar nada
        return

    airlines_list = {}                                                                          #   Crea una lista donde guardas los aeropuertos en question
    for avion in aircraft_list:                                                                 #   Por cada elemento en la lista
        airline = avion.airline                                                                 #   Miramos el atributo airline del elemento aircraft_list[i]

        if airline in airlines_list:                                                            #   Si la aerolínea está en la lista de aerolíneas
            airlines_list[airline] += 1                                                         #   Aumenta 1 en la lista de aerolíneas
        else:                                                                                   #   Si no
            airlines_list[airline] = 1                                                          #   Resetea la lista

    eje_x = list(airlines_list.keys())                                                          #   Eje x
    eje_y = list(airlines_list.values())

    plt.bar(eje_x, eje_y, color='blue', edgecolor='black')
    plt.title('Frecuencia de vuelos por aerolinea')
    plt.xlabel('Aerolinea (ICAO)')
    plt.ylabel('Numero de vuelos')
    plt.show()

####################################################    Plot Fligh Type  ##############################################################

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

####################################################    Map Flights     #############################################################

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