import pygame

class Arena():
    def __init__(self, surface, offset_from_border):
        width = surface.get_width() - offset_from_border
        height = surface.get_height() - offset_from_border
        Arena.rect = pygame.Rect(surface.get_width()//2 - (width)//2, surface.get_height()//2 - (height)//2, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color(0, 0, 0), Arena.rect, 5)