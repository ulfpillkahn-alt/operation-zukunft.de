#!/usr/bin/env python3
"""
pflege/leitseiten/pruefen.py — Prüfung der Leitseiten (AUFTRAG.md, Schritt 6)

Prüft jede gebaute Leitseite:
  1. JSON-LD gültig, jeder @id-Verweis hat einen Knoten, Person- und Organisations-@id stimmen
  2. genau eine H1
  3. Title ≤ 60, Description ≤ 155, Canonical auf sich selbst
  4. Wortzahlen: Antwortabsatz 40–60, Hauptteil 1.500–2.200 (Szenariotechnik bis 2.500)
  5. kein Absatz über 40 Wörter doppelt auf zwei Leitseiten
  6. Hauptbegriff in Title, H1, Antwortabsatz und URL der eigenen Seite,
     in keinem Title und keiner H1 einer anderen Leitseite
  7. Begriffe anderer Domains höchstens einmal im Text und dorthin verlinkt
  8. Preise stehen wörtlich in index.html oder strategie-pakete.html
  9. FAQ: sichtbarer Text und JSON-LD stimmen überein
 10. Links: interne Ziele existieren im Repo; mit --links zusätzlich alle
     externen Ziele per curl (SSRN weist curl ab und wird als „im Browser prüfen“ gemeldet)

Aufruf im Repo-Root:   python3 pflege/leitseiten/pruefen.py [--links]
Ende mit Status 1, wenn etwas nicht stimmt.
"""

import html
import json
import os
import re
import subprocess
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, os.path.join(REPO, "pflege"))
sys.path.insert(0, HIER)
import seo  # noqa: E402

DOMAIN = seo.DOMAIN
FREMD = {  # Begriff → Domain, der er gehört
    "Agentic Foresight": "agentic-foresight.com",
    "Szenariogenerierung mit KI": "picturesoftomorrow.com",
    "Zukunftsforscher": "pillkahn.de",
    "Trendradar": "squawk.de",
    "Flipped Foresight": "flipped-foresight.com",
}
NUR_BROWSER = ("papers.ssrn.com",)  # weisen curl ab
HAUPTTEIL_MAX = {"szenariotechnik": 2500}

fehler, hinweise = [], []


def lies(p):
    return open(p, encoding="utf-8").read()


def klartext(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def woerter(t):
    return len(klartext(t).split())


def lade():
    seiten = []
    wurzel = os.path.join(HIER, "seiten")
    for slug in sorted(os.listdir(wurzel)):
        j = os.path.join(wurzel, slug, "seite.json")
        if not os.path.isfile(j):
            continue
        s = json.load(open(j, encoding="utf-8"))
        s["slug"] = slug
        datei = os.path.join(REPO, slug, "index.html")
        if not os.path.exists(datei):
            fehler.append(f"{slug}: index.html fehlt – erst build.py laufen lassen")
            continue
        s["html"] = lies(datei)
        s["main"] = re.search(r"<main\b.*?</main>", s["html"], re.S).group(0)
        seiten.append(s)
    return seiten


def ids_sammeln(knoten, definiert, verwiesen):
    if isinstance(knoten, dict):
        if "@id" in knoten:
            (verwiesen if set(knoten) == {"@id"} else definiert).add(knoten["@id"])
        for v in knoten.values():
            ids_sammeln(v, definiert, verwiesen)
    elif isinstance(knoten, list):
        for v in knoten:
            ids_sammeln(v, definiert, verwiesen)


def pruefe_seite(s, alle):
    n, t, m = s["slug"], s["html"], s["main"]
    url = f"{DOMAIN}/{n}/"
    f = lambda text: fehler.append(f"{n}: {text}")

    # 1. JSON-LD
    bloecke = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    if len(bloecke) != 1:
        f(f"{len(bloecke)} JSON-LD-Blöcke statt einem")
    graph = []
    for b in bloecke:
        try:
            graph = json.loads(b)["@graph"]
        except Exception as ex:  # noqa: BLE001
            f(f"JSON-LD ungültig: {ex}")
    definiert, verwiesen = set(), set()
    ids_sammeln(graph, definiert, verwiesen)
    for v in sorted(verwiesen - definiert):
        f(f"@id-Verweis ohne Knoten: {v}")
    for pflicht in (seo.PERSON_ID, seo.ORG_ID, url + "#webpage", url + "#breadcrumb", url + "#faq"):
        if pflicht not in definiert:
            f(f"Knoten fehlt: {pflicht}")
    typen = [k.get("@type") for k in graph]
    for typ in ("WebPage", "BreadcrumbList", "FAQPage", "Service"):
        if typ not in typen:
            f(f"Typ fehlt im @graph: {typ}")
    for k in graph:
        if k.get("@type") == "WebPage":
            if k.get("author") != {"@id": seo.PERSON_ID} or k.get("publisher") != {"@id": seo.ORG_ID}:
                f("WebPage: author/publisher zeigen nicht auf Person/Organisation")
            for feld in ("about", "dateModified"):
                if feld not in k:
                    f(f"WebPage ohne {feld}")
            for z in k.get("citation", []):
                if z.get("@type") == "Book" and "pillkahn.de/publikationen/" not in z.get("@id", ""):
                    f(f"Buch ohne Book-@id auf pillkahn.de: {z}")
        if k.get("@type") == "Service":
            if k.get("provider") != {"@id": seo.ORG_ID}:
                f(f"Service ohne provider → Organisation: {k.get('name')}")

    # 2. H1
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", t, re.S)
    if len(h1) != 1:
        f(f"{len(h1)} H1 statt einer")
    h1text = klartext(h1[0]) if h1 else ""

    # 3. Kopf
    title = html.unescape(re.search(r"<title>(.*?)</title>", t, re.S).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', t).group(1))
    if len(title) > 60:
        f(f"Title {len(title)} Zeichen")
    if len(desc) > 155:
        f(f"Description {len(desc)} Zeichen")
    kanon = re.search(r'<link rel="canonical" href="([^"]*)"', t).group(1)
    if kanon != url:
        f(f"Canonical {kanon} statt {url}")
    for pflicht in ('property="og:title"', 'property="og:image"', 'name="twitter:card"'):
        if pflicht not in t:
            f(f"Kopf ohne {pflicht}")
    for img in re.findall(r"<img\b[^>]*>", m):
        if not re.search(r'alt="[^"]+"', img):
            f(f"Bild ohne alt-Text: {img[:80]}")

    # 4. Wortzahlen
    antwort = klartext(re.search(r'<p class="ls-antwort">(.*?)</p>', m, re.S).group(1))
    wa = len(antwort.split())
    if not 40 <= wa <= 60:
        f(f"Antwortabsatz {wa} Wörter")
    haupt = m[m.index("</div>", m.index('class="ls-inhalt"')):m.index('<section id="fragen">')]
    haupt = haupt[haupt.index("<section"):]
    wh = woerter(haupt)
    grenze = HAUPTTEIL_MAX.get(n, 2200)
    if not 1500 <= wh <= grenze:
        f(f"Hauptteil {wh} Wörter (Soll 1.500–{grenze})")
    faq_sichtbar = re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>",
                              m[m.index('<section id="fragen">'):m.index("</section>", m.index('<section id="fragen">'))], re.S)
    if not 5 <= len(faq_sichtbar) <= 6:
        f(f"{len(faq_sichtbar)} Fragen statt 5–6")
    for frage, a in faq_sichtbar:
        saetze = len(re.findall(r"[.!?](?:\s|$)", klartext(a).replace("zzgl. USt.", "zzgl USt.")))
        if not 2 <= saetze <= 4:
            f(f"Antwort mit {saetze} Sätzen: {klartext(frage)}")

    # 6. Hauptbegriff
    b = s["begriff"]
    for wo, text in (("Title", title), ("H1", h1text), ("Antwortabsatz", antwort)):
        if b not in text:
            f(f"Hauptbegriff „{b}“ fehlt in {wo}")
    if not h1text.startswith(b):
        f("H1 beginnt nicht mit dem Hauptbegriff")
    slug_soll = re.sub(r"[^a-z0-9]+", "-", b.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")).strip("-")
    if slug_soll != n:
        f(f"URL /{n}/ entspricht nicht dem Hauptbegriff ({slug_soll})")
    for o in alle:
        if o["slug"] != n and (o["begriff"] in title or o["begriff"] in h1text):
            f(f"Hauptbegriff von {o['slug']} („{o['begriff']}“) steht in Title oder H1")
    for nb in s.get("nebenbegriffe", []):
        if nb.lower() not in klartext(m).lower():
            hinweise.append(f"{n}: Nebenbegriff „{nb}“ kommt im Text nicht vor")

    # 7. Begriffe anderer Domains (Quellenangaben zählen nicht: Werktitel)
    text_ohne_quellen = m[:m.index('<section id="quellen">')]
    for begriff, domain in FREMD.items():
        zahl = klartext(text_ohne_quellen).count(begriff)
        if zahl > 1:
            f(f"„{begriff}“ steht {zahl}-mal im Text (höchstens einmal)")
        if zahl == 1 and not re.search(
                rf'<a href="https://(?:www\.)?{re.escape(domain)}[^"]*"[^>]*>[^<]*{re.escape(begriff)}', text_ohne_quellen):
            f(f"„{begriff}“ ist nicht auf {domain} verlinkt")

    # 8. Preise wörtlich aus dem Bestand
    bestand = klartext(lies(os.path.join(REPO, "index.html"))) + klartext(lies(os.path.join(REPO, "strategie-pakete.html")))
    for preis in set(re.findall(r"(?:ab )?\d{1,3}(?:\.\d{3})* €", klartext(m))):
        if preis not in bestand:
            f(f"Preis „{preis}“ steht weder auf der Startseite noch auf der Paketseite")
    if "Black Week" in klartext(m) or "Black-Week" in klartext(m):
        f("Black-Week-Konditionen auf der Leitseite")

    # 9. FAQ sichtbar = JSON-LD
    for k in graph:
        if k.get("@type") == "FAQPage":
            ld = [(q["name"], q["acceptedAnswer"]["text"]) for q in k["mainEntity"]]
            sichtbar = [(klartext(a), klartext(c)) for a, c in faq_sichtbar]
            if ld != sichtbar:
                f("FAQ im JSON-LD weicht vom sichtbaren Text ab")

    # Inhaltsverzeichnis: jede Sprungmarke hat ein Ziel
    for ziel in re.findall(r'<li><a href="#([^"]+)">', m[m.index('class="ls-inhalt"'):m.index("</ol>")]):
        if f'id="{ziel}"' not in m:
            f(f"Sprungmarke #{ziel} ohne Ziel")

    print(f"{n}: Title {len(title)} · Description {len(desc)} · Antwort {wa} Wörter · "
          f"Hauptteil {wh} Wörter · Seite gesamt {woerter(m)} Wörter · {len(faq_sichtbar)} Fragen · "
          f"{len(graph)} Knoten im @graph")
    return haupt


def pruefe_doppelt(seiten):
    """5. Kein Absatz über 40 Wörter auf zwei Leitseiten."""
    gesehen = {}
    for s in seiten:
        for absatz in re.findall(r"<(?:p|li|td)\b[^>]*>(.*?)</(?:p|li|td)>", s["main"], re.S):
            a = klartext(absatz)
            if len(a.split()) > 40:
                if a in gesehen and gesehen[a] != s["slug"]:
                    fehler.append(f'Absatz doppelt auf {gesehen[a]} und {s["slug"]}: {a[:70]}…')
                gesehen.setdefault(a, s["slug"])


def pruefe_links(seiten, extern):
    """10. Interne Ziele existieren, externe antworten mit 200."""
    ziele = {}
    for s in seiten:
        for h in set(re.findall(r'<a\b[^>]*href="([^"]+)"', s["html"])):
            ziele.setdefault(h, set()).add(s["slug"])
    aussen = []
    for h, wo in sorted(ziele.items()):
        if h.startswith(("mailto:", "tel:", "#")):
            continue
        if h.startswith("/"):
            pfad, _, anker = h.partition("#")
            lokal = os.path.join(REPO, pfad.lstrip("/"))
            if os.path.isdir(lokal):
                lokal = os.path.join(lokal, "index.html")
            if not os.path.exists(lokal):
                fehler.append(f"interner Link ohne Ziel: {h} (auf {', '.join(sorted(wo))})")
            elif anker and f'id="{anker}"' not in lies(lokal):
                # #themen entsteht erst in Schritt 3
                hinweise.append(f"Anker #{anker} fehlt in {pfad or '/'} (auf {', '.join(sorted(wo))})")
        elif h.startswith("http"):
            aussen.append(h)
        else:
            fehler.append(f"relativer Link (Wurzelpfad erwartet): {h}")
    if not extern:
        print(f"Links: {len(ziele)} Ziele, interne geprüft; externe mit --links prüfen")
        return
    for h in aussen:
        if any(d in h for d in NUR_BROWSER):
            hinweise.append(f"im Browser prüfen (weist curl ab): {h}")
            continue
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-L", "--max-time", "25", "-w", "%{http_code}", h],
                           capture_output=True, text=True)
        code = r.stdout.strip()
        print(f"  {code}  {h}")
        if code != "200":
            fehler.append(f"Link antwortet mit {code}: {h}")


def pruefe_bestand():
    """Alle übrigen Seiten der Website: JSON-LD gültig und @ids aufgelöst, genau eine H1,
    interne Links mit Ziel. Menü, Footer und #themen ändern diese Seiten mit."""
    dateien = [d for d in os.listdir(REPO) if d.endswith(".html")]
    dateien += [os.path.join("blog", d) for d in os.listdir(os.path.join(REPO, "blog")) if d.endswith(".html")]
    for wurzel, _, namen in os.walk(os.path.join(REPO, "videos")):
        dateien += [os.path.relpath(os.path.join(wurzel, n), REPO) for n in namen if n.endswith(".html")]
    ohne_h1 = {"404.html", "stats.html"}
    zahl = 0
    offen = []      # (Datei, verwiesene @id): Der Knoten darf auf einer anderen Seite der Website stehen
    ueberall = set()
    for d in sorted(dateien):
        t = lies(os.path.join(REPO, d))
        if 'http-equiv="refresh"' in t or "_vorlage" in d:
            continue
        zahl += 1
        definiert, verwiesen = set(), set()
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try:
                ids_sammeln(json.loads(b), definiert, verwiesen)
            except Exception as ex:  # noqa: BLE001
                fehler.append(f"{d}: JSON-LD ungültig: {ex}")
        ueberall |= definiert
        offen += [(d, v) for v in sorted(verwiesen - definiert)]
        h1 = len(re.findall(r"<h1\b", t))
        if h1 != 1 and d not in ohne_h1:
            fehler.append(f"{d}: {h1} H1 statt einer")
        ordner = os.path.dirname(os.path.join(REPO, d))
        for h in set(re.findall(r'<a\b[^>]*href="([^"]+)"', t)):
            if h.startswith(("http", "mailto:", "tel:", "#", "javascript:")):
                continue
            pfad, _, anker = h.partition("#")
            pfad = pfad.split("?")[0]
            lokal = os.path.join(REPO, pfad.lstrip("/")) if pfad.startswith("/") else os.path.normpath(os.path.join(ordner, pfad))
            if os.path.isdir(lokal):
                lokal = os.path.join(lokal, "index.html")
            if not os.path.exists(lokal):
                fehler.append(f"{d}: interner Link ohne Ziel: {h}")
            elif anker and lokal.endswith(".html") and not re.search(rf'id="{re.escape(anker)}"', lies(lokal)):
                fehler.append(f"{d}: Anker #{anker} fehlt im Ziel {h}")
    for d, v in offen:
        if v not in ueberall:
            fehler.append(f"{d}: @id-Verweis ohne Knoten: {v}")
    print(f"Bestand: {zahl} Seiten geprüft (JSON-LD, H1, interne Links)")


def main():
    seiten = lade()
    for s in seiten:
        pruefe_seite(s, seiten)
    pruefe_doppelt(seiten)
    pruefe_links(seiten, "--links" in sys.argv)
    pruefe_bestand()
    for h in hinweise:
        print("Hinweis:", h)
    if fehler:
        print("\nFEHLER:")
        for x in fehler:
            print("  -", x)
        sys.exit(1)
    print(f"\nAlles in Ordnung: {len(seiten)} Leitseite(n) geprüft.")


if __name__ == "__main__":
    main()
