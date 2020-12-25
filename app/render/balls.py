import pygame
import logging

from config import ALPHA_COLOR


class BallRender:
    def __init__(self, parent_surface, state, center, radius, dimensions, position):
        self.logger = logging.getLogger(__name__)

        self.parent_surface = parent_surface
        self.state = state
        self.center = center
        self.radius = radius
        self.dimensions = dimensions
        self.position = position

        pygame.font.init()
        self.font = pygame.font.SysFont('mono', 12, bold=True)

        self.draw()

    def draw(self):
        self.surface = pygame.Surface(self.dimensions).convert()
        self.surface.fill(ALPHA_COLOR)
        self.surface.set_colorkey(ALPHA_COLOR)

        text = f"{self.state.x}.{self.state.y}"
        fw, fh = self.font.size(text)
        self.font_surface = self.font.render(text, True, (0, 0, 0))

        pygame.draw.circle(self.surface, self.state.color_rgb, self.center, self.radius)

    def update(self):
        self.parent_surface.blit(self.surface, self.position)
        self.parent_surface.blit(self.font_surface, tuple(map(sum, zip(self.center, self.position))))
