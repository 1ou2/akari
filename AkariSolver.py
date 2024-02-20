from AkariPuzzle import AkariPuzzle, Cell

class AkariSolver:
    def __init__(self,puzzle:AkariPuzzle):
        self.non_candle = []
        self.p = puzzle
        self.liberties = {}
        self.progress = 1

    def get_liberties(self,cell:Cell)->int:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Up, down, right, left
        liberties = 4
        # first or last line
        if cell.row == 0 or cell.row == self.p.size_row - 1:
            liberties = liberties - 1
        if cell.col == 0 or cell.col == self.p.size_col - 1:
            liberties = liberties - 1
        
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Up, down, right, left
        for dr, dc in directions:
            new_row, new_col = cell.row + dr, cell.col + dc
            if 0 <= new_row < self.p.size_row and 0 <= new_col < self.p.size_col:
                new_cell = self.p.get_cell(new_row,new_col) 
                if new_cell.is_box() or new_cell.is_candle():
                    liberties = liberties -1
        return liberties
    
    def add_progress(self):
        # internal state, check if we are making progress while solving the puzzle.
        self.progress = self.progress + 1


    def direct_solving(self)->bool:
        """try basic techniques to solve the puzzle """
        lastprogress = 0
        while self.progress > lastprogress:
            lastprogress = self.progress
            for cell in self.p.iter_cells():
                # empty cell
                if cell.is_empty():
                    # this cell has no liberties and is not illuminated
                    # this means that this cell must be a candle
                    #if self.get_liberties(cell) == 0:
                    #    self.p.add_candle(cell)
                    #    self.add_progress()

                    reachable = self.p.get_reachable_cells(cell)
                    # Cell is isolated, it must be a Candle
                    if len(reachable) == 0:
                        self.p.add_candle(cell)
                        self.add_progress()
                    # Only two cells, and one of them is marked as NON-candle
                    elif len(reachable) == 1 and cell.non_candle == True:
                        self.p.add_candle(reachable[0])
                        self.add_progress()
                    else:
                        potential_candle = []
                        for pc in reachable:
                            # search in reachable cells, if there are other empty cells
                            # exclude cells that are marked as non candle.
                            if pc.val == Cell.EMPTY and pc.non_candle == False:
                                potential_candle.append(pc)
                        # no cell in range can be a candle, the only way to light this cell is that it is a candle
                        if len(potential_candle) == 0:
                            self.p.add_candle(cell)
                            self.add_progress()
                        # one candidate, and current cell is marked as a NON candle
                        # it implies the candidate is a candle
                        if len(potential_candle) == 1 and cell.non_candle == True:
                            self.p.add_candle(potential_candle[0])
                            self.add_progress()

                if cell.has_hint():
                    adj = self.p.get_adjacent_cells(cell)
                    # all cells around a 0, are marked as NON candle
                    if cell.val == 0:
                        for c in adj:
                            if c.is_empty() and c.non_candle == False:
                                c.non_candle = True
                                self.add_progress()

                    else:
                        nb_candle = 0
                        nb_empty = 0
                        for c in adj:
                            if c.is_candle():
                                nb_candle = nb_candle + 1
                            if c.is_empty():
                                nb_empty = nb_empty + 1
                        # all empty adjcent cell must be a candle
                        if nb_empty + nb_candle == cell.val:
                            for c in adj:
                                if c.is_empty():
                                    self.p.add_candle(c)
                                    self.add_progress()
        return self.p.is_solved()
    
    def advanced_solving(self):
        pass

    def solve(self):
        easy = self.direct_solving()
        if easy:
            print("EASY")
            return True
        else:
            self.advanced_solving()
          

    

    