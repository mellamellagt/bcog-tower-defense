import pygame as pg

class World: 
    def __init__(self, data, image):
        # Regarding Map
        self.level_data = data
        self.image = image
        self.waypoints = []

    def draw(self, surface):
        # Draw Map onto 'Surface'
        surface.blit(self.image, (0, 0))

    def get_waypoints(self):
        # Access Waypoints from JSON file
        self.waypoints = [(line['x'], line['y']) for layer in self.level_data['layers'] if layer['name'] == 'waypoints' for object in layer['objects'] for line in object['polyline']]