import React, { useRef, useEffect, forwardRef } from 'react'
import { T, TILE_S, WORLD_W, WORLD_H } from './worldData.js'
import { generateWorld, getBiome } from './WorldGenerator.js'
import { ThreeRenderer } from './ThreeRenderer.js'
import { generateAreaNarration, getWeather } from './api.js'
import { playFootstep, startWind } from './AudioEngine.js'
import { createPlayer, getSpeedMultiplier, collectItem, checkLevelUp } from './student.js'

const SURF = { [T.PATH]:'path',[T.BRIDGE]:'path',[T.VILLAGE]:'path',[T.BEACH]:'sand',[T.SNOW]:'snow',[T.FOREST]:'grass',[T.DENSE_FOREST]:'grass',[T.GRASS]:'grass',[T.TALL_GRASS]:'grass' }
const MOVE_KEYS = ['arrowup','arrowdown','arrowleft','arrowright','w','a','s','d']
const SPD = 185

const GameCanvas = forwardRef(function GameCanvas({ onHudUpdate }, fwdRef) {
  const mountRef = useRef(null), threeRef = useRef(null), gsRef = useRef(null)
  const inp = useRef({}), rafRef = useRef(null)
  const mouse = useRef({ locked: false })

  useEffect(() => {
    const world = generateWorld()
    const W = window.innerWidth, H = window.innerHeight

    // createPlayer() — student must implement this
    const player = createPlayer(world.startX, world.startY)

    gsRef.current = {
      world, player,
      enemies: [], npcs: [], items: world.items,
      camera: { x: world.startX - W / 2, y: world.startY - H / 2 }, W, H,
      timeOfDay: 8.5, weather: 'clear', currentBiome: 'coast',
      locationName: world.locations[0]?.name ?? 'Tsurumi Village',
      narration: '', narrationTimer: 0, gameTime: 0,
    }

    const three = new ThreeRenderer(mountRef.current)
    threeRef.current = three
    three.buildTerrain(world.tiles, world.heights)
    startWind(0.3)
    getWeather().then(w => { if (gsRef.current) gsRef.current.weather = w })
    setTimeout(() => generateAreaNarration(world.locations[0]?.name ?? 'Tsurumi Village', 'coast', 'morning', 'clear')
      .then(n => { if (n && gsRef.current) { gsRef.current.narration = n; gsRef.current.narrationTimer = 6 } }), 500)

    let lastT = 0
    const loop = ts => {
      const dt = Math.min((ts - lastT) / 1000, 0.05); lastT = ts
      try { if (gsRef.current) { update(dt); threeRef.current?.render(gsRef.current) } }
      catch (e) { console.error('loop:', e) }
      rafRef.current = requestAnimationFrame(loop)
    }
    rafRef.current = requestAnimationFrame(loop)
    return () => { cancelAnimationFrame(rafRef.current); threeRef.current?.dispose(); threeRef.current = null }
  }, [])

  useEffect(() => {
    const down = e => {
      const k = e.key.toLowerCase()
      if (MOVE_KEYS.includes(k)) e.preventDefault()
      inp.current[k] = true
      if (k === 'escape' && document.pointerLockElement) document.exitPointerLock()
    }
    const up = e => { inp.current[e.key.toLowerCase()] = false }
    document.addEventListener('keydown', down)
    document.addEventListener('keyup', up)
    return () => { document.removeEventListener('keydown', down); document.removeEventListener('keyup', up) }
  }, [])

  useEffect(() => {
    const el = mountRef.current; if (!el) return
    const onClick = () => { if (document.pointerLockElement !== el) el.requestPointerLock() }
    const onPLC = () => { mouse.current.locked = document.pointerLockElement === el }
    const onMove = e => { if (mouse.current.locked) threeRef.current?.orbitCamera(e.movementX, e.movementY) }
    const onWheel = e => { e.preventDefault(); threeRef.current?.zoomCamera(e.deltaY) }
    el.addEventListener('click', onClick)
    el.addEventListener('wheel', onWheel, { passive: false })
    document.addEventListener('pointerlockchange', onPLC)
    document.addEventListener('mousemove', onMove)
    return () => {
      el.removeEventListener('click', onClick); el.removeEventListener('wheel', onWheel)
      document.removeEventListener('pointerlockchange', onPLC); document.removeEventListener('mousemove', onMove)
      if (document.pointerLockElement === el) document.exitPointerLock()
    }
  }, [])

  function tileAt(wx, wy) {
    const tx = ~~(wx / TILE_S), ty = ~~(wy / TILE_S)
    if (tx < 0 || tx >= WORLD_W || ty < 0 || ty >= WORLD_H) return T.DEEP_SEA
    return gsRef.current.world.tiles[ty * WORLD_W + tx]
  }
  function walkable(wx, wy) {
    const t = tileAt(wx, wy)
    return t !== T.DEEP_SEA && t !== T.SEA && t !== T.ROCK && t !== T.MOUNTAIN
  }

  function update(dt) {
    const gs = gsRef.current; if (!gs) return
    const { player, world, camera } = gs, i = inp.current
    gs.gameTime += dt
    gs.timeOfDay = (gs.timeOfDay + dt * (24 / 180)) % 24
    gs.narrationTimer = Math.max(0, gs.narrationTimer - dt)

    const biome = getBiome(world.tiles, player.x, player.y)
    if (biome !== gs.currentBiome) {
      gs.currentBiome = biome
      generateAreaNarration(gs.locationName, biome, gs.timeOfDay < 12 ? 'morning' : 'afternoon', gs.weather)
        .then(n => { if (n && gsRef.current) { gsRef.current.narration = n; gsRef.current.narrationTimer = 5 } })
    }

    // WASD movement — uses getSpeedMultiplier() from student
    const mu = i['arrowup'] || i['w'], md = i['arrowdown'] || i['s']
    const ml = i['arrowleft'] || i['a'], mr = i['arrowright'] || i['d']
    if (mu || md || ml || mr) {
      let ix = (mr ? 1 : 0) - (ml ? 1 : 0), iy = (md ? 1 : 0) - (mu ? 1 : 0)
      if (ix !== 0 || iy !== 0) {
        const mag = Math.sqrt(ix * ix + iy * iy); ix /= mag; iy /= mag
        const yaw = threeRef.current?.getCameraYaw() ?? 0
        const vx = ix * Math.cos(yaw) + iy * Math.sin(yaw)
        const vy = -ix * Math.sin(yaw) + iy * Math.cos(yaw)
        // Build 2D tiles for getSpeedMultiplier (lesson4 engine format: 20×15)
        const tiles2d = Array.from({ length: 15 }, (_, ty) =>
          Array.from({ length: 20 }, (_, tx) => gs.world.tiles[ty * WORLD_W + tx] ?? T.GRASS)
        )
        const mult = getSpeedMultiplier({ x: player.x, y: player.y }, tiles2d)
        const spd = SPD * mult * dt
        if (walkable(player.x + vx * spd + vx * 12, player.y)) player.x += vx * spd
        if (walkable(player.x, player.y + vy * spd + vy * 12)) player.y += vy * spd
        player.facingYaw = Math.atan2(vx, vy)
        player.facingDir = vx > 0 ? 'right' : 'left'
        player.dir = Math.abs(vx) > Math.abs(vy) ? (vx > 0 ? 'right' : 'left') : (vy > 0 ? 'down' : 'up')
        player.state = 'walking'; player.walkFrame = (player.walkFrame ?? 0) + dt * 9
        playFootstep(SURF[tileAt(player.x, player.y)] ?? 'grass')
      }
    } else {
      player.state = 'idle'
    }

    // collectItem() + checkLevelUp() — student must implement both
    for (const it of gs.items) {
      if (it.collected) continue
      const dx = player.x - it.x, dy = player.y - it.y
      if (Math.sqrt(dx * dx + dy * dy) < 55) {
        it.collected = true
        const res = collectItem({ ...player }, it)
        Object.assign(player, res.player)
        if (res.message) { gs.narration = res.message; gs.narrationTimer = 3 }
        const lvRes = checkLevelUp({ ...player })
        if (lvRes.leveledUp) {
          Object.assign(player, lvRes.player)
          gs.narration = `★ Level Up! Now level ${player.level}.`
          gs.narrationTimer = 4
        }
      }
    }

    // Discover locations
    for (const loc of world.locations) {
      if (!loc.discovered) {
        const dx = player.x - loc.x * TILE_S, dy = player.y - loc.y * TILE_S
        if (Math.sqrt(dx * dx + dy * dy) < 130) {
          loc.discovered = true; gs.locationName = loc.name
          gs.narration = `✦ Discovered: ${loc.name}`; gs.narrationTimer = 4
        }
      }
    }

    // Camera follow
    camera.x += ((player.x - gs.W / 2) - camera.x) * 7 * dt
    camera.y += ((player.y - gs.H / 2) - camera.y) * 7 * dt
    camera.x = Math.max(0, Math.min(WORLD_W * TILE_S - gs.W, camera.x))
    camera.y = Math.max(0, Math.min(WORLD_H * TILE_S - gs.H, camera.y))

    if (~~(gs.gameTime * 10) % 4 === 0 && onHudUpdate) {
      const tiles2d = Array.from({ length: 15 }, (_, ty) =>
        Array.from({ length: 20 }, (_, tx) => gs.world.tiles[ty * WORLD_W + tx] ?? T.GRASS)
      )
      onHudUpdate(prev => ({
        ...prev,
        hp: player.hp, maxHp: player.maxHp,
        stamina: player.stamina, maxStamina: player.maxStamina,
        xp: player.xp, xpNext: player.level * 150,
        level: player.level, gold: player.gold,
        potions: player.potions, kills: player.kills,
        location: gs.locationName, time: gs.timeOfDay, weather: gs.weather,
        narration: gs.narrationTimer > 0 ? gs.narration : '',
        nearItem: gs.items.some(it => !it.collected && Math.sqrt((player.x - it.x) ** 2 + (player.y - it.y) ** 2) < 55),
        _speed: getSpeedMultiplier({ x: player.x, y: player.y }, tiles2d),
      }))
    }
  }

  return <div ref={mountRef} style={{ position: 'fixed', inset: 0, width: '100vw', height: '100vh', overflow: 'hidden', background: '#000' }} />
})

export default GameCanvas
