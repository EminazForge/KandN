# K&N Item/Character System

This repository contains a small Python project for generating items (bases and affixes), assembling gear, and managing a character with stats and equipment.

## Structure

- `Affixes.py`, `Affixes.json`: Affix definitions and loader
- `Bases.py`, `Bases.json`: Base item definitions and loader
- `Gear.py`: Item assembly and bonuses application
- `ItemGenerator.py`: Orchestrates random item generation
- `Character.py`: Character stats, equipment, and equipping rules
- `Stat.py`, `Bonus.py`: Primitive stat and bonus models

## Weight Model (Probabilities)

- Selections are weighted, not percentage-based. Each entry has a `weight`; the probability of picking one entry equals its weight divided by the sum of weights in the selection pool.
- Bases: `Bases.json` includes `weight` per base. `Bases.py` uses `random.choices(..., weights=...)` and provides an analysis utility that prints normalized chances per base and per slot (overall and within allowed item-level pools).
- Affixes: `Affixes.json` includes `weight` per affix. `Affixes.py` filters by slot and type, then samples with weights.

## Affix Scope (Local vs Global)

- `scope` in `Affixes.json` controls behavior:
	- `local`: modifies implicit base values before aggregation (e.g., local damage on weapons).
	- `global`: contributes explicit bonuses to the item’s aggregated bonuses.
- `Gear.py` applies locals to the base and adds globals to the item’s `boni` list.

## Responsibilities Split

- `ItemGenerator.py`: chooses category, rarity, base, and rolls affixes.
- `Gear.py`: derives item name, computes requirements, applies affixes (local/global), and renders tooltip via `to_tooltip()`.

## Quick Runs (Windows)

- Generate a random item and print its tooltip:
	```powershell
	& $Env:LOCALAPPDATA\Programs\Python\Python314\python.exe "u:/Privat/Scripts/K&N/ItemGenerator.py"
	```
- Explore base data, weights, and normalized probabilities:
	```powershell
	& $Env:LOCALAPPDATA\Programs\Python\Python314\python.exe "u:/Privat/Scripts/K&N/Bases.py"
	```

## Data Requirements

- Base entry: `name`, `slot`, `weight`, requirement fields (`lvl_req`, `str_req`, `int_req`, `dex_req`), implicit stat descriptors (`xStat/xType/xValue`, optional `y`/`z`).
- Affix entry: `type`, `name`, `clearName`, `slots`, `weight`, ranges (`xRange`, optional `yRange/zRange`), and `scope`.

## Next Steps

- Add CLI args to `Bases.py` (e.g., `--ilvl`, `--topN`) to inspect different pools quickly.
- Add CLI args to `ItemGenerator.py` (e.g., `--rarity`, `--slot`, `--ilvl`) for targeted generation.