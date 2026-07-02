from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import *
from utils import format_with_emojis
from config import OWNER_ID

async def owner_panel(update, context):
    """Owner panel - /owner"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only!")
        return
    
    users = load_users()
    approved = load_approved()
    banned = load_banned()
    upis = load_upi_keywords()
    qrs = load_qr_history()
    deals = load_deals()
    settings = load_settings()
    
    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data="owner_stats"),
         InlineKeyboardButton("👥 Users", callback_data="owner_users")],
        [InlineKeyboardButton("🔑 UPI Keywords", callback_data="owner_upi"),
         InlineKeyboardButton("📱 QR History", callback_data="owner_qr")],
        [InlineKeyboardButton("📝 Deals", callback_data="owner_deals"),
         InlineKeyboardButton("🎮 Games", callback_data="owner_games")],
        [InlineKeyboardButton("🔒 Lock", callback_data="owner_lock"),
         InlineKeyboardButton("🔓 Unlock", callback_data="owner_unlock")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="owner_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg = f"""
👑 <b>OWNER PANEL</b>
━━━━━━━━━━━━━━━━━━
🔹 Users: {len(users)}
✅ Approved: {len(approved)}
🚫 Banned: {len(banned)}
🔑 UPI Keywords: {len(upis)}
📱 QR Generated: {len(qrs)}
📋 Deals: {len(deals)}
🔐 Status: {'🔒 LOCKED' if settings.get('group_locked', False) else '🔓 UNLOCKED'}
━━━━━━━━━━━━━━━━━━
    """
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML", reply_markup=reply_markup)

async def button_callback(update, context):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "owner_stats":
        users = load_users()
        approved = load_approved()
        banned = load_banned()
        upis = load_upi_keywords()
        qrs = load_qr_history()
        deals = load_deals()
        total, hold, complete, amount = get_deal_stats()
        
        msg = f"""
📊 <b>BOT STATISTICS</b>
━━━━━━━━━━━━━━━━━━
👥 Users: {len(users)}
✅ Approved: {len(approved)}
🚫 Banned: {len(banned)}
🔑 UPI Keywords: {len(upis)}
📱 QR Generated: {len(qrs)}
📋 Deals: {len(deals)}
⏳ HOLD: {hold}
✅ Complete: {complete}
💰 Total Amount: ₹{amount}
━━━━━━━━━━━━━━━━━━
        """
        await query.edit_message_text(format_with_emojis(msg), parse_mode="HTML")
    
    elif data == "owner_users":
        users = load_users()
        approved = load_approved()
        
        msg = "👥 <b>USERS</b>\n━━━━━━━━━━━━━━━━━━\n"
        for uid, data in list(users.items())[-20:]:
            status = "✅" if uid in approved else "❌"
            msg += f"{status} @{data.get('username', 'N/A')}\n"
        msg += "━━━━━━━━━━━━━━━━━━"
        await query.edit_message_text(format_with_emojis(msg), parse_mode="HTML")
    
    elif data == "owner_upi":
        keyboard = [
            [InlineKeyboardButton("📋 List UPIs", callback_data="upi_list")],
            [InlineKeyboardButton("🔙 Back", callback_data="owner_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        upis = load_upi_keywords()
        msg = f"""
🔑 <b>UPI KEYWORD MANAGEMENT</b>
━━━━━━━━━━━━━━━━━━
Total Keywords: {len(upis)}/20
━━━━━━━━━━━━━━━━━━
Commands:
/addupi KEYWORD UPI_ID - Add
/removeupi KEYWORD - Remove
/listupi - List all
/setqrmessage TEXT - Set message
━━━━━━━━━━━━━━━━━━
        """
        await query.edit_message_text(format_with_emojis(msg), parse_mode="HTML", reply_markup=reply_markup)
    
    elif data == "upi_list":
        upis = load_upi_keywords()
        if not upis:
            await query.edit_message_text("📭 No UPI keywords added!")
            return
        
        msg = "🔑 <b>UPI KEYWORDS</b>\n━━━━━━━━━━━━━━━━━━\n\n"
        for key, data in upis.items():
            msg += f"🔹 <b>{data['keyword']}</b>\n"
            msg += f"💳 <code>{data['upi_id']}</code>\n"
            msg += f"📊 Used: {data.get('total_used', 0)} times\n"
            msg += "━━━━━━━━━━━━━━━━━━\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="owner_upi")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(format_with_emojis(msg), parse_mode="HTML", reply_markup=reply_markup)
    
    elif data == "owner_qr":
        qrs = load_qr_history()
        if not qrs:
            await query.edit_message_text("📭 No QR generated yet!")
            return
        
        msg = "📱 <b>QR HISTORY</b>\n━━━━━━━━━━━━━━━━━━\n\n"
        for qr_id, data in list(qrs.items())[-10:]:
            msg += f"🆔 {qr_id}\n"
            msg += f"👤 @{data.get('username', 'N/A')}\n"
            msg += f"💰 ₹{data.get('amount', 0)}\n"
            msg += f"📅 {data.get('date', 'N/A')}\n"
            msg += "━━━━━━━━━━━━━━━━━━\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="owner_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(format_with_emojis(msg), parse_mode="HTML", reply_markup=reply_markup)
    
    elif data == "owner_lock":
        settings = load_settings()
        settings['group_locked'] = True
        save_settings(settings)
        await query.edit_message_text("🔒 Group locked!")
    
    elif data == "owner_unlock":
        settings = load_settings()
        settings['group_locked'] = False
        save_settings(settings)
        await query.edit_message_text("🔓 Group unlocked!")
    
    elif data == "owner_back":
        await owner_panel(update, context)