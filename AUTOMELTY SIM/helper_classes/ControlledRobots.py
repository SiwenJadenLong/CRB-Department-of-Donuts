from helper_classes.Robot import Robot
import pygame
import math

class ControlledRobot(Robot):
    def __init__(self, FORWARD_KEY, BACKWARD_KEY, LEFT_KEY, RIGHT_KEY, accel, ang_accel, rect, color = pygame.Color(0, 0, 0), should_draw_heading=False):
        super().__init__(rect, color, should_draw_heading)
        self.FORWARD_KEY = FORWARD_KEY
        self.BACKWARD_KEY = BACKWARD_KEY
        self.LEFT_KEY = LEFT_KEY
        self.RIGHT_KEY = RIGHT_KEY
        self.accel = accel
        self.ang_accel = ang_accel

class ControlledMelty(ControlledRobot):
    def update(self, pressed_keys, delta_time):
        total_positional_accel = [0, 0]
        if pressed_keys[self.FORWARD_KEY]:
            total_positional_accel[1] -= self.accel

        if pressed_keys[self.BACKWARD_KEY]:
            total_positional_accel[1] += self.accel

        if pressed_keys[self.LEFT_KEY]:
            total_positional_accel[0] -= self.accel

        if pressed_keys[self.RIGHT_KEY]:
            total_positional_accel[0] += self.accel
        
        super().update(total_positional_accel, self.ang_accel, delta_time)

class ControlledNormalBot(ControlledRobot):
    def update(self, pressed_keys, delta_time):
        total_positional_accel = 0
        total_rotational_accel = 0
        if pressed_keys[self.FORWARD_KEY]:
            total_positional_accel += self.accel

        if pressed_keys[self.BACKWARD_KEY]:
            total_positional_accel -= self.accel

        if pressed_keys[self.LEFT_KEY]:
            total_rotational_accel += self.ang_accel

        if pressed_keys[self.RIGHT_KEY]:
            total_rotational_accel -= self.ang_accel
        
        total_positional_accel = [total_positional_accel * math.cos(math.radians(self.curr_heading)), total_positional_accel * -math.sin(math.radians(self.curr_heading))]
        super().update(total_positional_accel, total_rotational_accel, delta_time)