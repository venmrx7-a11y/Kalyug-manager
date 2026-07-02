import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN', "8999246230:AAG23Gx0QyCMHOmvMMs00TFjUBW8AO-OZxw")
OWNER_ID = int(os.environ.get('OWNER_ID',7977493987))
ADMIN_IDS = [OWNER_ID]

# Files
USERS_FILE = "users.json"
BANNED_FILE = "banned.json"
APPROVED_FILE = "approved.json"
DEALS_FILE = "deals.json"
UPI_FILE = "upi_keywords.json"
SETTINGS_FILE = "settings.json"
QR_HISTORY_FILE = "qr_history.json"

# Default Settings
DEFAULT_SETTINGS = {
    "lock_time": "00:00",
    "unlock_time": "19:00",
    "group_locked": False,
    "min_win": 4,
    "max_win": 10,
    "qr_message": "💳 Payment Amount: ₹{amount}\n\n📤 Send screenshot after payment\n\n👤 Reg-@ERRORLIVE\n\n⚠️ Don't pay in any DM!"
}

# Max UPI Keywords allowed
MAX_UPI_KEYWORDS = 20
