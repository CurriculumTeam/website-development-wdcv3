import React, { useState, useRef, useEffect } from 'react'
import { toggleAudio } from './AudioEngine.js'
import { getAllSaves, formatTimestamp } from './SaveSystem.js'
import { QUEST_TEMPLATES, T, TILE_S, WORLD_W, WORLD_H } from './worldData.js'

const C = { gold:'#c8a030', dim:'rgba(200,180,100,.6)', bg:'rgba(0,0,0,.65)', border:'rgba(200,160,40,.22)' }
const cinzel = "'Cinzel',serif", crimson = "'Crimson Text',serif"
const panel = { background:'rgba(5,3,14,.97)', border:'1px solid rgba(200,160,40,.3)', borderRadius:10, padding:'18px 20px', backdropFilter:'blur(12px)', boxShadow:'0 12px 50px rgba(0,0,0,.8)' }
const btnStyle = col => ({ fontFamily:cinzel, fontSize:'.55rem', color:col, background:'transparent', border:`1px solid ${col}44`, borderRadius:4, padding:'4px 10px', cursor:'pointer', letterSpacing:1, textTransform:'uppercase' })

function useAnimNum(v) {
  const [d,setD]=useState(v), r=useRef(v)
  useEffect(()=>{
    const diff=v-r.current; if(Math.abs(diff)<1){setD(v);r.current=v;return}
    const step=diff/8, t=setInterval(()=>{r.current+=step;setD(Math.round(r.current));if(Math.abs(r.current-v)<1){setD(v);r.current=v;clearInterval(t)}},20)
    return()=>clearInterval(t)
  },[v]); return d
}

function ArcBar({value,max,r=36,color,glow,label}){
  const pct=Math.max(0,Math.min(1,value/Math.max(1,max))), circ=2*Math.PI*r, dash=circ*pct, dv=useAnimNum(value)
  return <div style={{position:'relative',width:r*2+12,height:r*2+12,flexShrink:0}}>
    <svg width={r*2+12} height={r*2+12} style={{transform:'rotate(-90deg)',position:'absolute',top:0,left:0}}>
      <circle cx={r+6} cy={r+6} r={r} fill="none" stroke="rgba(0,0,0,0.5)" strokeWidth={5.5}/>
      <circle cx={r+6} cy={r+6} r={r} fill="none" stroke={color} strokeWidth={5.5} strokeLinecap="round" strokeDasharray={`${dash} ${circ}`} style={{transition:'stroke-dasharray .3s',filter:`drop-shadow(0 0 5px ${glow})`}}/>
    </svg>
    <div style={{position:'absolute',inset:0,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',fontFamily:"'Noto Serif JP',serif"}}>
      <div style={{fontSize:r>30?'1rem':'.78rem',fontWeight:700,color,lineHeight:1}}>{dv}</div>
      <div style={{fontSize:'.5rem',color:'rgba(220,200,140,.5)',letterSpacing:1}}>{label}</div>
    </div>
  </div>
}

function ThinBar({value,max,color,glow,label,W=130}){
  const pct=Math.max(0,Math.min(1,value/Math.max(1,max)))
  return <div style={{width:W}}>
    <div style={{display:'flex',justifyContent:'space-between',fontFamily:cinzel,fontSize:'.48rem',color:'rgba(200,180,100,.45)',letterSpacing:2,marginBottom:3}}><span>{label}</span><span>{value}/{max}</span></div>
    <div style={{height:5,background:'rgba(0,0,0,0.55)',borderRadius:3,overflow:'hidden',border:'1px solid rgba(255,255,255,.06)'}}>
      <div style={{height:'100%',borderRadius:3,width:`${pct*100}%`,background:color,boxShadow:`0 0 6px ${glow}`,transition:'width .25s'}}/>
    </div>
  </div>
}

function BossBar({boss}){
  if(!boss) return null
  const pct=boss.hp/boss.maxHp, cols=['','#e03020','#c020d0','#ff6000'], col=cols[boss.phase]??'#e03020'
  return <div style={{position:'absolute',top:14,left:'50%',transform:'translateX(-50%)',width:520,background:'rgba(0,0,0,0.8)',border:`1px solid ${col}55`,borderRadius:8,padding:'10px 16px',backdropFilter:'blur(8px)',boxShadow:`0 0 24px ${col}30`}}>
    <div style={{fontFamily:"'Cinzel Decorative',serif",fontSize:'.85rem',color:'#ff4040',textAlign:'center',letterSpacing:3,marginBottom:4}}>{boss.name}</div>
    <div style={{height:10,background:'rgba(0,0,0,0.6)',borderRadius:5,overflow:'hidden',marginBottom:4}}>
      <div style={{height:'100%',borderRadius:5,width:`${pct*100}%`,background:`linear-gradient(90deg,${col},${col}dd)`,boxShadow:`0 0 10px ${col}`,transition:'width .3s'}}/>
    </div>
    <div style={{display:'flex',justifyContent:'space-between',fontFamily:cinzel,fontSize:'.55rem',color:`${col}aa`}}>
      <span>{boss.hp} / {boss.maxHp}</span><span style={{color:col}}>{['','⚡ PHASE I','🔥 PHASE II','☠ PHASE III'][boss.phase]}</span>
    </div>
  </div>
}

function ComboDisplay({combo}){
  if(combo<2) return null
  return <div style={{position:'absolute',top:'35%',right:28}}>
    <div style={{fontFamily:cinzel,fontSize:'.5rem',color:'rgba(240,200,60,.5)',letterSpacing:2,marginBottom:4,textAlign:'center'}}>COMBO</div>
    <div style={{display:'flex',gap:4}}>{[0,1,2,3].map(i=><div key={i} style={{width:10,height:10,borderRadius:'50%',background:i<combo?'#f0c040':'rgba(200,180,80,.15)',boxShadow:i<combo?'0 0 8px #f0c040':'none',transition:'all .1s'}}/>)}</div>
    {combo===3&&<div style={{fontFamily:cinzel,fontSize:'.6rem',color:'#f0e060',textAlign:'center',marginTop:4,letterSpacing:2}}>FINISHER!</div>}
  </div>
}

function Narration({text}){
  if(!text) return null
  return <div style={{position:'absolute',top:22,left:'50%',transform:'translateX(-50%)',maxWidth:620,width:'90vw',textAlign:'center',fontFamily:crimson,fontSize:'1rem',color:'rgba(230,210,160,.92)',fontStyle:'italic',textShadow:'0 2px 10px rgba(0,0,0,.9)',pointerEvents:'none'}}>{text}</div>
}

function DialogueBox({dialogue,onClose}){
  if(!dialogue) return null
  return <div style={{position:'absolute',bottom:140,left:'50%',transform:'translateX(-50%)',width:560,background:'rgba(6,4,16,.96)',border:'1px solid rgba(200,160,40,.35)',borderRadius:8,padding:'14px 18px',backdropFilter:'blur(10px)',boxShadow:'0 8px 40px rgba(0,0,0,.7)'}}>
    <div style={{display:'flex',justifyContent:'space-between',marginBottom:7}}>
      <span style={{fontFamily:cinzel,fontSize:'.65rem',color:C.gold,letterSpacing:2}}>{dialogue.speaker}</span>
      <span style={{cursor:'pointer',opacity:.45,fontSize:'.7rem',color:C.gold}} onClick={onClose}>✕</span>
    </div>
    <div style={{fontFamily:crimson,fontSize:'.92rem',color:'#c0b090',lineHeight:1.65,fontStyle:'italic'}}>{dialogue.text}</div>
    <div style={{marginTop:8,fontFamily:cinzel,fontSize:'.48rem',color:'rgba(160,140,80,.35)',letterSpacing:2}}>PRESS E TO CONTINUE</div>
  </div>
}

function QuestLog({quests,completed,onClose,onAccept}){
  return <div style={{position:'absolute',top:'50%',left:'50%',transform:'translate(-50%,-50%)',width:480,maxHeight:'80vh',overflowY:'auto',...panel}}>
    <div style={{display:'flex',justifyContent:'space-between',marginBottom:14}}>
      <div style={{fontFamily:"'Cinzel Decorative',serif",fontSize:'.9rem',color:C.gold,letterSpacing:3}}>QUEST LOG</div>
      <span style={{cursor:'pointer',color:'rgba(200,160,40,.5)',fontSize:'.8rem'}} onClick={onClose}>✕</span>
    </div>
    {quests.length>0&&<div style={{fontFamily:cinzel,fontSize:'.55rem',color:'rgba(200,160,40,.4)',letterSpacing:3,marginBottom:8}}>ACTIVE</div>}
    {quests.map((q,i)=><div key={i} style={{background:'rgba(255,255,255,.03)',border:'1px solid rgba(100,160,200,.15)',borderRadius:6,padding:'10px 12px',marginBottom:6}}>
      <div style={{fontFamily:cinzel,fontSize:'.7rem',color:'#70a8c8',letterSpacing:1}}>{q.title}</div>
      <div style={{fontFamily:crimson,fontSize:'.82rem',color:'rgba(180,160,120,.7)',margin:'3px 0'}}>{q.desc}</div>
      <div style={{display:'flex',justifyContent:'space-between',fontFamily:cinzel,fontSize:'.55rem'}}>
        <span style={{color:'rgba(120,160,180,.5)'}}>Progress: {q.progress??0}/{q.count}</span>
        <span style={{color:'rgba(200,160,40,.5)'}}>Reward: {q.reward}g</span>
      </div>
      <div style={{height:3,background:'rgba(255,255,255,.06)',borderRadius:2,marginTop:5,overflow:'hidden'}}>
        <div style={{height:'100%',background:'#4098b8',borderRadius:2,width:`${((q.progress??0)/q.count)*100}%`,transition:'width .3s'}}/>
      </div>
    </div>)}
    <div style={{fontFamily:cinzel,fontSize:'.55rem',color:'rgba(200,160,40,.4)',letterSpacing:3,margin:'12px 0 8px'}}>AVAILABLE</div>
    {QUEST_TEMPLATES.filter(q=>!quests.find(a=>a.id===q.id)&&!completed.find(c=>c.id===q.id)).map((q,i)=>(
      <div key={i} style={{background:'rgba(255,255,255,.025)',border:'1px solid rgba(200,160,40,.1)',borderRadius:6,padding:'10px 12px',marginBottom:6,display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <div>
          <div style={{fontFamily:cinzel,fontSize:'.68rem',color:C.gold,letterSpacing:1}}>{q.title}</div>
          <div style={{fontFamily:crimson,fontSize:'.8rem',color:'rgba(170,150,110,.65)',margin:'2px 0'}}>{q.desc}</div>
          <div style={{fontFamily:cinzel,fontSize:'.52rem',color:'rgba(160,130,60,.45)'}}>Reward: {q.reward}g</div>
        </div>
        <button style={{...btnStyle(C.gold),flexShrink:0,marginLeft:10,whiteSpace:'nowrap'}} onClick={()=>onAccept(q)}>Accept</button>
      </div>
    ))}
    {completed.length>0&&<><div style={{fontFamily:cinzel,fontSize:'.55rem',color:'rgba(80,180,80,.4)',letterSpacing:3,margin:'12px 0 8px'}}>COMPLETED ({completed.length})</div>
    {completed.map((q,i)=><div key={i} style={{background:'rgba(40,180,40,.04)',border:'1px solid rgba(40,180,40,.1)',borderRadius:6,padding:'6px 12px',marginBottom:4,opacity:.65}}><div style={{fontFamily:cinzel,fontSize:'.65rem',color:'#40b040',letterSpacing:1}}>✓ {q.title}</div></div>)}</>}
  </div>
}

function SavePanel({onSave,onLoad,onClose}){
  const [saves,setSaves]=useState(()=>getAllSaves())
  return <div style={{position:'absolute',top:'50%',left:'50%',transform:'translate(-50%,-50%)',width:360,...panel}}>
    <div style={{display:'flex',justifyContent:'space-between',marginBottom:14}}>
      <div style={{fontFamily:cinzel,fontSize:'.75rem',color:C.gold,letterSpacing:3}}>SAVE / LOAD</div>
      <span style={{cursor:'pointer',color:'rgba(200,160,40,.5)'}} onClick={onClose}>✕</span>
    </div>
    {saves.map(s=><div key={s.slot} style={{background:'rgba(255,255,255,.025)',border:'1px solid rgba(200,160,40,.12)',borderRadius:6,padding:'10px 12px',marginBottom:6,display:'flex',justifyContent:'space-between',alignItems:'center'}}>
      <div>
        <div style={{fontFamily:cinzel,fontSize:'.62rem',color:'rgba(200,180,120,.7)'}}>Slot {s.slot+1}</div>
        {s.exists?<div style={{fontFamily:cinzel,fontSize:'.55rem',color:'rgba(160,140,80,.5)'}}>Lv {s.level} · {s.location} · {formatTimestamp(s.timestamp)}</div>:<div style={{fontFamily:cinzel,fontSize:'.52rem',color:'rgba(100,90,60,.4)'}}>Empty</div>}
      </div>
      <div style={{display:'flex',gap:5,flexShrink:0,marginLeft:10}}>
        <button style={btnStyle(C.gold)} onClick={()=>{onSave(s.slot);setSaves(getAllSaves())}}>Save</button>
        {s.exists&&<button style={btnStyle('#4090c0')} onClick={()=>onLoad(s.slot)}>Load</button>}
      </div>
    </div>)}
  </div>
}

function SkillBar({potions}){
  const skills=[{key:'SPC',icon:'⚔',color:'#e08020'},{key:'Q',icon:'💨',color:'#4080e0'},{key:'E',icon:'✋',color:'#40c070'},{key:'F',icon:'🧪',color:'#e04040',count:potions},{key:'TAB',icon:'📜',color:'#8080e0'},{key:'B',icon:'☠',color:'#c020c0'},{key:'M',icon:'🗺',color:'#80a060'}]
  return <div style={{display:'flex',gap:7,alignItems:'flex-end'}}>
    {skills.map(sk=><div key={sk.key} style={{textAlign:'center'}}>
      <div style={{width:42,height:42,background:'rgba(0,0,0,0.68)',border:`1.5px solid ${sk.color}44`,borderRadius:6,display:'flex',alignItems:'center',justifyContent:'center',fontSize:'1.15rem',position:'relative',boxShadow:`inset 0 0 8px ${sk.color}22`}}>
        {sk.icon}
        {sk.count!==undefined&&<div style={{position:'absolute',top:-6,right:-6,background:sk.count>0?sk.color:'#444',borderRadius:'50%',width:15,height:15,fontSize:'.58rem',fontFamily:cinzel,fontWeight:700,display:'flex',alignItems:'center',justifyContent:'center',color:'#fff'}}>{sk.count}</div>}
      </div>
      <div style={{fontFamily:cinzel,fontSize:'.42rem',color:`${sk.color}80`,letterSpacing:.5,marginTop:2}}>{sk.key}</div>
    </div>)}
  </div>
}

function TimeOrb({timeH,weather}){
  const h=String(~~timeH).padStart(2,'0'), m=String(~~((timeH%1)*60)).padStart(2,'0')
  const pct=(timeH-5.5)/14, sx=10+pct*80, sy=50-Math.sin(Math.PI*pct)*40
  const WICONS={clear:'☀️',cloudy:'☁️',rain:'🌧️',snow:'❄️',storm:'⛈️',foggy:'🌫️'}
  return <div style={{textAlign:'center',minWidth:75}}>
    <svg width="80" height="46" style={{display:'block',margin:'0 auto 2px'}}>
      <path d="M 4 42 A 36 36 0 0 1 76 42" fill="none" stroke="rgba(200,180,80,.2)" strokeWidth="1.5"/>
      {timeH>=5.5&&timeH<=19.5&&<circle cx={sx} cy={sy} r="7" fill={timeH<6||timeH>20?'#8090e0':'#f0c040'} style={{filter:`drop-shadow(0 0 6px ${timeH<6||timeH>20?'#6080ff':'#f0a000'})`}}/>}
    </svg>
    <div style={{fontFamily:cinzel,fontSize:'.62rem',color:'rgba(200,180,100,.75)',letterSpacing:1}}>{h}:{m}</div>
    <div style={{fontSize:'.72rem',marginTop:1}}>{WICONS[weather]??'☀️'}</div>
  </div>
}

function LevelBadge({level,xp,xpNext,gold,kills}){
  return <div style={{textAlign:'center',minWidth:65}}>
    <div style={{fontFamily:cinzel,fontSize:'.68rem',color:C.gold,background:'rgba(0,0,0,.55)',border:'1px solid rgba(200,160,40,.3)',borderRadius:4,padding:'3px 10px',letterSpacing:2,marginBottom:3}}>LV {level}</div>
    <div style={{height:3,background:'rgba(0,0,0,.4)',borderRadius:2,overflow:'hidden',marginBottom:3}}>
      <div style={{height:'100%',width:`${(xp/Math.max(1,xpNext))*100}%`,background:'linear-gradient(90deg,#c8a030,#f0d060)',borderRadius:2,transition:'width .3s'}}/>
    </div>
    <div style={{display:'flex',gap:6,justifyContent:'center',fontFamily:cinzel,fontSize:'.5rem'}}>
      <span style={{color:C.gold}}>¥{gold}</span><span style={{color:'#cc3030'}}>☠{kills}</span>
    </div>
  </div>
}

function DeathScreen({data}){
  if(!data) return null
  const {countdown,kills,level,score}=data
  return <div style={{position:'absolute',inset:0,background:'rgba(0,0,0,.82)',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',pointerEvents:'none',zIndex:100}}>
    <div style={{position:'absolute',inset:0,background:'radial-gradient(ellipse at center, transparent 40%, rgba(120,0,0,.55) 100%)'}}/>
    <div style={{fontFamily:"'Cinzel Decorative',serif",fontSize:'2.8rem',color:'#cc1010',letterSpacing:8,marginBottom:10,textShadow:'0 0 40px #ff000088'}}>YOU HAVE FALLEN</div>
    <div style={{fontFamily:crimson,fontSize:'1rem',color:'rgba(200,160,100,.7)',fontStyle:'italic',marginBottom:32,letterSpacing:2}}>The path of the samurai is paved with sacrifice.</div>
    <div style={{display:'flex',gap:32,marginBottom:36,fontFamily:cinzel}}>
      {[['LEVEL',level],['KILLS',kills],['SCORE',score]].map(([l,v])=><div key={l} style={{textAlign:'center'}}><div style={{fontSize:'1.4rem',color:C.gold,fontWeight:700}}>{v}</div><div style={{fontSize:'.5rem',color:'rgba(200,160,40,.45)',letterSpacing:3,marginTop:3}}>{l}</div></div>)}
    </div>
    <div style={{fontFamily:cinzel,fontSize:'.75rem',color:'rgba(200,160,40,.6)',letterSpacing:3}}>REBORN IN {countdown}...</div>
    <div style={{marginTop:14,fontFamily:cinzel,fontSize:'.55rem',color:'rgba(200,160,40,.35)',letterSpacing:2}}>NEW TASKS AWAIT</div>
  </div>
}

function Minimap({data}){
  const ref=useRef(null), SIZE=160
  useEffect(()=>{
    if(!data||!ref.current) return
    const ctx=ref.current.getContext('2d'), {tiles,enemies,npcs,playerX,playerY}=data
    const SC=SIZE/(WORLD_W*TILE_S), tp=SIZE/WORLD_W
    const TC={[T.DEEP_SEA]:'#0a1e3a',[T.SEA]:'#0e2e5a',[T.SHALLOW]:'#1a4a7a',[T.BEACH]:'#c8a050',[T.GRASS]:'#3a6a20',[T.TALL_GRASS]:'#2a5a18',[T.FOREST]:'#1a4a0e',[T.DENSE_FOREST]:'#122e08',[T.ROCK]:'#5a5550',[T.MOUNTAIN]:'#484440',[T.SNOW]:'#d8dce8',[T.PATH]:'#8a6a3a',[T.VILLAGE]:'#7a5030',[T.SHRINE]:'#5a3a7a',[T.BAMBOO]:'#2a6a2a',[T.RUINS]:'#4a4030',[T.BRIDGE]:'#7a5a38'}
    for(let ty=0;ty<WORLD_H;ty++) for(let tx=0;tx<WORLD_W;tx++){ctx.fillStyle=TC[tiles[ty*WORLD_W+tx]]??'#333';ctx.fillRect(tx*tp,ty*tp,tp+.5,tp+.5)}
    ctx.fillStyle='#ff3030'; for(const e of enemies){if(!e.alive)continue;ctx.beginPath();ctx.arc(e.x*SC,e.y*SC,1.5,0,Math.PI*2);ctx.fill()}
    ctx.fillStyle='#f0c040'; for(const n of npcs){ctx.beginPath();ctx.arc(n.x*SC,n.y*SC,1.5,0,Math.PI*2);ctx.fill()}
    ctx.fillStyle='#fff';ctx.strokeStyle='#000';ctx.lineWidth=1;ctx.beginPath();ctx.arc(playerX*SC,playerY*SC,3,0,Math.PI*2);ctx.fill();ctx.stroke()
  },[data])
  if(!data) return null
  return <div style={{position:'absolute',bottom:140,left:14,border:'1px solid rgba(200,160,40,.35)',borderRadius:6,overflow:'hidden',boxShadow:'0 4px 16px rgba(0,0,0,.6)'}}>
    <canvas ref={ref} width={SIZE} height={SIZE} style={{display:'block'}}/>
    <div style={{position:'absolute',top:3,left:5,fontFamily:cinzel,fontSize:'.42rem',color:'rgba(200,180,100,.6)',letterSpacing:1,pointerEvents:'none'}}>MAP · M</div>
  </div>
}

function PointerLockHint(){
  const [locked,setLocked]=useState(false)
  useEffect(()=>{const f=()=>setLocked(!!document.pointerLockElement);document.addEventListener('pointerlockchange',f);return()=>document.removeEventListener('pointerlockchange',f)},[])
  if(locked) return null
  return <div style={{position:'absolute',top:'50%',left:'50%',transform:'translate(-50%,-50%)',background:'rgba(0,0,0,.72)',border:'1px solid rgba(200,160,40,.3)',borderRadius:10,padding:'14px 24px',textAlign:'center',pointerEvents:'none',backdropFilter:'blur(8px)'}}>
    <div style={{fontFamily:cinzel,fontSize:'.75rem',color:C.gold,letterSpacing:3,marginBottom:6}}>CLICK TO CONTROL</div>
    <div style={{fontFamily:cinzel,fontSize:'.52rem',color:'rgba(200,180,100,.5)',letterSpacing:1,lineHeight:1.8}}>Mouse → Camera · Scroll → Zoom<br/>ESC → Release cursor</div>
  </div>
}

function QuestTracker({quests}){
  if(!quests?.length) return null
  return <div style={{position:'absolute',top:60,right:14,width:210,pointerEvents:'none'}}>
    <div style={{fontFamily:cinzel,fontSize:'.48rem',color:'rgba(200,160,40,.45)',letterSpacing:3,marginBottom:5,textAlign:'right'}}>OBJECTIVES</div>
    {quests.slice(0,3).map((q,i)=>{
      const pct=Math.min(1,(q.progress??0)/Math.max(1,q.count??1)), done=pct>=1
      return <div key={i} style={{background:'rgba(0,0,0,.62)',border:`1px solid ${done?'rgba(40,180,40,.3)':'rgba(200,160,40,.18)'}`,borderRadius:5,padding:'7px 10px',marginBottom:5,backdropFilter:'blur(6px)'}}>
        <div style={{fontFamily:cinzel,fontSize:'.6rem',color:done?'#40c040':C.gold,letterSpacing:1,marginBottom:3,display:'flex',justifyContent:'space-between'}}>
          <span>{done?'✓ ':'◈ '}{q.title}</span>{q.count&&<span style={{fontSize:'.52rem',opacity:.6}}>{q.progress??0}/{q.count}</span>}
        </div>
        {q.count&&<div style={{height:2,background:'rgba(255,255,255,.08)',borderRadius:1,overflow:'hidden'}}><div style={{height:'100%',borderRadius:1,width:`${pct*100}%`,background:done?'#40c040':'linear-gradient(90deg,#c8a030,#f0d060)',transition:'width .4s'}}/></div>}
        <div style={{fontFamily:crimson,fontSize:'.72rem',color:'rgba(180,160,120,.55)',marginTop:3,fontStyle:'italic',lineHeight:1.3}}>{q.desc}</div>
      </div>
    })}
    {quests.length>3&&<div style={{fontFamily:cinzel,fontSize:'.48rem',color:'rgba(200,160,40,.3)',textAlign:'right',letterSpacing:2}}>+{quests.length-3} more · TAB</div>}
  </div>
}

export default function HUD({data,canvasRef,onSave,onLoad}){
  const [showQuests,setShowQuests]=useState(false), [showSave,setShowSave]=useState(false)
  const [audioOn,setAudioOn]=useState(true), [showHelp,setShowHelp]=useState(true)
  const prevTab=useRef(0)
  useEffect(()=>{const t=setTimeout(()=>setShowHelp(false),9000);return()=>clearTimeout(t)},[])
  useEffect(()=>{const tab=data?._tabToggle??0;if(tab!==prevTab.current){prevTab.current=tab;setShowQuests(v=>!v)}},[data?._tabToggle])
  if(!data) return null
  const {hp=100,maxHp=100,stamina=100,maxStamina=100,xp=0,xpNext=150,level=1,gold=0,potions=3,kills=0,score=0,location='',time=8,weather='clear',combo=0,narration='',dialogue=null,boss=null,activeQuests=[],completedQuests=[],deathScreen=null,showMinimap=true,minimapData=null,nearNPC=false,nearItem=false}=data
  const hpCol=hp/maxHp>0.6?'#40d030':hp/maxHp>0.3?'#d0a020':'#e02020'
  const hpGlow=hp/maxHp>0.6?'#30c020':hp/maxHp>0.3?'#c09010':'#cc1010'
  const accept=q=>{canvasRef?.current?.__spawnQuest?.(q);setShowQuests(false)}

  return <div style={{position:'absolute',inset:0,pointerEvents:'none',userSelect:'none'}}>
    <DeathScreen data={deathScreen}/>
    <BossBar boss={boss}/>
    <Narration text={narration}/>
    <PointerLockHint/>
    <ComboDisplay combo={combo}/>
    <QuestTracker quests={activeQuests}/>
    {showMinimap&&<Minimap data={minimapData}/>}
    {(nearNPC||nearItem)&&!dialogue&&<div style={{position:'absolute',bottom:160,left:'50%',transform:'translateX(-50%)',background:'rgba(0,0,0,.72)',border:'1px solid rgba(200,160,40,.4)',borderRadius:6,padding:'6px 16px',pointerEvents:'none',backdropFilter:'blur(6px)'}}>
      <span style={{fontFamily:cinzel,fontSize:'.6rem',color:C.gold,letterSpacing:2}}>E  {nearNPC?'— Talk':'— Pick Up'}</span>
    </div>}
    <div style={{position:'absolute',bottom:0,left:0,right:0,height:130,background:'linear-gradient(to top, rgba(0,0,0,.88) 0%, transparent 100%)',display:'flex',alignItems:'flex-end',padding:'0 22px 14px',justifyContent:'space-between',pointerEvents:'none'}}>
      <div style={{display:'flex',alignItems:'flex-end',gap:12}}>
        <ArcBar value={hp} max={maxHp} r={36} color={hpCol} glow={hpGlow} label="HP"/>
        <div style={{paddingBottom:10}}><ThinBar value={stamina} max={maxStamina} color="linear-gradient(90deg,#20c080,#40e0a0)" glow="#20c080" label="STAMINA" W={120}/></div>
      </div>
      <SkillBar potions={potions}/>
      <div style={{display:'flex',alignItems:'flex-end',gap:14}}>
        <LevelBadge level={level} xp={xp} xpNext={xpNext} gold={gold} kills={kills}/>
        <TimeOrb timeH={time} weather={weather}/>
      </div>
    </div>
    <div style={{position:'absolute',top:14,left:14,background:C.bg,border:`1px solid ${C.border}`,borderRadius:6,padding:'5px 12px',backdropFilter:'blur(6px)'}}>
      <div style={{fontFamily:cinzel,fontSize:'.58rem',color:C.dim,letterSpacing:2}}>📍 {location}</div>
    </div>
    <div style={{position:'absolute',top:14,right:14,display:'flex',flexDirection:'column',gap:6,alignItems:'flex-end',pointerEvents:'all'}}>
      {[{label:'TAB Quests',icon:'📜',onClick:()=>setShowQuests(v=>!v),active:showQuests},{label:'💾 Save',icon:'💾',onClick:()=>setShowSave(v=>!v),active:showSave},{label:audioOn?'🔊':'🔇',icon:audioOn?'🔊':'🔇',onClick:()=>{setAudioOn(toggleAudio())},active:false}].map(btn=>(
        <button key={btn.label} style={{fontFamily:cinzel,fontSize:'.58rem',color:btn.active?'#e0c040':C.dim,background:btn.active?'rgba(200,160,40,.12)':C.bg,border:`1px solid ${btn.active?'rgba(200,160,40,.5)':C.border}`,borderRadius:5,padding:'5px 10px',cursor:'pointer',letterSpacing:1,backdropFilter:'blur(5px)',transition:'all .15s'}} onClick={btn.onClick}>{btn.icon} {btn.label}</button>
      ))}
    </div>
    {dialogue&&<div style={{pointerEvents:'all'}}><DialogueBox dialogue={dialogue} onClose={()=>{}}/></div>}
    {showQuests&&<div style={{pointerEvents:'all'}}><QuestLog quests={activeQuests} completed={completedQuests} onClose={()=>setShowQuests(false)} onAccept={accept}/></div>}
    {showSave&&<div style={{pointerEvents:'all'}}><SavePanel onSave={s=>{onSave?.(s);setShowSave(false)}} onLoad={s=>{onLoad?.(s);setShowSave(false)}} onClose={()=>setShowSave(false)}/></div>}
    {showHelp&&<div style={{position:'absolute',bottom:150,right:22,background:'rgba(0,0,0,.72)',border:'1px solid rgba(200,160,40,.18)',borderRadius:8,padding:'12px 16px',fontFamily:cinzel,fontSize:'.52rem',color:C.dim,lineHeight:2,letterSpacing:1,backdropFilter:'blur(4px)'}}>
      <div style={{fontSize:'.58rem',color:C.gold,letterSpacing:3,marginBottom:5}}>CONTROLS</div>
      {[['WASD / ↑↓←→','Move'],['Mouse','Camera'],['Scroll','Zoom'],['SPACE / J','Attack'],['Q','Dodge'],['E','Interact / Pickup'],['F','Potion'],['TAB','Quests'],['P','Pause'],['B','Spawn Boss'],['R','Respawn'],['Ctrl+S','Save'],['ESC','Release cursor']].map(([k,v])=>(
        <div key={k} style={{display:'flex',justifyContent:'space-between',gap:18}}><span style={{color:'#e0d070'}}>{k}</span><span>{v}</span></div>
      ))}
    </div>}
  </div>
}
