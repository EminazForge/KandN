from __future__ import annotations

import sys
from pathlib import Path

# Ensure repository root is on path when running directly
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from game.skill_tree.grid import GridState
from game.skill_tree.ui.pygame_ui import SkillTreeViewer


def main():
    world_seed = 1337
    grid = GridState(world_seed=world_seed)
    grid.ensure_origin()

    viewer = SkillTreeViewer(grid)
    viewer.run()


if __name__ == "__main__":
    main()
