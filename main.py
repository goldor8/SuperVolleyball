import pygame
import Game
import Graphic
import time

import Physics

running = True
is_on_game = False
frame = 0

if __name__ == "__main__":
    window = Graphic.Window("Test", 800, 800)
    start_program = time.time()
    pressed = {}
    play_button = pygame.image.load("resources/jouer.png")
    Game.set_objects()
    while running:
        start = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pressed[event.key] = True
                if is_on_game:
                    Game.event_keydown(event.key)
            elif event.type == pygame.KEYUP:
                pressed[event.key] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coord = pygame.mouse.get_pos()
                if 200 < coord[0] < 450 and 300 < coord[1] < 416 and not is_on_game:
                    is_on_game = True
                    Game.reset()
        # window.draw_text(str(Physics.get_circle_collider_penetration(body.get_collider(), thing.get_collider())), (0, 0), (255, 255, 255), 20)
        window.draw_color((0, 0, 0))
        if is_on_game:
            Game.update_game(window, pressed)
            if Game.detect_end():
                is_on_game = False
        else:
            window.screen.blit(play_button, (200, 300))
        window.update()
        frame_time = pygame.time.get_ticks() - start  # in milliseconds
        frame += 1
        if frame_time < int(Game.timeStep * 1000):
            pygame.time.delay(int(Game.timeStep * 1000) - frame_time)

    print("Program time: " + str(time.time() - start_program))
    print("Frame count: " + str(frame))
    print("FPS: " + str(frame / (time.time() - start_program)))
