import pygame 

class Robot:
    def __init__(self, pos, shape):
        self.pos = pos
        self.shape = shape
        self.curr_heading = 0 #in degrees from 0-360
        self.desired_direction = 0 #in degrees from 0-360

    def update_desired_direction(self): #only update desired_direction once every 360 degrees, throw out all dicts after
        #use a PID controller to update heading, make a separate class for PID
        ...

    def update(self): #needs deltaTime to update internal timer
        ...

    def draw(self, surface):
        if isinstance(self.shape, Circle):
            pygame.draw.circle(surface, self.shape.color, self.pos, self.shape.radius)

        if isinstance(self.shape, Rectangle):
            pygame.draw.rect(surface, self.shape.color, self.pos + (self.shape.width, self.shape.height))

class Melty(Robot):
    def __init__(self, pos, shape, rpm, poll_rate, agro = True):
        super().__init__(pos, shape)
        self.RPS = rpm / 60
        self.poll_rate = poll_rate #in ms
        self.agro = agro
        self.time_elapsed = 0 #in ms
        self.atd = [] #angle to distance | degrees, distance (D) in meters 
        self.atdd = [] #angle to delta distance | degrees, change in distance with respect to angle (avg rate of change)
        self.atwad = [] #angle to weighted delta distance | degrees, average distances

    def update_curr_heading(self, delta_time):
        self.curr_heading = (self.curr_heading + 360 * self.RPS * delta_time) % 360

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
    
    def populate_angle_to_weighted_average_distance(self):
        for i in range(len(self.atd)):
            for j in range(len(self.atd)):
                self.atwad.append(sum(map(lambda s: (1 / max(0.1,abs(i-j))) * self.atd[j], self.atd)))

    def update_desired_direction(self):
        self.populate_angle_to_delta_distance()
        self.populate_angle_to_weighted_average_distance()
        self.atd = []
        self.atdd = []
        self.atwad = []

    def get_distance(self):
        ...

    def update(self, delta_time):
        self.time_elapsed += delta_time
        self.update_curr_heading(delta_time)

        if self.time_elapsed // self.poll_rate > 0:
            self.atd.append((self.curr_heading, self.get_distance()))
            self.time_elapsed = 0

    #look into raycasting in Pygame

class Enemy(Robot):
    ...

class Shape:
    def __init__(self, color):
        self.color = color

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height

class Arena:
    def __init__(self):
        ...