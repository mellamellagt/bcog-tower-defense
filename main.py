import pygame as pg
from src.enemy import Enemy
from src.turret import Turret
from src.world import World
from src.button import Button
from config import constants as c
import json

def create_text(text, font, color, x, y, screen):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))

def create_world(data, image, lives, money, waves):
    # Load Map
    world = World(data, image, lives, money, waves)
    # Get Waypoints and Tilemap from Map
    world.process_data()
    # Load the first wave
    world.load_wave()
    # Return the World
    return world

def run_game(screen_width: int, screen_height: int, FPS: int) -> None:
    # Initialize Pygame
    pg.init()

    # Create Clock
    clock = pg.time.Clock()

    # Create Screen
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("BCOG 200 Tower Defense")

    # Load Map JSON Data
    with open('assets/maps/map_one.tmj') as file: 
        world_data = json.load(file)

    # Define Images (TEMP)
    map_image = pg.image.load(r'assets\images\map_one.png').convert_alpha()
    enemy_image = pg.image.load(r'assets\images\enemy_temp.png').convert_alpha()
    turret_image = pg.image.load(r'assets\images\turret_temp.png').convert_alpha()
    cursor_turret = pg.image.load(r'assets\images\turret_temp.png').convert_alpha()
    buy_button_image = pg.image.load(r'assets\images\buy_button.png').convert_alpha()
    cancel_button_image = pg.image.load(r'assets\images\buy_button.png').convert_alpha()
    begin_button_image = pg.image.load(r'assets\images\buy_button.png').convert_alpha()
    restart_button_image = pg.image.load(r'assets\images\buy_button.png').convert_alpha()
    upgrade_button_image = pg.image.load(r'assets\images\buy_button.png').convert_alpha()
    element_button_image = pg.image.load(r'assets\images\buy_button.png').convert_alpha()
    targeting_button_image = pg.image.load(r'assets\images\buy_button.png').convert_alpha()

    # Create the Map
    world = create_world(world_data, map_image, c.LIVES, c.MONEY, c.WAVES)

    # Create Enemy and Turret Groups (pygame data structure)
    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()

    # Define Font
    text_font = pg.font.SysFont('Consolas', 24, bold = True)

    # Set Game Mechanics to Starting State
    game_over = False
    game_outcome = 0
    level_started = False
    placing_turrets = False
    selected_turret = None
    last_enemy_spawned = pg.time.get_ticks()

    # Create Buttons (TEMP)
    buy_button = Button(c.TILE_SIZE * c.MAP_WIDTH + 75, 100, buy_button_image)
    cancel_button = Button(c.TILE_SIZE * c.MAP_WIDTH + 75, 200, cancel_button_image)
    begin_button = Button(c.TILE_SIZE * c.MAP_WIDTH + 75, 400, begin_button_image)
    upgrade_button = Button(c.TILE_SIZE * c.MAP_WIDTH + 75, 300, upgrade_button_image)
    restart_button = Button(310, 300, restart_button_image)

    # Game Loop
    run = True
    while run: 
        # Set FPS
        clock.tick(FPS)
        
        # Check if the Game is Over
        if game_over == False:
            if world.lives <= 0:
                game_over = True
                game_outcome = -1
            if world.wave >= len(world.waves):
                game_over = True
                game_outcome = 1
            
            # Update Group(s)
            enemy_group.update(world)
            turret_group.update(enemy_group, world)

            # Selected Turret
            if selected_turret:
                selected_turret.selected = True

        # Draw Map 
        world.draw(screen)
        # Draw Side Panel
        pg.draw.rect(screen, 'maroon', (c.TILE_SIZE * c.MAP_WIDTH, 0, c.SIDE_PANEL, c.TILE_SIZE * c.MAP_HEIGHT))
        # Draw Enemies
        enemy_group.draw(screen)
        # Draw Turrets
        for turret in turret_group:
            turret.draw(screen)
        # Draw Buy Button
        if buy_button.draw(screen):
            placing_turrets = True
        # Draw Turret on Cursor when Placing Turrets
        if placing_turrets: 
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= c.MAP_WIDTH * c.TILE_SIZE:
                screen.blit(cursor_turret, cursor_rect)
            # Draw Cancel Button only if Placing Turrets
            if cancel_button.draw(screen):
                placing_turrets = False
        if selected_turret:
            create_text('UPGRADE LEVEL: ' + str(selected_turret.upgrade_level) + '/5', text_font, 'grey100', c.TILE_SIZE * c.MAP_WIDTH + 25, 0, screen)
            create_text('ELEMENT: ' + str(selected_turret.element), text_font, 'grey100', c.TILE_SIZE * c.MAP_WIDTH + 25, 30, screen)
            create_text('TARGETING: ' + str(selected_turret.targeting), text_font, 'grey100', c.TILE_SIZE * c.MAP_WIDTH + 25, 60, screen)
            if selected_turret.upgrade_level < 5:
                if upgrade_button.draw(screen):
                    selected_turret.upgrade()

        # Draw Text
        create_text('LIVES: ' + str(world.lives), text_font, 'grey100', 5, 0, screen)
        create_text('MONEY: $' + str(world.money), text_font, 'grey100', 5, 30, screen)
        create_text('WAVE: ' + str(world.wave) + '/' + str(len(world.waves)), text_font, 'grey100', 5, 60, screen)

        # Enemy Spawning
        if game_over == False: 
            if level_started == False: 
                if begin_button.draw(screen):
                    level_started = True
            elif world.check_wave_completion():
                level_started = False
                world.money += c.WAVE_BONUS
                last_enemy_spawned = pg.time.get_ticks()
                world.next_wave()
                world.load_wave()
            else: 
                # Spawn Enemies
                if pg.time.get_ticks() - last_enemy_spawned > c.SPAWN_DELAY and world.enemies_spawned < len(world.enemy_list): 
                    enemy_type = world.enemy_list[world.enemies_spawned]
                    enemy = Enemy(enemy_type, c.ENEMIES, world.waypoints, enemy_image)
                    enemy_group.add(enemy)
                    world.enemies_spawned += 1
                    last_enemy_spawned = pg.time.get_ticks()
        else: 
            # Game Over Logic
            pg.draw.rect(screen, 'blue', (200, 200, 400, 200), border_radius = 30)
            if game_outcome == -1:
                create_text('GAME OVER', text_font, 'grey0', 310, 230, screen)
            elif game_outcome == 1:
                create_text('YOU WIN', text_font, 'grey0', 310, 230, screen)
            if restart_button.draw(screen):
                # Set Game Mechanics to Starting State
                game_over = False
                game_outcome = 0
                level_started = False
                placing_turrets = False
                selected_turret = None
                last_enemy_spawned = pg.time.get_ticks()
                # Create the Map
                world = create_world(world_data, map_image, c.LIVES, c.MONEY, c.WAVES)
                # Reset Groups
                enemy_group.empty()
                turret_group.empty()

        # Event handler
        for event in pg.event.get():
            # Quit Game when 'X' is clicked
            if event.type == pg.QUIT:
                run = False
            # Turret Placing Logic
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Check that Mouse is in the Game Area
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] <= c.TILE_SIZE * c.MAP_WIDTH and mouse_pos[1] <= c.TILE_SIZE * c.MAP_HEIGHT:
                    selected_turret = None
                    for turret in turret_group:
                        turret.selected = False
                    # Check if player is placing turrets or selecting a turret
                    if placing_turrets == True and world.money >= c.TURRET_COST:
                        # Assume Space is Free
                        space_free = True
                        # Calculate Mouse Position
                        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
                        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
                        # Calculate Tile Number
                        tile_num = (mouse_tile_y * c.MAP_HEIGHT) + mouse_tile_x
                        # Check if the Space is actually Free
                        for turret in turret_group:
                            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                                space_free = False
                        # Check if the Tile is placeable (need to implement)
                        if space_free == True and tile_num:
                            new_turret = Turret(turret_image, mouse_tile_x, mouse_tile_y, c.TILE_SIZE, c.TURRETS)
                            turret_group.add(new_turret)
                        # Subtract Money
                        world.money -= c.TURRET_COST
                    else:
                        # Calculate Mouse Position
                        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
                        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
                        # Need to remake the map so that the tile numbers are consistent I guess?
                        for turret in turret_group:
                            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                                selected_turret = turret
            
        # Update Screen
        pg.display.flip()
    # Quit Pygame
    pg.quit()

def main():
    run_game(c.TILE_SIZE * c.MAP_WIDTH + c.SIDE_PANEL, c.TILE_SIZE * c.MAP_HEIGHT, 60)

if __name__ == "__main__":
    main()