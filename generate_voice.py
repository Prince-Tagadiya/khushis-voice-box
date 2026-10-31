#!/usr/bin/env python3
"""
Fruit Speaker - Voice Generator & Uploader Tool
────────────────────────────────────────────────────────
Usage:
  1. Upload 1 word to ESP32:
       python3 generate_voice.py --btn 0 --word "Nisarg"
  2. Upload all 5 buttons:
       python3 generate_voice.py --words "Nisarg" "Banana" "Mango" "Grapes" "Orange"
  3. Re-bake audio.h with 5 new words (flashed directly into code):
       python3 generate_voice.py --bake "Nisarg" "Banana" "Mango" "Grapes" "Orange"
"""

import sys, os, argparse, subprocess, urllib.request

ESP32_IP = "192.168.4.1"
VOICE = "Samantha"  # macOS high quality voice (or try "Aman", "Rishi", "Daniel")

def text_to_pcm16k(word, voice=VOICE):
    """Generates crystal clear 16kHz 16-bit mono PCM using macOS built-in say + ffmpeg/afconvert"""
    aiff_tmp = f"/tmp/{word}_tmp.aiff"
    raw_tmp = f"/tmp/{word}_16k.raw"

    # Step 1: macOS native natural speech synthesis
    subprocess.run(["say", "-v", voice, "-r", "160", word, "-o", aiff_tmp], check=True)

    # Step 2: Convert to 16kHz mono 16-bit signed PCM
    if os.path.exists("/opt/homebrew/bin/ffmpeg"):
        cmd = ["/opt/homebrew/bin/ffmpeg", "-y", "-i", aiff_tmp, "-ar", "16000", "-ac", "1", "-f", "s16le", raw_tmp]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        # Fallback to macOS afconvert
        wav_tmp = f"/tmp/{word}_16k.wav"
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@16000", "-c", "1", aiff_tmp, wav_tmp], check=True)
        # Strip 44-byte wav header to get raw PCM
        with open(wav_tmp, "rb") as f:
            data = f.read()[44:]
        with open(raw_tmp, "wb") as f:
            f.write(data)
        if os.path.exists(wav_tmp): os.remove(wav_tmp)

    with open(raw_tmp, "rb") as f:
        pcm_bytes = f.read()

    if os.path.exists(aiff_tmp): os.remove(aiff_tmp)
    if os.path.exists(raw_tmp): os.remove(raw_tmp)

    return pcm_bytes

def upload_to_esp32(btn_idx, word, esp_ip=ESP32_IP):
    """Uploads raw PCM audio to ESP32 LittleFS via HTTP POST"""
    pcm = text_to_pcm16k(word)
    url = f"http://{esp_ip}/api/audio"

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="audio"; filename="btn{btn_idx}.raw"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode("latin-1") + pcm + f"\r\n--{boundary}--\r\n".encode("latin-1")

    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Cookie": "session=admin"  # Or whatever session
    })

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                print(f"✅ Button {btn_idx} ('{word}') successfully uploaded to ESP32 ({len(pcm)} bytes)!")
            else:
                print(f"❌ Server returned status {resp.status}")
    except Exception as e:
        print(f"❌ Upload failed: {e}. (Make sure you are connected to 'FruitSpeaker' WiFi)")

def bake_audio_header(words):
    """Generates audio.h with 5 crystal-clear words burned directly into PROGMEM"""
    if len(words) != 5:
        print("❌ Error: Must provide exactly 5 words for baking into audio.h")
        return

    var_names = ["apple", "banana", "mango", "grapes", "orange"]
    h_lines = [
        "// Auto-generated voice data: 16kHz, 16-bit, mono (Crystal Clear Speech)",
        "#pragma once",
        "#include <Arduino.h>",
        ""
    ]

    for i, (var, word) in enumerate(zip(var_names, words)):
        print(f"Synthesizing word {i+1}/5: '{word}'...")
        pcm = text_to_pcm16k(word)
        import struct
        samples = list(struct.unpack(f"<{len(pcm)//2}h", pcm))
        total_len = len(samples)

        h_lines.append(f"const uint32_t {var}_len = {total_len};")
        h_lines.append(f"const int16_t {var}_audio[] PROGMEM = {{")

        # Chunk into rows of 20 numbers
        for row_start in range(0, total_len, 20):
            row_vals = samples[row_start:row_start+20]
            row_str = ",".join(str(v) for v in row_vals)
            h_lines.append(f"{row_str},")

        h_lines.append("};")
        h_lines.append("")

    header_content = "\n".join(h_lines)
    header_path = "fruit_speaker/audio.h"
    with open(header_path, "w") as f:
        f.write(header_content)

    print(f"\n🎉 Successfully created '{header_path}' with words: {words}!")
    print("Now compile and upload fruit_speaker in Arduino IDE — it will speak these words with 100% crystal clarity!")

def main():
    parser = argparse.ArgumentParser(description="Fruit Speaker Voice Generator")
    parser.add_argument("--btn", type=int, help="Button index (0 to 4)")
    parser.add_argument("--word", type=str, help="1-word text to speak (e.g. Nisarg)")
    parser.add_argument("--words", nargs=5, help="Upload 5 words to buttons 0-4")
    parser.add_argument("--bake", nargs=5, help="Bake 5 words directly into fruit_speaker/audio.h")
    parser.add_argument("--ip", type=str, default=ESP32_IP, help=f"ESP32 IP (default: {ESP32_IP})")

    args = parser.parse_args()

    if args.bake:
        bake_audio_header(args.bake)
    elif args.words:
        for i, w in enumerate(args.words):
            upload_to_esp32(i, w, args.ip)
    elif args.btn is not None and args.word:
        upload_to_esp32(args.btn, args.word, args.ip)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python3 generate_voice.py --bake Nisarg Banana Mango Grapes Orange")
        print("  python3 generate_voice.py --btn 0 --word Nisarg")

if __name__ == "__main__":
    main()

