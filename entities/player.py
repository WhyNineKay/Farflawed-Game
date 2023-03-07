import globs
from entities.entity import Entity
import pygame
import config


class Player(Entity):
    def __init__(self) -> None:
        super().__init__(0, 0, config.playerSize, config.playerSize)

        self.x = config.windowRect.centerx - self.width / 2
        self.y = config.windowRect.centery - self.height / 2

        self._velocity = pygame.Vector2(0, 0)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, "#FF4000", self._rect)

    def update(self) -> None:
        self._controls()

        self._velocity.x *= config.playerDeceleration
        self._velocity.y *= config.playerDeceleration

        if self._velocity.x > config.playerMaxSpeed:
            self._velocity.x = config.playerMaxSpeed

        if self._velocity.x < -config.playerMaxSpeed:
            self._velocity.x = -config.playerMaxSpeed

        self._collision()

        globs.cameraOffset[0] -= self._velocity.x * globs.deltaMs
        globs.cameraOffset[1] -= self._velocity.y * globs.deltaMs

    def _controls(self) -> None:

        keys = pygame.key.get_pressed()

        if keys[config.controls["player"]["move"]["up"]]:
            self._velocity.y -= config.playerAcceleration * globs.deltaMs

        if keys[config.controls["player"]["move"]["down"]]:
            self._velocity.y += config.playerAcceleration * globs.deltaMs

        if keys[config.controls["player"]["move"]["left"]]:
            self._velocity.x -= config.playerAcceleration * globs.deltaMs

        if keys[config.controls["player"]["move"]["right"]]:
            self._velocity.x += config.playerAcceleration * globs.deltaMs

    def _collision(self) -> None:
        # get all the surrounding chunks. Depth of 1 means 9 chunks

        # player chunk
        playerChunk = globs.map.get_chunk_from_pos(self.x, self.y)

        # surrounding chunks (including player chunk)
        surroundingChunks = globs.map.get_surrounding_chunks(playerChunk, depth=1)

        # get all the tiles from the surrounding chunks
        tiles = []

        for chunk in surroundingChunks:
            tiles.extend(chunk.tiles)

        # check for collision
        for tile in tiles:
            if tile is None:
                continue

            if not tile.solid:
                continue

            futureRectX = self._rect.move(self._velocity.x * globs.deltaMs, 0)
            futureRectY = self._rect.move(0, self._velocity.y * globs.deltaMs)

            tileRect: pygame.Rect = tile.rect.copy()  # already affected by cameraOffset

            if futureRectX.colliderect(tileRect):
                self._velocity.x = 0

            if futureRectY.colliderect(tileRect):
                self._velocity.y = 0

    @property
    def velocity(self) -> pygame.Vector2:
        return self._velocity
