"""Baut die neuen Blogbeiträge und die Blog-Übersicht in das OZ-Repo ein.
Aufruf: python3 build.py <repo-pfad>   (idempotent)"""
import sys, os, re, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artikel import ARTIKEL

REPO = sys.argv[1]
P = lambda *a: os.path.join(REPO, *a)
lies = lambda p: open(p, encoding="utf-8").read()
def schreib(p, t):
    open(p, "w", encoding="utf-8").write(t)

vorlage = lies(P("blog", "strategieplanung-ki.html"))
STIL = vorlage[vorlage.index('    <link rel="stylesheet" href="../fonts/'):vorlage.index("    </style>")]
STIL += ("        article p a, article li a { color: var(--accent-cyan); text-decoration: none;"
         " border-bottom: 1px solid var(--accent-cyan-dim); }\n"
         "        article p a:hover, article li a:hover { color: #33ddff; }\n"
         "        .post-liste { list-style: none; margin: 0 !important; }\n"
         "        .post-liste li { border-bottom: 1px solid var(--border); padding: 1.4rem 0; margin: 0; }\n"
         "        .post-liste .datum { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;"
         " color: var(--text-dim); letter-spacing: 0.08em; text-transform: uppercase; }\n"
         "        .post-liste h2 { margin: 0.3rem 0 0.4rem; font-size: 1.25rem; }\n"
         "        .post-liste h2 a { color: var(--text-primary); text-decoration: none; }\n"
         "        .post-liste h2 a:hover { color: var(--accent-cyan); }\n"
         "        .post-liste p { margin: 0; font-size: 1rem; }\n"
         "        .video-player { margin: 0 0 2rem; }\n"
         "        .video-player video { width: 100%; aspect-ratio: 16 / 9; background: #000; border-radius: 6px;"
         " border: 1px solid var(--border); display: block; }\n"
         "        .video-player figcaption { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;"
         " color: var(--text-dim); margin-top: 0.6rem; }\n"
         "        .kapitel { list-style: none; margin: 0 0 2rem !important; columns: 2; column-gap: 2rem; }\n"
         "        .kapitel li { margin: 0 0 0.4rem; break-inside: avoid; }\n"
         "        .kapitel a { border: 0 !important; }\n"
         "        .kapitel .zeit { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--text-dim);"
         " display: inline-block; width: 3.2rem; }\n"
         "        @media (max-width: 600px) { .kapitel { columns: 1; } }\n"
         "    </style>\n")

NAV = """<nav>
    <a href="../index.html" class="nav-logo">OPERATION<span>::ZUKUNFT</span></a>
    <button class="nav-toggle" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menü">☰</button>
    <ul class="nav-links">
        <li><a href="../index.html#angebote">Angebote</a></li>
        <li><a href="../cluster.html">Das Cluster</a></li>
        <li><a href="./">Blog</a></li>
        <li><a href="../index.html#kontakt">Kontakt</a></li>
    </ul>
</nav>"""

FUSS = """<footer>
    <div class="footer-links">
        <a href="../index.html#impressum">Impressum</a>
        <a href="https://pillkahn.de/">Ein Projekt von Prof. Dr. Ulf Pillkahn</a>
    </div>
    <p class="footer-copy">© 2026 Prof. Dr. Ulf Pillkahn · Operation Zukunft</p>
</footer>"""

def seite(title, desc, inhalt):
    e = lambda t: html.escape(t, quote=True)
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{e(title)}</title>
    <meta name="description" content="{e(desc)}">
    <meta name="robots" content="index, follow">

{STIL}</head>
<body>

<div class="grid-bg"></div>

{NAV}

{inhalt}

{FUSS}

<script src="../track.js?v=2026-11-12" defer></script>
</body>
</html>
"""

def lesezeit(body):
    return max(3, round(len(re.sub(r"<[^>]+>", " ", body).split()) / 200))

# 1. Artikelseiten
for a in ARTIKEL:
    cta_text, cta_link, cta_label = a["cta"]
    ziel = ' target="_blank" rel="noopener"' if cta_link.startswith("http") else ""
    inhalt = f"""<article>
    <div class="article-meta">
        <a href="./">← Blog</a> &nbsp;·&nbsp; {a['label']} &nbsp;·&nbsp; {lesezeit(a['body'])} Min. Lesezeit
    </div>

    <h1>{a['h1']}</h1>
{a['body'].rstrip()}

    <div class="article-cta">
        <p>{cta_text}</p>
        <a href="{cta_link}"{ziel}>{html.escape(cta_label, quote=False)}</a>
    </div>

    <a href="./" class="back-link">← Alle Beiträge</a>
</article>"""
    schreib(P("blog", a["slug"] + ".html"), seite(a["title"], a["desc"], inhalt))

# 2. posts.js: neue Einträge vor die alten, vorhandene nicht doppeln
pj = lies(P("posts.js"))
alt_js = pj[pj.index("const posts = [") + len("const posts = ["):pj.rindex("];")]
neu = ""
for a in sorted(ARTIKEL, key=lambda a: a["datum"], reverse=True):
    url = f"blog/{a['slug']}.html"
    if url in alt_js:
        continue
    neu += ("\n    {\n"
            f'        titel: {json.dumps(a["kurz"], ensure_ascii=False)},\n'
            f'        datum: "{a["datum"]}",\n'
            f'        teaser: {json.dumps(a["teaser"], ensure_ascii=False)},\n'
            f'        url: "{url}"\n'
            "    },")
pj = pj.replace("const posts = [", "const posts = [" + neu, 1)
schreib(P("posts.js"), pj)

# Alle Einträge (für Übersicht, posts.json, Sitemap, noscript)
array = pj[pj.index("const posts = ["):]
eintraege = re.findall(r'titel:\s*"([^"\n]*)",\s*datum:\s*"([^"\n]*)",\s*teaser:\s*"([^"\n]*)",\s*url:\s*"([^"\n]*)"', array)
eintraege = sorted(eintraege, key=lambda e: e[1], reverse=True)
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"]
label = lambda d: f"{MONATE[int(d[5:7]) - 1]} {d[:4]}"

schreib(P("posts.json"), json.dumps(
    [{"title": t, "url": u, "date": d, "label": label(d), "teaser": te} for t, d, te, u in eintraege],
    ensure_ascii=False, indent=4) + "\n")

# 3. Blog-Übersicht
liste = "\n".join(
    f"""        <li>
            <span class="datum">{label(d)}</span>
            <h2><a href="{u.replace('blog/', '')}">{html.escape(t, quote=False)}</a></h2>
            <p>{html.escape(te, quote=False)}</p>
        </li>""" for t, d, te, u in eintraege)
schreib(P("blog", "index.html"), seite(
    "Blog: Foresight, Szenarien, KI-Agenten | Operation Zukunft",
    "Beiträge zu Corporate Foresight, Szenarioentwicklung, Innovationsmanagement und KI-Agenten "
    "von Prof. Dr. Ulf Pillkahn.",
    f"""<article>
    <div class="article-meta"><a href="../index.html">← Startseite</a></div>

    <h1>Blog: Foresight, Szenarien und KI-Agenten</h1>

    <p>Beiträge zu Corporate Foresight, Szenarioentwicklung, Innovationsmanagement und KI-Agenten – recherchiert im <a href="../cluster.html">Agenten-Cluster</a> von Operation Zukunft.</p>

    <ul class="post-liste">
{liste}
    </ul>
</article>"""))

# 4. Alte Beiträge: tote Anker reparieren
for f in os.listdir(P("blog")):
    if not f.endswith(".html") or f == "index.html":
        continue
    t = lies(P("blog", f))
    t2 = (t.replace('<a href="../index.html#buch">Buch</a>', '<a href="../index.html#publikationen">Buch</a>')
           .replace('href="../index.html#blog"', 'href="./"'))
    if "track.js" not in t2:
        t2 = t2.replace("</body>", '<script src="../track.js?v=2026-11-12" defer></script>\n</body>', 1)
    if t2 != t:
        schreib(P("blog", f), t2)

# 5. Sitemap: Blog-Block neu
sm = lies(P("sitemap.xml"))
block = "  <!-- Blogbeitraege (lastmod = Publikationsdatum aus posts.js) -->\n"
block += "  <url>\n    <loc>https://operation-zukunft.de/blog/</loc>\n" \
         f"    <lastmod>{eintraege[0][1]}</lastmod>\n  </url>\n"
for t, d, te, u in eintraege:
    block += f"  <url>\n    <loc>https://operation-zukunft.de/{u}</loc>\n    <lastmod>{d}</lastmod>\n  </url>\n"
sm = re.sub(r"  <!-- Blogbeitraege.*?(?=\n  <!-- Indexierbares)", block.rstrip("\n") + "\n", sm, flags=re.S)
schreib(P("sitemap.xml"), sm)

# 6. noscript-Liste auf der Startseite
ix = lies(P("index.html"))
lis = "\n".join(f'            <li><a href="{u}">{html.escape(t, quote=False)}</a></li>' for t, d, te, u in eintraege)
lis += '\n            <li><a href="blog/">Alle Beiträge</a></li>'
ix = re.sub(r'(<ul class="sidebar-static">\n).*?(\n[ \t]*</ul>)', lambda m: m.group(1) + lis + m.group(2), ix, flags=re.S)
schreib(P("index.html"), ix)

# 7. seo.py: SEITEN-Einträge ergänzen
sp = lies(P("pflege", "seo.py"))
zusatz = ""
if '"blog/index.html"' not in sp:
    zusatz += ('    {"datei": "blog/index.html", "pfad": "/blog/", "title": None, "desc": None,\n'
               '     "og": "website", "bild": HERO, "art": "seite"},\n')
for a in ARTIKEL:
    if f'"blog/{a["slug"]}.html"' in sp:
        continue
    zusatz += (f'    {{"datei": "blog/{a["slug"]}.html", "veroeffentlicht": "{a["datum"]}",\n'
               f'     "title": None, "desc": None}},\n')
if zusatz:
    sp = sp.replace('\n]\nfor s in SEITEN:', '\n' + zusatz + ']\nfor s in SEITEN:', 1)
    assert zusatz in sp, "seo.py-Anker nicht gefunden"
    schreib(P("pflege", "seo.py"), sp)

print(len(ARTIKEL), "Artikel,", len(eintraege), "Einträge gesamt")
