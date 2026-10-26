# The Interaction Loop — Teacher Reference

This is the **complete solution** for the Interaction Loop lesson.

## Running

```bash
npm install
npm run dev
```

Opens at `http://localhost:4055`

## What's Implemented

All 5 student functions are solved in `src/student.js`:

- `spawnEnemy` — calls `createEnemyTemplate(type)` and sets a random angle
- `attackEnemy` — full combo damage formula, XP/gold/kills on kill
- `enemyAttack` — enemy atk stat + random 0-6, sets invincible frame
- `usePotion` — guards against empty potions, heals min(55, missing HP)
- `updateQuestProgress` — pure `.map()` with completed flag

## Notes for Teachers

- The student folder (`lesson5/`) has the same engine but empty stubs for Lesson 5 tasks
- Lesson 4 functions are pre-filled in the student folder — students paste their own solutions into the stubs
- 8 enemies spawn near the player start — enough to test all combat functions without overwhelming
- The game crashes if student functions return wrong shapes — intentional
