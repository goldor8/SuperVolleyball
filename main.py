import pygame
import Game
import Graphic
import time

running = True
is_on_game = False
frame = 0
pressed = {}
background = pygame.image.load("resources/background.jpg")
play_button = pygame.image.load("resources/jouer.png")

def is_mouse_on_rect(mouse_pos, rect):
    """Return True if the mouse is on the rect"""
    return rect.collidepoint(mouse_pos)

if __name__ == "__main__":
    window = Graphic.Window("Test")
    start_program = time.time()

    background = pygame.transform.scale(background, window.get_size())
    while running:
        start = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coord = pygame.mouse.get_pos()
                if 200 < coord[0] < 450 and 300 < coord[1] < 416 and not is_on_game:
                    is_on_game = True
                    Game.reset()
                    Game.init_game(window)
        window.draw_image(background, (0, 0))
        if is_on_game:
            Game.update()
            if Game.ended:
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