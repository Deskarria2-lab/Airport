from binascii import a2b_qp  #   Airport Project Version 1.0
                                        #   Test f file!

#   "Libraries" From our project!
########################################
from Airport import *                                                           #   Import all the functions of airport
########################################

a1 = Airport("LEBL",  41.297445, 2.0832941)                        #   Define an airport to work
a2 = Airport("AFKS", 23.32, -0.98)
a3 = Airport('BIKF', 63.985, -22.605555555555558)

                                        #   Check Format
if not TryFormat(a1):
    raise ValueError("Invalid Airport")                                         #   If it's not correct raise and Error
else:
    print("Airport is valid")                                                   #   If it's valid, inform
    SetSchengen(a1)                                                             #   Check set_sch f
    LoadAirports('Airports.txt')                                                #   Check Airport list
    PrintAirport(a1)                                                            #   Print A1 data's
    print(LoadAirports('Airports.txt'))                                         #   Chek airports list from txt
    SaveSchengenAirports(LoadAirports('Airports.txt'),'Schengen.txt')   #   Create sch country file
    print(AddAirport(LoadAirports('Airports.txt'),a2))                          #   Chek Add Airport to list
    print(RemoveAirport(LoadAirports('Airports.txt'),a3.icao))                  #   Chek Delete Airport to list
    PlotAirport(LoadAirports('Airports.txt'))
    MapAirport(LoadAirports('Airports.txt'))