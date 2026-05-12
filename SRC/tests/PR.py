import tkinter as tk
from tkinter import messagebox, filedialog


# Asumo que tus imports funcionan correctamente
# from SRC.Airportsfunctions.Airport import *
# from SRC.Airportsfunctions.Aircraft import *

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Aeronáutica v0.1")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")

        # Datos compartidos entre ventanas
        self.airports_list = []
        self.aircraft_list = []

        self.setup_main_ui()

    def setup_main_ui(self):
        # Título
        tk.Label(self.root, text="AIRPORT MANAGER", font=("Helvetica", 18, "bold"), bg="#f0f0f0", pady=20).pack()

        # Contenedor de botones
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(expand=True)

        # Botones Principales
        tk.Button(btn_frame, text="Gestión de Aeropuertos", width=25, height=2,
                  command=self.open_airport_manager, font=("Arial", 10)).pack(pady=10)

        tk.Button(btn_frame, text="Gestión de Vuelos", width=25, height=2,
                  command=self.open_flight_manager, font=("Arial", 10)).pack(pady=10)

        tk.Button(btn_frame, text="Análisis y Gráficos", width=25, height=2,
                  command=self.open_analytics, font=("Arial", 10)).pack(pady=10)

        tk.Button(btn_frame, text="Salir", width=25, command=self.root.quit, fg="red").pack(pady=30)

    # --- Métodos para abrir ventanas nuevas ---

    def open_airport_manager(self):
        # Creamos una ventana secundaria
        new_window = tk.Toplevel(self.root)
        new_window.title("Editor de Aeropuertos")
        new_window.geometry("600x400")

        # Aquí meterías la lógica de añadir/eliminar que tenías en tu código original
        tk.Label(new_window, text="Panel de Control de Aeropuertos", font=("Arial", 12, "bold")).pack(pady=10)

        # Ejemplo rápido de integración con tu lógica anterior:
        frame_inputs = tk.Frame(new_window)
        frame_inputs.pack(pady=10)

        tk.Label(frame_inputs, text="ICAO:").grid(row=0, column=0)
        entry_icao = tk.Entry(frame_inputs)
        entry_icao.grid(row=0, column=1)

        # Botón para ejecutar la función que ya tenías
        tk.Button(new_window, text="Cargar desde Archivo", command=self.load_airports_logic).pack()

    def open_flight_manager(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Gestión de Vuelos")
        new_window.geometry("600x400")
        tk.Label(new_window, text="Listado de Vuelos Actuales", font=("Arial", 12, "bold")).pack(pady=10)
        # ... (Contenido similar al anterior)

    def open_analytics(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Estadísticas")
        new_window.geometry("400x300")

        tk.Button(new_window, text="Ver Mapa", command=self.map_logic).pack(fill=tk.X, padx=50, pady=10)
        tk.Button(new_window, text="Llegadas por Hora", command=self.plot_arrivals_logic).pack(fill=tk.X, padx=50,
                                                                                               pady=10)

    # --- Lógica (Aquí conectas con tus clases Airport y Aircraft) ---

    def load_airports_logic(self):
        file = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if file:
            # self.airports_list = Airport.LoadAirports(file)
            messagebox.showinfo("Éxito", "Aeropuertos cargados")

    def map_logic(self):
        # Airport.MapAirport(self.airports_list)
        print("Generando mapa...")

    def plot_arrivals_logic(self):
        if not self.aircraft_list:
            messagebox.showwarning("Aviso", "No hay datos de vuelos cargados.")
        else:
            # PlotArrivals(self.aircraft_list)
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()