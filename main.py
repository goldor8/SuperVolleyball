import pygame
import Game
import Graphic
import time

import Physics

running = True
frame = 0

if __name__ == "__main__":
    window = Graphic.Window("Test", 800, 800)
    body = Game.Body((100, 210), (100, 100), pygame.image.load("resources/circle.png"))
    body.set_color((255, 0, 0))
    body.set_collider(Physics.CircleCollider(body))
    body.dynamic_collider.velocity = (1000, 0)
    body.dynamic_collider.acceleration = (0, 300)
    body.dynamic_collider.bounciness = 1
    body2 = Game.Body((500, 210), (100, 100), pygame.image.load("resources/circle.png"))
    body2.set_color((255, 0, 0))
    body2.set_collider(Physics.CircleCollider(body2))
    body2.dynamic_collider.velocity = (-1000, 0)
    body2.dynamic_collider.acceleration = (0, 300)
    body2.dynamic_collider.bounciness = 1

    wall1 = Game.Body((400, 0), (800, 10))
    wall1.set_collider(Physics.BoxCollider(wall1))
    wall1.set_static(True)
    wall1.set_color((0, 0, 255))
    wall2 = Game.Body((0, 400), (10, 800))
    wall2.set_collider(Physics.BoxCollider(wall2))
    wall2.set_static(True)
    wall2.set_color((0, 0, 255))
    ground = Game.Body((400, 800), (800, 10))
    ground.set_collider(Physics.BoxCollider(ground))
    ground.set_static(True)
    ground.set_color((0, 0, 255))
    wall4 = Game.Body((800, 400), (10, 800))
    wall4.set_collider(Physics.BoxCollider(wall4))
    wall4.set_static(True)
    wall4.set_color((0, 0, 255))
    player1 = Game.Player((100, 630), (154, 303), pygame.image.load("resources/Bonhomme.png"))
    player1.set_collider(Physics.BoxCollider(player1))
    player1.dynamic_collider.acceleration = (0, 4000)
    player1.dynamic_collider.air_friction = 0.5
    player1.dynamic_collider.mass = 100
    player2 = Game.Player((700, 630), (154, 303), pygame.image.load("resources/Bonhomme2.png"))
    player2.set_collider(Physics.BoxCollider(player2))
    player2.dynamic_collider.mass = 100
    start_program = time.time()
    pressed = {}
    while running:
        start = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pressed[event.key] = True
                if event.key == pygame.K_SPACE and ground.get_collider() in player1.dynamic_collider.get_collisions():
                    player1.jump(1600)
            elif event.type == pygame.KEYUP:
                player1.dynamic_collider.velocity = (0, player1.dynamic_collider.velocity[1])
                pressed[event.key] = False
        window.draw_color((0, 0, 0))
        body.update()
        body2.update()
        player1.move(500, pressed)
        player1.update()
        window.draw_game_object(player1)
        player2.move(500, pressed, 0)
        player2.update()
        window.draw_game_object(player2)
        window.draw_game_object(body)
        window.draw_game_object(body2)
        window.draw_game_object(wall1)
        window.draw_game_object(wall2)
        window.draw_game_object(ground)
        window.draw_game_object(wall4)
        #window.draw_text(str(Physics.get_circle_collider_penetration(body.get_collider(), thing.get_collider())), (0, 0), (255, 255, 255), 20)
        window.update()
        frame_time = pygame.time.get_ticks() - start # in milliseconds
        frame += 1
        if frame_time < int(Game.timeStep * 1000):
            pygame.time.delay(int(Game.timeStep * 1000) - frame_time)

    print("Program time: " + str(time.time() - start_program))
    print("Frame count: " + str(frame))
    print("FPS: " + str(frame / (time.time() - start_program)))
