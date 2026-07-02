import threading
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Import all handlers
from config import BOT_TOKEN, OWNER_ID
from database import load_users, load_approved, load_upi_keywords
from upi_handler import handle_qr_request
from deal_handler import add_deal_command, deal_status_command, complete_deal_command
from game_handler import dice_command
from admin_handler import owner_panel, button_callback
from approve_handler import approve_user, remove_approval, ban_command, unban_command
from qr_handler import set_qr_message, qr_history_command, upi_keyword_commands, remove_upi_keyword, list_upi_keywords

# ============ FLASK ============
flask_app = Flask(__name__)

@flask_app.route('/')
@flask_app.route('/health')
def health():
    return "Premium Bot is running!", 200

def run_flask():
    import os
    port = int(os.environ.get('PORT', 5000))
    flask_app.run(host='0.0.0.0', port=port)

# ============ START COMMAND ============
async def start_command(update, context):
    from database import is_banned, is_approved, register_user, load_upi_keywords
    from utils import format_with_emojis
    
    user = update.effective_user
    user_id = user.id
    username = user.username or "NoUsername"
    
    if is_banned(user_id):
        await update.message.reply_text("❌ You are banned!")
        return
    
    register_user(user_id, username, user.first_name)
    
    if not is_approved(user_id):
        await update.message.reply_text(
            "❌ You are not approved!\n"
            "Contact owner to get approval."
        )
        return
    
    upis = load_upi_keywords()
    keyword_list = '\n'.join([f"🔹 {data['keyword']} - {data['upi_id']}" for data in upis.values()]) if upis else "No keywords added yet"
    
    msg = f"""
✨ <b>WELCOME TO PREMIUM BOT!</b>
━━━━━━━━━━━━━━━━━━
👋 Hey @{username}!

🔹 <b>Payments:</b>
<code>KEYWORD AMOUNT</code> - Generate QR
Example: <code>Bluddyxpay 500</code>

🔹 <b>Commands:</b>
🎲 /dice - Play dice game
📊 /dealstatus - Deal status
👤 /profile - Your profile

━━━━━━━━━━━━━━━━━━
💳 <b>UPI Keywords:</b>
{keyword_list}
━━━━━━━━━━━━━━━━━━
    """
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

async def profile_command(update, context):
    from database import is_banned, is_approved, get_user
    from utils import format_with_emojis
    
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "NoUsername"
    
    if is_banned(user_id) or not is_approved(user_id):
        await update.message.reply_text("❌ Not authorized!")
        return
    
    data = get_user(user_id)
    msg = f"""
👤 <b>PROFILE</b>
━━━━━━━━━━━━━━━━━━
📛 @{username}
🆔 {user_id}
📅 Joined: {data.get('joined', 'N/A')}
🏆 Wins: {data.get('wins', 0)}
💰 Earnings: ₹{data.get('earnings', 0)}
📱 QR Used: {data.get('qr_used', 0)}
━━━━━━━━━━━━━━━━━━
    """
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

async def help_command(update, context):
    from database import is_banned, is_approved, load_upi_keywords
    from utils import format_with_emojis
    
    user_id = update.effective_user.id
    
    if is_banned(user_id) or not is_approved(user_id):
        await update.message.reply_text("❌ Not authorized!")
        return
    
    upis = load_upi_keywords()
    keyword_list = '\n'.join([f"🔹 {data['keyword']}" for data in upis.values()]) if upis else "No keywords"
    
    msg = f"""
❓ <b>HELP MENU</b>
━━━━━━━━━━━━━━━━━━

💳 <b>PAYMENTS:</b>
<code>KEYWORD AMOUNT</code> - Get QR
Example: <code>Bluddyxpay 500</code>

🎮 <b>GAMES:</b>
/dice - Play dice game

📊 <b>INFO:</b>
/dealstatus - Deal status
/profile - Your profile

👑 <b>ADMIN:</b>
/addupi KEYWORD UPI_ID - Add
/removeupi KEYWORD - Remove
/listupi - List all
/setqrmessage TEXT - Set message
/qrhistory - View QR history
/adddeal STATUS BUYER SELLER AMOUNT
/completed @buyer @seller

━━━━━━━━━━━━━━━━━━
🔑 <b>Available Keywords:</b>
{keyword_list}
━━━━━━━━━━━━━━━━━━
    """
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

async def time_command(update, context):
    from database import load_settings
    from utils import format_with_emojis
    from datetime import datetime
    
    now = datetime.now()
    settings = load_settings()
    
    msg = f"""
🕐 <b>CURRENT TIME</b>
━━━━━━━━━━━━━━━━━━
📅 {now.strftime('%Y-%m-%d')}
🕐 {now.strftime('%H:%M:%S')}
🔒 Lock: {settings.get('lock_time', '00:00')}
🔓 Unlock: {settings.get('unlock_time', '19:00')}
🔐 Status: {'🔒 LOCKED' if settings.get('group_locked', False) else '🔓 UNLOCKED'}
━━━━━━━━━━━━━━━━━━
    """
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

# ============ MAIN ============
def main():
    # Start Flask
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Create bot
    application = Application.builder().token(BOT_TOKEN).build()
    
    # User commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CommandHandler("dice", dice_command))
    application.add_handler(CommandHandler("time", time_command))
    
    # Admin commands
    application.add_handler(CommandHandler("dealstatus", deal_status_command))
    application.add_handler(CommandHandler("adddeal", add_deal_command))
    application.add_handler(CommandHandler("completed", complete_deal_command))
    
    # Owner commands
    application.add_handler(CommandHandler("owner", owner_panel))
    application.add_handler(CommandHandler("approve", approve_user))
    application.add_handler(CommandHandler("remove", remove_approval))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("addupi", upi_keyword_commands))
    application.add_handler(CommandHandler("removeupi", remove_upi_keyword))
    application.add_handler(CommandHandler("listupi", list_upi_keywords))
    application.add_handler(CommandHandler("setqrmessage", set_qr_message))
    application.add_handler(CommandHandler("qrhistory", qr_history_command))
    
    # QR request handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_qr_request))
    
    # Callback handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("=" * 60)
    print("✨ PREMIUM BOT WITH SEPARATE FILES STARTED")
    print(f"👑 Owner: {OWNER_ID}")
    print(f"👥 Users: {len(load_users())}")
    print(f"✅ Approved: {len(load_approved())}")
    print(f"🔑 UPI Keywords: {len(load_upi_keywords())}")
    print("📁 All files separated for easy management!")
    print("=" * 60)
    
    application.run_polling()

if __name__ == "__main__":
    main()