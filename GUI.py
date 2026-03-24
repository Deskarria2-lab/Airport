#V0.0 PROTOTIPO!!!!

import tkinter as tk
from tkinter import messagebox, filedialog
import Airport
lista_aeropuertos = []

class AirportManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Aeropuertos - V1")
        self.root.geometry("750x500")
        self.airports_list = []

        self.setup_ui()

    def setup_ui(self):
        #PANEL SUPERIOR
        frame_top = tk.Frame(self.root, pady=10)
        frame_top.pack(fill=tk.X)
        tk.Button(frame_top, text="Cargar Archivos", command=self.load_data).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_top, text="Guardar Schengen", command=self.save_data).pack(side=tk.LEFT, padx=10)

        #CONTENEDOR CENTRAL
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #PANEL IZQUIERDO
        frame_left = tk.Frame(main_frame)
        frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Label(frame_left, text="Código ICAO:").pack(anchor=tk.W)
        self.entry_icao = tk.Entry(frame_left)
        self.entry_icao.pack(pady=2)

        tk.Label(frame_left, text="Latitud:").pack(anchor=tk.W)
        self.entry_lat = tk.Entry(frame_left)
        self.entry_lat.pack(pady=2)

        tk.Label(frame_left, text="Longitud:").pack(anchor=tk.W)
        self.entry_lon = tk.Entry(frame_left)
        self.entry_lon.pack(pady=2)

        tk.Button(frame_left, text="Añadir Aeropuerto", command=self.add_airport).pack(pady=10)
        tk.Button(frame_left, text="Eliminar Aeropuerto", command=self.delete_airport).pack(pady=5)

        #PANEL DERECHO
        frame_right = tk.Frame(main_frame)
        frame_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(frame_right, text="Lista de Aeropuertos:").pack(anchor=tk.W)
        self.listbox = tk.Listbox(frame_right, font=("Courier", 10))
        self.listbox.pack(fill=tk.BOTH, expand=True)

        #PANEL INFERIOR
        frame_bottom = tk.Frame(self.root, pady=10)
        frame_bottom.pack(fill=tk.X)
        tk.Button(frame_bottom, text="Gráfico Schengen", command=self.show_plot).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_bottom, text="Ver en Google Earth", command=self.show_map).pack(side=tk.LEFT, padx=10)

    def load_data(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not filename: return
        try:
            self.airports_list = Airport.LoadAirports(filename)
            self.update_listbox()
            messagebox.showinfo("Éxito", f"Datos cargados.")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al leer el archivo: {e}")

    def add_airport(self):
        icao = self.entry_icao.get().strip().upper()
        lat_str = self.entry_lat.get().strip()
        lon_str = self.entry_lon.get().strip()

        if not icao or not lat_str or not lon_str:
            messagebox.showwarning("Error", "Faltan datos.")
            return

        # Para que tu AddAirport funcione, DEBEMOS instanciar el objeto aquí
        nuevo_ap = Airport.Airport(icao, lat_str, lon_str)

        try:
            Airport.TryFormat(nuevo_ap)  # Usamos tu validador
            self.airports_list = Airport.AddAirport(self.airports_list, nuevo_ap)
            self.update_listbox()
        except Exception as e:
            messagebox.showerror("Error de formato", str(e))

    def delete_airport(self):
        icao = self.entry_icao.get().strip().upper()
        if not icao: return

        len_antes = len(self.airports_list)
        self.airports_list = Airport.RemoveAirport(self.airports_list, icao)

        if len(self.airports_list) == len_antes:
            messagebox.showerror("Error", "No encontrado.")
        else:
            self.update_listbox()

    def save_data(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            Airport.SaveSchengenAirports(self.airports_list, filename)
            messagebox.showinfo("Éxito", "Guardado.")

    def show_plot(self):
        Airport.PlotAirport(self.airports_list)

    def show_map(self):
        Airport.MapAirport(self.airports_list)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for ap in self.airports_list:
            texto = f"ICAO: {ap.icao} | Lat: {ap.lat:.4f} | Lon: {ap.lon:.4f}"
            self.listbox.insert(tk.END, texto)


if __name__ == "__main__":
    ventana = tk.Tk()
    app = AirportManagerApp(ventana)
    ventana.mainloop()