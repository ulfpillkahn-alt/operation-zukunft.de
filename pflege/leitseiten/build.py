#!/usr/bin/env python3
"""
pflege/leitseiten/build.py — Leitseiten für operation-zukunft.de

Eine Leitseite besitzt genau einen Suchbegriff (siehe AUFTRAG.md, Stand 22.11.2026).

Datenquelle je Seite:
  pflege/leitseiten/seiten/<slug>/seite.json   Kopf, Antwortabsatz, FAQ, Quellen, Verweise
  pflege/leitseiten/seiten/<slug>/inhalt.html  Hauptteil: <section id="…"><h2>…</h2>…</section>
                                               Platzhalter: {{MAIL_WORKSHOP}}, {{MAIL_AGENTEN}},
                                               {{KONTAKT}}, {{VIDEO}}

Erzeugt bzw. pflegt (idempotent, ein zweiter Lauf ändert nichts):
  <slug>/index.html      die Leitseite mit Brotkrumen, H1, Antwortabsatz, Autorenzeile,
                         Inhaltsverzeichnis, Hauptteil, Häufige Fragen, „Weiter im Thema“
                         (nur live geschaltete Seiten), Quellen und einem JSON-LD-@graph
  index.html             Abschnitt #themen zwischen den THEMEN-Markern, eine Karte je live
                         geschalteter Leitseite
  Footer                 Links zwischen <!-- THEMEN-LINKS --> auf Startseite, Cluster,
                         Szenariofilme, Paketseite und allen Blogseiten
  sitemap.xml            Block zwischen <!-- Leitseiten … --> und <!-- /Leitseiten -->
  llms.txt               Abschnitt „## Leitseiten“
  videos/…               ruft am Ende pflege/videos/build.py auf (Menü und Footer der
                         Videoseiten stammen aus cluster.html)

Menü und Footer kommen wie bei den Videoseiten aus cluster.html.
„live“: false heißt: Die Seite wird gebaut, aber von nirgends verlinkt.

Reihenfolge bei Änderungen am Blog: pflege/blog/build.py (ruft dieses Skript selbst auf),
dann pflege/seo.py.

Aufruf im Repo-Root:   python3 pflege/leitseiten/build.py
Danach prüfen:         python3 pflege/leitseiten/pruefen.py --links
"""

import html
import importlib.util
import json
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, os.path.join(REPO, "pflege"))
import seo  # noqa: E402  (Kanon: PERSON, ORG, SITE, @ids, Bücher, CSS-Version)

# Bausteine der Mediathek mitbenutzen (Kopf, Menü, Footer, Filmdaten)
_spec = importlib.util.spec_from_file_location("videos_build", os.path.join(REPO, "pflege", "videos", "build.py"))
videos = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(videos)

DOMAIN = seo.DOMAIN
MAIN_JS = "2026-11-12"
TRACK_JS = "2026-11-15"

_BODY = ("&amp;body=Worum%20geht%20es%3F%0D%0A%0D%0A%0D%0AZeitrahmen%3A%0D%0A%0D%0A"
         "Telefon%20f%C3%BCr%20R%C3%BCckfragen%20(optional)%3A%0D%0A")
MAIL = {  # Betreffs wie auf der Startseite
    "MAIL_WORKSHOP": ("mailto:info@operation-zukunft.de?subject=Anfrage%20Orientierungsworkshop%20KI%20"
                      "f%C3%BCr%20Innovation%20und%20Foresight" + _BODY),
    "MAIL_AGENTEN": ("mailto:info@operation-zukunft.de?subject=Anfrage%20KI-Agenten%20f%C3%BCr%20"
                     "Innovation%20und%20Foresight" + _BODY),
    "MAIL_VORTRAG": "mailto:info@operation-zukunft.de?subject=Anfrage%20Vortrag" + _BODY,
    "MAIL_DIREKT": "mailto:info@operation-zukunft.de?subject=Anfrage%20%C3%BCber%20operation-zukunft.de" + _BODY,
}

KONTAKT = f"""<div class="ls-kontakt">
<p class="ls-kontakt-intro">Lieber direkt? Rufen Sie an oder schreiben Sie mir.</p>
<div class="kontakt-direkt-grid">
<div class="kontakt-direkt-item">
<span class="kontakt-direkt-label">Telefon</span>
<a class="kontakt-direkt-wert" href="tel:+4915236191599" data-track="leit-telefon">+49 152 3619 1599</a>
<p class="kontakt-direkt-hinweis">Nicht erreicht? Ich rufe innerhalb eines Werktags zurück.</p>
</div>
<div class="kontakt-direkt-item">
<span class="kontakt-direkt-label">E-Mail</span>
<span class="kontakt-direkt-zeile">
<a class="kontakt-direkt-wert" href="{MAIL["MAIL_DIREKT"]}" data-track="leit-mail">info@operation-zukunft.de</a>
<button type="button" class="kontakt-kopieren" data-copy="info@operation-zukunft.de" data-track="leit-mail-kopieren">Adresse kopieren</button>
</span>
<p class="kontakt-direkt-hinweis">Öffnet sich kein Mailprogramm? Adresse kopieren und in Ihr Postfach einfügen.</p>
<span class="kontakt-kopiert-status" role="status" aria-live="polite"></span>
</div>
</div>
</div>"""

e = lambda t: html.escape(str(t), quote=True)
P = lambda *a: os.path.join(REPO, *a)


def lies(p):
    return open(p, encoding="utf-8").read()


def schreib(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    alt = lies(p) if os.path.exists(p) else None
    if alt != t:
        open(p, "w", encoding="utf-8").write(t)
        print("  geschrieben:", os.path.relpath(p, REPO))


def datum_de(iso):
    j, m, t = iso.split("-")
    return f"{t}.{m}.{j}"


# ------------------------------------------------------------------ Daten
def lade_seiten():
    seiten = []
    wurzel = os.path.join(HIER, "seiten")
    for slug in sorted(os.listdir(wurzel)):
        d = os.path.join(wurzel, slug)
        if not os.path.isfile(os.path.join(d, "seite.json")):
            continue
        s = json.load(open(os.path.join(d, "seite.json"), encoding="utf-8"))
        s["slug"] = slug
        s["pfad"] = f"/{slug}/"
        s["url"] = DOMAIN + s["pfad"]
        s["inhalt"] = lies(os.path.join(d, "inhalt.html"))
        seiten.append(s)
    return sorted(seiten, key=lambda s: s["reihenfolge"])


SEITEN = lade_seiten()
LIVE = [s for s in SEITEN if s["live"]]


# ------------------------------------------------------------------ Bausteine
def kopier_skript():
    """Das Skript „Adresse kopieren“ steht einmal in index.html und wird von dort übernommen."""
    ix = lies(P("index.html"))
    m = re.search(r'<!-- Kontakt: „Adresse kopieren".*?</script>', ix, re.S)
    assert m, "Kopier-Skript in index.html nicht gefunden"
    return m.group(0)


def menue():
    n = videos.wurzelpfade(videos._aus_cluster("nav"))
    n = n.replace(' aria-current="page"', "")
    return n.replace('href="/#themen"', 'href="/#themen" aria-current="page"', 1)


def videohinweis(s):
    v = s.get("video")
    if not v:
        return ""
    f = next(x for x in videos.VEROEFFENTLICHT if x["slug"] == v["slug"])
    return f"""<aside class="ls-video" aria-label="Video zum Thema">
<a class="ls-video-bild" href="/videos/{f["slug"]}/" data-track="leit-video">
<img src="{f["poster"]}" alt="Vorschaubild des Videos „{e(f["titel"])}“" width="{f["poster_breite"]}" height="{f["poster_hoehe"]}" loading="lazy">
<span class="mediathek-play" aria-hidden="true">▶</span>
</a>
<div class="ls-video-text">
<p class="ls-video-label">Video · {videos.mmss(f["dauer_sekunden"])} Min.</p>
<p>{v["text"]}</p>
<p><a href="/videos/{f["slug"]}/" data-track="leit-video-link">{e(v["linktext"])} →</a></p>
</div>
</aside>"""


def abschnitte(s):
    """Sprungmarken: alle <section id><h2> des Hauptteils, dann Fragen, Weiter, Quellen."""
    a = [(i, re.sub(r"<[^>]+>", "", t).strip())
         for i, t in re.findall(r'<section id="([^"]+)">\s*<h2>(.*?)</h2>', s["inhalt"], re.S)]
    a.append(("fragen", "Häufige Fragen"))
    if [x for x in LIVE if x["slug"] != s["slug"]]:
        a.append(("weiter", "Weiter im Thema"))
    a.append(("quellen", "Quellen"))
    return a


def hauptteil(s):
    t = s["inhalt"]
    for k, v in MAIL.items():
        t = t.replace("{{" + k + "}}", v)
    t = t.replace("{{KONTAKT}}", KONTAKT)
    t = t.replace("{{VIDEO}}", videohinweis(s))
    rest = re.findall(r"\{\{[A-Z_]+\}\}", t)
    assert not rest, f'{s["slug"]}: unbekannte Platzhalter {rest}'
    return t.strip()


def fragen(s):
    z = ['<section id="fragen">', "<h2>Häufige Fragen</h2>", '<div class="ls-faq">']
    for f, a in s["faq"]:
        z += [f"<h3>{e(f)}</h3>", f"<p>{e(a)}</p>"]
    z += ["</div>", "</section>"]
    return "\n".join(z)


def weiter(s):
    andere = [x for x in LIVE if x["slug"] != s["slug"]]
    if not andere:
        return ""
    z = ['<section id="weiter">', "<h2>Weiter im Thema</h2>", '<ul class="ls-weiter">']
    for x in andere:
        z.append(f'<li><a href="{x["pfad"]}" data-track="leit-weiter">{e(x["kurztitel"])}</a>'
                 f'<span>{e(x["karte"])}</span></li>')
    z += ["</ul>", "</section>"]
    return "\n".join(z) + "\n\n"


def quellen(s):
    z = ['<section id="quellen">', "<h2>Quellen</h2>", '<ol class="ls-quellen">']
    for q in s["quellen"]:
        kurz = re.sub(r"^https?://(www\.)?", "", q["url"]).split("?")[0].rstrip("/")
        z.append(f'<li>{e(q["text"])} <a href="{e(q["url"])}">{e(kurz)}</a></li>')
    z += ["</ol>", "</section>"]
    return "\n".join(z)


def graph(s):
    url = s["url"]
    zitiert = seo.buecher(*s.get("buecher", []))
    zitiert += [{"@type": q["typ"], "name": q["name"], "url": q["url"]}
                for q in s["quellen"] if q["typ"] != "buch"]
    seite = {
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": s["title"],
        "headline": s["h1"],
        "description": s["description"],
        "inLanguage": "de-DE",
        "isPartOf": {"@id": seo.SITE_ID},
        "about": {"@type": "Thing", "name": s["begriff"], "description": s["antwort"]},
        "author": {"@id": seo.PERSON_ID},
        "publisher": {"@id": seo.ORG_ID},
        "datePublished": s["veroeffentlicht"],
        "dateModified": s["stand"],
        "breadcrumb": {"@id": url + "#breadcrumb"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": seo.HERO["url"],
                               "width": seo.HERO["w"], "height": seo.HERO["h"]},
    }
    if zitiert:
        seite["citation"] = zitiert
    krumen = {
        "@type": "BreadcrumbList",
        "@id": url + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": s["kurztitel"], "item": url},
        ],
    }
    faq = {
        "@type": "FAQPage",
        "@id": url + "#faq",
        "url": url + "#fragen",
        "inLanguage": "de-DE",
        "isPartOf": {"@id": url + "#webpage"},
        "mainEntity": [{"@type": "Question", "name": f,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for f, a in s["faq"]],
    }
    # Leistungen: dieselben Knoten wie auf der Startseite (gleiche @id, offers nur mit Preis)
    leistungen = [dict(l) for l in seo.LEISTUNGEN
                  if l["@id"].split("#")[1] in s.get("leistungen", [])]
    assert len(leistungen) == len(s.get("leistungen", [])), f'{s["slug"]}: unbekannte Leistung'
    knoten = [seo.PERSON, seo.ORG, seo.SITE, seite, krumen, faq] + leistungen
    daten = {"@context": "https://schema.org", "@graph": knoten}
    t = json.dumps(daten, ensure_ascii=False, indent=2)
    t = "\n".join("    " + z for z in t.splitlines())
    return ('    <!-- Strukturdaten: generiert von pflege/leitseiten/build.py -->\n'
            '    <script type="application/ld+json">\n' + t + '\n    </script>\n')


def leitseite(s):
    for feld, grenze in (("title", 60), ("description", 155)):
        assert len(s[feld]) <= grenze, f'{s["slug"]}: {feld} hat {len(s[feld])} Zeichen'
    sprung = "\n".join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t in abschnitte(s))
    kopf = videos.kopf_meta(s["title"], s["description"], s["url"], "index, follow", "article",
                            seo.HERO["url"], seo.HERO["w"], seo.HERO["h"], seo.HERO["alt"])
    kopf += (f'\n    <meta property="article:published_time" content="{s["veroeffentlicht"]}">'
             f'\n    <meta property="article:modified_time" content="{s["stand"]}">'
             '\n    <meta property="article:author" content="https://pillkahn.de/">')
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
{kopf}
{graph(s)}    <link rel="stylesheet" href="/style.css?v={seo.CSS_VERSION}">
</head>
<body>

<!-- Kino-Ebenen: feines Raster, Film-Grain, Vignette -->
<div class="grid-bg" aria-hidden="true"></div>
<div class="film-grain" aria-hidden="true"></div>
<div class="vignette" aria-hidden="true"></div>

<!-- ===================== NAVIGATION ===================== -->
{menue()}

<!-- ===================== INHALT (generiert von pflege/leitseiten/build.py) ===================== -->
<main class="leitseite">
<nav class="brotkrumen" aria-label="Brotkrumen">
<a href="/">Start</a> <span aria-hidden="true">›</span> <span aria-current="page">{e(s["kurztitel"])}</span>
</nav>

<h1 class="ls-titel">{e(s["h1"])}</h1>

<p class="ls-antwort">{e(s["antwort"])}</p>

<p class="ls-autor">Von <a href="https://pillkahn.de/">Prof. Dr. Ulf Pillkahn</a> · Zuletzt aktualisiert: <time datetime="{s["stand"]}">{datum_de(s["stand"])}</time></p>

<div class="ls-inhalt" role="navigation" aria-label="Inhalt dieser Seite">
<p class="ls-inhalt-titel">Inhalt</p>
<ol>
{sprung}
</ol>
</div>

{hauptteil(s)}

{fragen(s)}

{weiter(s)}{quellen(s)}
</main>

<!-- ===================== FOOTER & IMPRESSUM ===================== -->
{videos.fuss()}

{kopier_skript()}
<!-- Seitenverhalten -->
<script src="/main.js?v={MAIN_JS}"></script>
<!-- Besucherzähler (eigener Zähler auf pillkahn.de, siehe track.js) -->
<script src="/track.js?v={TRACK_JS}" defer></script>

</body>
</html>
"""


# ------------------------------------------------------------------ Einbindung im Bestand
THEMEN_INTRO = ("Jede Seite erklärt einen Begriff gründlich: Definition, Vorgehen, Grenzen "
                "und der Weg in die Praxis.")


def startseite(t):
    """Abschnitt #themen mit einer Karte je live geschalteter Leitseite."""
    karten = "\n".join(f"""            <a class="themen-karte" href="{s["slug"]}/" data-track="themen-karte">
                <h3>{e(s["kurztitel"])}</h3>
                <p>{e(s["karte"])}</p>
                <span class="themen-mehr">Zur Seite →</span>
            </a>""" for s in LIVE)
    block = f"""<!-- THEMEN:START (generiert von pflege/leitseiten/build.py, nicht von Hand ändern) -->
<section id="themen" class="themen">
    <div class="section-full">
        <p class="section-label reveal">Themen</p>
        <h2 class="section-title reveal">Foresight zum Nachlesen</h2>
        <p class="section-intro reveal">{THEMEN_INTRO}</p>
        <div class="themen-karten reveal">
{karten}
        </div>
    </div>
</section>
<!-- THEMEN:ENDE -->
""" if LIVE else ""
    if "<!-- THEMEN:START" in t:
        return re.sub(r"<!-- THEMEN:START.*?<!-- THEMEN:ENDE -->\n\n?", lambda m: block + ("\n" if block else ""),
                      t, flags=re.S)
    if not block:
        return t
    anker = "<!-- MEDIATHEK:START"
    assert anker in t, "Startseiten-Anker (Mediathek) nicht gefunden"
    return t.replace(anker, block + "\n" + anker, 1)


def fusslinks(t, vor):
    """Links auf die live geschalteten Leitseiten in <div class="footer-links">.
    vor = "" für Seiten im Wurzelverzeichnis, "../" für den Blog."""
    links = "".join(f'<a href="{vor}{s["slug"]}/" data-track="footer-thema">{e(s["kurztitel"])}</a>'
                    for s in LIVE)
    block = f"<!-- THEMEN-LINKS -->{links}<!-- /THEMEN-LINKS -->"
    if "<!-- THEMEN-LINKS -->" in t:
        return re.sub(r"<!-- THEMEN-LINKS -->.*?<!-- /THEMEN-LINKS -->", lambda m: block, t, flags=re.S)
    if not LIVE:
        return t
    m = re.search(r'(<div class="footer-links">.*?)\n([ \t]*)</div>', t, re.S)
    assert m, "footer-links nicht gefunden"
    return t[:m.end(1)] + f"\n{m.group(2)}    {block}" + t[m.end(1):]


def sitemap(t):
    z = ["  <!-- Leitseiten (generiert von pflege/leitseiten/build.py) -->"]
    for s in LIVE:
        z += ["  <url>", f"    <loc>{s['url']}</loc>", f"    <lastmod>{s['stand']}</lastmod>", "  </url>"]
    z.append("  <!-- /Leitseiten -->")
    block = "\n".join(z) + "\n"
    if "<!-- Leitseiten (generiert" in t:
        return re.sub(r"  <!-- Leitseiten \(generiert.*?<!-- /Leitseiten -->\n", lambda m: block, t, flags=re.S)
    anker = "  <!-- Videos (generiert"
    assert anker in t, "Sitemap-Anker (Videos) nicht gefunden"
    return t.replace(anker, block + "\n" + anker, 1)


def llms(t):
    z = ["## Leitseiten", ""]
    z += [f"- [{s['kurztitel']}]({s['url']}): {s['karte']}" for s in LIVE]
    block = "\n".join(z) + "\n\n"
    if "\n## Leitseiten\n" in t:
        return re.sub(r"## Leitseiten\n.*?(?=## )", lambda m: block, t, flags=re.S)
    assert "## Videos" in t, "llms.txt-Anker (Videos) nicht gefunden"
    return t.replace("## Videos", block + "## Videos", 1)


WURZELSEITEN = ["index.html", "cluster.html", "szenariofilme.html", "strategie-pakete.html"]


# ------------------------------------------------------------------ Lauf
def main():
    # 1. Bestand: Startseite, Footer, Sitemap, llms.txt (nur live geschaltete Seiten)
    schreib(P("index.html"), startseite(lies(P("index.html"))))
    for d in WURZELSEITEN:
        schreib(P(d), fusslinks(lies(P(d)), ""))
    for d in sorted(os.listdir(P("blog"))):
        if d.endswith(".html") and 'http-equiv="refresh"' not in lies(P("blog", d)):
            schreib(P("blog", d), fusslinks(lies(P("blog", d)), "../"))
    schreib(P("sitemap.xml"), sitemap(lies(P("sitemap.xml"))))
    schreib(P("llms.txt"), llms(lies(P("llms.txt"))))
    # 2. Leitseiten (Menü und Footer aus cluster.html, deshalb nach Schritt 1)
    for s in SEITEN:
        schreib(P(s["slug"], "index.html"), leitseite(s))
    # 3. Videoseiten übernehmen Menü und Footer ebenfalls aus cluster.html
    videos.main()
    print(len(SEITEN), "Leitseiten gebaut,", len(LIVE), "davon live geschaltet")


if __name__ == "__main__":
    main()
