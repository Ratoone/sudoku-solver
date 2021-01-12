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
        self.numberCells[index].setValue(value)
        for i, number in enumerate(self.numberCells):
            filled = number.removePossibleValue(value)
            if filled > 0:
                self.fillValue(i, filled)

    def getCellAt(self, index):
        return self.numberCells[index]

    def checkCell(self):
        """
        Check if there exists one number cell that contains a possible value only it
        can have
        :return:
        """
        filled = False
        for value in self.possibleValues.copy():
            potentialCount = 0
            potentialSquare = 0
            for index, number in enumerate(self.numberCells):
                if value in number.possibleValues:
                    potentialCount += 1
                    potentialSquare = index
                if potentialCount > 1:
                    break
            if potentialCount == 1:
                self.fillValue(potentialSquare, value)
                filled = True
        return filled

    def __contains__(self, item):
        return item not in self.possibleValues
