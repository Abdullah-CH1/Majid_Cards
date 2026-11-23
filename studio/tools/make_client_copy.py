#!/usr/bin/env python3
"""Make "for client/Wedding Invitation Designs.zip": the studio in client view (no editor) + how-to-open note."""
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "for client"
OUT.mkdir(exist_ok=True)

src = (ROOT / "wedding_invite_studio_fully_customizable.html").read_text(encoding="utf-8")
pre = json.dumps({"client": True, "title": "Choose your invitation design"})
page, n = re.subn(r'(<script id="preset" type="application/json">)[\s\S]*?(</script>)',
                  lambda m: m.group(1) + pre + m.group(2), src, count=1)
assert n == 1, "preset block not found"

NOTE = """HOW TO VIEW THE INVITATION DESIGNS

1. Unzip this folder (right-click > Extract All).
2. Double-click "Wedding Invitation Designs.html".
   It opens in your web browser. Google Chrome or Microsoft Edge work best.
3. Keep the internet on (the fonts load online).

Browsing:
- Click any design in the list to watch it play. Use the arrows (or the left/right keys) to go through them one by one.
- Press Replay to watch it again.
- Switch between Baraat and Walima at the top to see each design in both colour schemes.
- When you find the one you like, press "I like Sample ..." and send us the message, or just tell us the sample number.

On a phone: save the file to your phone first, then open it with Chrome.
"""

html_path = OUT / "Wedding Invitation Designs.html"
note_path = OUT / "HOW TO OPEN.txt"
html_path.write_text(page, encoding="utf-8")
note_path.write_text(NOTE, encoding="utf-8")
zip_path = OUT / "Wedding Invitation Designs.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(html_path, html_path.name)
    z.write(note_path, note_path.name)
print(f"{zip_path}  ({zip_path.stat().st_size / 1e6:.1f} MB)")
