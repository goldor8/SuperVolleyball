import pygame
import Game as GameObject


class Window:
    main_window = None
    pygame.init()

    def __init__(self, title):
        if Window.main_window is not None:
            raise Exception("Window already exists")
        self.title = title
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.size = (self.screen.get_width(), self.screen.get_height())
        Window.main_window = self

        pygame.display.set_caption(self.title)

    def get_size(self):
        return self.size

    def draw_color(self, color):
        self.screen.fill(color)

    def draw_game_object(self, game_object: GameObject):
        game_object.draw(self)

    def draw_image(self, image, pos):
        self.screen.blit(image, pos)

    def draw_text(self, text, pos, color, size):
        font = pygame.font.SysFont("comicsansms", size)
        self.screen.blit(font.render(text, True, color), pos)

    def update(self):
        pygame.display.update()