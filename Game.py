import pygame
import Graphic
import Physics

timeStep = 1 / 60


class GameObject:
    def __init__(self, pos, size, image=None):
        self.pos = pos
        self.size = size
        self.image = image
        self.color = None

    def set_color(self, color):
        self.color = color

    def draw(self, window: Graphic.Window):
        if self.image is not None:
            window.screen.blit(self.image, (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2, self.size[0], self.size[1]))
        else:
            pygame.draw.rect(window.screen, self.color, (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2, self.size[0], self.size[1]))


class Body(GameObject):
    def __init__(self, pos, size, image=None):
        super().__init__(pos, size, image)
        self.dynamic_collider = Physics.DynamicCollider(self)
        self.static = False

    def set_static(self, static):
        self.static = static

    def set_collider(self, collider):
        self.dynamic_collider.collider = collider

    def get_collider(self):
        return self.dynamic_collider.collider

    def update(self):
        if not self.static:
            self.dynamic_collider.update()