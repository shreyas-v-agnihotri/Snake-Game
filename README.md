# Retro Snake Game

## Download notes
The actual game itself is run through snake_game.py, though the other files are necessary accessories!

## Inspiration
This was created in just a few hours as part of Dartmouth's Hackathon 2018. We were inspired by the Atari Pong lab we created as part of our introductory CS course at Dartmouth. We loved the idea of making retro games and wanted to try another one.

## What it does
The premise is simple. You are a snake, navigating with WASD, looking to eat as many munchies as possible by redirecting your head. Watch out for the walls and make sure you don't eat yourself!

## How I built it
We used Python and the cs1lib graphics framework developed by Devin Balkcom.

## Challenges I ran into
It was difficult to limit the directions of the snake (if the user presses up and right at the same time, for example) without limiting the users input choices. We decided to allow only the first of a given command within a 0.1 second timeframe to be recognized.

## Accomplishments that I'm proud of
The game is user-friendly and graphically pleasing.

## What I learned
Python is a robust development tool with some functionalities we didn't realize (such as class overriding methods for object equality).

## What's next for Old-School Snake
We hope to return to this project in the future to add more functionality, including 2 players and greater options for user input with regards to the game's settings (such as initial snake length and board size).