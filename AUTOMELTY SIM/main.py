import pygame
from helper_classes.ControlledRobots import ControlledNormalBot
from helper_classes.ControlledRobots import ControlledMelty
from helper_classes.AutoMelty import AutoMelty
from helper_classes.Arena import Arena

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AutoMelty Sim")

clock = pygame.time.Clock()
running = True
arena = Arena(screen, 20)
robot = ControlledNormalBot(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, 100, 2000, pygame.Rect(500, 500, 100, 100), should_draw_heading=True)
auto_melty = AutoMelty(25, 1000, 1, True, 10,  pygame.Rect(100, 100, 100, 100), should_draw_heading=True, should_draw_desired_heading=True)
 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color(255, 255, 255))

    arena.draw(screen)

    robot.update(pygame.key.get_pressed())
    robot.draw(screen)

    auto_melty.update()
    auto_melty.draw(screen)

    pygame.display.update()

    
    delta_time = clock.tick(60)

pygame.quit()