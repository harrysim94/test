import numpy as np
import matplotlib.pyplot as plt

import random
import tkinter as tk

class GridWorld:
    def __init__(self, rows, cols, levels, pairs):
        self.rows = rows
        self.cols = cols
        self.levels = levels
        self.grid = np.zeros((levels, rows, cols))  # Initialize multi-level grid
        self.paths = {key: np.zeros((levels, rows, cols)) for key in pairs}  # Store paths per key
        self.pairs = pairs  # Dictionary of keys mapping to (start, end) pairs
        self.state_size = (levels, rows, cols)
        self.action_size = 6  # Up, Down, Left, Right, Level Up, Level Down
        
        # Set goals for all pairs
        for key in self.pairs:
            self.set_goal(key)
    
    def reset(self):
        """Resets the grid to its initial state and returns an initial state."""
        self.grid = np.zeros((self.levels, self.rows, self.cols))
        self.paths = {key: np.zeros((self.levels, self.rows, self.cols)) for key in self.pairs}
        return self.grid
    
    def set_goal(self, key):
        """Sets a pair of points that must be connected using a key."""
        if key in self.pairs:
            start, end = self.pairs[key]
            if all(0 <= coord[0] < self.rows and 0 <= coord[1] < self.cols for coord in [start, end]):
                self.grid[0, start[0], start[1]] = 1  # Mark start point
                self.grid[0, end[0], end[1]] = 1  # Mark end point
    
    def add_path_segment(self, key, level, position):
        """Adds a path segment for a specific key at a given level and position."""
        if key in self.pairs and 0 <= level < self.levels and 0 <= position[0] < self.rows and 0 <= position[1] < self.cols:
            self.paths[key][level, position[0], position[1]] = 1
    
    def calculate_total_distance(self):
        """Calculates the total distance used by each path separately and returns a dictionary."""
        return {key: np.sum(path) for key, path in self.paths.items()}
    
    def render(self):
        """Displays the grid and paths using matplotlib with semi-translucent colors and labeled goals."""
        base_img = np.ones((self.rows, self.cols, 4))  # White background with alpha channel
        color_map = [
            (1, 0, 0, 0.3),  # Red for level 0 (semi-translucent)
            (0, 1, 0, 0.3),  # Green for level 1
            (0, 0, 1, 0.3),  # Blue for level 2
            (1, 1, 0, 0.3),  # Yellow for level 3
            (1, 0, 1, 0.3)   # Magenta for level 4
        ]
        for key, path in self.paths.items():
            for level in range(self.levels):
                mask = path[level] > 0
                for c in range(3):  # RGB channels only
                    base_img[..., c] = np.where(mask, (base_img[..., c] * (1 - color_map[level][3]) + color_map[level][c] * color_map[level][3]), base_img[..., c])
        
        plt.imshow(base_img, origin='upper')
        plt.xticks(range(self.cols))
        plt.yticks(range(self.rows))
        plt.grid(True)
        
        # Add goal labels
        for key, (start, end) in self.pairs.items():
            plt.text(start[1], start[0], f'{key}0', color='black', fontsize=12, ha='center', va='center', fontweight='bold')
            plt.text(end[1], end[0], f'{key}1', color='black', fontsize=12, ha='center', va='center', fontweight='bold')
        
        plt.show()

    
class GridGame:
    def __init__(self, rows=10, cols=10, levels=3):
        self.rows = rows
        self.cols = cols
        self.levels = levels
        self.pairs = {"A": ((random.randint(0, rows-1), random.randint(0, cols-1)),
                              (random.randint(0, rows-1), random.randint(0, cols-1))),
                      "B": ((random.randint(0, rows-1), random.randint(0, cols-1)),
                              (random.randint(0, rows-1), random.randint(0, cols-1)))}
        self.grid_world = GridWorld(rows, cols, levels, self.pairs)
        self.current_pair = None
        self.root = tk.Tk()
        self.cell_size=40
        self.canvas = tk.Canvas(self.root, width=cols*self.cell_size, height=rows*self.cell_size, bg='white')
        self.canvas.pack()
        self.cells = {} # Store cell rectangles
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.on_click)
        self.start_game()
    
    def draw_grid(self):
        self.canvas.delete("all")
        cell_width = 500 / self.cols
        cell_height = 500 / self.rows
        for i in range(self.rows):
            for j in range(self.cols):
                x0, y0 = j * cell_width, i * cell_height
                x1, y1 = x0 + cell_width, y0 + cell_height
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")
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
    
    def start_game(self):
        for key in self.pairs:
            self.current_pair = key
            print(f"Draw the path for {key}. Enter 'y' when done.")
            input()
        
        total_distance = self.grid_world.calculate_total_distance()
        print("Path distances:")
        for key, distance in total_distance.items():
            print(f"{key}: {distance}")
        print(f"Final Score: {sum(total_distance.values())}")
        self.root.quit()
    
    def run(self):
        self.root.mainloop()
        

if __name__ == "__main__":
    game = GridGame()
    game.run()
    

    
# # Example usage
# if __name__ == "__main__":
#     grid = GridWorld(10, 10, 3, {'A': ((0,0), (4,4)),  'B': ((2,7), (4,0))})   
#     grid.add_path_segment('A', 0, (0, 1))
#     grid.add_path_segment('A', 0, (0, 2))
#     grid.add_path_segment('A', 0, (1, 2))
#     grid.add_path_segment('A', 1, (1, 2))
#     grid.add_path_segment('A', 1, (1, 3))
#     grid.add_path_segment('A', 1, (1, 4))
#     grid.render()
#     print("Total Path Distances:", grid.calculate_total_distance())
    