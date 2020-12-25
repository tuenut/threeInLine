class AppState:
    """Класс для различных состояний приложения."""

    def __init__(self):
        self.__run = None
        self.__pause = False

    @property
    def is_run(self):
        return self.__run

    @property
    def is_pause(self):
        return self.__pause

    def pause(self):
        self.__pause = not self.__pause

    def run(self):
        self.__run = True

    def stop(self):
        self.__run = False
