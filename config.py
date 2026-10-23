import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID_STR = os.getenv("OWNER_ID", "0")
GUILD_ID_STR = os.getenv("GUILD_ID")
AUDIT_LOG_CHANNEL_ID_STR = os.getenv("AUDIT_LOG_CHANNEL_ID")

try:
    OWNER_ID = int(OWNER_ID_STR)
except ValueError:
    OWNER_ID = 0

try:
    GUILD_ID = int(GUILD_ID_STR) if GUILD_ID_STR else None
except ValueError:
    GUILD_ID = None

try:
    AUDIT_LOG_CHANNEL_ID = int(AUDIT_LOG_CHANNEL_ID_STR) if AUDIT_LOG_CHANNEL_ID_STR else None
except ValueError:
    AUDIT_LOG_CHANNEL_ID = None

EMBED_COLOR = 0x222222  # Polished dark graphite/black
ACCENT_COLOR = 0xC0C0C0 # Silver
