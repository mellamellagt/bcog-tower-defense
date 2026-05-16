import pygame as pg
from pygame.math import Vector2
import math

class Turret(pg.sprite.Sprite):
    def __init__(self, images, tile_x, tile_y, tile_size, data):
        # Sprite Init
        pg.sprite.Sprite.__init__(self)

        # Regarding Placement
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (self.tile_x + 0.5) * tile_size
        self.y = (self.tile_y + 0.5) * tile_size
        self.pos = Vector2((self.x, self.y))

        # Regarding Image
        self.original_image = images
        self.angle = 0
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # Regarding Game Mechanics
        self.data = data
        self.upgrade_level = 0
        self.type = 'basic'
        self.range = self.data.get('basic')['range']
        self.target = None
        self.element = None
        self.half_dmg = False
        self.double_dmg = False
        self.targeting = 'First'
        self.selected = False
        self.fire_delay = self.data.get('basic')['fire_delay']
        self.last_shot = pg.time.get_ticks()
        self.damage = self.data.get('basic')['fire_delay']
        self.create_range_image()

    def create_range_image(self):
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
            self.shoot(world, enemy_group)

    def find_target(self, enemy_group):
        # Clear Target from Prior Update
        self.target = None
        # Calculate Distances
        enemy_x = [enemy.pos[0] - self.x for enemy in enemy_group]
        enemy_y = [enemy.pos[1] - self.y for enemy in enemy_group]
        enemy_distances = [math.sqrt((enemy_x[i] ** 2) + (enemy_y[i] ** 2)) for i, enemy in enumerate(enemy_x)]
        
        # Convert Enemy Group to List
        enemy_list = enemy_group.sprites()
        # Check if there are enemies
        if bool(enemy_list) == False:
            return None
        # Targeting Closest Enemy
        if self.targeting == 'Close':
            if min(enemy_distances) <= self.range:
                index = enemy_distances.index(min(enemy_distances))
                self.target = enemy_list[index]
                if self.target and pg.time.get_ticks() - self.last_shot > self.fire_delay:
                    self.angle = math.degrees(math.atan2(-enemy_y[index], enemy_x[index])) - 90
        # Targeting First Enemy
        if self.targeting == 'First':
            for i, distance in enumerate(enemy_distances):
                if distance <= self.range:
                    self.target = enemy_list[i]
                    if self.target and pg.time.get_ticks() - self.last_shot > self.fire_delay:
                        self.angle = math.degrees(math.atan2(-enemy_y[index], enemy_x[index])) - 90

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    def shoot(self, world, enemy_group):
        if self.target.check_element():
            enemy_element = self.target.element()
            self.perform_reaction(enemy_element, enemy_group)
        else:
            self.target.apply_element(self.element)
        if self.half_dmg:
            self.target.health -= self.damage / 2
            self.half_dmg = False
        elif self.double_dmg:
            self.target.health -= self.damage * 2
            self.double_dmg = False
        else: 
            self.target.health -= self.damage
        self.target.check_health(world)
        self.target = None

    def perform_reaction(self, enemy_element, enemy_group):
        if enemy_element == 'Fire':
            if self.element == 'Water':
                self.double_dmg = True
                self.target.element = None
            if self.element == 'Lightning':
                self.target.explode(enemy_group)
                self.target.element = None
        elif enemy_element == 'Lightning':
            if self.element == 'Water':
                self.target.shocks_remaining += 5
                self.target.element = None
            if self.element == 'Fire':
                self.target.explode(enemy_group)
                self.target.element = None
        elif enemy_element == 'Water':
            if self.element == 'Fire':
                self.half_dmg = True
                self.target.element = None
            if self.element == 'Lightning':
                self.target.shocks_remaining += 5
                self.target.element = None

    def upgrade(self):
        self.upgrade_level += 1
        self.range = self.range * 1.1
        self.damage += 1
        self.fire_delay = self.fire_delay * 0.9
        self.create_range_image()

    def change_type(self, type):
        self.type = type
        self.range = self.data.get(type)['range']
        self.fire_delay = self.data.get(type)['fire_delay']
        self.damage = self.data.get(type)['damage']
        self.create_range_image()

    def apply_element(self, element):
        self.element = element

    def change_targeting(self):
        if self.targeting == 'First':
            self.targeting = 'Close'
        elif self.targeting == 'Close':
            self.targeting = 'First'