import sys

sys.path.append(".")

from spaceship.trajectory_solver import (
    construct_trajectory,
    initialize_variable_multiset,
    movement,
    VariableMultiset,
)
from spaceship.trajectory_visualization import TrajectoryVisualization


starting_values = initialize_variable_multiset(1)
starting_values[0].rx = 0
starting_values[0].ry = 0
starting_values[0].vx = 1
starting_values[0].vy = 1
starting_values[0].b = 1
starting_values[0].k = 1
starting_values[1].rx = 1
starting_values[1].ry = 1
starting_values[1].vx = 1
starting_values[1].vy = 1
starting_values[1].b = 15
starting_values[1].k = 90
starting_values[1].dt = 1


def constraints(v: VariableMultiset):
    return [
        v[0].vx - 10,
        v[0].vy - 10,
        v[0].rx,
        v[0].ry,
        v[0].b,
        v[0].k,
        v[0].dt,
        v[1].b - 15,
        v[1].rx - 100,
        v[1].ry,
    ]


G = 10


result = construct_trajectory(1, starting_values, G, constraints)


vis = TrajectoryVisualization(result, G)
vis.plot()
