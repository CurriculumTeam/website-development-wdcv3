// ============================================================
//  LESSON 6 — The Boss Battle & Victory Export
//  YOUR TASK: Complete the functions below.
//  DO NOT modify engine.js or index.html
// ============================================================

import { BOSS_PHASES, log } from './engine.js'

// ── TASK 1 ───────────────────────────────────────────────────
// createBoss()
// Returns a boss object with name, hp, maxHp, atk, phase (1), and alive (true).
// Use BOSS_PHASES[1] for initial stats.

export function createBoss() {
  // ✏️ YOUR CODE HERE
  const p = BOSS_PHASES[1]
  return { name: 'Demon Overlord', hp: p.hp, maxHp: p.hp, atk: p.atk, phase: 1, alive: true }
}

// ── TASK 2 ───────────────────────────────────────────────────
// checkPhaseTransition(boss)
// Boss transitions to the next phase when HP drops below a threshold:
//   Phase 1 → Phase 2 when hp < maxHp * 0.66
//   Phase 2 → Phase 3 when hp < maxHp * 0.33
// When transitioning, update boss.phase and boss.atk from BOSS_PHASES[newPhase].
// Returns { boss, transitioned, newPhase }

export function checkPhaseTransition(boss) {
  // ✏️ YOUR CODE HERE
  let transitioned = false, newPhase = boss.phase
  if (boss.phase < 2 && boss.hp < boss.maxHp * 0.66) {
    newPhase = 2; transitioned = true
  } else if (boss.phase < 3 && boss.hp < boss.maxHp * 0.33) {
    newPhase = 3; transitioned = true
  }
  const updatedBoss = transitioned
    ? { ...boss, phase: newPhase, atk: BOSS_PHASES[newPhase].atk }
    : boss
  return { boss: updatedBoss, transitioned, newPhase }
}

// ── TASK 3 ───────────────────────────────────────────────────
// generateVictoryReport(player, boss, turns)
// Called when the boss is defeated.
// Returns an object with:
//   { winner, bossName, turnsToWin, goldEarned, xpEarned, rank }
// rank is: 'S' if turns <= 5, 'A' if <= 10, 'B' if <= 20, 'C' otherwise
// goldEarned = 150 + (20 - turns) * 5 (min 50)
// xpEarned = 300

export function generateVictoryReport(player, boss, turns) {
  // ✏️ YOUR CODE HERE
  const rank = turns <= 5 ? 'S' : turns <= 10 ? 'A' : turns <= 20 ? 'B' : 'C'
  const goldEarned = Math.max(50, 150 + (20 - turns) * 5)
  return {
    winner: player.name ?? 'Hero',
    bossName: boss.name,
    turnsToWin: turns,
    goldEarned,
    xpEarned: 300,
    rank,
  }
}

// ── TASK 4 ───────────────────────────────────────────────────
// playerComboAttack(player, boss, comboCount)
// comboCount is how many times the player has attacked in a row (1, 2, 3...).
// Damage = player.atk * comboCount (combo multiplier).
// If comboCount >= 3, it's a FINISHER — deal double damage.
// Returns { boss, damage, isFinisher }

export function playerComboAttack(player, boss, comboCount) {
  // ✏️ YOUR CODE HERE
  const isFinisher = comboCount >= 3
  const damage = player.atk * comboCount * (isFinisher ? 2 : 1)
  return {
    boss: { ...boss, hp: Math.max(0, boss.hp - damage), alive: boss.hp - damage > 0 },
    damage,
    isFinisher,
  }
}
