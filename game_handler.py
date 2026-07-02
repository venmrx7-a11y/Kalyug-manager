import random
import asyncio
from database import *
from utils import format_with_emojis

async def dice_command(update, context):
    """Play dice game - /dice"""
    user_id = update.effective_user.id
    
    if is_banned(user_id):
        await update.message.reply_text("❌ You are banned!")
        return
    
    if not is_approved(user_id):
        await update.message.reply_text("❌ You are not approved!")
        return
    
    await update.message.reply_text("🎲 <b>ROLLING DICE...</b>", parse_mode="HTML")
    await asyncio.sleep(1.5)
    
    result = random.randint(1, 6)
    settings = load_settings()
    min_win = settings.get('min_win', 4)
    max_win = settings.get('max_win', 10)
    win = result >= 4
    amount = random.randint(min_win, max_win)
    
    if win:
        update_user(user_id, 'wins', get_user(user_id).get('wins', 0) + 1)
        update_user(user_id, 'earnings', get_user(user_id).get('earnings', 0) + amount)
    
    msg = f"""
🎲 <b>DICE RESULT</b>
━━━━━━━━━━━━━━━━━━
🎯 Result: <b>{result}</b>
{'🎉 YOU WIN!' if win else '😢 YOU LOSE!'}
{'💰 +₹' + str(amount) if win else '💔 Better luck next time!'}
━━━━━━━━━━━━━━━━━━
    """
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")