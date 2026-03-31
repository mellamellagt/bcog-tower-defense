import pygame as pg
from pygame.math import Vector2
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints: list, image):
        # Sprite Init
        pg.sprite.Sprite.__init__(self)
        
        # Regarding Waypoints
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1

        # Regarding Movement Speed
        self.speed = 1
        self.movement_remaining = 0

        # Regarding Image
        self.original_image = image
        self.angle = 0
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotate()
    
    def move(self):
        # Check if there is more 'track' to go
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()
        # Perform 'overflow' movement
        if self.movement_remaining != 0 and self.movement[0] >= self.movement_remaining[0] and self.movement[1] >= self.movement_remaining[1]:
            self.pos += self.movement_remaining
            self.movement_remaining = 0
        # Perform Movement
        dist = self.movement.length()
        if dist >= self.speed: 
            self.pos += self.movement.normalize() * self.speed
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