#!/usr/bin/env python3
import http.server
import socketserver
import subprocess
import urllib.parse
import os, sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/tts':
            params = urllib.parse.parse_qs(parsed.query)
            text = params.get('text', [''])[0].strip()
            if not text:
                self.send_error(400, "Missing text parameter")
                return

            try:
                # 1. Generate natural speech using macOS say command
                aiff_tmp = f"/tmp/{text}_tts.aiff"
                raw_tmp = f"/tmp/{text}_tts.raw"
                subprocess.run(["say", "-v", "Samantha", "-r", "160", text, "-o", aiff_tmp], check=True)
                
                # 2. Convert to exact 16kHz mono 16-bit raw PCM
                if os.path.exists("/opt/homebrew/bin/ffmpeg"):
                    subprocess.run(
                        ["/opt/homebrew/bin/ffmpeg", "-y", "-i", aiff_tmp, "-ar", "16000", "-ac", "1", "-f", "s16le", raw_tmp],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
                    )
                else:
                    wav_tmp = f"/tmp/{text}_tts.wav"
                    subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@16000", "-c", "1", aiff_tmp, wav_tmp], check=True)
                    with open(wav_tmp, "rb") as f:
                        data = f.read()[44:]
                    with open(raw_tmp, "wb") as f:
                        f.write(data)
                    if os.path.exists(wav_tmp): os.remove(wav_tmp)

                with open(raw_tmp, "rb") as f:
                    pcm_data = f.read()

                if os.path.exists(aiff_tmp): os.remove(aiff_tmp)
                if os.path.exists(raw_tmp): os.remove(raw_tmp)

                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(pcm_data)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(pcm_data)
                return
            except Exception as e:
                self.send_error(500, str(e))
                return

        super().do_GET()

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving Fruit Speaker Studio at http://localhost:{PORT}")
        httpd.serve_forever()

