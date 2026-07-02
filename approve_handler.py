from database import *
from utils import format_with_emojis
from config import OWNER_ID

async def approve_user(update, context):
    """Approve user - /approve @username"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only!")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text("📝 Usage: `/approve @username`", parse_mode="Markdown")
        return
    
    username = context.args[0].replace('@', '')
    users = load_users()
    
    user_id = None
    for uid, data in users.items():
        if data.get('username') == username:
            user_id = uid
            break
    
    if not user_id:
        await update.message.reply_text(f"❌ User @{username} not found!")
        return
    
    if approve_user(user_id):
        await update.message.reply_text(f"✅ User @{username} approved!")
    else:
        await update.message.reply_text(f"⚠️ User @{username} already approved!")

async def remove_approval(update, context):
    """Remove approval - /remove @username"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only!")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text("📝 Usage: `/remove @username`", parse_mode="Markdown")
        return
    
    username = context.args[0].replace('@', '')
    users = load_users()
    
    user_id = None
    for uid, data in users.items():
        if data.get('username') == username:
            user_id = uid
            break
    
    if not user_id:
        await update.message.reply_text(f"❌ User @{username} not found!")
        return
    
    if remove_approval(user_id):
        await update.message.reply_text(f"✅ Approval removed for @{username}!")
    else:
        await update.message.reply_text(f"⚠️ User @{username} is not approved!")

async def ban_command(update, context):
    """Ban user - /ban @username"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only!")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text("📝 Usage: `/ban @username`", parse_mode="Markdown")
        return
    
    username = context.args[0].replace('@', '')
    users = load_users()
    
    user_id = None
    for uid, data in users.items():
        if data.get('username') == username:
            user_id = uid
            break
    
    if not user_id:
        await update.message.reply_text(f"❌ User @{username} not found!")
        return
    
    if ban_user(user_id):
        await update.message.reply_text(f"🚫 User @{username} banned!")
    else:
        await update.message.reply_text(f"⚠️ User @{username} already banned!")

async def unban_command(update, context):
    """Unban user - /unban @username"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only!")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text("📝 Usage: `/unban @username`", parse_mode="Markdown")
        return
    
    username = context.args[0].replace('@', '')
    users = load_users()
    
    user_id = None
    for uid, data in users.items():
        if data.get('username') == username:
            user_id = uid
            break
    
    if not user_id:
        await update.message.reply_text(f"❌ User @{username} not found!")
        return
    
    if unban_user(user_id):
        await update.message.reply_text(f"✅ User @{username} unbanned!")
    else:
        await update.message.reply_text(f"⚠️ User @{username} is not banned!")