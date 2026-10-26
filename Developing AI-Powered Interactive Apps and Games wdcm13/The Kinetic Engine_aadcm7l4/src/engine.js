// ── Lesson 4 Engine — matches main game worldData/WorldGenerator ──
// Tile types (same as src/data/worldData.js)
export const T = {
  DEEP_SEA:0, SEA:1, SHALLOW:2, BEACH:3,
  GRASS:4, TALL_GRASS:5, FOREST:6, DENSE_FOREST:7,
  ROCK:8, MOUNTAIN:9, SNOW:10,
  PATH:11, VILLAGE:12, SHRINE:13,
  BAMBOO:14, RUINS:15, BRIDGE:16,
}
export const TILE_S = 48
export const WORLD_W = 20   // smaller grid for lesson (main game is 200)
export const WORLD_H = 15

// Walkable check — same logic as main game isWalkable()
export function isWalkable(t) {
  return t !== T.DEEP_SEA && t !== T.SEA && t !== T.ROCK && t !== T.MOUNTAIN
}

// Speed multiplier — same as main game spdMult()
export function speedMult(t) {
  if (t === T.SHALLOW)                                           return 0.5
  if (t === T.FOREST || t === T.DENSE_FOREST || t === T.BAMBOO) return 0.72
  if (t === T.TALL_GRASS)                                        return 0.85
  if (t === T.PATH || t === T.BRIDGE)                            return 1.18
  if (t === T.SNOW)                                              return 0.78
  return 1.0
}

// Tile colors matching TILE_DEF from worldData
export const TILE_COLOR = {
  [T.DEEP_SEA]:'#0a1e3a', [T.SEA]:'#0e2e5a', [T.SHALLOW]:'#1a4a7a',
  [T.BEACH]:'#c8a050',    [T.GRASS]:'#3a6a20', [T.TALL_GRASS]:'#2a5a18',
  [T.FOREST]:'#1a4a0e',   [T.DENSE_FOREST]:'#122e08', [T.ROCK]:'#5a5550',
  [T.MOUNTAIN]:'#484440', [T.SNOW]:'#d8dce8', [T.PATH]:'#8a6a3a',
  [T.VILLAGE]:'#7a5030',  [T.SHRINE]:'#5a3a7a', [T.BAMBOO]:'#2a6a2a',
  [T.RUINS]:'#4a4030',    [T.BRIDGE]:'#7a5a38',
}

// Default player — used as fallback before student implements createPlayer()
export function createDefaultPlayer(startX = 144, startY = 144) {
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
export function generateLessonWorld() {
  const tiles = Array.from({ length: WORLD_H }, (_, y) =>
    Array.from({ length: WORLD_W }, (_, x) => {
      if (x === 0 || y === 0 || x === WORLD_W-1 || y === WORLD_H-1) return T.SEA
      if (x < 3 || y < 3) return T.BEACH
      if (x > WORLD_W-4 || y > WORLD_H-4) return T.FOREST
      if ((x === 8 && y >= 4 && y <= 8) || (x === 12 && y >= 6 && y <= 10)) return T.ROCK
      if (x >= 5 && x <= 7 && y >= 5 && y <= 7) return T.VILLAGE
      if (x >= 13 && x <= 15 && y >= 3 && y <= 5) return T.SHRINE
      if (x >= 9 && x <= 11 && y >= 9 && y <= 11) return T.RUINS
      if (x % 6 === 0 || y % 5 === 0) return T.PATH
      if (x > 10 && y < 8) return T.TALL_GRASS
      return T.GRASS
    })
  )
  // Place items
  const items = [
    { id:'i1', x:6*TILE_S+24, y:6*TILE_S+24, type:'coin',   collected:false },
    { id:'i2', x:14*TILE_S+24, y:4*TILE_S+24, type:'potion', collected:false },
    { id:'i3', x:10*TILE_S+24, y:10*TILE_S+24, type:'coin',  collected:false },
  ]
  return { tiles, items, startX: 3*TILE_S+24, startY: 3*TILE_S+24 }
}
