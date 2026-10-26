# Boss Battle — Teacher Reference

This is the **complete solution** for the Boss Battle lesson.

## Running

```bash
npm install
npm run dev
```

Opens at `http://localhost:4066`

The `.env` file is included with the Groq API key for AI features.

## What's Implemented

All 4 student functions are solved in `src/student.js`:

- `createBossFight` — returns correct shape with `BOSS_HP`, phase 1, phaseTimer 0
- `checkPhaseTransition` — checks 66% and 33% thresholds, returns transitioned flag and new phase
- `attackBoss` — combo damage formula (14 + level*4 + big bonus), awards 300 XP / 150 gold / 5000 score on kill
- `generateVictoryReport` — rank logic (S/A/B/C by turns), returns full report object

## Notes for Teachers

- The student folder (`lesson6/`) has the same full game but empty stubs for Lesson 6 tasks
- Lessons 4 & 5 functions are pre-filled in the student folder
- The game has the complete main game experience: 300+ enemies, all quests, save/load, minimap, NPC dialogue
- Boss spawns near the player when B is pressed — the engine positions it after `createBossFight()` returns
- Victory report shows on screen when boss is killed — requires `generateVictoryReport()` to return a valid object
