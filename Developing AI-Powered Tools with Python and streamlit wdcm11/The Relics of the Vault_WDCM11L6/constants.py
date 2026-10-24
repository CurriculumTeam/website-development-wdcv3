# ── PROVIDED — do not edit ────────────────────────────────────────

APP_TITLE               = "AI Mystery Vault — Lesson 6"
MAX_TRUST               = 100
TRUST_TO_OPEN           = 35
TRUST_TO_ENTER          = 65
RELICS_NEEDED_FOR_FINAL = 2
TOTAL_CHAMBERS          = 2
BANISH_THRESHOLD        = 0
STREAK_BONUS_AT         = 2
EVENT_CHANCE            = 0.25

BG       = "#071018"
CARD     = "#101827"
ACCENT   = "#7c5cff"
ACCENT_2 = "#27c2ff"
TEXT     = "#e5ecf4"
MUTED    = "#95a2b8"
SUCCESS  = "#18b47b"
WARNING  = "#d9a441"
DANGER   = "#d85757"

RUDE_HINTS    = ["stupid","move","idiot","boring","shut up","useless","hurry","dumb","fool"]
HELPFUL_HINTS = ["please","sorry","thank you","help","respect","honor","understand","greet","bow","humble"]

CHAMBER_NAMES = [
    "Hall of Fractured Hours", "Crystal Echo Vault", "Shadow Archive",
    "Chamber of Silent Sparks", "Moonglass Reliquary", "The Whisper Engine",
]

RIDDLES = [
    {"question":"I have keys but no locks. I have space but no room. You can enter but can't go inside. What am I?","answer":"keyboard","hint":"You use me to type."},
    {"question":"The more you take, the more you leave behind. What am I?","answer":"footsteps","hint":"Think about walking."},
    {"question":"I speak without a mouth and hear without ears. I come alive with wind. What am I?","answer":"echo","hint":"Sound returns to you in caves."},
    {"question":"The more you feed me, the more I grow. Give me water and I die. What am I?","answer":"fire","hint":"I light the forge and warm the vault."},
    {"question":"What has hands but cannot clap?","answer":"clock","hint":"It tells you something every second."},
    {"question":"I am always in front of you but cannot be seen. What am I?","answer":"future","hint":"Time holds the answer."},
    {"question":"I can be cracked, made, told, and played. What am I?","answer":"joke","hint":"It makes people laugh."},
]

RANDOM_EVENTS = [
    {"id":"trap",           "title":"⚠️ Vault Trap!",      "description":"A hidden pressure plate triggers — stone spikes graze your arm!",                     "trust_delta":-8,  "color":"danger"},
    {"id":"vision",         "title":"🔮 Ancient Vision",   "description":"A spectral memory floods your mind — the vault shows you a secret path.",              "trust_delta":12,  "color":"success"},
    {"id":"sentinel_rage",  "title":"😡 Sentinel Rage!",   "description":"The Sentinel senses doubt in your heart. Its eyes burn red.",                          "trust_delta":-10, "color":"danger"},
    {"id":"secret_passage", "title":"🗝️ Secret Passage!", "description":"A hidden door slides open — ancient runes glow in approval.",                          "trust_delta":15,  "color":"success"},
    {"id":"rune_surge",     "title":"✨ Rune Surge!",       "description":"The vault walls pulse with energy — your presence resonates with the ancient magic.",  "trust_delta":10,  "color":"success"},
    {"id":"shadow_whisper", "title":"👁️ Shadow Whisper",  "description":"A dark presence brushes past you. Something watches from the walls.",                   "trust_delta":-5,  "color":"warn"},
    {"id":"crystal_gift",   "title":"💎 Crystal Gift",     "description":"A floating crystal drifts toward you and dissolves into your hands — warm and trusting.","trust_delta":18, "color":"success"},
    {"id":"time_rift",      "title":"⏳ Time Rift",         "description":"Reality flickers. You glimpse yourself failing — and choose differently.",              "trust_delta":8,   "color":"warn"},
]

ACHIEVEMENTS = [
    {"id":"first_words",  "title":"First Words",  "desc":"You spoke to the Sentinel.", "icon":"💬"},
    {"id":"riddle_master","title":"Riddle Master","desc":"You solved the logic lock.",  "icon":"🧩"},
    {"id":"trusted",      "title":"Trusted",      "desc":"Trust reached 50.",           "icon":"🤝"},
    {"id":"vault_open",   "title":"Vault Open",   "desc":"You entered the vault.",      "icon":"🚪"},
    {"id":"explorer",     "title":"Explorer",     "desc":"First chamber discovered.",   "icon":"🗺️"},
    {"id":"relic_hunter", "title":"Relic Hunter", "desc":"First relic forged.",         "icon":"💎"},
    {"id":"streak_3",     "title":"On Fire",      "desc":"3 good actions in a row!",    "icon":"🔥"},
    {"id":"survivor",     "title":"Survivor",     "desc":"Survived a vault trap.",      "icon":"🛡️"},
    {"id":"legend",       "title":"Legend",       "desc":"Final vault unlocked.",       "icon":"👑"},
]

RELIC_FALLBACKS = [
    {"name":"Chrono Glass Shard",   "rarity":"Rare",      "lore":"A splinter of frozen time taken from a clock that forgot how to move.",  "power":"Reveals hidden patterns in nearby walls and relics.",          "art_prompt":"glowing time crystal shard, ancient fantasy relic, dark velvet background, magical cinematic lighting"},
    {"name":"Whisper Coil",         "rarity":"Epic",      "lore":"A silver coil that remembers every secret ever spoken near the vault.",   "power":"Lets the bearer hear faint hints from the next chamber.",     "art_prompt":"silver mystical coil relic, arcane fantasy object, glowing mist, dramatic shadows"},
    {"name":"Ember Key of Silence", "rarity":"Legendary", "lore":"Forged in a room where fire burned without sound.",                       "power":"Can awaken locked mechanisms without making a single sound.", "art_prompt":"ancient ember key relic, glowing runes, dark fantasy vault, rich detail, cinematic light"},
]

REPEAT_REPLIES = [
    "You've said that already. Word for word. Do you think I don't notice? Say something new — or don't say anything at all.",
    "Again? That exact phrase? I've been guarding this vault for a thousand years. I remember every word spoken here. Try harder.",
    "I heard you the first time. And the second. Repeating yourself won't open this gate — it just tells me you've run out of ideas.",
    "Same words again. The gate doesn't respond to echoes, traveler. Speak something real.",
]

SENTINEL_STYLES = {
    "Suspicious": "You are deeply suspicious and cold. Speak in short, sharp sentences. You test every word.",
    "Watching":   "You are cautious but paying attention. Speak with quiet intensity — measured, a little poetic.",
    "Curious":    "You're genuinely intrigued. Ask questions back. Be mysterious but warmer.",
    "Accepting":  "You are ancient, wise, and almost warm. Speak in flowing, rich sentences. You're a guide now.",
}

SENTINEL_FEEL = [
    "You barely acknowledge them.",
    "You're starting to notice them.",
    "You're genuinely interested in them.",
    "You respect them. They've earned it.",
]

PHASE_COLORS = {
    "gate":    ("#7c5cff","#27c2ff","rgba(124,92,255,.55)","rgba(39,194,255,.55)","0a0520","1a0a40","2d1060"),
    "vault":   ("#27c2ff","#7c5cff","rgba(39,194,255,.55)","rgba(124,92,255,.55)","020810","041428","061e3a"),
    "forge":   ("#ff6414","#ff9a14","rgba(255,100,20,.65)","rgba(255,154,20,.55)","120400","220800","5a1000"),
    "endgame": ("#f2c14f","#fff0a0","rgba(242,193,79,.65)","rgba(255,240,160,.55)","0e0a00","1c1400","4a3600"),
}

WEATHER_MAP = {"gate":"snow","vault":"rain","forge":"sunny","endgame":"clouds"}

BG_POOLS = {
    "gate":    ["https://images.unsplash.com/photo-1448375240586-882707db888b?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1504701954957-2010ec3bcec1?w=1280&q=80&fit=crop&h=480"],
    "vault":   ["https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1504198266287-1659872e6590?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1551632811-561732d1e306?w=1280&q=80&fit=crop&h=480"],
    "forge":   ["https://images.unsplash.com/photo-1567095761054-7a02e69e5c43?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1610296669228-602fa827fc1f?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1536566482680-fca31930a0bd?w=1280&q=80&fit=crop&h=480"],
    "endgame": ["https://images.unsplash.com/photo-1548013146-72479768bada?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1519817650390-64a93db51149?w=1280&q=80&fit=crop&h=480","https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1280&q=80&fit=crop&h=480"],
}

SPRITE_TRAVELER_BASE = (
    "https://api.dicebear.com/9.x/adventurer/svg"
    "?backgroundColor=0a0f1e,0d1b2a,1a1040,0f0a2e&backgroundType=gradientLinear"
    "&radius=50&size=128&accessories=glasses,sunglasses,wayfarers&accessoriesProbability=60"
    "&earrings=variant01,variant02,variant03&earringsProbability=50"
    "&features=birthmark,blush,freckles&featuresProbability=70"
)
SPRITE_SENTINEL_URL = (
    "https://api.dicebear.com/9.x/bottts/svg?seed=vault-sentinel-IX"
    "&backgroundColor=1a0a2e,0d0820,2a0a40,180520&backgroundType=gradientLinear"
    "&radius=50&size=128"
    "&eyes=bulging,dizzy,eva,frame1,frame2,glow,happy,hearts,robocop,round,roundFrame01,roundFrame02,sensor,shade01"
    "&mouth=bite,diagram,grill01,grill02,grill03,square01,square02"
)
