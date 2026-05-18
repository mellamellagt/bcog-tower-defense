import pygame as pg
import random

'''
Methods draw, process_data, check_wave_completion, and next_wave likely consist of code that can entirely be found in the walkthrough
Methods __init__ and load_wave contain code from the Walkthrough but has definitely been modified / expanded upon
Method generate_wave is entirely original code
'''

class World: 
    def __init__(self, data, image, lives, money, waves):
        # Regarding Map
        self.level_data = data
        self.image = image
        self.waypoints = []
        self.tilemap = []

        # Regarding Game Mechanics
        self.lives = lives
        self.money = money
        self.waves = waves
        self.wave = 1
        self.enemy_list = []
        self.enemies_spawned = 0 
        self.enemies_completed = 0
        self.endless = False

    def draw(self, surface):
        # Draw Map onto 'Surface'
        surface.blit(self.image, (0, 0))

    def process_data(self):
        # Access Waypoints and Tilemap from JSON file
        for layer in self.level_data['layers']:
            if layer['name'] == 'map':
                self.tilemap = layer['data']
            if layer['name'] == 'waypoints':
                self.waypoints = [(line['x'], line['y']) for object in layer['objects'] for line in object['polyline']]
    
    # Randomize Wave
    def load_wave(self):
        if self.wave <= len(self.waves):
            enemies = self.waves[self.wave - 1]
            for type in enemies: 
                spawn_queue = enemies[type]
                for enemy in range(spawn_queue):
                    self.enemy_list.append(type)
            random.shuffle(self.enemy_list)
        else: 
            enemies = self.generate_wave()
            for type in enemies: 
                spawn_queue = enemies[type]
                for enemy in range(spawn_queue):
                    self.enemy_list.append(type)
            random.shuffle(self.enemy_list)
            

    # Check if the Current Wave is Done
    def check_wave_completion(self): 
        if self.enemies_completed >= len(self.enemy_list):
            return True
        return False
    
    # Set up Next Wave
    def next_wave(self): 
        self.wave += 1
        self.enemy_list = []
        self.enemies_completed = 0
        self.enemies_spawned = 0

    def generate_wave(self):
        weak = round(5 * self.wave * random.randint(7, 13) / 10)
        medium = round(5 * self.wave / 4 * random.randint(7, 13) / 10)
        strong = round(1 * self.wave / 5 * random.randint(7, 13) / 10)
        wave = {
            'weak': weak,
            'medium': medium,
            'strong': strong
        }
        return wave