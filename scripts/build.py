"""Builds the burkeruder.com photography museum into public/.

    python3 scripts/process.py   # only when curation.json changes (slow)
    python3 scripts/build.py     # HTML from photos.json + the copy below

PREVIEW=True keeps the site out of search engines while it lives on
workers.dev. Flip to False when burkeruder.com points here.
"""
import json, os, html
from datetime import date

PREVIEW = False
SITE = "https://burkeruder.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
photos = json.load(open(os.path.join(ROOT, "scripts/photos.json")))

ROOMS = [
    {
        "key": "austin", "slug": "the-quiet-city", "numeral": "I",
        "title": "The Quiet City", "place": "Downtown Austin, Texas",
        "dek": "Storefronts, sidewalks and the Capitol, with the volume turned down.",
        "wall": [
            "Downtown Austin between people. Storefronts before they open, sidewalks with no one on them, a crosswalk waiting for somebody to need it.",
            "Every street down here seems to end at the Capitol, so it keeps showing up — framed by live oaks, by glass towers, by a stop light. The edit is matte and cool: blacks that never quite go black, highlights rolled off, a little cyan in the shadows. It's the closest thing I have to a signature.",
        ],
        "cover": 11,
    },
    {
        "key": "conroe", "slug": "first-light", "numeral": "II",
        "title": "First Light", "place": "Lake Conroe, Texas",
        "dek": "A morning on the water, from the dark marina to a full table.",
        "wall": [
            "We left Seven Coves Marina before the sun was up, on Captain Scott Yeates's boat, and came back with a table covered in catfish.",
            "In between: the lighthouse going pink, then orange; the long quiet stretches where nobody says much; and the faces of men who have told these stories before and will tell them again.",
        ],
        "cover": 1,
    },
    {
        "key": "faire", "slug": "faire-folk", "numeral": "III",
        "title": "Faire Folk", "place": "Texas Renaissance Festival, Todd Mission",
        "dek": "Everyone decided to be someone else for an afternoon.",
        "wall": [
            "Portraits from a day at the Texas Renaissance Festival, where the rules of the century are loose. Knights in chain mail and sunglasses. A king filming on a gimbal. A wizard taking a phone call.",
        ],
        "cover": 2,
    },
    {
        "key": "cedar", "slug": "newbo-in-july", "numeral": "IV",
        "title": "NewBo, in July", "place": "Cedar Rapids, Iowa",
        "dek": "Signage and small details from a summer walk.",
        "wall": [
            "A walk through Cedar Rapids' NewBo district on a gray July day: the city market's long red roof, a painted piano left out for anyone, bike racks bent into the neighborhood's logo.",
            "Small-town lettering is its own kind of portrait. These are the signs a place puts up when it's telling you who it is.",
        ],
        "cover": 0,
    },
]

STATEMENT = [
    "I photograph what's in front of me: the city I live in, the people I'm with, the places we end up.",
    "This is where that work hangs. There's nothing to book and nothing to buy — just the pictures, arranged the way I'd want you to walk through them.",
]

ABOUT = [
    "Burke Ruder lives in Austin, Texas, with his wife and three kids. He shoots on a Canon EOS R6 Mark II.",
    "Most weekends the camera goes where the family goes — ballfields, lakes, festivals. The street work in <em>The Quiet City</em> is where he found a look he could call his own: matte, cool, patient.",
    "Every photograph here is edited by him in Lightroom.",
]


def esc(s):
    return html.escape(s or "", quote=True)


def nice_date(d):
    if not d:
        return ""
    y, m, dd = map(int, d.split("-"))
    return date(y, m, dd).strftime("%-d %B %Y")


def month_year(items):
    ds = sorted(p["date"] for p in items if p.get("date"))
    if not ds:
        return ""
    a, b = ds[0], ds[-1]
    fa = date(*map(int, a.split("-"))).strftime("%B %Y")
    if a[:7] == b[:7]:
        return nice_date(a) if a == b else fa
    return f"{fa} – {date(*map(int, b.split('-'))).strftime('%B %Y')}"


def settings(p):
    return " · ".join(x for x in (p.get("focal"), p.get("aperture"), p.get("shutter"), p.get("iso")) if x)


def img_tag(p, alt, cls="", eager=False, sizes="(max-width: 900px) 100vw, 80vw"):
    # photos.json holds the small rendition's size (long edge 900); the
    # large one has a 2400 long edge, so scale the width to match.
    big_w = round(p["w"] * 2400 / max(p["w"], p["h"]))
    mid_w = round(p["w"] * 1600 / max(p["w"], p["h"]))
    return (
        f'<img class="{cls}" src="{p["file"]}-m.jpg" srcset="{p["file"]}-s.jpg {p["w"]}w, {p["file"]}-m.jpg {mid_w}w, {p["file"]}.jpg {big_w}w" '
        f'sizes="{sizes}" width="{p["w"]}" height="{p["h"]}" alt="{esc(alt)}" '
        f'{"fetchpriority=high" if eager else "loading=lazy"} decoding="async">'
    )


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">')


def page(path, title, desc, body, og_image, cls="", preload=""):
    canon = SITE + path
    robots = '<meta name="robots" content="noindex, nofollow">' if PREVIEW else '<meta name="robots" content="index, follow">'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#11100e">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Burke Ruder Photographs">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}{og_image}.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="/site.css">
<script>
  // Hide reveal targets until Motion plays them in; fail open after 2.5s.
  if (!matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    document.documentElement.classList.add("m");
    setTimeout(() => {{ if (!window.__motion) document.documentElement.classList.remove("m"); }}, 2500);
  }}
</script>
{preload}
</head>
<body class="{cls}">
{nav(path)}
{body}
{footer()}
<script src="/vendor/motion-14.1.0.js" defer></script>
<script src="/site.js" defer></script>
</body>
</html>
"""


def nav(path):
    def a(href, label):
        cur = ' aria-current="page"' if (path == href or (href != "/" and path.startswith(href))) else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<header class="nav">
  <a class="mark" href="/">Burke Ruder <span>Photographs</span></a>
  <nav>{a("/exhibitions/", "Exhibitions")}{a("/index-of-works/", "Index")}{a("/about/", "About")}</nav>
</header>"""


def footer():
    return f"""<footer class="foot">
  <div class="footin">
    <p class="mark">Burke Ruder <span>Photographs</span></p>
    <p>All photographs © {date.today().year} Burke Ruder. Please ask before using them.</p>
    <p><a href="https://burkeruder.ai">burkeruder.ai</a> — the other things I make</p>
  </div>
</footer>"""


def room_photos(r):
    return photos[r["key"]]


def plate_label(r, i):
    return f"{r['numeral']}.{i:02d}"


# ---------- landing ----------
def landing():
    hero = photos["austin"][0]
    rooms = []
    for r in ROOMS:
        ps = room_photos(r)
        c = ps[r["cover"]]
        rooms.append(f"""
    <a class="room" href="/exhibitions/{r['slug']}/">
      <figure class="roomimg">{img_tag(c, r['title'], sizes="(max-width: 900px) 100vw, 60vw")}</figure>
      <div class="roomtext">
        <p class="label">Gallery {r['numeral']}</p>
        <h3 style="view-transition-name: t-{r['slug']}">{esc(r['title'])}</h3>
        <p class="dek">{esc(r['dek'])}</p>
        <p class="meta">{esc(r['place'])}<br>{esc(month_year(ps))} · {len(ps)} photographs</p>
        <span class="enter">Enter the gallery <span aria-hidden="true">→</span></span>
      </div>
    </a>""")
    total = sum(len(room_photos(r)) for r in ROOMS)
    body = f"""
<section class="hero">
  <div class="heroframe">{img_tag(hero, "The Texas Capitol at the end of Congress Avenue, framed by live oaks", "heroimg", eager=True, sizes="100vw")}</div>
  <div class="vignette"></div><div class="grain"></div>
  <div class="herotext">
    <h1>Burke Ruder</h1>
    <p class="label light">Photographs · Austin, Texas</p>
  </div>
  <a class="scrollcue" href="#entrance" aria-label="Scroll to the entrance">↓</a>
</section>

<section class="entrance" id="entrance">
  <p class="label">At the entrance</p>
  <div class="statement">{''.join(f'<p>{esc(p)}</p>' for p in STATEMENT)}</div>
  <p class="sig">— Burke</p>
</section>

<section class="rooms" id="exhibitions">
  <div class="roomshead">
    <p class="label">Now showing</p>
    <h2>Four galleries, {total} photographs</h2>
  </div>
  {''.join(rooms)}
</section>"""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Person", "@id": SITE + "/#burke", "name": "Burke Ruder", "jobTitle": "Photographer",
         "address": {"@type": "PostalAddress", "addressLocality": "Austin", "addressRegion": "TX", "addressCountry": "US"},
         "url": SITE, "sameAs": ["https://burkeruder.ai"]},
        {"@type": "WebSite", "name": "Burke Ruder Photographs", "url": SITE, "author": {"@id": SITE + "/#burke"}},
    ] + [{"@type": "ImageGallery", "name": r["title"], "url": f"{SITE}/exhibitions/{r['slug']}/",
          "description": r["dek"], "contentLocation": r["place"], "author": {"@id": SITE + "/#burke"},
          "image": f"{SITE}{room_photos(r)[r['cover']]['file']}.jpg"} for r in ROOMS]}
    body += f'\n<script type="application/ld+json">{json.dumps(ld)}</script>'
    return page("/", "Burke Ruder — Photographs",
                "The photography of Burke Ruder: street work from downtown Austin, mornings on Lake Conroe, portraits from the Texas Renaissance Festival, and more.",
                body, hero["file"], "home",
                preload=f'<link rel="preload" as="image" href="{hero["file"]}-m.jpg" imagesrcset="{hero["file"]}-s.jpg {hero["w"]}w, {hero["file"]}-m.jpg {round(hero["w"]*1600/max(hero["w"],hero["h"]))}w, {hero["file"]}.jpg {round(hero["w"]*2400/max(hero["w"],hero["h"]))}w" imagesizes="100vw" fetchpriority="high">')


# ---------- exhibitions index ----------
def exhibitions():
    items = []
    for r in ROOMS:
        ps = room_photos(r)
        items.append(f"""
  <a class="exitem" href="/exhibitions/{r['slug']}/">
    <figure>{img_tag(ps[r['cover']], r['title'], sizes="(max-width: 900px) 100vw, 45vw")}</figure>
    <p class="label">Gallery {r['numeral']} · {len(ps)} photographs</p>
    <h3 style="view-transition-name: t-{r['slug']}">{esc(r['title'])}</h3>
    <p class="meta">{esc(r['place'])} · {esc(month_year(ps))}</p>
  </a>""")
    body = f"""
<main class="wrap">
  <header class="pagehead">
    <p class="label">Exhibitions</p>
    <h1>Now showing</h1>
  </header>
  <div class="exgrid">{''.join(items)}</div>
</main>"""
    return page("/exhibitions/", "Exhibitions — Burke Ruder Photographs",
                "Four galleries of photographs by Burke Ruder.", body, photos["austin"][0]["file"])


# ---------- a gallery ----------
def hang(r):
    """Sequence the room: landscapes hang wide, two portraits in a row hang
    as a pair, a lone portrait hangs tall and centered."""
    ps = room_photos(r)
    out, i = [], 0
    def fig(p, n, cls):
        alt = f"{r['title']}, plate {plate_label(r, n)}. {r['place']}."
        return f"""<figure class="plate {cls}" id="p{n}" data-n="{n}">
      <button class="open" aria-label="View plate {plate_label(r, n)} larger">{img_tag(p, alt, sizes='(max-width: 900px) 100vw, 70vw')}</button>
      <figcaption><span class="no">{plate_label(r, n)}</span><span class="set">{esc(settings(p))}</span></figcaption>
    </figure>"""
    while i < len(ps):
        p = ps[i]
        portrait = p["h"] > p["w"]
        nxt = ps[i + 1] if i + 1 < len(ps) else None
        if portrait and nxt and nxt["h"] > nxt["w"]:
            out.append(f'<div class="pair">{fig(p, i + 1, "")}{fig(nxt, i + 2, "")}</div>')
            i += 2
            continue
        out.append(fig(p, i + 1, "tall" if portrait else "wide"))
        i += 1
    return "\n    ".join(out)


def gallery(idx):
    r = ROOMS[idx]
    ps = room_photos(r)
    nxt = ROOMS[(idx + 1) % len(ROOMS)]
    def srcset(p):
        k = max(p["w"], p["h"])
        return f'{p["file"]}-s.jpg {p["w"]}w, {p["file"]}-m.jpg {round(p["w"] * 1600 / k)}w, {p["file"]}.jpg {round(p["w"] * 2400 / k)}w'
    lb = json.dumps([{"src": p["file"] + "-m.jpg", "srcset": srcset(p), "w": p["w"], "h": p["h"], "no": plate_label(r, n),
                      "cap": r["place"] + (", " + nice_date(p.get("date")) if p.get("date") else ""),
                      "set": settings(p)} for n, p in enumerate(ps, 1)])
    body = f"""
<main>
  <section class="wall">
    <p class="label">Gallery {r['numeral']}</p>
    <h1 style="view-transition-name: t-{r['slug']}">{esc(r['title'])}</h1>
    <p class="meta">{esc(r['place'])} · {esc(month_year(ps))} · {len(ps)} photographs</p>
    <div class="walltext">{''.join(f'<p>{p}</p>' for p in r['wall'])}</div>
  </section>
  <section class="hang">
    {hang(r)}
  </section>
  <nav class="nextroom">
    <p class="label">Next gallery · {nxt['numeral']}</p>
    <a href="/exhibitions/{nxt['slug']}/"><span>{esc(nxt['title'])}</span> <span aria-hidden="true">→</span></a>
  </nav>
</main>
<dialog class="lightbox" aria-label="Photograph viewer">
  <button class="lbclose" aria-label="Close">Close</button>
  <button class="lbprev" aria-label="Previous photograph">←</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lbnext" aria-label="Next photograph">→</button>
</dialog>
<script type="application/json" id="plates">{lb}</script>"""
    return page(f"/exhibitions/{r['slug']}/", f"{r['title']} — Burke Ruder Photographs",
                f"{r['title']}: {r['dek']} {len(ps)} photographs by Burke Ruder, {r['place']}.",
                body, ps[r["cover"]]["file"], "exhibit")


# ---------- index of works ----------
def index_of_works():
    blocks = []
    for r in ROOMS:
        ps = room_photos(r)
        thumbs = "".join(
            f'<a href="/exhibitions/{r["slug"]}/#p{n}" class="thumb"><img src="{p["file"]}-s.jpg" width="{p["w"]}" height="{p["h"]}" alt="Plate {plate_label(r, n)}" loading="lazy" decoding="async"><span>{plate_label(r, n)}</span></a>'
            for n, p in enumerate(ps, 1))
        blocks.append(f"""
  <section class="iw">
    <h2><span class="label">Gallery {r['numeral']}</span> <a href="/exhibitions/{r['slug']}/">{esc(r['title'])}</a></h2>
    <div class="thumbs">{thumbs}</div>
  </section>""")
    body = f"""
<main class="wrap">
  <header class="pagehead">
    <p class="label">Index of works</p>
    <h1>Every photograph on view</h1>
  </header>
  {''.join(blocks)}
</main>"""
    return page("/index-of-works/", "Index of Works — Burke Ruder Photographs",
                "Every photograph currently on view, by gallery.", body, photos["austin"][0]["file"])


# ---------- about ----------
def about():
    p = photos["conroe"][0]
    body = f"""
<main class="wrap about">
  <header class="pagehead">
    <p class="label">About</p>
    <h1>The photographer</h1>
  </header>
  <div class="aboutgrid">
    <figure>{img_tag(p, "Boat slips on Lake Conroe at sunrise", sizes="(max-width: 900px) 100vw, 40vw")}</figure>
    <div class="abouttext">
      {''.join(f'<p>{x}</p>' for x in ABOUT)}
      <div class="elsewhere">
        <p class="label">Elsewhere</p>
        <p>When he isn't behind a camera, Burke builds things with AI. That work lives at <a href="https://burkeruder.ai">burkeruder.ai</a>.</p>
      </div>
    </div>
  </div>
</main>"""
    return page("/about/", "About — Burke Ruder Photographs",
                "Burke Ruder is a photographer in Austin, Texas.", body, photos["austin"][0]["file"])


def write(path, s):
    full = os.path.join(PUB, path.lstrip("/"), "index.html") if path.endswith("/") else os.path.join(PUB, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(s)


write("/", landing())
write("/exhibitions/", exhibitions())
for i, r in enumerate(ROOMS):
    write(f"/exhibitions/{r['slug']}/", gallery(i))
write("/index-of-works/", index_of_works())
write("/about/", about())

urls = ["/", "/exhibitions/", "/index-of-works/", "/about/"] + [f"/exhibitions/{r['slug']}/" for r in ROOMS]
write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
write("/robots.txt", "User-agent: *\nDisallow: /\n" if PREVIEW else f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("built", len(urls), "pages", "(PREVIEW)" if PREVIEW else "")
