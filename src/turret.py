import pygame as pg
from pygame.math import Vector2
import math

class Turret(pg.sprite.Sprite):
    def __init__(self, image, tile_x, tile_y, tile_size, element = None):
        # Sprite Init
        pg.sprite.Sprite.__init__(self)

        # Regarding Placement
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (self.tile_x + 0.5) * tile_size
        self.y = (self.tile_y + 0.5) * tile_size
        self.pos = Vector2((self.x, self.y))

        # Regarding Image
        self.original_image = image
        self.angle = 0
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # Regarding Game Mechanics
        self.range = 1000
        self.target = None
        self.element = element
        # self.enemy_group = enemy_group
    
    def update(self):
        pass
        # self.find_target(self.enemy_group)

    def find_target(self, enemy_group):
        # Clear Target from Prior Update
        self.target = None
        # Convert Enemy Group to List
        enemy_list = enemy_group.sprites()
        # Calculate the Distances to all Enemies
        enemy_positions = [enemy.pos - self.pos for enemy in enemy_list]
        distances = [math.sqrt(abs(position[0] * position[0]) * abs(position[1] * position[1])) for position in enemy_positions]
        # Check if closest enemy is in range
        if min(distances) <= self.range:
            self.target = enemy_list[distances.index(min(distances))]
        print(self.target)