                                        #   Airport Project Version 1.0
                                        #   Test f file!

#   "Libraries" From our project!
########################################
from SRC.Airportsfunctions.Airport import *                                                           #   Import all the functions of airport
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
    LoadAirports('../Files/Airports.txt')                                                #   Check Airport list
    PrintAirport(a1)                                                            #   Print A1 data's
    print(LoadAirports('../Files/Airports.txt'))                                         #   Chek airports list from txt
    SaveSchengenAirports(LoadAirports('../Files/Airports.txt'), '../Files/Schengen.txt')   #   Create sch country file
    print(AddAirport(LoadAirports('../Files/Airports.txt'), a2))                          #   Chek Add Airport to list
    print(RemoveAirport(LoadAirports('../Files/Airports.txt'), a3.icao))                  #   Chek Delete Airport to list
    PlotAirport(LoadAirports('../Files/Airports.txt'))
    MapAirport(LoadAirports('../Files/Airports.txt'))