# Snake Game

This is a classic implementation of the Snake game built using Python and Pygame. 

Snake is a game, where the player controls the snake (displayed as a growing line)
with the objective of collecting food from the game board.  
The snake eating food gives the player points and makes the snake grow longer.  
The snake has to grow and survive as long as possible without colliding into 
the borders or itself, which gets increasingly harder as 
the snake takes up more and more space on the game board.

![Snake Game Screenshot](https://via.placeholder.com/800x600?text=Screenshot+Coming+Soon)

## Game Features

* **Gameplay**  
The goal of the game is to navigate the snake through the game area and guide it towards food.
Snake grows each time it reaches a food block. 
The game becomes increasingly harder in time as the snake grows and takes up a bigger area of the game board,
while still having to avoid colliding into the borders and its own body.

* **Food Generation**  
Food items appear randomly in the game area one by one. Each time the snake eats one, another will appear, 
until the snake takes up all the room on the board - leaving no room for new foods to be generated.  
Eating the foods causes the snake to grow longer and score points.

* **Collision Detection**  
The game will end, once the snake either runs into a border or crashes into itself.  
The snake can't directly backwards, as it would cause self collision. 
The user can try to navigate the snake in the opposite direction, however the snake will not respond to this.

* **Winning & Losing**  
Winning the game of snake is hard. 
The game will be won, once the snake takes up all the space on the game board.  
The current version of the game, will not end if the snake reaches the field's maximum capacity, 
and lets the player keep moving the snake around, however, no more food can be generated as 
there won't be sufficient space. Once the snake incurs a collision, the game will end
with a winning status.  
The game will be lost if a collision is detected (with a border or the snake's own tail) any earlier,
than the snake reaching the maximum possible length.

* **Pause & Resume**  
The game supports pausing and resuming, allowing players to take breaks without losing their progress. 

* **Score Tracking**  
The game keeps track of the ongoing game's score and stores the gaming session's high score as well, 
to give the player a goal to beat. Both are displayed at the top of the screen. 
Scores are not stored permanently - once the game is closed, the scores will be lost

* **Color Customization**  
The game has 4 distinct snake themed color schemes to customize the snake's and its foods' visual appearance.  
The 3 themes, which have been added in addition to the default theme, have been included in the game as easter eggs 
(or should it be called snake egg `;)`). They can be toggled with specific keyboard keys, however 
the game UI does not mention them, much less include instructions for accessing them.  

  * **Default color scheme** provides the classic and nostalgic UX of snake game with a green snake and red foods.
  * **Python color scheme** is inspired by the Python programming language logo as the game is written in it, and 
      it doubles as a well-known snake species. 
      The snake is striped with the blue and yellow colors of the logo, and 
      the food items are white, just like the eyes of the snakes on the logo.
  * **Ekans color scheme** is a theme inspired by the snake Pokémon Ekans, whose name spells snake backwards.
      The color palette consists of a purple snake who has a yellow rattle tail. 
      The food is the color of the shiny variation of Ekans, which is green and is a very rare variant of Ekans.
  * **Slytherin color scheme** implements the colors of the Harry Potter Slytherin house (silver and green).
      The Slytherin mascot is a silver serpent with green eyes, and to represent it in the game, 
      the color theme incorporates a silver snake with a green head. 
      The food is colored gold, to represent the Golden Snitch.

## Game Controls

The game is controlled via keyboard buttons.
* **Movement**
  * Use the arrow keys (`←`, `↑`, `→`, `↓`) to control the direction of the snake and guide it towards food.
  * Snake, which is longer than a singular block can't move back in 
    the opposite direction of the direction it is currently moving in, 
    as it would cause the snake to collide into itself.
* **Pausing and Resuming the Game**
  * Pause - Press `Esc` to pause the game.
  * Resume - Press `Enter` or `Space` to resume to the game.
* **Restart and Quit**
  * Start a New Game - Press `S` to start a new game.
  * Quit the Gae - Press `Q` to quit the game.
* **Color Schemes**
  * Ekans Color Scheme - Press `E` to activate the Pokémon Ekans color scheme with 
    a yellow-tailed purple snake and green food.
  * Python Color Scheme - Press `P` to switch to the Python color scheme with a blue and yellow striped snake.
  * Slytherin Color Scheme - Press `Z` to use the Harry Potter Slytherin house color scheme with 
    a silver snake, which has a green head and gold food.
  * Default Color Scheme - Press `Delete` to revert to the default color scheme with a classic green snake and red food.

## Starting the Game

To play the Snake Game, you'll need to have Python installed on your machine along with the Pygame library. Follow these steps to get started:

### Prerequisites

- **Python:** You can download the latest version of Python from the official [Python website](https://www.python.org/downloads/).
- **Pygame:** Install Pygame using pip. Open your terminal or command prompt and run:

```bash
pip install pygame
```

### Running the Game

Run the game by executing the following command from your terminal or command prompt: 

```bash
python snake-game.py
```

