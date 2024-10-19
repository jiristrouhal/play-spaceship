from __future__ import annotations
import dataclasses
from typing import Callable
from math import cos, sin, radians

import scipy.optimize as opt


@dataclasses.dataclass()
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

    def __iter__(self):
        return iter(self._variables)

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
    r, v = movement(Vector2(v0.rx, v0.ry), Vector2(v0.vx, v0.vy), v1.b, g, v1.k, v1.dt)
    return [
        v1.rx - r.x,
        v1.ry - r.y,
        v1.vx - v.x,
        v1.vy - v.y,
    ]


@dataclasses.dataclass
class Vector2:
    x: float
    y: float


def movement(
    r0: Vector2, v0: Vector2, b: float, g: float, k: float, t: float
) -> tuple[Vector2, Vector2]:
    k_rad = radians(k)
    ax = -sin(k_rad) * b
    ay = cos(k_rad) * (b - g)
    v1 = Vector2(v0.x + ax * t, v0.y + ay * t)
    r1 = Vector2(
        r0.x + v0.x * t + 0.5 * ax * t**2,
        r0.y + v0.y * t + 0.5 * ay * t**2,
    )
    return r1, v1


def system(
    invars: list[float],
    n_segments: int,
    g: float,
    *constraints: Callable[[VariableMultiset], list[float]],
) -> list[float]:

    variables = VariableMultiset().from_list(invars, n_segments + 1)
    outvars = []
    for c in constraints:
        outvars.extend(c(variables))
    for i in range(n_segments):
        outvars.extend(segment(i + 1, variables, g))
    return outvars


def initialize_variable_multiset(n_segments: int) -> VariableMultiset:

    sets = []
    for _ in range(n_segments + 1):
        sets.append(VariableSet())
    return VariableMultiset(*sets)


def construct_trajectory(
    n_segments: int,
    starting_values: VariableMultiset,
    g: float,
    *constraints: Callable[[VariableMultiset], list[float]],
) -> VariableMultiset:

    result = opt.fsolve(
        system,
        starting_values.to_list(),
        args=(n_segments, g, *constraints),
        full_output=True,
    )
    print(result[-1])
    var_multiset = VariableMultiset().from_list(result[0], n_segments + 1)
    for i in range(var_multiset.n_sets):
        var_multiset[i].k = var_multiset[i].k % 360
    return var_multiset
