# Alien Invasion

A classic arcade-style space shooter game built with Python and the Pygame library, following the project from *Python Crash Course* by Eric Matthes.

## About This Project

This project was completed as part of my Python learning journey, following the comprehensive tutorial in *Python Crash Course*. It demonstrates fundamental game development concepts and object-oriented programming principles in Python.

## Game Features

- **Player-controlled spaceship** with left/right movement
- **Alien fleet** that moves across and down the screen
- **Bullet system** with limited ammunition (3 bullets at a time)
- **Collision detection** between bullets and aliens
- **Scoring system** with high score tracking
- **Progressive difficulty** - game speeds up as you clear alien fleets
- **Lives system** - 3 ships per game
- **Level progression** - displays current level
- **Play button** to start and restart the game


### Core Components

- **alien_invasion.py** - Main game loop and event handling
- **ship.py** - Player ship class with movement logic
- **alien.py** - Alien sprite class with fleet behavior
- **bullet.py** - Bullet sprite class and physics
- **settings.py** - Centralized game configuration and dynamic difficulty scaling
- **game_stats.py** - Game state and statistics tracking
- **scoreboard.py** - Score display
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
- **Quit**: Q key or close window

**Objective**: Destroy all aliens before they reach the bottom of the screen or collide with your ship. Each cleared fleet increases the difficulty.

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

