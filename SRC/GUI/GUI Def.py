#   Airport Project Version 4.0
                                            #   GUI Module - Modern FIDS Design
########################################
#   "Libraries" From our project!
########################################
try:
    from SRC.Airportsfunctions.Airport import *
    from SRC.Airportsfunctions.Aircraft import *
    from SRC.Airportsfunctions.LEBL import *
    from SRC.GUI.Gui_Functions import *
except ImportError:
    pass                                                                    #   Stubs defined below if project not found
########################################
#   External Libraries!
########################################
import tkinter as tk
from tkinter import messagebox, filedialog
import os
########################################

class AirportManagerApp:
                            #   Initialize window and data stores  #
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("LEBL · Airport Operations Center")
        self.root.geometry("1200x730")
        self.root.configure(bg=C["bg"])
        self.root.resizable(True, True)

        self.airports_list = []                                             #   List of Airport objects
        self.aircraft_list = []                                             #   List of Aircraft/Flight objects
        self.bcn_airport   = None                                           #   LEBL structure object

        self._build_ui()                                                    #   Build all UI components

    ########################################
    #   UI Construction
    ########################################

                                    #   Build all UI sections in order  #
    def _build_ui(self):
        self._build_status_bar()                                            #   Pack bottom first to anchor it
        self._build_header()                                                #   Then top header
        self._build_tabs()                                                  #   Then tab content area

                                    #   Status bar at the bottom of the window  #
    def _build_status_bar(self):
        bar = tk.Frame(self.root, bg=C["hdr"])
        bar.pack(side="bottom", fill="x")
        tk.Frame(bar, bg=C["border"], height=1).pack(fill="x")            #   Top borderline
        row = tk.Frame(bar, bg=C["hdr"], padx=14, pady=4)
        row.pack(fill ="x")
        self._status_lbl = tk.Label(row, text="Sistema listo.",            #   Status message label
                                    bg=C["hdr"], fg=C["text_dim"],
                                    font=F_SMALL, anchor="w")
        self._status_lbl.pack(side="left")
        tk.Label(row, text="LEBL · BCN · 2025",                            #   Static right label
                 bg=C["hdr"], fg=C["text_dim"], font=F_SMALL).pack(side="right")

                                    #   Update the status bar message  #
    def _set_status(self, msg, color=None):
        self._status_lbl.config(text=f"▸  {msg}",
                                fg=color or C["text_dim"])

                                    #   Top header with logo and stat counters  #
    def _build_header(self):
        hdr = tk.Frame(self.root, bg=C["hdr"])
        hdr.pack(side="top", fill="x")
        tk.Frame(hdr, bg=C["accent"], height=3).pack(fill="x")            #   Amber top accent line

        inner = tk.Frame(hdr, bg=C["hdr"], padx=20, pady=12)
        inner.pack(fill="x")

        left = tk.Frame(inner, bg=C["hdr"])                                #   Left side: logo and subtitle
        left.pack(side="left")
        tk.Label(left, text="✈  LEBL", bg=C["hdr"],
                 fg=C["accent"], font=F_TITLE).pack(side="left", padx=(0, 12))
        tk.Frame(left, bg=C["border"], width=2, height=40).pack(side="left", padx=12)  # Vertical divider
        titles = tk.Frame(left, bg=C["hdr"])
        titles.pack(side="left")
        tk.Label(titles, text="AIRPORT OPERATIONS CENTER",
                 bg=C["hdr"], fg=C["text"],
                 font=("Courier New", 13, "bold")).pack(anchor="w")
        tk.Label(titles, text="Barcelona · El Prat  |  Sistema de Gestión v4",
                 bg=C["hdr"], fg=C["text_dim"], font=F_SMALL).pack(anchor="w")

        right = tk.Frame(inner, bg=C["hdr"])                               #   Right side: live stat boxes
        right.pack(side="right")
        self._stat_airports = self._mini_stat(right, "AEROPUERTOS", "0")
        self._stat_flights   = self._mini_stat(right, "VUELOS",       "0")
        self._stat_gates     = self._mini_stat(right, "ESTRUCTURA",   "—")

        tk.Frame(hdr, bg=C["border"], height=1).pack(fill="x")            #   Bottom borderline

                                    #   Create a small stat counter box  #

    def _mini_stat(self, parent, label, value):
        f = tk.Frame(parent, bg=C["card"], padx=14, pady=8)
        f.pack(side="left", padx=6)
        val = tk.Label(
            f,
            text=value,
            bg=C["card"],                        #   Large number label
            fg=C["accent"],
            font=("Courier New", 18, "bold"))
        val.pack()
        tk.Label(f, text=label, bg=C["card"],                              #   Small description label
                 fg=C["text_dim"], font=F_SMALL).pack()
        return val

                                    #   Tab bar and content area  #
    def _build_tabs(self):
        tab_bar = tk.Frame(self.root, bg=C["panel"])                       #   Tab button row
        tab_bar.pack(side="top", fill="x")
        tk.Frame(tab_bar, bg=C["border"], height=1).pack(fill="x")
        btn_row = tk.Frame(tab_bar, bg=C["panel"])
        btn_row.pack(anchor="w", padx=10, pady=6)

        self._content = tk.Frame(self.root, bg=C["bg"])                    #   Shared content frame for all tabs
        self._content.pack(side="top", fill="both", expand=True, padx=10)

        tab_defs = [                                                        #   Tab definitions: name + builder
            ("🗺  AEROPUERTOS", self._build_airports_tab),
            ("✈  VUELOS",       self._build_flights_tab),
            ("🚪  PUERTAS",     self._build_gates_tab),
            ("💻  EXAMEN", self._build_gates_tab),
        ]

        self._tab_buttons = []                                              #   Store tab button refs
        self._tab_frames  = []                                              #   Store tab frame refs

        i = 0                                                               #   Counter
        while i < len(tab_defs):                                            #   Build each tab frame and button
            name, builder = tab_defs[i]
            frame = tk.Frame(self._content, bg=C["bg"])
            builder(frame)                                                  #   Call builder to fill the frame
            self._tab_frames.append(frame)

            btn = tk.Label(btn_row, text=name,
                           bg=C["panel"], fg=C["text_dim"],
                           font=F_SMALL, padx=18, pady=6, cursor="hand2")
            btn.pack(side="left", padx=2)
            btn.bind("<Button-1>", lambda e, idx=i: self._switch_tab(idx)) #   Bind click to switch
            self._tab_buttons.append(btn)
            i += 1

        self._switch_tab(0)                                                 #   Show first tab by default

                                    #   Switch active tab, hide others  #
    def _switch_tab(self, idx):
        i = 0                                                               #   Counter
        while i < len(self._tab_buttons):                                   #   Iterate all tabs
            btn   = self._tab_buttons[i]
            frame = self._tab_frames[i]
            if i == idx:                                                    #   Active tab: highlight button, show frame
                btn.config(bg=C["accent"], fg=C["bg"],
                           font=("Courier New", 9, "bold"))
                frame.pack(fill=tk.BOTH, expand=True)
            else:                                                           #   Inactive tab: dim button, hide frame
                btn.config(bg=C["panel"], fg=C["text_dim"], font=F_SMALL)
                frame.pack_forget()
            i += 1

    ########################################
    #   Tab 1 - Airports
    ########################################

                                    #   Build the Airports management tab  #
    def _build_airports_tab(self, parent):
        row = tk.Frame(parent, bg=C["bg"])                                  #   Horizontal split container
        row.pack(fill="both", expand=True, pady=8)

        left = tk.Frame(row, bg=C["panel"], padx=16, pady=14, width=190)   #   Left panel: form and buttons
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        self._sec(left, "AÑADIR / ELIMINAR")
        for lbl, attr in [("Código ICAO", "entry_icao"),                   #   Create the 3 input fields
                           ("Latitud",     "entry_lat"),
                           ("Longitud",    "entry_lon")]:
            tk.Label(left, text=lbl, bg=C["panel"],
                     fg=C["text_dim"], font=F_SMALL).pack(anchor="w", pady=(7, 1))
            e = tk.Entry(left, bg=C["card"], fg=C["text"],
                         insertbackground=C["accent"],
                         relief="flat", font=F_BODY, width=18)
            e.pack(fill="x", ipady=5)
            setattr(self, attr, e)                                          #   Assign entry as instance attribute

        self._div(left)
        FidsButton(left, "Añadir Aeropuerto",   self.add_airport,    icon="➕").pack(fill="x", pady=2)
        FidsButton(left, "Eliminar Aeropuerto", self.delete_airport, icon="🗑").pack(fill="x", pady=2)
        self._div(left)
        self._sec(left, "ARCHIVOS")
        FidsButton(left, "Cargar Aeropuertos",  self.load_airports,  icon="📂").pack(fill="x", pady=2)
        FidsButton(left, "Guardar Schengen",    self.save_airports,  icon="💾").pack(fill="x", pady=2)
        self._div(left)
        self._sec(left, "VISUALIZACIÓN")
        FidsButton(left, "Plot Aeropuertos",    self.plot_airports,  icon="📊").pack(fill="x", pady=2)
        FidsButton(left, "Mapa KML",            self.map_airports,   icon="🗺", accent=True).pack(fill="x", pady=2)

        right = tk.Frame(row, bg=C["panel"], padx=12, pady=12)             #   Right panel: airport list
        right.pack(side="left", fill="both", expand=True)

        self._sec(right, "AEROPUERTOS CARGADOS")

        hdr = tk.Frame(right, bg=C["border"])                              #   Column header bar
        hdr.pack(fill="x", pady=(6, 0))
        for col, w in [("ICAO", 8), ("LATITUD", 12), ("LONGITUD", 12), ("SCHENGEN", 10)]:
            tk.Label(hdr, text=col, bg=C["border"], fg=C["accent"],
                     font=("Courier New", 9, "bold"), width=w, pady=4).pack(side="left")

        lf = tk.Frame(right, bg=C["card"])                                 #   Listbox container frame
        lf.pack(fill="both", expand=True, pady=(2, 0))

        sb = tk.Scrollbar(lf, orient="vertical",
                          troughcolor=C["card"], bg=C["border"])
        sb.pack(side="right", fill="y")

        self.listbox_airports = tk.Listbox(
            lf, bg=C["card"], fg=C["text"],
            selectbackground=C["accent"], selectforeground=C["bg"],
            relief="flat", font=F_MONO,
            highlightthickness=0, activestyle="none",
            borderwidth=0, yscrollcommand=sb.set)
        self.listbox_airports.pack(side="left", fill="both", expand=True)
        sb.config(command=self.listbox_airports.yview)

    ########################################
    #   Tab 2 - Flights
    ########################################

                                    #   Build the Flights management tab  #
    def _build_flights_tab(self, parent):
        row = tk.Frame(parent, bg=C["bg"])                                  #   Horizontal split container
        row.pack(fill="both", expand=True, pady=8)

        left = tk.Frame(row, bg=C["panel"], padx=16, pady=14, width=190)   #   Left panel: buttons
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        self._sec(left, "ARCHIVOS")
        FidsButton(left, "Cargar Vuelos",  self.load_flights,    icon="📂").pack(fill="x", pady=2)
        FidsButton(left, "Guardar Vuelos", self.save_flights,    icon="💾").pack(fill="x", pady=2)
        self._div(left)
        self._sec(left, "ANÁLISIS")
        FidsButton(left, "Llegadas por hora",   self.plot_arrivals,    icon="📈").pack(fill="x", pady=2)
        FidsButton(left, "Por aerolínea",        self.plot_airlines,    icon="🏷").pack(fill="x", pady=2)
        FidsButton(left, "Schengen vs No",       self.plot_flight_type, icon="🌍", accent=True).pack(fill="x", pady=2)

        right = tk.Frame(row, bg=C["panel"], padx=12, pady=12)             #   Right panel: FIDS flight table
        right.pack(side="left", fill="both", expand=True)

        self._sec(right, "TABLA DE VUELOS (FIDS)")

        hdr = tk.Frame(right, bg=C["accent"])                              #   Amber column header bar
        hdr.pack(fill="x", pady=(6, 0))
        for col, w in [("VUELO", 10), ("ORIGEN", 10), ("HORA", 8), ("AEROLÍNEA", 16)]:
            tk.Label(hdr, text=col, bg=C["accent"], fg=C["bg"],
                     font=("Courier New", 9, "bold"), width=w, pady=5).pack(side="left")

        lf = tk.Frame(right, bg=C["card"])                                 #   Listbox container frame
        lf.pack(fill="both", expand=True, pady=(2, 0))

        sb = tk.Scrollbar(lf, orient="vertical",
                          troughcolor=C["card"], bg=C["border"])
        sb.pack(side="right", fill="y")

        self.listbox_flights = tk.Listbox(
            lf, bg=C["card"], fg=C["text"],
            selectbackground=C["accent2"], selectforeground=C["bg"],
            relief="flat", font=F_MONO,
            highlightthickness=0, activestyle="none",
            borderwidth=0, yscrollcommand=sb.set)
        self.listbox_flights.pack(side="left", fill="both", expand=True)
        sb.config(command=self.listbox_flights.yview)

    ########################################
    #   Tab 3 - Gates
    ########################################

                                    #   Build the Gate management tab  #
    def _build_gates_tab(self, parent):
        row = tk.Frame(parent, bg=C["bg"])                                  #   Horizontal split container
        row.pack(fill="both", expand=True, pady=8)

        left = tk.Frame(row, bg=C["panel"], padx=16, pady=14, width=190)   #   Left panel: buttons and legend
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        self._sec(left, "OPERACIONES")
        FidsButton(left, "Cargar Estructura", self.load_airport_structure, icon="🏗").pack(fill="x", pady=2)
        FidsButton(left, "Asignar Puertas",   self.assign_gates,           icon="🔀").pack(fill="x", pady=2)
        FidsButton(left, "Ver Ocupación",     self.view_gate_occupancy,    icon="👁", accent=True).pack(fill="x", pady=2)
        self._div(left)
        self._sec(left, "LEYENDA")
        for color, label in [(C["green"], "Puerta LIBRE"),                 #   Color legend entries
                             (C["red"],   "Puerta OCUPADA")]:
            leg = tk.Frame(left, bg=C["panel"])
            leg.pack(fill="x", pady=3)
            tk.Frame(leg, bg=color, width=12, height=12).pack(side="left", padx=(0, 8))
            tk.Label(leg, text=label, bg=C["panel"],
                     fg=C["text"], font=F_SMALL).pack(side="left")

        right = tk.Frame(row, bg=C["panel"], padx=12, pady=12)             #   Right panel: gate status list
        right.pack(side="left", fill="both", expand=True)

        self._sec(right, "ESTADO DE PUERTAS")
        tk.Label(right,
                 text="Carga la estructura y pulsa 'Ver Ocupación' para ver el estado de las puertas.",
                 bg=C["panel"], fg=C["text_dim"], font=F_SMALL,
                 wraplength=480, justify="left").pack(anchor="w", pady=(4, 6))

        lf = tk.Frame(right, bg=C["card"])                                 #   Listbox container frame
        lf.pack(fill="both", expand=True)

        sb = tk.Scrollbar(lf, orient="vertical",
                          troughcolor=C["card"], bg=C["border"])
        sb.pack(side="right", fill="y")

        self.listbox_gates = tk.Listbox(
            lf, bg=C["card"], fg=C["text"],
            selectbackground=C["border"],
            relief="flat", font=F_MONO,
            highlightthickness=0, activestyle="none",
            borderwidth=0, yscrollcommand=sb.set)
        self.listbox_gates.pack(side="left", fill="both", expand=True)
        sb.config(command=self.listbox_gates.yview)

    def _build_exam_tab(self, parent):
        row = tk.Frame(parent, bg=C["bg"])  # Horizontal split container
        row.pack(fill="both", expand=True, pady=8)

        left = tk.Frame(row, bg=C["panel"], padx=16, pady=14, width=190)  # Left panel: buttons and legend
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

    ########################################
    #   UI Helper Methods
    ########################################

                            #   Section heading label in amber  #

    @staticmethod
    def _sec(parent, text):
        tk.Label(parent, text=text, bg=parent.cget("bg"),
                 fg=C["accent"], font=F_SEC).pack(anchor="w", pady=(6, 2))

                            #   Horizontal divider line  #

    @staticmethod
    def _div(parent):
        tk.Frame(parent, bg=C["border"], height=1).pack(fill="x", pady=8)

                                     #   Refresh the three stat counter boxes  #
    def _update_stats(self):
        self._stat_airports.config(text=str(len(self.airports_list)))
        self._stat_flights.config(text=str(len(self.aircraft_list)))
        self._stat_gates.config(text="OK" if self.bcn_airport else "—",
                                fg=C["green"] if self.bcn_airport else C["accent"])

    ########################################
    #   Airport Logic
    ########################################

                                #   Load airports from a txt file  #
    def load_airports(self):
        file = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if not file:                                                        #   User canceled the dialog
            return
        self.airports_list = load_airports(file)                    #   Load via Airport module
        self.update_airports()
        self._set_status(f"Aeropuertos cargados: {len(self.airports_list)}", C["green"])

                                #   Add a new airport from form fields  #
    def add_airport(self):
        try:
            ap = Airport(self.entry_icao.get(),                    #   Create Airport object from entries
                                  self.entry_lat.get(),
                                  self.entry_lon.get())
            TryFormat(ap)                                          #   Validate and format the object
            self.airports_list = add_airport(self.airports_list, ap)
            self.update_airports()
            self._set_status(f"Aeropuerto {ap.icao} añadido.", C["green"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

                                #   Remove an airport by ICAO from the list  #
    def delete_airport(self):
        icao = self.entry_icao.get()                                        #   Read ICAO field
        self.airports_list = remove_airport(self.airports_list, icao)
        self.update_airports()
        self._set_status(f"Aeropuerto {icao} eliminado.", C["accent"])

                                #   Save Schengen airports to a txt file  #
    def save_airports(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            save_schengen_airports(self.airports_list, file)
            self._set_status(f"Guardado en {os.path.basename(file)}", C["green"])

                                #   Show airport bar chart  #
    def plot_airports(self):
        plot_airport(self.airports_list)

                                #   Generate KML map file  #
    def map_airports(self):
        map_airport(self.airports_list)

                                #   Refresh the airports listbox  #
    def update_airports(self):
        self.listbox_airports.delete(0, tk.END)                            #   Clear existing rows
        i = 0                                                               #   Counter
        while i < len(self.airports_list):                                  #   While not end of list
            ap = self.airports_list[i]
            schengen = "✓ SCH" if getattr(ap, "schengen", False) else "  —  "
            line = f"  {ap.icao:<8}  {str(ap.lat):<14}  {str(ap.lon):<14}  {schengen}"
            self.listbox_airports.insert(tk.END, line)
            if getattr(ap, "schengen", False):                             #   Highlight Schengen in sky blue
                self.listbox_airports.itemconfig(tk.END, fg=C["accent2"])
            i += 1
        self._update_stats()

    ########################################
    #   Flights Logic
    ########################################

                                #   Load flights from a txt file  #
    def load_flights(self):
        file = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if not file:                                                        #   User canceled the dialog
            return
        self.aircraft_list = LoadArrivals(file)                            #   Load via Aircraft module
        self.update_flights()
        self._set_status(f"Vuelos cargados: {len(self.aircraft_list)}", C["green"])

                                #   Save current flights to a txt file  #
    def save_flights(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            SaveFlights(self.aircraft_list, file)
            self._set_status(f"Guardado en {os.path.basename(file)}", C["green"])

                                #   Plot arrivals by hour  #
    def plot_arrivals(self):
        if not self.aircraft_list:                                          #   Check list is not empty
            messagebox.showwarning("Sin datos", "No hay vuelos cargados.")
            return
        PlotArrivals(self.aircraft_list)

                                #   Plot arrivals grouped by airline  #
    def plot_airlines(self):
        if not self.aircraft_list:                                          #   Check list is not empty
            messagebox.showwarning("Sin datos", "No hay vuelos cargados.")
            return
        PlotAirlines(self.aircraft_list)

                                #   Plot Schengen vs non-Schengen breakdown  #
    def plot_flight_type(self):
        if not self.aircraft_list:                                          #   Check list is not empty
            messagebox.showwarning("Sin datos", "No hay vuelos cargados.")
            return
        PlotFlighType(self.aircraft_list)

                                #   Refresh the flights FIDS listbox  #
    def update_flights(self):
        self.listbox_flights.delete(0, tk.END)                             #   Clear existing rows
        i = 0                                                               #   Counter
        while i < len(self.aircraft_list):                                  #   While not end of list
            f = self.aircraft_list[i]
            line = f"  {f.id:<10}  {f.origin:<10}  {f.arrival_time:<8}  {f.airline}"
            self.listbox_flights.insert(tk.END, line)
            if i % 2 == 0:                                                 #   Alternate row shading
                self.listbox_flights.itemconfig(tk.END, bg="#1e2d45")
            i += 1
        self._update_stats()

    ########################################
    #   Gates Logic
    ########################################

                                #   Load airport terminal structure from file  #
    def load_airport_structure(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if not file_path:                                                   #   User canceled the dialog
            return
        file_dir     = os.path.dirname(os.path.abspath(file_path))
        cwd_original = os.getcwd()                                         #   Save original working directory
        try:
            os.chdir(file_dir)                                             #   Change to file's directory for relative imports
            bcn = LoadAirportStructure(file_path)
            if bcn == -1:                                                  #   -1 means file format error
                messagebox.showerror("Error",
                    "No se pudo cargar la estructura. Verifica el formato del archivo.")
            else:
                self.bcn_airport = bcn                                     #   Store the loaded structure
                self._update_stats()
                self._set_status("Estructura del aeropuerto cargada.", C["green"])
        except Exception as e:
            messagebox.showerror("Error Crítico", f"Fallo al procesar la estructura: {str(e)}")
        finally:
            os.chdir(cwd_original)                                         #   Always restore original directory

                                #   Assign gates to all loaded flights  #
    def assign_gates(self):
        if self.bcn_airport is None:                                        #   Check structure is loaded
            messagebox.showwarning("Advertencia",
                "Primero debes cargar la estructura del aeropuerto.")
            return
        if not self.aircraft_list:                                          #   Check flights are loaded
            messagebox.showwarning("Advertencia", "No hay vuelos cargados.")
            return

        unassigned = 0                                                      #   Counter for failed assignments
        i = 0                                                               #   Counter
        while i < len(self.aircraft_list):                                  #   While not end of list
            if AssignGate(self.bcn_airport, self.aircraft_list[i]) != 0:   #   0 means success
                unassigned += 1                                             #   Count failures
            i += 1

        if unassigned:                                                      #   If any failed, warn user
            messagebox.showwarning("Asignación Parcial",
                f"{unassigned} vuelo(s) sin puerta asignada.")
            self._set_status(f"Asignación parcial: {unassigned} sin puerta.", C["accent"])
        else:                                                               #   All assigned successfully
            messagebox.showinfo("Éxito", "Todos los vuelos asignados correctamente.")
            self._set_status("Todas las puertas asignadas.", C["green"])

        self._refresh_gate_list()                                           #   Refresh gate display

                                #   Show gate occupancy in the list panel  #

    def view_gate_occupancy(self):
        if self.bcn_airport is None:                                        #   Check structure is loaded
            messagebox.showwarning("Advertencia",
                "No hay estructura de aeropuerto cargada.")
            return
        self._refresh_gate_list()
        self._set_status("Ocupación de puertas actualizada.", C["accent2"])

                                #   Rebuild the gate status listbox  #
    def _refresh_gate_list(self):
        if self.bcn_airport is None:                                        #   Nothing to show if not loaded
            return
        occupancy_data = GateOccupancy(self.bcn_airport)
        if occupancy_data == -1 or not occupancy_data:                     #   -1 or empty means error
            return

        self.listbox_gates.delete(0, tk.END)                           #   Clear existing rows
        free = 0                                                            #   Counter free gates
        occupied = 0                                                        #   Counter occupied gates
        i = 0                                                               #   Counter
        while i < len(occupancy_data):                                      #   While not end of list
            gate_name  = occupancy_data[i][0]
            status     = occupancy_data[i][1]
            aircraft_id = occupancy_data[i][2]
            if status == "Occupied":                                        #   Occupied: red row
                text = f"  🔴  {gate_name:<14}  OCUPADA  →  {aircraft_id}"
                self.listbox_gates.insert(tk.END, text)
                self.listbox_gates.itemconfig(tk.END, fg=C["red"], bg="#2d1515")
                occupied += 1
            else:                                                           #   Free: green row
                text = f"  🟢  {gate_name:<14}  LIBRE"
                self.listbox_gates.insert(tk.END, text)
                self.listbox_gates.itemconfig(tk.END, fg=C["green"], bg="#0f1f13")
                free += 1
            i += 1

        self._set_status(                                                   #   Update status bar summary
            f"Puertas: {free} libres · {occupied} ocupadas",
            C["green"] if occupied == 0 else C["accent"]
        )


########################################
#   Entry Point
########################################

if __name__ == "__main__":
    root = tk.Tk()
    app  = AirportManagerApp(root)                                          #   Create and launch the app
    root.mainloop()