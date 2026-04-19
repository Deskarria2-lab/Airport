class Aircraft:
    def __init__(self, id_aeronave, aerolinea, origen, hora_llegada):
        self.id = id_aeronave
        self.airline = aerolinea
        self.origin = origen
        self.arrival_time = hora_llegada

import matplotlib.pyplot as plt
import math
from Airportsfunctions import IsSchengenAirport
from Airportsfunctions import LoadAirports

lista_aeropuertos_v2 = LoadAirports ("Airports.txt")
diccionario_aeropuertos = {}
for a in lista_aeropuertos_v2:
    diccionario_aeropuertos [a.id] = a

def LoadArrivals(filename):
    lista_aviones = []
    try:
        with open(filename, "r") as f:
            f.readline()
            linea = f.readline()
        while linea != "":
            datos = linea.strip().split()
            if len(datos) == 4 and ":" in datos[2]:
                nuevo_avion = Aircraft(datos[0], datos[3], datos[1], datos[2])
                lista_aviones.append(nuevo_avion)
            linea = f.readline()
    except FileNotFoundError:
        return []
    return lista_aviones

def PlotArrivals(aircrafts):
    if len(aircrafts) == 0:
        print("Error: La lista de vuelos está vacía.")
        return
    conteo_por_hora = [0] * 24
    i=0
    while i < len(aircrafts):
        avion = aircrafts[i]
        partes_hora = avion.arrival_time.split(':')
        hora_entera = int(partes_hora[0])
        if 0 <= hora_entera < 24:
            conteo_por_hora[hora_entera] += 1
        i=i+1

horas = list(range(24))
plt.bar(horas, conteo_por_hora, color='blue')
plt.title("Frecuencia de Aterrizajes por Hora")
plt.xlabel("Hora")
plt.ylabel("Número de aviones")
plt.xticks(horas)
plt.show()

def SaveFlights(aircrafts, filename):
    if len(aircrafts) == 0:
        print("ERROR: La lista de aviones está vacía. No se puede crear el archivo.")
        return -1 # Devolvemos un código de error (por ejemplo -1)
    try:
        with open(filename, "w") as f:
            f.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE2\n")
            i = 0
            while i < len(aircrafts):
                a = aircrafts[i]
                id_avion = a.id if a.id else "-"
                origen = a.origin if a.origin else "-"
                llegada = a.arrival_time if a.arrival_time else "-"
                aerolinea = a.airline if a.airline else "-"
                linea = f"{id_avion} {origen} {llegada} {aerolinea}\n"
                f.write(linea)
                i=i+1
        print(f"Archivo '{filename}' guardado correctamente.")
        return 0  # Éxito

def PlotAirlines (aircrafts):
    if not aircrafts:
        print ("Error: No hay datos para graficar.")
        return

    conteo_aerolineas = {}
    for avion in aircrafts:
        aerolinea = avion.airline

        if aerolinea in conteo_aerolineas:
            conteo_aerolineas[aerolinea] += 1
        else:
            conteo_aerolineas[aerolinea] = 1

    eje_x = list(conteo_aerolineas.keys())
    eje_y = list(conteo_aerolineas.values())

    plt.bar(eje_x, eje_y, color='blue', edgecolor='black')
    plt.title('Frecuencia de vuelos por aerolinea')
    plt.xlabel('Aerolinea (ICAO)')
    plt.ylabel('Numero de vuelos')
    plt.show()

    def PlotFlighType (aircraft):
        if not aircrafts:
            print("Error: No hay datos para graficar.")
            return
        vuelos_schengen = 0
        vuelos_no_schengen = 0

        for avion in aircraft:
            if IsSchengenAirport (avion.origin):
                vuelos_schengen += 1
            else:
                vuelos_no_schengen += 1
        categoria_x = ["Vuelos totales a LEBL"]

        plt.bar(categoria_x, [vuelos_schengen], label = "Schengen", color='blue')
        plt.bar(categoria_x, [vuelos_no_schengen], bottom = [vuelos_schengen], label = "No Schengen", color='red')
        plt.title('Proporcion Schengen vs No Schengen')
        plt.ylabel('Numero de llegadas')
        plt.legend()
        plt.show()
def MapFlights (aircrafts):
    if not aircrafts:
        print("Error: No hay datos para graficar.")
        return

    if "LEBL" not in diccionario_aeropuertos:
        print("Error: LEBL no esta en la base de datos de aeropuertos.")
        return
    dest_lat = diccionario_aeropuertos["LEBL"].lat
    dest_lon = diccionario_aeropuertos["LEBL"].lon

    try:
        with open ("trajectories.kml", "w") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>')
            file.write('<Style id="estilo_schengen"><LineStyle><color>ffff0000</color><width>2</width></LineStyle></Style>')
            file.write('<Style id="estilo_no_schengen"><LineStyle><color>ff0000ff</color><width>2</width></LineStyle></Style>')

            for avion in aircrafts:
                origen = avion.origin
                if origen not in diccionario_aeropuertos:
                    continue

                orig_lat = diccionario_aeropuertos[origen].lat
                orig_lon = diccionario_aeropuertos[origen].lon

                if IsSchengenAirport (origen):
                    estilo = "estilo_schengen"
                else:
                    estilo = "estilo_no_schengen"

                file.write(f'<Placemark><name>Vuelo: {origen} -> LEBL</name><styleUrl>#{estilo}</styleUrl><LineString><tessellate>1</tessellate><coordinates>{orig_lon},{orig_lat},0 {dest_lon},{dest_lat},0</coordinates></LineString></Placemark>')
            file.write('</Document></kml>')

            except Exception as e:
                print("Error al generar archivo KMl")

def LongDistanceArrivals (aircrafts):
    vuelos_largos = []
    if not aircrafts:
        print("Error: La lista de aviones esta vacía.")
        return vuelos_largos
    if LEBL not in diccionario_aeropuertos:
        print("Error: LEBL no esta en la base de datos.")
        return vuelos_largos
    lat_destino = math.radians(diccionario_aeropuertos["LEBL"].lat)
    lon_destino = math.radians(diccionario_aeropuertos["LEBL"].lon)
    radio_tierra = 6371.0

    for avion in aircrafts:
        origen = avion.origin

        if origen not in diccionario_aeropuertos:
            continue

        lat_origen = math.radians(diccionario_aeropuertos[origen].lat)
        lon_origen = math.radians(diccionario_aeropuertos[origen].lon)

        delta_lat = abs(lat_destino - lat_origen)
        delta_lon = abs(lon_destino - lon_origen)

        a = (math.sin(delta_lat / 2)**2) + math.cos(lat_origen) * math.cos(lat_destino) * (math.sin(delta_lon / 2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia_km = radio_tierra * c
        if distancia_km > 2000
            vuelos_largos.append(avion)
        return vuelos_largos
