import logging
import pygame

from app.events import EventManager
from app.gamestate import GameStateController
from app.render import Render

from app.utils.logger import pp

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
        if button == pygame.BUTTON_LEFT:
            self.logger.debug(f"Click on LEFT button on {pos}")

            for cell in self.render.playground.cells_manager.cells:
                if cell.rect.collidepoint(pos):
                    self.logger.debug(f"Click on {cell.state}")

        elif button == pygame.BUTTON_RIGHT:
            self.logger.debug(f"Click on RIGHT button on {pos}")
