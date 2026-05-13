# Panda Attack

A small third-person turn-based game built with Python and Panda3D.

## What it demonstrates
- Third-person character controller with keyboard input
- Walk animation state system
- Collision detection using bitmasks (pusher + event handlers)
- Turn-based battle system architecture
- HUD-driven combat input system

## Gameplay Overview
- Explore the world in third-person
- Collide with an enemy to trigger battle mode
- Choose moves through the HUD
- Alternate turns between player and AI enemy
- Defeat the enemy to return to exploration

## Preview

https://github.com/user-attachments/assets/6b94b20a-8478-434e-b2b9-a9fc59548943

## How to run
1. Install Panda3D: `pip3 install panda3d`
2. Run: `python3 main.py`

## Controls
- Arrow Up / Down — move forward / backward
- Arrow Left / Right — turn
- Escape — quit

## Technical Focus
This project emphasizes system design and separation of concerns, including:
- BattleManager controlling turn flow
- HUD acting as input layer
- Modular combat architecture supporting player and AI actions

## Future Additions
- Enemy AI decision flow
- Modular move system (player and enemy actions)
- Combat moves defining behavior and effects
- Entity-based state management (Player and Enemy)
