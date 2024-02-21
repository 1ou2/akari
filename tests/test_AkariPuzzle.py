import unittest
#from unittest.mock import MagicMock

# Test AkariPuzzle
from akari.akariPuzzle import AkariPuzzle
from akari.cell import Cell

class TestAkariPuzzle(unittest.TestCase):

    """
       0 1 2 3 4 5 
       ------------
    0| . . . . 3 .
    1| . . . . . 3
    2| . . . . . .
    3| X . . . X .
    4| 1 . . . . 0
    5| X . X . . .
    """
    def sample_puzzle1(self):
        size = 6
        puzzle = AkariPuzzle(size,size)
        puzzle.add_box(0, 4, 3)
        puzzle.add_box(1, 5, 3)
        puzzle.add_box(3, 0)
        puzzle.add_box(3, 4)
        puzzle.add_box(4, 0, 1)
        puzzle.add_box(4, 5, 0)
        puzzle.add_box(5, 0)
        puzzle.add_box(5, 2)
        return puzzle
    
    """
       0 1 2 3 4 5 
       ------------
    0| . . X . X . 
    1| . . . X . X 
    2| . X 1 1 . X 
    3| 3 . . . X X 
    4| . X . . . .
    5| . . . 3 . .
    """
    def sample_puzzle2(self):
        size = 6
        puzzle = AkariPuzzle(size, size)
        puzzle.add_box(0, 2)
        puzzle.add_box(0, 4)
        puzzle.add_box(1, 3)
        puzzle.add_box(1, 5)
        puzzle.add_box(2, 1)
        puzzle.add_box(2, 2, 1)
        puzzle.add_box(2, 3, 1)
        puzzle.add_box(2, 5)
        puzzle.add_box(3, 0, 3)
        puzzle.add_box(3, 4)
        puzzle.add_box(3, 5)
        puzzle.add_box(4, 1)
        puzzle.add_box(5, 3, 3)
        
        return puzzle
        

    def test_reachable_cells(self):
        puzzle = self.sample_puzzle1()
        self.assertFalse(puzzle.get_reachable_cells(Cell(0, 5)))
        self.assertEqual(len(puzzle.get_reachable_cells(Cell(4, 0))),4)
        self.assertEqual(len(puzzle.get_reachable_cells(Cell(4, 5))), 7)
        self.assertEqual(len(puzzle.get_reachable_cells(Cell(5, 0))), 1)




