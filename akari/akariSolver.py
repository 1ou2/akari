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

    # store all details related to a hint
    #
    # cell_hint { "id": cell.id, "cell": cell,
    #    "adjacents": [cell1, cell2, cell3],  "value": cell.val, "is_solved": False, 
    #    "candles": [cell1, cell2, cell3],"candidates":[cell1,cell3]}
    #
    #
    def get_cell_details(self, cell:Cell):
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
            if c.is_empty() and c.non_candle == False:
                cell_hint["candidates"].append(c)
        if len(cell_hint["candles"]) == cell_hint["value"]:
            cell_hint["is_solved"] = True
        else:
            cell_hint["is_solved"] = False
        return cell_hint

    # set non candle marks
    # returns True if a change was made and a cell has been marked as NOT being a candle
    def rule_non_candle(self)->bool:
        has_changed = False
        for cell in self.p.iter_cells():
            if not cell.has_hint():
                continue
            cell_hint = self.get_cell_details(cell)
            if cell_hint["is_solved"]:
                for c in cell_hint["adjacents"]:
                    if c.is_empty() and c.non_candle == False:
                        c.set_non_candle()
                        has_changed = True

            # cells with value 3 or 4 cannot have a candle in all diagonal cells around them
            if cell.val ==4 or cell.val == 3:
                # left-up, lef-bottom, right-up, right-bottom
                directions = [(-1,-1),(-1, 1),(1, -1),(1, 1)]
                for dr, dc in directions:
                    new_row, new_col = cell.row + dr, cell.col + dc
                    if 0 <= new_row < self.p.size_row and 0 <= new_col < self.p.size_col:
                        new_cell = self.p.get_cell(new_row, new_col)
                        if new_cell.is_empty() and new_cell.non_candle == False:
                            new_cell.set_non_candle()
                            has_changed = True
                
            # cells with value 2, and with an adjacent cell blocked, cannot have a candle in the opposite diagonal
            if cell.val == 2:
                if len(cell_hint["candles"]) == 0 and len(cell_hint["candidates"]) == 3:
                    left_cell = self.p.get_left_cell(cell)
                    right_cell = self.p.get_right_cell(cell)
                    up_cell = self.p.get_top_cell(cell)
                    bottom_cell = self.p.get_bottom_cell(cell)
                    # if left cell is not a candidate then right-top, and right-bottom cells cannot be a candle
                    if left_cell and left_cell not in cell_hint["candidates"]:
                        right_top = self.p.get_right_top_cell(cell)
                        right_bottom = self.p.get_right_bottom_cell(cell)
                        if right_top and right_top.non_candle == False:
                            right_top.set_non_candle()
                            has_changed = True
                        if right_bottom and right_bottom.non_candle == False:
                            right_bottom.set_non_candle()
                            has_changed = True
                    # if right cell is not a candidate then left-top, and left-bottom cells cannot be a candle
                    if right_cell and right_cell not in cell_hint["candidates"]:
                        left_top = self.p.get_left_top_cell(cell)
                        left_bottom = self.p.get_left_bottom_cell(cell)
                        if left_top and left_top.non_candle == False:
                            left_top.set_non_candle()
                            has_changed = True
                        if left_bottom and left_bottom.non_candle == False:
                            left_bottom.set_non_candle()
                            has_changed = True    
                    # if up cell is not a candidate then left-bottom, and right-bottom cells cannot be a candle
                    if up_cell and up_cell not in cell_hint["candidates"]:
                        left_bottom = self.p.get_left_bottom_cell(cell)
                        right_bottom = self.p.get_right_bottom_cell(cell)
                        if left_bottom and left_bottom.non_candle == False:
                            left_bottom.set_non_candle()
                            has_changed = True
                        if right_bottom and right_bottom.non_candle == False:
                            right_bottom.set_non_candle()
                            has_changed = True
                    # if bottom cell is not a candidate then left-top, and right-top cells cannot be a candle
                    if bottom_cell and bottom_cell not in cell_hint["candidates"]:
                        left_top = self.p.get_left_top_cell(cell)
                        right_top = self.p.get_right_top_cell(cell)
                        if left_top and left_top.non_candle == False:
                            left_top.set_non_candle()
                            has_changed = True
                        if right_top and right_top.non_candle == False:
                            right_top.set_non_candle()
                            has_changed = True
        
        
            # cells with value 1, and with an adjacent cell blocked, cannot have a candle in the opposite diagonal
            if cell.val == 1 and len(cell_hint["candidates"]) == 2:
                # check that candidates are not in the row and not in the same column
                non_candle_row = []
                non_candle_col = []
                for candidate in cell_hint["candidates"]:
                    if candidate.row == cell.row:
                        non_candle_col.append(candidate.col)
                    # check if candidate is in the same column
                    if candidate.col == cell.col:
                        non_candle_row.append(candidate.row)

                if len(non_candle_row) == 1 and len(non_candle_col) == 1:
                    diag_cell = self.p.get_cell(non_candle_row[0], non_candle_col[0])
                    if diag_cell.non_candle == False:
                        diag_cell.set_non_candle()
                        has_changed = True
                           
        return has_changed
        
                                    

    def rule_only_choice(self)->bool:
        """
        check if there is only one possible value for each cell
        """
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
                    return True
                # Only two cells, and one of them is marked as NON-candle
                elif len(reachable) == 1 and cell.non_candle == True:
                    self.p.add_candle(reachable[0])
                    return True
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
                        return
                    # one candidate, and current cell is marked as a NON candle
                    # it implies the candidate is a candle
                    if len(potential_candle) == 1 and cell.non_candle == True:
                        self.p.add_candle(potential_candle[0])
                        return True
        return False
    
    def rule_restricted_hint(self)->bool:
        for cell in self.p.iter_cells():
            if cell.has_hint():
                adj = self.p.get_adjacent_cells(cell)
                # all cells around a 0, are marked as NON candle
                if cell.val == 0:
                    has_changed = False
                    for c in adj:
                        if c.is_empty() and c.non_candle == False:
                            c.non_candle = True
                            has_changed = True
                    if has_changed:
                        return True

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
                                return True
        return False
    

    
    def double_check(self):
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
                cell_hint = self.get_cell_details(cell)
                hints[cell.id] = cell_hint

        for hint in hints.values():
            # For each hint that is not solved, and that has at least 2 missing candles around it
            # Select, 2 adjacents cells as candidates for being a candle
            # check if another hint cannot be solved with these candles
            # if not, we know that this pair of candles is not possible
            if hint["is_solved"] == False and len(hint["candidates"]) == 3 and hint["value"] >1:
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
                                    for c in h["candidates"]:
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
                                        return True
                                break
                    if inconsistency == True:
                        break
    
        return False
    
    def direct_solving(self)->bool:
        """try basic techniques to solve the puzzle """
        lastprogress = 0
        while self.progress > lastprogress:
            lastprogress = self.progress
            if self.rule_only_choice():
                self.add_progress()
            if self.rule_restricted_hint():
                self.add_progress()
            if self.p.is_solved():
                return True         
        return False
    
    # try solving, by using a chain. Try placing a candle, check if it triggers the placement other candles, until no other 
    # candles can be placed. Check if this can be a valid board.
    def rule_chain(self):
        # copy state in order to be able to restore, if this hypothesis is wrong
        saved_puzzle= self.p.copy()

        # we try to place a candle, and check if it triggers the placement of other candles
        # if a ValueError is raised, it means that this hypothesis is wrong, and we restore the state
        try:
            for cell in self.p.iter_cells():
                if cell.is_empty():
                    self.p.add_candle(cell)
                    if not self.p.check_puzzle():
                        raise ValueError
        
        # we can eliminate this cell, it cannot be a candle
        except ValueError:
            self.p = saved_puzzle
            return False
        

        self.p = saved_puzzle                
        return True

    def advanced_solving(self)->bool:
        lastprogress = 0
        while self.progress > lastprogress:
            print(".",end="")
            lastprogress = self.progress
            if self.double_check():
                self.add_progress()
            if self.rule_only_choice():
                self.add_progress()
            if self.rule_restricted_hint():
                self.add_progress()
            if self.rule_non_candle():
                self.add_progress()
            if self.p.is_solved():
                return True
            
        return False               


    def solve(self):
        easy = self.direct_solving()
        if easy:
            return("EASY")
        else:
            if self.advanced_solving():
                return("HARD")
        return("IMPOSSIBLE")

          

    

    