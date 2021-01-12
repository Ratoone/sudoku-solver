class SudokuNumberCell:
    def __init__(self, value: int, sudokuSize):
        self.value = value
        if value == 0:
            self.possibleValues = list(range(1, sudokuSize + 1))

    def removePossibleValue(self, x):
        self.possibleValues.remove(x)
        if len(self.possibleValues) == 1:
            self.value = self.possibleValues[0]