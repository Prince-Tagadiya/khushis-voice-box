import os
from PIL import Image, ImageDraw, ImageFont

def create_caregiver_card(pin="1234", name="Prince's Voice Box", output_path="Voice_Box_Caregiver_PIN_Card.png"):
    W, H = 1400, 880
    im = Image.new('RGB', (W, H), (248, 249, 251))
    d = ImageDraw.Draw(im)

    # Fonts
    f_title_bold = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 34, index=1)
    f_h2_bold    = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 22, index=1)
    f_body       = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 16, index=0)
    f_body_bold  = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 16, index=1)
    f_sub        = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 13, index=0)
    f_sub_bold   = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 13, index=1)
    f_pin        = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 56, index=1)
    f_guj        = ImageFont.truetype('/System/Library/Fonts/KohinoorGujarati.ttc', 16)

    # Colors
    c_bg_card   = (255, 255, 255)
    c_border    = (226, 232, 240)
    c_text_dark = (15, 23, 42)
    c_text_muted= (100, 116, 139)
    c_teal      = (13, 148, 136)
    c_teal_bg   = (240, 253, 250)
    c_green_dark= (26, 77, 46)

    # Outer Container Card
    pad = 40
    d.rounded_rectangle([pad, pad, W - pad, H - pad], radius=28, fill=c_bg_card, outline=c_border, width=2)

    # Top Header
    # Logo square
    logo_size = 56
    logo_x = pad + 36
    logo_y = pad + 36
    d.rounded_rectangle([logo_x, logo_y, logo_x + logo_size, logo_y + logo_size], radius=14, fill=c_green_dark)
    f_logo = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 11, index=1)
    d.text((logo_x + 9, logo_y + 14), "The\nCreato4\nLab", fill=(255, 255, 255), font=f_logo, spacing=1)

    # Brand Title
    d.text((logo_x + 72, logo_y + 6), "CREATO4 LAB · ASSISTIVE CARE", fill=c_teal, font=f_sub_bold)
    d.text((logo_x + 72, logo_y + 24), "Voice Box · Caregiver Memory Card", fill=c_text_dark, font=f_title_bold)

    # Verified Pill (Top Right)
    pill_w, pill_h = 160, 32
    pill_x = W - pad - 36 - pill_w
    pill_y = logo_y + 12
    d.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=16, fill=c_teal_bg, outline=c_teal, width=1)
    d.text((pill_x + 18, pill_y + 8), "● OFFICIAL SYSTEM", fill=c_teal, font=f_sub_bold)

    # Divider line
    div_y = pad + 115
    d.line([(pad + 36, div_y), (W - pad - 36, div_y)], fill=c_border, width=1)

    # Left Box: Security PIN (Confidential)
    box_top = div_y + 28
    box_bottom = H - pad - 80
    box_w = 580
    box_l_x = pad + 36
    d.rounded_rectangle([box_l_x, box_top, box_l_x + box_w, box_bottom], radius=20, fill=(248, 250, 252), outline=c_border, width=1)

    # Inside Left Box
    d.text((box_l_x + 28, box_top + 26), "SECURITY ACCESS PIN", fill=c_text_muted, font=f_sub_bold)
    d.text((box_l_x + 28, box_top + 48), "Keep this 4-digit PIN confidential. Used to unlock studio controls.", fill=c_text_muted, font=f_sub)

    # 4 PIN Tiles
    pin_tile_w = 76
    pin_tile_h = 96
    tile_gap = 18
    tiles_start_x = box_l_x + 28
    tiles_y = box_top + 84

    pin_str = (str(pin) + "    ")[:4]
    for i, ch in enumerate(pin_str):
        tx = tiles_start_x + i * (pin_tile_w + tile_gap)
        d.rounded_rectangle([tx, tiles_y, tx + pin_tile_w, tiles_y + pin_tile_h], radius=14, fill=(255, 255, 255), outline=c_teal, width=2)
        # Center digit
        bbox = f_pin.getbbox(ch)
        cw = bbox[2] - bbox[0]
        ch_h = bbox[3] - bbox[1]
        cx = tx + (pin_tile_w - cw) // 2
        cy = tiles_y + (pin_tile_h - ch_h) // 2 - 4
        d.text((cx, cy), ch, fill=c_text_dark, font=f_pin)

    # Device & Specs Meta below PIN
    meta_y = tiles_y + pin_tile_h + 38
    d.text((box_l_x + 28, meta_y), "ASSIGNED DEVICE NAME", fill=c_text_muted, font=f_sub_bold)
    d.text((box_l_x + 28, meta_y + 18), name, fill=c_text_dark, font=f_h2_bold)

    meta_y2 = meta_y + 64
    d.text((box_l_x + 28, meta_y2), "HARDWARE CONFIGURATION", fill=c_text_muted, font=f_sub_bold)
    d.text((box_l_x + 28, meta_y2 + 18), "ESP32-C3 Super Mini · MAX98357A I2S 3W DAC", fill=c_text_dark, font=f_body_bold)
    d.text((box_l_x + 28, meta_y2 + 42), "Tactile 5-Key Matrix · Instant Touch Wake (~5 uA)", fill=c_text_muted, font=f_sub)

    # Right Box: Assistive Features & System Details
    box_r_x = box_l_x + box_w + 24
    box_r_w = W - pad - 36 - box_r_x
    d.rounded_rectangle([box_r_x, box_top, box_r_x + box_r_w, box_bottom], radius=20, fill=(248, 250, 252), outline=c_border, width=1)

    # 4 Feature Items on Right
    features = [
        ("SPEECH VOCABULARY ENGINE", "English + ગુજરાતી Dual Speech", "Out-of-the-box native fruit vocabulary for multi-lingual clarity", True),
        ("COGNITIVE PACING (ANTI-SPAM)", "1.2s Anti-Spam Sensory Latch", "Protects user from rapid sensory overload and repetitive tapping", False),
        ("POWER ARCHITECTURE", "True Deep Sleep with Instant Wake", "Preserves battery life indefinitely; activates on any single touch", False),
        ("ACOUSTIC SHOUTING ENGINE", "16-Bit 16kHz Vocal Clarification", "Acoustically calibrated loudness optimized for accessible learning", False)
    ]

    item_y = box_top + 24
    for title, val, desc, is_guj in features:
        d.text((box_r_x + 28, item_y), title, fill=c_teal, font=f_sub_bold)
        if is_guj:
            # Draw English part with Helvetica, Gujarati part with Kohinoor
            d.text((box_r_x + 28, item_y + 18), "English + ", fill=c_text_dark, font=f_body_bold)
            w_eng = f_body_bold.getbbox("English + ")[2]
            d.text((box_r_x + 28 + w_eng, item_y + 18), "ગુજરાતી", fill=c_text_dark, font=f_guj)
            w_guj = f_guj.getbbox("ગુજરાતી")[2]
            d.text((box_r_x + 28 + w_eng + w_guj + 4, item_y + 18), " Dual Speech", fill=c_text_dark, font=f_body_bold)
        else:
            d.text((box_r_x + 28, item_y + 18), val, fill=c_text_dark, font=f_body_bold)
        d.text((box_r_x + 28, item_y + 40), desc, fill=c_text_muted, font=f_sub)
        item_y += 78

    # Bottom Footer
    footer_y = H - pad - 46
    d.text((pad + 36, footer_y), "Designed & Engineered by Creato4 Lab · Non-Profit Assistive Care Research", fill=c_text_muted, font=f_sub)
    d.text((W - pad - 240, footer_y), "Official Support Active · Till 31 Dec 2026", fill=c_text_muted, font=f_sub)

    im.save(output_path, quality=95)
    print(f"Created {output_path} successfully!")

create_caregiver_card("1234", "Prince's Voice Box", "Voice_Box_Caregiver_PIN_Card.png")
create_caregiver_card("1234", "Prince's Voice Box", "web_dashboard/Voice_Box_Caregiver_PIN_Card.png")
