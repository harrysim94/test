import random
import tkinter as tk

class InteractiveGrid:
    def __init__(self, root, rows=10, cols=10, cell_size=40):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size, bg='white')
        self.canvas.pack()
        self.cells = {}  # Store cell rectangles
        self.pairs = {"A": ((random.randint(0, rows-1), random.randint(0, cols-1)),
                              (random.randint(0, rows-1), random.randint(0, cols-1))),
                      "B": ((random.randint(0, rows-1), random.randint(0, cols-1)),
                              (random.randint(0, rows-1), random.randint(0, cols-1)))}           
        self.create_grid()
        self.canvas.bind("<Button-1>", self.on_click)
    
    def create_grid(self):
        # Create grid
        for row in range(self.rows):
            for col in range(self.cols):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='white')
                self.cells[(row, col)] = rect
        # Add pair labels to the grid
        cell_width = 500 / self.cols
        cell_height = 500 / self.rows
        for key, (start, end) in self.pairs.items():
            sx, sy = start
            ex, ey = end
            self.canvas.create_text(sy * cell_width + cell_width / 2, sx * cell_height + cell_height / 2, text=f"{key}0", font=("Arial", 12, "bold"))
            self.canvas.create_text(ey * cell_width + cell_width / 2, ex * cell_height + cell_height / 2, text=f"{key}1", font=("Arial", 12, "bold"))
    
    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        rect = self.cells.get((row, col))
        if rect:
            current_color = self.canvas.itemcget(rect, "fill")
            new_color = 'blue' if current_color == 'white' else 'white'
            self.canvas.itemconfig(rect, fill=new_color)
            
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Interactive Grid")
    grid = InteractiveGrid(root)
    root.mainloop()