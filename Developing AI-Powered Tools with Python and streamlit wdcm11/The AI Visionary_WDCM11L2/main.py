import base64
from io import BytesIO

import streamlit as st
from PIL import Image
from groq import Groq
import config

st.set_page_config(page_title="AI Visionary", page_icon="🕵️", layout="centered")

STYLES = {
    "Normal": (
        "Look at this image carefully and write a clear, detailed report. "
        "Describe the scene, objects, and what seems to be happening."
    ),
    "Funny": (
        "Look at this image carefully and write a funny image report. "
        "Mention objects, details, and make the report playful and humorous, "
        "but still describe the image correctly."
    ),
    "Detective": (
        "Look at this image like a detective. "
        "Write an investigation-style report with clues, observations, and smart deductions."
    ),
    "Dramatic": (
        "Look at this image and describe it in a dramatic, cinematic way. "
        "Make the report vivid, exciting, and expressive."
    ),
    "Story Mode": (
        "Look at this image and write a short story-like scene description. "
        "Describe the setting, objects, and mood in a creative way."
    ),
}

client = Groq(api_key=config.GROQ_API_KEY)


st.title("🕵️ The AI Visionary")
st.write("Upload an image and let AI create a fun report about it!")
st.markdown(
    "Choose an image, pick a report style, and click **Analyze Image**. "
    "The AI will study the image and write a detailed report."
)


def analyze_image(uploaded_file, style):
    encoded = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
    response = client.chat.completions.create(
        model=config.GROQ_VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": STYLES.get(style, STYLES["Normal"])},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{uploaded_file.type};base64,{encoded}"
                        },
                    },
                ],
            }
        ],
        temperature=0.8,
        max_completion_tokens=500,
    )
    return response.choices[0].message.content


uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg", "webp"],
)


report_style = st.selectbox("Choose report style", list(STYLES))


if uploaded_file:
    st.image(
        Image.open(BytesIO(uploaded_file.getvalue())),
        caption="Uploaded Image",
        use_container_width=True,
    )

if st.button("🔍 Analyze Image"):
    if not config.GROQ_API_KEY:
        st.error("Groq API key is missing. Please add it to your .env file.")
    elif not uploaded_file:
        st.warning("Please upload an image first.")
    else:
        with st.spinner("The AI is studying your image..."):
            try:
                st.success("Report ready!")
                st.subheader("📝 AI Report")
                st.write(analyze_image(uploaded_file, report_style))
            except Exception as error:
                st.error(f"Something went wrong: {error}")