import numpy as np

from SudokuNumberCell import SudokuNumberCell


class SudokuPuzzle:
    def __init__(self, size: int, puzzle: np.ndarray = None):
        self.size = size

        self.cellSize = round(np.math.sqrt(size))
        if self.cellSize ** 2 != size:
            raise Exception("Invalid Sudoku size")

        self.rowValues = [set() for _ in range(size)]
        self.colValues = [set() for _ in range(size)]
        self.cellValues = [set() for _ in range(size)]
        if puzzle is not None:
            self.puzzle = []
            for i in range(size):
                self.puzzle.append([])
                for j in range(size):
                    self.puzzle[-1].append(SudokuNumberCell(puzzle[i][j], size))
                    if puzzle[i][j] != 0:
                        self.rowValues[i].add(puzzle[i][j])
                        self.colValues[j].add(puzzle[i][j])
                        self.cellValues[self.coordinatesToCell(i, j)].add(puzzle[i][j])
        else:
            self.puzzle = size * [size * [SudokuNumberCell(0, size)]]

    def coordinatesToCell(self, i, j) -> int:
        reducedRowNumber = i // self.cellSize
        reducedColNumber = j // self.cellSize
        return int(reducedRowNumber * self.cellSize + reducedColNumber)

    def checkAtRowCol(self, i, j) -> bool:
        currentNumber = self.puzzle[i][j]

        if currentNumber.value != 0:
            return False

        modified = False
        index = 0
        while index < len(currentNumber.possibleValues):
            value = currentNumber.possibleValues[index]
            if value in self.rowValues[i] or \
                    value in self.colValues[j] or \
                    value in self.cellValues[self.coordinatesToCell(i, j)]:
                currentNumber.possibleValues.remove(value)
                modified = True
            else:
                index += 1

        if len(currentNumber.possibleValues) == 1:
            value = currentNumber.possibleValues[0]
            currentNumber.value = value
            self.rowValues[i].add(value)
            self.colValues[j].add(value)
            self.cellValues[self.coordinatesToCell(i, j)].add(value)
            modified = True

        return modified

    def printSudoku(self) -> np.ndarray:
        output = []
        for i in range(self.size):
            output.append([])
            for j in range(self.size):
                output[-1].append(self.puzzle[i][j].value)

        return np.array(output)

    @staticmethod
    def createFromFile(path):
        puzzleMatrix = np.loadtxt(path)
        return SudokuPuzzle(puzzleMatrix.shape[0], puzzleMatrix)
