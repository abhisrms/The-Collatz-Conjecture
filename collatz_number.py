import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.collections import LineCollection

# First define the CollatzVisualizer class
class CollatzVisualizer:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.cmap = plt.cm.get_cmap('gist_rainbow')
        self.angle_even = np.radians(self.angle_even)
        self.angle_odd = np.radians(self.angle_odd)

    def generate_starts(self):
        half = self.num_sequences // 2
        evens = np.random.choice(np.arange(2, self.max_start, 2), half, False)
        odds = np.random.choice(np.arange(3, self.max_start, 2), half, False)
        return np.concatenate([evens, odds])

    def collatz_sequence(self, n):
        seq = []
        while n != 1 and len(seq) < self.max_depth:
            seq.append(n)
            n = n//2 if n%2 ==0 else 3*n+1
        seq.append(1)
        return seq

    def generate_path(self, sequence):
        x, y, angle = 0, 0, np.pi/2
        path = []
        for num in sequence:
            new_x = x + self.branch_length * np.cos(angle)
            new_y = y + self.branch_length * np.sin(angle)
            path.append((x, y, new_x, new_y))
            angle += self.angle_even if num%2 ==0 else self.angle_odd
            x, y = new_x, new_y
        return path

    def draw(self, ax):
        ax.set_facecolor('black')
        ax.axis('off')
        starts = self.generate_starts()
        colors = self.cmap(np.linspace(0, 1, len(starts)))

        for start, color in zip(starts, colors):
            seq = self.collatz_sequence(start)
            path = self.generate_path(seq)
            
            segments = [[(x1,y1),(x2,y2)] for x1,y1,x2,y2 in path]
            lc = LineCollection(segments, colors=[color], linewidths=1.5, alpha=0.8)
            ax.add_collection(lc)
            
            if segments:
                last_x, last_y = segments[-1][1]
                ax.text(last_x, last_y, str(start),
                        color='white',
                        fontsize=self.font_size,
                        ha='center',
                        va='center',
                        rotation=np.degrees(np.arctan2(last_y, last_x)) - 90)

        ax.scatter(0, 0, s=50, c='white', edgecolors='black', zorder=3)
        ax.set_title("Collatz Sequences with Interactive Controls", color='white', pad=20)
        
class CollatzVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Collatz Conjecture Visualizer")
        self.root.configure(bg='black')  # Main window background
        
        # Create dark theme style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background='black', foreground='white')
        self.style.configure('TEntry', fieldbackground='#333', foreground='white')
        self.style.map('TEntry', 
                     fieldbackground=[('active', '#444'), ('!active', '#333')],
                     foreground=[('active', 'white'), ('!active', 'white')])
        
        # Create input frame
        input_frame = ttk.Frame(root, padding=10)
        input_frame.grid(row=0, column=0, sticky="nsew")
        
        # Parameters with default values
        self.params = {
            'num_sequences': tk.IntVar(value=20),
            'max_start': tk.IntVar(value=500),
            'angle_even': tk.DoubleVar(value=-8),
            'angle_odd': tk.DoubleVar(value=16),
            'branch_length': tk.DoubleVar(value=0.5),
            'max_depth': tk.IntVar(value=25),
            'font_size': tk.IntVar(value=8)
        }
        
        # Create dark-themed widgets
        ttk.Label(input_frame, text="Number of Sequences (even):", style='TLabel').grid(row=0, column=0, sticky="w", pady=2)
        ttk.Entry(input_frame, textvariable=self.params['num_sequences']).grid(row=0, column=1, pady=2)
        
        ttk.Label(input_frame, text="Max Starting Number:", style='TLabel').grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(input_frame, textvariable=self.params['max_start']).grid(row=1, column=1, pady=2)
        
        ttk.Label(input_frame, text="Even Angle:", style='TLabel').grid(row=2, column=0, sticky="w", pady=2)
        ttk.Entry(input_frame, textvariable=self.params['angle_even']).grid(row=2, column=1, pady=2)
        
        ttk.Label(input_frame, text="Odd Angle:", style='TLabel').grid(row=3, column=0, sticky="w", pady=2)
        ttk.Entry(input_frame, textvariable=self.params['angle_odd']).grid(row=3, column=1, pady=2)
        
        ttk.Label(input_frame, text="Branch Length:", style='TLabel').grid(row=4, column=0, sticky="w", pady=2)
        ttk.Entry(input_frame, textvariable=self.params['branch_length']).grid(row=4, column=1, pady=2)
        
        ttk.Label(input_frame, text="Max Depth:", style='TLabel').grid(row=5, column=0, sticky="w", pady=2)
        ttk.Entry(input_frame, textvariable=self.params['max_depth']).grid(row=5, column=1, pady=2)
        
        ttk.Label(input_frame, text="Label Font Size:", style='TLabel').grid(row=6, column=0, sticky="w", pady=2)
        ttk.Entry(input_frame, textvariable=self.params['font_size']).grid(row=6, column=1, pady=2)
        
        ttk.Button(input_frame, text="Generate", command=self.update_visualization, style='Dark.TButton').grid(row=7, columnspan=2, pady=10)
        
        # Button style
        self.style.configure('Dark.TButton', 
                           background='#444', 
                           foreground='white',
                           bordercolor='#666',
                           lightcolor='#333',
                           darkcolor='#333')
        self.style.map('Dark.TButton',
                     background=[('active', '#555'), ('!active', '#444')],
                     foreground=[('active', 'white'), ('!active', 'white')])
        
        # Visualization frame
        self.viz_frame = ttk.Frame(root, padding=10)
        self.viz_frame.grid(row=0, column=1, sticky="nsew")
        
        # Configure grid weights
        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Initialize plot with dark background
        self.fig = plt.Figure(figsize=(10, 6), facecolor='black')
        self.ax = self.fig.add_subplot(111, facecolor='black')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_visualization(self):
        try:
            self.ax.clear()
            params = {k: v.get() for k, v in self.params.items()}
            
            if params['num_sequences'] % 2 != 0:
                raise ValueError("Number of sequences must be even")
            
            vis = CollatzVisualizer(**params)
            vis.draw(self.ax)
            
            # Maintain dark theme after redraw
            self.ax.set_facecolor('black')
            for text in self.ax.texts:
                text.set_color('white')
            
            self.canvas.draw()
            
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

# Rest of the CollatzVisualizer class remains unchanged from previous version

if __name__ == "__main__":
    root = tk.Tk()
    app = CollatzVisualizerApp(root)
    root.mainloop()