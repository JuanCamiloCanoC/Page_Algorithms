import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==========================================
# LÓGICA DE LOS ALGORITMOS
# ==========================================

def simulate_fifo(pages, capacity):
    memory, history, faults, replaced, outs = [], [], [], [], []
    page_faults = 0

    for page in pages:
        fault = page not in memory
        removed = None

        if fault:
            page_faults += 1
            if len(memory) < capacity:
                memory.append(page)
            else:
                removed = memory.pop(0)
                memory.append(page)
                outs.append(removed)

        faults.append(fault)
        replaced.append(removed)
        history.append(memory.copy())

    return page_faults, outs, history, faults, replaced

def simulate_lru(pages, capacity):
    memory, history, faults, replaced, outs = [], [], [], [], []
    page_faults = 0

    for page in pages:
        fault = page not in memory
        removed = None

        if fault:
            page_faults += 1
            if len(memory) < capacity:
                memory.append(page)
            else:
                removed = memory.pop(0)
                memory.append(page)
                outs.append(removed)
        else:
            memory.remove(page)
            memory.append(page)

        faults.append(fault)
        replaced.append(removed)
        history.append(memory.copy())

    return page_faults, outs, history, faults, replaced

def simulate_mru(pages, capacity):
    memory, history, faults, replaced, outs = [], [], [], [], []
    page_faults = 0

    for page in pages:
        fault = page not in memory
        removed = None

        if fault:
            page_faults += 1
            if len(memory) < capacity:
                memory.append(page)
            else:
                removed = memory.pop(-1)
                memory.append(page)
                outs.append(removed)
        else:
            memory.remove(page)
            memory.append(page)

        faults.append(fault)
        replaced.append(removed)
        history.append(memory.copy())

    return page_faults, outs, history, faults, replaced

def simulate_clock(pages, capacity):
    memory, history, faults, replaced, outs = [], [], [], [], []
    reference_bits = [0] * capacity
    pointer = 0
    page_faults = 0

    for page in pages:
        fault = page not in memory
        removed = None

        if fault:
            page_faults += 1
            if len(memory) < capacity:
                memory.append(page)
                reference_bits[len(memory) - 1] = 1
            else:
                while reference_bits[pointer] == 1:
                    reference_bits[pointer] = 0
                    pointer = (pointer + 1) % capacity
                removed = memory[pointer]
                memory[pointer] = page
                reference_bits[pointer] = 1
                pointer = (pointer + 1) % capacity
                outs.append(removed)
        else:
            index = memory.index(page)
            reference_bits[index] = 1

        faults.append(fault)
        replaced.append(removed)
        history.append(memory.copy())

    return page_faults, outs, history, faults, replaced

ALGORITHMS = {
    "FIFO": simulate_fifo,
    "LRU": simulate_lru,
    "MRU": simulate_mru,
    "Clock": simulate_clock,
}

# ==========================================
# INTERFAZ GRÁFICA
# ==========================================

class PageReplacementSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmos de paginacion - Simulador Visual")
        self.root.geometry("1200x720")
        self.root.minsize(980, 680)

        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        palette = {
            "bg": "#f3f6fb",
            "card": "#ffffff",
            "text": "#1f2937",
            "muted": "#5b6578",
            "border": "#d7deeb",
            "accent": "#2f6fed",
            "accent_hover": "#2558bc",
            "success_bg": "#dcfce7",
            "warning_bg": "#fef3c7",
        }

        self.colors = palette
        self.root.configure(bg=palette["bg"])

        style.configure("App.TFrame", background=palette["bg"])
        style.configure("Card.TFrame", background=palette["card"])
        style.configure("App.TLabel", background=palette["bg"], foreground=palette["text"], font=("Segoe UI", 10))
        style.configure("Card.TLabel", background=palette["card"], foreground=palette["text"], font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=palette["bg"], foreground="#111827", font=("Segoe UI", 24, "bold"))
        style.configure("Subtitle.TLabel", background=palette["bg"], foreground=palette["muted"], font=("Segoe UI", 10))
        style.configure("StatTitle.TLabel", background=palette["card"], foreground=palette["muted"], font=("Segoe UI", 9, "bold"))
        style.configure("StatValue.TLabel", background=palette["card"], foreground=palette["text"], font=("Segoe UI", 15, "bold"))

        style.configure(
            "Modern.TLabelframe",
            background=palette["card"],
            bordercolor=palette["border"],
            relief="solid",
            borderwidth=1,
        )
        style.configure(
            "Modern.TLabelframe.Label",
            background=palette["card"],
            foreground=palette["text"],
            font=("Segoe UI", 10, "bold"),
        )

        style.configure(
            "Modern.TEntry",
            fieldbackground="#f9fbff",
            bordercolor=palette["border"],
            foreground=palette["text"],
            insertcolor=palette["text"],
            padding=7,
        )
        style.map("Modern.TEntry", bordercolor=[("focus", palette["accent"])])

        style.configure(
            "Modern.TCombobox",
            fieldbackground="#f9fbff",
            bordercolor=palette["border"],
            foreground=palette["text"],
            padding=6,
        )
        style.map("Modern.TCombobox", bordercolor=[("focus", palette["accent"])])

        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground="#ffffff",
            background=palette["accent"],
            borderwidth=0,
            padding=(12, 10),
        )
        style.map(
            "Accent.TButton",
            background=[("active", palette["accent_hover"]), ("pressed", palette["accent_hover"])],
        )

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, style="App.TFrame", padding=18)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(main_frame, text="Algoritmos de Paginacion", style="Title.TLabel")
        title.grid(row=0, column=0, columnspan=3, sticky="w")

        controls_card = ttk.LabelFrame(main_frame, text="Configuracion", style="Modern.TLabelframe", padding=14)
        controls_card.grid(row=2, column=0, sticky="nsew", padx=(0, 10), pady=(0, 12))

        stats_card = ttk.LabelFrame(main_frame, text="Resumen", style="Modern.TLabelframe", padding=14)
        stats_card.grid(row=2, column=1, columnspan=2, sticky="nsew", pady=(0, 12))

        controls_card.columnconfigure(1, weight=1)
        stats_card.columnconfigure(0, weight=1)
        stats_card.columnconfigure(1, weight=1)
        stats_card.columnconfigure(2, weight=1)

        ttk.Label(controls_card, text="Paginas (espacio/coma):", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        self.pages_entry = ttk.Entry(controls_card, width=50, style="Modern.TEntry")
        self.pages_entry.grid(row=0, column=1, sticky="ew", pady=6)
        self.pages_entry.insert(0, "1 2 3 4 1 2 5 1 2 3 4 5")

        ttk.Label(controls_card, text="Capacidad de marcos:", style="Card.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        self.capacity_entry = ttk.Entry(controls_card, width=20, style="Modern.TEntry")
        self.capacity_entry.grid(row=1, column=1, sticky="w", pady=6)
        self.capacity_entry.insert(0, "3")

        ttk.Label(controls_card, text="Algoritmo:", style="Card.TLabel").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
        self.algorithm_combo = ttk.Combobox(
            controls_card,
            values=list(ALGORITHMS.keys()),
            state="readonly",
            width=18,
            style="Modern.TCombobox",
        )
        self.algorithm_combo.grid(row=2, column=1, sticky="w", pady=6)
        self.algorithm_combo.set("FIFO")

        run_button = ttk.Button(controls_card, text="Ejecutar Simulacion", style="Accent.TButton", command=self.run_simulation)
        run_button.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        self.stat_algorithm = tk.StringVar(value="-")
        self.stat_faults = tk.StringVar(value="0")
        self.stat_replaced = tk.StringVar(value="0")

        self.build_stat_tile(stats_card, 0, "Algoritmo", self.stat_algorithm, self.colors["card"])
        self.build_stat_tile(stats_card, 1, "Fallos de Pagina", self.stat_faults, self.colors["success_bg"])
        self.build_stat_tile(stats_card, 2, "Reemplazos", self.stat_replaced, self.colors["warning_bg"])

        self.summary_var = tk.StringVar(value="Ejecuta una simulacion para ver la linea de tiempo.")
        summary_label = ttk.Label(main_frame, textvariable=self.summary_var, style="Subtitle.TLabel")
        summary_label.grid(row=3, column=0, columnspan=3, sticky="w", pady=(0, 10))

        self.visual_frame = ttk.LabelFrame(main_frame, text="Vista de Simulacion", style="Modern.TLabelframe", padding=10)
        self.visual_frame.grid(row=4, column=0, columnspan=3, sticky="nsew")

        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=2)
        main_frame.columnconfigure(2, weight=2)
        main_frame.rowconfigure(4, weight=1)

        self.figure = plt.Figure(figsize=(11, 4.8), dpi=100)
        self.figure.patch.set_facecolor(self.colors["card"])
        self.ax = self.figure.add_subplot(111)
        self.ax.axis('off')
        self.ax.set_facecolor(self.colors["card"])
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.visual_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def build_stat_tile(self, parent, column, title, value_var, bg_color):
        tile = tk.Frame(parent, bg=bg_color, highlightbackground=self.colors["border"], highlightthickness=1)
        tile.grid(row=0, column=column, padx=(0 if column == 0 else 8, 0), sticky="nsew")
        title_lbl = tk.Label(tile, text=title, bg=bg_color, fg=self.colors["muted"], font=("Segoe UI", 9, "bold"))
        title_lbl.pack(anchor="w", padx=10, pady=(8, 2))
        value_lbl = tk.Label(tile, textvariable=value_var, bg=bg_color, fg=self.colors["text"], font=("Segoe UI", 16, "bold"))
        value_lbl.pack(anchor="w", padx=10, pady=(0, 10))

    def parse_pages(self, raw_pages):
        cleaned = raw_pages.replace(",", " ").split()
        if not cleaned:
            raise ValueError("Por favor, ingresa al menos un número de página.")
        try:
            return [int(page) for page in cleaned]
        except ValueError:
            raise ValueError("Las páginas deben ser números enteros.")

    def run_simulation(self):
        algorithm_name = self.algorithm_combo.get()
        raw_pages = self.pages_entry.get()
        raw_capacity = self.capacity_entry.get()

        try:
            pages = self.parse_pages(raw_pages)
            capacity = int(raw_capacity)
            if capacity <= 0:
                raise ValueError()
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e) if str(e) else "La capacidad debe ser un entero positivo.")
            return

        # Ejecutar algoritmo
        simulate_fn = ALGORITHMS[algorithm_name]
        page_faults, outs, history, fault_timeline, replaced_timeline = simulate_fn(pages, capacity)

        # Actualizar resumen de texto
        self.stat_algorithm.set(algorithm_name)
        self.stat_faults.set(str(page_faults))
        self.stat_replaced.set(str(len(outs)))
        replaced_label = outs if outs else "ninguna"
        self.summary_var.set(f"Secuencia evaluada con {algorithm_name}. Reemplazos en orden: {replaced_label}")

        # Dibujar la tabla
        self.render_matplotlib_table(pages, capacity, history, fault_timeline, replaced_timeline)

    def render_matplotlib_table(self, pages, capacity, history, fault_timeline, replaced_timeline):
        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_facecolor(self.colors["card"])

        # Preparar los datos para la tabla
        row_labels = ["Referencia"] + [f"Marco {i+1}" for i in range(capacity)] + ["Fallo", "Reemplazo"]

        cell_text = []
        cell_colors = []

        for _ in range(len(row_labels)):
            cell_text.append([""] * len(pages))
            cell_colors.append(["#ffffff"] * len(pages))

        for col, page in enumerate(pages):
            # Fila de Referencia
            cell_text[0][col] = str(page)
            cell_colors[0][col] = "#bfe9d0"

            # Filas de Marcos de Memoria
            state = history[col]
            for frame_idx in range(capacity):
                if frame_idx < len(state):
                    cell_text[frame_idx + 1][col] = str(state[frame_idx])

            # Fila de Fallos
            if fault_timeline[col]:
                cell_text[capacity + 1][col] = "X"
                cell_colors[capacity + 1][col] = "#ffd6d6"

            # Fila de Reemplazos
            if replaced_timeline[col] is not None:
                cell_text[capacity + 2][col] = str(replaced_timeline[col])
                cell_colors[capacity + 2][col] = "#ffefad"

        # Crear la tabla
        table = self.ax.table(
            cellText=cell_text,
            cellColours=cell_colors,
            rowLabels=row_labels,
            loc='center',
            cellLoc='center'
        )

        # Estilizar la tabla
        table.scale(1.0, 2.0)
        table.auto_set_font_size(False)
        table.set_fontsize(11)

        for (row, col), cell in table.get_celld().items():
            cell.set_edgecolor("#d3dbea")
            cell.set_linewidth(1.0)
            if col == -1:
                cell.set_facecolor("#eef2fb")
                cell.set_text_props(weight='bold', color="#27324a")
            if row == capacity + 1 and col >= 0 and fault_timeline[col]:
                cell.set_text_props(weight='bold', color="#a52c2c")
            if row == capacity + 2 and col >= 0 and replaced_timeline[col] is not None:
                cell.set_text_props(weight='bold', color="#7a5600")

        self.ax.set_title(
            "Linea de Tiempo de Referencias",
            fontsize=13,
            fontweight='bold',
            color="#24314a",
            pad=12,
        )

        self.figure.tight_layout(pad=1.2)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementSimulatorApp(root)
    root.mainloop()