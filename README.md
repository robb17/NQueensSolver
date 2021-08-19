# Solving the N-Queens Problem

The N-Queens problem is a generalization of the eight-queens puzzle, which was originally published in 1848 as a brain-teaser for fans of chess. It requires the placement of `n` queens onto a chess board of width and length `n` such that no two queens threaten one another. With the exception of `n` = 2 and `n` = 3, solutions exist for all natural numbers.

In this suite several methods for obtaining valid solutions to the problem are presented and implemented, and interesting features of each are discussed.

## Brute Force (with a Catch™)

This one's not all that interesting. That being said, it is quite a bit better than the most naive of solvers, which would simply check all possible placements.

This solver exploits the fact that there can exist at most one queen in a given row and at most one queen in a given column by generating all possible permutations of a list of integers from 0 to `n` - 1, inclusive. If the ordered version of that list gives `x` coordinates for each point on the board, each permutation of that list gives the `y` coordinates for each point on the board. We simply add each piece to the board, starting anew if and only if an invalid board is generated.

## Backtracking

Now we're using our brain. This solver traverses the board row-by-row, greedily placing queens whenever it's the case that no previous placement threatens the current location. If we've placed the requisite number of queens, we're done. If we've traversed to the end of the board, however, and we haven't placed `n` queens, we need to *backtrack*––that is, remove the most-recently added queen.

How do we know where the most-recently added queen is? Well, we can simply maintain a stack of pointers to all the queens we've ever added to the board. So, when we need to backtrack, we pop a queen off that stack and remove it from the board. Then, we begin evaluating spaces *after* that most-recently popped queen, as the algorithm is greedy. More specifically, the most-recently popped queen represents the first place the `i`-th queen could have been placed, so it must be the case that there are suitable locations further along (provided there exists a solution).

As with the prior solver, a few minor optimizations have been implemented. First, on the addition of a queen, the solver immediately jumps to examining the next row. Similarly, columns in which queens have already been placed are summarily skipped. The motivation is the same as above: we know there cannot exist more than one queen in a given row or column.

## Lookahead

Now, we're *really* cooking! Here we traverse the board in the same manner as above, although a new optimization is introduced: lookahead checking. If it's ever the case that the solver reaches a row `r` and some `r'` < `r` does not contain a queen, the solver backtracks. This kind of behavior is very efficient, as it enables us to more quickly discard partial solutions that would ultimately not lead to a valid solution.

## Most-Threatened Heuristic

The cream of the crop. The cat's meow. This solver features an approach that differs widly from that associated with each presented above, and the central tenet is efficiency. Instead of making greedy queen placement after greedy queen placement and revisiting early placements only after expanding on the entire subtree of the guess-and-check space, the idea is to assume that no placement is holy.

More specifically, it involves populating the board with the correct number of queens and attempting to iteratively arrive at a solution by shuffling them around, worst-placements first. So, how does one know which queens are most-horribly placed? Unfortunately, attempting to come up with a metric for this sort of thing is very difficult, but it can be approximated it with a heuristic.

Let's consider the *most-threatened heuristic*. That is, a heuristic that selects for the queens that are most threatened by others (and, because threats are transitive, the queens that are the most threatening). Basic pseudocode is presented below.

<pre>
<b>repeat</b>
	select a most-threatened queen q for relocation
	place the queen in a new location that minimizes the number of threats associated with q
<b>until</b> no more threats
</pre>

Why this type of solver is dramatically more efficient than each of those presented above might not be immediately apparent, but it becomes a bit more intuitive if we think about the puzzle once again as a gigantic tree wherein the root is the unfilled board, and each placement of a queen brings us to a new branch. With each of the backtracking solvers, we're fully exploring each subtree (albeit with a bit of pruning), but in this case we're gracefully dancing from one subtree to the next.

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
The most-threatened queens are emboldened, and all other queens are unthreatened. Choosing one of these two problematic pieces for movement, however, places us in a bit of a tricky spot: we cannot do better by moving them. For this reason, in our implementation we cannot assume that heuristic progress can be made on each iteration. Instead, we must instantaneously relax either 1) our placement constraints (`h1`) or 2) our selection constraints (`h2`).

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
| 11  | 0.05        | 0.04        | 0.01        | 0.02		     | 21.0			 |
| 12  | 0.05        | 0.04        | 0.05        | 0.07		     | -			 |
| 13  | 0.06        | 0.02        | 0.05        | 0.07		     | -			 |
| 14  | 0.06        | 0.06        | 0.11        | 0.99		     | -			 |
| 15  | 0.06        | 0.04        | 0.12        | 1.12		     | -			 |
| 16  | 0.07        | 0.07        | 0.24        | 18.8		     | -			 |
| 17  | 0.07        | 0.11        | 0.17        | -			     | -			 |
| 18  | 0.08        | 0.06        | 0.33        | -			     | -			 |
| 19  | 0.09        | 0.09        | 0.14        | -			     | -			 |
| 20  | 0.05†	    | 0.09†	      | 1.23        | -			     | -			 |
| 21  | 0.06†	    | 0.09†	      | 0.18        | -			     | -			 |
| 22  | 0.07†	    | 0.10†	      | 9.14        | -			     | -			 |
| 23  | 0.07†	    | 0.15†	      | 0.27        | -			     | -			 |
| 24  | 0.09†	    | 0.15†	      | 2.52        | -			     | -			 |
| 25  | 0.09†	    | 0.18†	      | 0.40        | -			     | -			 |
| 26  | 0.11†	    | 0.20†	      | 2.59        | -			     | -			 |
| 27  | 0.12†	    | 0.22†	      | 3.29        | -			     | -			 |
| 28  | 0.15†	    | 0.23†	      | 20.0        | -			     | -			 |
| ... | ...			| ...		  | ...		  	| ...			 | ...		     |
| 40  | 0.44†	    | 0.57†	      | -		    | -			     | -			 |
| ... | ...			| ...		  | ...		  	| ...			 | ...		     |
| 60  | 2.02††	    | 1.95††	  | -		    | -			     | -			 |
| ... | ...			| ...		  | ...		  	| ...			 | ...		     |
| 80  | 6.60††	    | 7.33††	  | -		    | -			     | -			 |
| ... | ...			| ...		  | ...		  	| ...			 | ...		     |
| 100 | 15.8††	    | 17.4††	  | -		    | -			     | -			 |

† Denotes averages from 10 samples.

†† Denotes averages from 5 samples.

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