#!/usr/bin/env python3
"""
pflege/videos/build.py — Mediathek „Foresight erklärt“ für operation-zukunft.de

Datenquelle:
  pflege/videos/reihe.json                 Reihenfolge und Arbeitstitel aller Filme
  pflege/videos/filme/<slug>/film.json     ein Datensatz je VERÖFFENTLICHTEM Film
  pflege/videos/filme/<slug>/transkript.md Transkript, je Kapitel ein „## Überschrift“

Erzeugt bzw. pflegt (idempotent, ein zweiter Lauf ändert nichts):
  videos/<slug>/index.html      Videoseite je veröffentlichtem Film
  videos/index.html             Übersicht der Reihe
  videos/_vorlage/index.html    Vorlage mit Platzhaltern (noindex, nicht verlinkt)
  video-sitemap.xml             Video-Sitemap nach Google-Schema
  sitemap.xml                   Block zwischen <!-- Videos … --> und <!-- /Videos -->
  robots.txt                    zweite Sitemap-Zeile
  llms.txt                      Abschnitt „## Videos“
  index.html                    Startseitenabschnitt zwischen MEDIATHEK-Markern
  <alte_url>                    schlanke Weiterleitungsseite, falls ein Film
                                vorher anderswo stand (Feld alte_url)

Menü und Footer der Videoseiten werden aus cluster.html übernommen, damit sie
mit dem Rest der Website übereinstimmen.

Aufruf im Repo-Root:   python3 pflege/videos/build.py
Danach prüfen:         python3 pflege/videos/pruefen.py
"""

import html
import json
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, os.path.join(REPO, "pflege"))
import seo  # noqa: E402  (Kanon: PERSON, ORG, SITE, @ids, CSS-Version)

DOMAIN = seo.DOMAIN
REIHE_ID = DOMAIN + "/videos/#reihe"
UEBERSICHT_URL = DOMAIN + "/videos/"
UEBERSICHT_STAND = "2026-11-20"

e = lambda t: html.escape(str(t), quote=True)


def P(*a):
    return os.path.join(REPO, *a)


def lies(p):
    return open(p, encoding="utf-8").read()


def schreib(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    alt = lies(p) if os.path.exists(p) else None
    if alt != t:
        open(p, "w", encoding="utf-8").write(t)
        print("  geschrieben:", os.path.relpath(p, REPO))


# ------------------------------------------------------------------ Daten
REIHE = json.load(open(os.path.join(HIER, "reihe.json"), encoding="utf-8"))


def lade_film(slug):
    d = os.path.join(HIER, "filme", slug)
    if not os.path.exists(os.path.join(d, "film.json")):
        return None
    f = json.load(open(os.path.join(d, "film.json"), encoding="utf-8"))
    f["slug"] = slug
    f["url"] = f"{DOMAIN}/videos/{slug}/"
    abschnitte = []
    for block in re.split(r"^## ", lies(os.path.join(d, "transkript.md")), flags=re.M):
        if not block.strip():
            continue
        kopf, _, rest = block.partition("\n")
        absaetze = [re.sub(r"\s+", " ", a).strip() for a in rest.strip().split("\n\n") if a.strip()]
        abschnitte.append((kopf.strip(), absaetze))
    f["transkript"] = abschnitte
    return f


FILME_ALLE = REIHE["filme"]
for eintrag in FILME_ALLE:
    eintrag["film"] = lade_film(eintrag["slug"])
VEROEFFENTLICHT = [x["film"] for x in FILME_ALLE if x["film"]]
GEPLANT = [x for x in FILME_ALLE if not x["film"]]


# ------------------------------------------------------------------ Helfer
def mmss(s):
    if isinstance(s, str):
        return s
    return f"{s // 60}:{s % 60:02d}"


def iso_dauer(s):
    if isinstance(s, str):
        return s
    m, sek = divmod(s, 60)
    return f"PT{m}M{sek}S" if m else f"PT{sek}S"


def text(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t))).strip()


# Menü und Footer aus cluster.html, Links auf Wurzelpfade umgestellt
def _aus_cluster(tag):
    c = lies(P("cluster.html"))
    return re.search(rf"<{tag}\b.*?</{tag}>", c, re.S).group(0)


def wurzelpfade(t):
    t = re.sub(r'href="index\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1) or ""}"', t)
    t = re.sub(r'href="(cluster|datenschutz|szenariofilme|strategie-pakete)\.html"', r'href="/\1.html"', t)
    t = t.replace('href="videos/"', 'href="/videos/"')
    # Leitseiten und andere Verzeichnisse: "slug/" → "/slug/"
    t = re.sub(r'href="([a-z0-9][a-z0-9-]*/)"', r'href="/\1"', t)
    return t


def menue(aktuell_videos=True):
    n = wurzelpfade(_aus_cluster("nav"))
    n = n.replace(' aria-current="page"', "")
    if aktuell_videos:
        n = n.replace('href="/videos/"', 'href="/videos/" aria-current="page"', 1)
    return n


def fuss():
    return wurzelpfade(_aus_cluster("footer"))


def jsonld(knoten):
    daten = {"@context": "https://schema.org", "@graph": knoten}
    t = json.dumps(daten, ensure_ascii=False, indent=2)
    t = "\n".join("    " + z for z in t.splitlines())
    return ('    <!-- Strukturdaten: generiert von pflege/videos/build.py -->\n'
            '    <script type="application/ld+json">\n' + t + '\n    </script>\n')


def seite(kopf, inhalt, skript=""):
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
{kopf}
    <link rel="stylesheet" href="/style.css?v={seo.CSS_VERSION}">
</head>
<body>

<!-- Kino-Ebenen: feines Raster, Film-Grain, Vignette -->
<div class="grid-bg" aria-hidden="true"></div>
<div class="film-grain" aria-hidden="true"></div>
<div class="vignette" aria-hidden="true"></div>

<!-- ===================== NAVIGATION ===================== -->
{menue()}

<!-- ===================== INHALT (generiert von pflege/videos/build.py) ===================== -->
{inhalt}

<!-- ===================== FOOTER & IMPRESSUM ===================== -->
{fuss()}
{skript}
<!-- Seitenverhalten -->
<script src="/main.js?v=2026-11-12"></script>
<!-- Besucherzähler (eigener Zähler auf pillkahn.de, siehe track.js) -->
<script src="/track.js?v=2026-11-12" defer></script>

</body>
</html>
"""


def kopf_meta(title, desc, url, robots, og_typ, bild, bild_b, bild_h, bild_alt, video=None):
    z = [
        f'    <title>{e(title)}</title>',
        f'    <meta name="description" content="{e(desc)}">',
        f'    <meta name="robots" content="{robots}">',
        f'    <link rel="canonical" href="{url}">',
        f'    <meta property="og:type" content="{og_typ}">',
        '    <meta property="og:site_name" content="Operation Zukunft">',
        '    <meta property="og:locale" content="de_DE">',
        f'    <meta property="og:url" content="{url}">',
        f'    <meta property="og:title" content="{e(title)}">',
        f'    <meta property="og:description" content="{e(desc)}">',
        f'    <meta property="og:image" content="{bild}">',
        f'    <meta property="og:image:width" content="{bild_b}">',
        f'    <meta property="og:image:height" content="{bild_h}">',
        f'    <meta property="og:image:alt" content="{e(bild_alt)}">',
    ]
    if video:
        z += [
            f'    <meta property="og:video" content="{video}">',
            f'    <meta property="og:video:secure_url" content="{video}">',
            '    <meta property="og:video:type" content="video/mp4">',
        ]
    z += [
        '    <meta name="twitter:card" content="summary_large_image">',
        '    <meta name="twitter:creator" content="@Ulf_Pillkahn">',
        f'    <meta name="twitter:title" content="{e(title)}">',
        f'    <meta name="twitter:description" content="{e(desc)}">',
        f'    <meta name="twitter:image" content="{bild}">',
        f'    <meta name="twitter:image:alt" content="{e(bild_alt)}">',
    ]
    return "\n".join(z)


SERIE_KURZ = {"@type": "CreativeWorkSeries", "@id": REIHE_ID,
              "name": REIHE["name"], "url": UEBERSICHT_URL}


def video_objekt(f):
    url = f["url"]
    starts = [k[0] for k in f["kapitel"]]
    clips = []
    for i, (t, name) in enumerate(f["kapitel"]):
        ende = starts[i + 1] if i + 1 < len(starts) else f["dauer_sekunden"]
        clips.append({"@type": "Clip", "name": name, "startOffset": t, "endOffset": ende,
                      "url": f"{url}?t={t}"})
    return {
        "@type": "VideoObject",
        "@id": url + "#video",
        "name": f["name"],
        "description": f["beschreibung"],
        "thumbnailUrl": DOMAIN + f["poster"],
        "uploadDate": f["upload_date"],
        "duration": iso_dauer(f["dauer_sekunden"]),
        "contentUrl": f["mp4"],
        "embedUrl": f"https://www.youtube.com/embed/{f['youtube_id']}",
        "sameAs": f"https://www.youtube.com/watch?v={f['youtube_id']}",
        "inLanguage": "de",
        "transcript": " ".join(" ".join(a) for _, a in f["transkript"]),
        "creator": {"@id": seo.PERSON_ID},
        "author": {"@id": seo.PERSON_ID},
        "publisher": {"@id": seo.ORG_ID},
        "isPartOf": {"@id": REIHE_ID},
        "mainEntityOfPage": {"@id": url + "#webpage"},
        "hasPart": clips,
    }


# ------------------------------------------------------------------ Videoseite
SPRUNG_SKRIPT = """
<script>
/* Kapitel und ?t=Sekunden springen im eigenen Player an die Stelle
   (die Clip-Adressen in den Strukturdaten nutzen genau dieses Muster).
   preload="none": Beim Klick startet play() das Laden, die Zeit wird
   gesetzt, sobald die Metadaten da sind. */
(function () {
    var v = document.getElementById('video');
    if (!v) return;
    function springe(s, abspielen) {
        if (v.readyState >= 1) {
            v.currentTime = s;
            if (abspielen) v.play().catch(function () {});
            return;
        }
        v.addEventListener('loadedmetadata', function () { v.currentTime = s; }, { once: true });
        if (abspielen) { v.play().catch(function () {}); }
        else { v.preload = 'metadata'; v.load(); }
    }
    var t = parseInt(new URLSearchParams(location.search).get('t'), 10);
    if (t > 0) { springe(t, false); v.scrollIntoView({ block: 'center' }); }
    document.querySelectorAll('.kapitel a[data-t]').forEach(function (a) {
        a.addEventListener('click', function (ev) {
            ev.preventDefault();
            springe(parseInt(a.getAttribute('data-t'), 10), true);
            v.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    });
})();
</script>
"""


def weiter_in_der_reihe(f):
    andere = [x for x in VEROEFFENTLICHT if x["slug"] != f["slug"]]
    z = []
    if andere:
        z.append('    <ul class="reihe-liste">')
        for x in andere:
            z.append(f'        <li><a href="/videos/{x["slug"]}/">{e(x["titel"])}</a>'
                     f' <span class="reihe-dauer">{mmss(x["dauer_sekunden"])} Min.</span></li>')
        z.append('    </ul>')
    if GEPLANT:
        z.append(f'    <p class="reihe-naechstes">Als Nächstes: {e(GEPLANT[0]["titel"])}</p>')
    z.append('    <p><a href="/videos/" class="reihe-alle">Alle Videos der Reihe „'
             + e(REIHE["name"]) + '“ →</a></p>')
    return "\n".join(z)


def videoseite(f, vorlage=False):
    url = f["url"]
    kapitel = "\n".join(
        f'        <li><a href="?t={t}" data-t="{t}"><span class="zeit">{mmss(t)}</span> {e(n)}</a></li>'
        for t, n in f["kapitel"])
    transkript = "\n".join(
        f'    <h3>{e(h)}</h3>\n' + "\n".join(f"    <p>{e(a)}</p>" for a in ps)
        for h, ps in f["transkript"])
    worum = " ".join(f["worum_es_geht"])
    weiterlesen = ""
    if f.get("weiterlesen"):
        # Satz/Sätze als HTML aus film.json, Bücher nur als Verweis (seo.BUCH)
        weiterlesen = f"""
    <aside class="video-weiterlesen">
        <h2>Zum Weiterlesen</h2>
        <p>{f["weiterlesen"]["text"]}</p>
    </aside>
"""
    quelle = (f' <span class="video-quelle">({e(f["antwort_quelle"])})</span>'
              if f.get("antwort_quelle") else "")
    inhalt = f"""<main class="mediathek video-seite">
    <nav class="brotkrumen" aria-label="Brotkrumen">
        <a href="/videos/">Videos</a> <span aria-hidden="true">›</span> <span aria-current="page">{e(f["titel"])}</span>
    </nav>

    <h1 class="video-titel">{e(f["titel"])}</h1>

    <figure class="video-player">
        <video id="video" controls preload="none" playsinline width="{f["poster_breite"]}" height="{f["poster_hoehe"]}" poster="{f["poster"]}">
            <source src="{f["mp4"]}" type="video/mp4">
            <track kind="subtitles" srclang="de" label="Deutsch" src="{f["vtt"]}">
        </video>
    </figure>

    <p class="video-antwort">{f["antwort"]}{quelle}</p>

    <p class="video-meta">{mmss(f["dauer_sekunden"])} Min. · Untertitel im Player zuschaltbar · <a href="https://www.youtube.com/watch?v={f["youtube_id"]}" rel="noopener" data-track="video-youtube">Auf YouTube ansehen</a></p>

    <h2>Kapitel</h2>
    <ol class="kapitel">
{kapitel}
    </ol>

    <h2>Worum es geht</h2>
    <p>{e(worum)}</p>
{weiterlesen}
    <h2 id="transkript">Transkript</h2>
{transkript}

    <h2>Weiter in der Reihe</h2>
{weiter_in_der_reihe(f)}

    <div class="video-cta">
        <p>{e(f["cta_text"])}</p>
        <a href="{f["cta_link"]}" class="btn btn-primary" data-track="video-cta">{e(f["cta_label"])}</a>
    </div>
</main>"""

    knoten = [seo.PERSON, seo.ORG, seo.SITE,
              {
                  "@type": "WebPage",
                  "@id": url + "#webpage",
                  "url": url,
                  "name": f["seitentitel"],
                  "description": f["meta_description"],
                  "inLanguage": "de-DE",
                  "isPartOf": {"@id": seo.SITE_ID},
                  "mainEntity": {"@id": url + "#video"},
                  "primaryImageOfPage": {"@type": "ImageObject", "url": DOMAIN + f["poster"],
                                         "width": f["poster_breite"], "height": f["poster_hoehe"]},
                  "breadcrumb": {"@id": url + "#breadcrumb"},
                  "author": {"@id": seo.PERSON_ID},
                  "publisher": {"@id": seo.ORG_ID},
                  "datePublished": f["upload_date"],
                  "dateModified": f["seite_stand"],
                  **({"citation": seo.buecher(*f["weiterlesen"]["buecher"])}
                     if f.get("weiterlesen") else {}),
              },
              video_objekt(f),
              SERIE_KURZ,
              {
                  "@type": "BreadcrumbList",
                  "@id": url + "#breadcrumb",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Startseite", "item": DOMAIN + "/"},
                      {"@type": "ListItem", "position": 2, "name": "Videos", "item": UEBERSICHT_URL},
                      {"@type": "ListItem", "position": 3, "name": f["titel"], "item": url},
                  ],
              }]
    robots = "noindex, nofollow" if vorlage else "index, follow"
    kopf = kopf_meta(f["seitentitel"], f["meta_description"], url, robots, "video.other",
                     DOMAIN + f["poster"], f["poster_breite"], f["poster_hoehe"], f["titel"],
                     video=f["mp4"])
    if vorlage:
        kopf = ("    <!-- VORLAGE: wird von pflege/videos/build.py erzeugt und nicht veröffentlicht.\n"
                "         Neue Filme NICHT hier eintragen, sondern in pflege/videos/filme/<slug>/\n"
                "         (siehe videos/NEUER-FILM.md). -->\n" + kopf)
    return seite(kopf + "\n" + jsonld(knoten), inhalt, SPRUNG_SKRIPT)


# ------------------------------------------------------------------ Übersicht
UEBERSICHT_TITLE = "Foresight erklärt – Videos | Operation Zukunft"
UEBERSICHT_DESC = ("Videoreihe „Foresight erklärt“: Prof. Dr. Ulf Pillkahn erklärt Zukunftsforschung, "
                   "Szenarien, Trends und KI im Foresight – mit Kapiteln und Transkript.")
UEBERSICHT_EINLEITUNG = (
    "In der Reihe „Foresight erklärt“ erklärt Prof. Dr. Ulf Pillkahn in kurzen Videos, wie "
    "Zukunftsforschung und Corporate Foresight arbeiten: von den Grundlagen über Szenarien und "
    "Trends bis zur Rolle von KI. Für Führungskräfte, Strategie- und Innovationsteams, die "
    "Zukunftsfragen methodisch angehen wollen. Jedes Video hat Kapitel, Untertitel und ein "
    "vollständiges Transkript.")


def uebersicht():
    karten = "\n".join(f"""        <li>
            <a class="film-karte" href="/videos/{f["slug"]}/">
                <span class="film-bild">
                    <img src="{f["poster"]}" alt="" width="{f["poster_breite"]}" height="{f["poster_hoehe"]}" loading="lazy">
                    <span class="film-dauer">{mmss(f["dauer_sekunden"])}</span>
                </span>
                <span class="film-nr">Folge {next(x["nr"] for x in FILME_ALLE if x["slug"] == f["slug"])}</span>
                <h2>{e(f["titel"])}</h2>
                <p>{e(f["karte"])}</p>
            </a>
        </li>""" for f in VEROEFFENTLICHT)
    vorbereitung = (f'    <p class="in-vorbereitung">In Vorbereitung: '
                    + " · ".join(e(x["titel"]) for x in GEPLANT) + "</p>") if GEPLANT else ""
    inhalt = f"""<main class="mediathek">
    <nav class="brotkrumen" aria-label="Brotkrumen">
        <a href="/">Startseite</a> <span aria-hidden="true">›</span> <span aria-current="page">Videos</span>
    </nav>

    <h1 class="video-titel">{e(REIHE["name"])} – Videos</h1>
    <p class="mediathek-lead">{e(UEBERSICHT_EINLEITUNG)}</p>

    <ul class="film-karten">
{karten}
    </ul>

{vorbereitung}
    <p class="mediathek-kanal"><a href="{REIHE["youtube_kanal"]}" rel="noopener" data-track="youtube-kanal">Alle Filme auch auf YouTube: @profandprompt →</a></p>
</main>"""
    knoten = [seo.PERSON, seo.ORG, seo.SITE,
              {
                  "@type": "CollectionPage",
                  "@id": UEBERSICHT_URL + "#webpage",
                  "url": UEBERSICHT_URL,
                  "name": UEBERSICHT_TITLE,
                  "description": UEBERSICHT_DESC,
                  "inLanguage": "de-DE",
                  "isPartOf": {"@id": seo.SITE_ID},
                  "mainEntity": {"@id": REIHE_ID},
                  "breadcrumb": {"@id": UEBERSICHT_URL + "#breadcrumb"},
                  "dateModified": UEBERSICHT_STAND,
              },
              {
                  "@type": "CreativeWorkSeries",
                  "@id": REIHE_ID,
                  "name": REIHE["name"],
                  "description": UEBERSICHT_EINLEITUNG,
                  "url": UEBERSICHT_URL,
                  "inLanguage": "de",
                  "author": {"@id": seo.PERSON_ID},
                  "creator": {"@id": seo.PERSON_ID},
                  "publisher": {"@id": seo.ORG_ID},
                  "hasPart": [{"@id": f["url"] + "#video"} for f in VEROEFFENTLICHT],
              },
              {
                  "@type": "ItemList",
                  "@id": UEBERSICHT_URL + "#liste",
                  "name": REIHE["name"],
                  "numberOfItems": len(VEROEFFENTLICHT),
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f["url"],
                                       "name": f["titel"]} for i, f in enumerate(VEROEFFENTLICHT)],
              },
              {
                  "@type": "BreadcrumbList",
                  "@id": UEBERSICHT_URL + "#breadcrumb",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Startseite", "item": DOMAIN + "/"},
                      {"@type": "ListItem", "position": 2, "name": "Videos", "item": UEBERSICHT_URL},
                  ],
              }]
    neuester = max(VEROEFFENTLICHT, key=lambda f: f["upload_date"])
    kopf = kopf_meta(UEBERSICHT_TITLE, UEBERSICHT_DESC, UEBERSICHT_URL, "index, follow", "website",
                     DOMAIN + neuester["poster"], neuester["poster_breite"], neuester["poster_hoehe"],
                     REIHE["name"])
    return seite(kopf + "\n" + jsonld(knoten), inhalt)


# ------------------------------------------------------------------ Vorlage
def vorlage():
    v = {
        "slug": "{{SLUG}}", "url": DOMAIN + "/videos/{{SLUG}}/",
        "titel": "{{TITEL}}", "name": "{{VOLLER_NAME}}",
        "seitentitel": "{{TITEL}} – Video | Operation Zukunft",
        "meta_description": "{{META_DESCRIPTION_MAX_155}}",
        "beschreibung": "{{BESCHREIBUNG_VIDEOOBJECT}}",
        "antwort": "<strong>{{ANTWORTSATZ}}</strong> {{ANTWORT_REST_40_BIS_60_WOERTER}}",
        "antwort_quelle": "{{QUELLE_DER_DEFINITION}}",
        "worum_es_geht": ["{{SATZ_1}}", "{{SATZ_2}}", "{{SATZ_3}}"],
        "karte": "{{EIN_SATZ_FUER_DIE_KARTE}}",
        "youtube_id": "{{YOUTUBE_ID}}",
        "mp4": "https://pillkahn.de/media/{{DATEI}}.mp4",
        "poster": "/videos/{{POSTER}}.jpg", "poster_breite": 1280, "poster_hoehe": 720,
        "vtt": "/videos/{{UNTERTITEL}}.de.vtt",
        "upload_date": "{{JJJJ-MM-TT}}", "dauer_sekunden": "{{DAUER}}", "seite_stand": "{{JJJJ-MM-TT}}",
        "kapitel": [[0, "{{KAPITEL_1}}"], [60, "{{KAPITEL_2}}"]],
        "transkript": [("{{KAPITEL_1}}", ["{{ABSATZ}}"]), ("{{KAPITEL_2}}", ["{{ABSATZ}}"])],
        "cta_text": "{{AUFRUF_TEXT}}", "cta_link": "{{/vorhandene-seite.html}}", "cta_label": "{{LINKTEXT →}}",
    }
    return videoseite(v, vorlage=True)


# ------------------------------------------------------------------ Weiterleitung
def weiterleitung(f):
    ziel = f["url"]
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Umgezogen: Der Film hat eine eigene Videoseite. GitHub Pages kennt keine
         Server-Weiterleitung; eine sofortige Meta-Weiterleitung wertet Google wie
         eine dauerhafte. Erzeugt von pflege/videos/build.py. -->
    <title>{e(f["titel"])} – umgezogen | Operation Zukunft</title>
    <link rel="canonical" href="{ziel}">
    <meta http-equiv="refresh" content="0; url={ziel}">
    <style>body{{background:#0b0e15;color:#e9edf6;font:1.05rem/1.6 system-ui,sans-serif;padding:3rem 1.5rem}}a{{color:#4fd8ff}}</style>
</head>
<body>
    <p>Diese Seite ist umgezogen: <a href="{ziel}">{e(f["titel"])} – Video mit Kapiteln und Transkript</a></p>
</body>
</html>
"""


# ------------------------------------------------------------------ Dateien im Bestand
def video_sitemap():
    z = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<!-- Video-Sitemap: generiert von pflege/videos/build.py -->',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
         '        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">']
    for f in VEROEFFENTLICHT:
        x = lambda t: html.escape(t, quote=False)
        z += ['  <url>',
              f'    <loc>{f["url"]}</loc>',
              '    <video:video>',
              f'      <video:thumbnail_loc>{DOMAIN}{f["poster"]}</video:thumbnail_loc>',
              f'      <video:title>{x(f["name"])}</video:title>',
              f'      <video:description>{x(f["beschreibung"])}</video:description>',
              f'      <video:content_loc>{f["mp4"]}</video:content_loc>',
              f'      <video:player_loc>https://www.youtube.com/embed/{f["youtube_id"]}</video:player_loc>',
              f'      <video:duration>{f["dauer_sekunden"]}</video:duration>',
              f'      <video:publication_date>{f["upload_date"]}</video:publication_date>',
              '      <video:family_friendly>yes</video:family_friendly>',
              '    </video:video>',
              '  </url>']
    z.append('</urlset>')
    return "\n".join(z) + "\n"


def sitemap(t):
    block = ["  <!-- Videos (generiert von pflege/videos/build.py) -->",
             "  <url>", f"    <loc>{UEBERSICHT_URL}</loc>",
             f"    <lastmod>{max([UEBERSICHT_STAND] + [f['seite_stand'] for f in VEROEFFENTLICHT])}</lastmod>",
             "  </url>"]
    for f in VEROEFFENTLICHT:
        block += ["  <url>", f"    <loc>{f['url']}</loc>", f"    <lastmod>{f['seite_stand']}</lastmod>", "  </url>"]
    block.append("  <!-- /Videos -->")
    block = "\n".join(block) + "\n"
    if "<!-- Videos (generiert" in t:
        return re.sub(r"  <!-- Videos \(generiert.*?<!-- /Videos -->\n", lambda m: block, t, flags=re.S)
    return t.replace("  <!-- Blogbeitraege", block + "\n  <!-- Blogbeitraege", 1)


def robots(t):
    zeile = f"Sitemap: {DOMAIN}/video-sitemap.xml"
    if zeile in t:
        return t
    return t.rstrip("\n") + "\n" + zeile + "\n"


def llms(t):
    z = ["## Videos", "",
         f"- [{REIHE['name']} – Videos]({UEBERSICHT_URL}): Videoreihe von Prof. Dr. Ulf Pillkahn "
         "zu Zukunftsforschung und Corporate Foresight, jedes Video mit Kapiteln und Transkript."]
    for f in VEROEFFENTLICHT:
        z.append(f"- [{f['titel']}]({f['url']}): {f['karte']}")
    block = "\n".join(z) + "\n\n"
    if "\n## Videos\n" in t:
        return re.sub(r"## Videos\n.*?(?=## )", lambda m: block, t, flags=re.S)
    return t.replace("## Belege und Methodik", block + "## Belege und Methodik", 1)


def startseite(t):
    f = max(VEROEFFENTLICHT, key=lambda f: f["upload_date"])
    block = f"""<!-- MEDIATHEK:START (generiert von pflege/videos/build.py, nicht von Hand ändern) -->
<section id="videos" class="mediathek-teaser">
    <div class="section-full">
        <p class="section-label reveal">Videos</p>
        <h2 class="section-title reveal">{e(REIHE["name"])}</h2>
        <div class="mediathek-teaser-grid reveal">
            <a href="videos/{f["slug"]}/" class="mediathek-teaser-bild" data-track="start-video">
                <img src="{f["poster"].lstrip("/")}" alt="Vorschaubild: {e(f["titel"])}" width="{f["poster_breite"]}" height="{f["poster_hoehe"]}" loading="lazy">
                <span class="mediathek-play" aria-hidden="true">▶</span>
            </a>
            <div class="mediathek-teaser-text">
                <p class="mediathek-teaser-neu">Neueste Folge · {mmss(f["dauer_sekunden"])} Min.</p>
                <h3><a href="videos/{f["slug"]}/" data-track="start-video-titel">{e(f["titel"])}</a></h3>
                <p>{e(f["karte"])}</p>
                <a href="videos/" class="btn btn-outline" data-track="start-mediathek">Alle Videos der Reihe →</a>
            </div>
        </div>
    </div>
</section>
<!-- MEDIATHEK:ENDE -->
"""
    if "<!-- MEDIATHEK:START" in t:
        return re.sub(r"<!-- MEDIATHEK:START.*?<!-- MEDIATHEK:ENDE -->\n", lambda m: block, t, flags=re.S)
    anker = "<!-- ===================== BUCH & WORKBOOKS"
    assert anker in t, "Startseiten-Anker nicht gefunden"
    return t.replace(anker, block + "\n" + anker, 1)


# ------------------------------------------------------------------ Lauf
def main():
    for f in VEROEFFENTLICHT:
        schreib(P("videos", f["slug"], "index.html"), videoseite(f))
        if f.get("alte_url"):
            schreib(P(f["alte_url"].lstrip("/")), weiterleitung(f))
    schreib(P("videos", "index.html"), uebersicht())
    schreib(P("videos", "_vorlage", "index.html"), vorlage())
    schreib(P("video-sitemap.xml"), video_sitemap())
    schreib(P("sitemap.xml"), sitemap(lies(P("sitemap.xml"))))
    schreib(P("robots.txt"), robots(lies(P("robots.txt"))))
    schreib(P("llms.txt"), llms(lies(P("llms.txt"))))
    schreib(P("index.html"), startseite(lies(P("index.html"))))
    print(len(VEROEFFENTLICHT), "veröffentlicht,", len(GEPLANT), "in Vorbereitung")


if __name__ == "__main__":
    main()
