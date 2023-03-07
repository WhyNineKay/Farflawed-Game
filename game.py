from pathlib import Path

import globs
from base import BaseElement
from entities.player import Player
import pygame

from game_map import Tile, Map


class Game(BaseElement):
    def __init__(self) -> None:
        self._player = Player()
        self._entities = [
            # Add entities here
            self._player,
        ]

        self._map = Map()
        self._map.from_file(Path("maps/testmap.txt"))

        globs.map = self._map

    def update(self) -> None:
        for entity in self._entities:
            entity.update()

    def draw(self, surface: pygame.Surface) -> None:
        chunk = self._map.get_chunk_from_pos(self._player.x, self._player.y)

        if chunk is not None:
            chunks = self._map.get_surrounding_chunks(chunk, depth=2)
        else:
            chunks = []

        for chunk in chunks:
            chunk.draw(surface)

        for entity in self._entities:
            entity.draw(surface)

        self._map.debug_draw(surface)

    def handle_event(self, event: pygame.event.Event) -> None:
        for entity in self._entities:
            entity.handle_event(event)
