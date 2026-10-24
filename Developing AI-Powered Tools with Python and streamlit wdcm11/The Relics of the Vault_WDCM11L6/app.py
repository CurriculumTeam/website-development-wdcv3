# ── PROVIDED — do not edit ────────────────────────────────────────
"""
Lesson 6 — The Vault Opens
Run with:  streamlit run lesson_6/app.py
"""
import html, random
import streamlit as st
import streamlit.components.v1 as components

from constants import (
    APP_TITLE, MAX_TRUST, TRUST_TO_ENTER, TOTAL_CHAMBERS,
    RELICS_NEEDED_FOR_FINAL, ACCENT, ACCENT_2, BG, MUTED, TEXT,
    RIDDLES, BG_POOLS, SPRITE_TRAVELER_BASE, SPRITE_SENTINEL_URL,
)
from ui_html import hud_html, door_anim_html, feedback_html, build_scene_html

try:
    from student_logic import (
        trust_pct, get_phase_label,
        current_scene_title, current_objective,
        process_player_message, process_riddle_answer,
        maybe_generate_current_chamber, chamber_scenarios,
        apply_scenario, forge_relic, unlock_final_vault,
        change_trust, append_log, check_achievements,
        get_sentinel_mood, analyze_player_tone, ask_sentinel,
        generate_chamber, generate_relic, generate_final_ending,
    )
    _LOADED = True
except Exception as e:
    _LOADED = False; _ERR = str(e)

st.set_page_config(page_title=APP_TITLE, page_icon="🎮", layout="wide", initial_sidebar_state="collapsed")

# ── CSS ───────────────────────────────────────────────────────────
def inject_styles():
    st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');
:root{{--bg:{BG};--accent:{ACCENT};--accent2:{ACCENT_2};--text:{TEXT};--muted:{MUTED};}}
html,body,[data-testid="stAppViewContainer"]{{background:var(--bg)!important;overflow:hidden;}}
.block-container{{padding:0!important;max-width:100%!important;}}
header[data-testid="stHeader"],[data-testid="stToolbar"],.stSidebar,footer{{display:none!important;}}
iframe{{display:block!important;width:100%!important;border:none!important;}}
[data-testid="stIFrame"]{{width:100%!important;}}
div[data-testid="stVerticalBlock"]>div{{gap:0!important;}}
.ctrl-strip{{background:rgba(5,9,18,.98);border-top:1px solid rgba(124,92,255,.28);padding:8px 14px 6px;display:flex;flex-direction:column;gap:6px;overflow:hidden;}}
.ctrl-label{{font-size:.58rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:2px;}}
.stButton>button{{border-radius:8px!important;border:1px solid rgba(124,92,255,.35)!important;background:linear-gradient(180deg,rgba(124,92,255,.22),rgba(39,194,255,.12))!important;color:var(--text)!important;font-family:'Rajdhani',sans-serif!important;font-weight:600!important;font-size:.8rem!important;min-height:2rem!important;padding:0 10px!important;}}
.stTextInput input{{background:rgba(255,255,255,.03)!important;color:var(--text)!important;border-radius:8px!important;border:1px solid rgba(124,92,255,.22)!important;font-family:'Share Tech Mono',monospace!important;font-size:.82rem!important;}}
</style>""", unsafe_allow_html=True)

# ── State init (provided here since student_logic imports it) ─────
def _init_state():
    defaults = {
        "player_name":"","trust_score":0,"sentinel_mood":"Suspicious",
        "current_chamber":0,"unlocked_chambers":[],"relic_inventory":[],
        "final_unlocked":False,"chamber_history":[],"chamber_descriptions":{},
        "sentinel_messages":["[SYSTEM]: Localizing coordinates...","[SYSTEM]: Dimensional breach detected...","[SENTINEL]: Stop where you are, Traveler..."],
        "riddle":random.choice(RIDDLES),"riddle_solved":False,"last_chamber":None,
        "ending_text":"","latest_clue":"The outer gate is silent, but it is listening.",
        "scenario_history":[],"streak":0,"banished":False,"achievements":[],
        "last_event":None,"trust_delta_display":None,"messages_sent":0,
        "rules_accepted":False,"door_anim":None,"last_action_feedback":None,"player_messages":[],
    }
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v

def _reset_game():
    for k in list(st.session_state.keys()): del st.session_state[k]
    _init_state()

def _cached(key, fn):
    if key not in st.session_state: st.session_state[key] = fn()
    return st.session_state[key]

def _get_sprite_uri(kind, player_name=""):
    if kind == "traveler":
        seed = (player_name or "traveler").replace(" ","-").lower()
        return f"{SPRITE_TRAVELER_BASE}&seed={seed}"
    return SPRITE_SENTINEL_URL

def _get_scene_bg(phase):
    return random.choice(BG_POOLS.get(phase, BG_POOLS["gate"]))

# ── Input callbacks ───────────────────────────────────────────────
def _on_msg_submit():
    msg = st.session_state.get("ctrl_msg","").strip()
    if msg and _LOADED: process_player_message(msg); st.session_state["_clear_msg"] = True

def _on_riddle_submit():
    ans = st.session_state.get("ctrl_riddle","").strip()
    if ans and _LOADED: process_riddle_answer(ans); st.session_state["_clear_riddle"] = True

# ── Rules popup ───────────────────────────────────────────────────
def render_rules_popup():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Rajdhani:wght@400;600;700&display=swap');
[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse at 50% 30%,#1a0a40 0%,#0a0520 55%,#050210 100%) !important;}
.rules-wrap{max-width:700px;margin:0 auto;padding:32px 20px 20px;}
.rules-title{font-family:'Cinzel',serif;font-size:2.2rem;font-weight:700;color:#fff;text-align:center;letter-spacing:.18em;text-transform:uppercase;margin-bottom:4px;text-shadow:0 0 40px rgba(124,92,255,.9),0 0 80px rgba(39,194,255,.4);}
.rules-sub{text-align:center;font-size:.78rem;color:#7c5cff;letter-spacing:.22em;text-transform:uppercase;margin-bottom:20px;font-family:'Rajdhani',sans-serif;}
.rules-divider{height:1px;background:linear-gradient(90deg,transparent,rgba(124,92,255,.7),rgba(39,194,255,.5),transparent);margin-bottom:20px;}
.rules-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:18px;}
.rule-card{background:rgba(124,92,255,.08);border:1px solid rgba(124,92,255,.25);border-radius:12px;padding:12px 14px;display:flex;gap:10px;align-items:flex-start;}
.rule-icon{font-size:1.5rem;flex-shrink:0;}
.rule-title{font-size:.78rem;font-weight:700;color:#c9f4ff;letter-spacing:.06em;text-transform:uppercase;margin-bottom:3px;font-family:'Rajdhani',sans-serif;}
.rule-desc{font-size:.7rem;color:#95a2b8;line-height:1.5;font-family:'Rajdhani',sans-serif;}
.phases-row{display:flex;gap:8px;margin-bottom:16px;justify-content:center;}
.phase-box{flex:1;background:rgba(39,194,255,.06);border:1px solid rgba(39,194,255,.22);border-radius:10px;padding:8px 6px;text-align:center;}
.phase-icon{font-size:1.2rem;}.phase-name{font-size:.62rem;font-weight:700;color:#27c2ff;text-transform:uppercase;letter-spacing:.1em;margin-top:3px;font-family:'Rajdhani',sans-serif;}
.phase-desc{font-size:.58rem;color:#7a8aaa;margin-top:2px;font-family:'Rajdhani',sans-serif;}
.tip-box{background:rgba(242,193,79,.07);border:1px solid rgba(242,193,79,.28);border-radius:10px;padding:10px 16px;margin-bottom:20px;font-size:.72rem;color:#f2c14f;line-height:1.6;text-align:center;font-family:'Rajdhani',sans-serif;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#7c5cff,#27c2ff)!important;border:none!important;border-radius:12px!important;font-family:'Cinzel',serif!important;font-size:1.05rem!important;font-weight:700!important;color:#fff!important;letter-spacing:.15em!important;padding:14px 0!important;min-height:52px!important;box-shadow:0 0 30px rgba(124,92,255,.5)!important;text-transform:uppercase!important;}
</style>
<div class="rules-wrap">
  <div class="rules-title">⚔ AI Mystery Vault</div><div class="rules-sub">Lesson 6 — The Vault Opens</div>
  <div class="rules-divider"></div>
  <div class="rules-grid">
    <div class="rule-card"><div class="rule-icon">🗣️</div><div><div class="rule-title">Speak Wisely</div><div class="rule-desc">Polite, respectful words earn Trust. Rude words lose it fast.</div></div></div>
    <div class="rule-card"><div class="rule-icon">🔒</div><div><div class="rule-title">Solve the Riddle</div><div class="rule-desc">A logic lock guards the gate. Solve it to earn a big Trust boost.</div></div></div>
    <div class="rule-card"><div class="rule-icon">🏛️</div><div><div class="rule-title">Explore Chambers</div><div class="rule-desc">Enter the vault and explore AI-generated chambers with unique clues.</div></div></div>
    <div class="rule-card"><div class="rule-icon">💎</div><div><div class="rule-title">Forge Relics</div><div class="rule-desc">After all chambers, forge magical relics from your memories.</div></div></div>
    <div class="rule-card"><div class="rule-icon">🔑</div><div><div class="rule-title">Unlock the Vault</div><div class="rule-desc">Reach 100 trust with relics forged to unlock the final vault.</div></div></div>
    <div class="rule-card"><div class="rule-icon">👑</div><div><div class="rule-title">Read the Ending</div><div class="rule-desc">The Sentinel narrates your triumphant ending — unique to your journey.</div></div></div>
  </div>
  <div class="phases-row">
    <div class="phase-box"><div class="phase-icon">🚪</div><div class="phase-name">Trust Gate</div><div class="phase-desc">Earn trust, solve riddle</div></div>
    <div class="phase-box"><div class="phase-icon">🏛️</div><div class="phase-name">Vault</div><div class="phase-desc">Explore chambers</div></div>
    <div class="phase-box"><div class="phase-icon">🔥</div><div class="phase-name">Forge</div><div class="phase-desc">Craft relics</div></div>
    <div class="phase-box"><div class="phase-icon">👑</div><div class="phase-name">Endgame</div><div class="phase-desc">Final vault unlocked</div></div>
  </div>
  <div class="tip-box">💡 You built the AI that generates all of this — chambers, relics, and the ending are all your Groq calls.</div>
</div>""", unsafe_allow_html=True)
    _, col, _ = st.columns([1,2,1])
    with col:
        if st.button("⚔  Begin Your Journey", use_container_width=True, key="rules_begin", type="primary"):
            st.session_state.rules_accepted = True; st.rerun()

# ── HUD ───────────────────────────────────────────────────────────
def render_hud():
    s = st.session_state
    components.html(hud_html(
        APP_TITLE, s.player_name, s.trust_score, MAX_TRUST,
        s.sentinel_mood, len(s.relic_inventory), RELICS_NEEDED_FOR_FINAL,
        len(s.chamber_history), TOTAL_CHAMBERS,
        get_phase_label() if _LOADED else "TRUST GATE",
        s.streak, s.trust_delta_display,
    ), height=52, scrolling=False)

# ── Scene ─────────────────────────────────────────────────────────
def render_scene():
    s = st.session_state
    if s.banished:
        components.html("""<!DOCTYPE html><html><head><style>*{margin:0;padding:0;box-sizing:border-box;}html,body{width:100%;height:480px;background:#0a0005;display:flex;align-items:center;justify-content:center;font-family:'Rajdhani',sans-serif;overflow:hidden;}.wrap{text-align:center;}.title{font-size:3rem;font-weight:700;color:#d85757;letter-spacing:.2em;text-transform:uppercase;text-shadow:0 0 30px rgba(216,87,87,.6);animation:pulse 1.5s ease-in-out infinite;}.sub{font-size:1.1rem;color:#95a2b8;margin-top:12px;letter-spacing:.1em;}@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.5;}}</style></head><body><div class="wrap"><div class="title">&#x1F480; BANISHED</div><div class="sub">The Sentinel has cast you from the vault.<br>Your disrespect is remembered in stone.</div></div></body></html>""", height=480)
        return
    phase = ("endgame" if s.final_unlocked else
             "forge"   if len(s.chamber_history) >= TOTAL_CHAMBERS else
             "vault"   if s.trust_score >= TRUST_TO_ENTER else "gate")
    latest   = s.sentinel_messages[-1]
    is_you   = "[YOU]" in latest
    dialogue = html.escape(latest.split(":",1)[-1].strip())
    t_uri = _cached(f"_tv_{s.player_name or 'traveler'}", lambda: _get_sprite_uri("traveler", s.player_name))
    s_uri = _cached("_sv", lambda: _get_sprite_uri("sentinel"))
    bg    = _cached(f"_bg_{phase}", lambda: _get_scene_bg(phase))
    scene_title = current_scene_title() if _LOADED else ("Outer Gate")
    objective   = current_objective()   if _LOADED else ("Win the Sentinel's trust.")
    tp = trust_pct() if _LOADED else (s.trust_score / MAX_TRUST)
    components.html(build_scene_html(
        phase, bg, t_uri, s_uri,
        s.player_name or "Traveler",
        dialogue if is_you else "...",
        dialogue if not is_you else "...",
        scene_title, objective,
        s.latest_clue, s.sentinel_mood, tp, s.last_event,
        door_anim_html(s.door_anim, ACCENT, ACCENT_2),
        feedback_html(s.last_action_feedback, ACCENT_2),
    ), height=480, scrolling=False)
    s.last_event = s.trust_delta_display = s.door_anim = s.last_action_feedback = None

# ── Controls ──────────────────────────────────────────────────────
def render_controls():
    s = st.session_state
    if not _LOADED:
        st.error(f"Could not load student_logic.py — fix the error and refresh.\n\n`{_ERR}`"); return
    if s.banished:
        c1, c2 = st.columns([6,1])
        with c1: st.markdown("<div style='color:#d85757;font-family:Rajdhani,sans-serif;padding:12px 14px;font-size:.9rem;'>You have been banished. Reset to try again.</div>", unsafe_allow_html=True)
        with c2:
            if st.button("↺ Reset", use_container_width=True, key="banish_reset"): _reset_game(); st.rerun()
        return

    st.markdown("<div class='ctrl-strip'>", unsafe_allow_html=True)
    c_name, c_msg, c_send, c_reset = st.columns([1.3,4,1,0.8])
    with c_name:
        st.markdown("<div class='ctrl-label'>Traveler Name</div>", unsafe_allow_html=True)
        n = st.text_input("name", value=s.player_name, placeholder="Your name…", label_visibility="collapsed", key="ctrl_name")
        if n != s.player_name: s.player_name = n
    if s.pop("_clear_msg", False):    st.session_state["ctrl_msg"]    = ""
    if s.pop("_clear_riddle", False): st.session_state["ctrl_riddle"] = ""
    with c_msg:
        st.markdown("<div class='ctrl-label'>Message</div>", unsafe_allow_html=True)
        st.text_input("msg", placeholder="Speak to the Sentinel…", label_visibility="collapsed", key="ctrl_msg", on_change=_on_msg_submit)
    with c_send:
        st.markdown("<div class='ctrl-label'>Send</div>", unsafe_allow_html=True)
        if st.button("▶ Send", use_container_width=True, key="ctrl_send"):
            msg = st.session_state.get("ctrl_msg","").strip()
            if msg: process_player_message(msg); st.session_state["_clear_msg"] = True
            st.rerun()
    with c_reset:
        st.markdown("<div class='ctrl-label'>Reset</div>", unsafe_allow_html=True)
        if st.button("↺", use_container_width=True, key="ctrl_reset"): _reset_game(); st.rerun()

    phase = get_phase_label()

    if phase == "TRUST GATE":
        riddle = s.riddle
        if not s.riddle_solved:
            r1, r2, r3 = st.columns([4,2,1])
            with r1: st.markdown(f"<div style='font-size:.75rem;color:#c9f4ff;padding:4px 0;font-family:Rajdhani,sans-serif;'>&#x1F512; <b>Logic Lock:</b> {html.escape(riddle['question'])}</div>", unsafe_allow_html=True)
            with r2: st.text_input("riddle_ans", placeholder="Your answer…", label_visibility="collapsed", key="ctrl_riddle", on_change=_on_riddle_submit)
            with r3:
                if st.button("🔓 Solve", use_container_width=True, key="riddle_solve_btn"):
                    ans = st.session_state.get("ctrl_riddle","").strip()
                    if ans: process_riddle_answer(ans); st.session_state["_clear_riddle"] = True
                    st.rerun()
        else:
            st.markdown("<div style='font-size:.75rem;color:#18b47b;padding:4px 0;font-family:Rajdhani,sans-serif;'>✅ Logic lock solved! Keep talking to the Sentinel to build trust.</div>", unsafe_allow_html=True)

    elif phase == "VAULT EXPLORATION":
        ch = maybe_generate_current_chamber()
        if ch:
            for i, sc in enumerate(chamber_scenarios()):
                with st.columns(4)[i]:
                    if st.button(sc["title"], use_container_width=True, key=f"sc_{i}"):
                        apply_scenario(sc); st.toast(f"{sc['title']} — {sc['effect']}", icon="✨")
                        if sc["title"].startswith("👂"):
                            components.html('<audio autoplay style="display:none"><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>', height=1)
                        st.rerun()

    elif phase == "RELIC FORGE":
        c1, c2 = st.columns([3,1])
        with c1:
            if len(s.relic_inventory) < RELICS_NEEDED_FOR_FINAL:
                st.markdown("<div style='font-size:.78rem;color:#f2c14f;padding:4px 0;font-family:Rajdhani,sans-serif;'>&#x1F525; All chambers explored. Forge relics from your memories.</div>", unsafe_allow_html=True)
            elif s.trust_score < MAX_TRUST:
                st.markdown(f"<div style='font-size:.78rem;color:#27c2ff;padding:4px 0;font-family:Rajdhani,sans-serif;'>&#x1F512; Need <b>{MAX_TRUST - s.trust_score} more trust</b> — speak to the Sentinel.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='font-size:.78rem;color:#18b47b;padding:4px 0;font-family:Rajdhani,sans-serif;'>&#x2705; Trust is full. The final vault seal is ready to break.</div>", unsafe_allow_html=True)
        with c2:
            if len(s.relic_inventory) < RELICS_NEEDED_FOR_FINAL:
                if st.button("&#x1F4AB; Forge Relic", use_container_width=True, key="forge_btn"): forge_relic(); st.rerun()
            elif not s.final_unlocked:
                if s.trust_score >= MAX_TRUST:
                    if st.button("&#x1F511; Unlock Vault", use_container_width=True, key="unlock_btn"): unlock_final_vault(); st.rerun()
                else:
                    st.button("&#x1F512; Trust Needed", use_container_width=True, key="unlock_locked", disabled=True)

    elif phase == "ENDGAME ONLINE" and s.ending_text:
        relics   = ", ".join(r["name"] for r in s.relic_inventory) or "none"
        chambers = ", ".join(s.chamber_history) or "none"
        name     = html.escape(s.player_name or "Traveler")
        st.markdown(f"""<div style='background:linear-gradient(135deg,rgba(242,193,79,.12),rgba(124,92,255,.1));border:1px solid rgba(242,193,79,.5);border-radius:16px;padding:20px 24px;font-family:Rajdhani,sans-serif;text-align:center;margin:6px 0;'>
          <div style='font-family:Cinzel,serif;font-size:1.6rem;font-weight:700;color:#f2c14f;letter-spacing:.18em;text-transform:uppercase;text-shadow:0 0 30px rgba(242,193,79,.6);margin-bottom:8px;'>🏆 Vault Conquered!</div>
          <div style='font-size:.85rem;color:#eef3ff;line-height:1.7;margin-bottom:14px;'>{html.escape(s.ending_text)}</div>
          <div style='display:flex;gap:18px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;'>
            <div style='background:rgba(124,92,255,.12);border:1px solid rgba(124,92,255,.3);border-radius:10px;padding:8px 16px;'><div style='font-size:.52rem;color:#95a2b8;text-transform:uppercase;'>Traveler</div><div style='font-size:.9rem;font-weight:700;color:#c9f4ff;'>{name}</div></div>
            <div style='background:rgba(242,193,79,.08);border:1px solid rgba(242,193,79,.3);border-radius:10px;padding:8px 16px;'><div style='font-size:.52rem;color:#95a2b8;text-transform:uppercase;'>Relics</div><div style='font-size:.9rem;font-weight:700;color:#f2c14f;'>{html.escape(relics)}</div></div>
            <div style='background:rgba(39,194,255,.08);border:1px solid rgba(39,194,255,.3);border-radius:10px;padding:8px 16px;'><div style='font-size:.52rem;color:#95a2b8;text-transform:uppercase;'>Chambers</div><div style='font-size:.9rem;font-weight:700;color:#27c2ff;'>{html.escape(chambers)}</div></div>
          </div></div>""", unsafe_allow_html=True)
        _, c2, _ = st.columns([1,2,1])
        with c2:
            if st.button("🔄 Play Again", use_container_width=True, key="endgame_reset", type="primary"):
                _reset_game(); st.rerun()

    if s.relic_inventory:
        st.markdown("<div style='font-size:.58rem;color:#95a2b8;text-transform:uppercase;letter-spacing:.08em;margin-top:4px;'>Relic Inventory</div>", unsafe_allow_html=True)
        rcols = st.columns(min(len(s.relic_inventory), 5))
        for i, relic in enumerate(s.relic_inventory):
            with rcols[i % 5]:
                if "card_bytes" in relic: st.image(relic["card_bytes"], use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Main ──────────────────────────────────────────────────────────
def main():
    inject_styles(); _init_state()
    if not st.session_state.rules_accepted: render_rules_popup(); return
    render_hud(); render_scene(); render_controls()

if __name__ == "__main__": main()
