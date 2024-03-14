puzzle_string = """----617--
-51--78--
----2---4
-1------8
82--19---
--98---72
--59-263-
---73---5
-63--428-"""


class SudokuSolver:
    puzzle = []

    def __init__(self, puzzle_string):
        puzzle_string = puzzle_string.replace("-", " ")
        puzzle_string = puzzle_string.split("\n")
        for i, row in enumerate(puzzle_string):
            self.puzzle.append(
                [
                    (
                        {
                            "value": number,
                            "notes": [],
                            "block": ((i // 3) * 3) + ((j // 3) + 1),
                        }
                        if number.isnumeric()
                        else {
                            "value": None,
                            "notes": [],
                            "block": ((i // 3) * 3) + ((j // 3) + 1),
                        }
                    )
                    for j, number in enumerate(row)
                ]
            )

    def print_puzzle(self):
        for column in self.puzzle:
            print()
            for c in column:
                if c["value"] != None:
                    if c["block"] % 2 == 0:
                        print(f'\033[92m{c["value"]}\033[00m', end=" ")
                    else:
                        print(c["value"], end=" ")
                else:
                    if c["block"] % 2 == 0:
                        print("\033[92m-\033[00m", end=" ")
                    else:
                        print("-", end=" ")
        print()

    def write_puzzle(self):
        with open("output.py", "w") as output_file:
            output_file.write(str(self.puzzle))

    def fetch_cell_notes(self, column, row):
        cell_block = ((column // 3) * 3) + ((row // 3) + 1)
        master_list = [str(i) for i in range(1, 10)]
        for i in range(9):
            current_key = self.puzzle[column][i]["value"]
            if current_key is not None and current_key in master_list:
                master_list.remove(current_key)
        for i in range(9):
            current_key = self.puzzle[i][row]["value"]
            if current_key is not None and current_key in master_list:
                master_list.remove(current_key)

        for i in range(9):
            for j in range(9):
                current_key = self.puzzle[i][j]["value"]
                current_key_block = ((i // 3) * 3) + ((j // 3) + 1)
                if (
                    current_key_block == cell_block
                    and current_key is not None
                    and current_key in master_list
                ):
                    master_list.remove(current_key)

        return master_list

    def fetch_all_notes(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j]["value"] is None:
                    self.puzzle[i][j]["notes"] = self.fetch_cell_notes(i, j)

    def fetch_singles(self):
        single_found = False
        for i in range(9):
            for j in range(9):
                current_key = self.puzzle[i][j]["value"]
                if current_key is None:
                    if len(self.puzzle[i][j]["notes"]) == 1:
                        self.input_cell(i, j, self.puzzle[i][j]["notes"][0])
                        single_found = True
        return single_found

    def input_cell(self, column, row, value):
        self.puzzle[column][row]["value"] = value
        self.fetch_all_notes()


sudoku_solver = SudokuSolver(puzzle_string)
sudoku_solver.print_puzzle()
sudoku_solver.fetch_all_notes()
while sudoku_solver.fetch_singles():
    sudoku_solver.print_puzzle()
sudoku_solver.write_puzzle()
