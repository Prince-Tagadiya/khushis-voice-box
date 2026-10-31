import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_instagram_story(device_name="Prince's Voice Box", output_path="Voice_Box_Instagram_Story.png"):
    W, H = 1080, 1920
    im = Image.new('RGB', (W, H), (11, 15, 23)) # Deep obsidian luxury dark
    d = ImageDraw.Draw(im)

    # Ambient subtle gradient glow at top and center
    # Fonts
    f_badge     = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 16, index=1)
    f_eyebrow   = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 18, index=1)
    f_hero_bold = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 68, index=1)
    f_tagline   = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 24, index=0)
    f_card_val  = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 20, index=1)
    f_card_sub  = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 15, index=0)
    f_guj       = ImageFont.truetype('/System/Library/Fonts/KohinoorGujarati.ttc', 20)
    f_footer    = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 15, index=0)

    # Colors
    c_white     = (255, 255, 255)
    c_muted     = (148, 163, 184)
    c_teal      = (45, 212, 191)
    c_teal_dim  = (20, 184, 166)
    c_teal_bg   = (13, 148, 136, 40)
    c_card_bg   = (18, 24, 38)
    c_card_bor  = (33, 44, 66)

    # Top Navigation Bar
    pad_x = 72
    top_y = 120

    # Creato4 Logo
    logo_size = 54
    d.rounded_rectangle([pad_x, top_y, pad_x + logo_size, top_y + logo_size], radius=14, fill=(20, 60, 40), outline=(45, 212, 191), width=1)
    f_logo = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 10, index=1)
    d.text((pad_x + 9, top_y + 12), "The\nCreato4\nLab", fill=(255, 255, 255), font=f_logo, spacing=1)

    d.text((pad_x + 70, top_y + 10), "CREATO4 LAB", fill=c_white, font=f_badge)
    d.text((pad_x + 70, top_y + 30), "Assistive Speech Systems", fill=c_muted, font=f_card_sub)

    # Activated Pill (Top Right)
    pill_w, pill_h = 168, 40
    pill_x = W - pad_x - pill_w
    pill_y = top_y + 7
    d.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=20, fill=(15, 35, 30), outline=c_teal, width=1)
    d.text((pill_x + 22, pill_y + 11), "● ACTIVATED", fill=c_teal, font=f_badge)

    # Editorial Header
    head_y = top_y + 110
    d.text((pad_x, head_y), "JUST UNBOXED & ACTIVATED", fill=c_teal, font=f_eyebrow)
    d.text((pad_x, head_y + 36), "Voice Box", fill=c_white, font=f_hero_bold)
    d.text((pad_x, head_y + 126), "Tactile 1-word speech assistant designed for single-touch\nclarity and focused cognitive processing.", fill=c_muted, font=f_tagline, spacing=6)

    # Product Photo Card
    card_y = head_y + 240
    card_w = W - pad_x * 2
    card_h = 560
    d.rounded_rectangle([pad_x, card_y, pad_x + card_w, card_y + card_h], radius=24, fill=(15, 20, 30), outline=c_card_bor, width=2)

    # Load and place product photo
    photo_path = "/Users/princetagadiya/Downloads/Fruit Learning Talking Button Device.png"
    if os.path.exists(photo_path):
        p_img = Image.open(photo_path).convert('RGB')
        # Target width inside card: card_w - 24
        target_w = card_w - 24
        target_h = int(p_img.height * (target_w / p_img.width))
        if target_h > card_h - 24:
            target_h = card_h - 24
            target_w = int(p_img.width * (target_h / p_img.height))
        p_img_resized = p_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        pos_x = pad_x + (card_w - target_w) // 2
        pos_y = card_y + (card_h - target_h) // 2
        im.paste(p_img_resized, (pos_x, pos_y))

    # Re-draw clean border on top of image
    d.rounded_rectangle([pad_x, card_y, pad_x + card_w, card_y + card_h], radius=24, outline=c_card_bor, width=2)

    # 4 Sleek Minimalist Feature Chips (2x2 Grid)
    grid_y = card_y + card_h + 46
    gw = (card_w - 20) // 2
    gh = 130

    chips = [
        ("DUAL SPEECH ENGINE", "English + ", True, "ગુજરાતી", "Native fruit speech"),
        ("COGNITIVE PACING", "1.2s Anti-Spam Latch", False, "", "Sensory overload guard"),
        ("INSTANT TOUCH WAKE", "ESP32-C3 Super Mini", False, "", "Ultra-low ~5 uA sleep"),
        ("ACOUSTIC TUNING", "16-Bit 16kHz Vocal Boost", False, "", "MAX98357A I2S DAC")
    ]

    for idx, (title, val, is_guj, guj_val, desc) in enumerate(chips):
        col = idx % 2
        row = idx // 2
        cx = pad_x + col * (gw + 20)
        cy = grid_y + row * (gh + 18)

        d.rounded_rectangle([cx, cy, cx + gw, cy + gh], radius=16, fill=c_card_bg, outline=c_card_bor, width=1)
        d.text((cx + 20, cy + 18), title, fill=c_teal, font=f_badge)

        if is_guj:
            d.text((cx + 20, cy + 44), val, fill=c_white, font=f_card_val)
            w_val = f_card_val.getbbox(val)[2]
            d.text((cx + 20 + w_val, cy + 44), guj_val, fill=c_white, font=f_guj)
        else:
            d.text((cx + 20, cy + 44), val, fill=c_white, font=f_card_val)

        d.text((cx + 20, cy + 76), desc, fill=c_muted, font=f_card_sub)

    # Bottom Editorial Bar
    bot_y = H - 140
    d.line([(pad_x, bot_y), (W - pad_x, bot_y)], fill=(30, 41, 59), width=1)
    d.text((pad_x, bot_y + 24), "Creato4 Lab · Non-Profit Assistive Care Research", fill=c_muted, font=f_footer)
    d.text((W - pad_x - 130, bot_y + 24), "creato4lab.org", fill=c_teal_dim, font=f_footer)

    im.save(output_path, quality=95)
    print(f"Created {output_path} successfully!")

create_instagram_story("Prince's Voice Box", "Voice_Box_Instagram_Story.png")
create_instagram_story("Prince's Voice Box", "web_dashboard/Voice_Box_Instagram_Story.png")
