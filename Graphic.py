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
        """Return the size of the screen"""
        return self.size

    def draw_color(self, color):
        """Draw background color"""
        self.screen.fill(color)

    def draw_game_object(self, game_object: GameObject):
        """Draw a gameobject to the screen"""
        game_object.draw(self)

    def draw_image(self, image, pos):
        """Draw an image to the screen"""
        self.screen.blit(image, pos)

    def draw_text(self, text, pos, color, size):
        """Draw text on the screen"""
        font = pygame.font.SysFont("comicsansms", size)
        surface = font.render(text, True, color)
        self.screen.blit(surface, (pos[0] - surface.get_width() / 2, pos[1] - surface.get_height() / 2))

    def update(self):
        """Update the display"""
        pygame.display.update()