import re

import numpy as np

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
        for value in currentNumber.possibleValues.copy():
            if value in self.rowValues[i] or \
                    value in self.colValues[j] or \
                    value in self.cells[self.coordinatesToCell(i, j)]:
                currentNumber.removePossibleValue(value)
                modified = True

        if currentNumber.value != 0:
            value = currentNumber.value
            self.fillAt(i, j, value)
            self.updateAll()
            modified = True

        if not modified:
            for cell in self.cells:
                modified = cell.checkCell() or modified

            if modified:
                self.updateAll()

        return modified

    def updateAll(self):
        for i in range(self.size):
            for j in range(self.size):
                currentCell = self.getCellAt(i, j)
                if currentCell.value != 0:
                    self.rowValues[i].add(currentCell.value)
                    self.colValues[j].add(currentCell.value)
                else:
                    currentCell.possibleValues = currentCell.possibleValues.difference(self.rowValues[i])
                    currentCell.possibleValues = currentCell.possibleValues.difference(self.colValues[j])
                    if len(currentCell.possibleValues) == 1:
                        self.fillAt(i, j, currentCell.possibleValues.pop())
                        self.updateAll()
                        return

    def printSudoku(self):
        output = []
        for i in range(self.size):
            output.append([])
            for j in range(self.size):
                output[-1].append(self.getCellAt(i, j).value)

        return re.sub("[\[\]. ]", "", np.array2string(np.array(output), separator="|")) + "|"

    @staticmethod
    def createFromFile(path):
        puzzleMatrix = np.loadtxt(path)
        return SudokuPuzzle(puzzleMatrix.shape[0], puzzleMatrix)
