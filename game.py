from pathlib import Path

import globs
from base import BaseElement
from debug import debugger
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

        debugger.debug("playerVel",
                       f"playervel: {self._player.velocity.x:.2f}, {self._player.velocity.y:.2f}")

        debugger.debug("cameraOffset",
                       f"cameraOffset: {globs.cameraOffset[0]:.2f}, {globs.cameraOffset[1]:.2f}"
                       )

        debugger.debug("deltaTime",
                       f"deltaMs/deltaS: {globs.deltaMs:.2f}, {globs.deltaS:.5f}"
                       )

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                debugger.toggle()
