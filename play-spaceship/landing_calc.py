import dataclasses
from math import sqrt
import datetime

from actions import State, read_state


@dataclasses.dataclass
class SuicideBurn:
    current_time: datetime.datetime
    t_wait: float
    t_burn: float


def calculate_landing() -> tuple[float, float]:
    """Returns the time to wait before thrust and the time for which to thrust (both in seconds)."""
    state = read_state()
    burn = _calculate_suicide_burn(state)
    return burn.t_wait*0.9-1, burn.t_burn*0.85


def _calculate_suicide_burn(state: State) -> SuicideBurn:
    e0 = state.vy**2/2 + state.g*state.y
    b = state.thrust/state.mass
    t_burn = state.time_slowdown * sqrt(2*e0/(b*(b-state.g)))
    t_wait = state.time_slowdown * (state.vy + sqrt(2*e0*(b-state.g)/b))/state.g

    now = datetime.datetime.now()
    dt = (now - state.time).total_seconds()
    return SuicideBurn(now, t_wait=max(0, t_wait-dt), t_burn=max(0, t_burn))
