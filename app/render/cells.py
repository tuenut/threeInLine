import pygame
import logging
import math

from typing import List

from .balls import BallRender
from app.gamestate.objects import CellState
from config import COLOR_CELL_BG, COLOR_CELL_BORDER_DARK, COLOR_CELL_BORDER_LIGHT


class CellRender:
    BORDER = 3

    def __init__(self, parent_surface: pygame.Surface, cell_state: CellState, width, height):
        self.logger = logging.getLogger(__name__)

        self.w = width
        self.h = height

        self.state = cell_state
        self.ball = None

        self.parent_surface = parent_surface
        self.surface = pygame.Surface((self.w, self.h)).convert()

    @property
    def x(self):
        return self.w * self.state.x

    @property
    def y(self):
        return self.h * self.state.y

    def __draw_cell(self):
        pygame.draw.rect(
            surface=self.surface,
            color=COLOR_CELL_BG,
            rect=(self.BORDER, self.BORDER, self.w - 2 * self.BORDER, self.h - 2 * self.BORDER)
        )
        pygame.draw.lines(
            surface=self.surface,
            color=COLOR_CELL_BORDER_LIGHT,
            closed=False,
            points=[(1, self.h), (1, 1), (self.w, 1), ],
            width=self.BORDER
        )
        pygame.draw.lines(
            surface=self.surface,
            color=COLOR_CELL_BORDER_DARK,
            closed=False,
            points=[(self.w - 2, - 1), (self.w - 2, self.h - 2), (0, self.h - 2)],
            width=self.BORDER
        )

    def __draw_ball(self):
        if self.state.ball:
            self.ball = BallRender(
                self.parent_surface,
                self.state.ball,
                ((self.w - self.BORDER * 2) / 2, (self.h - self.BORDER * 2) / 2),
                ((self.w + self.h) / 4) - math.floor(self.BORDER * 1.75),
                (self.w - CellRender.BORDER * 2, self.h - CellRender.BORDER * 2),
                (self.x + self.BORDER, self.y + self.BORDER)
            )

    def update(self):
        self.__draw_cell()
        self.__draw_ball()

        self.parent_surface.blit(self.surface, (self.x, self.y))
        self.ball.update()


class CellsRenderManager:
    def __init__(self, parent_surface: pygame.Surface, cells_state):
        self.logger = logging.getLogger(__name__)

        self.surface = parent_surface

        self.__cells_state = cells_state
        self.cells = []  # type: List[CellRender]

        playground_width, playground_heigth = self.surface.get_size()
        self.cell_width = math.ceil(playground_width / max([len(row) for row in self.__cells_state]))
        self.cell_height = math.ceil(playground_heigth / len(self.__cells_state))

        self.__init_draw()

    def __init_draw(self):
        for cell_row in self.__cells_state:
            for cell in cell_row:
                cell_render = CellRender(self.surface, cell, self.cell_width, self.cell_height)

                self.cells.append(cell_render)

    def update(self):
        for cell in self.cells:
            cell.update()
