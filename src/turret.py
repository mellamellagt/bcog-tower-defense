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
        self.damage = self.data.get('basic')['damage']
        self.type_chosen = False
        
        # Creating Range Circle
        self.create_range_image()

    def create_range_image(self):
        # Creating Range Circle
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, 'grey100', (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def update(self, enemy_group, world):
        # Actions performed per frame
        self.find_target(enemy_group)
        if self.target and pg.time.get_ticks() - self.last_shot > self.fire_delay:
            self.last_shot = pg.time.get_ticks()
            if self.targeting == 'aoe':
                for target in self.target:
                    self.shoot(world, target, enemy_group)
            else:
                self.shoot(world, self.target, enemy_group)

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
                        self.angle = math.degrees(math.atan2(-enemy_y[i], enemy_x[i])) - 90
                    break
        # Targeting Last Enemy
        if self.targeting == 'Last':
            for i, distance in enumerate(enemy_distances):
                if distance <= self.range:
                    self.target = enemy_list[i]
            if self.target and pg.time.get_ticks() - self.last_shot > self.fire_delay:
                self.angle = math.degrees(math.atan2(-enemy_y[i], enemy_x[i])) - 90
        # Targeting AOE
        if self.targeting == 'aoe':
            self.target = [enemy_list[i] for i, distance in enumerate(enemy_distances) if distance <= self.range]

    def draw(self, surface):
        # Draw Method
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    def shoot(self, world, target, enemy_group):
        # Check for Element and Perform Reactions on Target
        if target.check_element():
            enemy_element = target.check_element()
            self.perform_reaction(target, enemy_element, enemy_group)
        # Apply Element onto Target if one is not already applied
        else:
            target.apply_element(self.element)
        # Logic regarding Fire + Water Reaction impact on Damage
        if self.half_dmg:
            target.health -= self.damage / 2
            self.half_dmg = False
            print('Water Reduced Your Fire Damage')
        elif self.double_dmg:
            target.health -= self.damage * 2
            self.double_dmg = False
            print('Fire increased Your Water Damage')
        else: 
            target.health -= self.damage
        # Check if the Target Dies
        target.check_health(world)
        # Clear Target
        self.target = None

    def perform_reaction(self, target, enemy_element, enemy_group):
        # Reaction Logic
        if enemy_element == 'fire':
            if self.element == 'water':
                self.double_dmg = True
                target.element = None
            if self.element == 'lightning':
                target.explode(enemy_group)
                target.element = None
        elif enemy_element == 'lightning':
            if self.element == 'water':
                target.shocks_remaining += 5
                target.element = None
            if self.element == 'fire':
                target.explode(enemy_group)
                target.element = None
        elif enemy_element == 'water':
            if self.element == 'fire':
                self.half_dmg = True
                target.element = None
            if self.element == 'lightning':
                target.shocks_remaining += 5
                target.element = None

    # Upgrades the Turret
    def upgrade(self):
        # Upgrade Turret
        self.upgrade_level += 1
        self.range = self.range * 1.1
        self.damage += 0.2
        self.fire_delay = self.fire_delay * 0.9
        self.create_range_image()

    # Changes Type of the Turret and Resets Upgrade Level
    def change_type(self, type):
        self.type = type
        self.upgrade_level = 0
        self.range = self.data.get(type)['range']
        self.fire_delay = self.data.get(type)['fire_delay']
        self.damage = self.data.get(type)['damage']
        self.create_range_image()
        if self.type == 'aoe':
            self.targeting = 'aoe'

    # Applies an Element to the Turret
    def apply_element(self, element):
        self.element = element

    # Cycles through Targetting Methods
    def change_targeting(self):
        if self.targeting == 'First':
            self.targeting = 'Close'
        elif self.targeting == 'Close':
            self.targeting = 'Last'
        elif self.targeting == 'Last':
            self.targeting = 'First'