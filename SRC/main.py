class Aircraft:
    def __init__(self, id_aeronave, aerolinea, origen, hora_llegada):
        self.id = id_aeronave
        self.airline = aerolinea
        self.origin = origen
        self.arrival_time = hora_llegada
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
import matplotlib.pyplot as plt
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