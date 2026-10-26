import React, { useState, useCallback, useRef } from 'react'
import GameCanvas from './GameCanvas.jsx'
import HUD from './HUD.jsx'
import { getAllSaves, formatTimestamp } from './SaveSystem.js'

const cinzel = "'Cinzel',serif"
const gold = '#c8a030'

function TitleBtn({ onClick, disabled, children, secondary, style: extra }) {
  const [h, setH] = useState(false)
  return <button onClick={onClick} disabled={disabled} onMouseEnter={() => setH(true)} onMouseLeave={() => setH(false)} style={{
    fontFamily: cinzel, fontSize: '.78rem', fontWeight: 600, letterSpacing: '0.2em',
    color: disabled ? '#7a6020' : h ? '#fff' : secondary ? '#a09028' : '#e8d070',
    background: h ? (secondary ? 'rgba(180,160,40,.12)' : 'rgba(200,160,40,.15)') : 'transparent',
    border: `2px solid ${disabled ? 'rgba(120,100,40,.25)' : secondary ? 'rgba(180,160,40,.3)' : 'rgba(200,160,40,.5)'}`,
    borderRadius: 5, padding: '11px 32px', cursor: disabled ? 'wait' : 'pointer',
    textTransform: 'uppercase', boxShadow: h && !secondary ? '0 0 20px rgba(200,160,40,.2)' : 'none',
    transition: 'all .25s', ...extra,
  }}>{children}</button>
}

const Divider = ({ mb = 14, op = .4 }) => <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: mb, opacity: op }}>
  {[18,8,5,5,48,48,5,5,8,18].map((w,i) => <div key={i} style={{ width: w, height: 1, background: gold }} />)}
</div>

function TitleScreen({ onStart, onContinue }) {
  const [key, setKey] = useState(import.meta.env.VITE_GROQ_API_KEY || '')
  const [loading, setLoading] = useState(false)
  const [showSaves, setShowSaves] = useState(false)
  const saves = getAllSaves(), hasSave = saves.some(s => s.exists)

  const go = (fn, ...args) => {
    if (loading) return
    if (key.trim()) globalThis.__GROQ_KEY = key.trim()
    setLoading(true)
    setTimeout(() => fn(key.trim(), ...args), 900)
  }

  return <div style={{ position: 'fixed', inset: 0, background: 'radial-gradient(ellipse at 50% 60%, #1c1208 0%, #080608 55%, #000 100%)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: "'Noto Serif JP',serif", overflow: 'hidden' }}>
    {Array.from({ length: 24 }).map((_, i) => <div key={i} style={{ position: 'absolute', left: `${(i*37+10)%100}%`, top: `${(i*19+5)%100}%`, width: i%5<2?3:2, height: i%5<2?3:2, borderRadius: '50%', background: `rgba(${200+i*2},${130+i*4},${60+i},${0.25+i%4*0.08})`, animation: `float-${i%3} ${3.5+i*0.28}s ease-in-out infinite` }} />)}
    <Divider />
    <div style={{ fontFamily: "'Noto Serif JP',serif", fontSize: 'clamp(1rem,3vw,1.6rem)', color: 'rgba(200,180,120,.35)', letterSpacing: '0.5em', marginBottom: 6 }}>戦国クロニクル</div>
    <div style={{ fontFamily: "'Cinzel Decorative','Cinzel',serif", fontSize: 'clamp(2.2rem,6vw,4.2rem)', fontWeight: 900, background: 'linear-gradient(180deg,#f8e880 0%,#c8a030 40%,#7a5810 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', letterSpacing: '0.15em', lineHeight: 1.1, textAlign: 'center', filter: 'drop-shadow(0 4px 28px rgba(200,160,40,.35))', marginBottom: 6 }}>BOSS BATTLE</div>
    <div style={{ fontFamily: cinzel, fontSize: '.63rem', color: 'rgba(180,160,100,.4)', letterSpacing: '0.28em', marginBottom: 32 }}>FULL GAME · ALL QUESTS · BOSS FIGHT · SAVE/LOAD</div>
    <div style={{ fontSize: '4.5rem', margin: '0 0 28px', filter: 'drop-shadow(0 8px 22px rgba(200,160,40,.22))' }}>☠</div>
    <Divider mb={28} op={.35} />
    <div style={{ marginBottom: 18, textAlign: 'center' }}>
      <div style={{ fontFamily: cinzel, fontSize: '.56rem', color: 'rgba(200,180,100,.45)', letterSpacing: 2, marginBottom: 5 }}>GROQ API KEY — optional (free AI dialogue)</div>
      <input type="password" placeholder="gsk_... (free at console.groq.com)" value={key} onChange={e => setKey(e.target.value)} onKeyDown={e => e.key === 'Enter' && go(onStart)}
        style={{ background: 'rgba(0,0,0,.55)', color: '#c8b890', border: '1px solid rgba(200,160,40,.22)', borderRadius: 5, padding: '7px 14px', fontSize: '.82rem', width: 300, fontFamily: "'Crimson Text',serif", outline: 'none' }} />
      <div style={{ fontFamily: cinzel, fontSize: '.48rem', color: 'rgba(100,90,55,.4)', marginTop: 4, letterSpacing: 1 }}>Images: Pollinations.ai (FREE) · Weather: Open-Meteo (FREE)</div>
    </div>
    <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', justifyContent: 'center' }}>
      <TitleBtn onClick={() => go(onStart)} disabled={loading}>{loading ? '⏳  Generating World...' : '⚔  New Chronicle  ⚔'}</TitleBtn>
      {hasSave && <TitleBtn onClick={() => setShowSaves(v => !v)} secondary>📜  Continue</TitleBtn>}
    </div>
    {showSaves && hasSave && <div style={{ marginTop: 14, background: 'rgba(0,0,0,.7)', border: '1px solid rgba(200,160,40,.2)', borderRadius: 8, padding: '12px 16px', maxWidth: 380, width: '90vw' }}>
      {saves.filter(s => s.exists).map(s => <div key={s.slot} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '7px 0', borderBottom: '1px solid rgba(255,255,255,.05)' }}>
        <div>
          <div style={{ fontFamily: cinzel, fontSize: '.62rem', color: 'rgba(200,180,120,.8)' }}>Slot {s.slot+1} · Lv {s.level}</div>
          <div style={{ fontFamily: cinzel, fontSize: '.52rem', color: 'rgba(160,140,80,.5)' }}>{s.location} · {formatTimestamp(s.timestamp)}</div>
        </div>
        <TitleBtn onClick={() => go(onContinue, s.slot)} secondary style={{ width: 'auto', padding: '5px 14px', fontSize: '.58rem', margin: 0 }}>Load</TitleBtn>
      </div>)}
    </div>}
    <div style={{ display: 'flex', gap: 20, marginTop: 28, flexWrap: 'wrap', justifyContent: 'center', maxWidth: 560 }}>
      {[['☠','Boss Fight','3-phase battles'],['🗺️','Open World','200×150 procedural map'],['⚔','Combat','4-hit combos + dodge'],['🧙','AI NPCs','Groq LLaMA-70B'],['💾','Save System','3 save slots'],['📜','All Quests','Full quest system']].map(([e,t,d]) => (
        <div key={t} style={{ textAlign: 'center', minWidth: 75 }}>
          <div style={{ fontSize: '1.2rem', marginBottom: 3 }}>{e}</div>
          <div style={{ fontFamily: cinzel, fontSize: '.5rem', color: 'rgba(180,160,80,.65)', letterSpacing: 1 }}>{t}</div>
          <div style={{ fontFamily: "'Crimson Text',serif", fontSize: '.58rem', color: 'rgba(120,100,60,.5)' }}>{d}</div>
        </div>
      ))}
    </div>
  </div>
}

function LoadingScreen() {
  return <div style={{ position: 'fixed', inset: 0, background: '#000', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
    <div style={{ fontFamily: "'Cinzel Decorative',serif", fontSize: '1.4rem', color: gold, letterSpacing: 4, marginBottom: 20 }}>GENERATING WORLD</div>
    <div style={{ width: 220, height: 4, background: 'rgba(200,160,40,.15)', borderRadius: 2, overflow: 'hidden' }}>
      <div style={{ height: '100%', background: 'linear-gradient(90deg,#c8a030,#f0d060)', borderRadius: 2, animation: 'loading-bar 1.5s ease-in-out infinite' }} />
    </div>
    <div style={{ fontFamily: "'Noto Serif JP',serif", fontSize: '.68rem', color: 'rgba(200,160,80,.35)', marginTop: 14, letterSpacing: 4 }}>世界を生成中...</div>
  </div>
}

export default function App() {
  const [screen, setScreen] = useState('title')
  const [groqKey, setGroqKey] = useState('')
  const [savedSlot, setSavedSlot] = useState(null)
  const [hudData, setHudData] = useState(null)
  const canvasRef = useRef(null)

  const handleHudUpdate = useCallback(fn => setHudData(prev => typeof fn === 'function' ? (fn(prev) ?? prev) : fn), [])
  const startNew = (k) => { setGroqKey(k); setScreen('loading'); setSavedSlot(null); setTimeout(() => setScreen('game'), 1100) }
  const startContinue = (k, slot) => { setGroqKey(k); setScreen('loading'); setSavedSlot(slot); setTimeout(() => setScreen('game'), 1100) }
  const handleSave = useCallback(slot => canvasRef.current?.__gameSave?.(slot), [])
  const handleLoad = useCallback(slot => { setSavedSlot(slot); setScreen('loading'); setTimeout(() => setScreen('game'), 800) }, [])

  return <div style={{ width: '100vw', height: '100vh', overflow: 'hidden', background: '#000', position: 'relative' }}>
    {screen === 'title'   && <TitleScreen onStart={startNew} onContinue={startContinue} />}
    {screen === 'loading' && <LoadingScreen />}
    {screen === 'game'    && <>
      <GameCanvas key={`${savedSlot}-${groqKey}`} groqKey={groqKey} savedSlot={savedSlot} onHudUpdate={handleHudUpdate} ref={canvasRef} />
      <HUD data={hudData} canvasRef={canvasRef} onSave={handleSave} onLoad={handleLoad} />
    </>}
  </div>
}
