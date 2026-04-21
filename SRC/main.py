from SRC.Airportsfunctions.Aircraft import *

if __name__ == "__main__":
    # airport_list = LoadAirports('../Files/Airports.txt')
    # print(airport_list)
    aircraft_list = LoadArrivals('../Files/Arrivals.txt')
    print(aircraft_list)
    PlotArrivals(aircraft_list)
    SaveFlights(aircraft_list, 'SaveFlights.txt')
    PlotAirlines(aircraft_list)
    PlotFlighType(aircraft_list)
    MapFlights(aircraft_list)
    LongDistanceArrivals(aircraft_list)