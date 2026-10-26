from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "keras_model.h5"
LABELS_PATH = BASE_DIR / "models" / "labels.txt"

APP_TITLE = "Magic Gesture Recognizer"
APP_ICON = "🖐️"
CAMERA_HELP = "Show one clear hand sign, then click Take Photo."
