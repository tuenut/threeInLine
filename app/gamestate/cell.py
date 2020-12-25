from .ball import BallState


class CellState:
    def __init__(self, x, y, *args, ball: BallState = None, **kwargs):
        self.ball = ball  # type: BallState
        self.x = x
        self.y = y

    def put_ball_on_cell(self, ball_obj):
        if self.ball:
            raise Exception(f"Can't place {ball_obj} in cell, because it already contains {self.ball}")

        self.ball = ball_obj

    def __repr__(self):
        return f"<Cell on ({self.x}, {self.y} with {self.ball})>"
