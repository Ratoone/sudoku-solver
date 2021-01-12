import numpy as np

from SudokuNumberCell import SudokuNumberCell
from SudokuCell import SudokuCell


class SudokuPuzzle:
    def __init__(self, size: int, puzzle: np.ndarray = None):
        self.size = size

        self.cellSize = round(np.math.sqrt(size))
        if self.cellSize ** 2 != size:
            raise Exception("Invalid Sudoku size")

        self.rowValues = [set() for _ in range(size)]
        self.colValues = [set() for _ in range(size)]
        self.cells = [SudokuCell(self.cellSize) for _ in range(size)]
        if puzzle is not None:
            for i in range(size):
                for j in range(size):
                    if puzzle[i][j] != 0:
                        self.rowValues[i].add(puzzle[i][j])
                        self.colValues[j].add(puzzle[i][j])
                        self.fillAt(i, j, puzzle[i][j])

    # TODO: cross checks?

    def fillAt(self, i, j, value):
        index = (i % self.cellSize) * self.cellSize + j % self.cellSize
        self.cells[self.coordinatesToCell(i, j)].fillValue(index, value)

    def getCellAt(self, i, j):
        index = (i % self.cellSize) * self.cellSize + j % self.cellSize
        return self.cells[self.coordinatesToCell(i, j)].getCellAt(index)

    def coordinatesToCell(self, i, j) -> int:
        reducedRowNumber = i // self.cellSize
        reducedColNumber = j // self.cellSize
        return int(reducedRowNumber * self.cellSize + reducedColNumber)

    def checkAtRowCol(self, i, j) -> bool:
        currentNumber = self.getCellAt(i, j)

        if currentNumber.value != 0:
            return False

        modified = False
        index = 0
        while index < len(currentNumber.possibleValues):
            value = currentNumber.possibleValues[index]
            if value in self.rowValues[i] or \
                    value in self.colValues[j] or \
                    value in self.cells[self.coordinatesToCell(i, j)]:
                currentNumber.removePossibleValue(value)
                modified = True
            else:
                index += 1

        if currentNumber.value != 0:
            value = currentNumber.value
            self.rowValues[i].add(value)
            self.colValues[j].add(value)
            self.fillAt(i, j, value)
            modified = True

        return modified

    def printSudoku(self) -> np.ndarray:
        output = []
        for i in range(self.size):
            output.append([])
            for j in range(self.size):
                output[-1].append(self.getCellAt(i, j).value)

        return np.array(output)

    @staticmethod
    def createFromFile(path):
        puzzleMatrix = np.loadtxt(path)
        return SudokuPuzzle(puzzleMatrix.shape[0], puzzleMatrix)
