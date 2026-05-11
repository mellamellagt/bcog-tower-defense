import pygame as pg

class World: 
    def __init__(self, data, image, lives, money):
        # Regarding Map
        self.level_data = data
        self.image = image
        self.lives = lives
        self.money = money
        self.waypoints = []
        self.tilemap = []

    def draw(self, surface):
        # Draw Map onto 'Surface'
        surface.blit(self.image, (0, 0))

    def process_data(self):
        # Access Waypoints from JSON file
        self.waypoints = [(line['x'], line['y']) for layer in self.level_data['layers'] if layer['name'] == 'waypoints' for object in layer['objects'] for line in object['polyline']]
        # Access Tilemap from JSON file
        for layer in self.level_data['layers']:
            if layer['name'] == 'map':
                self.tilemap = layer['data']