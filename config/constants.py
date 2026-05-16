# Map Constants
TILE_SIZE = 40
MAP_HEIGHT = 13
MAP_WIDTH = 13
SIDE_PANEL = 300

# Game Constants
FPS = 60
LIVES = 100
MONEY = 600
TURRET_COST = 100
UPGRADE_COST = 100
SPAWN_DELAY = 400
WAVE_BONUS = 100

# Turret Constants
TURRETS = {
    'basic':{
        'range': 100,
        'fire_delay': 1000,
        'damage': 2
    },
    'aoe':{
        'range': 200,
        'fire_delay': 250,
        'damage': 1
    },
    'sniper':{
        'range': 500,
        'fire_delay': 5000,
        'damage': 10
    }
}

# Enemy Constants
ENEMIES = {
    'weak':{
        'health': 10,
        'speed': 1,
        'reward': 1,
        'damage': 1
    },
    'medium':{
        'health': 20,
        'speed': 2,
        'reward': 5,
        'damage': 5
    },
    'strong':{
        'health': 40,
        'speed': 1,
        'reward': 10,
        'damage': 10
    }
}
WAVES = [
    {
        # Wave 1
        'weak': 5,
        'medium': 0,
        'strong': 0
    },
    {
        # Wave 2
        'weak': 10,
        'medium': 0,
        'strong': 0
    },
        {
        # Wave 3
        'weak': 15,
        'medium': 0,
        'strong': 0
    },
        {
        # Wave 4
        'weak': 15,
        'medium': 5,
        'strong': 0
    },
        {
        # Wave 5
        'weak': 15,
        'medium': 5,
        'strong': 1
    }
]