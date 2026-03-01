"""Domain models for recorded mouse automation scenarios."""

from dataclasses import dataclass
from enum import Enum
from typing import List


class MouseEventType(Enum):
    MOVE = "move"
    LEFT_CLICK = "left_click"


@dataclass(frozen=True)
class RecordedEvent:
    event_type: MouseEventType
    timestamp: float
    x: int
    y: int


Scenario = List[RecordedEvent]
