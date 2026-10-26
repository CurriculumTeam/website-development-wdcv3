"""
Lesson 3 — Gesture-to-Magic Studio (Full App)
Complete magic control app: gesture detection + AI narration + spell image + spell card + spell log.
Run: streamlit run lesson3/app.py
"""

# ===== LESSON 3 ===============================================================

import streamlit as st
from PIL import Image
import config
from ai_helpers import (
    build_spell_image_prompt, create_spell_card,
    generate_magic_response, generate_magic_visual, get_spell_name_for_gesture,
)
from gesture_utils import load_local_teachable_machine_model, predict_gesture_from_image

st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_ICON, layout="wide")

_DEFAULTS = {
    "prediction": None, "captured_image": None, "input_source": "", "spell_name": "",
    "spell_text": "", "spell_prompt": "", "spell_scene_image": None, "spell_card_image": None,
    "spell_log": [], "last_generated_key": "",
    "gesture_mapping": {"Palm": "Shield of Light", "Peace": "Healing Aura",
                        "Pointer": "Lightning Strike", "Thumbs Up": "Phoenix Blessing"},
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

_LABEL_MAP = {
    "Open Palm": "Palm", "Palm": "Palm", "Peace": "Peace",
    "Pointer": "Pointer", "Point": "Pointer",
    "Thumbs Up": "Thumbs Up", "Thumbsup": "Thumbs Up", "No Gesture": "No Gesture",
}

def render_styles():
    st.markdown("""
        <style>
        .stApp       { background: radial-gradient(circle at top, #241339 0%, #100914 42%, #07070b 100%); color: #f5efff; }
        .hero-panel  { padding: 22px; border-radius: 22px; border: 1px solid rgba(191,158,255,.20); background: linear-gradient(135deg,rgba(44,24,70,.92),rgba(15,12,30,.96)); margin-bottom: 1rem; }
        .main-panel  { padding: 20px; border-radius: 22px; border: 1px solid rgba(191,158,255,.18); background: rgba(255,255,255,.03); box-shadow: 0 0 32px rgba(118,80,255,.10); margin-bottom: 1rem; }
        .status-card { padding: 14px; border-radius: 16px; background: rgba(148,99,255,.10); border: 1px solid rgba(180,148,255,.18); text-align: center; min-height: 86px; }
        .spell-box   { padding: 16px; border-radius: 16px; background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.08); margin-bottom: 12px; }
        .small-note  { color: #ccbdfa; font-size: .95rem; }
        .source-pill { display: inline-block; padding: 7px 12px; border-radius: 999px; background: rgba(108,75,214,.18); border: 1px solid rgba(193,170,255,.18); color: #efe7ff; margin-bottom: 12px; }
        .detect-card { padding: 14px; border-radius: 16px; background: rgba(94,67,170,.14); border: 1px solid rgba(186,163,255,.18); margin-bottom: 10px; }
        </style>""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def get_model_and_labels():
    return load_local_teachable_machine_model(str(config.MODEL_PATH), str(config.LABELS_PATH))

def normalize_label(label: str) -> str:
    return _LABEL_MAP.get(label.strip(), label.strip())

def build_hidden_prompt(label: str, spell: str, source: str) -> str:
    ctx = ("The magic scene should clearly feel triggered by a live webcam-captured hand gesture."
           if source == "webcam" else
           "The magic scene should clearly feel triggered by the uploaded hand gesture image.")
    return build_spell_image_prompt(spell, label, extra_context=(
        f"{ctx} Keep the hand sign influence visible in the composition. "
        "Make it cinematic, fantasy-rich, colorful, magical, and suitable for a student project."
    ))

def show_input_panel():
    st.markdown('<div class="main-panel">', unsafe_allow_html=True)
    st.subheader("📷 Input")
    st.markdown('<p class="small-note">Use webcam capture or upload an image. The app will detect Palm, Peace, Pointer, or Thumbs Up.</p>', unsafe_allow_html=True)
    tabs = st.tabs(["Webcam Capture", "Upload Image"])
    with tabs[0]:
        cam = st.camera_input("Capture gesture from webcam", help=config.CAMERA_HELP)
        if cam:
            prediction_panel(Image.open(cam).convert("RGB"), "webcam")
        else:
            st.info("Take a photo with your webcam to detect a gesture.")
    with tabs[1]:
        up = st.file_uploader("Upload a gesture image", type=["png", "jpg", "jpeg"])
        if up:
            prediction_panel(Image.open(up).convert("RGB"), "upload")
        else:
            st.info("Upload a hand gesture image to detect a gesture.")
    st.markdown('</div>', unsafe_allow_html=True)

def show_output_panel():
    st.markdown('<div class="main-panel">', unsafe_allow_html=True)
    st.subheader("🪄 Output")
    for label, val in [("Spell Name", st.session_state.spell_name), ("Spell Narration", st.session_state.spell_text)]:
        if val:
            st.markdown(f'<div class="spell-box"><b>{label}</b><br><br>{val.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.session_state.spell_scene_image is not None:
            st.image(st.session_state.spell_scene_image, caption="AI-generated spell scene", use_container_width=True)
        else:
            st.info("The spell image will appear here after generation.")
    with c2:
        if st.session_state.spell_card_image is not None:
            st.image(st.session_state.spell_card_image, caption="Collectible spell card", use_container_width=True)
        else:
            st.info("The spell card will appear here after generation.")
    st.markdown('</div>', unsafe_allow_html=True)

def show_spell_log():
    st.markdown('<div class="main-panel">', unsafe_allow_html=True)
    c1, c2 = st.columns([0.8, 0.2])
    c1.subheader("📚 Spell Log")
    with c2:
        if st.button("Reset Studio", use_container_width=True):
            reset_magic_session()
            st.rerun()
    if st.session_state.spell_log:
        for i, item in enumerate(st.session_state.spell_log, 1):
            with st.expander(f"Spell {i}: {item['spell']} ({item['gesture']})"):
                st.write(f"Source: {item['source']}")
                st.write(item["text"])
    else:
        st.caption("Your spell history will appear here after you generate magic.")
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    render_styles()
    st.markdown(f"""
        <div class="hero-panel">
            <h1 style="margin:0 0 6px 0;">✨ {config.APP_TITLE}</h1>
            <p style="margin:0;">Show a hand gesture in the webcam or upload a gesture image. The app detects the sign,
            maps it to a magical spell, then creates AI story and AI image output automatically.</p>
        </div>""", unsafe_allow_html=True)
    with st.expander("ℹ️ What this app does and what it detects", expanded=False):
        st.write("This app looks at a webcam capture or uploaded image, predicts the hand gesture using your Teachable Machine model, and turns it into a magic spell experience.")
        st.markdown("**Detected gestures**\n- Palm\n- Peace\n- Pointer\n- Thumbs Up")
        st.markdown("**Flow**\n1. Capture or upload a hand gesture image\n2. Detect the gesture\n3. Convert it into a spell\n4. Generate AI spell story\n5. Generate AI spell image")
    show_hud()
    left, right = st.columns([0.95, 1.05], gap="large")
    with left:
        show_input_panel()
    with right:
        show_output_panel()
    show_spell_log()

# ----- STUDENT CODE -----------------------------------------------------------

def reset_magic_session():
    for k, v in _DEFAULTS.items():
        st.session_state[k] = v

def generate_magic_bundle():
    if not st.session_state.prediction:
        st.warning("Capture or upload an image first.")
        return
    label = st.session_state.prediction["label"]
    spell = st.session_state.spell_name
    st.session_state.spell_prompt = build_hidden_prompt(label, spell, st.session_state.input_source)
    with st.spinner("Casting AI magic from the detected gesture..."):
        st.session_state.spell_text = generate_magic_response(label, spell, f"This spell came from a {st.session_state.input_source} hand-gesture image.")
        img, err = generate_magic_visual(st.session_state.spell_prompt)
        if img:
            st.session_state.spell_scene_image = img
            st.session_state.spell_card_image = create_spell_card(spell, label, st.session_state.spell_text, img)
        else:
            st.session_state.spell_scene_image = st.session_state.spell_card_image = None
            st.error(err or "Could not generate the spell image.")
        st.session_state.spell_log = ([{"gesture": label, "spell": spell, "text": st.session_state.spell_text, "source": st.session_state.input_source}]
                                       + st.session_state.spell_log)[:config.MAX_SPELL_LOG]

def show_hud():
    c1, c2, c3, c4 = st.columns(4)
    gesture = st.session_state.prediction["label"] if st.session_state.prediction else "Waiting"
    spell = st.session_state.spell_name or "No Spell Yet"
    for col, label, val in [
        (c1, "Supported Gestures", "Palm · Peace · Pointer · Thumbs Up"),
        (c2, "Detected Gesture", gesture),
        (c3, "Active Spell", spell),
        (c4, "Spell Log", len(st.session_state.spell_log)),
    ]:
        col.markdown(f'<div class="status-card"><b>{label}</b><br>{val}</div>', unsafe_allow_html=True)

def prediction_panel(current_image: Image.Image, source_name: str):
    st.session_state.captured_image = current_image
    st.session_state.input_source = source_name
    st.image(current_image, caption="Gesture image used for magic casting", use_container_width=True)
    st.markdown(f'<div class="source-pill">Input source: {source_name.title()}</div>', unsafe_allow_html=True)
    try:
        model, labels = get_model_and_labels()
        pred = predict_gesture_from_image(model, labels, current_image)
        pred["label"] = normalize_label(pred["label"])
        for item in pred["top_predictions"]:
            item["label"] = normalize_label(item["label"])
        st.session_state.prediction = pred
        spell = get_spell_name_for_gesture(pred["label"], st.session_state.gesture_mapping)
        st.session_state.spell_name = spell
        st.success(f"Detected gesture: {pred['label']}")
        st.progress(float(pred["confidence"]), text=f"Confidence: {pred['confidence']:.1%}")
        c1, c2 = st.columns(2)
        c1.markdown(f'<div class="detect-card"><b>Detected</b><br>{pred["label"]}</div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="detect-card"><b>Mapped Spell</b><br>{spell}</div>', unsafe_allow_html=True)
        with st.expander("See all prediction scores"):
            for item in pred["top_predictions"]:
                st.progress(float(item["confidence"]), text=f"{item['label']} — {item['confidence']:.1%}")
        key = f"{source_name}:{pred['label']}:{pred['confidence']:.4f}"
        if st.session_state.last_generated_key != key:
            if st.button("Generate Magic From This Image ✨", use_container_width=True):
                generate_magic_bundle()
                st.session_state.last_generated_key = key
    except Exception as e:
        st.error(f"Could not load or run the local model: {e}\n\nTip: use Python 3.10/3.11 and tensorflow==2.15.0 for Teachable Machine .h5 models.")

# ===== END LESSON 3 ===========================================================

if __name__ == "__main__":
    main()
