import logging
import pygame
import math

from app.events import EventManager
from app.gamestate import GameStateController
from app.render import Render


class Game:
    """Класс игры.
    Описывает все поведение игры и управляет взаимодействием сущностей игры.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        self.logger.debug("Init Game...")

        self.state = GameStateController()
        self.render = Render(game_state=self.state)
        self.events = EventManager()

        self.__init_game_events()

    def update(self):
        self.render.update()

    def __init_game_events(self):
        self.events.subscribe(event_type=pygame.MOUSEBUTTONDOWN, callback=self._handle_mouse, kwargs=["pos", "button"])

    def _handle_mouse(self, *args, pos, button, **kwargs):
        self.logger.debug(f"Click on {pos}")

        if button == pygame.BUTTON_LEFT:
            self._handle_left_click(pos)

        elif button == pygame.BUTTON_RIGHT:
            self.logger.debug(f"Click on RIGHT button on {pos}")

    def _handle_left_click(self, pos):
        w = self.render.playground.cells_manager.cell_width
        h = self.render.playground.cells_manager.cell_height

        try:
            x, y = math.ceil(pos[0] / w) - 1, math.ceil(pos[1] / h) - 1

            self.logger.debug(f"Assume that cell ({x}, {y})")
            self.logger.debug(f"{self.state.cells[y][x]}")
        except Exception as e:
            self.logger.exception("Something goes wrong while calculate cell address.")

            return

        self.state.handle_click_on_ball(x, y)
