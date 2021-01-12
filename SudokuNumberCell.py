class SudokuNumberCell:
    def __init__(self, value: int, sudokuSize):
        self.value = value
        if value == 0:
            self.possibleValues = set(range(1, sudokuSize + 1))

    def removePossibleValue(self, x):
        if self.value > 0:
            return 0

        if x in self.possibleValues:
            self.possibleValues.remove(x)
        if len(self.possibleValues) == 1:
            self.value = self.possibleValues.pop()
            return self.value
        return 0

    def setValue(self, value):
        self.value = value
        self.possibleValues = set()
