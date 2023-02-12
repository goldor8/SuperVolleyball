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
    body.dynamic_collider.acceleration = (0, 0)
    body.dynamic_collider.air_friction = 0.0
    body.dynamic_collider.bounciness = 1
    body.dynamic_collider.ground_friction = 0
    thing = Game.Body((300, 280), (100, 100), pygame.image.load("resources/circle.png"))
    thing.set_collider(Physics.CircleCollider(thing))
    thing.set_color((0, 255, 0))
    thing.set_static(True)
    wall1 = Game.Body((400, 0), (800, 10))
    wall1.set_collider(Physics.BoxCollider(wall1))
    wall1.set_static(True)
    wall1.set_color((0, 0, 255))
    wall2 = Game.Body((0, 400), (10, 800))
    wall2.set_collider(Physics.BoxCollider(wall2))
    wall2.set_static(True)
    wall2.set_color((0, 0, 255))
    wall3 = Game.Body((400, 800), (800, 10))
    wall3.set_collider(Physics.BoxCollider(wall3))
    wall3.set_static(True)
    wall3.set_color((0, 0, 255))
    wall4 = Game.Body((800, 400), (10, 800))
    wall4.set_collider(Physics.BoxCollider(wall4))
    wall4.set_static(True)
    wall4.set_color((0, 0, 255))
    start_program = time.time()
    while running:
        start = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        window.draw_color((0, 0, 0))
        body.update()
        window.draw_game_object(body)
        window.draw_game_object(thing)
        window.draw_game_object(wall1)
        window.draw_game_object(wall2)
        window.draw_game_object(wall3)
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
