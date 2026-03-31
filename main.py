import pygame as pg
from src.enemy import Enemy
from src.turret import Turret

def run_game(screen_width: int, screen_height: int, FPS: int) -> None:
    # Initialize Pygame
    pg.init()

    # Create Clock
    clock = pg.time.Clock()

    # Create Screen
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("BCOG 200 Tower Defense")

    # TEMPORARY CLASS TESTING
    enemy_image = pg.image.load(r'assets\images\enemy_temp.png').convert_alpha()
    turret_image = pg.image.load(r'assets\images\turret_temp.png').convert_alpha()
    waypoints = [
        (100, 200),
        (300, 100),
        (500, 200),
        (0, 0),
        (600, 600)
    ]
    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()
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
        turret_group.draw(screen)
        
        # Event handler
        for event in pg.event.get():
            # Quit Game when 'X' is clicked
            if event.type == pg.QUIT:
                run = False
            # Temporary Testing for placing 'turrets'
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                turret = Turret(turret_image, mouse_pos)
                turret_group.add(turret)
        
        # Update Screen
        pg.display.flip()
    # Quit Pygame
    pg.quit()

def main():
    run_game(600, 600, 60)

if __name__ == "__main__":
    main()