import pygame as _pygame

windowWidth = 1920
windowHeight = 1080
windowResolution = (windowWidth, windowHeight)
windowRect = _pygame.Rect(0, 0, windowWidth, windowHeight)
windowFps = 165
windowTitle = "Farflawed - A game by Y9K"

tileSize = 128
chunkSize = 5  # in tiles

playerAcceleration = 0.003
playerMaxSpeed = 3
playerSize = 32
playerDeceleration = 0.98

controls = {
    "player": {
        "move": {
            "up": _pygame.K_w,
            "down": _pygame.K_s,
            "left": _pygame.K_a,
            "right": _pygame.K_d
        }
    }
}
