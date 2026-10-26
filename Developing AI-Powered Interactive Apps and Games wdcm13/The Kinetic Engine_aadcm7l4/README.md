# The Kinetic Engine — Teacher Reference

This is the **complete solution** for the Kinetic Engine lesson.

## Running

```bash
npm install
npm run dev
```

Opens at `http://localhost:4044`

## What's Implemented

All 5 student functions are solved in `src/student.js`:

- `createPlayer` — returns full player object with all required fields
- `movePlayer` — tile-based movement with bounds + walkability checks
- `getSpeedMultiplier` — reads tile type and returns correct multiplier via `speedMult()`
- `collectItem` — handles coin (+10 gold) and potion (+1 potion) with messages
- `checkLevelUp` — checks `xp >= level * 150`, applies stat increases on level up

## Notes for Teachers

- The student folder (`lesson4/`) has the same engine but empty stubs in `student.js`
- Students should not modify `engine.js`, `App.jsx`, or `GameCanvas.jsx`
- The game crashes intentionally if student functions return wrong types — this is by design
- `movePlayer` is called by the engine for WASD but the engine also does smooth movement — the student version validates tile walkability
