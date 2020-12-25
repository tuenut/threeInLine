import logging
import pygame

from app.appstate import AppState
from app.events import EventManager
from app.game import Game
from config import FPS


class App:
    _playtime = 0.0
    _HINT_IN_TITLE = "Press ESC to quit"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Init App...")

        self.title = self._HINT_IN_TITLE
        self.fps = FPS

        self.state = AppState()

        self.events = EventManager()
        self.game = Game()

        self.__init_pygame()
        self.__init_global_app_events()

    def run(self):
        self.state.run()
        self.__mainloop()
        self.exit()

    def exit(self):
        pygame.quit()

    def __mainloop(self):
        while self.state.is_run:
            self.events.check_events()

            if not self.state.is_pause:
                self.__fps_update()
                self.game.update()

    def __init_pygame(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        pygame.display.set_caption(self.title)

    def __init_global_app_events(self):
        self.events.subscribe(event_type=pygame.QUIT, callback=self.state.stop, )
        self.events.subscribe(event_type=pygame.KEYDOWN, callback=self.state.stop, conditions={"key": pygame.K_q})
        self.events.subscribe(event_type=pygame.KEYDOWN, callback=self.state.stop, conditions={"key": pygame.K_ESCAPE})
        self.events.subscribe(event_type=pygame.KEYDOWN, callback=self.state.pause, conditions={"key": pygame.K_p})

    def __fps_update(self):
        milliseconds = self._clock.tick(self.fps)
        self._playtime += milliseconds / 1000.0

        fps = "FPS: {0:.2f}   Playtime: {1:.2f}".format(self._clock.get_fps(), self._playtime)
        self.title = "{title}. {fps}".format(title=self._HINT_IN_TITLE, fps=fps)

        pygame.display.set_caption(self.title)
