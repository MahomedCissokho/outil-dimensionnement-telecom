import tkinter as tk
from tkinter import ttk
from math import cos, sin, sqrt, radians

class FillHexagon:
    def __init__(self, parent, x, y, length, color, tags):
        self.parent = parent
        self.x = x
        self.y = y
        self.length = length
        self.color = color
        self.selected = False
        self.tags = tags
        self.draw()

    def draw(self):
        start_x = self.x
        start_y = self.y
        angle = 60
        coords = []
        for i in range(6):
            end_x = start_x + self.length * cos(radians(angle * i))
            end_y = start_y + self.length * sin(radians(angle * i))
            coords.append([start_x, start_y])
            start_x = end_x
            start_y = end_y
        self.parent.create_polygon(
            coords[0][0], coords[0][1], 
            coords[1][0], coords[1][1],
            coords[2][0], coords[2][1],
            coords[3][0], coords[3][1],
            coords[4][0], coords[4][1], 
            coords[5][0], coords[5][1], 
            fill=self.color, outline="gray", tags=self.tags
        )

class FrequencyReuseGame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Outil de Répartition de la Fréquence et de Calcul de la Capacité")
        self.rowconfigure(0, minsize=800, weight=1)
        self.columnconfigure(0, minsize=150, weight=1)
        self.columnconfigure(3, minsize=800, weight=1)
        
        self.hex_frame = tk.Canvas(self, width=300, height=300, bg="#ffffff")
        self.hexagons = []
        self.selected_hexagons = {}
        
        self.colors = ["pink", "orange", "yellow", "purple", "cyan", "magenta", "blue", "green", "red", "brown"]
        self.color_index = 0

        menu = tk.Frame(self)
        self.first_cell = None
        self.click_count = 0
        
        self.i_entry = tk.Entry(master=menu, width=10)
        i_lbl = tk.Label(master=menu, text="i :", width=2)
        
        self.j_entry = tk.Entry(master=menu, width=10)
        j_lbl = tk.Label(master=menu, text="j :", width=2)
        
        i_lbl.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.i_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        j_lbl.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.j_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        self.n_lbl = tk.Label(master=menu, text="N :")
        self.n_lbl.grid(row=2, column=0, columnspan=2)
        
        self.start_btn = tk.Button(menu, text="Commencer", width=10, command=self.start)
        self.reset_btn = tk.Button(menu, text="Réinitialiser", width=10, command=self.reset)
        self.end_btn = tk.Button(menu, state="disabled", text="Terminer", width=10, command=self.end)
        
        self.start_btn.grid(row=3, column=0, sticky="n", padx=5, pady=5, columnspan=2)
        self.reset_btn.grid(row=4, column=0, sticky="n", padx=5, pady=5, columnspan=2)
        self.end_btn.grid(row=5, column=0, sticky="n", padx=5, pady=5, columnspan=2)
        
        self.res_lbl = tk.Label(master=menu, text="")
        self.res_lbl.grid(row=6, column=0, columnspan=2)
        
        sep = ttk.Separator(orient=tk.VERTICAL)
        
        self.initGrid(25, 25, 40, debug=False)
        
        menu.grid(row=0, column=0, sticky="ns", pady=20)
        sep.grid(row=0, column=2, sticky="ns")
        self.hex_frame.grid(row=0, column=3, sticky="nsew")

        # Bouton pour ouvrir la fenêtre de calcul de capacité
        self.capacity_btn = tk.Button(menu, text="Calculer la Capacité", width=20, command=self.open_capacity_window)
        self.capacity_btn.grid(row=7, column=0, columnspan=2, pady=10)

    def initGrid(self, cols, rows, size, debug):
        for c in range(cols):
            if c % 2 == 0:
                offset = size * sqrt(3) / 2
            else:
                offset = 0
            for r in range(rows):
                if debug:
                    coords = "{}, {}".format(c, 2*r if c%2==0 else 2*r-1)
                    self.hex_frame.create_text(c*(size*1.5) + (size/2), (r*(size*sqrt(3))) + offset + (size/2), text=coords)
                h = FillHexagon(self.hex_frame, c*(size*1.5), (r*(size*sqrt(3))) + offset, size, "#ffffff", "{}.{}".format(c, 2*r if c%2==0 else 2*r-1))
                self.hexagons.append(h)

    def click(self, evt):
        x, y = evt.x, evt.y
        clicked = self.hex_frame.find_closest(x, y)[0] # find closest hexagon
        if self.click_count < self.n:
            color = self.colors[self.click_count % len(self.colors)]
            self.hex_frame.itemconfigure(self.hexagons[int(clicked)-1].tags, fill=color)
            self.hexagons[int(clicked)-1].selected = True
            self.selected_hexagons[self.hexagons[int(clicked)-1].tags] = color
            self.click_count += 1

    def reset(self):
        for i in self.hexagons:
            self.hex_frame.itemconfigure(i.tags, fill="#ffffff")
            i.selected = False
        self.first_cell = None
        self.reset_btn["state"] = "active"
        self.end_btn["state"] = "active"
        self.start_btn["state"] = "active"
        self.points = 0
        self.res_lbl["text"] = ""
        self.i_entry["state"] = "normal"
        self.j_entry["state"] = "normal"
        self.click_count = 0
        self.selected_hexagons = {}

    def calculate_n(self):
        i = int(self.i_entry.get()) if self.i_entry.get() != "" else 0
        j = int(self.j_entry.get()) if self.j_entry.get() != "" else 0
        self.n = i**2 + j**2 + i*j
        self.n_lbl["text"] = f"N : {self.n}"

    def start(self):
        self.calculate_n()
        self.reset()
        self.hex_frame.bind("<Button-1>", self.click)
        self.i_entry["state"] = "readonly"
        self.j_entry["state"] = "readonly"
        self.end_btn["state"] = "active"

    def end(self):
        self.reset_btn["state"] = "active"
        self.end_btn["state"] = "disabled"
        self.start_btn["state"] = "active"
        self.i_entry["state"] = "normal"
        self.j_entry["state"] = "normal"
        self.find_cells()
        self.hex_frame.unbind("<Button-1>")

    def find_cells(self):
        i = int(self.i_entry.get()) if self.i_entry.get() != "" else 0
        j = int(self.j_entry.get()) if self.j_entry.get() != "" else 0
        
        for cell_tag, color in self.selected_hexagons.items():
            f_x, f_y = map(int, cell_tag.split("."))
            cells = [
                f"{f_x-j}.{f_y-2*i-j}", f"{f_x-i-j}.{f_y-i+j}", 
                f"{f_x-i}.{f_y+i+2*j}", f"{f_x+j}.{f_y+2*i+j}", 
                f"{f_x+i+j}.{f_y+i-j}", f"{f_x+i}.{f_y-i-2*j}"
            ]

            for cell in cells:
                self.hex_frame.itemconfigure(cell, fill=color)

    def open_capacity_window(self):
        # Ouvre une nouvelle fenêtre pour le calcul de capacité
        self.capacity_window = tk.Toplevel(self)
        self.capacity_window.title("Calcul de la Capacité")
        
        tk.Label(self.capacity_window, text="Surface Totale :").grid(row=0, column=0, padx=10, pady=5)
        self.total_area_entry = tk.Entry(self.capacity_window)
        self.total_area_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.capacity_window, text="Surface d'une Cellule :").grid(row=1, column=0, padx=10, pady=5)
        self.cell_area_entry = tk.Entry(self.capacity_window)
        self.cell_area_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(self.capacity_window, text="Nombre de Canaux :").grid(row=2, column=0, padx=10, pady=5)
        self.channels_entry = tk.Entry(self.capacity_window)
        self.channels_entry.grid(row=2, column=1, padx=10, pady=5)
        
        self.calculate_btn = tk.Button(self.capacity_window, text="Calculer", command=self.calculate_capacity)
        self.calculate_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.capacity_lbl = tk.Label(self.capacity_window, text="")
        self.capacity_lbl.grid(row=4, column=0, columnspan=2)

    def calculate_capacity(self):
        # Lire les valeurs des entrées
        total_area = float(self.total_area_entry.get())
        cell_area = float(self.cell_area_entry.get())
        channels = int(self.channels_entry.get())

        # Calculer la capacité
        capacity = (total_area / cell_area) * (channels / self.n)
        self.capacity_lbl["text"] = f"Capacité: {capacity:.2f}"

if __name__ == "__main__":
    window = FrequencyReuseGame()
    window.mainloop()
