# A\* Algorithm Heuristic Comparison for 8-Puzzle

## Indroduction

### Packages
*Runs seamlessly using these versions as of September 23, 2026. Subject to change according to conda compatibility.*

* python 3.13
* scipy 1.18.1
* numpy 2.5.3

### Experiment
The experiment consists of running A* using each of the three heuristics [misplaced tiles, Manhattan distance, relaxed adjacency], at each depth [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]. 

This was averaged over 100 iterations, with each iteration being a new random puzzle board.

We tracked the average number of nodes generated, and the average effective branching factor.

## Results

### Search-cost and EBF comparison

| d | A\*(h<sub>1</sub>) cost | A\*(h<sub>2</sub>) cost | A\*(h<sub>3</sub>) cost | A\*(h<sub>1</sub>) EBF | A\*(h<sub>2</sub>) EBF | A\*(h<sub>3</sub>) EBF |
|---:|------------------------:|------------------------:|------------------------:|----------------:|----------------:|----------------:|
| 6  |                      24 |                      20 |                      22 |            1.41 |            1.36 |            1.39 |
| 8  |                      47 |                      32 |                      47 |            1.39 |            1.31 |            1.39 |
| 10 |                     116 |                      50 |                     104 |            1.43 |            1.27 |            1.41 |
| 12 |                     266 |                      87 |                     249 |            1.44 |            1.27 |            1.43 |
| 14 |                     642 |                     170 |                     604 |            1.46 |            1.29 |            1.45 |
| 16 |                   1,566 |                     332 |                   1,456 |            1.47 |            1.30 |            1.47 |
| 18 |                   3,842 |                     593 |                   3,393 |            1.49 |            1.31 |            1.47 |
| 20 |                   9,338 |                   1,256 |                   8,254 |            1.49 |            1.33 |            1.48 |
| 22 |                  22,371 |                   2,436 |                  19,173 |            1.50 |            1.33 |            1.49 |
| 24 |                  50,957 |                   4,651 |                  43,342 |            1.50 |            1.34 |            1.49 |
| 26 |                 104,857 |                   9,909 |                  93,757 |            1.49 |            1.35 |            1.49 |
| 28 |                 194,202 |                  20,253 |                 175,866 |            1.48 |            1.36 |            1.48 |

*Comparison of search costs and effective branching factors for 8-puzzle
problems using A\* with h<sub>1</sub> (misplaced tiles), h<sub>2</sub> (Manhattan
distance), and h<sub>3</sub> (relaxed adjacency). Values are averages over 100
puzzles for each solution length \(d\).*

## Implications

The effective branching factors stay close to 1 (1.22-1.50 across all three heuristics, which by R&N's definition make the tested heuristics reasonably good.

For any node n, h<sub>2</sub>(n) ≥ h<sub>3</sub>(n) ≥ h<sub>1</sub>(n), where Manhattan distance dominates both misplaced tiles and relaxed adjacency (e.g. at d=28, h<sub>2</sub> expands roughly 10x fewer nodes than either).

Although Manhattan distance takes longer to compute per node than h<sub>1</sub>/h<sub>3</sub>, the reduction in nodes expanded far outweighs that per-node overhead.

## References

Hansson, O., Mayer, A. E., & Yung, M. M. (1985). Generating admissible heuristics by criticizing solutions to relaxed models (Technical Report CUCS-219-85). Columbia University. https://doi.org/10.7916/D89Z9CW3

Russell, S. J., & Norvig, P. (2020). Artificial intelligence: A modern approach (4th ed.). Pearson.
