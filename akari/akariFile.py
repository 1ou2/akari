from akari.akariPuzzle import AkariPuzzle
from akari.cell import Cell

class AkariFile:
    def __init__(self, filename):
          self.filename = filename

    def get_puzzle(self):
        with open(self.filename, 'r') as f:
            content = f.read().splitlines()

        # Display the content.
        size_r = len(content)
        size_c = len(content[0])
        puzzle = AkariPuzzle(size_r,size_c)
        for row,line in enumerate(content):
            for col, val in enumerate(line):
                
                if val.isdigit():
                    cell = Cell(row,col,int(val))
                    puzzle.cells[cell.id] = cell
                else:
                    cell = Cell(row,col,val)
                    puzzle.cells[cell.id] = cell

        return puzzle
    
    def write_puzzle(self):
        puzzle = self.get_puzzle()
        with open(self.filename, 'w') as f:
            for row in range(puzzle.size_row):
                for col in range(puzzle.size_col):
                    f.write(puzzle.get_cell(row,col).val)
                f.write("\n")