from akari.cell import Cell

class AkariPuzzle:
    def __init__(self, size_row,size_col):
        """ Creates an empty Akari puzzle 
        size_row : number of rows
        size_col : number of columns """
        self.size_row = size_row
        self.size_col = size_col
        # internal representation of a board
        # empty cells are represented by a "."
        
        self.cells = {}
        for r in range(self.size_row):
            for c in range(self.size_col):
                cell = Cell(r,c,Cell.EMPTY)
                self.cells[cell.id] =  cell

    def add_cell(self,r,c,v):
        cell = Cell(r,c,v)
        self.cells[cell.id] = cell

    def set_candle(self,row,col):
        if self.cells[Cell.get_id(row, col)].non_candle == True:
            raise ValueError("set_candle: Cell is non candle") 
        self.cells[Cell.get_id(row,col)].val = Cell.CANDLE
    
    def add_non_candle(self,cell:Cell)->bool:
        if cell.is_empty() and cell.non_candle == False:
            cell.non_candle = True
            return True
        else:
            raise ValueError("add_non_candle: Cell is not empty or already non candle")
        

    # return a copy of the current state of the puzzle
    def copy(self):
        puzzle = AkariPuzzle(self.size_row, self.size_col)
        for cell in self.cells.values():
            puzzle.add_cell(cell.row, cell.col, cell.val)
        return puzzle

    def get_reachable_cells(self,cell:Cell)->list[Cell]:
        """ Return a list of all reachable cells, from a given cell
         search cells in all directions : Up, down, right, left """
        reachable = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Up, down, right, left
        for dr, dc in directions:
            new_row, new_col = cell.row, cell.col
            while True:
                new_row, new_col = new_row + dr, new_col + dc
                # check coordinates are inside the board
                if 0 <= new_row < self.size_row and 0 <= new_col < self.size_col:
                    new_cell = self.get_cell(new_row,new_col)
                    #
                    if new_cell.val == Cell.EMPTY or new_cell.val == Cell.ILLUMINATED:
                        reachable.append(new_cell)
                    # a candle, a box, or a box with hint found
                    # stop iterating in this direction
                    else:
                        break
                else:
                    break
        return reachable  

    def get_adjacent_cells(self,cell:Cell)->list[Cell]:
        """ Return a list of all adjacents cells, from a cell Up, down, right, left 
        when cell is on a border can return less than 4 adjacent cells"""
        adj = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Up, down, right, left
        for dr, dc in directions:
            new_row, new_col = cell.row + dr, cell.col + dc
            if 0 <= new_row < self.size_row and 0 <= new_col < self.size_col:
                adj.append(self.get_cell(new_row,new_col))
        return adj  
    

    def iter_cells(self)->list[Cell]:
        return list(self.cells.values())

    def get_cell(self,row,col)->Cell:
        return self.cells[Cell.get_id(row,col)]
    
    def get_left_cell(self, cell:Cell)->Cell:
        """ Return the cell to the left of the given cell """
        if cell.col == 0:
            return None  # leftmost column, no cell to the left
        return self.get_cell(cell.row, cell.col - 1)
    
    def get_right_cell(self, cell:Cell)->Cell:
        """ Return the cell to the right of the given cell """
        if cell.col == self.size_col - 1:
            return None  # rightmost column, no cell to the right
        return self.get_cell(cell.row, cell.col + 1)

    def get_top_cell(self, cell:Cell)->Cell:
        """ Return the cell above the given cell """
        if cell.row == 0:
            return None  # topmost row, no cell above
        return self.get_cell(cell.row - 1, cell.col)
    
    def get_bottom_cell(self, cell:Cell)->Cell:
        """ Return the cell below the given cell """
        if cell.row == self.size_row - 1:
            return None  # bottommost row, no cell below
        return self.get_cell(cell.row + 1, cell.col)
    
    def get_right_top_cell(self, cell:Cell)->Cell:
        """ Return the cell to the right and above the given cell """
        if cell.row == 0 or cell.col == self.size_col - 1:
            return None  # topmost or rightmost row, no cell to the right or above
        return self.get_cell(cell.row - 1, cell.col + 1)
    
    def get_right_bottom_cell(self, cell:Cell)->Cell:
        """ Return the cell to the right and below the given cell """
        if cell.row == self.size_row - 1 or cell.col == self.size_col - 1:
            return None  # bottommost or rightmost row, no cell to the right or below
        return self.get_cell(cell.row + 1, cell.col + 1)
    
    def get_left_top_cell(self, cell:Cell)->Cell:
        """ Return the cell to the left and above the given cell """
        if cell.row == 0 or cell.col == 0:
            return None  # topmost or leftmost row, no cell to the left or above
        return self.get_cell(cell.row - 1, cell.col - 1)
    
    def get_left_bottom_cell(self, cell:Cell)->Cell:
        """ Return the cell to the left and below the given cell """
        if cell.row == self.size_row - 1 or cell.col == 0:
            return None  # bottommost or leftmost row, no cell to the left or below
        return self.get_cell(cell.row + 1, cell.col - 1)

    def is_box(self,row,col):
        """ Returns true if the cell at coordinates row/col is a box """
        if self.get_cell(row, col).is_box():
            return True
       
        return False
    
    def is_candle(self,row,col):
        if self.get_cell(row, col).is_candle():
            return True
        
        return False
    
    def is_solved(self):
        """Return true if the puzzle is solved"""
                
        for cell in self.cells.values():
            if cell.val == Cell.EMPTY:
                return False
        return True
    
    def illuminate(self,cell:Cell):
        if cell.is_box():
            raise ValueError("Cannot illuminate a box")
        if cell.is_candle():
            raise ValueError("Cannot illuminate a candle")
        
        self.cells[cell.id].val = Cell.ILLUMINATED

        
    def add_candle(self, cell:Cell):
        """ Add a candle, and illuminate all reachable cells"""
        row = cell.row
        col = cell.col
        if self.is_box(row,col):
            raise ValueError("Cannot place candle on a box")
        
        illuminated = self.get_reachable_cells(cell)
        
        for illuminated_cell in illuminated:
            self.illuminate(illuminated_cell)

        self.set_candle(row,col)

    def add_box(self, row, col, label=None):
        # box without a label
        if label is None:
            self.get_cell(row, col).val = Cell.BOX
            
        else:
            if not isinstance(label, int) or label < 0:
                raise ValueError("Label must be a positive integer")
            elif row >= self.size_row or col >= self.size_col:
                raise ValueError("Row and column indices out of range")
            
            self.get_cell(row, col).val = label
            
    # check puzzle state. There must be no candles that are facing each other
    def check_puzzle(self):
        # dict associating a row with a list of candles in that row
        candles_by_row = {}
        # dict associating a column with a list of candles in that column
        candles_by_col = {}
        for cell in self.cells.values():
            if cell.val == Cell.CANDLE:
                row = cell.row
                col = cell.col
                if row not in candles_by_row:
                    candles_by_row[row] = []
                    # add the candle to the list of candles in the row
                    candles_by_row[row].append(cell)
                else:
                    # add the candle to the list of candles in the row
                    candles_by_row[row].append(cell)
                if col not in candles_by_col:
                    candles_by_col[col] = []
                    # add the candle to the list of candles in the column
                    candles_by_col[col].append(cell)
                else:
                    candles_by_col[col].append(cell)
        
        # check candles in each row
        for row in candles_by_row:
            cols = sorted([c.col for c in candles_by_row[row]])
            # for each pair of candles in the row, check if there are only empty or illuminated cells between them
            for col1, col2 in zip(cols, cols[1:]):
                # check that col1 and col2 are not adjacent
                if col1 + 1 == col2:
                    return False
                for col in range(col1 + 1, col2):
                    cell = self.get_cell(row, col)
                    # it means that two candles are facing each other, so the puzzle is not solvable
                    if cell.val != Cell.EMPTY and cell.val != Cell.ILLUMINATED:
                        return False
        
        # check candles in each column
        for col in candles_by_col:
            rows = sorted([c.row for c in candles_by_col[col]])
            # for each pair of candles in the column, check if there are only empty or illuminated cells between them
            for row1, row2 in zip(rows, rows[1:]):
                # check that row1 and row2 are not adjacent
                if row1 + 1 == row2:
                    return False
                for row in range(row1 + 1, row2):
                    cell = self.get_cell(row, col)
                    # it means that two candles are facing each other, so the puzzle is not solvable
                    if cell.val != Cell.EMPTY and cell.val != Cell.ILLUMINATED:
                        return False
        
        return True

    def print(self):
        print()
        # offset for line numbering
        col_offset = '  '
        print(col_offset,end=' ')
        # print column number
        for c in range(self.size_col):
            print(c,end=' ')
        print()
        print(col_offset,end=' ')
        for c in range(self.size_col):
            print('--',end='')
        print()
        for row in range(self.size_row):
            print(str(row) + '| ',end='')
            for col in range(self.size_col):
                print(self.get_cell(row, col).val,end=' ')       
            print()







