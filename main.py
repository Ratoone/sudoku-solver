from SudokuPuzzle import SudokuPuzzle

if __name__ == '__main__':
    sudoku = SudokuPuzzle.createFromFile("Sample Puzzles/puzzle1.txt")

    modified = True

    iterations = 0
    while modified:
        modified = False
        iterations += 1
        for i in range(sudoku.size):
            for j in range(sudoku.size):
                modified = modified or sudoku.checkAtRowCol(i, j)

    print(sudoku.printSudoku())
    print(iterations)
