# maze-solver

A 2D maze solver to explore the effectiveness of different search algorithms.

## Getting started:
1. Clone the repository with:
   ```bash
   git clone https://github.com/BrunoGreenfield/maze-solver.git
   ```
2. Navigate into the main 'maze-solver' directory where you will find `main.py`. This is all of the code for the maze solver.

## Usage:
maze-solver is a terminal based program. To run it, ensure you have python installed. Run it with:
```bash
python main.py --flags
```
Replace `--flags` with your appropriate flags. To decide these, here's a flag guide:

### Mandatory flags:
 - `-n` - This is followed by path to the maze file: e.g. `-n mazes/maze1.txt`
 - `-a` - This is followed by the name of the algorithm you wish to use (`dfs`, `bfs`, `gbfs`, `a*`)

### Optional flag:
`-d` - If used, this flag can provide a delay (in seconds) between each move. This way, you can see exactly how the algorithms are solving the mazes. The following demo was created with the command `python main.py -n mazes/maze2.txt -a dfs -d 0.2`

You can see examples of this being used below in the 'Meet the Algorithms' section.

If no delay is provided (i.e. `-d` is not provided), the program will only output the final solved state.

## The algorithms:

### Non-heuristic based:

| Depth-First Search:                                              | Breadth-First Search:                                            |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| ![DFS delayed maze3.gif](example-gifs/DFS%20delayed%20maze3.gif) | ![BFS delayed maze3.gif](example-gifs/BFS%20delayed%20maze3.gif) |

### Heuristic based:

| Greedy Best-First Search:                                          | A* Search:                                                             |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| ![GBFS delayed maze3.gif](example-gifs/GBFS%20delayed%20maze3.gif) | ![A_star delayed maze3.gif](example-gifs/A_star%20delayed%20maze3.gif) |

## Final words...

Download and have fun playing around with different algorithms and different mazes! Maybe create your own! If you need help creating mazes, consult the README located in the `mazes` directory. Happy coding!