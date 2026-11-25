"""Open Canva images in a real browser window and save them at full size.
    python tools/canva_fetch.py <outdir> <mediaId> [<mediaId> ...]
A Chromium window opens. The first time, log in to Canva in that window yourself (the login is kept in a
private profile folder on this PC, outside the project, so it is never uploaded anywhere). The script then
opens each image's page and saves the largest picture the page loads, plus a screenshot of the page.
"""
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
IDS = sys.argv[2:]
PROFILE = Path.home() / "AppData" / "Local" / "canva-viewer-profile"      # not inside the git repo
LOGIN_WAIT_S = 420

def logged_out(url):
    u = url.lower()
    return any(k in u for k in ("/login", "/signup", "accounts.google", "/sso", "oauth"))

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(str(PROFILE), headless=False, viewport={"width": 1280, "height": 900},
                                               args=["--disable-blink-features=AutomationControlled"])
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    best = {}
    cur = {"id": None}
    def on_resp(r):
        try:
            ct = r.headers.get("content-type", "")
            if not ct.startswith("image/") or cur["id"] is None: return
            body = r.body()
            if len(body) > len(best.get(cur["id"], (b"", ""))[0]): best[cur["id"]] = (body, ct)
        except Exception:
            pass
    pg.on("response", on_resp)
    for n, mid in enumerate(IDS):
        cur["id"] = mid
        pg.goto(f"https://www.canva.com/M/{mid}", wait_until="domcontentloaded", timeout=90000)
        pg.wait_for_timeout(4000)
        t0 = time.time()
        if logged_out(pg.url):
            print("WAITING FOR LOGIN in the browser window ...", flush=True)
            while logged_out(pg.url) and time.time() - t0 < LOGIN_WAIT_S:
                pg.wait_for_timeout(2000)
            if logged_out(pg.url):
                print("NOT LOGGED IN after waiting; stopping.", flush=True); break
            print("logged in", flush=True)
            pg.goto(f"https://www.canva.com/M/{mid}", wait_until="domcontentloaded", timeout=90000)
        pg.wait_for_timeout(9000)
        pg.screenshot(path=str(OUT / f"{mid}_page.png"))
        if mid in best:
            body, ct = best[mid]
            ext = {"image/png": "png", "image/webp": "webp", "image/jpeg": "jpg", "image/avif": "avif"}.get(ct.split(";")[0], "img")
            (OUT / f"{mid}.{ext}").write_bytes(body)
            print(f"{mid}: saved {len(body)} bytes ({ct}); page {pg.url[:80]}", flush=True)
        else:
            print(f"{mid}: no image captured; page {pg.url[:80]}", flush=True)
    ctx.close()
print("DONE", flush=True)
