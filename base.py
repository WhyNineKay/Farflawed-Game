from abc import ABC, abstractmethod
import pygame


class BaseElement(ABC):
    def draw(self, surface: pygame.Surface) -> None:
        pass

    def update(self) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        pass
