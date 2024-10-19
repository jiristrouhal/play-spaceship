import sys

sys.path.append(".")

from spaceship.trajectory_solver import (
    construct_trajectory,
    initialize_variable_multiset,
    VariableSet,
    VariableMultiset,
)


initial_conditions = VariableSet(1, 1, 0, 10)
print(initial_conditions.to_list())
starting_values = initialize_variable_multiset(1, initial_conditions)


def constraints(v: VariableMultiset):
    return [
        v[1].b - 5,
        v[1].vy,
        v[1].ry,
    ]


result = construct_trajectory(1, starting_values, initial_conditions, constraints, g=1)
