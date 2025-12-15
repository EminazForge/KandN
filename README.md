# K&N Item/Character System

This repository contains a small Python project for generating items (bases and affixes), assembling gear, and managing a character with stats and equipment.

## Structure

- `Affixes.py`, `Affixes.json`: Affix definitions and loader
- `Bases.py`, `Bases.json`: Base item definitions and loader
- `Gear.py`: Item assembly and bonuses application
- `ItemGenerator.py`: Orchestrates random item generation
- `Character.py`: Character stats, equipment, and equipping rules
- `Stat.py`, `Bonus.py`: Primitive stat and bonus models

## Quick Start

1. Ensure you have Python 3.10+ installed.
2. Run your scripts directly, e.g., `python Character.py` or integrate into your own runner.

## Version Control

This repo is set up with a Python-friendly `.gitignore`. After you connect your private remote, push changes to back up your work and enable rollbacks.

## Next Steps

- Link your private remote and push the initial commit.
- Consider adding a small runner script and tests.