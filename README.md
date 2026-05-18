# Tower Defense Game
This repository contains an interactive tower defense game built with pygame. The Tower Defense game features three different types of towers and three different Elements that can be applied to your towers. The Elemental Towers can trigger various Elemental Reactions. There are 5 pre-defined waves but an Endless Mode does exist. The game is not currently designed with any regard to game balance, and it has rather been made rather easy due to the large amount of starting cash. Players are free to do balancing for themselves by changing values in the constants.py file (found under the config folder)

# Installation
    # Install uv
    pip add uv

    # Install pygame to uv
    uv add pygame-ce

    # Run the Tower Defense
    uv run main.py

# Testing
There is no core testing implementation as it is difficult to test pygame functionality. Instead, some expected functionalit is listed below: 
- The 'buy turrets' button should allow the player to place turrets as long as they have money
- As long as the player is placing turrets, the 'cancel' button should appear and allow the player to stop placing turrets
- If a turret is selected, the player should be able to switch targeting methods, upgrade the turret, and apply an element through buttons
    - Each turret can be upgraded up to 5 times, which increases the damage, range, and fire rate
    - When a turret has been upgraded 3 times, the 'type' of the turret can be modified which resets the upgrade count
- Turrets apply their Element on hit and then may trigger 'Elemental Reactions'.
    - There is currently no visual indicator, so the 'print' function is used as a substitute
- The 'begin round' button should allow the player to send out the next wave of enemies
- When the player dies or completes all the waves, a popup should come up acknowledging the outcome and then providing the option to restart

# Code Structure
- main.py - Run Tower Defense game
- src/ - Core implementation
    - enemy.py - Defines 'Enemy' class and corresponding logic
    - turret.py - Defines 'Turret' class and corresponding logic
    - world.py - Defines 'World' class and corresponding logic
    - button.py - Defines 'Button' class and corresponding logic
- assets/ - contains assets for the game
    - images/ - contains images
    - maps/ - contains map data
- config/ - constants for running the program
    - constants.py - contains game constants (FPS, screen size, etc;)

# Controls
Everything in the program is controlled by the mouse, click on buttons to activate their corresponding functions. 
Click on the 'X' button on the pygame window to close the Tower Defense game. 

# Attribution
Map: Created using the PC Program 'Tiled'
    Map Assets: Kenney (www.kenney.nl/assets/tower-defense-top-down)
Pixel Art: Created using Website 'www.pixilart.com'
    Various Inspiration Taken from Magnific (www.magnific.com)
Tower Defense Walkthrough: Coding with Russ (www.youtube.com/watch?v=WRuf9iPAXfM)