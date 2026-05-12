#OBJETIVO, DEFINIR 4 CLASES


####################################################    OBJECTS    #################################################################################

class Gate:                                                         #   Gate Object
    def __init__(self):
        self.g_name = None                                          #   Name of the Object
        self.occupancy = False                                      #   Is the gate occupied?
        self.a_id = None                                            #   ID of the

class BoardingArea:                                                 #   Boarding Area Object
    def __init__(self):
        self.b_name = None                                          #   Name of the Boarding Area
        self.sch = False                                            #   Is schengen the Boarding area?
        self.gate_list = []                                         #   List of Gate's

class Terminal:                                                     #   Terminal Object
    def __init__(self):
        self.t_name = None
        self.b_list = []
        self.icao_list = []

class BarcelonaAP:
    def __init__(self):
        self.code = None
        self.t_list = []

###########################################     Functions       #######################################################################################

def set_gates(b_area, init_gate, end_gate, prefix):

#   OBJETIVO: crear una funcion que actualice la lista del objetivo Boarding Area (gate_list)

#   FORMA: Tu le das un objeto Boarding Area, si el objeto b_area ya tiene una gate_list, se elimina primero
#   Lo que tiene que hacer la funcion es rellenar la lista
    pass