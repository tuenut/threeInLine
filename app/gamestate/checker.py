import logging

from typing import List

from .objects import CellState


class DestroyableChecker:
    _buffer = None

    def __init__(self, cells: List[List[CellState]]):
        self.logger = logging.getLogger(__name__)
        self.cells = cells

        self.x = None
        self.y = None
        self.comparing_color = None
        self.balls_to_destroy = None

        self.DIRECTIONS = {
            "left": self.__slice_left_of,
            "right": self.__slice_right_of,
            "up": self.__slice_up_on,
            "down": self.__slice_down_on,
        }
        self.DIAGONALS = {
            "up-left": self.__slice_up_left_of,
            "up-right": self.__slice_up_right_of,
            "down-left": self.__slice_down_left_of,
            "down-right": self.__slice_down_right_of
        }

    def check(self, x, y, color=None):
        self.x = x
        self.y = y
        self.comparing_color = color if color else self.cells[self.y][self.x].ball.color
        self.balls_to_destroy = []
        self._buffer = []

        self.logger.debug(f"Check for ({self.x}, {self.y}) of <{self.comparing_color}> color.")

        for direction in self.DIRECTIONS:
            self.__check_sice(self.DIRECTIONS.get(direction)())

        for diagonal in self.DIAGONALS:
            self.__check_sice(self.DIAGONALS.get(diagonal)())

        if self.balls_to_destroy:
            self.balls_to_destroy.append(self.cells[y][x].ball)

        self.logger.debug(f"Neighbour same color balls: {self.balls_to_destroy}")

        return self.balls_to_destroy

    def __check_sice(self, cells_slice):
        self.logger.debug(f"Check from ({self.x}, {self.y}) in: {cells_slice}")

        for cell in cells_slice:
            if cell.ball:
                if cell.ball.color != self.comparing_color:
                    break
                else:
                    self._buffer.append(cell.ball)

        self.logger.debug(f"Found: {self._buffer}")

        self.__flush()

    def __flush(self):
        if len(self._buffer) >= 2:
            self.balls_to_destroy.extend(self._buffer)

        self._buffer = []

    def __slice_left_of(self):
        return [self.cells[self.y][x] for x in range(self.x - 1, -1, -1)]

    def __slice_right_of(self):
        return [self.cells[self.y][x] for x in range(self.x + 1, len(self.cells[self.y]))]

    def __slice_up_on(self):
        return [self.cells[y][self.x] for y in range(self.y - 1, -1, -1)]

    def __slice_down_on(self):
        return [self.cells[y][self.x] for y in range(self.y + 1, len(self.cells))]

    def __slice_up_left_of(self):
        return [
            self.cells[y][x]
            for x, y in zip(
                range(self.x - 1, -1, -1),
                range(self.y - 1, -1, -1)
            )
        ]

    def __slice_up_right_of(self):
        return [
            self.cells[y][x]
            for x, y in zip(
                range(self.x + 1, len(self.cells[self.y])),
                range(self.y - 1, -1, -1)
            )
        ]

    def __slice_down_left_of(self):
        return [
            self.cells[y][x]
            for x, y in zip(
                range(self.x - 1, -1, -1),
                range(self.y + 1, len(self.cells))
            )
        ]

    def __slice_down_right_of(self):
        return [
            self.cells[y][x]
            for x, y in zip(
                range(self.x + 1, len(self.cells[self.y])),
                range(self.y + 1, len(self.cells))
            )
        ]
