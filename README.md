# Solving the N-Queens Problem

## Brute Force (with a Catch™)

## Backtracking

## Lookahead

## Most-Threatened Heuristic

## Convergence

Provided there exists a solution for the given board size, the fact that the brute-force, backtracking, and lookahead solvers will converge on a solution is easy to show. They explore all possible placements until a solution is found, skipping over only invalid solutions. That the heuristic solver will converge, however, is a bit more interesting to think about.

If a naive implementation of the most-threatened heuristic solver always moves one of the most-threatened queens first, could there exist an infinite loop wherein some subset of threatened queens are continually moved, bringing about live-lock behavior? Yes, absolutely. In the following 6x6 board, no heuristic progress can be made, as there exists a set of unthreatened internal queens:

```
Q - - - - - 
- - Q - - - 
- - - - Q - 
- Q - - - - 
- - - Q - - 
- - - - - Q 
```
The two exterior queens may be placed in any of the four corners, but they will always threaten one another. No solution can be discovered; instead, we've found a local minimum.

Similarly, consider the following board:
<pre>
- - - - - - Q - - - - 
- - - - - - - - - - Q 
- <b>Q</b> - - - - - <b>Q</b> - - - 
- - - - - Q - - - - - 
Q - - - - - - - - - - 
- - Q - - - - - - - - 
- - - - Q - - - - - - 
- - - - - - - - Q - - 
- - - - - - - - - - - 
- - - - - - - - - Q - 
- - - Q - - - - - - - 
</pre>
The most-threatened queens are emboldened, and all other queens are unthreatened. Choosing one of these two problematic pieces for movement, however, places us in a bit of a tricky spot: we cannot do better by moving them, as we've found a local minimum. For this reason, in our implementation we cannot assume that heuristic "progress" can be made on each iteration. Instead, we must instantaneously relax either 1) our placement constraints (`h1`) or 2) our selection constraints (`h2`).

In general, `h1` appears to outperform `h2`. See the following section for supporting data.

## Speed

In general, `h1` > `h2` > `lookahead` > `backtracking` > `brute_force`. Results on my machine are tabulated below.

| `s` | `h1`		| `h2`		  | `lookahead` | `backtracking` | `brute_force` |
| --- | ----------- | ----------- | ----------- | -------------- | ------------- |
| 1   | 0.00		| 0.00		  | 0.00		| 0.00		     | 0.00		   	 |
| ... | ...			| ...		  | ...		  	| ...			 | ...		   	 |
| 8   | 0.03        | 0.04        | 0.01        | 0.03		   	 | 0.07		   	 |
| 9	  | 0.03        | 0.03        | 0.01        | 0.03		     | 0.20		   	 |
| 10  | 0.03        | 0.08        | 0.01        | 0.03		     | 1.74		     |
| 11  | 0.05        | 0.04        | 0.01        | 0.02		     | -			 |
| 12  | 0.05        | 0.04        | 0.05        | 0.07		     | -			 |
| 13  | 0.06        | 0.02        | 0.05        | 0.07		     | -			 |
| 14  | 0.06        | 0.06        | 0.11        | 0.99		     | -			 |
| 15  | 0.06        | 0.04        | 0.12        | 1.12		     | -			 |
| 16  | 0.07        | 0.07        | 0.24        | 18.8		     | -			 |
| 17  | 0.07        | 0.11        | 0.17        | -			     | -			 |
| 18  | 0.08        | 0.06        | 0.64        | -			     | -			 |
| 19  | 0.09        | 0.09        | 0.14        | -			     | -			 |
| 20  | 0.05†	    | 0.09†	      | 2.88        | -			     | -			 |
| 21  | 0.06†	    | 0.09†	      | 0.26        | -			     | -			 |
| 22  | 0.07†	    | 0.10†	      | 28.0        | -			     | -			 |
| 23  | 0.07†	    | 0.15†	      | 0.81        | -			     | -			 |
| 24  | 0.09†	    | 0.15†	      | 9.57        | -			     | -			 |
| 25  | 0.09†	    | 0.18†	      | 1.33        | -			     | -			 |
| 26  | 0.11†	    | 0.20†	      | 10.9        | -			     | -			 |
| 27  | 0.12†	    | 0.22†	      | 13.2        | -			     | -			 |
| ... | ...			| ...		  | ...		  	| ...			 | ...		     |
| 40  | 0.44†	    | 0.57†	      | -		    | -			     | -			 |
| ... | ...			| ...		  | ...		  	| ...			 | ...		     |
| 60  | 2.02††	    | 1.95††	  | -		    | -			     | -			 |
| ... | ...			| ...		  | ...		  	| ...			 | ...		     |
| 80  | 6.60††	    | 7.33††	  | -		    | -			     | -			 |
| ... | ...			| ...		  | ...		  	| ...			 | ...		     |
| 100 | 15.8††	    | 17.4††	  | -		    | -			     | -			 |

* Denotes averages from 10 samples
** Denotes averages from 5 samples
Results from deployment of `lookahead`, `backtracking`, and `brute_force` are not aggregates as a result of these implementations' deterministic nature.

## Usage
Use of `pypy3` is recommended, but the executable `python3` works, as well.
```
pypy3 solvers.py chess_board_size [ [solution_generation_method] ...] [-l board_to_load]
```
Recognized solver type keywords:
- `h1`
- `h2`
- `lookahead`
- `backtracking`
- `brute_force`