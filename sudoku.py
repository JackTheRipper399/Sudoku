import tkinter as tk
from tkinter import messagebox


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.configure(bg="black")  # Add this line

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()

        # Buttons
        solve_button = tk.Button(root, text="Solve", command=self.solve)
        solve_button.grid(row=10, column=0, columnspan=4, sticky="nsew")

        clear_button = tk.Button(root, text="Clear", command=self.clear_grid)
        clear_button.grid(row=10, column=5, columnspan=4, sticky="nsew")

    def create_grid(self):
        for row in range(9):
            for col in range(9):
                # Determine border thickness for 3x3 grid lines
                top = 3 if row % 3 == 0 and row != 0 else 1
                left = 3 if col % 3 == 0 and col != 0 else 1
                # Use sticky to fill the cell
                frame = tk.Frame(
                    self.root,
                    highlightbackground="black",
                    highlightcolor="black",
                    highlightthickness=0,
                    bd=0
                )
                frame.grid(
                    row=row,
                    column=col,
                    padx=(left, 0),
                    pady=(top, 0)
                )
                entry = tk.Entry(frame, width=3, font=(
                    "Arial", 18), justify="center", bd=0)
                entry.pack(ipady=5)
                self.entries[row][col] = entry

    def get_grid(self):
        grid = []
        for row in range(9):
            current_row = []
            for col in range(9):
                val = self.entries[row][col].get()
                if val.isdigit():
                    current_row.append(int(val))
                else:
                    current_row.append(0)
            grid.append(current_row)
        return grid

    def set_grid(self, grid):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                if grid[row][col] != 0:
                    self.entries[row][col].insert(0, str(grid[row][col]))

    def clear_grid(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)

    def is_valid(self, grid, row, col, num):
        # Check row
        if num in grid[row]:
            return False
        # Check column
        if num in [grid[r][col] for r in range(9)]:
            return False
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if grid[r][c] == num:
                    return False
        return True

    def solve_sudoku(self, grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if self.solve_sudoku(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True

    def solve(self):
        grid = self.get_grid()
        if self.solve_sudoku(grid):
            self.set_grid(grid)
        else:
            messagebox.showwarning(
                "Unsolvable", "This puzzle cannot be solved. Please check your input.")


if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
