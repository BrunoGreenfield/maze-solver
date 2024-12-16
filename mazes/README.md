# Creating mazes

### Mazes are made exclusively from 4 simple characters:
 - '#' - Represents a hedge
 - '0' - Represents an empty square that can be moved into
 - 'A' - Represents the starting square
 - 'Z' - Represents the goal square

All mazes must have at least one of all the above characters. Mazes with no solution will still have a goal state, but no path that leads to it from the starting position.

It is important to note that all rows in this maze must include at least one of the following characters: '0', '#'

***
### Below the mazes, descriptive text may be included.

This text must follow the following rules:
 - The following characters must not be used: '0', '#'
 - The text must be on a separate line/row a part of the maze

The program decides whether or not it should count a row of the text file as part of the maze by checking if it contains a '0' or a '#'. Therefore, any row with any one of these characters is counted, and thus should not include description.

***
### Tips on creating mazes:
Use graphical software such as gimp to draw out your maze before hand:
  1. Create a canvas the size of your maze (e.g. 10*10 pixels), and set the background as black.
  2. Then, simply carve your path by colouring squares white.
  3. Finally, create a text file and go through each square in each row of your visualisation, typing the '#' for a black square and the '0' for a white square.