from akari.akariPuzzle import AkariPuzzle
from akari.cell import Cell
from akari.akariFile import AkariFile
from akari.akariSolver import AkariSolver
import os,glob

dir = "puzzles"
# list all files in puzzles directory using glob module
files = glob.glob(os.path.join(dir, "*.txt"))
# solve each file
for file in files:
    print(f"\n-- {file}")
    puzzle = AkariFile(file).get_puzzle()
    solver = AkariSolver(puzzle)
    status = solver.solve()
    solver.p.print()
    print(f"Status: {status}")


#puzzle = AkariFile("puzzles/easy-8-01.txt").get_puzzle()
#puzzle = AkariFile("puzzles/easy-6-02.txt").get_puzzle()
#puzzle = AkariFile("puzzles/hard-10-02.txt").get_puzzle()
#puzzle.print()
#solver = AkariSolver(puzzle)
#solver.solve()
#solver.p.print()
