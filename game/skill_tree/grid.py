from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from .generator import generate_cluster
from .types import Affinity, Cluster, Connector


Coord = Tuple[int, int]


@dataclass
class GridState:
    world_seed: int
    clusters: Dict[Coord, Cluster] = field(default_factory=dict)

    def ensure_origin(self) -> None:
        if (0, 0) not in self.clusters:
            # Origin has neutral bias
            self.clusters[(0, 0)] = generate_cluster(self.world_seed, 0, 0, bias=None)

    def get_cluster(self, cx: int, cy: int) -> Optional[Cluster]:
        return self.clusters.get((cx, cy))

    def reveal_neighbor_from_connector(self, src_cluster: Cluster, connector: Connector) -> Cluster:
        # Compute neighbor coords from connector
        ncx, ncy = connector.neighbor(src_cluster.cx, src_cluster.cy)
        if (ncx, ncy) not in self.clusters:
            # New cluster inherits bias from connector affinity
            self.clusters[(ncx, ncy)] = generate_cluster(self.world_seed, ncx, ncy, bias=connector.affinity)
        neighbor = self.clusters[(ncx, ncy)]
        # Map connector onto neighbor border node and mark assigned
        if connector.direction == 'N':
            ix, iy = connector.edge_index, 4
        elif connector.direction == 'S':
            ix, iy = connector.edge_index, 0
        elif connector.direction == 'E':
            ix, iy = 0, connector.edge_index
        else:  # 'W'
            ix, iy = 4, connector.edge_index

        node = neighbor.get_node(ix, iy)
        node.affinity = connector.affinity
        node.node_type = connector.node_type
        node.assigned = True

        connector.assigned = True
        return neighbor

    def visible_clusters(self):
        return list(self.clusters.values())
