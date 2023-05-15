import asyncio
import random
from math import sqrt

import pygame

import Game
import Graphic
import Physics

timeStep = 1 / 150
all_objects = []
update_loop = []

def init_objects(screen_size):
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
    player1 = Player((screen_size[0] * 1 / 4, screen_size[1] / 2), (character_size, character_size),
                     pygame.transform.scale(pygame.image.load("resources/bonhomme.png"),
                                            (character_size, character_size)))
    player1.set_collider(Physics.CircleCollider(player1))
    player1.dynamic_collider.acceleration = player1.dynamic_collider.initial_acceleration = (0, 4000)
    player1.dynamic_collider.air_friction = 0.5
    player1.dynamic_collider.mass = 50
    player2 = Player((screen_size[0] * 3 / 4, screen_size[1] / 2), (character_size, character_size),
                     pygame.transform.scale(pygame.image.load("resources/bonhomme.png"),
                                            (character_size, character_size)))
    player2.set_collider(Physics.CircleCollider(player2))
    player2.dynamic_collider.acceleration = player2.dynamic_collider.initial_acceleration = (0, 4000)
    player2.dynamic_collider.air_friction = 0.5
    player2.dynamic_collider.mass = 50
    player2.is_player1 = False
    ball = Ball((random.randint(10, screen_size[0] - 10), screen_size[1] / 5), (66, 66),
                pygame.transform.scale(pygame.image.load("resources/ball.png"), (66, 66)))
    ball.set_color((255, 0, 0))
    ball.set_collider(Physics.CircleCollider(ball))
    ball.dynamic_collider.velocity = ball.dynamic_collider.initial_velocity = (400, 0)
    ball.dynamic_collider.acceleration = ball.dynamic_collider.initial_acceleration = (0, 1200)
    ball.dynamic_collider.bounciness = 1
    ball.dynamic_collider.mass = 1
    ball.set_static(True)
    ice_cube_power_up = IceCubePowerUp((random.randint(50, screen_size[0]-50), 55), (50, 50),
                                        pygame.transform.scale(pygame.image.load("resources/ice_cube.png"), (100, 100)),
                                        player1, player2)
    ice_cube_power_up.set_collider(Physics.CircleCollider(ice_cube_power_up))
    ice_cube_power_up.dynamic_collider.velocity = ice_cube_power_up.dynamic_collider.initial_velocity = (0, 0)
    ice_cube_power_up.dynamic_collider.acceleration = ice_cube_power_up.dynamic_collider.initial_acceleration = (0, 100)


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
    if key == pygame.K_UP and ground.get_collider() in player2.dynamic_collider.get_collisions():
        player2.jump(1600)


def register_update_loop(loop):
    update_loop.append(loop)


def unregister_update_loop(loop):
    update_loop.remove(loop)


def update(pressed):
    Physics.update(timeStep)
    for gameObject in all_objects:
        gameObject.update()
        if isinstance(gameObject, Player):
            gameObject.move(500, pressed)
    for loop in update_loop:
        loop()


def detect_end():
    ball = None
    ground = None
    for objects in all_objects:
        if isinstance(objects, Ball):
            ball = objects
        if objects.is_ground:
            ground = objects
    if ground.dynamic_collider.get_collider() in ball.dynamic_collider.get_collisions():
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
            window.screen.blit(self.image, (
            self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2, self.size[0], self.size[1]))
        else:
            pygame.draw.rect(window.screen, self.color, (
            self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2, self.size[0], self.size[1]))

    def update(self):
        self.draw()

    def delete(self):
        all_objects.remove(self)


class Body(GameObject):
    def __init__(self, pos, size, image=None):
        super().__init__(pos, size, image)
        self.dynamic_collider = Physics.DynamicCollider(self)
        self.is_ground = False

    def set_static(self, static):
        self.dynamic_collider.static = static

    def set_collider(self, collider):
        self.dynamic_collider.set_collider(collider)

    def get_collider(self):
        return self.dynamic_collider.collider

    def update(self):
        self.dynamic_collider.update()
        super().draw()

    def delete(self):
        super().delete()
        self.dynamic_collider.delete()


class Ball(Body):
    def __init__(self, pos, size, image):
        super().__init__(pos, size, image)
        self.max_speed = 1200

    def update(self):
        self.dynamic_collider.update()
        hypothenuse = sqrt(self.dynamic_collider.velocity[0] ** 2 + self.dynamic_collider.velocity[1] ** 2)
        if hypothenuse > self.max_speed:
            x = (self.dynamic_collider.velocity[0] / hypothenuse) * self.max_speed
            y = (self.dynamic_collider.velocity[1] / hypothenuse) * self.max_speed
            self.dynamic_collider.velocity = (x, y)
        self.draw()



class Player(Body):
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
                self.dynamic_collider.velocity = (0, self.dynamic_collider.velocity[1])
        else:
            if pressed.get(pygame.K_LEFT):
                self.dynamic_collider.velocity = (-speed, self.dynamic_collider.velocity[1])
            elif pressed.get(pygame.K_RIGHT):
                self.dynamic_collider.velocity = (speed, self.dynamic_collider.velocity[1])
            else:
                self.dynamic_collider.velocity = (0, self.dynamic_collider.velocity[1])

    def jump(self, speed):
        self.dynamic_collider.velocity = (self.dynamic_collider.velocity[0], -speed)


class PowerUp(Body):
    def __init__(self, pos, size, image):
        super().__init__(pos, size, image)
        self.dynamic_collider = Physics.DynamicCollider(self)
        self.dynamic_collider.collider = Physics.CircleCollider(self)

    def power_trigger(self, player):
        pass

    def update(self):
        super().update()
        if(len(self.dynamic_collider.get_collisions()) > 1):
            pass
        for collider in self.dynamic_collider.get_collisions():
            if isinstance(collider.game_object, Player):
                self.power_trigger(collider.game_object)
                break


class BoxingGlovePowerUp(PowerUp):
    def __init__(self, pos, size):
        super().__init__(pos, size, pygame.image.load("resources/boxing_glove.png"))

    def power_trigger(self, player):
        player.dynamic_collider.register_on_collision(self.punch)
        self.delete()

    def punch(self, player, colliders):
        for collider in colliders:
            if isinstance(collider.game_object, Ball):
                collider.game_object.dynamic_collider.velocity = (collider.game_object.dynamic_collider.velocity[0] * 4, collider.game_object.dynamic_collider.velocity[1] * 4)
                collider.game_object.max_speed = 2400
                #collider.game_object.dynamic_collider.register_on_collision(self.reset_ball_speed(collider.game_object, 1200))
                self.reset_speed_smoothly(collider.game_object, 1200, 1.5)
                player.dynamic_collider.unregister_on_collision(self.punch)
                break

    def reset_ball_speed(self, ball, speed):
        def reset_speed(player, colliders):
            ball.max_speed = speed
            ball.dynamic_collider.unregister_on_collision(reset_speed)

        return reset_speed

    def reset_speed_smoothly(self, ball, speed, time):
        def loop():
            steps = time / Game.timeStep
            if ball.max_speed > speed:
                ball.max_speed -= (ball.max_speed - speed)/steps
                return
            ball.max_speed = speed
            unregister_update_loop(loop)

        # loop = asyncio.get_event_loop()
        # loop.run_in_executor(None, loop)
        register_update_loop(loop)


class IceCubePowerUp(PowerUp):
    def __init__(self, pos, size, image, player1, player2):
        super().__init__(pos, size, image)
        self.player1 = player1
        self.player2 = player2

    def power_trigger(self, player):
        if player == self.player1:
            self.freeze_player(self.player2)
        else:
            self.freeze_player(self.player1)
        self.delete()

    def freeze_player(self, player):
        player.image = pygame.transform.scale(pygame.image.load("resources/bonhomme_freeze.png"), (200, 200))
        player.set_static(True)

    def unfreeze(self, player):
        player.image = pygame.transform.scale(pygame.image.load("resources/bonhomme.png"), player.size)
        player.set_static(False)


class ReversePowerUp(PowerUp):
    def __init__(self, pos, size, image):
        super().__init__(pos, size, image)

    def power_trigger(self, player):
        pass


class StopPowerUp(PowerUp):
    def __init__(self, pos, size, image):
        super().__init__(pos, size, image)

    def power_trigger(self, player):
        pass


class TwoBallsPowerUp(PowerUp):
    def __init__(self, pos, size, image):
        super().__init__(pos, size, image)

    def power_trigger(self, player):
        pass
