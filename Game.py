import random
from math import sqrt

import pygame

import Game
import Graphic
import Physics

timeStep = 1 / 150
max_score = 11
all_objects = []
update_loop = []
game_window = None
ended = False

def init_game(window: Graphic.Window):
    """Initialize the game"""
    global game_window, ended
    ended = False
    game_window = window
    init_objects(window.get_size())

def init_objects(screen_size):
    """Initialize the objects"""
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
    ground.add_tag("ground")
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
    # ball.set_static(True)
    ice_cube_power_up = IceCubePowerUp((random.randint(50, screen_size[0]-50), 55), (50, 50), player1, player2)
    ice_cube_power_up.dynamic_collider.velocity = ice_cube_power_up.dynamic_collider.initial_velocity = (0, 0)
    ice_cube_power_up.dynamic_collider.acceleration = ice_cube_power_up.dynamic_collider.initial_acceleration = (0, 300)
    # boxing_glove = BoxingGlovePowerUp((100,100), (100, 100))
    # boxing_glove.dynamic_collider.acceleration = (0, 300)
    gameplay_loop(player1, player2, ball, ground)


def register_update_loop(loop):
    """Register a loop to be called every frame"""
    update_loop.append(loop)


def unregister_update_loop(loop):
    """Unregister a loop"""
    update_loop.remove(loop)


def update():
    """Update the game"""
    Physics.update(timeStep)
    for gameObject in all_objects:
        gameObject.update()
    for loop in update_loop:
        loop()


def gameplay_loop(player1, player2, ball, ground):
    """The main gameplay loop"""
    player1Score = 0
    player2Score = 0
    screen_size = game_window.get_size()
    spawn_ball(ball, screen_size)

    def loop():
        nonlocal player1Score
        nonlocal player2Score
        if ball.dynamic_collider.get_collider() in ground.dynamic_collider.get_collisions():
            if ball.pos[0] < screen_size[0] / 2:
                player2Score += 1
            else:
                player1Score += 1
            if player1Score == max_score or player2Score == max_score:
                unregister_update_loop(loop)
                show_text("Player " + str(1 if player1Score == max_score else 2) + " wins !", (screen_size[0] / 2, screen_size[1] / 2), (255, 255, 255), 50, 3)
                delay(stop_game, 3)
                return
            spawn_ball(ball, screen_size)


        game_window.draw_text(str(player1Score), (screen_size[0] / 4, 50), (255, 255, 255), 50)
        game_window.draw_text(str(player2Score), (screen_size[0] * 3 / 4, 50), (255, 255, 255), 50)

    register_update_loop(loop)


def show_text(text, pos, color, size, time):
    """Show a text for a certain amount of time"""
    def loop():
        game_window.draw_text(text, pos, color, size)

    register_update_loop(loop)
    delay(lambda: unregister_update_loop(loop), time)


def spawn_ball(ball, screen_size):
    """Spawn the ball in the middle of the screen and launch it in a random direction"""
    ball.pos = (screen_size[0] / 2, screen_size[1] / 4)
    ball.dynamic_collider.velocity = (random.choice([-1, 1]) * 500, -500)
    ball.dynamic_collider.acceleration = ball.dynamic_collider.initial_acceleration
    ball.dynamic_collider.static = True
    textPos = (screen_size[0] / 2, screen_size[1] / 2)
    textColor = (255, 255, 255)
    show_text("3", textPos, textColor, 50, 1)
    delay(lambda: show_text("2", textPos, textColor, 50, 1), 1)
    delay(lambda: show_text("1", textPos, textColor, 50, 1), 2)
    delay(lambda: show_text("GO !", textPos, textColor, 50, 0.5), 3)

    def start():
        ball.dynamic_collider.static = False

    delay(start, 3)


def stop_game():
    """Stop the game"""
    global ended
    ended = True


def delay(function, time):
    """Call a function after a certain amount of time"""
    def waitLoop():
        nonlocal time
        time -= timeStep
        if time <= 0:
            unregister_update_loop(waitLoop)
            function()

    register_update_loop(waitLoop)

def reset():
    """Reset the game"""
    Physics.reset()
    all_objects.clear()


class GameObject:
    def __init__(self, pos, size, image=None):
        all_objects.append(self)
        self.initial_pos = pos
        self.pos = pos
        self.size = size
        self.image = image
        self.color = None
        self.tags = []

    def set_color(self, color):
        """Set the color of the object"""
        self.color = color

    def draw(self):
        """Draw the object on the screen"""
        window = Graphic.Window.main_window
        if self.image is not None:
            window.screen.blit(self.image, (
            self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2, self.size[0], self.size[1]))
        else:
            pygame.draw.rect(window.screen, self.color, (
            self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2, self.size[0], self.size[1]))

    def update(self):
        """Called every frame"""
        self.draw()

    def add_tag(self, tag):
        """Add a tag to the object"""
        self.tags.append(tag)

    def remove_tag(self, tag):
        """Remove a tag from the object"""
        self.tags.remove(tag)

    def delete(self):
        """Delete the object"""
        all_objects.remove(self)


class Body(GameObject):
    def __init__(self, pos, size, image=None):
        super().__init__(pos, size, image)
        self.dynamic_collider = Physics.DynamicCollider(self)

    def set_static(self, static):
        """Set the object as static or not (static objects don't move)"""
        self.dynamic_collider.static = static

    def set_collider(self, collider):
        """Set the collider of the object"""
        self.dynamic_collider.set_collider(collider)

    def get_collider(self):
        """Get the collider of the object"""
        return self.dynamic_collider.collider

    def update(self):
        """Called every frame"""
        self.dynamic_collider.update()
        super().draw()

    def delete(self):
        """Delete the object"""
        super().delete()
        self.dynamic_collider.delete()


class Ball(Body):
    def __init__(self, pos, size, image):
        super().__init__(pos, size, image)
        self.max_speed = 1200

    def update(self):
        """Called every frame"""
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

    def move(self, speed):
        """Move the player"""
        pressed = pygame.key.get_pressed()
        if self.is_player1:
            if pressed[pygame.K_q]:
                self.dynamic_collider.velocity = (-speed, self.dynamic_collider.velocity[1])
            elif pressed[pygame.K_d]:
                self.dynamic_collider.velocity = (speed, self.dynamic_collider.velocity[1])
            else:
                self.dynamic_collider.velocity = (0, self.dynamic_collider.velocity[1])
        else:
            if pressed[pygame.K_LEFT]:
                self.dynamic_collider.velocity = (-speed, self.dynamic_collider.velocity[1])
            elif pressed[pygame.K_RIGHT]:
                self.dynamic_collider.velocity = (speed, self.dynamic_collider.velocity[1])
            else:
                self.dynamic_collider.velocity = (0, self.dynamic_collider.velocity[1])

    def jump(self, speed):
        """Make the player jump"""
        isCollidingGround = False
        for collider in self.dynamic_collider.get_collisions():
            for tag in collider.game_object.tags:
                if tag == "ground":
                    isCollidingGround = True
        if not isCollidingGround:
            return

        pressed = pygame.key.get_pressed()
        if self.is_player1:
            if pressed[pygame.K_z]:
                self.dynamic_collider.velocity = (self.dynamic_collider.velocity[0], -speed)
        else:
            if pressed[pygame.K_UP]:
                self.dynamic_collider.velocity = (self.dynamic_collider.velocity[0], -speed)

    def update(self):
        """Called every frame"""
        super().update()
        self.move(500)
        self.jump(1600)


class PowerUp(Body):
    def __init__(self, pos, size, image):
        super().__init__(pos, size, image)
        self.dynamic_collider = Physics.DynamicCollider(self)
        self.dynamic_collider.collider = Physics.CircleCollider(self)

    def power_trigger(self, player):
        """Called when the player takes the power up"""
        pass

    def update(self):
        """Called every frame"""
        super().update()
        if(len(self.dynamic_collider.get_collisions()) > 1):
            pass
        for collider in self.dynamic_collider.get_collisions():
            if isinstance(collider.game_object, Player):
                self.power_trigger(collider.game_object)
                break


class BoxingGlovePowerUp(PowerUp):
    def __init__(self, pos, size):
        super().__init__(pos, size, pygame.transform.scale(pygame.image.load("resources/boxing_glove.png"), size))

    def power_trigger(self, player):
        """Called when the player takes the power up"""
        player.dynamic_collider.register_on_collision(self.punch)
        self.delete()

    def punch(self, player, colliders):
        """Called when the player collide the ball"""
        for collider in colliders:
            if isinstance(collider.game_object, Ball):
                collider.game_object.dynamic_collider.velocity = (collider.game_object.dynamic_collider.velocity[0] * 4, collider.game_object.dynamic_collider.velocity[1] * 4)
                collider.game_object.max_speed = 2400
                #collider.game_object.dynamic_collider.register_on_collision(self.reset_ball_speed(collider.game_object, 1200))
                self.reset_speed_smoothly(collider.game_object, 1200, 1.5)
                player.dynamic_collider.unregister_on_collision(self.punch)
                break

    def reset_ball_speed(self, ball, speed):
        """Called when the ball collide the ground"""
        def reset_speed(player, colliders):
            ball.max_speed = speed
            ball.dynamic_collider.unregister_on_collision(reset_speed)

        return reset_speed

    def reset_speed_smoothly(self, ball, speed, time):
        """Reset the ball speed smoothly"""
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
    def __init__(self, pos, size, player1, player2):
        image = pygame.transform.scale(pygame.image.load("resources/ice_cube.png"), (100, 100))
        super().__init__(pos, size, image)
        self.player1 = player1
        self.player2 = player2

    def power_trigger(self, player):
        """Called when the player takes the power up"""
        if player == self.player1:
            self.freeze_player(self.player2)
        else:
            self.freeze_player(self.player1)
        self.delete()

    def freeze_player(self, player):
        """Freeze the player for 1 second"""
        player.image = pygame.transform.scale(pygame.image.load("resources/bonhomme_freeze.png"), (200, 200))
        player.set_static(True)
        delay(lambda: self.unfreeze(player), 1)

    def unfreeze(self, player):
        """Unfreeze the player"""
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
