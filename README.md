# Platformer

This is a 2-D platformer game developed by group of students as a part of python course. The game uses the Pygame library for creating the game environment and handling user input. In this game, players navigate a character through a level, avoiding obstacles and collecting items to reach the end.

## Team Members

- Prashant Jaitly
- Pradeep Kumar
- Simran Bhardwaj
- Rishabh Raj

## Features

- Character Movement: Players can move the character left, right, and jump using the arrow keys.
- Obstacles: Collide with obstacles to lose health or restart the level.
- Item Collection: Collect items such as coins or power-ups to increase score or abilities.
- Smooth Jumping and Physics: Gravity and smooth jumping mechanics for a fluid platforming experience.

## Technology Used

- Python 3.x – The programming language used for development.
- Pygame – A library used for creating game window, handling user input, rendering graphics, and managing game events.
- Pytmx – For loading map into the game.
- Tiled (Map Editor) - For creating the map for the game.

## Installation

#### Prerequisites

Ensure you have Python 3.x installed. You can check your version by running:\

```bash
  python --version
```

If you don't have Python installed, download it from [python.org](https://www.python.org).

#### Clone the Repository

Clone the project repository to your local machine:

```bash
  git clone https://github.com/rishabh8n/python-project.git
```

#### Install Dependencies

Navigate to the project folder and install Pygame and Pytmx:

```bash
  cd project-name
  pip install pygame-ce
  pip install pytmx
```

#### Running the Game

Once you have the dependencies set up, run the game by executing:

```bash
  python code/main.py
```

This will open the game window, and you can start playing immediately.

## Project Structure

Here's an overview of the project structure:

```bash
  /project-name
  /graphics              # contains all the assets

  /data
    /tsx                 # contains tiles data
    /tmx                 # contains level data

  /code
    AllSprites.py        # rendering sprites to the screen
    main.py              # entry point
    config.py            # basic configurations
    Game.py              # Main game loop and logic
    Level.py             # Level handling and creation
    Obstacle.py          # Obstacle class and behaviour
    Player.py            # Player class and movement
    sprites.py           # handling sprites and animation
    support.py           # for importing assets
    ui.py                # showing scores and health status

  README.md              # Project Documentation
```
