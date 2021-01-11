class SudokuNumberCell:
    def __init__(self, value: int, sudokuSize):
        self.value = value
        if value == 0:
            self.possibleValues = list(range(1, sudokuSize + 1))
