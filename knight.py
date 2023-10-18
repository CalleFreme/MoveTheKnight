import tkinter as tk
import random

class ChessboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Knight's Movement")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close event

        # Main menu buttons
        menu_button1 = tk.Button(root, text="Version 1", command=lambda: self.start_game(version=1))
        menu_button1.pack()
        menu_button2 = tk.Button(root, text="Version 2", command=lambda: self.start_game(version=2))
        menu_button2.pack()
        menu_button3 = tk.Button(root, text="Version 3", command=lambda: self.start_game(version=3))
        menu_button3.pack()

    def start_game(self, version):
        self.cleanup_game()
        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Knight's Movement Game")

        self.create_chessboard()
        self.knight_position = None
        self.step = 0
        self.version = version
        self.visited_cells = []
        self.starting_points = set()
        self.game_over = False

    def cleanup_game(self):
        if hasattr(self, "game_window"):
            self.game_window.destroy()

    def create_chessboard(self):
        self.chessboard = [[None for _ in range(8)] for _ in range(8)]

        for row in range(8):
            for col in range(8):
                button = tk.Button(self.game_window, text="", width=4, height=2,
                                  command=lambda row=row, col=col: self.on_button_click(row, col))
                button.grid(row=row, column=col)
                self.chessboard[row][col] = button

    def move_knight(self):
        self.step += 1
        valid_moves = self.get_valid_moves(self.knight_position)
        if not valid_moves:
            self.end_game()
            return

        # Randomly select the next move
        next_move = random.choice(valid_moves)
        self.knight_position = next_move
        self.visited_cells.append(next_move)
        self.update_chessboard()
        self.game_window.after(1000, self.move_knight)  # Delay between moves (1 second)

    def on_button_click(self, row, col):
        if self.game_over:
            return

        if self.step == 0:
            # The user selects a starting point, where step=1
            self.step = 1
            self.knight_position = (row, col)
            self.starting_points.add(self.knight_position)
            self.visited_cells.append(self.knight_position)
            self.update_chessboard()
            if self.version == 1:
                self.move_knight()  # Start the knight's automated movement in version 1
            elif self.version == 3:
                if not self.solve_game(self.knight_position):
                    self.starting_points.remove(self.knight_position)
                    self.visited_cells.remove(self.knight_position)
                    self.step = 0
                else:
                    self.chessboard[row][col].config(bg="green")
        elif self.version == 2 and (row, col) in self.get_valid_moves(self.knight_position):
            # The user manually selects the next move in version 2
            self.step += 1
            self.knight_position = (row, col)
            self.visited_cells.append(self.knight_position)
            self.update_chessboard()

    def get_valid_moves(self, position):
        row, col = position
        moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2),
        ]

        return [(r, c) for r, c in moves if 0 <= r < 8 and 0 <= c < 8 and (r, c) not in self.visited_cells]

    def update_chessboard(self):
        for row in range(8):
            for col in range(8):
                if (row, col) in self.visited_cells:
                    self.chessboard[row][col].config(text=str(self.visited_cells.index((row, col)) + 1))
                else:
                    self.chessboard[row][col].config(text="")

    def end_game(self):
        self.game_over = True
        self.game_window.destroy()
        self.root.deiconify()

    def solve_game(self, current_position):
        if self.step == 64:
            return True  # All cells have been visited

        valid_moves = self.get_valid_moves(current_position)
        random.shuffle(valid_moves)

        for move in valid_moves:
            self.step += 1
            self.knight_position = move
            self.visited_cells.append(move)
            self.update_chessboard()

            if self.solve_game(move):
                return True

            # Backtrack if the path is not successful
            self.step -= 1
            self.knight_position = current_position
            self.visited_cells.remove(move)
            self.update_chessboard()

    def on_closing(self):
        if self.version == 1 and self.move_knight_flag:
            return  # Prevent closing while knight is moving in version 1
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessboardApp(root)
    root.mainloop()
