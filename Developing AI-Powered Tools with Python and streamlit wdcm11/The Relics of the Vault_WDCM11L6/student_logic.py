# ═══════════════════════════════════════════════════════════════════
#  LESSON 6 — The Vault Opens
#  YOUR FILE — only edit the sections between START and END markers.
#  Everything outside those markers is provided — do not change it.
# ═══════════════════════════════════════════════════════════════════

import io, json, random
import streamlit as st
from groq import Groq
from PIL import Image, ImageDraw, ImageFont

import config
from constants import (
    MAX_TRUST, TRUST_TO_ENTER, TOTAL_CHAMBERS, BANISH_THRESHOLD,
    STREAK_BONUS_AT, EVENT_CHANCE, RELICS_NEEDED_FOR_FINAL, TRUST_TO_OPEN,
    HELPFUL_HINTS, RUDE_HINTS, SENTINEL_STYLES, SENTINEL_FEEL,
    CHAMBER_NAMES, RELIC_FALLBACKS, REPEAT_REPLIES, ACHIEVEMENTS, RANDOM_EVENTS,
)

_RARITY_COLORS = {
    "Common":(180,180,180), "Rare":(39,194,255),
    "Epic":(169,101,255),   "Legendary":(255,192,67),
}


# ── PROVIDED (completed in Lessons 4 & 5) — do not change ────────
def append_log(role: str, text: str):
    st.session_state.sentinel_messages.append(f"[{role}]: {text}")

def call_groq(sys_p: str, usr_p: str, temp: float = 0.9):
    if not config.GROQ_API_KEY: return None
    try:
        r = Groq(api_key=config.GROQ_API_KEY).chat.completions.create(
            model=config.GROQ_TEXT_MODEL, temperature=temp,
            messages=[{"role":"system","content":sys_p},{"role":"user","content":usr_p}],
        )
        return r.choices[0].message.content.strip()
    except Exception: return None

def analyze_player_tone(message: str, streak: int = 0, recent_messages: list = None) -> int:
    msg = message.lower().strip()
    if recent_messages and [m.lower().strip() for m in recent_messages[-6:]].count(msg) >= 2: return 0
    delta = 4 - (1 if len(msg) < 4 else 0)
    if any(w in msg for w in HELPFUL_HINTS): delta += 10
    if any(w in msg for w in RUDE_HINTS):    delta -= 12
    if "?" in msg: delta += 2
    if streak >= STREAK_BONUS_AT and delta > 0: delta += 6
    return max(-15, min(20, delta))

def get_sentinel_mood(trust: int) -> str:
    return "Suspicious" if trust < 20 else "Watching" if trust < 50 else "Curious" if trust < 80 else "Accepting"

def change_trust(delta: int):
    s = st.session_state
    s.trust_score = max(0, min(MAX_TRUST, s.trust_score + delta))
    s.sentinel_mood = get_sentinel_mood(s.trust_score)
    s.trust_delta_display = f"+{delta}" if delta >= 0 else str(delta)

def trust_pct() -> float:
    return st.session_state.trust_score / MAX_TRUST

def get_phase_label() -> str:
    s = st.session_state
    if s.final_unlocked:                         return "ENDGAME ONLINE"
    if len(s.chamber_history) >= TOTAL_CHAMBERS: return "RELIC FORGE"
    if s.trust_score >= TRUST_TO_ENTER:          return "VAULT EXPLORATION"
    return "TRUST GATE"

def current_scene_title() -> str:
    lc = st.session_state.last_chamber
    return lc["title"] if lc else ("Vault Threshold" if st.session_state.trust_score >= TRUST_TO_ENTER else "Outer Gate")

def current_objective() -> str:
    s = st.session_state
    if s.final_unlocked:                         return "Final vault reached. Read the ending narration."
    if len(s.chamber_history) >= TOTAL_CHAMBERS: return "Forge relics and unlock the final seal."
    if s.trust_score >= TRUST_TO_ENTER:          return "Explore chambers and collect relic-worthy clues."
    if s.trust_score >= TRUST_TO_OPEN:           return "Gate opening — earn full trust to enter."
    return "Win the Sentinel's trust and solve the logic lock."

def maybe_trigger_event():
    return random.choice(RANDOM_EVENTS) if random.random() < EVENT_CHANCE else None

def check_achievements():
    earned, s = st.session_state.achievements, st.session_state
    for ach_id, cond in [
        ("first_words",  s.messages_sent >= 1),       ("riddle_master", s.riddle_solved),
        ("trusted",      s.trust_score >= 50),         ("vault_open",    s.trust_score >= 100),
        ("explorer",     len(s.chamber_history) >= 1), ("relic_hunter",  len(s.relic_inventory) >= 1),
        ("streak_3",     s.streak >= 3),               ("legend",        s.final_unlocked),
    ]:
        if cond and ach_id not in earned:
            earned.append(ach_id)
            ach = next((a for a in ACHIEVEMENTS if a["id"] == ach_id), None)
            if ach: st.toast(f"{ach['icon']} Achievement: {ach['title']} — {ach['desc']}", icon="🏆")

def ask_sentinel(name: str, msg: str, trust: int, mood: str) -> str:
    sys_p = (f"You are The Sentinel — an ancient immortal gatekeeper.\n{SENTINEL_STYLES.get(mood, SENTINEL_STYLES['Suspicious'])}\n"
             "Talk like a real person: contractions, varied sentence length, emotional reactions.\n"
             "Never break character. Never mention being an AI. Under 80 words. End with a question, warning, or hint.")
    feel  = SENTINEL_FEEL[0 if trust < 20 else 1 if trust < 50 else 2 if trust < 80 else 3]
    usr_p = f'Traveler: {name or "Unknown"}\nHow you feel: {feel}\nMessage: "{msg}"\nRespond naturally. Don\'t reveal numbers.'
    result = call_groq(sys_p, usr_p, 0.9)
    if result: return result
    n = name or "Traveler"
    if any(w in msg.lower() for w in RUDE_HINTS):
        return random.choice([f"Watch yourself, {n}. I've turned away far greater than you for less.",
                               "That kind of talk doesn't open doors here. It closes them."])
    tiers = [(20,[f"You're here, {n}. That's something. But the gate doesn't open for just anyone."]),
             (50,["You're getting somewhere. I can feel it. Keep going."]),
             (100,["You're close. Closer than most ever get. Don't stop now."]),
             (999,[f"You've done it, {n}. The vault is yours."])]
    return random.choice(next(opts for t, opts in tiers if trust < t)).format(n=n)

def process_player_message(msg: str):
    s = st.session_state
    if not s.player_name.strip(): st.toast("Enter your traveler name first.", icon="⚠️"); return
    if not msg.strip(): return
    if [m.lower().strip() for m in s.player_messages[-6:]].count(msg.lower().strip()) >= 2:
        st.toast("The Sentinel noticed you're repeating yourself.", icon="😐")
        append_log("YOU", msg); append_log("SENTINEL", random.choice(REPEAT_REPLIES))
        s.player_messages.append(msg); s.messages_sent += 1; return
    delta = analyze_player_tone(msg, s.streak, s.player_messages)
    change_trust(delta); s.streak = s.streak + 1 if delta > 0 else 0
    append_log("YOU", msg)
    append_log("SENTINEL", ask_sentinel(s.player_name, msg, s.trust_score, s.sentinel_mood))
    s.player_messages.append(msg); s.latest_clue = "The Sentinel studies your tone."
    s.scenario_history.append(f"Gate Talk: {msg[:60]}"); s.messages_sent += 1
    if s.trust_score <= BANISH_THRESHOLD and delta < 0: s.banished = True
    event = maybe_trigger_event()
    if event:
        s.last_event = event; change_trust(event["trust_delta"])
        append_log("SYSTEM", f"EVENT: {event['title']} — {event['description']}")
        if event["id"] == "trap" and "survived_trap" not in s.achievements: s.achievements.append("survived_trap")
    check_achievements()

def process_riddle_answer(answer: str):
    s = st.session_state
    if s.riddle_solved: st.toast("Logic lock already solved.", icon="ℹ️"); return
    if not answer.strip(): return
    riddle = s.riddle
    if riddle["answer"].lower() in answer.lower().strip():
        s.riddle_solved = True; change_trust(35); s.streak += 1
        append_log("YOU", f"Riddle: {answer}")
        append_log("SENTINEL", random.choice([
            "Yes. That's it. I felt the lock shift just now — something old and heavy, finally moving.",
            "Hm. You actually got it. The seal loosens. Don't make me regret this.",
            "Correct. The gate remembers that answer. You're smarter than you look, traveler.",
        ]))
        s.latest_clue = "The runes brighten — a thin line of light appears in the gate."
        st.toast("Correct! The lock flashes open.", icon="✅")
    else:
        change_trust(-5); s.streak = 0
        append_log("YOU", f"Riddle: {answer}")
        append_log("SENTINEL", random.choice([
            "That's not it. Think harder — the hint is right in front of you.",
            "No... you're not there yet. Read the riddle again, slowly.",
            f"Wrong answer. The lock doesn't budge. Hint: {riddle['hint']}",
            f"Not quite. The gate stays shut. Here's a nudge: {riddle['hint']}",
        ]))
        s.latest_clue = f"Hint: {riddle['hint']}"
        st.toast("Incorrect — the seal holds.", icon="❌")
    check_achievements()

def chamber_scenarios() -> list:
    ch = st.session_state.last_chamber
    if not ch: return []
    t = ch["title"]
    return [
        {"title":"🔍 Inspect",    "message":f"I inspect the strange object in {t}.",   "effect":"Small details the vault wanted you to see.",  "trust":8},
        {"title":"👂 Listen",     "message":f"I listen closely to the echoes in {t}.", "effect":"A hidden rhythm points to the next mystery.", "trust":7},
        {"title":"✋ Touch Rune", "message":f"I touch the rune wall in {t}.",           "effect":"A fresh clue is revealed.",                   "trust":9},
        {"title":"➡ Follow Clue","message":f"I follow the clue in {t}.",               "effect":ch["clue"],                                    "trust":10},
    ]

def _relic_icon_art(rarity: str) -> Image.Image:
    w, h = 300, 300; img = Image.new("RGBA",(w,h),(0,0,0,0)); draw = ImageDraw.Draw(img)
    rc = _RARITY_COLORS.get(rarity,(124,92,255)); r2 = tuple(min(255,c+60) for c in rc)
    draw.ellipse((10,10,w-10,h-10), fill=(8,14,24))
    for i in range(8,0,-1): draw.ellipse((10+i*3,10+i*3,w-10-i*3,h-10-i*3), outline=rc+(int(120*i/8),), width=2)
    cx, cy = w//2, h//2
    draw.polygon([(cx,cy-70),(cx+55,cy),(cx,cy+70),(cx-55,cy)], fill=rc)
    draw.polygon([(cx,cy-70),(cx+55,cy),(cx,cy)], fill=r2)
    draw.polygon([(cx,cy-70),(cx-55,cy),(cx,cy)], fill=tuple(max(0,c-40) for c in rc))
    draw.ellipse((cx-12,cy-12,cx+12,cy+12), fill=(255,255,255,200))
    draw.ellipse((cx-5,cy-5,cx+5,cy+5), fill=(255,255,255,255))
    draw.ellipse((6,6,w-6,h-6), outline=r2+(200,), width=3)
    try: font = ImageFont.truetype("DejaVuSans-Bold.ttf",18)
    except Exception: font = ImageFont.load_default()
    lbl = rarity.upper(); bbox = draw.textbbox((0,0),lbl,font=font)
    draw.text(((w-(bbox[2]-bbox[0]))//2,h-32), lbl, fill=r2+(230,), font=font)
    return img.convert("RGB")

def _wrap_text(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textbbox((0,0),trial,font=font)[2] <= max_w: cur = trial
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines

def make_relic_card(relic: dict, relic_image: Image.Image) -> Image.Image:
    cw, ch = 900, 520; card = Image.new("RGB",(cw,ch),(8,14,24)); draw = ImageDraw.Draw(card)
    draw.rounded_rectangle((10,10,cw-10,ch-10), radius=24, outline=(124,92,255), width=4)
    draw.rounded_rectangle((24,24,cw-24,ch-24), radius=18, fill=(16,24,39))
    art = relic_image.copy().convert("RGB"); art.thumbnail((300,300))
    panel = Image.new("RGB",(300,300),(11,18,32)); panel.paste(art,((300-art.width)//2,(300-art.height)//2))
    card.paste(panel,(50,110)); draw.rounded_rectangle((50,110,350,410), radius=16, outline=(39,194,255), width=2)
    try: tf,bf,lf = ImageFont.truetype("DejaVuSans-Bold.ttf",34),ImageFont.truetype("DejaVuSans.ttf",22),ImageFont.truetype("DejaVuSans-Bold.ttf",20)
    except Exception: tf = bf = lf = ImageFont.load_default()
    x, y = 390, 60
    draw.text((x,y), relic["name"], fill=(229,236,244), font=tf); y += 52
    rc = _RARITY_COLORS.get(relic.get("rarity","Common"),(39,194,255))
    draw.text((x,y), f"Rarity: {relic['rarity']}", fill=rc, font=lf); y += 46
    for heading, content in [("Lore",relic["lore"]),("Power",relic["power"])]:
        draw.text((x,y), heading, fill=(124,92,255), font=lf); y += 30
        for line in _wrap_text(draw, content, bf, 450)[:5]: draw.text((x,y), line, fill=(229,236,244), font=bf); y += 28
        y += 18
    return card

def get_relic_image(art_prompt: str, rarity: str = "Rare") -> Image.Image:
    return _relic_icon_art(rarity)


# ═══════════════════════════════════════════════════════════════════
#  TASK 1 — generate_chamber
#
#  Use Groq to generate a chamber for the vault.
#  Returns a dict with keys: title, description, clue
#
#  Steps:
#  1. name = CHAMBER_NAMES[idx % len(CHAMBER_NAMES)]
#  2. hist = " | ".join(history[-3:]) if history else "None"
#  3. Call call_groq() with:
#       system: "Write immersive fantasy-mystery chamber descriptions.
#                Output JSON: title, description, clue."
#       user:   f"Chamber {idx+1}. Title: {name}. History: {hist}.
#                Return valid JSON only."
#       temp: 1.0
#  4. json.loads() the result → validate all 3 keys → return dict
#  5. Wrap in try/except
#  6. Fallback: return {"title": name,
#                       "description": f"{name} opens before you like a forgotten dream...",
#                       "clue": one of 4 fallback clues (use idx % 4)}
#
#  Fallback clues:
#    "A cracked clock face points toward a hidden seam in the wall."
#    "A blue crystal hums whenever the truth is spoken nearby."
#    "Dust shifts in a pattern that looks almost like writing."
#    "A silent spark jumps between metal rings above the doorway."
# ═══════════════════════════════════════════════════════════════════
def generate_chamber(idx: int, history: list) -> dict:
    # ── LESSON 6 START ───────────────────────────────────────────

    name = CHAMBER_NAMES[idx % len(CHAMBER_NAMES)]
    hist = " | ".join(history[-3:]) if history else "None"
    text = call_groq(
        "Write immersive fantasy-mystery chamber descriptions. Output JSON: title, description, clue.",
        f"Chamber {idx+1}. Title: {name}. History: {hist}. Return valid JSON only.", 1.0)
    if text:
        try:
            d = json.loads(text)
            if all(k in d for k in ["title","description","clue"]): return d
        except Exception: pass
    clues = ["A cracked clock face points toward a hidden seam in the wall.",
             "A blue crystal hums whenever the truth is spoken nearby.",
             "Dust shifts in a pattern that looks almost like writing.",
             "A silent spark jumps between metal rings above the doorway."]
    return {"title": name,
            "description": f"{name} opens before you like a forgotten dream. Pale light spills across ancient stone.",
            "clue": clues[idx % len(clues)]}

    # ── LESSON 6 END ─────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════
#  TASK 2 — generate_relic
#
#  Use Groq to generate a magical relic from a chamber.
#  Returns a dict with keys: name, rarity, lore, power, art_prompt
#
#  Steps:
#  1. Call call_groq() with:
#       system: "Create magical relics for a vault adventure.
#                Output JSON: name, rarity, lore, power, art_prompt.
#                Rarity: Common/Rare/Epic/Legendary."
#       user:   f"Relic from: {chamber_title}\n{description}\n
#                Relics so far: {count}\nReturn valid JSON only."
#       temp: 1.0
#  2. json.loads() → validate all 5 keys → return dict
#  3. Wrap in try/except
#  4. Fallback: copy RELIC_FALLBACKS[count % len(RELIC_FALLBACKS)]
#     append f" It resonates with the memory of {chamber_title}."
#     to the lore field → return it
# ═══════════════════════════════════════════════════════════════════
def generate_relic(chamber_title: str, description: str, count: int) -> dict:
    # ── LESSON 6 START ───────────────────────────────────────────

    text = call_groq(
        "Create magical relics for a vault adventure. Output JSON: name, rarity, lore, power, art_prompt. Rarity: Common/Rare/Epic/Legendary.",
        f"Relic from: {chamber_title}\n{description}\nRelics so far: {count}\nReturn valid JSON only.", 1.0)
    if text:
        try:
            d = json.loads(text)
            if all(k in d for k in ["name","rarity","lore","power","art_prompt"]): return d
        except Exception: pass
    d = RELIC_FALLBACKS[count % len(RELIC_FALLBACKS)].copy()
    d["lore"] += f" It resonates with the memory of {chamber_title}."
    return d

    # ── LESSON 6 END ─────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════
#  TASK 3 — generate_final_ending
#
#  Use Groq to narrate the triumphant ending when the vault opens.
#  Returns a string.
#
#  Steps:
#  1. Call call_groq() with:
#       system: "Narrate the final ending of a mystery vault game.
#                Triumphant, magical, under 160 words."
#       user:   f"Player: {player_name}\n
#                Relics: {', '.join(relic_names) or 'None'}\n
#                Chambers: {', '.join(chamber_history) or 'None'}"
#       temp: 0.9
#  2. If response → return it
#  3. Fallback string:
#       f"The final seal withdraws as {player_name or 'Traveler'} steps forward,
#         carrying {', '.join(relic_names) or 'no relics'}.
#         Ancient light spills across the floor.
#         A voice older than stone declares: Vault Access Granted.
#         Your journey is now legend."
# ═══════════════════════════════════════════════════════════════════
def generate_final_ending(player_name: str, relic_names: list, chamber_history: list) -> str:
    # ── LESSON 6 START ───────────────────────────────────────────

    text = call_groq(
        "Narrate the final ending of a mystery vault game. Triumphant, magical, under 160 words.",
        f"Player: {player_name}\nRelics: {', '.join(relic_names) or 'None'}\nChambers: {', '.join(chamber_history) or 'None'}")
    return text or (f"The final seal withdraws as {player_name or 'Traveler'} steps forward, carrying "
                    f"{', '.join(relic_names) or 'no relics'}. Ancient light spills across the floor. "
                    f"A voice older than stone declares: Vault Access Granted. Your journey is now legend.")

    # ── LESSON 6 END ─────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════
#  TASK 4 — apply_scenario
#
#  Called when the player clicks a chamber action button.
#  sc = {"title": str, "message": str, "effect": str, "trust": int}
#
#  Steps:
#  1.  ch = maybe_generate_current_chamber() — if None, return
#  2.  change_trust(sc["trust"])
#  3.  s.streak += 1
#  4.  append_log("YOU", sc["message"])
#  5.  append_log("SENTINEL", ask_sentinel(s.player_name or "Traveler",
#                  sc["message"], s.trust_score, s.sentinel_mood))
#  6.  s.latest_clue = sc["effect"]
#  7.  s.last_action_feedback = sc["effect"]
#  8.  s.scenario_history.append(f"{ch['title']}: {sc['title']}")
#  9.  actions = sum(1 for h in s.scenario_history if h.startswith(ch["title"]))
#  10. if sc["title"].startswith("➡") or actions >= 2:
#        nxt = s.current_chamber + 1
#        s.current_chamber = nxt
#        s.last_chamber = None
#        if nxt >= TOTAL_CHAMBERS:
#            s.door_anim = "vault"
#            append_log("SENTINEL", "All chambers have spoken. The forge awaits you now.")
#        else:
#            s.door_anim = "chamber"
#            append_log("SYSTEM", f"Chamber {nxt+1} unlocked — the door opens.")
#  11. event = maybe_trigger_event()
#      if event:
#          s.last_event = event
#          change_trust(event["trust_delta"])
#          append_log("SYSTEM", f"EVENT: {event['title']} — {event['description']}")
#  12. check_achievements()
# ═══════════════════════════════════════════════════════════════════
def apply_scenario(sc: dict):
    s = st.session_state

    # ── LESSON 6 START ───────────────────────────────────────────

    ch = maybe_generate_current_chamber()
    if not ch: return

    change_trust(sc["trust"]); s.streak += 1
    append_log("YOU", sc["message"])
    append_log("SENTINEL", ask_sentinel(s.player_name or "Traveler", sc["message"], s.trust_score, s.sentinel_mood))
    s.latest_clue = sc["effect"]; s.last_action_feedback = sc["effect"]
    s.scenario_history.append(f"{ch['title']}: {sc['title']}")

    actions = sum(1 for h in s.scenario_history if h.startswith(ch["title"]))
    if sc["title"].startswith("➡") or actions >= 2:
        nxt = s.current_chamber + 1; s.current_chamber = nxt; s.last_chamber = None
        if nxt >= TOTAL_CHAMBERS:
            s.door_anim = "vault"; append_log("SENTINEL", "All chambers have spoken. The forge awaits you now.")
        else:
            s.door_anim = "chamber"; append_log("SYSTEM", f"Chamber {nxt+1} unlocked — the door opens.")

    event = maybe_trigger_event()
    if event:
        s.last_event = event; change_trust(event["trust_delta"])
        append_log("SYSTEM", f"EVENT: {event['title']} — {event['description']}")
    check_achievements()

    # ── LESSON 6 END ─────────────────────────────────────────────


# ── PROVIDED: chamber loader — do not change ─────────────────────
def maybe_generate_current_chamber():
    s = st.session_state
    if s.trust_score < TRUST_TO_ENTER or s.current_chamber >= TOTAL_CHAMBERS: return None
    if s.last_chamber is None:
        ch = generate_chamber(s.current_chamber, s.chamber_history)
        s.last_chamber = ch; s.latest_clue = ch["clue"]
        if ch["title"] not in s.unlocked_chambers:
            s.unlocked_chambers.append(ch["title"]); s.chamber_history.append(ch["title"])
            s.chamber_descriptions[ch["title"]] = ch["description"]
            append_log("SYSTEM", f"Chamber loaded: {ch['title']}")
        check_achievements()
    return s.last_chamber


# ═══════════════════════════════════════════════════════════════════
#  TASK 5 — forge_relic
#
#  Called when the player clicks "Forge Relic" in the RELIC FORGE phase.
#  Generates a relic, builds the card image, saves it to session state.
#
#  Steps:
#  1. s = st.session_state
#  2. Guard: if not s.chamber_history → st.toast("No chambers explored yet.", icon="⚠️"), return
#  3. last_title = s.chamber_history[-1]
#  4. relic = generate_relic(last_title,
#               s.chamber_descriptions.get(last_title, f"Ancient memories of {last_title}."),
#               len(s.relic_inventory))
#  5. Inside st.spinner(f"Forging {relic['name']}…"):
#       card = make_relic_card(relic, get_relic_image(relic["art_prompt"], relic.get("rarity","Rare")))
#  6. buf = io.BytesIO(); card.save(buf, format="PNG"); relic["card_bytes"] = buf.getvalue()
#  7. s.relic_inventory.append(relic)
#  8. s.latest_clue = f"Relic materialized: {relic['name']}."
#  9. append_log("SYSTEM", f"Relic forged: {relic['name']} · {relic['rarity']}")
#  10. append_log("SENTINEL", f"I can feel it taking shape — {relic['name']}. Hold onto it. You'll need it.")
#  11. st.toast(f"💎 Relic forged: {relic['name']} [{relic['rarity']}]", icon="💎")
#  12. check_achievements()
# ═══════════════════════════════════════════════════════════════════
def forge_relic():
    s = st.session_state

    # ── LESSON 6 START ───────────────────────────────────────────

    if not s.chamber_history: st.toast("No chambers explored yet.", icon="⚠️"); return
    last_title = s.chamber_history[-1]
    relic = generate_relic(last_title, s.chamber_descriptions.get(last_title, f"Ancient memories of {last_title}."), len(s.relic_inventory))
    with st.spinner(f"Forging {relic['name']}…"):
        card = make_relic_card(relic, get_relic_image(relic["art_prompt"], relic.get("rarity","Rare")))
    buf = io.BytesIO(); card.save(buf, format="PNG"); relic["card_bytes"] = buf.getvalue()
    s.relic_inventory.append(relic); s.latest_clue = f"Relic materialized: {relic['name']}."
    append_log("SYSTEM", f"Relic forged: {relic['name']} · {relic['rarity']}")
    append_log("SENTINEL", f"I can feel it taking shape — {relic['name']}. Hold onto it. You'll need it.")
    st.toast(f"💎 Relic forged: {relic['name']} [{relic['rarity']}]", icon="💎")
    check_achievements()

    # ── LESSON 6 END ─────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════
#  TASK 6 — unlock_final_vault
#
#  Called when the player clicks "Unlock Vault" (trust = 100, relics forged).
#  Generates the ending narration and sets the final state.
#
#  Steps:
#  1. s = st.session_state
#  2. s.ending_text = generate_final_ending(
#         s.player_name,
#         [r["name"] for r in s.relic_inventory],
#         s.chamber_history)
#  3. s.final_unlocked = True
#  4. s.door_anim = "final"
#  5. s.latest_clue = "The final vault recognizes your journey."
#  6. append_log("SYSTEM", "Final seal lifted. Vault Access Granted.")
#  7. check_achievements()
# ═══════════════════════════════════════════════════════════════════
def unlock_final_vault():
    s = st.session_state

    # ── LESSON 6 START ───────────────────────────────────────────

    s.ending_text = generate_final_ending(s.player_name, [r["name"] for r in s.relic_inventory], s.chamber_history)
    s.final_unlocked = True
    s.door_anim = "final"
    s.latest_clue = "The final vault recognizes your journey."
    append_log("SYSTEM", "Final seal lifted. Vault Access Granted.")
    check_achievements()

    # ── LESSON 6 END ─────────────────────────────────────────────
