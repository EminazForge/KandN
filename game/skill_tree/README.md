# Skill Tree Grid System

A semi-random, infinite 2D skill grid composed of aligned 5x5 clusters. The player starts at the center of the origin cluster and expands the visible world by pathing onto connector nodes that reveal neighboring clusters. Clusters bias node affinities based on the connector that spawned them.

## Overview
- Grid of clusters: each cluster is 5x5 nodes.
- Start at origin cluster (0,0), center cell (2,2).
- Connectors: special nodes just outside a cluster’s border that, when taken, reveal/generate the adjacent cluster.
- Infinite layout: clusters tile perfectly as a large super-grid.
- Affinities: Red (Strength), Blue (Intelligence), Yellow (Dexterity), plus mixed Orange (R+Y), Green (Y+B), Violet (R+B).
- Node types: Passive (+stats), Skill (active skills), Habit (automation-like behaviors, e.g., “use potion when ...”).

## Terminology
- Node: a single selectable point on the grid with an affinity and one effect (passive/skill/habit).
- Cluster: a 5x5 block of nodes; has an overall affinity bias.
- Connector: a special node bordering a cluster that unlocks/generates a neighbor cluster when traversed.
- Visible: rendered and interactable in the UI; generated and known to the player.

## Coordinates
- Cluster coords: `(cx, cy)` integers in world space.
- In-cluster coords: `(ix, iy)` where `ix, iy ∈ [0..4]`.
- Global node coords (canonical): `(gx, gy) = (cx*5 + ix, cy*5 + iy)`.
- Start: `(cx, cy, ix, iy) = (0, 0, 2, 2)`.

## Generation Rules
- Deterministic RNG seeded by `(world_seed, cx, cy)` so clusters are reproducible but infinite.
- Cluster affinity derived from the connector used to spawn it (e.g., Orange connector → Orange-biased cluster).
- Affinity bias controls probabilities of node affinities in that cluster (still allowing all types to appear).
- Connectors per cluster: random count within bounds (e.g., 2–6), distributed along outside edges so they point to undiscovered neighbors.
- Skills/Habits appear at weighted frequencies per affinity; passives are the backbone.

## Affinity System
- Base affinities: Red (Strength/melee), Blue (Intelligence/magic), Yellow (Dexterity/precision).
- Mixed: Orange (R+Y), Green (Y+B), Violet (R+B).
- Bias: In Orange clusters, Orange/Red/Yellow are more common; others still possible.

## Node Types
- Passive: stat bonuses (e.g., +5 STR, +10 HP). Stackable and straightforward.
- Skill: grants an active ability (e.g., Tackle, Fireball) that other systems can equip/use.
- Habit: automation-like triggers (e.g., use potion under condition); separate execution context from Skills.

## Visibility & Pathing
- Player can select nodes reachable via valid pathing from currently visible clusters.
- Taking a connector reveals/generates the adjacent cluster; the cluster becomes visible and interactable.
- Only visible clusters render in UI; RNG deterministically defines non-visible clusters but they are not generated until revealed.

## UI Requirements
- Mouse input: panning, smooth zooming, hover tooltips, node selection.
- Visuals: show cluster boundaries, connector nodes, selected path, and reachable highlights.
- Performance: virtualize rendering so only visible region draws.

## Modules & APIs (planned)
- `types.py`: dataclasses for `Affinity`, `NodeType`, `Node`, `Cluster`, `GridPos`.
- `rng.py`: seeded RNG helpers keyed by `(world_seed, cx, cy)`.
- `generator.py`: cluster generation by affinity bias, connector placement, node distributions.
- `grid.py`: discovery state, neighbor revealing, pathing rules, reachability.
- `effects.py`: application of node effects (passives, skills, habits) to character.
- `persist.py`: save/load of discovered clusters and node picks.
- `ui/`: view + controller for pan/zoom, selection, tooltips; pluggable backend (e.g., Qt/PySide6, Pygame, DearPyGui).
- `demo.py`: minimal launcher to showcase navigation and revealing.

## Persistence
- Persist: discovered clusters, selected nodes, player position, world seed.
- Rebuild visible graph from persisted state on load.

## Testing Plan
- Generation: deterministic reproducibility per `(seed, cx, cy)`.
- Distribution: affinity bias adheres to configured weights within tolerance.
- Connectivity: connectors correctly map to neighbor clusters; no gaps.
- Pathing: only reachable nodes are selectable; visibility updates correctly.
- Effects: passive stacking, skill/habit registration to character systems.

## Roadmap / TODOs
1. Draft skill grid spec + README
2. Define core data types (Node, Cluster, Grid)
3. Implement deterministic RNG + seeding scheme
4. Procedural cluster generation (5x5, affinity-biased)
5. Connector discovery + neighbor cluster reveal
6. Player pathing + visibility rules
7. Node effects engine (passive, skill, habit)
8. Persistence: save/load grid state
9. UI: pan/zoom, hover/select, tooltips
10. UI: connector preview + edge spawning
11. Integration: apply node effects to character
12. Tests: generation, distribution, connectivity, path rules
13. Demo: minimal runner showcasing navigation
14. Performance: caching + large-grid sanity
15. Docs: API + extension points

## Open Questions
- UI toolkit preference (Qt/PySide6, Pygame, DearPyGui)?
- Visual language for affinities (icons, hues, shapes)?
- Default weight config per affinity/cluster stored in JSON or Python?
- Constraints on skill/habit rarity or unlock ordering?
