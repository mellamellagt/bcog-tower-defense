import pygame as pg
from enemy import Enemy

def run_game(screen_width, screen_height, FPS):
    # Initialize Pygame
    pg.init()

    # Create Clock
    clock = pg.time.Clock()

    # Create Screen
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("BCOG 200 Tower Defense")

    # TEMPORARY ENEMY TESTING
    enemy_image = pg.image.load('assets\enemies\placeholder.png').convert_alpha()
    waypoints = [
        (100, 200),
        (300, 100),
        (500, 200),
        (0, 0),
        (600, 600)
    ]
    enemy_group = pg.sprite.Group()
    enemy = Enemy(waypoints, enemy_image)
    enemy_group.add(enemy)

    run = True
    while run: 
        # Set FPS
        clock.tick(FPS)

        # Update Group(s)
        enemy_group.update()

        # Draw Stuff?
        screen.fill("grey100")
        enemy_group.draw(screen)
        
        # Event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        
        # Update Screen
        pg.display.flip()
    # Quit Pygame
    pg.quit()

def main():
    run_game(600, 600, 60)

if __name__ == "__main__":
    main()