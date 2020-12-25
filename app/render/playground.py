import logging

from .cells import CellsRenderManager


class PlayGround:
    def __init__(self, parent_surface, cells_state):
        self.surface = parent_surface

        self.cells_manager = CellsRenderManager(self.surface, cells_state)

    def update(self):
        self.cells_manager.update()
