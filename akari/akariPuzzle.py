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
        
        # positions where there cannot be a candle
        # list of coordinates e.g. [(1,2),(2,2)]
        self.non_candle = []

    def add_cell(self,r,c,v):
        cell = Cell(r,c,v)
        self.cells[cell.id] = cell

    def set_candle(self,row,col):
        self.cells[Cell.get_id(row,col)].val = Cell.CANDLE

    def get_range(self,row,col):
        """ Returns all cells that are reachable from this cell 
        """
        cell_range = []

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
        when cell is on a border can return less than 4 adjecent cells"""
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







