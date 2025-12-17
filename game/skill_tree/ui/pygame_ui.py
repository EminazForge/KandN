from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from typing import Dict, Tuple

import pygame

from ..grid import GridState
from ..types import Affinity, Cluster, Connector, NodeType


AFFINITY_COLORS: Dict[Affinity, Tuple[int, int, int]] = {
    Affinity.RED: (220, 70, 70),
    Affinity.BLUE: (70, 120, 220),
    Affinity.YELLOW: (230, 200, 80),
    Affinity.ORANGE: (240, 140, 60),
    Affinity.GREEN: (90, 190, 90),
    Affinity.VIOLET: (160, 90, 200),
}


@dataclass
class Camera:
    x: float = 0.0
    y: float = 0.0
    zoom: float = 1.0

    def world_to_screen(self, wx: float, wy: float) -> Tuple[int, int]:
        return int((wx - self.x) * self.zoom), int((wy - self.y) * self.zoom)

    def screen_to_world(self, sx: int, sy: int) -> Tuple[float, float]:
        return sx / self.zoom + self.x, sy / self.zoom + self.y


class SkillTreeViewer:
    def __init__(self, grid: GridState, width: int = 1200, height: int = 800):
        self.grid = grid
        self.width = width
        self.height = height
        self.camera = Camera(x=-250, y=-200, zoom=1.2)
        self.running = False
        self.dragging = False
        self.last_mouse = (0, 0)

        self.node_size_px = 36
        self.gap_px = 4
        # Make clusters touch: remove outer padding and compute size accordingly
        self.cluster_size_px = 5 * (self.node_size_px + self.gap_px) - self.gap_px
        self.connector_radius = 8

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Skill Tree Grid (Pygame)")
        clock = pygame.time.Clock()

        self.running = True
        while self.running:
            dt = clock.tick(60)
            self._handle_events()

            screen.fill((18, 18, 22))
            self._draw_grid(screen)
            pygame.display.flip()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.dragging = True
                    self.last_mouse = event.pos
                elif event.button == 3:
                    # Right click: attempt to reveal neighbor if clicking a connector
                    self._try_click_connector(event.pos)
                elif event.button == 4:  # wheel up
                    self._zoom_at(event.pos, 1.1)
                elif event.button == 5:  # wheel down
                    self._zoom_at(event.pos, 1/1.1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
                    # First try connector, then node
                    if not self._try_click_connector(event.pos):
                        self._try_click_node(event.pos)
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                mx, my = event.pos
                lx, ly = self.last_mouse
                dx, dy = mx - lx, my - ly
                # Pan inversely with zoom
                self.camera.x -= dx / self.camera.zoom
                self.camera.y -= dy / self.camera.zoom
                self.last_mouse = (mx, my)

    def _zoom_at(self, screen_pos, factor):
        # Zoom relative to cursor position to keep it stable
        sx, sy = screen_pos
        wx_before, wy_before = self.camera.screen_to_world(sx, sy)
        self.camera.zoom = max(0.2, min(3.0, self.camera.zoom * factor))
        wx_after, wy_after = self.camera.screen_to_world(sx, sy)
        self.camera.x += (wx_before - wx_after)
        self.camera.y += (wy_before - wy_after)

    def _draw_grid(self, screen):
        for cluster in self.grid.visible_clusters():
            self._draw_cluster(screen, cluster)

    def _draw_cluster(self, screen, cluster: Cluster):
        cx, cy = cluster.cx, cluster.cy
        # Clusters tile flush without extra spacing
        base_x = cx * (self.cluster_size_px)
        base_y = cy * (self.cluster_size_px)

        # Draw cluster boundary
        top_left = self.camera.world_to_screen(base_x, base_y)
        size = int((self.cluster_size_px) * self.camera.zoom)
        pygame.draw.rect(screen, (60, 60, 70), (*top_left, size, size), width=max(1, int(1 * self.camera.zoom)))

        # Cluster tint background based on bias affinity (low alpha)
        tint_color = (70, 70, 78) if cluster.bias is None else AFFINITY_COLORS[cluster.bias]
        alpha = 45
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((*tint_color, alpha))
        screen.blit(surf, top_left)

        # Draw 5x5 nodes
        for iy in range(5):
            for ix in range(5):
                node = cluster.nodes[iy][ix]
                nx = base_x + ix * (self.node_size_px + self.gap_px)
                ny = base_y + iy * (self.node_size_px + self.gap_px)
                sx, sy = self.camera.world_to_screen(nx, ny)
                size = int(self.node_size_px * self.camera.zoom)
                rect = pygame.Rect(sx, sy, size, size)
                # Determine base color, center is grey; EMPTY uses light grey to indicate no effect
                if node.is_center:
                    base_color = (140, 140, 150)
                elif node.node_type == NodeType.EMPTY:
                    base_color = (180, 180, 190)
                else:
                    base_color = AFFINITY_COLORS[node.affinity]
                # Draw shape based on node type; unassigned nodes are hollow, assigned are filled
                if node.node_type.name == 'SKILL':
                    # Rectangle
                    if node.assigned:
                        pygame.draw.rect(screen, base_color, rect, border_radius=max(2, int(4 * self.camera.zoom)))
                    else:
                        pygame.draw.rect(screen, base_color, rect, width=max(1, int(2 * self.camera.zoom)), border_radius=max(2, int(4 * self.camera.zoom)))
                elif node.node_type.name == 'HABIT':
                    # Triangle (isosceles) pointing up
                    points = [(sx + size // 2, sy), (sx, sy + size), (sx + size, sy + size)]
                    if node.assigned:
                        pygame.draw.polygon(screen, base_color, points)
                    else:
                        pygame.draw.polygon(screen, base_color, points, width=max(1, int(2 * self.camera.zoom)))
                else:
                    # PASSIVE: Circle
                    center = (sx + size // 2, sy + size // 2)
                    radius = max(2, int((size // 2)))
                    if node.assigned:
                        pygame.draw.circle(screen, base_color, center, radius)
                    else:
                        pygame.draw.circle(screen, base_color, center, radius, width=max(1, int(2 * self.camera.zoom)))

        # Draw connectors along edges (hide when assigned since they became real nodes)
        for c in cluster.connectors:
            if c.assigned:
                continue
            cx_world, cy_world = self._connector_world_pos(base_x, base_y, c)
            sx, sy = self.camera.world_to_screen(cx_world, cy_world)
            size = int(self.node_size_px * 0.7 * self.camera.zoom)
            base_color = AFFINITY_COLORS[c.affinity]
            # Render connector using same shapes rules
            if c.node_type == NodeType.SKILL:
                rect = pygame.Rect(sx - size // 2, sy - size // 2, size, size)
                if c.assigned:
                    pygame.draw.rect(screen, base_color, rect, border_radius=max(2, int(4 * self.camera.zoom)))
                else:
                    pygame.draw.rect(screen, base_color, rect, width=max(1, int(2 * self.camera.zoom)), border_radius=max(2, int(4 * self.camera.zoom)))
            elif c.node_type == NodeType.HABIT:
                points = [(sx, sy - size // 2), (sx - size // 2, sy + size // 2), (sx + size // 2, sy + size // 2)]
                if c.assigned:
                    pygame.draw.polygon(screen, base_color, points)
                else:
                    pygame.draw.polygon(screen, base_color, points, width=max(1, int(2 * self.camera.zoom)))
            elif c.node_type == NodeType.EMPTY:
                r = max(2, int(self.connector_radius * self.camera.zoom))
                pygame.draw.circle(screen, (200, 200, 210), (sx, sy), r, width=max(1, int(2 * self.camera.zoom)))
            else:
                r = max(2, int(self.connector_radius * self.camera.zoom))
                if c.assigned:
                    pygame.draw.circle(screen, base_color, (sx, sy), r)
                else:
                    pygame.draw.circle(screen, base_color, (sx, sy), r, width=max(1, int(2 * self.camera.zoom)))

    def _connector_world_pos(self, base_x: int, base_y: int, conn: Connector):
        # Position circles just outside the 5x5 area
        step = self.node_size_px + self.gap_px
        if conn.direction == 'N':
            x = base_x + conn.edge_index * step + self.node_size_px // 2
            y = base_y - self.gap_px - 8
        elif conn.direction == 'S':
            x = base_x + conn.edge_index * step + self.node_size_px // 2
            y = base_y + 5 * step + 8
        elif conn.direction == 'E':
            x = base_x + 5 * step + 8
            y = base_y + conn.edge_index * step + self.node_size_px // 2
        else:  # 'W'
            x = base_x - self.gap_px - 8
            y = base_y + conn.edge_index * step + self.node_size_px // 2
        return x, y

    def _try_click_connector(self, screen_pos):
        # Convert click to world and check proximity to any connector; if within radius, assign and reveal neighbor
        wx, wy = self.camera.screen_to_world(*screen_pos)
        for cluster in self.grid.visible_clusters():
            base_x = cluster.cx * (self.cluster_size_px)
            base_y = cluster.cy * (self.cluster_size_px)
            for conn in cluster.connectors:
                cx_world, cy_world = self._connector_world_pos(base_x, base_y, conn)
                dist2 = (wx - cx_world) ** 2 + (wy - cy_world) ** 2
                if dist2 <= (self.connector_radius * 2) ** 2:
                    self.grid.reveal_neighbor_from_connector(cluster, conn)
                    return True
        return False

    def _try_click_node(self, screen_pos):
        # Toggle assignment for clicked node (simple prototype; pathing rules to be added)
        wx, wy = self.camera.screen_to_world(*screen_pos)
        for cluster in self.grid.visible_clusters():
            base_x = cluster.cx * (self.cluster_size_px)
            base_y = cluster.cy * (self.cluster_size_px)
            for iy in range(5):
                for ix in range(5):
                    nx = base_x + ix * (self.node_size_px + self.gap_px)
                    ny = base_y + iy * (self.node_size_px + self.gap_px)
                    if nx <= wx <= nx + self.node_size_px and ny <= wy <= ny + self.node_size_px:
                        node = cluster.nodes[iy][ix]
                        if not node.is_center:
                            node.assigned = not node.assigned
                        return
