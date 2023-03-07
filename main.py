import debug
import globs
import config
import pygame

from game import Game


class MainWindow:
    """The main window of the game"""
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(config.windowResolution)
        self.fps = config.windowFps
        self.clock = pygame.time.Clock()
        self.running = True

        self.game = Game()

        globs.mainWindow = self

        pygame.display.set_caption(config.windowTitle)

    def main_loop(self) -> None:
        while self.running:
            globs.deltaMs = self.clock.tick(self.fps)
            globs.deltaS = globs.deltaMs / 1000
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.game.handle_event(event)


    def update(self) -> None:
        pygame.display.set_caption(config.windowTitle + f" - FPS: {self.clock.get_fps():.2f} - DT: {globs.deltaMs:.2f}")

        self.game.update()

    def draw(self) -> None:
        self.window.fill((0, 0, 0))

        self.game.draw(self.window)

        debug.debugger.draw(self.window)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    window = MainWindow()
    window.main_loop()
    pygame.quit()
