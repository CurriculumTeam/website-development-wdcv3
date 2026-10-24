import io
import streamlit as st
from huggingface_hub import InferenceClient
import config

st.set_page_config(page_title="AI Avatar Creator", page_icon="🎨", layout="centered")

OPTIONS = {
    "avatar type": ["boy hero", "girl hero", "wizard", "robot explorer", "space warrior", "animal adventurer"],
    "hairstyle": ["short spiky hair", "curly hair", "long straight hair", "ponytail", "glowing hair", "helmet"],
    "outfit": ["superhero suit", "magical robe", "space armor", "casual hoodie", "battle costume", "royal outfit"],
    "expression": ["happy", "confident", "excited", "brave", "mysterious", "playful"],
    "background": ["forest", "space station", "magic castle", "city skyline", "rainbow world", "cloud kingdom"],
    "art style": ["cartoon style", "anime style", "3D game style", "fantasy illustration", "comic style"],
}

client = InferenceClient(api_key=config.HF_API_KEY)
st.session_state.setdefault("generated_image", None)

st.title("🎨 AI Avatar Creator")
st.write("Create your own avatar with AI!")
st.markdown("Choose your avatar details or write your own custom prompt, then click **Generate Avatar**.")
st.subheader("🛠️ Create Your Avatar")

mode = st.selectbox("Choose prompt mode", ["Use Avatar Builder", "Write Custom Prompt"])

if mode == "Use Avatar Builder":
    values = {k: st.selectbox(f"Choose {k}", v) for k, v in OPTIONS.items()}
    extra = st.text_input("Add one extra detail (optional)", placeholder="Example: glowing blue eyes").strip()

    prompt = (
        f"A kid-friendly {values['avatar type']}, "
        f"with {values['hairstyle']}, "
        f"wearing {values['outfit']}, "
        f"with a {values['expression']} expression, "
        f"in a {values['background']} background, "
        f"{values['art style']}, colorful, highly detailed, digital art"
    )
    final_prompt = f"{prompt}, {extra}" if extra else prompt
else:
    final_prompt = st.text_area(
        "Write your own prompt",
        placeholder="Example: A brave young wizard with silver hair, glowing green eyes, a floating spell book, standing in a magical forest, fantasy illustration",
        height=150,
    ).strip()

with st.expander("👀 See the AI prompt"):
    st.write(final_prompt or "Your prompt will appear here.")

if st.button("✨ Generate Avatar"):
    if not config.HF_API_KEY:
        st.error("Hugging Face API key is missing. Please add it to your .env file.")
    elif not final_prompt:
        st.warning("Please create or enter a prompt first.")
    else:
        with st.spinner("Creating your avatar..."):
            try:
                st.session_state.generated_image = client.text_to_image(
                    prompt=final_prompt,
                    model=config.HF_IMAGE_MODEL,
                )
                st.success("Your avatar is ready!")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if st.session_state.generated_image:
    st.image(st.session_state.generated_image, caption="Your AI Avatar", use_container_width=True)

    buffer = io.BytesIO()
    st.session_state.generated_image.save(buffer, format="PNG")

    st.download_button(
        "📥 Download Avatar",
        data=buffer.getvalue(),
        file_name="ai_avatar.png",
        mime="image/png",
    )