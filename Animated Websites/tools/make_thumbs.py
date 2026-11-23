"""Checks every site in a phone-sized browser and saves the gallery pictures (thumbs/NN.jpg).

Run after build_sites.py:  python "Animated Websites/tools/make_thumbs.py"
Needs: pip install playwright pillow  (and: playwright install chromium)
"""
import asyncio
import io
import json
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

OUT = Path(__file__).resolve().parent.parent
THUMBS = OUT / 'thumbs'
SHEET = Path(sys.argv[1]) if len(sys.argv) > 1 else None   # optional: save a contact sheet of all designs here


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


async def main():
    THUMBS.mkdir(exist_ok=True)
    pages = sorted(OUT.glob('[0-9][0-9]-*.html'))
    wedding = json.loads((OUT / 'shared' / 'config.js').read_text(encoding='utf-8').split('=', 1)[1].strip().rstrip(';'))
    srv = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(OUT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{srv.server_port}/'
    problems, images = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2,
                                        is_mobile=True, has_touch=True, reduced_motion='reduce')
        await ctx.route('**/shared/music.mp3', lambda r: r.fulfill(status=404, body=''))
        for path in pages:
            num = path.name[:2]
            pg = await ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)))
            await pg.goto(base + path.name, wait_until='load')
            await pg.wait_for_function('window.SITE_READY === true', timeout=20000)
            await pg.evaluate('document.fonts.ready')
            await pg.tap('#openBtn')
            await pg.wait_for_timeout(700)
            info = await pg.evaluate('''() => ({
                groom: (document.getElementById('gn') || {}).textContent || '',
                bride: (document.getElementById('bn') || {}).textContent || '',
                date: (document.getElementById('dt') || {}).textContent || '',
                venue: (document.getElementById('vn') || {}).textContent || '',
                event: (document.getElementById('ev') || {}).textContent || '',
                overflow: document.documentElement.scrollWidth - innerWidth,
                stageW: document.getElementById('st').getBoundingClientRect().width
            })''')
            bad = []
            if wedding['groom'] not in info['groom'] or wedding['bride'] not in info['bride']: bad.append(f"names {info['groom']!r}/{info['bride']!r}")
            if wedding['dateDisplay'] not in info['date']: bad.append(f"date {info['date']!r}")
            if wedding['venue'] not in info['venue']: bad.append(f"venue {info['venue']!r}")
            if 'Baraat' not in info['event']: bad.append(f"event {info['event']!r}")
            if info['overflow'] > 1: bad.append(f"sideways scroll {info['overflow']}px")
            if info['stageW'] < 300: bad.append(f"stage width {info['stageW']}")
            if errs: bad.append('errors: ' + '; '.join(errs[:3]))
            if bad: problems.append(f'{path.name}: ' + ' | '.join(bad))
            png = await pg.locator('#st').screenshot()
            im = Image.open(io.BytesIO(png)).convert('RGB').resize((270, 480), Image.LANCZOS)
            im.save(THUMBS / f'{num}.jpg', quality=84, optimize=True, progressive=True)
            images.append(im)
            await pg.close()
            print(f'{num} {"OK" if not bad else "PROBLEM"}', flush=True)
        await browser.close()
    srv.shutdown()
    if SHEET and images:
        cols, tw, th = 11, 135, 240
        rows = (len(images) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * tw, rows * th), 'white')
        for i, im in enumerate(images):
            sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
        sheet.save(SHEET, quality=85)
    print(f'\n{len(pages)} sites checked, {len(pages) - len(problems)} OK')
    for line in problems:
        print('PROBLEM', line)


asyncio.run(main())
