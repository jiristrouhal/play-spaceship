import sys

sys.path.append(".")

from spaceship.trajectory_solver import (
    construct_trajectory,
    initialize_variable_multiset,
    VariableMultiset,
)


starting_values = initialize_variable_multiset(1)
starting_values[0].rx = 0
starting_values[0].ry = 0
starting_values[0].vx = 1
starting_values[0].vy = 1
starting_values[0].b = 0
starting_values[0].k = 1
starting_values[1].rx = 1
starting_values[1].ry = 0
starting_values[1].vx = 1
starting_values[1].vy = 1
starting_values[1].b = 0
starting_values[1].k = 1
starting_values[1].dt = 1


def constraints(v: VariableMultiset):
    return [
        v[0].vx - v[0].vy,
        v[0].rx,
        v[0].ry,
        v[0].b,
        v[0].k,
        v[0].dt,
        v[1].k,
        v[1].b,
        v[1].rx - 100,
        v[1].ry,
    ]


result = construct_trajectory(1, starting_values, constraints, g=1)

