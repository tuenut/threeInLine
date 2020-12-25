import logging
import random
import copy

from pprint import PrettyPrinter

from .cell import CellState
from .ball import BallState
from .checker import DestroyableChecker

pp = PrettyPrinter(indent=4, width=80, compact=True)


class GameStateController:
    def __init__(self, *args, rows=10, columns=10, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Init GameState...")

        self.__color_debug = False

        self.rows = rows
        self.columns = columns

        self.cells = [
            [
                CellState(x, y)
                for x in range(self.rows)
            ]
            for y in range(self.columns)
        ]

        self.destroy_checker = DestroyableChecker(self.cells)

        for row in self.cells:
            for cell_obj in row:
                ball_obj = self._create_new_ball_on_init(cell_obj.x, cell_obj.y)
                cell_obj.put_ball_on_cell(ball_obj)

        # self.logger.debug(pp.pformat(self.cells))

    def _create_new_ball_on_init(self, x, y):
        self.logger.debug(f"Create ball in cell ({x}, {y})")

        if self.__color_debug:
            return BallState("debug", x, y)

        colors = copy.deepcopy(BallState.COLORS)
        color = list(colors.keys())[random.randint(0, len(colors)-1)]

        self.logger.debug(f"Choosing <{color}> from {colors.keys()}")

        same_color_balls = self.destroy_checker.check(x, y, color)

        while same_color_balls:
            colors.pop(color)
            color = list(colors.keys())[random.randint(0, len(colors) - 1)]
            same_color_balls = self.destroy_checker.check(x, y, color)

        return BallState(color, x, y)

    def update(self):
        pass
