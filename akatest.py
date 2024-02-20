from AkariPuzzle import AkariPuzzle
from AkariFile import AkariFile
from AkariSolver import AkariSolver

puzzle = AkariFile("easy-8-01.txt").get_puzzle()

puzzle.print()
solver = AkariSolver(puzzle)

solver.solve()

solver.p.print()
"""
puzzle = AkariPuzzle(5,6)
print(puzzle.board)


puzzle.add_box(2, 1, 4)
puzzle.add_box(3, 3)
puzzle.add_candle(0,3)
puzzle.add_candle(1,0)

puzzle.print()

"""