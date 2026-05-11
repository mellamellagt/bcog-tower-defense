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
        self.range = 100
        self.target = None
        self.element = element
        self.selected = False
        self.fire_delay = 1000
        self.last_shot = pg.time.get_ticks()
        self.damage = 5

        # Regarding Range Circle
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, 'grey100', (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def update(self, enemy_group, world):
        self.find_target(enemy_group)
        if self.target and pg.time.get_ticks() - self.last_shot > self.fire_delay:
            self.last_shot = pg.time.get_ticks()
            self.shoot(world)

    def find_target(self, enemy_group):
        # Clear Target from Prior Update
        self.target = None
        # Calculate Distances
        enemy_x = [enemy.pos[0] - self.x for enemy in enemy_group]
        enemy_y = [enemy.pos[1] - self.y for enemy in enemy_group]
        enemy_distances = [math.sqrt((enemy_x[i] ** 2) + (enemy_y[i] ** 2)) for i, enemy in enumerate(enemy_x)]
        
        # Target Close
        # Convert Enemy Group to List
        enemy_list = enemy_group.sprites()
        if bool(enemy_list) == False:
            return None
        if min(enemy_distances) <= self.range:
            index = enemy_distances.index(min(enemy_distances))
            self.target = enemy_list[index]
            if self.target and pg.time.get_ticks() - self.last_shot > self.fire_delay:
                self.angle = math.degrees(math.atan2(-enemy_y[index], enemy_x[index])) - 90

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    def shoot(self, world):
        self.target.health -= self.damage
        self.target.check_health(world)
        print('Shot')
        self.target = None