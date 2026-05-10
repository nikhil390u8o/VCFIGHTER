# ══════════════════════════════════════════════════════════════
#  VCFIGHTER — Config (Direct Variables — Paste Your Values)
# ══════════════════════════════════════════════════════════════

# ── REQUIRED — Telegram ───────────────────────────────────────
API_ID    = 0                   # apna API ID yahan likho (int)
API_HASH  = ""                  # apna API HASH yahan likho
BOT_TOKEN = ""                  # apna BOT TOKEN yahan likho

# ── REQUIRED — Owner ─────────────────────────────────────────
OWNER_ID  = 0                   # apna Telegram user ID yahan likho (int)

# ── OPTIONAL — Sudo Users ────────────────────────────────────
SUDO_USERS: list[int] = []      # e.g. [123456, 789012]

# ── OPTIONAL — Log Channel ───────────────────────────────────
LOG_CHANNEL = 0                 # log channel ID (int), 0 = off

# ── OPTIONAL — Startup String Sessions ───────────────────────
STARTUP_SESSIONS: list[str] = []  # e.g. ["session1", "session2"]

# ── OPTIONAL — PyTgCalls Defaults ────────────────────────────
DEFAULT_STREAM_TYPE       = "audio"   # "audio" | "video"
DEFAULT_QUALITY           = "medium"  # "low" | "medium" | "high"
DEFAULT_NOISE_SUPPRESSION = False

# ── OPTIONAL — FFmpeg Defaults ───────────────────────────────
DEFAULT_VOLUME     = 1.0       # 1.0 = 100%
DEFAULT_BASS       = 0         # 0 to 40
DEFAULT_PITCH      = "normal"  # "normal" | "demon" | "chipmunk"
DEFAULT_ECHO       = False
DEFAULT_COMPRESSOR = False
DEFAULT_LIMITER    = False

# ── OPTIONAL — VC Behaviour ──────────────────────────────────
DEFAULT_MODE      = "dm"          # "dm" | "auto"
RECORDINGS_DIR    = "recordings"
MAX_RECORDING_AGE = 3600          # seconds

# ── OPTIONAL — Branding ──────────────────────────────────────
BOT_NAME    = "VCFighter"
BOT_VERSION = "2.0"
SUPPORT_URL = "https://t.me/Zcziiy"
SOURCE_URL  = "https://github.com/YOURNAME/VCFIGHTER"

# ── OPTIONAL — Support Links ─────────────────────────────────
SUPPORT_CHAT    = "https://t.me/Zcziiy"
SUPPORT_CHANNEL = "https://t.me/Zcziiy"

# ── OPTIONAL — Bot Pictures ──────────────────────────────────
VC_PICS: list[str] = [
    "https://files.catbox.moe/eje8y8.jpeg",
    "https://files.catbox.moe/ey2jzp.jpeg",
    "https://files.catbox.moe/ah5y0f.jpeg",
    "https://files.catbox.moe/we4yju.jpeg",
]

# ── OPTIONAL — Start Animation ───────────────────────────────
START_FIRE_EFFECT = True
FIRE_FRAME_DELAY  = 0.4
DING_DONG_DELETE  = True

# ── DB (unused — MongoDB hata diya) ──────────────────────────
MONGO_URI = ""
DB_NAME   = "vcfighter"

# ══════════════════════════════════════════════════════════════
#  CONSTANTS (mat chhedo)
# ══════════════════════════════════════════════════════════════

AUDIO_QUALITIES = {
    "low":    {"bitrate": 32000,  "channels": 1},
    "medium": {"bitrate": 48000,  "channels": 2},
    "high":   {"bitrate": 96000,  "channels": 2},
}

PITCH_RATES = {
    "normal":   1.0,
    "demon":    0.7,
    "chipmunk": 1.6,
}

BASS_LEVELS = {
    0:  "Normal",
    15: "Heavy",
    30: "Earthquake",
    40: "💀 MAX",
}
