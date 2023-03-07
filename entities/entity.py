from base import BaseElement
import pygame


class Entity(BaseElement):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._rect = pygame.Rect(x, y, width, height)

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def update(self) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value
        self._rect.x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value
        self._rect.y = value

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height