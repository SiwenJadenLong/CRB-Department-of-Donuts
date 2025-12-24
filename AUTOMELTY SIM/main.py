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
robot = ControlledNormalBot(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, 10, 200, pygame.Rect(500, 500, 100, 100), should_draw_heading=True)
auto_melty = AutoMelty(4, 300, 1, False,  pygame.Rect(100, 100, 100, 100), should_draw_heading=True, should_draw_desired_heading=True)
 
#interesting observations
# it loves to false positively flag the far away corners/walls as the enemy robot because its sensor data is more sparse there, therefore it thinks
# there's a large change in distance when its just the fact that the arena is big 
# the counter to this ^ is having as many data point at as many angles as possible

while running:
    delta_time = clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                auto_melty.toggle_agro()

    screen.fill(pygame.Color(255, 255, 255))

    arena.draw(screen)

    robot.update(pygame.key.get_pressed(), delta_time)
    robot.draw(screen)

    auto_melty.update(delta_time)
    auto_melty.draw(screen)

    pygame.display.update()

pygame.quit()