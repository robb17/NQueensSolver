# Solving the N-Queens Problem

## Brute Force (with a Catch™)

## Backtracking

## Lookahead

## Most-Threatened Heuristic

## Speed

In general, `brute_force` < `backtracking` < `lookahead` < `heuristic`. Results on my machine are tabulated below.

| `s` | `heuristic` | `lookahead` | `backtracking` | `brute_force` |
| --- | ----------- | ----------- | -------------- | ------------- |
| 1   | 0.00		| 0.00		  | 0.00		   | 0.00		   |
| ... | ...			| ...		  | ...			   | ...		   |
| 8   | 0.03        | 0.01        | 0.03		   | 0.07		   |
| 9	  | 0.03        | 0.01        | 0.03		   | 0.20		   |
| 10  | 0.03        | 0.01        | 0.03		   | 1.74		   |
| 11  | 0.06        | 0.01        | 0.02		   | -			   |
| 12  | 0.04        | 0.05        | 0.07		   | -			   |
| 13  | 0.04        | 0.05        | 0.07		   | -			   |
| 14  | 0.08        | 0.11        | 0.99		   | -			   |
| 15  | 0.05        | 0.12        | 1.12		   | -			   |
| 16  | 0.06        | 0.24        | 18.8		   | -			   |
| 17  | 0.05        | 0.17        | -			   | -			   |
| 18  | 0.12        | 0.64        | -			   | -			   |
| 19  | 0.11        | 0.14        | -			   | -			   |
| 20  | 0.09	    | 2.88        | -			   | -			   |
| 21  | 0.06	    | 0.26        | -			   | -			   |
| 22  | 0.08	    | 28.0        | -			   | -			   |
| ... | ...			| ...		  | ...			   | ...		   |
| 40  | 0.65	    | -		      | -			   | -			   |
| ... | ...			| ...		  | ...			   | ...		   |
| 60  | 1.45	    | -		      | -			   | -			   |
| ... | ...			| ...		  | ...			   | ...		   |
| 80  | 5.24	    | -		      | -			   | -			   |
| ... | ...			| ...		  | ...			   | ...		   |
| 100 | 10.8	    | -		      | -			   | -			   |

## Convergence

Provided there exists a solution for the given board size, the fact that the brute-force, backtracking, and lookahead solvers will converge on a solution is easy to show. They explore all possible placements until a solution is found, skipping over only invalid solutions. That the heuristic solver will converge, however, is a bit more interesting to think about.

Because the solver always moves one of the most-threatened queens first, could there exist an infinte loop wherein some subset of threatened queens are continually moved, bringing about live-lock behavior? Certainly such an event could occur if the same queen was always selected for re-placement.

## Usage
Use of `pypy3` is recommended, but the executable `python3` works, as well.
```
pypy3 solvers.py chess_board_size [ [solution_generation_method] ...]
```
Recognized solution keywords:
- `heuristic`
- `lookahead`
- `backtracking`
- `brute_force`