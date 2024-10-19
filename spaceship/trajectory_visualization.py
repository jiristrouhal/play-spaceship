import matplotlib.pyplot

from .trajectory_solver import (
    movement,
    VariableMultiset,
    Vector2,
)


N_STEPS = 2000
MIN_DT = 0.01


class TrajectoryVisualization:
    def __init__(self, vals: VariableMultiset, g: float):
        print(vals)
        self._x, self._y = self._simulate_trajectory(vals, g)

    @staticmethod
    def _simulate_trajectory(vals: VariableMultiset, g: float) -> tuple[list[float], list[float]]:
        total_time = sum(v.dt for v in vals)
        if total_time == 0:
            return [], []
        x, y = [], []
        for i in range(1, vals.n_sets):
            v0 = vals[i - 1]
            v1 = vals[i]
            t = 0.0
            dt = max(MIN_DT, vals[i].dt / N_STEPS)
            rvec, vvec = Vector2(v0.rx, v0.ry), Vector2(v0.vx, v0.vy)
            while t < v1.dt + dt:
                r, _ = movement(rvec, vvec, v1.b, g, v1.k, t)
                x.append(r.x)
                y.append(r.y)
                t += dt
        return x, y

    def values(self) -> tuple[list[float], list[float]]:
        return self._x.copy(), self._y.copy()

    def plot(self):
        matplotlib.pyplot.plot(self._x, self._y)
        matplotlib.pyplot.show()
