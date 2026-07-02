import qrcode
from io import BytesIO
from telegram import InputFile
from database import *
from utils import format_with_emojis
from config import OWNER_ID

def generate_upi_qr(upi_id, amount, keyword):
    """Generate UPI QR code"""
    upi_string = f"upi://pay?pa={upi_id}&am={amount}&cu=INR&tn={keyword} payment"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_string)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

async def handle_qr_request(update, context):
    """Handle UPI QR requests"""
    user_id = update.effective_user.id
    username = update.effective_user.username or "NoUsername"
    text = update.message.text.strip()
    
    # Check banned
    if is_banned(user_id):
        await update.message.reply_text("❌ You are banned!")
        return
    
    # Check approved
    if not is_approved(user_id):
        await update.message.reply_text("❌ You are not approved! Contact owner.")
        return
    
    # Check group lock
    settings = load_settings()
    if settings.get('group_locked', False):
        await update.message.reply_text("🔒 Group is locked! No transactions.")
        return
    
    # Parse: KEYWORD AMOUNT
    parts = text.split()
    if len(parts) != 2:
        return
    
    keyword, amount_str = parts[0], parts[1]
    
    try:
        amount = float(amount_str)
        if amount <= 0 or amount > 10000:
            return
    except ValueError:
        return
    
    # Find keyword
    upi_data = find_upi_keyword(keyword)
    if not upi_data:
        return
    
    upi_id = upi_data['upi_id']
    
    # Generate QR
    try:
        qr_image = generate_upi_qr(upi_id, amount, keyword)
        
        # Update usage
        increment_upi_usage(keyword)
        
        # Save history
        qr_id = add_qr_history(user_id, username, keyword, upi_id, amount)
        
        # Update user
        user = get_user(user_id)
        if user:
            update_user(user_id, 'qr_used', user.get('qr_used', 0) + 1)
        
        # Get QR message
        settings = load_settings()
        qr_message = settings.get('qr_message', DEFAULT_SETTINGS['qr_message']).format(amount=amount)
        
        # Create caption
        caption = f"""
📱 <b>PAYMENT QR CODE</b>
━━━━━━━━━━━━━━━━━━
🔑 Keyword: <b>{keyword}</b>
💳 UPI: <code>{upi_id}</code>
💰 Amount: <b>₹{amount}</b>
👤 User: @{username}

━━━━━━━━━━━━━━━━━━
{qr_message}
━━━━━━━━━━━━━━━━━━
🆔 {qr_id}
📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━
        """
        
        # Send QR
        await update.message.reply_photo(
            photo=InputFile(qr_image, filename="qr.png"),
            caption=format_with_emojis(caption),
            parse_mode="HTML"
        )
        
        # Send to owner
        await context.bot.send_photo(
            chat_id=OWNER_ID,
            photo=InputFile(qr_image, filename=f"qr_{qr_id}.png"),
            caption=f"""
📱 <b>QR GENERATED</b>
━━━━━━━━━━━━━━━━━━
🔑 Keyword: {keyword}
💳 UPI: {upi_id}
💰 Amount: ₹{amount}
👤 User: @{username}
🆔 ID: {user_id}
📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━
            """,
            parse_mode="HTML"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")