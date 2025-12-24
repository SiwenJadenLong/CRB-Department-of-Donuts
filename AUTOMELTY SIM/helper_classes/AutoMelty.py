from helper_classes.Robot import Robot
from helper_classes.Arena import Arena
import pygame
import math

#TO DO
# actually show each distance ray that is being cast at what angle
# make sure robot never leaves box
# tune delta_distance_threshold value to make sure opponent robot is actually being detected

class AutoMelty(Robot):
    def __init__(self, accel, ang_accel, poll_resolution, agro, rect, color = pygame.Color(0, 0, 0), should_draw_heading=False, should_draw_desired_heading=False):
        super().__init__(rect, color, should_draw_heading)
        self.should_draw_desired_heading = should_draw_desired_heading
        self.accel = accel
        self.ang_accel = ang_accel
        self.poll_resolution = poll_resolution
        self.agro = agro
        self.desired_direction = 0
        self.poll_count = 0
        self.atd = [] #angle to distance | degrees, distance (D) in meters 
        self.atwad = [] #angle to weighted delta distance | degrees, average distances
        self.detected_distance_line_ends = []

    def find_opponent(self):
        index_of_largest_angle_change = max(range(len(self.atd)), key=lambda i: abs(self.atd[i][1]-self.atd[i-1][1]))
        first = self.atd.pop(index_of_largest_angle_change)
        index_of_second_largest_angle_change = max(range(len(self.atd)), key=lambda i: abs(self.atd[i][1]-self.atd[i-1][1]))
        second = self.atd.pop(index_of_second_largest_angle_change)

        # this catches 10 - 350 cases where the bottom formula calculates 180 instead of 0, 
        # the angle between first and second should never be 180 otherwise
        if abs(first[0] - second[0]) > 180: 
            desired_direction = ((first[0] + second[0]) % 360) / 2
        else:
            desired_direction = (first[0] + second[0]) / 2
        
        return index_of_largest_angle_change, index_of_second_largest_angle_change, desired_direction

    def populate_angle_to_weighted_average_distance(self): #this is probably not giving the right numbers 
        begin, end, _ = self.find_opponent()
        def get_weighted_value(j):
            multiplier = 1
            if self.atd[0] in range(begin, end):
                multiplier = 10
            value = (1 / (max(0.1,abs(i-j))*multiplier)) * self.atd[j][1] #this just doesn't work
            return value

        for i in range(len(self.atd)):
            self.atwad.append((self.atd[i][0], sum(map(get_weighted_value, range(len(self.atd))))))

    def run_away_from_opponent(self):
        
        max_pair = max(self.atd, key=lambda s: s[1])
        self.desired_direction = max_pair[0]

    def get_distance(self):
        other_robot = [robot for robot in Robot.robots if robot is not self][0]
        for d in range(2000):
            pos = [self.rect.center[0] + d * math.cos(math.radians(self.curr_heading)), self.rect.center[1] + d * -math.sin(math.radians(self.curr_heading))]
            current_rect = pygame.Rect(pos[0], pos[1], 1, 1)
            if other_robot.rect.colliderect(current_rect) or not Arena.rect.colliderect(current_rect):
                self.detected_distance_line_ends.append((pos[0], pos[1]))
                return d
        self.detected_distance_line_ends.append((pos[0], pos[1]))
        return d

    def update_desired_direction(self):
        if self.agro:
            _, _, self.desired_direction = self.find_opponent()
        else:
            #self.populate_angle_to_weighted_average_distance()
            self.run_away_from_opponent()

        self.atd = []
        self.atwad = []
        self.detected_distance_line_ends = []

    def toggle_agro(self):
        self.agro = not self.agro
        print("TOGGLED AGRO TO", self.agro)

    def update(self, delta_time):
        self.poll_count += 1
        self.poll_count %= self.poll_resolution

        if self.poll_count == 0:
            self.atd.append((self.curr_heading, self.get_distance()))
    
        if self.curr_heading >= 360:
            self.update_desired_direction()

        total_positional_accel = [self.accel * math.cos(math.radians(self.desired_direction)), self.accel * -math.sin(math.radians(self.desired_direction))]
        super().update(total_positional_accel, self.ang_accel, delta_time)

    def draw(self, surface):
        super().draw(surface)

        for line_end in self.detected_distance_line_ends:
            pygame.draw.line(surface, pygame.Color(0, 0, 255), self.rect.center, line_end)

        if self.should_draw_desired_heading:
            self.draw_line_at_angle(surface, self.desired_direction, self.HEADING_LINE_LENGTH, pygame.Color(0, 255, 0))