class Cell:
    EMPTY = "."
    CANDLE = "C"
    BOX = "X"
    ILLUMINATED = "*"

    def get_id(row,col):
        return str(row) + "x" + str(col)
    
    def __init__(self, row,col,val=EMPTY):
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
    
    def set_non_candle(self):
        self.non_candle = True