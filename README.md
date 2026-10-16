# What is this?

This is a solver for the "numbers game" featured on the British game show
"Countdown". Given any problem, it will find a solution if one exists or
exhaust all possibilities and find no solution.

# How does the game work?

In the numbers game, contestants are given six numbers to use as well as a
3-digit target number. The goal is to produce the target number using only the
six given numbers and the four basic operations of addition, subtraction,
multiplication, and division. Intermediary numbers must be positive integers at
all stages. Each number can only be used once.

For example, given the numbers 25, 50, 2, 6, 9, and 1, and the target number
113, a solution could be (25 * 9 + 1) / 2.

While most problems have many possible solutions, you need only find one and
need not find the most "efficient" (this is, the one which uses the fewest
numbers).

# How does the solver work?

The solver treats the game like a tree with the original 6 numbers as the root
node where each node's children are all possible, allowed combinations of its
operands. The solver performs a greedy, heuristic-based pre-order depth-first
search on the tree until either a problem state containing an expression
evaluating to the target number is found or all branches are exhausted without
finding such an expression, in which case there is no solution.

The heuristic is simple, summing the absolute differences between each
expression in the problem state and the target and prioritising states with the
lowest heuristic scores.

# How do I use the solver?

Clone this repo.

Build the virtual environment.

## Venv {.tabset}

### Linux

```python3 -m venv .venv```

```source .venv/bin/activate```

```pip install -r requirements.txt```

### Windows

## {-}

Once the required packages are installed, the program can be run. The solver
exposes a simple web interface made with Streamlit.

```streamlit run main.py```

This should open a browser window. If not, open either of the links it outputs
when run.
