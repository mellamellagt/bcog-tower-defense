# Tower Defense Game
This repository contains an interactive tower defense game built with pygame. 

# Installation
    # Install uv
    pip add uv

    # Install pygame to uv
    uv add pygame-ce

    # Run the Tower Defense
    uv run main.py

# Testing
TBD

# Code Structure
- main.py - Run Tower Defense game
- src/ - Core implementation
    - enemy.py - Defines 'Enemy' class and corresponding logic
    - turret.py - Defines 'Turret' class and corresponding logic
    - world.py - Defines 'World' class and corresponding logic
- assets/ - contains assets for the game
    - images/ - contains images
    - maps/ - contains map data
- config/ - constants for running the program
    - constants.py - contains game constants (FPS, screen size, etc;)

# Controls
Everything in the program is controlled by the mouse, click on buttons to activate their corresponding functions. 
Click on the 'X' button on the pygame window to close the Tower Defense game. 

# Attribution
Map Assets: Kenney (www.kenney.nl/assets/tower-defense-top-down)