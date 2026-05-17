import pygame as pg
from pygame.math import Vector2
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, type, data, waypoints, images):
        # Sprite Init
        pg.sprite.Sprite.__init__(self)
        
        # Regarding Waypoints
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1

        # Regarding Enemy Information
        self.health = data.get(type)['health']
        self.speed = data.get(type)['speed']
        self.movement_remaining = 0
        self.reward = data.get(type)['reward']
        self.damage = data.get(type)['damage']
        self.element = None
        self.shocks_remaining = 0
        self.last_shock = pg.time.get_ticks()

        # Regarding Image
        self.original_image = images
        self.angle = 0
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        if self.shocks_remaining > 0:
            self.get_shocked(world)
        self.rotate()
    
    def move(self, world):
        # Check if Enemy is at the end and if so remove it
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            world.lives -= 1
            world.enemies_completed += 1
            self.kill()
        # Perform 'overflow' movement
        if self.movement_remaining != 0 and self.movement[0] >= self.movement_remaining[0] and self.movement[1] >= self.movement_remaining[1]:
            self.pos += self.movement_remaining
            self.movement_remaining = 0
        # Perform Normal Movement
        dist = self.movement.length()
        if dist >= self.speed: 
            self.pos += self.movement.normalize() * self.speed
        # Make sure that we don't overshoot the waypoint, bank 'extra' movement, and update target waypoint
        else:
            if dist != 0: 
                self.pos += self.movement.normalize()
                self.movement_remaining = (self.movement.normalize() * self.speed) - self.movement.normalize()
            self.target_waypoint += 1

    def rotate(self):
        # Calculate + Perform Rotation
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    # Checks if the Enemy is Alive
    def check_health(self, world):
        if self.health <= 0:
            self.kill()
            world.enemies_completed += 1
            world.money += self.reward

    # Applies an Element to the Enemy
    def apply_element(self, element): 
        self.element = element

    # Returns Element
    def check_element(self):
        if self.element:
            return self.element
        return False
    
    # DoT Effect from Shock (Lightning + Water)
    def get_shocked(self, world):
        if pg.time.get_ticks() - self.last_shock > 250:
            self.last_shock = pg.time.get_ticks()
            self.health -= 1
            self.check_health(world)
            print('Shock DoT Taken Succesfully')

    # Damage Effect from Explosion (Fire + Lightning)
    def explode(self, enemy_group):
        self.health -= 5
        for enemy in enemy_group:
            enemy_x = enemy.pos[0] - self.pos[0]
            enemy_y = enemy.pos[1] - self.pos[1]
            enemy_distance = math.sqrt((enemy_x ** 2) + (enemy_y ** 2))
            if enemy_distance <= 100:
                enemy.health -= 5
        print('Explosion Successful')