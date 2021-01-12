from SudokuNumberCell import SudokuNumberCell


class SudokuCell:
    def __init__(self, cellSize: int):
        self.cellSize = cellSize
        self.possibleValues = set(range(1, cellSize ** 2 + 1))
        self.numberCells = [SudokuNumberCell(0, cellSize ** 2) for _ in range(cellSize ** 2)]

    def fillValue(self, index, value: int):
        if value not in self.possibleValues:
            raise Exception("Value {} already taken!".format(value))

        self.possibleValues.remove(value)
        self.numberCells[index].value = value

    def getCellAt(self, index):
        return self.numberCells[index]

    def checkRow(self, columns):
        if len(columns) != self.cellSize:
            raise Exception("Invalid number of columns fed")

    def __contains__(self, item):
        return item not in self.possibleValues
