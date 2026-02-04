# Alien Invasion

A classic arcade-style space shooter game built with Python and the Pygame library, following the project from *Python Crash Course* by Eric Matthes.

## About This Project

This project was completed as part of my Python learning journey, following the comprehensive tutorial in *Python Crash Course*. It demonstrates fundamental game development concepts and object-oriented programming principles in Python.

### Original Features (From Book)

- Player-controlled spaceship with left/right movement
- Alien fleet that moves across and down the screen
- Bullet system with limited ammunition (3 bullets at a time)
- Collision detection between bullets and aliens
- Scoring system with high score tracking
- Progressive difficulty - game speeds up as you clear fleets
- Lives system - 3 ships per game
- Level progression tracking
- Play button to start and restart the game

### Additional Features (My Implementations)

- **Three alien types** with different colors and point values:
  - Red aliens (top row): 50 points
  - Yellow aliens (middle rows): 20 points
  - Green aliens (bottom rows): 10 points
- **Alien shooting mechanics** - aliens fire red bullets back at the player
- **Collision detection** between alien bullets and player ship
- **Dynamic difficulty scaling** - alien fire frequency increases each level
- **Pause functionality** - press P to pause/unpause the game with visual feedback
- **Game Over screen** - displays "GAME OVER" message when all ships are lost
- **Labeled scoreboard** - added "Score:", "Level:", and "High:" labels for clarity

## Core Components

- **alien_invasion.py** - Main game loop and event handling
- **ship.py** - Player ship class with movement logic
- **alien.py** - Alien sprite class with fleet behavior and point values
- **bullet.py** - Player bullet sprite class and physics
- **alien_bullet.py** - Alien bullet sprite class for enemy fire
- **settings.py** - Centralized game configuration and dynamic difficulty scaling
- **game_stats.py** - Game state and statistics tracking (including pause state)
- **scoreboard.py** - Score display with labels
- **button.py** - UI button implementation

### Key Concepts Demonstrated

- Object-oriented programming with Python classes
- Pygame sprite groups for efficient collision detection
- Game loop architecture (event handling, updating, rendering)
- Dynamic difficulty progression
- State management (game active/inactive states)
- Rectangle-based collision detection and boundary checking

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pygame.git
   cd pygame
   ```

2. **Create a virtual environment (optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. **Install Pygame**
   ```bash
   pip install pygame
   ```

4. **Run the game**
   ```bash
   python alien_invasion.py
   ```

## How to Play

- **Move Left/Right**: Arrow keys or A/D keys
- **Shoot**: Spacebar
- **Start Game**: Click "Play" button or press P
- **Pause/Unpause**: P key (during gameplay)
- **Quit**: Q key or close window

**Objective**: Destroy all aliens before they reach the bottom of the screen or collide with your ship. Dodge alien bullets while shooting. Each cleared fleet increases the difficulty - aliens move faster and shoot more frequently. The game continues indefinitely with unlimited levels - see how high you can score!

**Scoring**: Higher-value aliens are positioned at the top (harder to reach):
- Red aliens: 50 points
- Yellow aliens: 20 points  
- Green aliens: 10 points

**Difficulty Progression**: Every level increases:
- Alien movement speed (10% faster)
- Bullet speed (10% faster)
- Alien fire frequency (10% more frequent)

## What I Learned

- Setting up and managing a Pygame project
- Implementing game physics and collision detection
- Managing game state and user input
- Working with sprite groups for efficient rendering
- Scaling difficulty dynamically
- Organizing code with OOP principles
- Debugging game logic and timing issues

## Requirements

- Python 3.x
- Pygame

## Acknowledgments

This project is based on the Alien Invasion game from [*Python Crash Course, 2nd Edition*](https://nostarch.com/pythoncrashcourse2e) by Eric Matthes. The tutorial provided an excellent foundation for learning Pygame and game development concepts.

