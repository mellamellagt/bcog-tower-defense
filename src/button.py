import pygame as pg

'''
The Class Button is entirely unoriginal code taken from the Walkthrough
'''

class Button():
  def __init__(self, x, y, image):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
    self.clickable = True

  def draw(self, surface):
    # Assume the button was not clicked
    clicked = False
    # Get the mouse position
    pos = pg.mouse.get_pos()
    # Check if mouse is over the button
    if self.rect.collidepoint(pos):
      # Check if the button is clicked
      if pg.mouse.get_pressed()[0] == 1 and self.clickable == True:
        clicked = True
        self.clickable = False
    # Allow button to be clicked again if mouse is released
    if pg.mouse.get_pressed()[0] == 0:
      self.clickable = True
    # Draw the button
    surface.blit(self.image, self.rect)
    # Return whether the button was clicked
    return clicked