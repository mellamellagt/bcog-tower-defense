import pygame as pg
from src.enemy import Enemy
from src.turret import Turret
from src.world import World
from src.button import Button
from config import constants as c
import json

def run_game(screen_width: int, screen_height: int, FPS: int) -> None:
    # Initialize Pygame
    pg.init()

    # Create Clock
    clock = pg.time.Clock()

    # Create Screen
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("BCOG 200 Tower Defense")

    # Load Level JSON Data
    with open('assets/maps/map_one.tmj') as file: 
        world_data = json.load(file)

    # temporary game mechanics testing
    game_over = False
    game_outcome = 0

    # temporary button testing
    placing_turrets = False

    # temporary range indicator testing
    selected_turret = None

    # Define Class Images (TEMPORARY)
    enemy_image = pg.image.load(r'assets\images\enemy_temp.png').convert_alpha()
    turret_image = pg.image.load(r'assets\images\turret_temp.png').convert_alpha()
    cursor_turret = pg.image.load(r'assets\images\turret_temp.png').convert_alpha()
    map_image = pg.image.load(r'assets\images\map_one.png').convert_alpha()
    buy_button_image = pg.image.load(r'assets\images\buy_button.png').convert_alpha()
    cancel_button_image = pg.image.load(r'assets\images\buy_button.png').convert_alpha()

    # Load Map
    world = World(world_data, map_image, c.LIVES, c.MONEY)
    # Get Waypoints and Tilemap from Map
    world.process_data()
    # Temporary Class Testing
    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()
    enemy = Enemy(world.waypoints, enemy_image)
    enemy_group.add(enemy)
    buy_button = Button(c.TILE_SIZE * c.MAP_WIDTH + 75, 100, buy_button_image)
    cancel_button = Button(c.TILE_SIZE * c.MAP_WIDTH + 75, 200, cancel_button_image)

    # Displaying Text
    text_font = pg.font.SysFont('Consolas', 24, bold = True)

    def create_text(text, font, color, x, y):
        image = font.render(text, True, color)
        screen.blit(image, (x, y))

    def create_turret(mouse_pos): 
        # Assume Space is Free
        space_free = True
        # Calculate Mouse Position
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        # Calculate Tile Number
        tile_num = (mouse_tile_y * c.MAP_HEIGHT) + mouse_tile_x
        # Need to remake the map so that the tile numbers are consistent I guess?
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_free = False
        if space_free == True:
            new_turret = Turret(turret_image, mouse_tile_x, mouse_tile_y, c.TILE_SIZE)
            turret_group.add(new_turret)

    def select_turret(mouse_pos):
        # Calculate Mouse Position
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        # Need to remake the map so that the tile numbers are consistent I guess?
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                return turret
        return None

    def clear_selection(): 
        for turret in turret_group:
            turret.selected = False

    run = True
    while run: 
        # Set FPS
        clock.tick(c.FPS)

        if game_over == False and world.lives <= 0:
            game_over = True
            game_outcome = -1
            
            # Update Group(s)
            enemy_group.update(world)
            turret_group.update(enemy_group, world)

            # Selected Turret
            if selected_turret:
                selected_turret.selected = True

        # Draw Stuff
        screen.fill("grey100")
        world.draw(screen)
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)
        if buy_button.draw(screen):
            placing_turrets = True
        if placing_turrets: 
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= c.MAP_WIDTH * c.TILE_SIZE:
                screen.blit(cursor_turret, cursor_rect)
            if cancel_button.draw(screen):
                placing_turrets = False
        
        create_text('LIVES: ' + str(world.lives), text_font, 'grey100', 0, 0)
        create_text('MONEY: ' + str(world.money), text_font, 'grey100', 0, 30)

        # Event handler
        for event in pg.event.get():
            # Quit Game when 'X' is clicked
            if event.type == pg.QUIT:
                run = False
            # Temporary Testing for placing 'turrets'
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] <= c.TILE_SIZE * c.MAP_WIDTH and mouse_pos[1] <= c.TILE_SIZE * c.MAP_HEIGHT:
                    selected_turret = None
                    clear_selection()
                    if placing_turrets == True and world.money >= c.TURRET_COST:
                        create_turret(mouse_pos)
                        world.money -= c.TURRET_COST
                    else:
                        selected_turret = select_turret(mouse_pos)
            
        # Update Screen
        pg.display.flip()
    # Quit Pygame
    pg.quit()

def main():
    run_game(c.TILE_SIZE * c.MAP_WIDTH + 300, c.TILE_SIZE * c.MAP_HEIGHT, 60)

if __name__ == "__main__":
    main()