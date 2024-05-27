class RowSizeException(Exception):
    def __init__(self, desired, actual):
        super().__init__(f"Неверные размеры строки: ожидалось {desired}, оказалось {actual}")


class WallsLocationException(Exception):
    def __init__(self, first_cell, second_cell):
        super().__init__(f"Неверно заданы стены между клетками {first_cell} и {second_cell}")

