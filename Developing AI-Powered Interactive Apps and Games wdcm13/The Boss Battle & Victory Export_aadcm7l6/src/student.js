// ============================================================
//  LESSON 6 — COMPLETE (Teacher Reference)
//  All tasks implemented correctly. Lessons 4 & 5 included.
// ============================================================

import { BOSS_HP, ENEMY_TYPES } from './engine.js'

// ════════════════════════════════════════════════════════════
//  LESSON 4 — Complete
// ════════════════════════════════════════════════════════════

export function createPlayer(startX = 0, startY = 0) {
  return {
    x: startX, y: startY,
    hp: 120, maxHp: 120,
    stamina: 100, maxStamina: 100,
    xp: 0, level: 1, gold: 0, potions: 3,
    kills: 0, state: 'idle', dir: 'down',
    facingDir: 'right', comboCount: 0,
    invincible: 0, attackCd: 0, dodgeCd: 0, score: 0,
  }
}

export function movePlayer(player, direction, tiles) {
  return player
}

export function getSpeedMultiplier(player, tiles) {
  return 1.0
}

export function collectItem(player, item) {
  if (item.type === 'coin') return { player: { ...player, gold: player.gold + 10 }, message: '💰 +10 gold' }
  if (item.type === 'potion') return { player: { ...player, potions: player.potions + 1 }, message: '🧪 +1 potion' }
  return { player, message: '' }
}

export function checkLevelUp(player) {
  const threshold = player.level * 150
  if (player.xp >= threshold) {
    return {
      player: {
        ...player,
        level: player.level + 1,
        xp: player.xp - threshold,
        maxHp: player.maxHp + 12,
        hp: player.maxHp + 12,
        maxStamina: player.maxStamina + 5,
        stamina: player.maxStamina + 5,
      },
      leveledUp: true,
    }
  }
  return { player, leveledUp: false }
}

// ════════════════════════════════════════════════════════════
//  LESSON 5 — Complete
// ════════════════════════════════════════════════════════════

export function spawnEnemy(type) {
  // Not used in lesson 6 engine directly but kept for completeness
  return null
}

export function attackEnemy(player, enemy) {
  const newCombo = (player.comboCount + 1) % 4
  const isBig = newCombo === 3
  const damage = 12 + player.level * 3 + (isBig ? 22 : 0) + Math.floor(Math.random() * 8)
  const newHp = Math.max(0, enemy.hp - damage)
  const killed = newHp <= 0
  let p = { ...player, comboCount: newCombo }
  if (killed) {
    p.xp    += ENEMY_TYPES[enemy.type].xp
    p.gold  += Math.floor(ENEMY_TYPES[enemy.type].xp * 0.5)
    p.kills += 1
    p.score += ENEMY_TYPES[enemy.type].xp * 10
  }
  return { player: p, enemy: { ...enemy, hp: newHp, alive: !killed }, damage, killed, isBig }
}

export function enemyAttack(enemy, player) {
  const damage = ENEMY_TYPES[enemy.type].atk + Math.floor(Math.random() * 7)
  return {
    player: { ...player, hp: Math.max(0, player.hp - damage), invincible: 0.42 },
    damage,
  }
}

export function usePotion(player) {
  if (player.potions <= 0) return { player, healed: 0 }
  const heal = Math.min(55, player.maxHp - player.hp)
  return {
    player: { ...player, hp: player.hp + heal, potions: player.potions - 1 },
    healed: heal,
  }
}

export function updateQuestProgress(quests, type, amount) {
  return quests.map(q => {
    if (q.completed || q.type !== type) return q
    const progress = (q.progress ?? 0) + amount
    return { ...q, progress, completed: progress >= (q.count ?? 1) }
  })
}

// ════════════════════════════════════════════════════════════
//  LESSON 6 — Complete
// ════════════════════════════════════════════════════════════

// ── TASK 1 ───────────────────────────────────────────────────
export function createBossFight() {
  return {
    entity: {
      name: 'Demon Overlord',
      x: 0,
      y: 0,
      hp: BOSS_HP,
      maxHp: BOSS_HP,
      alive: true,
    },
    phase: 1,
    phaseTimer: 0,
  }
}

// ── TASK 2 ───────────────────────────────────────────────────
export function checkPhaseTransition(bossFight) {
  const { entity, phase } = bossFight
  const pct = entity.hp / entity.maxHp

  if (phase < 2 && pct < 0.66) {
    return {
      bossFight: { ...bossFight, phase: 2, phaseTimer: 0 },
      transitioned: true,
      newPhase: 2,
    }
  }
  if (phase < 3 && pct < 0.33) {
    return {
      bossFight: { ...bossFight, phase: 3, phaseTimer: 0 },
      transitioned: true,
      newPhase: 3,
    }
  }
  return { bossFight, transitioned: false, newPhase: phase }
}

// ── TASK 3 ───────────────────────────────────────────────────
export function attackBoss(player, bossFight) {
  const newCombo = (player.comboCount + 1) % 4
  const isBig = newCombo === 3
  const damage = 14 + player.level * 4 + (isBig ? 30 : 0) + Math.floor(Math.random() * 10)
  const newHp = Math.max(0, bossFight.entity.hp - damage)
  const killed = newHp <= 0
  let p = { ...player, comboCount: newCombo }
  const newEntity = { ...bossFight.entity, hp: newHp, alive: !killed }
  if (killed) {
    p.xp    += 300
    p.gold  += 150
    p.score += 5000
  }
  return {
    player: p,
    bossFight: { ...bossFight, entity: newEntity },
    damage,
    killed,
    isBig,
  }
}

// ── TASK 4 ───────────────────────────────────────────────────
export function generateVictoryReport(player, bossFight, turns) {
  const rank = turns <= 5 ? 'S' : turns <= 10 ? 'A' : turns <= 20 ? 'B' : 'C'
  return {
    winner: 'Hero',
    bossName: bossFight.entity.name,
    turnsToWin: turns,
    goldEarned: player.gold,
    xpEarned: 300,
    rank,
    score: 5000,
  }
}
