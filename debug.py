from typing import Dict

import pygame

from base import BaseElement
import buttonup


class _Debug(BaseElement):
    def __init__(self) -> None:
        self._debugs: Dict[str, buttonup.label.DefaultLabel] = {}
        self._y = 20
        self._x = 20
        self._text_size = 20
        self._enabled = True

    def __call__(self, *args, **kwargs) -> None:
        self.debug(*args, **kwargs)

    def debug(self, debugId: str, value: str) -> None:
        if debugId not in self._debugs:
            # create a new debug
            self._debugs[debugId] = buttonup.label.DefaultLabel(
                pos_x=self._x,
                pos_y=int(self._y + len(self._debugs) * self._text_size * 1.2),
                text=f"{value}",
                text_size=self._text_size)
        else:
            # update the debug
            self._debugs[debugId].text = f"{value}"

    def draw(self, surface: pygame.Surface) -> None:
        if self._enabled:
            for debug in self._debugs.values():
                debug.draw(surface)

    def update(self) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def toggle(self) -> None:
        self._enabled = not self._enabled

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value


debugger = _Debug()
