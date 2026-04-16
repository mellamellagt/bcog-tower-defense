import pygame as pg

class Turret(pg.sprite.Sprite):
    def __init__(self, image, pos, element = None):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.element = element