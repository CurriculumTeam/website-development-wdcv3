// ── Lesson 6 Engine — matches main game exactly ───────────────

// Boss constants from GameCanvas.jsx
export const BOSS_HP  = 320
export const BOSS_ATK = 28

// Enemy types — same as main game worldData.js
export const ENEMY_TYPES = {
  RONIN:  { name:'Rogue Ronin',    hp:60,  atk:15, spd:1.2, range:55, color:'#8a3010', xp:40  },
  BANDIT: { name:'Forest Bandit',  hp:40,  atk:10, spd:1.5, range:50, color:'#5a4020', xp:25  },
  GUARD:  { name:'Corrupted Guard',hp:80,  atk:20, spd:1.0, range:60, color:'#303060', xp:60  },
  DEMON:  { name:'Mountain Oni',   hp:120, atk:30, spd:0.8, range:70, color:'#8a0010', xp:100 },
  ARCHER: { name:'Shadow Archer',  hp:35,  atk:18, spd:1.8, range:200,color:'#1a3a10', xp:35  },
}

// Boss phase config — matches GameCanvas.jsx boss AI logic
// Phase 1 → 2 at 66% HP, Phase 2 → 3 at 33% HP
// Attack interval: phase1=1.2s, phase2=0.9s, phase3=0.7s
// Speed multiplier: 1.0 + phase * 0.3
export const BOSS_PHASES = {
  1: { label:'⚡ PHASE I',   color:'#e03020', atkInterval:1.2, spdMult:1.3 },
  2: { label:'🔥 PHASE II',  color:'#c020d0', atkInterval:0.9, spdMult:1.6 },
  3: { label:'☠ PHASE III', color:'#ff6000', atkInterval:0.7, spdMult:1.9 },
}

// Boss entity shape — matches main game gsRef.current.bossFight
// { entity: { name, x, y, hp, maxHp, alive }, phase, phaseTimer }
export function createBossFight() {
  return {
    entity: { name:'Demon Overlord', x:0, y:0, hp:BOSS_HP, maxHp:BOSS_HP, alive:true },
    phase: 1,
    phaseTimer: 0,
  }
}

// Player shape — matches main game player object
export function createDefaultPlayer() {
  return {
    x: 0, y: 0,
    hp: 120, maxHp: 120,
    stamina: 100, maxStamina: 100,
    xp: 0, level: 1, gold: 0, potions: 3,
    kills: 0, state: 'idle', comboCount: 0,
    attackCd: 0, invincible: 0,
  }
}

// Quest templates — same as main game QUEST_TEMPLATES
export const QUEST_TEMPLATES = [
  { id:'demon_overlord', title:'The Demon Overlord', desc:'Face the Demon Overlord and survive.', type:'boss', reward:500 },
  { id:'ten_kills',      title:'Trial by Blood',     desc:'Defeat ten enemies without retreating.', type:'kill', count:10, reward:350 },
]

export const RANK_COLORS = { S:'#f0d060', A:'#40d040', B:'#4090e0', C:'#a0a0a0' }
