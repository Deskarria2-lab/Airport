#OBJETIVO, DEFINIR 4 CLASES

import matplotlib.pyplot as plt
####################################################    OBJECTS    #################################################################################

class Gate:                                                         #   Gate Object
    def __init__(self, g_name):
        self.g_name = g_name                                          #   Name of the Object
        self.occupancy = False                                      #   Is the gate occupied?
        self.a_id = None                                            #   ID of the

class BoardingArea:                                                 #   Boarding Area Object
    def __init__(self, b_name, sch):
        self.b_name = b_name                                          #   Name of the Boarding Area
        self.sch = sch                                            #   Is schengen the Boarding area?
        self.gate_list = []                                         #   List of Gate's

class Terminal:
    def __init__(self, t_name):
        self.t_name = t_name
        self.b_list = []
        self.icao_list = []
        self.airlines = []

class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.t_list = []

###########################################     Functions       #######################################################################################


def SetGates(area,init_gate,end_gate,prefix):
    if end_gate<init_gate:
        return -1
    area.gates=[]
    i=init_gate
    # Bucle para recorrer todas las puertas desde la inicial hasta la final
    while i<=end_gate:
        gate_name=prefix+str(i) # Junta el prefijo (ej: "T1A") con el número (ej: "5") -> "T1A5"
        gate=Gate(gate_name) # Crea un objeto de la clase Gate con ese nombre
        area.gates.append(gate)
        i=i+1
    return 0

def LoadAirlines(terminal,t_name):
    airlines_list=[]
    name_file=str(t_name)+"_Airlines.txt" # Construye el nombre del archivo (ej: "T1_Airlines.txt")
    try:
        with open(name_file,"r") as f:
            for line in f:
                if line!="":
                    parts=line.split("\t")
                    if len(parts)>=2:
                        code=parts[1].strip() # Si la línea tiene al menos dos columnas, limpia los espacios/saltos de línea de la segunda columna (código ICAO)
                        airlines_list.append(code)
        terminal.airlines=airlines_list
        return 0
    except:
        return -1



def LoadAirportStructure(filename):
    try:
        f=open(filename,"r")
    except:
        return -1
    line=f.readline().strip()
    parts=line.split()
    code=parts[0]
    bcn=BarcelonaAP(code)  # Crea el objeto principal del aeropuerto de Barcelona
    num_terminals=int(parts[1]) # El segundo elemento es el número de terminales que tiene
#Read terminals.
    i=0
    while i<num_terminals:
        line=f.readline().strip()
        parts=line.split()
        name_terminal=parts[1]
        areas_num=int(parts[2])
        terminal=Terminal(name_terminal)
        LoadAirlines(terminal,name_terminal)

#Boarding areas.
        j=0
        while j<areas_num:
            line=f.readline().strip()
            parts=line.split()
            area_name=parts[1]
            area_type=parts[2]
            init_gate=int(parts[4])
            end_gate=int(parts[6])
            area=BoardingArea(area_name,area_type)
            prefix=name_terminal+area_name
            SetGates(area,init_gate,end_gate,prefix)
            terminal.b_list.append(area)
            j=j+1
        bcn.t_list.append(terminal)
        i=i+1
    f.close()
    return bcn

def GateOccupancy(bcn):
    if bcn is None:
        return []
    allGates = []
    i = 0
    while i < len(bcn.t_list):
        terminal=bcn.t_list[i]
        j = 0
        while j < len(terminal.b_list):
            area=terminal.b_list[j]
            k=0
            while k < len(area.gates):
                gate = area.gates[k]
                if gate.occupancy:
                    status = "Occupied"
                    aircraft = gate.a_id
                else:
                    status = "Unoccupied"
                    aircraft = None
                allGates.append([gate.g_name, status, aircraft])
                k = k+1
            j = j+1
        i = i+1
    return allGates

def IsAirlineInTerminal(terminal, name):
    if name=="":
        return False
    if len(terminal.airlines)==0:
        return False
    i=0
    found=False
    while i<len(terminal.airlines) and not found:
        if terminal.airlines[i]==name:
            found=True
        i=i+1
    if found:
        return True
    if not found:
        return False

def SearchTerminal (bcn, name):
    i=0
    found=False
    terminal=None
    while i<len(bcn.t_list) and not found:
        if IsAirlineInTerminal(bcn.t_list[i],name):
            terminal=bcn.t_list[i]
            found=True
        i=i+1
    if found:
        return terminal.t_name
    if not found:
        return ""

from SRC.Airportsfunctions.Airport import is_schengen_airport
def AssignGate(bcn, aircraft):
#Buscar terminal por aerolínea
    terminal_name = SearchTerminal(bcn, aircraft.airline)
    if terminal_name == "":
        return -1
#Encontrar terminal
    terminal = None
    i = 0
    while i < len(bcn.t_list) and terminal is None:
        if bcn.t_list[i].t_name == terminal_name:
            terminal = bcn.t_list[i]
        i += 1
    if terminal is None:
        return -1

#Determinar el ICAO a evaluar (origen si llega, destino si es vuelo nocturno de salida)
    icao_to_check = aircraft.origin
    if icao_to_check == "" or icao_to_check == "None":
        icao_to_check = aircraft.destination
#Comprobar si el vuelo es schengen
    schengen = is_schengen_airport(icao_to_check)

#Buscar BoardingArea
    j = 0
    while j < len(terminal.b_list):
        area = terminal.b_list[j]
        if schengen == True and area.sch=="Schengen":
            #Buscar la puerta libre
            k = 0
            while k < len(area.gates):
                gate = area.gates[k]
                if not gate.occupancy:
                    gate.occupancy = True
                    gate.a_id = aircraft.id
                    return 0
                k += 1
        elif schengen==False and area.sch=="non-Schengen":
            k = 0
            while k < len(area.gates):
                gate = area.gates[k]
                if not gate.occupancy:
                    gate.occupancy = True
                    gate.a_id = aircraft.id
                    return 0
                k += 1
        j += 1
    return -1

def AssignNightGates(bcn, aircrafts):
    if len(aircrafts) == 0:
        return -1

    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        #Asegurar que no tiene llegada y sí tiene salida
        if (ac.arrival_time == "" or ac.arrival_time == "None") and ac.departure_time != "":
            AssignGate(bcn, ac) #Asignamos la puerta

        i += 1

    return 0

def FreeGates(bcn, id):
    i = 0
    while i < len(bcn.t_list):                                 #Iteramos sobre las terminales
        terminal = bcn.t_list[i]

        j = 0
        while j < len(terminal.b_list):                        #Iteramos sobre las areas de embarque
            area = terminal.b_list[j]

            k = 0
            while k < len(area.gates):                         #Iteramos sobre las puertas
                gate = area.gates[k]

                if gate.occupancy == True and gate.a_id == id: #Si la puerta esta ocupada y coincide el ID
                    gate.occupancy = False                     #Liberamos la puerta
                    gate.a_id = None
                    return 0
                k += 1
            j += 1
        i += 1
    return -1

def AssignGatesAtTime(bcn, aircrafts, time):
    # Convertir la hora recibida a minutos
    parts = time.split(":")
    time_mins = int(parts[0]) * 60 + int(parts[1])
    end_mins = time_mins + 60

    # 1. Liberar puertas de aviones que ya han salido antes de la hora recibida
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        if ac.departure_time != "" and ac.departure_time != "None":
            dep_parts = ac.departure_time.split(":")
            dep_mins = int(dep_parts[0]) * 60 + int(dep_parts[1])
            if dep_mins <= time_mins:
                FreeGates(bcn, ac.id)
        i += 1

    # 2. Asignar puertas a los aviones que aterrizan en la franja [time_mins, end_mins)
    not_assigned = 0
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        if ac.arrival_time != "" and ac.arrival_time != "None":
            arr_parts = ac.arrival_time.split(":")
            arr_mins = int(arr_parts[0]) * 60 + int(arr_parts[1])
            if time_mins <= arr_mins < end_mins:
                if AssignGate(bcn, ac) != 0:
                    not_assigned += 1
        i += 1

    return not_assigned

def PlotDayOccupancy(bcn, aircrafts):
    # Contar terminales
    num_terminals = len(bcn.t_list)

    # Para cada hora, guardar [gates_T1, gates_T2, ..., not_assigned]
    hours_data = []
    hour = 0
    while hour < 24:
        # Construir la hora como string "HH:00"
        if hour < 10:
            time_str = "0" + str(hour) + ":00"
        else:
            time_str = str(hour) + ":00"

        not_assigned = AssignGatesAtTime(bcn, aircrafts, time_str)

        # Contar puertas ocupadas por terminal
        t_counts = []
        t = 0
        while t < num_terminals:
            terminal = bcn.t_list[t]
            count = 0
            b = 0
            while b < len(terminal.b_list):
                area = terminal.b_list[b]
                k = 0
                while k < len(area.gates):
                    if area.gates[k].occupancy:
                        count += 1
                    k += 1
                b += 1
            t_counts.append(count)
            t += 1

        hours_data.append([t_counts, not_assigned])
        hour += 1

    # Dibujar el gráfico
    horas = list(range(24))
    colors = ["blue", "orange", "green", "red"]

    t = 0
    while t < num_terminals:
        values = []
        h = 0
        while h < 24:
            values.append(hours_data[h][0][t])
            h += 1
        plt.bar(horas, values, label=bcn.t_list[t].t_name,
                color=colors[t % len(colors)], alpha=0.7)
        t += 1

    # Barras de no asignados
    not_assigned_vals = []
    h = 0
    while h < 24:
        not_assigned_vals.append(hours_data[h][1])
        h += 1
    plt.bar(horas, not_assigned_vals, label="No asignados",
            color="black", alpha=0.5)

    plt.title("Ocupacion de puertas por hora y terminal")
    plt.xlabel("Hora")
    plt.ylabel("Puertas asignadas")
    plt.xticks(horas)
    plt.legend()
    plt.show()