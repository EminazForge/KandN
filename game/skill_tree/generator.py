from __future__ import annotations

from typing import Dict, List, Optional

from .rng import cluster_rng, weighted_choice, choose_n_unique
from .types import Affinity, Cluster, Connector, Node, NodeType


# Hard-coded distributions

AFFINITY_WEIGHTS_NEUTRAL: Dict[Affinity, float] = {
    Affinity.RED: 1.0,
    Affinity.BLUE: 1.0,
    Affinity.YELLOW: 1.0,
    Affinity.ORANGE: 0.8,
    Affinity.GREEN: 0.8,
    Affinity.VIOLET: 0.8,
}

# Bias maps: when a cluster has an affinity bias, boost related colors
AFFINITY_WEIGHTS_BIASED: Dict[Affinity, Dict[Affinity, float]] = {
    Affinity.RED: {Affinity.RED: 2.2, Affinity.ORANGE: 1.8, Affinity.VIOLET: 1.8},
    Affinity.BLUE: {Affinity.BLUE: 2.2, Affinity.GREEN: 1.8, Affinity.VIOLET: 1.8},
    Affinity.YELLOW: {Affinity.YELLOW: 2.2, Affinity.ORANGE: 1.8, Affinity.GREEN: 1.8},
    Affinity.ORANGE: {Affinity.ORANGE: 2.2, Affinity.RED: 1.6, Affinity.YELLOW: 1.6},
    Affinity.GREEN: {Affinity.GREEN: 2.2, Affinity.BLUE: 1.6, Affinity.YELLOW: 1.6},
    Affinity.VIOLET: {Affinity.VIOLET: 2.2, Affinity.RED: 1.6, Affinity.BLUE: 1.6},
}


NODETYPE_WEIGHTS_BY_AFFINITY: Dict[Affinity, Dict[NodeType, float]] = {
    Affinity.RED: {NodeType.PASSIVE: 2.5, NodeType.SKILL: 1.5, NodeType.HABIT: 1.0, NodeType.EMPTY: 0.6},
    Affinity.BLUE: {NodeType.PASSIVE: 2.2, NodeType.SKILL: 1.7, NodeType.HABIT: 1.1, NodeType.EMPTY: 0.6},
    Affinity.YELLOW:{NodeType.PASSIVE: 2.3, NodeType.SKILL: 1.6, NodeType.HABIT: 1.1, NodeType.EMPTY: 0.6},
    Affinity.ORANGE:{NodeType.PASSIVE: 2.4, NodeType.SKILL: 1.6, NodeType.HABIT: 1.0, NodeType.EMPTY: 0.7},
    Affinity.GREEN: {NodeType.PASSIVE: 2.2, NodeType.SKILL: 1.6, NodeType.HABIT: 1.2, NodeType.EMPTY: 0.7},
    Affinity.VIOLET:{NodeType.PASSIVE: 2.2, NodeType.SKILL: 1.7, NodeType.HABIT: 1.0, NodeType.EMPTY: 0.7},
}


def _affinity_weights_for_bias(bias: Optional[Affinity]) -> Dict[Affinity, float]:
    base = dict(AFFINITY_WEIGHTS_NEUTRAL)
    if bias is None:
        return base
    boosts = AFFINITY_WEIGHTS_BIASED.get(bias, {})
    for a, w in boosts.items():
        base[a] = base.get(a, 0.0) + w
    return base


def _pick_affinity(rng, bias: Optional[Affinity]) -> Affinity:
    weights_map = _affinity_weights_for_bias(bias)
    items = list(weights_map.keys())
    weights = [weights_map[a] for a in items]
    return weighted_choice(rng, items, weights)


def _pick_node_type(rng, affinity: Affinity) -> NodeType:
    m = NODETYPE_WEIGHTS_BY_AFFINITY[affinity]
    items = list(m.keys())
    weights = [m[k] for k in items]
    return weighted_choice(rng, items, weights)


def _make_connectors(rng, bias: Optional[Affinity]) -> List[Connector]:
    # Choose 2-6 connectors placed along edges, ensure some variety
    sides = ['N', 'S', 'E', 'W']
    count = int(rng.random() * 5) + 2  # 2..6
    connectors: List[Connector] = []
    for _ in range(count):
        side = weighted_choice(rng, sides, [1, 1, 1, 1])
        edge_index = int(rng.random() * 5)  # 0..4
        # The connector is a real node of the neighbor cluster; its affinity will bias that cluster
        a = _pick_affinity(rng, bias)
        nt = _pick_node_type(rng, a)
        c = Connector(direction=side, edge_index=edge_index, affinity=a, node_type=nt, assigned=False)
        # Avoid exact duplicates
        if all(not (x.direction == c.direction and x.edge_index == c.edge_index) for x in connectors):
            connectors.append(c)
    return connectors


def generate_cluster(world_seed: int, cx: int, cy: int, bias: Optional[Affinity]) -> Cluster:
    rng = cluster_rng(world_seed, cx, cy)
    nodes: List[List[Node]] = []
    for iy in range(5):
        row: List[Node] = []
        for ix in range(5):
            a = _pick_affinity(rng, bias)
            nt = _pick_node_type(rng, a)
            is_center = (cx == 0 and cy == 0 and ix == 2 and iy == 2)
            # Center node is a neutral grey and marked assigned
            node = Node(affinity=a, node_type=nt, assigned=is_center, is_center=is_center)
            row.append(node)
        nodes.append(row)

    connectors = _make_connectors(rng, bias)
    return Cluster(cx=cx, cy=cy, bias=bias, nodes=nodes, connectors=connectors)
