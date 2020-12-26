from __future__ import annotations

import logging


class CellState:
    def __init__(self, x, y, *args, ball: BallState = None, **kwargs):
        self.logger = logging.getLogger(__name__)

        self.ball = ball  # type: BallState
        self.x = x
        self.y = y

    @property
    def pos(self):
        return self.x, self.y

    def put_ball_on_cell(self, ball_obj):
        self.ball = ball_obj
        self.ball.cell = self

    def __repr__(self):
        return f"<Cell on ({self.x}, {self.y} with {self.ball})>"


class BallState:
    COLORS = {
        "red": {"color": (200, 0, 0)},
        "green": {"color": (0, 200, 0)},
        "blue": {"color": (0, 0, 200)},
        "yellow": {"color": (200, 200, 0)}
    }

    DEBUG_COLOR = (200, 0, 200)
    __selected = False

    def __init__(self, color: str, cell: CellState):
        self.logger = logging.getLogger(__name__)

        self.color = color

        self.__color = self.COLORS.get(self.color).get("color")
        self.__selected_color = self.__get_higlight_color()

        self.cell = cell

    @property
    def color_rgb(self):
        if self.selected:
            return self.__selected_color
        else:
            return self.__color

    def __get_higlight_color(self):
        if any(map(lambda rgb_part: (rgb_part - 30) <= 30, self.__color)):
            return tuple(map(lambda rgb_part: rgb_part + 30 if (rgb_part + 30) <= 255 else 255, self.__color))
        else:
            return tuple(map(lambda rgb_part: rgb_part - 30, self.__color))

    @property
    def selected(self):
        return self.__selected

    def select(self):
        self.__selected = True
        return self

    def unselect(self):
        self.__selected = False
        return None

    def __repr__(self):
        selected_status = 'SELECTED' if self.selected else 'UNSELECTED'
        return f"<{self.color} {self.color_rgb} {selected_status} ball on ({self.cell.x}, {self.cell.y})>"
