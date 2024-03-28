puzzle_string = """5-----9--
---521---
---6-72--
-8-----39
--7-6----
42-1--8-5
8----4--1
--9-----8
-3-------"""


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
                            "answered": False,
                        }
                        if number.isnumeric()
                        else {
                            "value": None,
                            "notes": [],
                            "block": ((i // 3) * 3) + ((j // 3) + 1),
                            "answered": False,
                        }
                    )
                    for j, number in enumerate(row)
                ]
            )

    def print_puzzle(self):
        for column in self.puzzle:
            print()
            for c in column:
                color_prefix = "\033[92m" if c["block"] % 2 == 0 else ""
                color_suffix = "\033[00m" if color_prefix else ""

                def wrap_with_background(text):
                    if c["answered"]:
                        return f"\033[40m{text}\033[00m"
                    else:
                        return text

                def wrap_with_color(text):
                    return wrap_with_background(
                        f"{color_prefix}{str(text)}{color_suffix}"
                    )

                print(
                    wrap_with_color(c["value"] if c["value"] else "-"),
                    end=" ",
                )
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
                else:
                    self.puzzle[i][j]["notes"] = []

    def fetch_single_note(self):
        cell_found = False
        for i in range(9):
            for j in range(9):
                current_key = self.puzzle[i][j]["value"]
                if current_key is None:
                    if len(self.puzzle[i][j]["notes"]) == 1:
                        self.input_cell(i, j, self.puzzle[i][j]["notes"][0])
                        cell_found = True
        return cell_found

    def fetch_single_row_column(self):
        cell_found = False
        for i in range(9):
            for j in range(9):
                current_key = self.puzzle[i][j]["value"]
                if current_key is None:
                    for note in self.puzzle[i][j]["notes"]:
                        flag_row = False
                        flag_column = False
                        for x in range(9):
                            if x != j:
                                if note in self.puzzle[i][x]["notes"]:
                                    flag_row = True
                        for x in range(9):
                            if x != i:
                                if note in self.puzzle[x][j]["notes"]:
                                    flag_column = True
                        if flag_row == False or flag_column == False:
                            self.input_cell(i, j, note)
                            cell_found = True
        return cell_found

    def fetch_single_block(self):
        for i in range(9):
            for j in range(9):
                current_key = self.puzzle[i][j]["value"]
                if current_key is None:
                    current_block = self.puzzle[i][j]["block"]
                    for note in self.puzzle[i][j]["notes"]:
                        flag = False
                        for x in range(9):
                            for y in range(9):
                                if i == x and j == y:
                                    pass
                                else:
                                    comp_block = self.puzzle[x][y]["block"]
                                    if comp_block == current_block:
                                        if note in self.puzzle[x][y]["notes"]:
                                            flag = True
                        if flag == False:
                            self.input_cell(i, j, note)

    def input_cell(self, column, row, value):
        self.puzzle[column][row]["value"] = value
        self.puzzle[column][row]["answered"] = True
        self.fetch_all_notes()


sudoku_solver = SudokuSolver(puzzle_string)
sudoku_solver.print_puzzle()
sudoku_solver.fetch_all_notes()
flag = True
while flag:
    flag = False
    if sudoku_solver.fetch_single_note():
        flag = True
        sudoku_solver.print_puzzle()

    if sudoku_solver.fetch_single_row_column():
        flag = True
        sudoku_solver.print_puzzle()

    if sudoku_solver.fetch_single_block():
        flag = True
        sudoku_solver.print_puzzle()


sudoku_solver.print_puzzle()
sudoku_solver.write_puzzle()


"""
TODO:

all element in single row/column in a cell

double combinations

XY Wing elimination
"""
