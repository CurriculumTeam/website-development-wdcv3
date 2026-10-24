# ═══════════════════════════════════════════════════════════════════
#  LESSON 5 — The Sentinel Speaks
#  YOUR FILE — only edit the sections between START and END markers.
#  Everything outside those markers is provided — do not change it.
# ═══════════════════════════════════════════════════════════════════

import random
import streamlit as st
from groq import Groq

import config
from constants import (
    MAX_TRUST, BANISH_THRESHOLD, STREAK_BONUS_AT,
    HELPFUL_HINTS, RUDE_HINTS,
    MOOD_STYLES, MOOD_FEEL,
    SENTINEL_FALLBACKS, REPEAT_REPLIES,
)


# ── PROVIDED (completed in Lesson 4) — do not change ─────────────
def _append_log(role: str, text: str):
    st.session_state.sentinel_messages.append(f"[{role}]: {text}")

def analyze_player_tone(message: str, streak: int = 0, recent_messages: list = None) -> int:
    msg = message.lower().strip()
    if recent_messages:
        recent_lower = [m.lower().strip() for m in recent_messages[-6:]]
        if recent_lower.count(msg) >= 2:
            return 0
    delta = 4
    if len(msg) < 4:                                 delta -= 1
    if any(w in msg for w in HELPFUL_HINTS):         delta += 10
    if any(w in msg for w in RUDE_HINTS):            delta -= 12
    if "?" in msg:                                   delta += 2
    if streak >= STREAK_BONUS_AT and delta > 0:      delta += 6
    return max(-15, min(20, delta))

def get_sentinel_mood(trust: int) -> str:
    if trust < 20: return "Suspicious"
    if trust < 50: return "Watching"
    if trust < 80: return "Curious"
    return "Accepting"


# ═══════════════════════════════════════════════════════════════════
#  TASK 1 — fallback_sentinel
#
#  When there is no API key or the API fails, the Sentinel still
#  needs to respond. Write a fallback that picks a reply based on
#  the current mood and whether the player was rude.
#
#  Rules:
#  • If any word in RUDE_HINTS appears in message → pick from rude replies:
#      "Watch yourself. I've turned away far greater than you for less."
#      "That kind of talk doesn't open doors here. It closes them."
#      "Careful. The vault remembers every word spoken at its gate."
#  • Otherwise → return random.choice(SENTINEL_FALLBACKS[mood])
#    (SENTINEL_FALLBACKS is a dict: mood → list of reply strings)
# ═══════════════════════════════════════════════════════════════════
def fallback_sentinel(player_name: str, message: str, mood: str) -> str:
    # ── LESSON 5 START ───────────────────────────────────────────

    if any(w in message.lower() for w in RUDE_HINTS):
        return random.choice([
            "Watch yourself. I've turned away far greater than you for less.",
            "That kind of talk doesn't open doors here. It closes them.",
            "Careful. The vault remembers every word spoken at its gate.",
        ])
    return random.choice(SENTINEL_FALLBACKS.get(mood, SENTINEL_FALLBACKS["Suspicious"]))

    # ── LESSON 5 END ─────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════
#  TASK 2 — ask_sentinel
#
#  Call the Groq API to get a live AI response from the Sentinel,
#  shaped by the current mood and the player's message.
#
#  Steps:
#  1. Guard — if config.GROQ_API_KEY is empty → return fallback_sentinel(...)
#  2. Build system_prompt:
#       "You are The Sentinel — an ancient immortal gatekeeper.\n"
#       + MOOD_STYLES[mood] + "\n"
#       + "Use contractions, vary sentence length, react emotionally.\n"
#       + "Never break character. Never mention being an AI.\n"
#       + "Under 80 words. End with a question, warning, or hint."
#  3. Build user_prompt:
#       "Traveler: {player_name}\n"
#       + "How you feel: {MOOD_FEEL[mood]}\n"
#       + "Their message: \"{message}\"\n"
#       + "Respond naturally. Don't reveal any numbers."
#  4. Call Groq:
#       Groq(api_key=config.GROQ_API_KEY).chat.completions.create(
#           model=config.GROQ_TEXT_MODEL, temperature=0.9,
#           messages=[{"role":"system","content":system_prompt},
#                     {"role":"user","content":user_prompt}])
#       return r.choices[0].message.content.strip()
#  5. Wrap steps 3–4 in try/except → on error return fallback_sentinel(...)
# ═══════════════════════════════════════════════════════════════════
def ask_sentinel(player_name: str, message: str, trust: int, mood: str) -> str:
    # ── LESSON 5 START ───────────────────────────────────────────

    if not config.GROQ_API_KEY:
        return fallback_sentinel(player_name, message, mood)

    system_prompt = (
        f"You are The Sentinel — an ancient immortal gatekeeper.\n"
        f"{MOOD_STYLES.get(mood, MOOD_STYLES['Suspicious'])}\n"
        "Use contractions, vary sentence length, react emotionally.\n"
        "Never break character. Never mention being an AI.\n"
        "Under 80 words. End with a question, warning, or hint."
    )

    user_prompt = (
        f"Traveler: {player_name or 'Unknown'}\n"
        f"How you feel about them: {MOOD_FEEL.get(mood, MOOD_FEEL['Suspicious'])}\n"
        f"Their message: \"{message}\"\n"
        "Respond naturally. Don't reveal any numbers."
    )

    try:
        r = Groq(api_key=config.GROQ_API_KEY).chat.completions.create(
            model=config.GROQ_TEXT_MODEL,
            temperature=0.9,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
        )
        return r.choices[0].message.content.strip()
    except Exception:
        return fallback_sentinel(player_name, message, mood)

    # ── LESSON 5 END ─────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════
#  TASK 3 — generate_riddle_hint
#
#  When the player gets the riddle wrong, use Groq to generate a
#  creative, in-character hint from the Sentinel — not just the
#  plain hint text from constants.
#
#  Steps:
#  1. Guard — if no API key → return f"Hint: {plain_hint}"
#  2. Build a system prompt:
#       "You are The Sentinel. Give a cryptic, atmospheric one-line
#        hint for a riddle. Stay in character. Under 30 words."
#  3. Build a user prompt:
#       f"The riddle is: {riddle_question}\n
#         The answer is: {riddle_answer}\n
#         Give a cryptic hint without revealing the answer."
#  4. Call Groq (temperature=1.0) → return the response
#  5. Wrap in try/except → on error return f"Hint: {plain_hint}"
# ═══════════════════════════════════════════════════════════════════
def generate_riddle_hint(riddle_question: str, riddle_answer: str, plain_hint: str) -> str:
    # ── LESSON 5 START ───────────────────────────────────────────

    if not config.GROQ_API_KEY:
        return f"Hint: {plain_hint}"

    try:
        r = Groq(api_key=config.GROQ_API_KEY).chat.completions.create(
            model=config.GROQ_TEXT_MODEL,
            temperature=1.0,
            messages=[
                {"role": "system", "content": (
                    "You are The Sentinel. Give a cryptic, atmospheric one-line hint "
                    "for a riddle. Stay in character. Under 30 words."
                )},
                {"role": "user", "content": (
                    f"The riddle is: {riddle_question}\n"
                    f"The answer is: {riddle_answer}\n"
                    "Give a cryptic hint without revealing the answer."
                )},
            ],
        )
        return r.choices[0].message.content.strip()
    except Exception:
        return f"Hint: {plain_hint}"

    # ── LESSON 5 END ─────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════
#  TASK 4 — generate_event_narration
#
#  When a random vault event fires, use Groq to narrate it in the
#  Sentinel's voice instead of showing the plain description.
#
#  Steps:
#  1. Guard — if no API key → return plain_description
#  2. Build a system prompt:
#       "You are The Sentinel narrating a vault event. One dramatic
#        sentence, in character, under 25 words."
#  3. Build a user prompt:
#       f"Event: {event_title}\nDescription: {plain_description}\n
#         Narrate this as The Sentinel in one sentence."
#  4. Call Groq (temperature=0.95) → return the response
#  5. Wrap in try/except → on error return plain_description
# ═══════════════════════════════════════════════════════════════════
def generate_event_narration(event_title: str, plain_description: str) -> str:
    # ── LESSON 5 START ───────────────────────────────────────────

    if not config.GROQ_API_KEY:
        return plain_description

    try:
        r = Groq(api_key=config.GROQ_API_KEY).chat.completions.create(
            model=config.GROQ_TEXT_MODEL,
            temperature=0.95,
            messages=[
                {"role": "system", "content": (
                    "You are The Sentinel narrating a vault event. "
                    "One dramatic sentence, in character, under 25 words."
                )},
                {"role": "user", "content": (
                    f"Event: {event_title}\n"
                    f"Description: {plain_description}\n"
                    "Narrate this as The Sentinel in one sentence."
                )},
            ],
        )
        return r.choices[0].message.content.strip()
    except Exception:
        return plain_description

    # ── LESSON 5 END ─────────────────────────────────────────────


# ── PROVIDED: game message handler (completed in Lesson 4) — do not change
def process_player_message(msg: str):
    s = st.session_state
    if not s.player_name.strip():
        st.toast("Enter your traveler name first.", icon="⚠️"); return
    if not msg.strip(): return
    recent = [m.lower().strip() for m in s.player_messages[-6:]]
    if recent.count(msg.lower().strip()) >= 2:
        st.toast("The Sentinel noticed you're repeating yourself.", icon="😐")
        _append_log("YOU", msg)
        _append_log("SENTINEL", random.choice(REPEAT_REPLIES))
        s.player_messages.append(msg); s.messages_sent += 1; return
    delta = analyze_player_tone(msg, s.streak, s.player_messages)
    s.trust_score = max(0, min(MAX_TRUST, s.trust_score + delta))
    s.sentinel_mood = get_sentinel_mood(s.trust_score)
    s.streak = s.streak + 1 if delta > 0 else 0
    _append_log("YOU", msg)
    _append_log("SENTINEL", ask_sentinel(s.player_name, msg, s.trust_score, s.sentinel_mood))
    s.player_messages.append(msg)
    s.latest_clue = "The Sentinel studies your tone."
    s.messages_sent += 1
    if s.trust_score <= BANISH_THRESHOLD and delta < 0: s.banished = True


# ── PROVIDED: riddle handler (completed in Lesson 4) — do not change
def process_riddle_answer(answer: str):
    s = st.session_state
    if s.riddle_solved: st.toast("Logic lock already solved.", icon="ℹ️"); return
    if not answer.strip(): return
    riddle = s.riddle
    if riddle["answer"].lower() in answer.lower().strip():
        s.riddle_solved = True
        s.trust_score = min(MAX_TRUST, s.trust_score + 35)
        s.sentinel_mood = get_sentinel_mood(s.trust_score)
        s.streak += 1
        _append_log("YOU", f"Riddle: {answer}")
        _append_log("SENTINEL", random.choice([
            "Yes. That's it. I felt the lock shift just now — something old and heavy, finally moving.",
            "Hm. You actually got it. The seal loosens. Don't make me regret this.",
            "Correct. The gate remembers that answer. You're smarter than you look, traveler.",
        ]))
        s.latest_clue = "The runes brighten — a thin line of light appears in the gate."
        st.toast("Correct! The lock flashes open.", icon="✅")
    else:
        s.trust_score = max(0, s.trust_score - 5)
        s.sentinel_mood = get_sentinel_mood(s.trust_score)
        s.streak = 0
        _append_log("YOU", f"Riddle: {answer}")
        # Use AI-generated hint if available
        hint_reply = generate_riddle_hint(riddle["question"], riddle["answer"], riddle["hint"])
        _append_log("SENTINEL", hint_reply)
        s.latest_clue = f"Hint: {riddle['hint']}"
        st.toast("Incorrect — the seal holds.", icon="❌")
