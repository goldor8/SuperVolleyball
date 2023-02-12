import pygame
import Game as GameObject


class Window:
    pygame.init()
    __main_screen = None

    def __init__(self, title, width, height):
        if Window.__main_screen is not None:
            raise Exception("Window already exists")
        self.title = title
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        __main_window = self.screen

        pygame.display.set_caption(self.title)

    def draw_color(self, color):
        self.screen.fill(color)

    def draw_game_object(self, game_object: GameObject):
        game_object.draw(self)

    def draw_text(self, text, pos, color, size):
        font = pygame.font.SysFont("comicsansms", size)
        self.screen.blit(font.render(text, True, color), pos)

    def update(self):
        pygame.display.update()