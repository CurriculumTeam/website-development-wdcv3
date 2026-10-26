// ============================================================
//  LESSON 5 — COMPLETE (Teacher Reference)
//  All tasks implemented correctly. Lesson 4 code included.
// ============================================================

import { ENEMY_TYPES, createEnemyTemplate } from './engine.js'

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
  // Not used in lesson 5 engine but kept for completeness
  return player
}

export function getSpeedMultiplier(player, tiles) {
  // Not used in lesson 5 engine but kept for completeness
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

// ── TASK 1 ───────────────────────────────────────────────────
export function spawnEnemy(type) {
  const enemy = createEnemyTemplate(type)
  enemy.angle = Math.random() * Math.PI * 2
  return enemy
}

// ── TASK 2 ───────────────────────────────────────────────────
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

// ── TASK 3 ───────────────────────────────────────────────────
export function enemyAttack(enemy, player) {
  const damage = ENEMY_TYPES[enemy.type].atk + Math.floor(Math.random() * 7)
  return {
    player: { ...player, hp: Math.max(0, player.hp - damage), invincible: 0.42 },
    damage,
  }
}

// ── TASK 4 ───────────────────────────────────────────────────
export function usePotion(player) {
  if (player.potions <= 0) return { player, healed: 0 }
  const heal = Math.min(55, player.maxHp - player.hp)
  return {
    player: { ...player, hp: player.hp + heal, potions: player.potions - 1 },
    healed: heal,
  }
}

// ── TASK 5 ───────────────────────────────────────────────────
export function updateQuestProgress(quests, type, amount) {
  return quests.map(q => {
    if (q.completed || q.type !== type) return q
    const progress = (q.progress ?? 0) + amount
    return { ...q, progress, completed: progress >= (q.count ?? 1) }
  })
}
