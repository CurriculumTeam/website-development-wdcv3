"""AI helper functions for turning gestures into spells, text, and images."""

from __future__ import annotations
from typing import Optional, Tuple

import requests
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont

import config

DEFAULT_GESTURE_TO_SPELL = {
    "Open Palm": "Shield of Light", "Fist": "Fire Burst", "Peace": "Healing Aura",
    "Point": "Lightning Strike", "Thumbs Up": "Phoenix Blessing", "No Gesture": "Dormant Magic",
}

SPELL_IMAGE_PROMPTS = {
    "Shield of Light": "A radiant magical shield forming from a glowing open hand, golden energy barrier, fantasy spell casting, cinematic fantasy art, luminous particles, enchanted temple",
    "Fire Burst": "A powerful fire spell exploding from a clenched fist, flames and sparks, fantasy combat magic, cinematic scene, glowing embers, epic magical action",
    "Healing Aura": "A peaceful healing spell with green and silver glowing energy, floating magical particles, restoration magic, fantasy art, gentle mystical light",
    "Lightning Strike": "A sharp bolt of magical lightning cast from a pointing hand, storm energy, glowing blue electricity, ancient ruins, epic fantasy spell scene",
    "Phoenix Blessing": "A fiery phoenix spirit blessing the caster, warm magical glow, flame wings, fantasy spell scene, sacred mystical fire",
    "Dormant Magic": "A quiet mystical chamber with faint glowing runes, sleeping magic, soft enchanted mist, fantasy environment art",
}


def get_spell_name_for_gesture(gesture_label: str, custom_mapping: Optional[dict] = None) -> str:
    return (custom_mapping or DEFAULT_GESTURE_TO_SPELL).get(gesture_label, "Arcane Pulse")


def build_spell_image_prompt(spell_name: str, gesture_label: str, extra_context: str = "") -> str:
    base = SPELL_IMAGE_PROMPTS.get(spell_name, f"A magical fantasy spell scene for {spell_name}, triggered by a {gesture_label} hand gesture, glowing enchanted energy, cinematic fantasy art")
    return f"{base}. {extra_context.strip()}" if extra_context.strip() else base


def generate_magic_response(gesture_label: str, spell_name: str, extra_context: str = "") -> str:
    fallback = (f"Spell Name: {spell_name}\n\nThe studio reads the gesture '{gesture_label}' and channels {spell_name}. "
                "Runes shimmer through the air as the magic awakens. "
                "A wave of energy surges outward and the room responds like a living spellbook.")
    if not config.GROQ_API_KEY:
        return fallback
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {config.GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": config.GROQ_TEXT_MODEL,
                "messages": [
                    {"role": "system", "content": "You create clean fantasy spell text for a Streamlit classroom project."},
                    {"role": "user", "content": (
                        f"You are the narrator inside a magical gesture-controlled AI studio.\n"
                        f"The user performed this gesture: {gesture_label}\n"
                        f"The detected spell is: {spell_name}\n"
                        f"Extra scene context: {extra_context}\n\n"
                        "Write a student-friendly fantasy response with:\n"
                        "1. Spell Name\n2. 3 short vivid lines of magical narration\n3. A one-line power summary\n\n"
                        "Keep it immersive, exciting, and easy to read."
                    )},
                ],
                "temperature": 0.9,
            },
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return fallback


def generate_magic_visual(prompt: str) -> Tuple[Optional[Image.Image], Optional[str]]:
    if not config.HF_API_KEY:
        return None, "HF_API_KEY is missing. Add your Hugging Face key in .env."
    try:
        image = InferenceClient(provider=config.HF_PROVIDER, api_key=config.HF_API_KEY).text_to_image(prompt, model=config.HF_IMAGE_MODEL)
        return image.convert("RGB"), None
    except Exception as e:
        return None, f"Image generation failed with model '{config.HF_IMAGE_MODEL}' and provider '{config.HF_PROVIDER}': {e}"


def wrap_text(text: str, max_chars: int = 40):
    lines, current = [], []
    for word in text.split():
        if len(" ".join(current + [word])) <= max_chars:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def create_spell_card(spell_name: str, gesture_label: str, narration_text: str, scene_image: Optional[Image.Image]) -> Image.Image:
    W, H = 900, 560
    card = Image.new("RGB", (W, H), (14, 10, 24))
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle((10, 10, W - 10, H - 10), radius=26, outline=(175, 136, 255), width=4)
    draw.rounded_rectangle((24, 24, W - 24, H - 24), radius=20, outline=(80, 60, 140), width=2)

    try:
        tf = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
        bf = ImageFont.truetype("DejaVuSans.ttf", 20)
        sf = ImageFont.truetype("DejaVuSans.ttf", 18)
    except Exception:
        tf = bf = sf = ImageFont.load_default()

    if scene_image:
        card.paste(scene_image.copy().resize((360, 360)), (40, 110))
    else:
        draw.rounded_rectangle((40, 110, 400, 470), radius=24, fill=(35, 28, 58), outline=(120, 92, 190), width=2)
        draw.text((100, 270), "No spell image", font=bf, fill=(220, 210, 255))

    draw.text((40, 36), "Gesture-to-Magic Studio", font=sf, fill=(180, 165, 235))
    draw.text((430, 60), spell_name, font=tf, fill=(245, 238, 255))
    draw.text((430, 108), f"Gesture: {gesture_label}", font=bf, fill=(190, 175, 245))

    y = 160
    for line in wrap_text(narration_text.replace("\n", " "), max_chars=38)[:10]:
        draw.text((430, y), line, font=bf, fill=(235, 230, 255))
        y += 34

    draw.text((430, 495), "Magic recognized from webcam capture", font=sf, fill=(160, 145, 220))
    return card
