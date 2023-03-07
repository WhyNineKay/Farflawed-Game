"""
Game Map.
"""
import math
from pathlib import Path

import config
import globs
from entities.tile import Tile, WallTile, FloorTile
from base import BaseElement
import pygame


class Chunk(BaseElement):
    """
    A chunk of the map.
    Holds multiple tiles to form a chunk.
    """

    def __init__(self, chunkX: int, chunkY: int, tiles: list[Tile | None]) -> None:
        self._chunkX: int = chunkX
        self._chunkY: int = chunkY
        self._tiles: list[Tile | None] = tiles

    @property
    def chunkX(self) -> int:
        return self._chunkX

    @property
    def chunkY(self) -> int:
        return self._chunkY

    @property
    def tiles(self) -> list[Tile]:
        return self._tiles

    @property
    def rect(self) -> pygame.Rect:
        rect = pygame.Rect(
            self._chunkX * config.chunkSize * config.tileSize,
            self._chunkY * config.chunkSize * config.tileSize,
            config.chunkSize * config.tileSize,
            config.chunkSize * config.tileSize
        )

        return rect.move(globs.cameraOffset)

    def draw(self, surface: pygame.Surface) -> None:
        for tile in self._tiles:
            if tile is not None:
                tile.draw(surface)

    def debug_draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, "#FF0000", self.rect, 1)


class Map(BaseElement):
    """
    The game map.
    Holds multiple chunks to form the map.
    """

    def __init__(self) -> None:
        self._chunks: list[Chunk] = []
        self._tiles: list[Tile | None] = []
        self._tilesWidth: int = 0

    def from_file(self, filePath: Path) -> None:
        with open(filePath, "r") as file:
            data = file.read()

        lines = data.splitlines()

        tileMap = {
            "0": FloorTile,
            "1": WallTile,
        }

        lineExpectedLength = -1

        for y, line in enumerate(lines):
            line = line.strip()

            if lineExpectedLength == -1:
                lineExpectedLength = len(line)

            for x, char in enumerate(line):

                tileObj = tileMap.get(char)

                if tileObj is not None:
                    tile = tileObj(x, y)
                    self._tiles.append(tile)
                else:
                    self._tiles.append(None)

            if len(line) != lineExpectedLength:
                raise ValueError("Map file lines are not the same length.")

        self._tilesWidth = lineExpectedLength
        self._create_chunks()

    def draw(self, surface: pygame.Surface) -> None:
        # for tile in self._tiles:
        #     if tile is not None:
        #         tile.draw(surface)

        self._chunks[0].draw(surface)

    def get_tile(self, tileX: int, tileY: int) -> Tile | None:
        index = tileY * self._tilesWidth + tileX

        if index >= len(self._tiles):
            return None

        return self._tiles[index]

    def _create_chunks(self) -> None:
        chunksX = math.ceil(self._tilesWidth / config.chunkSize)
        chunksY = math.ceil(len(self._tiles) / self._tilesWidth / config.chunkSize)

        for chunkY in range(chunksY):
            for chunkX in range(chunksX):

                chunkTiles = []

                for tileY in range(config.chunkSize):
                    for tileX in range(config.chunkSize):
                        tile = self.get_tile(chunkX * config.chunkSize + tileX, chunkY * config.chunkSize + tileY)
                        chunkTiles.append(tile)

                self._chunks.append(Chunk(chunkX, chunkY, chunkTiles))

    def get_chunk_from_tile_pos(self, tileX: int, tileY: int) -> Chunk | None:
        chunkX = math.floor(tileX / config.chunkSize)
        chunkY = math.floor(tileY / config.chunkSize)

        for chunk in self._chunks:
            if chunk.chunkX == chunkX and chunk.chunkY == chunkY:
                return chunk

        return None

    def get_chunk_from_chunk_pos(self, chunkX: int, chunkY: int) -> Chunk | None:
        for chunk in self._chunks:
            if chunk.chunkX == chunkX and chunk.chunkY == chunkY:
                return chunk

        return None

    def get_chunk_from_pos(self, x: int, y: int) -> Chunk | None:
        # make sure to apply globs.cameraOffset to x and y
        tileX = math.floor((x - globs.cameraOffset.x) / config.tileSize)
        tileY = math.floor((y - globs.cameraOffset.y) / config.tileSize)

        return self.get_chunk_from_tile_pos(tileX, tileY)

    def get_surrounding_chunks(self, mainChunk: Chunk, depth: int = 1) -> list[Chunk]:
        chunks = []

        chunk = None

        for x in range(-depth, depth + 1):
            for y in range(-depth, depth + 1):
                chunk = self.get_chunk_from_chunk_pos(mainChunk.chunkX + x, mainChunk.chunkY + y)

                if chunk is not None:
                    chunks.append(chunk)

        return chunks

    def debug_draw(self, surface: pygame.Surface) -> None:
        for chunk in self._chunks:
            chunk.debug_draw(surface)