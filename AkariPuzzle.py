class Cell:
    EMPTY = "."
    CANDLE = "C"
    BOX = "X"
    ILLUMINATED = "*"

    def get_id(row,col):
        return str(row) + "x" + str(col)
    
    def __init__(self, row,col,val):
        """ Creates an empty Akari puzzle 
        size_row : number of rows
        size_col : number of columns """
        self.row = row
        self.col = col
        self.val = val
        self.id = Cell.get_id(row,col)
        # True, if we know for sure that this cell cannot be a candle
        self.non_candle = False

    def is_empty(self):
        return self.val == Cell.EMPTY
    
    def is_candle(self):
        return self.val == Cell.CANDLE
    
    def is_illuminated(self):
        return self.val == Cell.ILLUMINATED
    
    def is_box(self):
        return self.val == "X" or isinstance(self.val,int)
    
    def has_hint(self):
        return isinstance(self.val,int)
    
    

class AkariPuzzle:
    def __init__(self, size_row,size_col):
        """ Creates an empty Akari puzzle 
        size_row : number of rows
        size_col : number of columns """
        self.size_row = size_row
        self.size_col = size_col
        # internal representation of a board
        # empty cells are represented by a "."
        self.board = [['.' for _ in range(size_col)] for _ in range(size_row)]
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
        self.board[row][col] = "C"
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
        if self.board[row][col] == "X" or isinstance(self.board[row][col],int):
            return True
        return False
    
    def is_candle(self,row,col):
        if self.board[row][col] == "C":
            return True
        return False
    
    def is_solved(self):
        """Return true if the puzzle is solved"""
                
        for cell in self.cells.values():
            if cell.val == Cell.EMPTY:
                return False
        return True
    
    def illuminate(self,row,col):
        if self.is_box(row,col):
            raise ValueError("Cannot illuminate a box")
        if self.is_candle(row,col):
            raise ValueError("Cannot illuminate a candle")
        
        self.board[row][col] = '*'
        self.cells[Cell.get_id(row,col)].val = Cell.ILLUMINATED

        
    def add_candle(self, cell:Cell):
        row = cell.row
        col = cell.col
        if self.is_box(row,col):
            raise ValueError("Cannot place candle on a box")
        
        illumintated = []
        # illuminate right
        c = col + 1
        while c <= self.size_col -1:
            if self.board[row][c] == "C":
                raise ValueError("A candle cannot illuminate another candle")
            # found a box, cannot illumate cells after that point
            if self.is_box(row,c):
                break
            illumintated.append((row,c))
            c = c + 1
        # illuminate left
        c = col - 1
        while c >= 0:
            if self.board[row][c] == "C":
                raise ValueError("A candle cannot illuminate another candle")
            # found a box, cannot illumate cells after that point
            if self.is_box(row,c):
                break
            illumintated.append((row,c))
            c = c - 1
        # illuminate top
        r = row - 1
        while r >= 0:
            if self.board[r][col] == "C":
                raise ValueError("A candle cannot illuminate another candle")
            # found a box, cannot illumate cells after that point
            if self.is_box(r,col):
                break
            illumintated.append((r,col))
            r = r - 1

         # illuminate bottom
        r = row + 1
        while r <= self.size_row -1:
            if self.board[r][col] == "C":
                raise ValueError("A candle cannot illuminate another candle")
            # found a box, cannot illumate cells after that point
            if self.is_box(r,col):
                break
            illumintated.append((r,col))
            r = r + 1
        
        for (r,c) in illumintated:
            self.illuminate(r,c)

        self.set_candle(row,col)

    def add_box(self, row, col, label=None):
        # box without a label
        if label is None:
            self.board[row][col] = "X"
            
        else:
            if not isinstance(label, int) or label < 0:
                raise ValueError("Label must be a positive integer")
            elif row >= self.size_row or col >= self.size_col:
                raise ValueError("Row and column indices out of range")
            
            self.board[row][col] = label
            

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
                print(self.board[row][col],end=' ')       
            print()

    def solve(self):
        # check cells that 
        for row in range(self.size_row):
            for col in range(self.size_col):
                self.board[row][col]






