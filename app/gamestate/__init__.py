from __future__ import annotations

import logging
import random
import copy

from pprint import PrettyPrinter

from .objects import CellState
from app.gamestate.objects import BallState
from .checker import DestroyableChecker

pp = PrettyPrinter(indent=4, width=80, compact=True)


class GameActions:
    def __init__(self, state: GameStateController):
        self.state = state

    def select_ball(self, ball_object: BallState):
        self.unselect_ball()

        self.state.selected_ball = ball_object.select()

    def unselect_ball(self):
        try:
            self.state.selected_ball = self.state.selected_ball.unselect()
        except AttributeError:
            pass

    def swap_balls(self, departure_cell: CellState, destination_cell: CellState):
        buffered_ball = destination_cell.ball

        destination_cell.put_ball_on_cell(departure_cell.ball)
        departure_cell.put_ball_on_cell(buffered_ball)

        self.state.selected_ball = self.state.selected_ball.unselect()


class GameStateController:
    __selected_ball = None  # type: BallState

    def __init__(self, *args, rows=10, columns=10, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Init GameState...")

        self.rows = rows
        self.columns = columns

        self.cells = [[CellState(x, y) for x in range(self.rows)] for y in range(self.columns)]

        self.destroy_checker = DestroyableChecker(self.cells)
        self.actions = GameActions(self)

        for row in self.cells:
            for cell_object in row:
                ball_obj = self._create_new_ball_on_init(cell_object)
                cell_object.put_ball_on_cell(ball_obj)

    @property
    def selected_ball(self):
        return self.__selected_ball

    @selected_ball.setter
    def selected_ball(self, ball_object):
        if isinstance(ball_object, BallState) or ball_object is None:
            self.__selected_ball = ball_object
        else:
            raise Exception(f"received object does not match type of {BallState} or {None}")

    def _create_new_ball_on_init(self, cell_object):
        self.logger.debug(f"Create ball in cell ({cell_object.x}, {cell_object.y})")

        colors = copy.deepcopy(BallState.COLORS)
        color = list(colors.keys())[random.randint(0, len(colors) - 1)]

        self.logger.debug(f"Choosing <{color}> from {colors.keys()}")

        same_color_balls = self.destroy_checker.check(cell_object.x, cell_object.y, color)

        while same_color_balls:
            colors.pop(color)
            color = list(colors.keys())[random.randint(0, len(colors) - 1)]
            same_color_balls = self.destroy_checker.check(cell_object.x, cell_object.y, color)

        return BallState(color, cell_object)

    def update(self):
        """May be unnecessary, because not any background activity in game, only reaction on user actions."""
        pass

    def handle_click_on_ball(self, x, y):
        self.logger.debug(f"Handle click on ({x}, {y}).")

        clicked_ball = self.get_cell(x, y).ball

        self.logger.debug(f"Found {clicked_ball}.")

        if self.selected_ball is None:
            self.actions.select_ball(clicked_ball)

        elif self.selected_ball is clicked_ball:
            self.actions.unselect_ball()

        else:
            destination_cell = self.get_cell(x, y)
            departure_cell = self.selected_ball.cell

            if self.is_cells_swapable(departure_cell, destination_cell):
                self.actions.swap_balls(departure_cell, destination_cell)

            else:
                self.actions.select_ball(clicked_ball)

    @staticmethod
    def is_cells_swapable(departure_cell: CellState, destination_cell: CellState) -> bool:
        vector = tuple(map(lambda pos: pos[0] - pos[1], zip(departure_cell.pos, destination_cell.pos)))
        return bool(vector[0]) != bool(vector[1]) and (any(map(lambda coordinate: abs(coordinate) == 1, vector)))

    def get_cell(self, x: int, y: int) -> CellState:
        return self.cells[y][x]
