from akari.akariPuzzle import AkariPuzzle
from akari.cell import Cell

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
        lastprogress = 0
        # store all cells related to a hint
        # cells_hints[cell.id] = [cell1, cell2, cell3]
        # cell1, cell2, cell3 are the cells around the hint cell.
        #
        # cell_hint { "id": cell.id, "cell": cell,"adjacents": [cell1, cell2, cell3],  "value": cell.val, "is_solved": False, "candles": [cell1, cell2, cell3],"candidates":[cell1,cell3]}
        #
        # hints = { cell.id : cell_hint }
        #
        hints = {}
        for cell in self.p.iter_cells():
            if cell.has_hint():
                cell_hint = {}
                cell_hint["id"] = cell.id
                cell_hint["cell"] = cell
                cell_hint["adjacents"] = self.p.get_adjacent_cells(cell)
                cell_hint["value"] = cell.val
                cell_hint["is_solved"] = False
                cell_hint["candles"] = []
                cell_hint["candidates"] = []
                for c in cell_hint["adjacents"]:
                    if c.is_candle():
                        cell_hint["candles"].append(c)
                    if c.is_empty():
                        cell_hint["candidates"].append(c)
                if len(cell_hint["candles"]) == cell_hint["value"]:
                    cell_hint["is_solved"] = True
                hints[cell.id] = cell_hint
                
        while self.progress > lastprogress:
            lastprogress = self.progress
            for hint in hints.values():
                # For each hint that is not solved, and that has at least 2 missing candles around it
                # Select, 2 adjacents cells as candidates for being a candle
                # check if another hint cannot be solved with these candles
                # if not, we know that this pair of candles is not possible
                if hint["is_solved"] == False and len(hint["candidates"]) == 3:
                    inconsistency = False
                    for c1 in hint["candidates"]:
                        for c2 in hint["candidates"]:
                            if c1 != c2:
                                # here are the cells that would be reachable by the 2 candidates
                                reachable1 = self.p.get_reachable_cells(c1)
                                reachable2 = self.p.get_reachable_cells(c2)

                                # merge the two list
                                reachable = reachable1 + reachable2
                                # remove duplicates
                                reachable = list(set(reachable))

                                # check if there is another hint that cannot be solved because of these candles
                                # to do so, check if all adjcent cells of the hint are in the list of reachable cells
                                
                                for h in hints.values():
                                    if h["is_solved"] == False and h["id"] != hint["id"]:
                                        solvable = False
                                        for c in h["adjacents"]:
                                            if c not in reachable:
                                                # this hint cannot be solved because of these candles
                                                # we can stop here
                                                solvable = True
                                                break
                                        if solvable == False:
                                            inconsistency = True
                                            break
                            

                                # We found an inconsistency, it means that both c1 and c2 cannot be candles
                                # As we have 3 candidates, we can deduce that the third candidate is a candle
                                if inconsistency == True:
                                    for c3 in hint["candidates"]:
                                        if c3 != c1 and c3 != c2:
                                            self.p.add_candle(c3)
                                            self.add_progress()
                                            break
                                    break
                        if inconsistency == True:
                            break
                        
                                    

                                    

                                


    def solve(self):
        easy = self.direct_solving()
        if easy:
            print("EASY")
            return True
        else:
            self.advanced_solving()
          

    

    