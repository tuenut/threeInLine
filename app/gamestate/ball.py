class BallState:
    COLORS = {
        "red": {"color": (200, 0, 0)},
        "green": {"color": (0, 200, 0)},
        "blue": {"color": (0, 0, 200)},
        "yellow": {"color": (200, 200, 0)}
    }

    DEBUG_COLOR = (200, 0, 200)

    def __init__(self, color: str, x: int, y: int):
        self.color = color
        self.color_rgb = self.DEBUG_COLOR if color == "debug" else self.COLORS.get(self.color).get("color")
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<{self.color} {self.color_rgb} ball on ({self.x}, {self.y})>"
