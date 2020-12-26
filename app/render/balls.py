import pygame
import logging

from config import ALPHA_COLOR
from app.gamestate.objects import BallState


class BallRender:
    SELECTED_BORDER = 3
    BORDER_COLOR = (0, 0, 0)

    def __init__(self, parent_surface, state: BallState, center, radius, dimensions, position):
        self.logger = logging.getLogger(__name__)

        self.parent_surface = parent_surface
        self.state = state
        self.center = center
        self.radius = radius
        self.dimensions = dimensions
        self.position = position

        pygame.font.init()
        self.font = pygame.font.SysFont('mono', 12, bold=True)

        self.surface = pygame.Surface(self.dimensions).convert()
        self.surface.fill(ALPHA_COLOR)
        self.surface.set_colorkey(ALPHA_COLOR)

        self.__draw()

    def __draw(self):
        text = f"{str(id(self.state))[-5:]}"
        self.font_surface = self.font.render(text, True, (0, 0, 0))

        if self.state.selected:
            pygame.draw.circle(self.surface, self.BORDER_COLOR, self.center, self.radius)
            pygame.draw.circle(self.surface, self.state.color_rgb, self.center, self.radius-self.SELECTED_BORDER)
        else:
            pygame.draw.circle(self.surface, self.state.color_rgb, self.center, self.radius)


    def update(self):
        self.__draw()
        self.parent_surface.blit(self.surface, self.position)
        self.parent_surface.blit(self.font_surface, self.position)
