from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple


class Affinity(Enum):
    RED = auto()       # Strength / melee
    BLUE = auto()      # Intelligence / magic
    YELLOW = auto()    # Dexterity / precision
    ORANGE = auto()    # Red + Yellow
    GREEN = auto()     # Yellow + Blue
    VIOLET = auto()    # Red + Blue


class NodeType(Enum):
    PASSIVE = auto()
    SKILL = auto()
    HABIT = auto()
    EMPTY = auto()


@dataclass(frozen=True)
class GridPos:
    cx: int  # cluster x
    cy: int  # cluster y
    ix: int  # in-cluster x [0..4]
    iy: int  # in-cluster y [0..4]

    def global_xy(self) -> Tuple[int, int]:
        return (self.cx * 5 + self.ix, self.cy * 5 + self.iy)


@dataclass
class Node:
    affinity: Affinity
    node_type: NodeType
    assigned: bool = False
    is_center: bool = False
    # Minimal payload for now; extend later for stats/skills/habits
    data: Dict[str, object] = field(default_factory=dict)


@dataclass
class Connector:
    # Direction to neighbor cluster and the edge index (0..4)
    # dir is one of: 'N','S','E','W'
    direction: str
    edge_index: int
    affinity: Affinity
    node_type: NodeType
    assigned: bool = False

    def neighbor(self, cx: int, cy: int) -> Tuple[int, int]:
        if self.direction == 'N':
            return (cx, cy - 1)
        if self.direction == 'S':
            return (cx, cy + 1)
        if self.direction == 'E':
            return (cx + 1, cy)
        if self.direction == 'W':
            return (cx - 1, cy)
        raise ValueError(f"Invalid direction {self.direction}")


@dataclass
class Cluster:
    cx: int
    cy: int
    bias: Optional[Affinity]  # None means neutral distribution
    nodes: List[List[Node]]  # 5x5 [iy][ix]
    connectors: List[Connector] = field(default_factory=list)

    def get_node(self, ix: int, iy: int) -> Node:
        return self.nodes[iy][ix]


VisibleKey = Tuple[int, int]  # (cx, cy)
