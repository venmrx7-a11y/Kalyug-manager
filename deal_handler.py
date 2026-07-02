from datetime import datetime
import random
import asyncio
from database import *
from utils import format_with_emojis
from config import ADMIN_IDS

async def add_deal_command(update, context):
    """Add deal - /adddeal STATUS BUYER SELLER AMOUNT"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("❌ Admin only!")
        return
    
    args = context.args
    if len(args) < 4:
        await update.message.reply_text(
            "📝 Usage: `/adddeal STATUS BUYER SELLER AMOUNT`\n"
            "Example: `/adddeal HOLD @buyer @seller 50`",
            parse_mode="Markdown"
        )
        return
    
    status = args[0].upper()
    buyer = args[1].replace('@', '')
    seller = args[2].replace('@', '')
    amount = args[3]
    
    if status not in ["HOLD", "COMPLETE"]:
        await update.message.reply_text("❌ Status must be HOLD or COMPLETE!")
        return
    
    deal_id = add_deal(buyer, seller, amount, status)
    
    msg = f"""
✅ <b>DEAL ADDED!</b>
━━━━━━━━━━━━━━━━━━
📋 ID: {deal_id}
👤 Buyer: @{buyer}
👤 Seller: @{seller}
💰 Amount: ₹{amount}
📌 Status: {status}
━━━━━━━━━━━━━━━━━━
    """
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

async def deal_status_command(update, context):
    """Check deal status - /dealstatus"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("❌ Admin only!")
        return
    
    total, hold, complete, amount = get_deal_stats()
    
    msg = f"""
📊 <b>DEAL STATUS</b>
━━━━━━━━━━━━━━━━━━
📋 Total Deals: {total}
⏳ HOLD: {hold}
✅ Complete: {complete}
💰 Total Amount: ₹{amount}
━━━━━━━━━━━━━━━━━━
    """
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

async def complete_deal_command(update, context):
    """Complete deal and dice game - /completed @buyer @seller"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("❌ Admin only!")
        return
    
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("📝 Usage: `/completed @buyer @seller`", parse_mode="Markdown")
        return
    
    buyer = args[0].replace('@', '')
    seller = args[1].replace('@', '')
    
    # Random numbers
    buyer_nums = random.sample(range(1, 7), 3)
    seller_nums = random.sample(range(1, 7), 3)
    
    # Announce
    msg1 = f"""
✅ <b>DEAL COMPLETED!</b>
━━━━━━━━━━━━━━━━━━
👤 Buyer: @{buyer}
👤 Seller: @{seller}
🎮 Let's play dice game!
━━━━━━━━━━━━━━━━━━
    """
    await update.message.reply_text(format_with_emojis(msg1), parse_mode="HTML")
    
    await asyncio.sleep(1)
    
    msg2 = f"""
🎲 <b>DICE GAME STARTED!</b>
━━━━━━━━━━━━━━━━━━
@{buyer} numbers: <b>{', '.join(map(str, buyer_nums))}</b>
@{seller} numbers: <b>{', '.join(map(str, seller_nums))}</b>
I roll the dice...
━━━━━━━━━━━━━━━━━━
    """
    await update.message.reply_text(format_with_emojis(msg2), parse_mode="HTML")
    
    await asyncio.sleep(2)
    
    # Roll dice
    result = random.randint(1, 6)
    await update.message.reply_text(f"🎲 <b>ROLLING...</b>\nResult: <b>{result}</b>", parse_mode="HTML")
    
    await asyncio.sleep(1)
    
    # Determine winner
    settings = load_settings()
    min_win = settings.get('min_win', 4)
    max_win = settings.get('max_win', 10)
    win_amount = random.randint(min_win, max_win)
    
    buyer_diff = min(abs(n - result) for n in buyer_nums)
    seller_diff = min(abs(n - result) for n in seller_nums)
    
    if buyer_diff < seller_diff:
        winner, loser = buyer, seller
    elif seller_diff < buyer_diff:
        winner, loser = seller, buyer
    else:
        msg3 = "🤝 <b>IT'S A TIE!</b>\n━━━━━━━━━━━━━━━━━━\nPlay again!"
        await update.message.reply_text(format_with_emojis(msg3), parse_mode="HTML")
        return
    
    msg3 = f"""
🎉 <b>HURREY! WINNER FOUND!</b>
━━━━━━━━━━━━━━━━━━
🏆 Winner: @{winner}
💔 Loser: @{loser}
💰 Win Amount: ₹{win_amount}
━━━━━━━━━━━━━━━━━━
📤 Please send QR in DM to claim!
    """
    await update.message.reply_text(format_with_emojis(msg3), parse_mode="HTML")