import customtkinter as ctk
import tkinter.messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class SudokuGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Solver")
        self.geometry("520x600")
        self.resizable(False, False)

        self.entries = [[None for _ in range(9)] for _ in range(9)]

        title = ctk.CTkLabel(self, text="Sudoku Solver", font=("Arial", 24, "bold"))
        title.pack(pady=10)

        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack()

        self.create_grid()

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=20)

        solve_button = ctk.CTkButton(self.button_frame, text="Solve", command=self.solve_gui)
        solve_button.grid(row=0, column=0, padx=10)

        clear_button = ctk.CTkButton(self.button_frame, text="Clear", command=self.clear_grid)
        clear_button.grid(row=0, column=1, padx=10)

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                entry = ctk.CTkEntry(self.grid_frame, width=40, height=40, font=("Arial", 16), justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry

    def read_grid(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                if val == "":
                    row.append(0)
                else:
                    try:
                        num = int(val)
                        if 1 <= num <= 9:
                            row.append(num)
                        else:
                            raise ValueError
                    except ValueError:
                        tkinter.messagebox.showerror("Invalid Input", f"Invalid number at row {i+1}, column {j+1}")
                        return None
            grid.append(row)
        return grid

    def display_grid(self, grid):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, "end")
                self.entries[i][j].insert(0, str(grid[i][j]))

    def solve_gui(self):
        grid = self.read_grid()
        if grid is not None:
            if solve(grid):
                self.display_grid(grid)
            else:
                tkinter.messagebox.showinfo("No Solution", "This Sudoku puzzle has no solution.")

    def clear_grid(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, "end")


# === Sudoku Solver Logic ===

def is_valid(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

def solve(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True


if __name__ == "__main__":
    app = SudokuGUI()
    app.mainloop()
