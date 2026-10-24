"""HTML/SVG/CSS string builders — no Streamlit imports here."""
import html as _h
from typing import Optional
from constants import PHASE_COLORS, WEATHER_MAP, MUTED, TEXT

# ── HUD ───────────────────────────────────────────────────────────
def hud_html(title, player_name, trust, max_trust, mood, relics, relics_needed, chambers, total_chambers, phase_label, streak, delta_display) -> str:
    pct = int(trust / max_trust * 100)
    streak_part = (f"<span style='padding:2px 9px;border-radius:999px;font-size:.68rem;font-weight:700;"
                   f"border:1px solid rgba(242,193,79,.5);background:rgba(242,193,79,.12);color:#f2c14f;margin-left:6px;'>🔥 x{streak}</span>") if streak >= 3 else ""
    delta = delta_display or ""
    delta_part = (f"<span style='font-size:.68rem;color:{'#18b47b' if delta.startswith('+') else '#d85757'};"
                  f"margin-left:4px;font-weight:700;'>{_h.escape(delta)}</span>") if delta else ""
    return f"""<!DOCTYPE html><html><head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;}}
html,body{{width:100%;height:52px;overflow:hidden;background:rgba(7,12,22,.97);font-family:'Rajdhani',sans-serif;border-bottom:1px solid rgba(124,92,255,.35);}}
.bar{{display:flex;align-items:center;height:52px;padding:0 14px;}}
.title{{font-size:1.05rem;font-weight:700;letter-spacing:.12em;color:#27c2ff;text-transform:uppercase;margin-right:16px;white-space:nowrap;}}
.stat{{display:flex;flex-direction:column;align-items:center;padding:0 11px;border-left:1px solid rgba(255,255,255,.07);min-width:76px;}}
.lbl{{font-size:.56rem;color:#95a2b8;text-transform:uppercase;letter-spacing:.08em;}}
.val{{font-size:.88rem;font-weight:700;color:#e5ecf4;white-space:nowrap;}}
.bar-wrap{{flex:1;max-width:150px;margin:0 10px;}}
.bar-bg{{height:6px;border-radius:3px;background:rgba(255,255,255,.08);overflow:hidden;}}
.bar-fill{{height:100%;border-radius:3px;background:linear-gradient(90deg,#7c5cff,#27c2ff);}}
.phase{{margin-left:auto;padding:3px 12px;border-radius:999px;font-size:.68rem;letter-spacing:.1em;border:1px solid rgba(39,194,255,.4);background:rgba(39,194,255,.08);color:#c9f4ff;text-transform:uppercase;}}
</style></head><body>
<div class="bar">
  <div class="title">&#x2694; {_h.escape(title)}</div>
  <div class="stat"><span class="lbl">Traveler</span><span class="val">{_h.escape(player_name or '—')}</span></div>
  <div class="stat"><span class="lbl">Trust</span><span class="val">{trust}/{max_trust}{delta_part}</span></div>
  <div class="bar-wrap"><div class="lbl" style="font-size:.52rem;">TRUST CORE</div><div class="bar-bg"><div class="bar-fill" style="width:{pct}%;"></div></div></div>
  <div class="stat"><span class="lbl">Mood</span><span class="val">{_h.escape(mood)}</span></div>
  <div class="stat"><span class="lbl">Relics</span><span class="val">{relics}/{relics_needed}</span></div>
  <div class="stat"><span class="lbl">Chambers</span><span class="val">{chambers}/{total_chambers}</span></div>
  {streak_part}
  <div class="phase">{_h.escape(phase_label)}</div>
</div></body></html>"""

# ── Door animation ────────────────────────────────────────────────
def door_anim_html(anim_type: Optional[str], accent: str, accent2: str) -> str:
    if not anim_type: return ""
    if anim_type == "chamber":   label,sub,color = "CHAMBER UNLOCKED","The door groans open... step forward.",accent2
    elif anim_type == "vault":   label,sub,color = "ALL CHAMBERS CLEARED","The forge fires ignite. Your relics await.",accent
    else:                        label,sub,color = "VAULT ACCESS GRANTED","You have conquered the AI Mystery Vault.","#f2c14f"
    dur = "6s" if anim_type=="final" else "3.2s"
    ddur = "3.5s" if anim_type=="final" else "2.4s"
    burst = '<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(242,193,79,.18) 0%,transparent 70%);animation:final-burst 3.5s ease 0.5s forwards;opacity:0;"></div>' if anim_type=="final" else ""
    fsz = "2.2rem" if anim_type=="final" else "1.6rem"
    tdur = "5s" if anim_type=="final" else "3s"
    gw = "6px" if anim_type=="final" else "3px"
    return f"""<div id="doorAnim" style="position:absolute;inset:0;z-index:50;pointer-events:none;display:flex;align-items:center;justify-content:center;animation:door-fade {dur} ease forwards;">
  <div style="position:absolute;top:0;left:0;width:50%;height:100%;background:linear-gradient(90deg,rgba(5,4,18,.97),rgba(10,8,28,.85));animation:door-left {ddur} cubic-bezier(.4,0,.2,1) 0.3s forwards;"></div>
  <div style="position:absolute;top:0;right:0;width:50%;height:100%;background:linear-gradient(270deg,rgba(5,4,18,.97),rgba(10,8,28,.85));animation:door-right {ddur} cubic-bezier(.4,0,.2,1) 0.3s forwards;"></div>
  <div style="position:absolute;top:0;left:50%;width:{gw};height:100%;background:linear-gradient(180deg,transparent,{color},{color},transparent);animation:door-glow {ddur} ease 0.3s forwards;opacity:0;transform:translateX(-50%);"></div>
  {burst}
  <div style="position:relative;z-index:2;text-align:center;animation:door-text {tdur} ease 0.8s forwards;opacity:0;">
    <div style="font-family:'Cinzel',serif;font-size:{fsz};font-weight:700;color:#fff;letter-spacing:.2em;text-transform:uppercase;text-shadow:0 0 40px {color},0 0 80px {color}88;">{label}</div>
    <div style="font-family:'Rajdhani',sans-serif;font-size:.85rem;color:{color};letter-spacing:.15em;margin-top:8px;">{sub}</div>
  </div>
</div>
<style>
@keyframes door-left{{0%{{transform:translateX(0);}}100%{{transform:translateX(-100%);}}}}
@keyframes door-right{{0%{{transform:translateX(0);}}100%{{transform:translateX(100%);}}}}
@keyframes door-glow{{0%{{opacity:0;}}20%{{opacity:1;}}80%{{opacity:1;}}100%{{opacity:0;}}}}
@keyframes door-text{{0%{{opacity:0;transform:scale(.9);}}20%{{opacity:1;transform:scale(1);}}80%{{opacity:1;}}100%{{opacity:0;}}}}
@keyframes door-fade{{0%,90%{{pointer-events:all;}}100%{{opacity:0;pointer-events:none;}}}}
@keyframes final-burst{{0%{{opacity:0;}}30%{{opacity:1;}}70%{{opacity:1;}}100%{{opacity:0;}}}}
</style>"""

# ── Feedback pop ──────────────────────────────────────────────────
def feedback_html(feedback: Optional[str], accent2: str) -> str:
    if not feedback: return ""
    return (f'<div style="position:absolute;bottom:175px;left:50%;transform:translateX(-50%);background:rgba(5,8,18,.96);'
            f'border:1px solid {accent2}88;border-radius:12px;padding:10px 22px;z-index:45;max-width:420px;text-align:center;'
            f'font-family:\'Rajdhani\',sans-serif;font-size:.82rem;color:#eef3ff;box-shadow:0 0 20px {accent2}44;animation:feedback-pop 3s ease forwards;">'
            f'<span style="color:{accent2};font-weight:700;margin-right:6px;">&#x2728;</span>{_h.escape(feedback)}</div>'
            f'<style>@keyframes feedback-pop{{0%{{opacity:0;transform:translateX(-50%) translateY(10px);}}15%{{opacity:1;transform:translateX(-50%) translateY(0);}}70%{{opacity:1;}}100%{{opacity:0;transform:translateX(-50%) translateY(-8px);}}}}</style>')

# ── Scene HTML ────────────────────────────────────────────────────
def scene_css(pa, pa2, muted, text_c) -> str:
    return f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Rajdhani:wght@400;600;700&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;}}html,body{{width:100%;height:480px;overflow:hidden;font-family:'Rajdhani',sans-serif;}}
#bgPhoto{{position:absolute;inset:0;z-index:0;background-size:cover;background-position:center;}}
#env{{position:absolute;inset:0;z-index:1;width:100%;height:100%;}}
.torch{{position:absolute;bottom:148px;width:12px;z-index:6;}}.torch.left{{left:calc(50% - 110px);}}.torch.right{{right:calc(50% - 110px);}}
.torch-body{{width:8px;height:28px;background:linear-gradient(180deg,#8b6914,#5a3e0a);margin:0 auto;border-radius:2px 2px 0 0;}}
.torch-flame{{width:14px;height:22px;margin:-4px auto 0;position:relative;}}
.torch-flame::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 80%,#fff176 0%,#ffb300 35%,#ff6d00 65%,transparent 100%);border-radius:50% 50% 30% 30%;animation:flicker .18s ease-in-out infinite alternate;}}
@keyframes flicker{{0%{{transform:scaleX(1) scaleY(1) rotate(-2deg);opacity:.9;}}100%{{transform:scaleX(.85) scaleY(1.12) rotate(2deg);opacity:1;}}}}
.torch-glow{{position:absolute;top:-20px;left:50%;transform:translateX(-50%);width:60px;height:60px;border-radius:50%;background:radial-gradient(circle,rgba(255,180,0,.35) 0%,transparent 70%);animation:torch-pulse 1.2s ease-in-out infinite alternate;}}
@keyframes torch-pulse{{0%{{transform:translateX(-50%) scale(1);}}100%{{transform:translateX(-50%) scale(1.2);}}}}
#weather{{position:absolute;inset:0;z-index:9;pointer-events:none;overflow:hidden;}}
.snowflake{{position:absolute;top:-10px;border-radius:50%;background:#e8f4ff;animation:snow-fall linear infinite;opacity:.8;}}
@keyframes snow-fall{{0%{{transform:translateY(0) translateX(0);}}50%{{transform:translateY(240px) translateX(15px);}}100%{{transform:translateY(490px) translateX(-10px);opacity:0;}}}}
.raindrop{{position:absolute;top:-20px;width:1.5px;background:linear-gradient(180deg,transparent,#7ec8e3cc);animation:rain-fall linear infinite;border-radius:1px;}}
@keyframes rain-fall{{0%{{transform:translateY(0) rotate(12deg);opacity:.7;}}100%{{transform:translateY(510px) rotate(12deg);opacity:0;}}}}
.sun{{position:absolute;top:18px;right:80px;width:60px;height:60px;z-index:10;}}
.sun-core{{width:60px;height:60px;border-radius:50%;background:radial-gradient(circle,#fff9c4 0%,#ffeb3b 40%,#ff9800 70%,transparent 100%);animation:sun-pulse 3s ease-in-out infinite;box-shadow:0 0 30px #ffeb3b88,0 0 60px #ff980044;}}
@keyframes sun-pulse{{0%,100%{{transform:scale(1);}}50%{{transform:scale(1.08);}}}}
.sun-ray{{position:absolute;top:50%;left:50%;width:3px;border-radius:2px;background:linear-gradient(180deg,#ffeb3b88,transparent);transform-origin:0 0;animation:ray-spin 8s linear infinite;}}
.cloud{{position:absolute;border-radius:50px;background:linear-gradient(180deg,#c8d8e8 0%,#a0b4c8 100%);animation:cloud-drift linear infinite;opacity:.75;}}
.cloud::before,.cloud::after{{content:'';position:absolute;border-radius:50%;background:inherit;}}
@keyframes cloud-drift{{0%{{transform:translateX(-200px);}}100%{{transform:translateX(1400px);}}}}
.badge{{position:absolute;top:12px;left:12px;background:rgba(5,8,18,.92);border:1px solid {pa}66;border-radius:10px;padding:5px 13px;z-index:30;backdrop-filter:blur(8px);}}
.badge-label{{font-size:.52rem;color:{muted};text-transform:uppercase;letter-spacing:.12em;}}
.badge-value{{font-size:.88rem;font-weight:700;color:{text_c};font-family:'Cinzel',serif;}}
.objective{{position:absolute;top:12px;right:12px;max-width:260px;background:rgba(5,8,18,.92);border:1px solid {pa2}55;border-radius:10px;padding:5px 13px;z-index:30;backdrop-filter:blur(8px);}}
.obj-label{{font-size:.52rem;color:{pa2};text-transform:uppercase;letter-spacing:.12em;margin-bottom:2px;}}
.obj-text{{font-size:.74rem;color:#eaf0ff;line-height:1.4;}}
.clue{{position:absolute;top:100px;left:12px;background:rgba(5,8,18,.85);border:1px solid rgba(255,255,255,.1);border-radius:999px;padding:4px 13px;font-size:.68rem;color:#e9f1ff;max-width:340px;z-index:30;backdrop-filter:blur(6px);animation:clue-pulse 3s ease-in-out infinite;}}
@keyframes clue-pulse{{0%,100%{{box-shadow:0 0 0 0 {pa}22;}}50%{{box-shadow:0 0 10px 2px {pa}44;}}}}
.event-banner{{position:absolute;top:42%;left:50%;transform:translate(-50%,-50%);background:rgba(5,8,18,.97);border:1px solid;border-radius:14px;padding:11px 22px;z-index:40;display:flex;align-items:center;gap:10px;max-width:480px;backdrop-filter:blur(12px);box-shadow:0 8px 32px rgba(0,0,0,.6);animation:event-pop 4s ease forwards;}}
@keyframes event-pop{{0%{{opacity:0;transform:translate(-50%,-65%) scale(.9);}}12%{{opacity:1;transform:translate(-50%,-50%) scale(1);}}75%{{opacity:1;}}100%{{opacity:0;transform:translate(-50%,-38%) scale(.95);}}}}
.char-card{{position:absolute;bottom:14px;z-index:20;width:130px;background:linear-gradient(160deg,rgba(10,8,28,.97),rgba(5,4,18,.99));border-radius:16px;padding:10px 10px 8px;display:flex;flex-direction:column;align-items:center;gap:4px;backdrop-filter:blur(12px);}}
.char-card.traveler{{left:2%;border:1.5px solid {pa}88;box-shadow:0 0 28px {pa}44,0 4px 20px rgba(0,0,0,.7),inset 0 1px 0 {pa}22;}}
.char-card.sentinel{{right:2%;border:1.5px solid {pa2}88;box-shadow:0 0 28px {pa2}44,0 4px 20px rgba(0,0,0,.7),inset 0 1px 0 {pa2}22;}}
.portrait-ring{{position:relative;width:80px;height:80px;}}
.portrait-ring::before{{content:'';position:absolute;inset:-4px;border-radius:50%;background:conic-gradient({pa},transparent,{pa2},transparent,{pa});animation:ring-spin 4s linear infinite;}}
.char-card.sentinel .portrait-ring::before{{background:conic-gradient({pa2},transparent,{pa},transparent,{pa2});animation-duration:5s;animation-direction:reverse;}}
.portrait-ring::after{{content:'';position:absolute;inset:-2px;border-radius:50%;background:rgba(5,4,18,.95);}}
@keyframes ring-spin{{to{{transform:rotate(360deg);}}}}
.portrait-img{{position:relative;z-index:1;width:80px;height:80px;border-radius:50%;object-fit:cover;background:rgba(10,8,28,.9);}}
.char-name{{font-size:.72rem;font-weight:700;color:#eef3ff;letter-spacing:.06em;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:110px;}}
.char-class{{font-size:.52rem;text-transform:uppercase;letter-spacing:.14em;color:{pa};margin-top:-2px;}}
.char-card.sentinel .char-class{{color:{pa2};}}
.char-bar-wrap{{width:100%;margin-top:2px;}}.char-bar-label{{font-size:.46rem;color:#95a2b8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:2px;}}
.char-bar-bg{{height:4px;border-radius:2px;background:rgba(255,255,255,.08);overflow:hidden;}}
.char-bar-fill{{height:100%;border-radius:2px;background:linear-gradient(90deg,{pa},{pa2});transition:width .6s ease;}}
.mood-badge{{font-size:.5rem;padding:2px 7px;border-radius:999px;margin-top:2px;border:1px solid {pa}55;background:{pa}18;color:{pa2};text-transform:uppercase;letter-spacing:.1em;font-weight:700;}}
.char-card.traveler{{animation:card-float-t 3.5s ease-in-out infinite;}}.char-card.sentinel{{animation:card-float-s 4.2s ease-in-out infinite;}}
@keyframes card-float-t{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-7px);}}}}
@keyframes card-float-s{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-9px);}}}}
.char-aura{{position:absolute;bottom:0;width:140px;height:140px;border-radius:50%;z-index:19;animation:aura-pulse 2.5s ease-in-out infinite;pointer-events:none;}}
.bubble{{position:absolute;bottom:168px;max-width:200px;background:rgba(5,8,18,.96);border:1px solid {pa}66;border-radius:13px;padding:8px 12px;box-shadow:0 6px 20px rgba(0,0,0,.6),0 0 10px {pa}22;z-index:25;backdrop-filter:blur(10px);animation:bubble-in .4s ease;}}
@keyframes bubble-in{{from{{opacity:0;transform:translateY(8px);}}to{{opacity:1;transform:translateY(0);}}}}
.bubble.traveler-bubble{{left:2%;}}.bubble.sentinel-bubble{{right:2%;}}
.bubble::after{{content:"";position:absolute;bottom:-9px;width:13px;height:13px;background:rgba(5,8,18,.96);border-right:1px solid {pa}66;border-bottom:1px solid {pa}66;transform:rotate(45deg);}}
.bubble.traveler-bubble::after{{left:20px;}}.bubble.sentinel-bubble::after{{right:20px;}}
.bubble-name{{color:{pa2};font-size:.56rem;text-transform:uppercase;letter-spacing:.12em;margin-bottom:3px;font-weight:700;}}
.bubble-text{{font-size:.76rem;line-height:1.4;color:#eef3ff;}}
.scanlines{{position:absolute;inset:0;z-index:35;pointer-events:none;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.04) 2px,rgba(0,0,0,.04) 4px);}}
</style>"""

def scene_svg(pa, pa2, sky_a, sky_b, sky_c) -> str:
    return f"""<svg id="env" viewBox="0 0 1280 480" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#{sky_a}"/><stop offset="55%" stop-color="#{sky_b}"/><stop offset="100%" stop-color="#{sky_c}"/></linearGradient>
    <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="{pa2}" stop-opacity=".35"/><stop offset="100%" stop-color="{pa2}" stop-opacity="0"/></radialGradient>
    <radialGradient id="gateGlow" cx="50%" cy="100%" r="60%"><stop offset="0%" stop-color="{pa}" stop-opacity=".7"/><stop offset="100%" stop-color="{pa}" stop-opacity="0"/></radialGradient>
    <filter id="blur4"><feGaussianBlur stdDeviation="4"/></filter><filter id="blur2"><feGaussianBlur stdDeviation="2"/></filter>
    <linearGradient id="groundGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0c0a1a"/><stop offset="100%" stop-color="#060410"/></linearGradient>
    <linearGradient id="stoneGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2a2440"/><stop offset="100%" stop-color="#16122a"/></linearGradient>
    <linearGradient id="archGlow" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{pa}" stop-opacity=".9"/><stop offset="100%" stop-color="{pa2}" stop-opacity=".6"/></linearGradient>
    <linearGradient id="armorGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#3a2e5a"/><stop offset="100%" stop-color="#1a1230"/></linearGradient>
    <linearGradient id="capeGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{pa}" stop-opacity=".85"/><stop offset="100%" stop-color="#0a0520" stop-opacity=".6"/></linearGradient>
    <radialGradient id="eyeGlow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="{pa2}" stop-opacity="1"/><stop offset="100%" stop-color="{pa}" stop-opacity=".3"/></radialGradient>
    <filter id="guardGlow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="softGlow"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>
  <rect width="1280" height="480" fill="url(#skyGrad)" opacity=".55"/>
  <circle cx="640" cy="60" r="55" fill="url(#moonGlow)" filter="url(#blur4)"/><circle cx="640" cy="60" r="28" fill="{pa2}" opacity=".18" filter="url(#blur2)"/><circle cx="640" cy="60" r="14" fill="{pa2}" opacity=".28"/>
  <g opacity=".7"><circle cx="80" cy="30" r="1.2" fill="#fff"/><circle cx="160" cy="55" r="1" fill="#fff"/><circle cx="240" cy="20" r="1.5" fill="#fff"/><circle cx="320" cy="45" r="1" fill="#fff"/><circle cx="420" cy="15" r="1.2" fill="#fff"/><circle cx="500" cy="38" r="1" fill="#fff"/><circle cx="780" cy="22" r="1.2" fill="#fff"/><circle cx="860" cy="48" r="1" fill="#fff"/><circle cx="960" cy="18" r="1.5" fill="#fff"/><circle cx="1040" cy="35" r="1" fill="#fff"/><circle cx="1120" cy="25" r="1.2" fill="#fff"/><circle cx="1200" cy="50" r="1" fill="#fff"/></g>
  <g opacity=".55"><polygon points="0,280 80,180 160,280" fill="#0d0b22"/><polygon points="100,280 220,150 340,280" fill="#0a0818"/><polygon points="280,280 420,130 560,280" fill="#0c0a20"/><polygon points="460,280 620,110 780,280" fill="#080616"/><polygon points="660,280 840,145 1020,280" fill="#0a0818"/><polygon points="860,280 1020,125 1180,280" fill="#0d0b22"/><polygon points="1060,280 1180,160 1280,280" fill="#0a0818"/></g>
  <g opacity=".75"><polygon points="0,320 100,220 200,320" fill="#12102a"/><polygon points="140,320 280,195 420,320" fill="#0e0c24"/><polygon points="340,320 500,175 660,320" fill="#100e28"/><polygon points="520,320 700,160 880,320" fill="#0c0a20"/><polygon points="720,320 920,190 1100,320" fill="#0e0c24"/><polygon points="940,320 1100,210 1260,320" fill="#12102a"/><polygon points="1100,320 1200,230 1280,320" fill="#0e0c24"/></g>
  <g opacity=".9"><polygon points="0,360 120,270 240,360" fill="#1a1630"/><polygon points="180,360 340,245 500,360" fill="#161228"/><polygon points="400,360 580,230 760,360" fill="#1a1630"/><polygon points="620,360 820,240 1020,360" fill="#161228"/><polygon points="840,360 1040,255 1240,360" fill="#1a1630"/><polygon points="1060,360 1180,270 1280,360" fill="#161228"/></g>
  <rect x="0" y="360" width="1280" height="120" fill="url(#groundGrad)"/>
  <ellipse cx="640" cy="480" rx="220" ry="40" fill="#1a1630" opacity=".6"/>
  <rect x="520" y="380" width="240" height="100" fill="#100e20" opacity=".5"/>
  <g stroke="#2a2440" stroke-width="1" opacity=".5"><line x1="580" y1="390" x2="700" y2="390"/><line x1="560" y1="405" x2="720" y2="405"/><line x1="545" y1="420" x2="735" y2="420"/><line x1="530" y1="435" x2="750" y2="435"/><line x1="610" y1="380" x2="610" y2="480"/><line x1="640" y1="380" x2="640" y2="480"/><line x1="670" y1="380" x2="670" y2="480"/></g>
  <g><rect x="60" y="290" width="10" height="90" fill="#1a1428" rx="2"/><polygon points="65,180 30,310 100,310" fill="#0d1a10"/><polygon points="65,210 35,305 95,305" fill="#0f1e12"/><rect x="130" y="300" width="9" height="80" fill="#1a1428" rx="2"/><polygon points="134,195 104,315 164,315" fill="#0c1a0e"/><polygon points="134,225 107,310 161,310" fill="#0e1c10"/><rect x="195" y="310" width="8" height="70" fill="#1a1428" rx="2"/><polygon points="199,215 174,320 224,320" fill="#0d1a10"/><polygon points="199,240 177,315 221,315" fill="#0f1e12"/><rect x="30" y="320" width="7" height="60" fill="#1a1428" rx="2"/><polygon points="33,240 12,330 54,330" fill="#0c1a0e"/><rect x="250" y="315" width="8" height="65" fill="#1a1428" rx="2"/><polygon points="254,225 228,325 280,325" fill="#0d1a10"/></g>
  <g><rect x="1210" y="290" width="10" height="90" fill="#1a1428" rx="2"/><polygon points="1215,180 1180,310 1250,310" fill="#0d1a10"/><polygon points="1215,210 1185,305 1245,305" fill="#0f1e12"/><rect x="1141" y="300" width="9" height="80" fill="#1a1428" rx="2"/><polygon points="1145,195 1115,315 1175,315" fill="#0c1a0e"/><polygon points="1145,225 1118,310 1172,310" fill="#0e1c10"/><rect x="1077" y="310" width="8" height="70" fill="#1a1428" rx="2"/><polygon points="1081,215 1056,320 1106,320" fill="#0d1a10"/><polygon points="1081,240 1059,315 1103,315" fill="#0f1e12"/><rect x="1243" y="320" width="7" height="60" fill="#1a1428" rx="2"/><polygon points="1246,240 1225,330 1267,330" fill="#0c1a0e"/><rect x="1022" y="315" width="8" height="65" fill="#1a1428" rx="2"/><polygon points="1026,225 1000,325 1052,325" fill="#0d1a10"/></g>
  <g opacity=".7"><rect x="380" y="310" width="7" height="70" fill="#141020" rx="2"/><polygon points="383,230 360,320 406,320" fill="#0c1810"/><rect x="440" y="320" width="6" height="60" fill="#141020" rx="2"/><polygon points="443,245 422,328 464,328" fill="#0b1610"/><rect x="840" y="310" width="7" height="70" fill="#141020" rx="2"/><polygon points="843,230 820,320 866,320" fill="#0c1810"/><rect x="900" y="320" width="6" height="60" fill="#141020" rx="2"/><polygon points="903,245 882,328 924,328" fill="#0b1610"/></g>
  <rect x="548" y="200" width="44" height="180" fill="url(#stoneGrad)" rx="4"/><rect x="688" y="200" width="44" height="180" fill="url(#stoneGrad)" rx="4"/>
  <g stroke="#3a3060" stroke-width="1" opacity=".5"><line x1="548" y1="230" x2="592" y2="230"/><line x1="548" y1="260" x2="592" y2="260"/><line x1="548" y1="290" x2="592" y2="290"/><line x1="548" y1="320" x2="592" y2="320"/><line x1="688" y1="230" x2="732" y2="230"/><line x1="688" y1="260" x2="732" y2="260"/><line x1="688" y1="290" x2="732" y2="290"/><line x1="688" y1="320" x2="732" y2="320"/></g>
  <rect x="542" y="192" width="56" height="14" fill="#3a3060" rx="3"/><rect x="682" y="192" width="56" height="14" fill="#3a3060" rx="3"/>
  <circle cx="570" cy="185" r="10" fill="{pa}" opacity=".9" filter="url(#blur2)"/><circle cx="570" cy="185" r="6" fill="{pa2}"/>
  <circle cx="710" cy="185" r="10" fill="{pa}" opacity=".9" filter="url(#blur2)"/><circle cx="710" cy="185" r="6" fill="{pa2}"/>
  <path d="M548,200 Q640,100 732,200" fill="none" stroke="url(#archGlow)" stroke-width="8"/>
  <path d="M548,200 Q640,100 732,200" fill="none" stroke="{pa}" stroke-width="3" opacity=".9"/>
  <polygon points="630,108 640,92 650,108 640,112" fill="{pa2}" opacity=".95"/>
  <rect x="592" y="200" width="96" height="180" fill="#08060f" rx="2"/>
  <rect x="598" y="210" width="38" height="80" fill="#0e0c1e" rx="2" stroke="#2a2440" stroke-width="1"/><rect x="644" y="210" width="38" height="80" fill="#0e0c1e" rx="2" stroke="#2a2440" stroke-width="1"/>
  <rect x="598" y="298" width="38" height="75" fill="#0e0c1e" rx="2" stroke="#2a2440" stroke-width="1"/><rect x="644" y="298" width="38" height="75" fill="#0e0c1e" rx="2" stroke="#2a2440" stroke-width="1"/>
  <circle cx="634" cy="295" r="5" fill="{pa}" opacity=".8"/><circle cx="646" cy="295" r="5" fill="{pa}" opacity=".8"/>
  <text x="617" y="260" font-size="14" fill="{pa}" opacity=".7" font-family="serif">&#x16A0;</text><text x="648" y="260" font-size="14" fill="{pa}" opacity=".7" font-family="serif">&#x16B7;</text>
  <text x="617" y="340" font-size="14" fill="{pa2}" opacity=".6" font-family="serif">&#x16C3;</text><text x="648" y="340" font-size="14" fill="{pa2}" opacity=".6" font-family="serif">&#x16A2;</text>
  <ellipse cx="640" cy="385" rx="120" ry="18" fill="{pa}" opacity=".18" filter="url(#blur4)"/>
  <rect x="592" y="200" width="96" height="180" fill="url(#gateGlow)" opacity=".4"/>
  <ellipse cx="755" cy="378" rx="38" ry="10" fill="{pa}" opacity=".22" filter="url(#softGlow)"/>
  <path d="M730,230 Q718,260 712,310 Q708,345 714,378 Q730,382 756,380 Q762,345 758,310 Q754,260 762,230 Z" fill="url(#capeGrad)" opacity=".9"/>
  <rect x="733" y="255" width="44" height="70" fill="url(#armorGrad)" rx="6"/>
  <rect x="737" y="260" width="36" height="28" fill="#2a2248" rx="4" stroke="{pa}" stroke-width="1" opacity=".8"/>
  <text x="748" y="279" font-size="11" fill="{pa2}" opacity=".9" font-family="serif">&#x16B9;</text>
  <rect x="733" y="318" width="44" height="8" fill="#2a1e40" rx="2" stroke="{pa}" stroke-width="1" opacity=".7"/>
  <rect x="751" y="319" width="8" height="6" fill="{pa}" rx="1" opacity=".9"/>
  <rect x="735" y="325" width="18" height="55" fill="#221a38" rx="4"/><rect x="735" y="370" width="18" height="10" fill="#1a1230" rx="3"/>
  <rect x="757" y="325" width="18" height="55" fill="#221a38" rx="4"/><rect x="757" y="370" width="18" height="10" fill="#1a1230" rx="3"/>
  <rect x="736" y="330" width="16" height="20" fill="#2a2248" rx="3" stroke="{pa}" stroke-width=".8" opacity=".7"/>
  <rect x="758" y="330" width="16" height="20" fill="#2a2248" rx="3" stroke="{pa}" stroke-width=".8" opacity=".7"/>
  <rect x="720" y="258" width="14" height="50" fill="#221a38" rx="5"/><rect x="720" y="258" width="14" height="22" fill="#2a2248" rx="4" stroke="{pa}" stroke-width=".8" opacity=".7"/>
  <rect x="776" y="258" width="14" height="50" fill="#221a38" rx="5"/><rect x="776" y="258" width="14" height="22" fill="#2a2248" rx="4" stroke="{pa}" stroke-width=".8" opacity=".7"/>
  <ellipse cx="727" cy="260" rx="12" ry="8" fill="#3a2e5a" stroke="{pa}" stroke-width="1.5" opacity=".9"/>
  <ellipse cx="783" cy="260" rx="12" ry="8" fill="#3a2e5a" stroke="{pa}" stroke-width="1.5" opacity=".9"/>
  <polygon points="720,254 727,244 734,254" fill="{pa2}" opacity=".8"/><polygon points="776,254 783,244 790,254" fill="{pa2}" opacity=".8"/>
  <rect x="746" y="238" width="18" height="20" fill="#2a2040" rx="3"/>
  <rect x="736" y="210" width="38" height="32" fill="#2e2450" rx="6"/>
  <ellipse cx="755" cy="210" rx="20" ry="12" fill="#3a2e5a"/>
  <path d="M748,198 Q755,182 762,198" fill="{pa}" opacity=".9"/>
  <rect x="752" y="184" width="6" height="16" fill="{pa}" rx="2" opacity=".85"/>
  <rect x="738" y="228" width="34" height="6" fill="#0a0818" rx="2"/>
  <circle cx="748" cy="231" r="3.5" fill="url(#eyeGlow)" filter="url(#guardGlow)"/><circle cx="762" cy="231" r="3.5" fill="url(#eyeGlow)" filter="url(#guardGlow)"/>
  <circle cx="748" cy="231" r="1.5" fill="#fff" opacity=".9"/><circle cx="762" cy="231" r="1.5" fill="#fff" opacity=".9"/>
  <rect x="734" y="214" width="8" height="22" fill="#2a2248" rx="3"/><rect x="768" y="214" width="8" height="22" fill="#2a2248" rx="3"/>
  <rect x="742" y="236" width="26" height="8" fill="#221a38" rx="3"/>
  <rect x="724" y="140" width="4" height="240" fill="#3a3060" rx="2"/>
  <polygon points="722,140 726,140 724,112" fill="{pa2}" opacity=".95"/>
  <polygon points="722,140 726,140 724,112" fill="{pa}" opacity=".5" filter="url(#blur2)"/>
  <line x1="724" y1="112" x2="724" y2="160" stroke="{pa2}" stroke-width="2" opacity=".6" filter="url(#blur2)"/>
  <rect x="718" y="175" width="16" height="4" fill="{pa}" rx="2" opacity=".8"/>
  <rect x="733" y="255" width="44" height="70" fill="none" rx="6" stroke="{pa}" stroke-width="1" opacity=".4"/>
  <rect x="718" y="388" width="76" height="16" fill="rgba(5,8,18,.85)" rx="4"/>
  <text x="756" y="400" font-size="9" fill="{pa2}" font-family="Rajdhani,sans-serif" font-weight="700" text-anchor="middle" letter-spacing="1">VAULT GUARDIAN</text>
  <g stroke="{pa}" stroke-width="1" opacity=".4"><rect x="556" y="240" width="28" height="4" rx="2" fill="{pa}" opacity=".5"/><rect x="556" y="270" width="28" height="4" rx="2" fill="{pa}" opacity=".4"/><rect x="696" y="240" width="28" height="4" rx="2" fill="{pa}" opacity=".5"/><rect x="696" y="270" width="28" height="4" rx="2" fill="{pa}" opacity=".4"/></g>
  <rect x="0" y="340" width="1280" height="80" fill="#{sky_a}" opacity=".35" filter="url(#blur4)"/>
</svg>"""

WEATHER_JS = """<script>(function(){
  var w="__WEATHER__",c=document.getElementById("weather");
  if(w==="snow"){for(var i=0;i<55;i++){var s=document.createElement("div");s.className="snowflake";var sz=(Math.random()*4+2).toFixed(1);s.style.cssText="width:"+sz+"px;height:"+sz+"px;left:"+(Math.random()*100).toFixed(1)+"%;animation-duration:"+(Math.random()*5+4).toFixed(1)+"s;animation-delay:-"+(Math.random()*8).toFixed(1)+"s;opacity:"+(Math.random()*.5+.3).toFixed(2)+";";c.appendChild(s);}}
  else if(w==="rain"){for(var i=0;i<90;i++){var r=document.createElement("div");r.className="raindrop";var h=(Math.random()*30+15).toFixed(0);r.style.cssText="height:"+h+"px;left:"+(Math.random()*100).toFixed(1)+"%;animation-duration:"+(Math.random()*.4+.5).toFixed(2)+"s;animation-delay:-"+(Math.random()*1.5).toFixed(2)+"s;opacity:"+(Math.random()*.4+.3).toFixed(2)+";";c.appendChild(r);}}
  else if(w==="sunny"){var sd=document.createElement("div");sd.className="sun";var sc=document.createElement("div");sc.className="sun-core";sd.appendChild(sc);for(var i=0;i<12;i++){var ray=document.createElement("div");ray.className="sun-ray";var len=(Math.random()*20+25).toFixed(0);ray.style.cssText="height:"+len+"px;transform:rotate("+(i*30)+"deg) translateY(-34px);animation-delay:"+(i*.15)+"s;";sd.appendChild(ray);}c.appendChild(sd);}
  else if(w==="clouds"){[{w:180,h:55,top:30,dur:28,delay:0},{w:130,h:40,top:55,dur:22,delay:-8},{w:220,h:65,top:15,dur:35,delay:-15},{w:100,h:35,top:70,dur:18,delay:-5},{w:160,h:50,top:40,dur:30,delay:-20}].forEach(function(d){var cl=document.createElement("div");cl.className="cloud";cl.style.cssText="width:"+d.w+"px;height:"+d.h+"px;top:"+d.top+"px;animation-duration:"+d.dur+"s;animation-delay:"+d.delay+"s;";var b1=document.createElement("div");b1.style.cssText="width:"+(d.w*.55).toFixed(0)+"px;height:"+(d.h*1.1).toFixed(0)+"px;top:-"+(d.h*.35).toFixed(0)+"px;left:"+(d.w*.15).toFixed(0)+"px;border-radius:50%;background:inherit;";var b2=document.createElement("div");b2.style.cssText="width:"+(d.w*.4).toFixed(0)+"px;height:"+(d.h*.9).toFixed(0)+"px;top:-"+(d.h*.25).toFixed(0)+"px;left:"+(d.w*.5).toFixed(0)+"px;border-radius:50%;background:inherit;";cl.appendChild(b1);cl.appendChild(b2);c.appendChild(cl);});}
})();</script>"""

def build_scene_html(phase, bg_uri, traveler_uri, sentinel_uri, traveler_name, traveler_text, sentinel_text,
                     scene_title, objective, clue, mood, trust_pct, event, door_anim_str, feedback_str) -> str:
    pa, pa2, pg_t, pg_s, sky_a, sky_b, sky_c = PHASE_COLORS[phase]
    weather = WEATHER_MAP[phase]
    ec_map = {"danger":"#d85757","success":"#18b47b","warn":"#d9a441"}
    event_html = ""
    if event:
        ec = ec_map.get(event["color"],"#27c2ff")
        event_html = (f'<div class="event-banner" style="border-color:{ec};color:{ec};">'
                      f'<span style="font-size:1.2rem;">{_h.escape(event["title"])}</span>'
                      f'<span style="font-size:.82rem;opacity:.9;margin-left:10px;">{_h.escape(event["description"])}</span></div>')
    tn = _h.escape(traveler_name); tt = _h.escape(traveler_text); st2 = _h.escape(sentinel_text)
    sc_title = _h.escape(scene_title); obj = _h.escape(objective); cl = _h.escape(clue); md = _h.escape(mood)
    tp = int(trust_pct * 100)
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8">'
            + scene_css(pa, pa2, MUTED, TEXT)
            + f'</head><body><div id="bgPhoto" style="background-image:url(\'{bg_uri}\');"></div>'
            + scene_svg(pa, pa2, sky_a, sky_b, sky_c)
            + f'<div class="torch left"><div class="torch-glow"></div><div class="torch-flame"></div><div class="torch-body"></div></div>'
            + f'<div class="torch right"><div class="torch-glow"></div><div class="torch-flame"></div><div class="torch-body"></div></div>'
            + f'<div id="weather"></div>'
            + f'<div class="badge"><div class="badge-label">Scene</div><div class="badge-value">{sc_title}</div></div>'
            + f'<div class="objective"><div class="obj-label">Objective</div><div class="obj-text">{obj}</div></div>'
            + f'<div class="clue">&#x1F4A1; {cl}</div>'
            + event_html
            + f'<div class="char-aura traveler" style="background:radial-gradient(circle,{pg_t} 0%,transparent 70%);"></div>'
            + f'<div class="bubble traveler-bubble"><div class="bubble-name">{tn}</div><div class="bubble-text">{tt}</div></div>'
            + f'<div class="char-card traveler"><div class="portrait-ring"><img class="portrait-img" src="{traveler_uri}" alt="Traveler"/></div>'
            + f'<div class="char-name">{tn}</div><div class="char-class">&#x2694; Traveler</div>'
            + f'<div class="char-bar-wrap"><div class="char-bar-label">Trust</div><div class="char-bar-bg"><div class="char-bar-fill" style="width:{tp}%;"></div></div></div>'
            + f'<div class="mood-badge">{md}</div></div>'
            + f'<div class="char-aura sentinel" style="background:radial-gradient(circle,{pg_s} 0%,transparent 70%);"></div>'
            + f'<div class="bubble sentinel-bubble"><div class="bubble-name">&#x1F480; The Sentinel</div><div class="bubble-text">{st2}</div></div>'
            + f'<div class="char-card sentinel"><div class="portrait-ring"><img class="portrait-img" src="{sentinel_uri}" alt="Sentinel"/></div>'
            + f'<div class="char-name">The Sentinel</div><div class="char-class">&#x1F9FF; Gatekeeper</div>'
            + f'<div class="char-bar-wrap"><div class="char-bar-label">Power</div><div class="char-bar-bg"><div class="char-bar-fill" style="width:100%;"></div></div></div>'
            + f'<div class="mood-badge">{md}</div></div>'
            + '<div class="scanlines"></div>'
            + door_anim_str + feedback_str
            + WEATHER_JS.replace("__WEATHER__", weather)
            + '</body></html>')
