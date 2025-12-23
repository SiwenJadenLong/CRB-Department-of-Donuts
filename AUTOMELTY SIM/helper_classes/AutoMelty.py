from helper_classes.Robot import Robot
import pygame
import math

class AutoMelty(Robot):
    def __init__(self, accel, ang_accel, poll_resolution, agro, delta_distance_threshold, rect, color = pygame.Color(0, 0, 0), should_draw_heading=False, should_draw_desired_heading=False):
        super().__init__(rect, color, should_draw_heading)
        self.should_draw_desired_heading = should_draw_desired_heading
        self.accel = accel
        self.ang_accel = ang_accel
        self.poll_resolution = poll_resolution
        self.agro = agro
        self.delta_distance_threshold = delta_distance_threshold
        self.desired_direction = 0
        self.poll_count = 0
        self.atd = [] #angle to distance | degrees, distance (D) in meters 
        self.atdd = [] #angle to delta distance | degrees, change in distance with respect to angle (avg rate of change)
        self.atwad = [] #angle to weighted delta distance | degrees, average distances

    def populate_angle_to_delta_distance(self):
        for i in range(len(self.atd)-1):
            self.atdd.append(
                (self.atd[i-1][1] - self.atd[i+1][1])
                /
                (self.atd[i-1][0] - self.atd[i+1][0])
            )
        self.atdd.append(
            (self.atd[-2][1] - self.atd[0][1])
            /
            (self.atd[-2][0] - self.atd[0][0])
        )

    def find_opponent(self):
        opponent_list = []
        current_section = []
        for dd in zip(map(lambda s: s[0], self.atd), self.atdd):
            if dd[1] > self.delta_distance_threshold and current_section:
                opponent_list.append(current_section)
                current_section = []
            
            current_section.append(dd)

        if current_section:
            opponent_list.append(current_section)

        opponent_list.remove(max(opponent_list, key=len))
        shortened_list = list(reversed(opponent_list[0]))
        if len(opponent_list) > 1:
            shortened_list += opponent_list[1]
        
        self.desired_direction = shortened_list[len(shortened_list)//2][0]

    def populate_angle_to_weighted_average_distance(self):
        for i in range(len(self.atd)):
            for j in range(len(self.atd)):
                self.atwad.append(sum(map(lambda s: (1 / max(0.1,abs(i-j))) * self.atd[j], self.atd)))

    def get_distance(self):
        other_robot = [robot for robot in Robot.robots if robot is not self][0]
        for d in range(800):
            pos = [d * math.cos(math.radians(self.curr_heading)), d * -math.sin(math.radians(self.curr_heading))]
            if other_robot.rect.colliderect(pygame.Rect(pos[0], pos[1], 1, 1)):
                return d
        return d

    def update_desired_direction(self):
        if self.agro:
            self.populate_angle_to_delta_distance()
            self.find_opponent()
        else:
            self.populate_angle_to_weighted_average_distance()
            max_weighted_average_distance_index = max(range(len(self.atd)), key=lambda i: self.atwad[i])
            self.desired_direction = self.atd[max_weighted_average_distance_index][0]
        self.atd = []
        self.atdd = []
        self.atwad = []

    def update(self):
        self.poll_count += 1
        self.poll_count %= self.poll_resolution

        if self.poll_count == 0:
            self.atd.append((self.curr_heading, self.get_distance()))
    
        if self.curr_heading > 360:
            self.update_desired_direction()

        total_positional_accel = [self.accel * math.cos(math.radians(self.desired_direction)), self.accel * -math.sin(math.radians(self.desired_direction))]
        super().update(total_positional_accel, self.ang_accel)

    def draw(self, surface):
        super().draw(surface)
        if self.should_draw_desired_heading:
            self.draw_line_at_angle(surface, self.desired_direction, self.HEADING_LINE_LENGTH, pygame.Color(0, 255, 0))