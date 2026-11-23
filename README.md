# Wedding Card project — Abdul Aleem & Laiba

Baraat · Thursday, 31 December 2026 · 2:00 PM · Noor Mahal Marquee, G.T Road, Islamabad

Double-click any `.html` file to open it in Chrome or Edge. Keep the internet on so the fonts load.

## Invitation websites (send these to guests)

| What | Open this | Notes |
|---|---|---|
| **88 animated websites** | `Animated Websites/index.html` | Gallery of all 88. Each design is its own website: tap to open, animated card, countdown, Google/Apple calendar, directions, WhatsApp RSVP, share, music. |
| Reference-video website | `Wedding Website/index.html` | Copy of the website in your reference video: mauve envelope, bow, rose card, scratch-to-reveal photo, location. How-to: `Wedding Website/HOW TO USE.txt`. |
| 9 classic websites | `designs.html` | Gallery of 9 envelope-style websites built from your card images (`emerald-jharokha.html`, `firoza.html`, … and `index.html`). |
| 88 designs on one page | `animated-invitations.html` | All 88 animations in one page with a picker. Use this for choosing, not for guests. |

### Changing the details on the 88 websites
The wording, date, venue and WhatsApp number for all 88 are in `Animated Websites/tools/build_sites.py` (the `WEDDING` block at the top). After changing it, run:

```
python "Animated Websites/tools/build_sites.py"
python "Animated Websites/tools/make_thumbs.py"
```

The first rebuilds all 88 sites. The second checks each one in a phone-sized browser and redraws the gallery pictures.
- **RSVP straight to the family:** put the number in `hostWhatsApp`, e.g. `'923001234567'`. While it's empty, the guest picks the chat in WhatsApp.
- **Your own song:** put an mp3 at `Animated Websites/shared/music.mp3`. Without it, a soft built-in tune plays.

### Putting a website online
Upload the whole folder (for example `Animated Websites`) to a free static host such as Netlify Drop (drag the folder onto app.netlify.com/drop) or GitHub Pages. Then send the link of the design you chose. Adding `?guest=Saad%20%26%20Family` to the end of a link puts "Dear Saad & Family" on the opening screen.

## Image cards (pictures to send on WhatsApp or print)

| What | Open this |
|---|---|
| **All image cards, one by one** | `Baraat Card Studio/All Images (one by one)/` (45 pictures) |
| All image cards on one sheet | `Baraat Card Studio/All new designs.jpg` |
| Image card studio (browse and edit) | `Baraat Card Studio/Baraat Card Studio.html` |
| Print-size and WhatsApp-size cards | `Baraat Card Studio/Print/` and `Baraat Card Studio/WhatsApp/` |
| Video end-card designs | `Baraat Card Studio/Video designs (15)/` |
| First image card set | `Baraat Cards/All designs.jpg`, `Baraat Cards/Print/`, `Baraat Cards/WhatsApp/` |

## Card and video tools

| Folder / file | What it is |
|---|---|
| `wedding_invite_studio_fully_customizable.html` | The animated video-card studio (88 designs, editor, video download). The 88 websites are built from this. |
| `studio/` | Source modules and `build.py` that assemble the studio file. |
| `Baraat Card Studio/` | Printable / WhatsApp image cards (40 designs). See its `HOW TO USE.txt`. |
| `Baraat Cards/` | Earlier image card set (`Print/`, `WhatsApp/`, `All designs.jpg`). `work.txt` is the old chat log with Kimi. |
| `Lotus Card Versions/` | Lotus card artwork versions v1–v4. |
| `html2mp4.py`, `Make Video.bat` | Turn an HTML invite into an MP4 video. |
| `for client/` | Zipped studio files prepared for sending. |
| `images/` | The original card photos (`1.jpeg`, `2.jpeg`). |
| `Website Reference/` | The reference video of the website you liked, plus its frames. |
| `backup/` | Older copies of the studio, kept for safety. |
| `baraat_walima_invite_with_colour_pickers.html` | Earlier single invite with colour pickers. |
