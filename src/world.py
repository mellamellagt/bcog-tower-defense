import pygame as pg

class World: 
    def __init__(self, data, image):
        self.level_data = data
        self.image = image
        
    def draw(self, surface):
        surface.blit(self.image, (0, 0))

    def process_data(self): 
        for layer in self.level_data['layers']:
            if layer['name'] == 'waypoints':
                print(layer)