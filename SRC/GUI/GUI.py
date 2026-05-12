#V0.0 PROTOTIPO!!!!

import tkinter as tk
from tkinter import messagebox, filedialog
from SRC.Airportsfunctions.Airport import *
from SRC.Airportsfunctions.Aircraft import *
lista_aeropuertos = []

class AirportManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión Aeropuertos + Vuelos")
        self.root.geometry("900x550")

        self.airports_list = []
        self.aircraft_list = []

        self.setup_ui()

    def setup_ui(self):
        # ================= TOP =================
        frame_top = tk.Frame(self.root, pady=10)
        frame_top.pack(fill=tk.X)

        tk.Button(frame_top, text="Cargar Aeropuertos", command=self.load_airports).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Cargar Vuelos", command=self.load_flights).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Guardar Schengen", command=self.save_airports).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Guardar Vuelos", command=self.save_flights).pack(side=tk.LEFT, padx=5)

        # ================= MAIN =================
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # -------- LEFT PANEL --------
        frame_left = tk.Frame(main_frame)
        frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Label(frame_left, text="Código ICAO:").pack(anchor=tk.W)
        self.entry_icao = tk.Entry(frame_left)
        self.entry_icao.pack()

        tk.Label(frame_left, text="Latitud:").pack(anchor=tk.W)
        self.entry_lat = tk.Entry(frame_left)
        self.entry_lat.pack()

        tk.Label(frame_left, text="Longitud:").pack(anchor=tk.W)
        self.entry_lon = tk.Entry(frame_left)
        self.entry_lon.pack()

        tk.Button(frame_left, text="Añadir Aeropuerto", command=self.add_airport).pack(pady=5)
        tk.Button(frame_left, text="Eliminar Aeropuerto", command=self.delete_airport).pack(pady=5)

        # -------- RIGHT PANEL --------
        frame_right = tk.Frame(main_frame)
        frame_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(frame_right, text="Aeropuertos:").pack(anchor=tk.W)
        self.listbox_airports = tk.Listbox(frame_right)
        self.listbox_airports.pack(fill=tk.BOTH, expand=True)

        # -------- FLIGHTS PANEL --------
        frame_flights = tk.Frame(main_frame)
        frame_flights.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(frame_flights, text="Vuelos:").pack(anchor=tk.W)
        self.listbox_flights = tk.Listbox(frame_flights)
        self.listbox_flights.pack(fill=tk.BOTH, expand=True)

        # ================= BOTTOM =================
        frame_bottom = tk.Frame(self.root, pady=10)
        frame_bottom.pack(fill=tk.X)

        tk.Button(frame_bottom, text="Plot Aeropuertos", command=self.plot_airports).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_bottom, text="Mapa Aeropuertos", command=self.map_airports).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_bottom, text="Llegadas por hora", command=self.plot_arrivals).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_bottom, text="Por aerolínea", command=self.plot_airlines).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_bottom, text="Schengen vs No", command=self.plot_flight_type).pack(side=tk.LEFT, padx=5)

    # ================= AIRPORTS =================

    def load_airports(self):
        file = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if not file: return
        self.airports_list = Airport.LoadAirports(file)
        self.update_airports()

    def add_airport(self):
        try:
            ap = Airport.Airport(
                self.entry_icao.get(),
                self.entry_lat.get(),
                self.entry_lon.get()
            )
            Airport.TryFormat(ap)
            self.airports_list = Airport.AddAirport(self.airports_list, ap)
            self.update_airports()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_airport(self):
        icao = self.entry_icao.get()
        self.airports_list = Airport.RemoveAirport(self.airports_list, icao)
        self.update_airports()

    def save_airports(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            Airport.SaveSchengenAirports(self.airports_list, file)

    def plot_airports(self):
        Airport.PlotAirport(self.airports_list)

    def map_airports(self):
        Airport.MapAirport(self.airports_list)

    def update_airports(self):
        self.listbox_airports.delete(0, tk.END)
        for ap in self.airports_list:
            self.listbox_airports.insert(tk.END, f"{ap.icao} ({ap.lat}, {ap.lon})")

    # ================= FLIGHTS =================

    def load_flights(self):
        file = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if not file: return
        self.aircraft_list = LoadArrivals(file)
        self.update_flights()

    def save_flights(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            SaveFlights(self.aircraft_list, file)

    def plot_arrivals(self):
        if not self.aircraft_list:
            messagebox.showwarning("Error", "No hay vuelos")
            return
        PlotArrivals(self.aircraft_list)

    def plot_airlines(self):
        PlotAirlines(self.aircraft_list)

    def plot_flight_type(self):
        PlotFlighType(self.aircraft_list)

    def update_flights(self):
        self.listbox_flights.delete(0, tk.END)
        for f in self.aircraft_list:
            self.listbox_flights.insert(
                tk.END,
                f"{f.id} | {f.origin} | {f.arrival_time} | {f.airline}"
            )


if __name__ == "__main__":
    ventana = tk.Tk()
    app = AirportManagerApp(ventana)
    ventana.mainloop()