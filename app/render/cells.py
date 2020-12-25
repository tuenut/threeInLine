import pygame
import logging
import math

from typing import List

from .balls import BallRender
from app.gamestate.cell import CellState
from config import COLOR_CELL_BG, COLOR_CELL_BORDER_DARK, COLOR_CELL_BORDER_LIGHT


class CellRender:
    BORDER = 3

    def __init__(self, parent_surface: pygame.Surface, cell_state: CellState, width, height):
        self.logger = logging.getLogger(__name__)

        self.w = width
        self.h = height
        self.parent_surface = parent_surface
        self.state = cell_state

        self.__draw()

    @property
    def x(self):
        return self.w * self.state.x

    @property
    def y(self):
        return self.h * self.state.y

    def __draw(self):
        self.surface = pygame.Surface((self.w, self.h)).convert()
        self.rect = pygame.draw.rect(
            self.surface,
            COLOR_CELL_BG,
            (
                self.BORDER,
                self.BORDER,
                self.w - 2 * self.BORDER,
                self.h - 2 * self.BORDER
            )
        )
        pygame.draw.lines(
            self.surface,
            COLOR_CELL_BORDER_LIGHT,
            closed=False,
            points=[(1, self.h), (1, 1), (self.w, 1), ],
            width=self.BORDER
        )
        pygame.draw.lines(
            self.surface,
            COLOR_CELL_BORDER_DARK,
            closed=False,
            points=[(self.w - 2, - 1), (self.w - 2, self.h - 2), (0, self.h - 2)],
            width=self.BORDER
        )

    def update(self):
        self.parent_surface.blit(self.surface, (self.x, self.y))


class CellsRenderManager:
    def __init__(self, parent_surface: pygame.Surface, cells_state):
        self.logger = logging.getLogger(__name__)

        self.surface = parent_surface

        self.__cells_state = cells_state
        self.cells = []  # type: List[CellRender]
        self.balls = []

        playground_width, playground_heigth = self.surface.get_size()
        self.cell_width = math.ceil(playground_width / max([len(row) for row in self.__cells_state]))
        self.cell_height = math.ceil(playground_heigth / len(self.__cells_state))
        self.ball_center = (
            (self.cell_width - CellRender.BORDER * 2) / 2,
            (self.cell_height - CellRender.BORDER * 2) / 2
        )
        self.ball_radius = ((self.cell_width + self.cell_height) / 4) - math.floor(CellRender.BORDER * 1.75)
        self.ball_surface_dimensions = (
            self.cell_width - CellRender.BORDER * 2,
            self.cell_height - CellRender.BORDER * 2
        )

        self.__init_draw()

    def __init_draw(self):
        for cell_row in self.__cells_state:
            for cell in cell_row:
                cell_render = CellRender(self.surface, cell, self.cell_width, self.cell_height)
                ball_render = BallRender(
                    self.surface,
                    state=cell.ball,
                    center=self.ball_center,
                    radius=self.ball_radius,
                    dimensions=self.ball_surface_dimensions,
                    position=(cell_render.x + CellRender.BORDER, cell_render.y + CellRender.BORDER)
                )

                self.cells.append(cell_render)
                self.balls.append(ball_render)

    def update(self):
        for cell, ball in zip(self.cells, self.balls):
            cell.update()
            ball.update()
