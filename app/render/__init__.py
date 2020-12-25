import logging
import pygame  # type: ignore

from .playground import PlayGround
from config import COLOR_RENDER_BG
from app.gamestate import GameStateController


class Render:
    logger = logging.getLogger(__name__)

    def __init__(self, game_state: GameStateController, width=640, height=640):
        self.logger.debug("Init Render...")

        self.__game_state = game_state

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)

        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.surface.fill(COLOR_RENDER_BG)

        self.playground = PlayGround(self.surface, self.__game_state.cells)

    def update(self):
        pygame.display.flip()
        self.surface.fill(COLOR_RENDER_BG)

        self.playground.update()

        self.screen.blit(self.surface, (0, 0))
