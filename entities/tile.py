from entities.entity import Entity
import pygame
import config
import globs


class Tile(Entity):
    """
    A tile of the map.
    """

    def __init__(self, tileX: int, tileY: int, surface: pygame.Surface, solid: bool = False) -> None:
        super().__init__(tileX * config.tileSize,
                         tileY * config.tileSize,
                         config.tileSize, config.tileSize)
        self._tileX = tileX
        self._tileY = tileY
        self._surface = surface
        self._solid = solid

        if self._surface.get_size() != (config.tileSize, config.tileSize):
            self._surface = pygame.transform.scale(self._surface, (config.tileSize, config.tileSize))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, self._rect.move(globs.cameraOffset))

    @property
    def x(self) -> int:
        # self._rect is already affected by cameraOffset
        return self._rect.move(globs.cameraOffset).x

    @property
    def y(self) -> int:
        # self._rect is already affected by cameraOffset
        return self._rect.move(globs.cameraOffset).y

    @property
    def rect(self) -> pygame.Rect:
        return self._rect.move(globs.cameraOffset)

    @property
    def literal_rect(self) -> pygame.Rect:
        return self._rect

    @property
    def tileX(self) -> int:
        return self._tileX

    @property
    def tileY(self) -> int:
        return self._tileY

    @property
    def solid(self) -> bool:
        return self._solid


class WallTile(Tile):
    def __init__(self, tileX: int, tileY: int) -> None:
        surface = pygame.Surface((config.tileSize, config.tileSize))
        surface.fill("#252525")

        super().__init__(tileX, tileY, surface, True)


class FloorTile(Tile):
    def __init__(self, tileX: int, tileY: int) -> None:
        surface = pygame.Surface((config.tileSize, config.tileSize))
        surface.fill("#111111")

        super().__init__(tileX, tileY, surface, False)
