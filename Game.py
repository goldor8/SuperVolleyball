import random
from math import sqrt

import pygame
import Graphic
import Physics

timeStep = 1 / 200
all_objects = []


def init_objects(screen_size):
    ball = Ball((random.randint(10, screen_size[0] - 10), screen_size[1] / 5), (66, 66), pygame.transform.scale(pygame.image.load("resources/ball.png"), (66, 66)))
    ball.set_color((255, 0, 0))
    ball.set_collider(Physics.CircleCollider(ball))
    ball.dynamic_collider.velocity = ball.dynamic_collider.initial_velocity = (400, 0)
    ball.dynamic_collider.acceleration = ball.dynamic_collider.initial_acceleration = (0, 800)
    ball.dynamic_collider.bounciness = 0.9
    ball.dynamic_collider.mass = 1
    wall1 = Body((screen_size[0] / 2, 0), (screen_size[0], 10))
    wall1.set_collider(Physics.BoxCollider(wall1))
    wall1.set_static(True)
    wall1.set_color((0, 0, 255))
    wall2 = Body((0, screen_size[1] / 2), (10, screen_size[1]))
    wall2.set_collider(Physics.BoxCollider(wall2))
    wall2.set_static(True)
    wall2.set_color((0, 0, 255))
    ground = Body((screen_size[0] / 2, screen_size[1]), (screen_size[0], 10))
    ground.set_collider(Physics.BoxCollider(ground))
    ground.set_static(True)
    ground.set_color((0, 0, 255))
    ground.is_ground = True
    wall4 = Body((screen_size[0], screen_size[1] / 2), (10, screen_size[1]))
    wall4.set_collider(Physics.BoxCollider(wall4))
    wall4.set_static(True)
    wall4.set_color((0, 0, 255))
    net = Body((screen_size[0] / 2, screen_size[1] * 5 / 6), (10, screen_size[1] / 3))
    net.set_collider(Physics.BoxCollider(net))
    net.set_static(True)
    net.set_color((0, 0, 255))
    character_size = 150
    player1 = Player((screen_size[0] * 1 / 4, screen_size[1] / 2), (character_size, character_size), pygame.transform.scale(pygame.image.load("resources/bonhomme.png"), (character_size, character_size)))
    player1.set_collider(Physics.CircleCollider(player1))
    player1.dynamic_collider.acceleration = player1.dynamic_collider.initial_acceleration = (0, 4000)
    player1.dynamic_collider.air_friction = 0.5
    player1.dynamic_collider.mass = 50
    player2 = Player((screen_size[0] * 3 / 4, screen_size[1] / 2), (character_size, character_size), pygame.transform.scale(pygame.image.load("resources/bonhomme.png"), (character_size, character_size)))
    player2.set_collider(Physics.CircleCollider(player2))
    player2.dynamic_collider.acceleration = player2.dynamic_collider.initial_acceleration = (0, 4000)
    player2.dynamic_collider.air_friction = 0.5
    player2.dynamic_collider.mass = 50
    player2.is_player1 = False


def event_keydown(key):
    ground = None
    player1 = None
    player2 = None
    for objects in all_objects:
        if objects.is_ground:
            ground = objects
        if isinstance(objects, Player):
            if objects.is_player1:
                player1 = objects
            else:
                player2 = objects
    if key == pygame.K_SPACE and ground.get_collider() in player1.dynamic_collider.get_collisions():
        player1.jump(1600)
    elif key == pygame.K_UP and ground.get_collider() in player2.dynamic_collider.get_collisions():
        player2.jump(1600)


def update(pressed):
    for gameObject in all_objects:
        gameObject.update()
        if isinstance(gameObject, Player):
            gameObject.move(500, pressed)


def detect_end():
    ball = None
    ground = None
    for objects in all_objects:
        if isinstance(objects, Ball):
            ball = objects
        if objects.is_ground:
            ground = objects
    if ground.dynamic_collider.get_colliders() in ball.dynamic_collider.get_collisions():
        return True
    return False


def reset(size):
    Physics.reset()
    all_objects.clear()
    init_objects(size)


class GameObject:
    def __init__(self, pos, size, image=None):
        all_objects.append(self)
        self.initial_pos = pos
        self.pos = pos
        self.size = size
        self.image = image
        self.color = None

    def set_color(self, color):
        self.color = color

    def draw(self):
        window = Graphic.Window.main_window
        if self.image is not None:
            window.screen.blit(self.image, (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2, self.size[0], self.size[1]))
        else:
            pygame.draw.rect(window.screen, self.color, (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2, self.size[0], self.size[1]))

    def update(self):
        self.draw()


class Body(GameObject):
    def __init__(self, pos, size, image=None):
        super().__init__(pos, size, image)
        self.dynamic_collider = Physics.DynamicCollider(self)
        self.is_ground = False

    def set_static(self, static):
        self.dynamic_collider.static = static

    def set_collider(self, collider):
        self.dynamic_collider.collider = collider

    def get_collider(self):
        return self.dynamic_collider.collider

    def update(self):
        self.dynamic_collider.update()
        super().draw()


class Ball(Body):
    def __init__(self, pos, size, image):
        super().__init__(pos, size, image)

    def update(self):
        self.dynamic_collider.update()
        hypothenuse = sqrt(self.dynamic_collider.velocity[0]**2 + self.dynamic_collider.velocity[1]**2)
        max_velo = 1200
        if hypothenuse > max_velo:
            x = (self.dynamic_collider.velocity[0]/hypothenuse) * max_velo
            y = (self.dynamic_collider.velocity[1] / hypothenuse) * max_velo
            self.dynamic_collider.velocity = (x, y)
        self.draw()


class Player (Body):
    def __init__(self, pos, size, image):
        super().__init__(pos, size, image)
        self.is_player1 = True

    def move(self, speed, pressed):
        if self.is_player1:
            if pressed.get(pygame.K_q):
                self.dynamic_collider.velocity = (-speed, self.dynamic_collider.velocity[1])
            elif pressed.get(pygame.K_d):
                self.dynamic_collider.velocity = (speed, self.dynamic_collider.velocity[1])
        else:
            if pressed.get(pygame.K_LEFT):
                self.dynamic_collider.velocity = (-speed, self.dynamic_collider.velocity[1])
            elif pressed.get(pygame.K_RIGHT):
                self.dynamic_collider.velocity = (speed, self.dynamic_collider.velocity[1])

    def jump(self, speed):
        self.dynamic_collider.velocity = (self.dynamic_collider.velocity[0], -speed)
