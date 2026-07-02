# All Premium Emojis with Telegram IDs
PREMIUM_EMOJIS = {
    # Check Marks
    "verified": {"id": "6246537187614005254", "fallback": "✅"},
    "verify": {"id": "6246782404476803545", "fallback": "✅"},
    "verify_blue": {"id": "6010060634803148161", "fallback": "✅"},
    "verify_purple": {"id": "6010498532488778300", "fallback": "✅"},
    
    # Eyes
    "eye": {"id": "6035338338406242050", "fallback": "👁️"},
    "eyeball": {"id": "6035051267087143217", "fallback": "👁️"},
    "eyes": {"id": "6035225389356290238", "fallback": "👀"},
    "eyes_blue": {"id": "6035081585261287115", "fallback": "👀"},
    
    # Fire
    "fire": {"id": "4956222745814762495", "fallback": "🔥"},
    "fire_red": {"id": "4956606007221421405", "fallback": "🔥"},
    "fire_orange": {"id": "4956429969396859866", "fallback": "🔥"},
    "explosion": {"id": "6032673796530377389", "fallback": "💥"},
    
    # Hearts
    "heart": {"id": "5783157259152397008", "fallback": "❤️"},
    "heart_red": {"id": "5801084710343938087", "fallback": "❤️"},
    "heart_pink": {"id": "6010280773351904888", "fallback": "❤️"},
    "heart_blue": {"id": "5780496071645991525", "fallback": "💙"},
    "heart_green": {"id": "5888789252493283486", "fallback": "💚"},
    "heart_yellow": {"id": "5840261097719148872", "fallback": "💛"},
    "heart_orange": {"id": "5840263144212529797", "fallback": "🧡"},
    "heart_purple": {"id": "5840265018655703965", "fallback": "💜"},
    "heart_black": {"id": "5840266939932994956", "fallback": "🖤"},
    
    # Stars
    "star": {"id": "6244496562752331516", "fallback": "⭐"},
    "star_gold": {"id": "5904618938578243567", "fallback": "⭐"},
    "star_blue": {"id": "6010193314932855525", "fallback": "⭐"},
    "star_glow": {"id": "6010156854955480259", "fallback": "🌟"},
    "sparkle": {"id": "6010338729640596556", "fallback": "✨"},
    "sparkle_blue": {"id": "6010086134023985536", "fallback": "✨"},
    
    # Crown
    "crown": {"id": "5794422335599546668", "fallback": "👑"},
    "crown_gold": {"id": "6089003761496232797", "fallback": "👑"},
    "crown_blue": {"id": "6247039939305808563", "fallback": "👑"},
    
    # Money
    "money": {"id": "6089104607328342288", "fallback": "💰"},
    "money_bag": {"id": "6086730718774300509", "fallback": "💰"},
    "dollar": {"id": "6089140105233044310", "fallback": "💵"},
    "diamond": {"id": "6086778246882399112", "fallback": "💎"},
    
    # Thumbs
    "like": {"id": "6089313931149448495", "fallback": "👍"},
    "unlike": {"id": "6088789257285988672", "fallback": "👎"},
    "clap": {"id": "6093744967304352336", "fallback": "👏"},
    
    # Smileys
    "smile": {"id": "6093864814071780526", "fallback": "😀"},
    "big_smile": {"id": "6093922327978840798", "fallback": "😀"},
    "laugh": {"id": "5782741660936966676", "fallback": "😂"},
    "teeth": {"id": "6035060329468137931", "fallback": "😁"},
    "wink": {"id": "6089024570612781324", "fallback": "😉"},
    "heart_eyes": {"id": "6010179687001625256", "fallback": "😍"},
    "kiss": {"id": "6044373012566774137", "fallback": "😘"},
    "cool": {"id": "6032853480782172520", "fallback": "😎"},
    "sad": {"id": "5780793884678296697", "fallback": "😢"},
    "cry": {"id": "5783024321324651865", "fallback": "😭"},
    "angry": {"id": "6035355642829475999", "fallback": "😡"},
    "think": {"id": "5782756916660802905", "fallback": "🤔"},
    
    # Flags
    "flag_in": {"id": "5433601609076586221", "fallback": "🇮🇳"},
    "flag_us": {"id": "5433865586356531140", "fallback": "🇺🇸"},
    "flag_gb": {"id": "5433827537241258614", "fallback": "🇬🇧"},
    "flag_pk": {"id": "5434064563601421981", "fallback": "🇵🇰"},
    "flag_bd": {"id": "5433854239052935880", "fallback": "🇧🇩"},
    
    # Extra
    "flex": {"id": "6147464060305676048", "fallback": "😎"},
    "frozen": {"id": "5449449325434266744", "fallback": "❄️"},
    "bolt": {"id": "5791970059597386804", "fallback": "⚡"},
    "zap": {"id": "6087079590377820415", "fallback": "⚡"},
    "dice_emoji": {"id": "5791970059597386804", "fallback": "🎲"},
    "trophy": {"id": "6010156854955480259", "fallback": "🏆"},
    "gift": {"id": "6010338729640596556", "fallback": "🎁"},
    "lock": {"id": "5465443379917629504", "fallback": "🔒"},
    "unlock": {"id": "5465443379917629504", "fallback": "🔓"},
    "qr_emoji": {"id": "6089104607328342288", "fallback": "📱"},
    "warning": {"id": "6035355642829475999", "fallback": "⚠️"},
}

def get_emoji_html(name):
    """Get premium emoji HTML by name"""
    if name in PREMIUM_EMOJIS:
        data = PREMIUM_EMOJIS[name]
        return f'<tg-emoji emoji-id="{data["id"]}">{data["fallback"]}</tg-emoji>'
    return ""

def get_random_emoji():
    """Get random premium emoji"""
    import random
    names = list(PREMIUM_EMOJIS.keys())
    return get_emoji_html(random.choice(names)) if names else ""