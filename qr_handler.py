from database import *
from utils import format_with_emojis
from config import OWNER_ID

async def set_qr_message(update, context):
    """Set QR message - /setqrmessage TEXT"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only!")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text("📝 Usage: `/setqrmessage your message here`", parse_mode="Markdown")
        return
    
    message = " ".join(context.args)
    settings = load_settings()
    settings['qr_message'] = message
    save_settings(settings)
    await update.message.reply_text("✅ QR message updated!")

async def qr_history_command(update, context):
    """View QR history - /qrhistory"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only!")
        return
    
    qrs = load_qr_history()
    if not qrs:
        await update.message.reply_text("📭 No QR generated yet!")
        return
    
    msg = "📱 <b>QR HISTORY</b>\n━━━━━━━━━━━━━━━━━━\n\n"
    for qr_id, data in list(qrs.items())[-20:]:
        msg += f"🆔 {qr_id}\n"
        msg += f"👤 @{data.get('username', 'N/A')}\n"
        msg += f"🔑 {data.get('keyword', 'N/A')}\n"
        msg += f"💰 ₹{data.get('amount', 0)}\n"
        msg += f"📅 {data.get('date', 'N/A')}\n"
        msg += "━━━━━━━━━━━━━━━━━━\n"
    
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

async def upi_keyword_commands(update, context):
    """Add UPI keyword - /addupi KEYWORD UPI_ID"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only!")
        return
    
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "📝 Usage: `/addupi KEYWORD UPI_ID`\n"
            "Example: `/addupi Bluddyxpay example@upi`\n\n"
            "📌 User will type: `Bluddyxpay 500` to get QR",
            parse_mode="Markdown"
        )
        return
    
    keyword = args[0]
    upi_id = args[1]
    
    success, message = add_upi_keyword(keyword, upi_id, str(update.effective_user.id))
    
    if success:
        msg = f"""
✅ <b>UPI KEYWORD ADDED!</b>
━━━━━━━━━━━━━━━━━━
🔑 Keyword: <b>{keyword}</b>
💳 UPI: <b>{upi_id}</b>
━━━━━━━━━━━━━━━━━━
📌 User command: <code>{keyword} AMOUNT</code>
Example: <code>{keyword} 500</code>
━━━━━━━━━━━━━━━━━━
        """
        await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")
    else:
        await update.message.reply_text(f"❌ {message}")

async def remove_upi_keyword(update, context):
    """Remove UPI keyword - /removeupi KEYWORD"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only!")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text("📝 Usage: `/removeupi KEYWORD`", parse_mode="Markdown")
        return
    
    keyword = context.args[0]
    if remove_upi_keyword(keyword):
        await update.message.reply_text(f"✅ Keyword '{keyword}' removed!")
    else:
        await update.message.reply_text(f"❌ Keyword '{keyword}' not found!")

async def list_upi_keywords(update, context):
    """List all UPI keywords - /listupi"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only!")
        return
    
    upis = load_upi_keywords()
    if not upis:
        await update.message.reply_text("📭 No UPI keywords added!")
        return
    
    msg = "🔑 <b>UPI KEYWORDS</b>\n━━━━━━━━━━━━━━━━━━\n\n"
    for key, data in upis.items():
        msg += f"🔹 <b>{data['keyword']}</b>\n"
        msg += f"💳 <code>{data['upi_id']}</code>\n"
        msg += f"📊 Used: {data.get('total_used', 0)} times\n"
        msg += "━━━━━━━━━━━━━━━━━━\n"
    
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")