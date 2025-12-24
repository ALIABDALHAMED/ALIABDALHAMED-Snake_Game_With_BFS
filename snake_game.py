import tkinter as tk
from tkinter import messagebox
import random
from bfs_search import BFSPathfinder

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game with BFS AI")
        self.root.geometry("800x650")
        self.root.resizable(False, False)
        
        self.grid_width = 40
        self.grid_height = 30
        self.cell_size = 20
        
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.food = self._generate_food()
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.ai_path = []
        
        self.pathfinder = BFSPathfinder(self.grid_width, self.grid_height)
        self._setup_ui()
        self.game_speed = 100
        self.move_game()
        
    def _setup_ui(self):
        self.root.config(bg='#000000')
        
        top_frame = tk.Frame(self.root, bg='#000000', height=100)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        title_label = tk.Label(top_frame, text="Snake Game (BFS Algorithm)", 
                               font=('Arial', 18, 'bold'), 
                               bg='#000000', fg="#0089c8")
        title_label.pack(side=tk.LEFT, padx=20)
        
        tk.Label(top_frame, text="Score: ", 
                 font=('Arial', 16, 'bold'), 
                 bg='#000000', fg='#ffff00').pack(side=tk.LEFT)
        
        self.score_label = tk.Label(top_frame, text=f"{self.score}", 
                                    font=('Arial', 16, 'bold'), 
                                    bg='#000000', fg='#00ff00')
        self.score_label.pack(side=tk.LEFT)
        
        self.restart_btn = tk.Button(top_frame, text="🔄 Restart", 
                                     command=self._handle_restart,
                                     font=('Arial', 11, 'bold'),
                                     bg='#ff0000', fg='#ffffff')
        self.restart_btn.pack(side=tk.RIGHT, padx=20)
        
        self.canvas = tk.Canvas(
            self.root,
            width=self.grid_width * self.cell_size,
            height=self.grid_height * self.cell_size,
            bg='#000000',
            highlightthickness=1,
            highlightbackground="#3A3A3A"
        )
        self.canvas.pack(pady=5)
        
    def _reset_game(self):
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.food = self._generate_food()
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.ai_path = []
        self.score_label.config(text=f"{self.score}")
    
    def _handle_restart(self):
        self._reset_game()
        
    def _generate_food(self):
        while True:
            food = (random.randint(0, self.grid_width - 1),
                    random.randint(0, self.grid_height - 1))
            if food not in self.snake:
                return food
    
    def _ai_move(self):
        if not self.ai_path:
            obstacles = set(self.snake)
            self.ai_path = self.pathfinder.find_path(
                self.snake[0], self.food, obstacles
            )
        
        if self.ai_path:
            nx, ny = self.ai_path.pop(0)
            hx, hy = self.snake[0]
            self.next_direction = (nx - hx, ny - hy)
    
    def move_game(self):
        if not self.game_over:
            self._ai_move()
            self.direction = self.next_direction
            
            head_x, head_y = self.snake[0]
            new_x = head_x + self.direction[0]
            new_y = head_y + self.direction[1]
            
            # ✅ WRAP AROUND (التعديل الوحيد)
            new_x = new_x % self.grid_width
            new_y = new_y % self.grid_height
            
            if (new_x, new_y) in self.snake:
                self._end_game()
                return
            
            self.snake.insert(0, (new_x, new_y))
            
            if (new_x, new_y) == self.food:
                self.score += 20
                self.score_label.config(text=f"{self.score}")
                self.food = self._generate_food()
                self.ai_path = []
            else:
                self.snake.pop()
            
            self._draw()
        
        self.root.after(self.game_speed, self.move_game)
    
    def _draw(self):
        self.canvas.delete('all')
        
        for i in range(self.grid_width + 1):
            self.canvas.create_line(
                i * self.cell_size, 0,
                i * self.cell_size, self.grid_height * self.cell_size,
                fill='#333333'
            )
        for i in range(self.grid_height + 1):
            self.canvas.create_line(
                0, i * self.cell_size,
                self.grid_width * self.cell_size, i * self.cell_size,
                fill='#333333'
            )
        
        fx, fy = self.food
        self.canvas.create_rectangle(
            fx * self.cell_size + 1, fy * self.cell_size + 1,
            (fx + 1) * self.cell_size - 1,
            (fy + 1) * self.cell_size - 1,
            fill='#ff0000'
        )
        
        for i, (x, y) in enumerate(self.snake):
            color = "#1d5b1d" if i == 0 else "#00aa00"
            self.canvas.create_rectangle(
                x * self.cell_size + 1, y * self.cell_size + 1,
                (x + 1) * self.cell_size - 1,
                (y + 1) * self.cell_size - 1,
                fill=color
            )
    
    def _end_game(self):
        self.game_over = True
        messagebox.showinfo(
            "🎮 Game Over!",
            f"🐍 Final Score: {self.score}\n\nClick Restart to play again!"
        )

def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
