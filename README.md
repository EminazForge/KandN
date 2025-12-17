# K&N — Systems Sandbox (Items, Character, Skill Tree)

This project explores core ARPG-style systems in Python: item and gear generation, character stats/equipment, and a procedural, infinite skill grid with a minimal Pygame UI.

## What’s Included
- Items & Affixes: data-driven bases and affixes with weighted rolls (see `data/`).
- Equipment & Character: equip rules and stat aggregation (see `systems/`, `core/`).
- Skill Grid (NEW): infinite 2D grid composed of 5x5 clusters; connectors reveal neighboring clusters. Pygame viewer supports pan/zoom and selection (see `game/skill_tree/`).
- Scripts/Demos: quick runners and sandboxes (see `scripts/` and `game/skill_tree/demo.py`).
- Tests (scaffold): structure in place for future coverage.

## Repository Layout
- `core/`: character, stats, bonus, and item domain models.
- `systems/`: equipment assembly and item generator orchestrations.
- `game/`: gameplay features
	- `skill_tree/`: procedural grid, deterministic RNG, and Pygame UI demo.
	- `skills/`, `combat/`: placeholders for future gameplay.
- `data/`: JSON assets and helpers (`Affixes.json`, `Bases.json`, plus loaders).
- `scripts/`: quick demos (e.g., item generation showcase).
- `utils/`: shared helpers.
- `tests/`: unit tests scaffold.

## Quick Start (Windows)
Prereqs: Python 3.14. For the Pygame demo, install `pygame-ce` once per interpreter.

- Install Pygame into your chosen interpreter:
	```powershell
	# System interpreter
	& $Env:LOCALAPPDATA\Programs\Python\Python314\python.exe -m pip install pygame-ce

	# Or your venv (from the repo root)
	cd "u:/Privat/Scripts/K&N"
	.\.venv\Scripts\python.exe -m pip install pygame-ce
	```

- Run item generator demo:
	```powershell
	& $Env:LOCALAPPDATA\Programs\Python\Python314\python.exe "u:/Privat/Scripts/K`&N/scripts/demo_generate.py"
	```

- Run the skill grid viewer (Pygame):
	```powershell
	# Using system Python
	& $Env:LOCALAPPDATA\Programs\Python\Python314\python.exe -m game.skill_tree.demo

	# Or using your venv
	cd "u:/Privat/Scripts/K&N"
	.\.venv\Scripts\python.exe -m game.skill_tree.demo
	```

Tip: The path contains an ampersand (`K&N`), so quote paths and escape `&` as needed (PowerShell treats `&` as an operator).

## Skill Grid Snapshot
- Clusters: 5x5 nodes that tile seamlessly; origin starts at the center.
- Connectors: real nodes beyond the border; assigning one reveals the neighboring cluster and maps the connector to a border node in that cluster.
- Affinities: Red, Blue, Yellow, plus mixed (Orange, Green, Violet). Cluster tint reflects bias.
- Node Types: Passive (circle), Skill (rectangle), Habit (triangle), Empty (hollow); assigned nodes render filled.
- Determinism: generation is seeded by world seed and cluster coordinates.

## Notes
- Selections use weighted randomness; distributions are hard-coded for now.
- Data assets in `data/` define bases and affixes used by the generator.

## Roadmap (High Level)
- Pathing rules and reachability highlights on the skill grid.
- Persistence for discovered clusters and selected nodes.
- Skill/habit effect plumbing into character systems.
- Expanded tests and profiling on large grids.