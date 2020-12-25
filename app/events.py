import pygame
import logging

from typing import Optional, Dict, List


class __EventManagerSingleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)

        return cls.__instance


class EventManager(metaclass=__EventManagerSingleton):
    logger = logging.getLogger(__name__)
    logger.level = logging.INFO

    def __init__(self):
        self.logger.debug("Init events manager.")

        self.__subscribtions = {}  # type: Dict[int: List[Dict]]
        self.__events = []

    def check_events(self):
        self.logger.debug("Start handling pygame events.")

        self.__events = pygame.event.get()
        for event in self.__events:
            self.logger.debug("Handle <%s>", event)
            self.on_event(event)

        self.logger.debug("Clear events.")
        self.__events = []

        self.logger.debug("End of handling pygame events.")

    def on_event(self, event):
        event_subscribtions = self.__subscribtions.get(event.type, [])

        for subscribtion in event_subscribtions:
            callback = subscribtion['callback']
            subtype = subscribtion['subtype']
            conditions = subscribtion['conditions']

            if self.__check_conditions(event, conditions) and self.__check_event_subtype(event, subtype):
                kwargs = self.__get_kwargs(event, subscribtion['kwargs'])
                callback(**kwargs)

    @classmethod
    def __check_conditions(cls, event, conditions):
        if not conditions:
            return True

        try:
            return all([cls.__check_condition(getattr(event, attr), value) for attr, value in conditions.items()])
        except AttributeError:
            cls.logger.debug("Check event <%s> conditions for <%s> not successfull.", event, conditions)
            return False

    @classmethod
    def __check_condition(cls, event_value, expected_value):
        if isinstance(expected_value, (list, tuple)):
            return event_value in expected_value
        else:
            return event_value == expected_value

    @classmethod
    def __check_event_subtype(cls, event, subtype):
        if subtype is None:
            return True

        try:
            return event.subtype == subtype
        except AttributeError:
            cls.logger.debug("Event <%s> is has no subtype of <%s>", event, subtype)
            return False

    @classmethod
    def __get_kwargs(cls, event, kwargs):
        if kwargs is None:
            return {}

        try:
            return {arg_name: getattr(event, arg_name) for arg_name in kwargs}
        except AttributeError:
            cls.logger.exception("Try get kwargs <%s> for callback, but event <%s> has no some attrs.", kwargs, event)
            raise

    @classmethod
    def dispatch(cls, event_type, **kwargs):
        cls.logger.debug("Dispatch <%s> with kwargs <%s>.", event_type, kwargs)

        event = pygame.event.Event(event_type, kwargs)
        pygame.event.post(event)

    def subscribe(
            self,
            event_type,
            callback,
            subtype: Optional[int] = None,
            conditions: Optional[dict] = None,
            kwargs: Optional[list] = None
    ):
        self.logger.debug("Subscribe callback <%s> on event_type <%s>.", callback, event_type)
        self.logger.debug("Conditions <%s>.", conditions)
        self.logger.debug("Kwargs <%s>.", kwargs)
        self.logger.debug("Subtype <%s>", subtype)

        subscribtion = {"callback": callback, "subtype": subtype, "conditions": conditions, "kwargs": kwargs}
        try:
            self.__subscribtions[event_type].append(subscribtion)
        except KeyError:
            self.__subscribtions[event_type] = [subscribtion, ]
