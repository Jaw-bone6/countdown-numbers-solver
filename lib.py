from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
from pprint import pprint

"""
Abstract base class for a mathematical expression
"""
@dataclass
class Expression:
    def value(self):
        raise NotImplementedError()

"""
Base class for binary (2-argument) operations. For the purpose of this program,
"+", "-", "*", and "/"
"""
class Operation:
    # operator name
    operator: str

    # whether the operands can be swapped without affecting the result, e.g., 2
    # + 3 = 3 + 2, but 2 - 3 != 3 - 2
    commutative: bool

    # calculate result of this operation with given operands
    def calculate(_self, left_value: int, right_value: int) -> int | None:
        raise NotImplementedError()
    
    def __repr__(self):
        return self.operator

class CommutativeOperation(Operation):
    commutative = True

class NonCommutativeOperation(Operation):
    commutative = False

class Add(CommutativeOperation):
    operator = "+"
    
    def calculate(_self, left_value: int, right_value: int) -> int | None:
        return left_value + right_value

class Subtract(NonCommutativeOperation):
    operator = "-"

    def calculate(_self, left_value: int, right_value: int) -> int | None:
        # one may not use negative numbers in the Countdown numbers game, so
        # subtractions resulting in negative results are rejected
        if right_value >= left_value:
            return None

        return left_value - right_value

class Multiply(CommutativeOperation):
    operator = "*"

    def calculate(_self, left_value: int, right_value: int) -> int | None:
        return left_value * right_value

class Divide(NonCommutativeOperation):
    operator = "/"

    def calculate(_self, left_value: int, right_value: int) -> int | None:
        # reject division by zero
        if right_value == 0:
            return None

        # reject non integer division
        if left_value % right_value != 0:
            return None

        return left_value // right_value

"""
Represents an operator with two operands, forming a complete mathematical
expression which can recursively hold other expressions as operands
"""
@dataclass
class Operator(Expression):
    operation: Operation
    left_operand: Expression
    right_operand: Expression

    # recursively evaluate the values of the operands and then evaluate the
    # root expression based on its operation
    def value(self) -> int | None:
        value_left = self.left_operand.value()
        value_right = self.right_operand.value()
        return self.operation.calculate(value_left, value_right)

    def __repr__(self) -> str:
        return f"({self.left_operand} {self.operation} {self.right_operand})"

"""
A single number as a complete mathematical expression, e.g., 3

The leaves of the binary tree which represents the overall expression and thus
the point where recursive evaluation stops
"""
@dataclass
class Literal(Expression):
    literal_value: int

    def value(self):
        return self.literal_value

    def __repr__(self) -> str:
        return str(self.literal_value)

"""
The "available expressions" which can be used. At the start of a game, it would
be a list of literals which can then be combined into expressions which would
then be available for the next step.

For example, if the available numbers are [25, 100, 2, 4, 7, 8], the first
search step may be adding 25 and 4 in which case the state would be updated to
[(25 + 4), 100, 2, 7, 8].

The end goal of this program is to combine available expressions in the state
until an expression which evaluates to the target number is found, or until all
possibilities have been exhausted, demonstrating that no solution exists.
"""
@dataclass
class State:
    nodes: List[Expression]

"""
Search heuristic to speed up search.

It is the sum of all the differences of the value of each expression in the
state and the target. The smaller the sum, the more "promising" the state, the
earlier the search looks at it.
"""
def heuristic(state: State, target_number: int) -> int:
    sum_difference = 0

    for expr in state.nodes:
        sum_difference += abs(expr.value() - target_number)

    return sum_difference

"""
Take a problem state and produce all possibilities for the next search step
when using a commutative operation.

That is, each search step involves combining all possible combinations of two
elements of the state using each of the four operations.

For commutative operations, only one possible ordering of each operation is
produced to avoid wasting time.

Commutatively iterating [1, 2, 3, 4] and "+" should give you:
    [(1 + 2), 3, 4],
    [(1 + 3), 2, 4],
    [(1 + 4), 2, 3],
    [1, (2 + 3), 4],
    [1, (2 + 4), 3], and
    [1, 2, (3 + 4)]
"""
def commutatively_iterate_state(state: State, operation: Operation) -> List[State]:
    output = list()

    for left_operand_index, left_operand in enumerate(state.nodes):

        # for each operand iterated by the above loop, only iterate though
        # nodes after it to achieve the "single ordering" described above
        for right_operand_index, right_operand in enumerate(state.nodes[left_operand_index + 1:]):
            new_expression = Operator(operation, left_operand, right_operand)

            # if the result of the produced expression is forbidden (negative,
            # non-integer), reject it
            if not new_expression.value():
                continue

            # copy state without the two selected operands
            new_state_nodes = [
                node for i, node in enumerate(state.nodes) 
                if i not in [left_operand_index, right_operand_index + left_operand_index + 1]
            ]

            # add new state node
            new_state_nodes.append(new_expression)
            output.append(State(new_state_nodes))

    return output

"""
Take a problem state and produce all possibilities for the next search step
when using a non-commutative operation.

That is, each search step involves combining all possible combinations of two
elements of the state using each of the four operations.

For non-commutative operations, both orderings of operands are used as they are
not identical.

Non-commutatively iterating [1, 2, 3] and "-" should give you:
    [(1 - 2), 3],
    [(1 - 3), 2],
    [(2 - 1), 3],
    [(2 - 3), 1],
    [(3 - 1), 2],
    [(3 - 2), 1]

N.B.: some of the above possibilities would be ignored due to resulting in a
negative nubmer. There inclusion here is to demonstrate the possibilities which
are checked by this function
"""
def noncommutatively_iterate_state(state: State, operation: Operation) -> List[State]:
    output = list()

    # iteratie all possible pairs of operands
    for left_operand_index, left_operand in enumerate(state.nodes):
        for right_operand_index, right_operand in enumerate(state.nodes):
            # avoid pairing an operand with itself
            if left_operand_index == right_operand_index:
                continue

            new_expression = Operator(operation, left_operand, right_operand)

            # reject new expression if it has a disallowed value
            if not new_expression.value():
                continue

            # copy state without the two selected operands
            new_state_nodes = [
                node for i, node in enumerate(state.nodes) 
                if i not in [left_operand_index, right_operand_index]
            ]
            new_state_nodes.append(new_expression)
            output.append(State(new_state_nodes))

    return output

"""
Take a problem state and produce all possibilities for the next search step,
selecting the correct type of iteration based on the given operation
"""
def iterate_state(state: State, operation: Operation) -> List[State]:
    if operation.commutative:
        return commutatively_iterate_state(state, operation)
    else:
        return noncommutatively_iterate_state(state, operation)

"""
Attempt to solve the given state and achieve the target number, returning None
if no solution exists or returning the solution Expression if found.

This function accepts and returns a lookup list containing all states already
searched. The search is depth-first, meaning that if the state has already been
searched and the solver did not terminate, no solution was found and the state
need not be checked again, saving time. This is important as any given state
may have multiple ways of reaching it which would otherwise be searched
indivdually.
"""
def solve(state: State, target_number: int, lookup: List[State]=list()) -> Tuple[Expression | None, List[State]]:
    # check if the state has more than three expressions and and if the state
    # exists in the lookup. If the state has 3 or fewer nodes, the if statement
    # will short-circuit, preventing the lookup from being checked. This is
    # because, at 3 nodes of fewer, there are so few possibilities to search
    # that checking the lookup would be a waste of time.
    if len(state.nodes) > 3 and state in lookup:
        # if state found in lookup, there is no solution. Return None for no
        # solution and lookup unchanged
        return None, lookup

    state_heuristic_pairs = list()
    
    # iterate state for each operation, calculate heuristic for each new state
    # and populate state_heuristic_pairs with tuples of each state and its
    # heuristic value
    for operation in (Add(), Subtract(), Multiply(), Divide()):
        new_states = iterate_state(state, operation)

        # check if any of the newly iterated states contain an expression
        # evaluating to the target, returning it as the solution
        for new_state in new_states:
            for expression in new_state.nodes:
                if expression.value() == target_number:
                    return expression, lookup

        new_pairs = [(state, heuristic(state, target_number)) for state in new_states]
        state_heuristic_pairs.extend(new_pairs)

    # sort the iterated states by their heuristic values in ascending order.
    # Lower heuristic values are prefered, so this puts the states in
    # descending order of search importance
    sorted_state_heuristic_pairs = sorted(state_heuristic_pairs, key=lambda x: x[1])

    # recursively attempt to solve each of the iterated states
    for next_state, _ in sorted_state_heuristic_pairs:
        result, lookup = solve(next_state, target_number, lookup)

        # if a solution was found, return it
        if result:
            return result, lookup

    # if the above loop terminates without returning, no solution was found.
    # Add this state to the lookup and return none along with the updated
    # lookup
    lookup.append(state)
    return None, lookup

