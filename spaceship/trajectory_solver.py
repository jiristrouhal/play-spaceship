from __future__ import annotations
import dataclasses
from typing import Callable
from math import cos, sin

import scipy.optimize as opt


@dataclasses.dataclass(frozen=True)
class VariableSet:
    vx: float = 0
    vy: float = 0
    rx: float = 0
    ry: float = 0
    b: float = 0
    k: float = 0
    dt: float = 0

    @classmethod
    def n_vars(cls) -> int:
        return 7

    def to_list(self) -> list[float]:
        return [getattr(self, slot) for slot in self.__dict__]

    @staticmethod
    def from_list(vars: list[float]) -> VariableSet:
        return VariableSet(*vars)


class VariableMultiset:
    def __init__(self, *variables: VariableSet):
        self._variables = list(variables)

    @property
    def n_sets(self) -> int:
        return len(self._variables)

    def to_list(self) -> list[float]:
        return [var for v in self._variables for var in v.to_list()]

    @staticmethod
    def from_list(vars: list[float], n_sets: int) -> VariableMultiset:

        if len(vars) % VariableSet.n_vars() != 0:
            raise ValueError(
                f"The number of input values ({len(vars)}) is not a multiple of the number of "
                f"the number of variables in a VariableSet ({VariableSet.n_vars()})."
            )

        if len(vars) / VariableSet.n_vars() != n_sets:
            raise ValueError(
                f"The number of variables in the input values ({len(vars)}) does not correspond "
                f"to the required number of VariableSets ({n_sets})."
            )
        return VariableMultiset(
            *(
                VariableSet.from_list(vars[i : i + VariableSet.n_vars()])
                for i in range(0, len(vars), VariableSet.n_vars())
            )
        )

    def __str__(self) -> str:
        return "\n".join(str(v) for v in self._variables)

    def __getitem__(self, index: int) -> VariableSet:
        return self._variables[index]


def segment(index: int, variables: VariableMultiset, g: float) -> list[float]:
    if not (0 < index < variables.n_sets):
        raise ValueError(f"Index {index} must be in range [1, {variables.n_sets}].")
    i = index
    v1 = variables._variables[i]
    v0 = variables._variables[i - 1]
    ax = -sin(v1.k) * v1.b
    ay = cos(v1.k) * (v1.b - g)
    return [
        v1.vx - (v0.vx + ax * v1.dt),
        v1.vy - (v0.vy + ay * v1.dt),
        v1.rx - (v0.rx + v0.vx * v1.dt + ax * v1.dt**2 / 2),
        v1.ry - (v0.ry + v0.vy * v1.dt + ay * v1.dt**2 / 2),
    ]


def initial_conditions(values: VariableSet) -> list[float]:
    return values.to_list()


def system(
    invars: list[float],
    n_segments: int,
    initial_conditions: VariableSet,
    constraints: Callable[[VariableMultiset], list[float]],
    g: float,
) -> list[float]:

    variables = VariableMultiset().from_list(invars, n_segments + 1)
    outvars = []
    outvars.extend(initial_conditions.to_list())
    for i in range(n_segments):
        outvars.extend(segment(i + 1, variables, g))
    outvars.extend(constraints(variables))
    print(outvars)
    return outvars


def initialize_variable_multiset(
    n_segments: int, initial_conditions: VariableSet
) -> VariableMultiset:

    sets = [initial_conditions]
    for _ in range(n_segments):
        sets.append(VariableSet())
    return VariableMultiset(*sets)


def construct_trajectory(
    n_segments: int,
    starting_values: VariableMultiset,
    initial_conditions: VariableSet,
    constraints: Callable[[VariableMultiset], list[float]],
    g: float,
) -> VariableMultiset:

    result = opt.fsolve(
        system,
        starting_values.to_list(),
        args=(n_segments, initial_conditions, constraints, g),
    )
    return VariableMultiset.from_list(result, n_segments + 1)
