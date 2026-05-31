#OBJETIVO, DEFINIR 4 CLASES


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

class Terminal:                                                     #   Terminal Object
    def __init__(self, t_name):
        self.t_name = t_name
        self.b_list = []
        self.icao_list = []

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
#Comprobar si el vuelo es Schengen
    schengen = is_schengen_airport(aircraft.origin)
#Buscar BoardingArea
    j = 0
    while j < len(terminal.b_list):
        area = terminal.b_list[j]
        if schengen == True and area.sch=="Schengen":
            # buscar gate libre
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