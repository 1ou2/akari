from akari.akariPuzzle import AkariPuzzle
from akari.cell import Cell
from akari.akariFile import AkariFile
from akari.akariSolver import AkariSolver


puzzle = AkariFile("puzzles/easy-8-01.txt").get_puzzle()
#puzzle = AkariFile("puzzles/easy-6-02.txt").get_puzzle()
puzzle.print()
solver = AkariSolver(puzzle)

solver.solve()

solver.p.print()
