import pygame
import math

class Robot:
    HEADING_LINE_LENGTH = 100
    ANG_ACCEL_REDUCTION = 1000000
    ACCEL_REDUCTION = 100
    VEL_LOSS = 0.9
    ANG_VEL_LOSS = 0.9
    robots = []
    def __init__(self, rect, color = pygame.Color(0, 0, 0), should_draw_heading=False):
        self.rect = rect
        self.color = color
        self.should_draw_heading = should_draw_heading
        self.curr_heading = 0
        self.vel = [0, 0]
        self.ang_vel = 0
        Robot.robots.append(self)

    def draw(self, surface):
        robot_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(robot_surface, self.color, pygame.Rect(0, 0, *self.rect.size))
        robot_surface = pygame.transform.rotate(robot_surface, self.curr_heading)
        rotated_robot = robot_surface.get_rect(center=self.rect.center)
        surface.blit(robot_surface, rotated_robot)

        if self.should_draw_heading:
           self.draw_line_at_angle(surface, self.curr_heading, Robot.HEADING_LINE_LENGTH)

    def draw_line_at_angle(self, surface, angle, length, color = pygame.Color(255, 0, 0)):
        line_end_pos = (self.rect.center[0] + length * math.cos(math.radians(angle)),
                        self.rect.center[1] + length * -math.sin(math.radians(angle)))
        pygame.draw.line(surface, color, self.rect.center, line_end_pos, 5)

    def update(self, accel, angular_accel):
        self.vel[0] += accel[0] / Robot.ACCEL_REDUCTION
        self.vel[1] += accel[1] / Robot.ACCEL_REDUCTION
        self.rect.center = (self.rect.center[0] + self.vel[0], self.rect.center[1] + self.vel[1])
        self.vel[0] *= Robot.VEL_LOSS
        self.vel[1] *= Robot.VEL_LOSS

        self.ang_vel += angular_accel / Robot.ANG_ACCEL_REDUCTION
        self.ang_vel *= Robot.ANG_VEL_LOSS
        
        self.curr_heading = (self.curr_heading + 360 * self.ang_vel) % 360
