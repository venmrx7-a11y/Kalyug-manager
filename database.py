import json
import os
from datetime import datetime
from config import *

# ============ GENERIC FUNCTIONS ============

def load_json(filename, default=None):
    """Load JSON file"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return default or {}
    return default or {}

def save_json(filename, data):
    """Save JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# ============ USER FUNCTIONS ============

def load_users():
    return load_json(USERS_FILE, {})

def save_users(users):
    save_json(USERS_FILE, users)

def register_user(user_id, username, first_name):
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {
            "id": user_id,
            "username": username,
            "name": first_name,
            "joined": str(datetime.now()),
            "wins": 0,
            "earnings": 0,
            "qr_used": 0
        }
        save_users(users)
        return True
    return False

def get_user(user_id):
    users = load_users()
    return users.get(str(user_id), {})

def update_user(user_id, key, value):
    users = load_users()
    if str(user_id) in users:
        users[str(user_id)][key] = value
        save_users(users)
        return True
    return False

# ============ BANNED FUNCTIONS ============

def load_banned():
    return load_json(BANNED_FILE, [])

def save_banned(banned):
    save_json(BANNED_FILE, banned)

def is_banned(user_id):
    return str(user_id) in load_banned()

def ban_user(user_id):
    banned = load_banned()
    if str(user_id) not in banned:
        banned.append(str(user_id))
        save_banned(banned)
        return True
    return False

def unban_user(user_id):
    banned = load_banned()
    if str(user_id) in banned:
        banned.remove(str(user_id))
        save_banned(banned)
        return True
    return False

# ============ APPROVED FUNCTIONS ============

def load_approved():
    return load_json(APPROVED_FILE, [])

def save_approved(approved):
    save_json(APPROVED_FILE, approved)

def is_approved(user_id):
    return str(user_id) in load_approved() or str(user_id) == str(OWNER_ID)

def approve_user(user_id):
    approved = load_approved()
    if str(user_id) not in approved:
        approved.append(str(user_id))
        save_approved(approved)
        return True
    return False

def remove_approval(user_id):
    approved = load_approved()
    if str(user_id) in approved:
        approved.remove(str(user_id))
        save_approved(approved)
        return True
    return False

# ============ DEAL FUNCTIONS ============

def load_deals():
    return load_json(DEALS_FILE, {})

def save_deals(deals):
    save_json(DEALS_FILE, deals)

def add_deal(buyer, seller, amount, status):
    deals = load_deals()
    deal_id = f"DEAL_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    deals[deal_id] = {
        "buyer": buyer,
        "seller": seller,
        "amount": amount,
        "status": status,
        "date": str(datetime.now())
    }
    save_deals(deals)
    return deal_id

def get_deal_stats():
    deals = load_deals()
    total = len(deals)
    hold = sum(1 for d in deals.values() if d.get('status') == 'HOLD')
    complete = sum(1 for d in deals.values() if d.get('status') == 'COMPLETE')
    amount = sum(int(d.get('amount', 0)) for d in deals.values())
    return total, hold, complete, amount

# ============ UPI KEYWORD FUNCTIONS ============

def load_upi_keywords():
    return load_json(UPI_FILE, {})

def save_upi_keywords(upis):
    save_json(UPI_FILE, upis)

def add_upi_keyword(keyword, upi_id, added_by):
    upis = load_upi_keywords()
    
    # Check limit
    if len(upis) >= 20:
        return False, "Maximum 20 keywords allowed!"
    
    # Check duplicate
    for data in upis.values():
        if data.get('keyword', '').lower() == keyword.lower():
            return False, f"Keyword '{keyword}' already exists!"
    
    key = f"UPI_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    upis[key] = {
        "keyword": keyword,
        "upi_id": upi_id,
        "added_by": added_by,
        "added_date": str(datetime.now()),
        "total_used": 0
    }
    save_upi_keywords(upis)
    return True, "Keyword added successfully!"

def remove_upi_keyword(keyword):
    upis = load_upi_keywords()
    found = False
    for key, data in list(upis.items()):
        if data.get('keyword', '').lower() == keyword.lower():
            del upis[key]
            found = True
            break
    if found:
        save_upi_keywords(upis)
        return True
    return False

def find_upi_keyword(keyword):
    upis = load_upi_keywords()
    for key, data in upis.items():
        if data.get('keyword', '').lower() == keyword.lower():
            return data
    return None

def increment_upi_usage(keyword):
    upis = load_upi_keywords()
    for key, data in upis.items():
        if data.get('keyword', '').lower() == keyword.lower():
            upis[key]['total_used'] = upis[key].get('total_used', 0) + 1
            save_upi_keywords(upis)
            return True
    return False

# ============ SETTINGS FUNCTIONS ============

def load_settings():
    return load_json(SETTINGS_FILE, DEFAULT_SETTINGS)

def save_settings(settings):
    save_json(SETTINGS_FILE, settings)

def update_setting(key, value):
    settings = load_settings()
    settings[key] = value
    save_settings(settings)
    return settings

# ============ QR HISTORY FUNCTIONS ============

def load_qr_history():
    return load_json(QR_HISTORY_FILE, {})

def save_qr_history(qrs):
    save_json(QR_HISTORY_FILE, qrs)

def add_qr_history(user_id, username, keyword, upi_id, amount):
    qrs = load_qr_history()
    qr_id = f"QR_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    qrs[qr_id] = {
        "user_id": str(user_id),
        "username": username,
        "keyword": keyword,
        "upi_id": upi_id,
        "amount": amount,
        "date": str(datetime.now())
    }
    save_qr_history(qrs)
    return qr_id