#!/usr/bin/env python3
"""
pflege/videos/pruefen.py — Prüfungen nach jedem Lauf von pflege/videos/build.py

  1. JSON-LD aller HTML-Seiten: gültiges JSON, @id-Verweise lösen sich auf
     (websiteweit), VideoObject vollständig, Clips lückenlos
  2. Videoseiten: Title ≤ 60, Description ≤ 155, Antwortabsatz 40–60 Wörter,
     preload="none", kein YouTube-iframe, Canonical auf sich selbst
  3. video-sitemap.xml und sitemap.xml: wohlgeformt, Pflichtfelder nach dem
     Google-Schema für Video-Sitemaps, jede <loc> hat eine Datei im Repo
  4. robots.txt mit beiden Sitemap-Zeilen
  5. interne Links und Quellen (href/src) aller Seiten zeigen auf vorhandene Dateien
  6. Weiterleitungsseiten: Meta-Refresh, Canonical, kein JSON-LD, kein noindex

Aufruf im Repo-Root:  python3 pflege/videos/pruefen.py      (Exit-Code 1 bei Fehlern)
"""
import glob
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOMAIN = "https://operation-zukunft.de"
fehler, hinweise = [], []
F = fehler.append


def lies(p):
    return open(os.path.join(REPO, p), encoding="utf-8").read()


def seiten():
    for p in sorted(glob.glob(os.path.join(REPO, "**", "*.html"), recursive=True)):
        r = os.path.relpath(p, REPO)
        if r.startswith(("Präsentationen", ".git", "pflege")):
            continue
        yield r


def url_zu_datei(u):
    """Absolute oder wurzelrelative URL dieser Domain → Datei im Repo (oder None)."""
    u = u.split("#")[0].split("?")[0]
    if u.startswith(DOMAIN):
        u = u[len(DOMAIN):]
    if not u.startswith("/"):
        return None
    p = u.lstrip("/")
    if p == "" or p.endswith("/"):
        p += "index.html"
    return p


# ------------------------------------------------------------ 1. JSON-LD
definiert, verweise, graphen = set(), [], {}
for s in seiten():
    t = lies(s)
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            d = json.loads(block)
        except json.JSONDecodeError as ex:
            F(f"{s}: JSON-LD ungültig ({ex})")
            continue
        knoten = d.get("@graph", [d])
        graphen.setdefault(s, []).extend(knoten)

        def laufe(o):
            if isinstance(o, dict):
                if "@id" in o and len(o) == 1:
                    verweise.append((s, o["@id"]))
                elif "@id" in o:
                    definiert.add(o["@id"])
                for v in o.values():
                    laufe(v)
            elif isinstance(o, list):
                for v in o:
                    laufe(v)
        laufe(knoten)

for s, ref in verweise:
    if ref not in definiert:
        F(f"{s}: @id-Verweis ohne Definition: {ref}")

PFLICHT_VIDEO = ["name", "description", "thumbnailUrl", "uploadDate", "duration", "contentUrl",
                 "embedUrl", "inLanguage", "transcript", "author", "creator", "publisher",
                 "isPartOf", "hasPart"]
videos = {}
for s, knoten in graphen.items():
    for k in knoten:
        if k.get("@type") == "VideoObject":
            videos[k["@id"]] = (s, k)
            fehlt = [f for f in PFLICHT_VIDEO if not k.get(f)]
            if fehlt:
                F(f"{s}: VideoObject ohne {', '.join(fehlt)}")
            m = re.fullmatch(r"PT(?:(\d+)M)?(\d+)S", k.get("duration", ""))
            dauer = int(m.group(1) or 0) * 60 + int(m.group(2)) if m else None
            clips = k.get("hasPart", [])
            for a, b in zip(clips, clips[1:]):
                if a["endOffset"] != b["startOffset"]:
                    F(f"{s}: Clip-Lücke zwischen „{a['name']}“ und „{b['name']}“")
            if clips and dauer and clips[-1]["endOffset"] != dauer:
                F(f"{s}: letzter Clip endet nicht bei der Dauer ({dauer} s)")
            if k.get("author", {}).get("@id") != "https://pillkahn.de/#person":
                F(f"{s}: author ist nicht die Person-@id")
            if k.get("publisher", {}).get("@id") != "https://operation-zukunft.de/#organization":
                F(f"{s}: publisher ist nicht die Organisations-@id")
        if k.get("@type") == "WebPage" and "mainEntity" in k and "/videos/" in k.get("url", ""):
            if k["mainEntity"]["@id"] != k["url"] + "#video":
                F(f"{s}: WebPage.mainEntity zeigt nicht auf das VideoObject")

# Jedes VideoObject nur einmal websiteweit (kein doppelter Inhalt)
namen = {}
for vid, (s, k) in videos.items():
    namen.setdefault(k.get("contentUrl"), []).append(s)
for cu, orte in namen.items():
    if len(orte) > 1 and not all("_vorlage" in o for o in orte[1:]):
        F(f"Film {cu} hat VideoObjects auf mehreren Seiten: {orte}")

# ------------------------------------------------------------ 2. Videoseiten
for s in seiten():
    if not re.fullmatch(r"videos/[^_/][^/]*/index\.html", s):
        continue
    t = lies(s)
    title = html.unescape(re.search(r"<title>(.*?)</title>", t).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', t).group(1))
    if len(title) > 60:
        F(f"{s}: Title {len(title)} Zeichen")
    if len(desc) > 155:
        F(f"{s}: Description {len(desc)} Zeichen")
    ant = re.search(r'<p class="video-antwort">(.*?)<span class="video-quelle">', t, re.S)
    if ant:
        woerter = len(re.sub(r"<[^>]+>", " ", ant.group(1)).split())
        if not 40 <= woerter <= 60:
            F(f"{s}: Antwortabsatz hat {woerter} Wörter (Soll 40–60)")
        hinweise.append(f"{s}: Title {len(title)}, Description {len(desc)}, Antwort {woerter} Wörter")
    if 'preload="none"' not in t:
        F(f"{s}: Player ohne preload=\"none\"")
    if re.search(r"<iframe[^>]+youtube", t):
        F(f"{s}: YouTube-iframe eingebettet")
    if 'og:type" content="video.other"' not in t or 'property="og:video"' not in t:
        F(f"{s}: Open Graph für Video fehlt")
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', t).group(1)
    if url_zu_datei(canon) != s:
        F(f"{s}: Canonical zeigt auf {canon}")
    if s.startswith("videos/") and t.find("<video") > t.find('class="video-antwort"'):
        F(f"{s}: Player steht nicht vor dem Antwortabsatz")

v = lies("videos/_vorlage/index.html")
if 'content="noindex' not in v:
    F("videos/_vorlage/index.html: noindex fehlt")

# ------------------------------------------------------------ 3. Sitemaps
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9",
      "video": "http://www.google.com/schemas/sitemap-video/1.1"}
for datei in ["sitemap.xml", "video-sitemap.xml"]:
    try:
        baum = ET.parse(os.path.join(REPO, datei))
    except ET.ParseError as ex:
        F(f"{datei}: nicht wohlgeformt ({ex})")
        continue
    wurzel = baum.getroot()
    if wurzel.tag != "{%s}urlset" % NS["s"]:
        F(f"{datei}: Wurzel ist nicht sitemap-0.9-urlset")
    locs = [u.find("s:loc", NS).text for u in wurzel.findall("s:url", NS)]
    for loc in locs:
        p = url_zu_datei(loc)
        if not p or not os.path.exists(os.path.join(REPO, p)):
            F(f"{datei}: <loc> ohne Datei: {loc}")
        if "_vorlage" in loc:
            F(f"{datei}: Vorlage steht in der Sitemap")
    if len(locs) != len(set(locs)):
        F(f"{datei}: doppelte <loc>")
    if datei == "sitemap.xml":
        if f"{DOMAIN}/blog/was-ist-zukunftsforschung.html" in locs:
            F("sitemap.xml: alte Blog-URL steht noch drin")
        for need in [f"{DOMAIN}/videos/", f"{DOMAIN}/videos/was-ist-zukunftsforschung/"]:
            if need not in locs:
                F(f"sitemap.xml: {need} fehlt")
    else:
        for u in wurzel.findall("s:url", NS):
            loc = u.find("s:loc", NS).text
            vids = u.findall("video:video", NS)
            if not vids:
                F(f"video-sitemap.xml: {loc} ohne <video:video>")
            for vv in vids:
                g = lambda n: (vv.find("video:" + n, NS).text if vv.find("video:" + n, NS) is not None else None)
                for pf in ["thumbnail_loc", "title", "description"]:
                    if not g(pf):
                        F(f"video-sitemap.xml: {loc} ohne video:{pf}")
                if not (g("content_loc") or g("player_loc")):
                    F(f"video-sitemap.xml: {loc} braucht content_loc oder player_loc")
                if len(g("description") or "") > 2048:
                    F(f"video-sitemap.xml: {loc} description > 2048 Zeichen")
                d = g("duration")
                if not (d and d.isdigit() and 1 <= int(d) <= 28800):
                    F(f"video-sitemap.xml: {loc} duration ungültig ({d})")
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}(T.*)?", g("publication_date") or ""):
                    F(f"video-sitemap.xml: {loc} publication_date ungültig")
                th = url_zu_datei(g("thumbnail_loc") or "")
                if th and not os.path.exists(os.path.join(REPO, th)):
                    F(f"video-sitemap.xml: Vorschaubild fehlt im Repo: {th}")
                # Abgleich mit dem VideoObject der Seite
                vo = videos.get(loc + "#video")
                if not vo:
                    F(f"video-sitemap.xml: zu {loc} gibt es kein VideoObject")
                else:
                    k = vo[1]
                    if k["contentUrl"] != g("content_loc"):
                        F(f"video-sitemap.xml: content_loc ≠ contentUrl ({loc})")
                    if k["uploadDate"] != g("publication_date")[:10]:
                        F(f"video-sitemap.xml: publication_date ≠ uploadDate ({loc})")

# ------------------------------------------------------------ 4. robots.txt
r = lies("robots.txt")
for z in [f"Sitemap: {DOMAIN}/sitemap.xml", f"Sitemap: {DOMAIN}/video-sitemap.xml"]:
    if z not in r:
        F(f"robots.txt: Zeile fehlt: {z}")

# ------------------------------------------------------------ 5. interne Links
gezaehlt = 0
for s in seiten():
    t = lies(s)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    for attr, ziel in re.findall(r'\b(href|src)="([^"]+)"', t):
        if ziel.startswith(("mailto:", "tel:", "javascript:", "data:", "#", "?")):
            continue
        if ziel.startswith("http"):
            if not ziel.startswith(DOMAIN):
                continue
            p = url_zu_datei(ziel)
        elif ziel.startswith("/"):
            p = url_zu_datei(ziel)
        else:
            basis = os.path.dirname(s)
            rel = ziel.split("#")[0].split("?")[0]
            p = os.path.normpath(os.path.join(basis, rel))
            if rel.endswith("/") or rel == "":
                p = os.path.join(p, "index.html") if rel else s
        if "{{" in ziel:
            continue
        gezaehlt += 1
        if not os.path.exists(os.path.join(REPO, p)):
            F(f"{s}: toter Link {attr}=\"{ziel}\"")
    if "blog/was-ist-zukunftsforschung.html" in t and s != "blog/was-ist-zukunftsforschung.html":
        F(f"{s}: verlinkt noch die alte Blog-URL")
for p in ["posts.js", "posts.json", "llms.txt"]:
    if "blog/was-ist-zukunftsforschung.html" in lies(p):
        F(f"{p}: enthält noch die alte Blog-URL")

# ------------------------------------------------------------ 6. Weiterleitungen
for s in seiten():
    t = lies(s)
    if 'http-equiv="refresh"' not in t:
        continue
    ziel = re.search(r'http-equiv="refresh" content="0; url=([^"]+)"', t)
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', t)
    if not ziel or not canon or ziel.group(1) != canon.group(1):
        F(f"{s}: Weiterleitung und Canonical stimmen nicht überein")
    if "ld+json" in t:
        F(f"{s}: Weiterleitungsseite enthält JSON-LD")
    if "noindex" in t:
        F(f"{s}: Weiterleitungsseite hat noindex")
    hinweise.append(f"{s}: Weiterleitung → {ziel.group(1)}")

# ------------------------------------------------------------ Ergebnis
print(f"JSON-LD: {sum(len(k) for k in graphen.values())} Knoten auf {len(graphen)} Seiten, "
      f"{len(verweise)} @id-Verweise, {len(videos)} VideoObject(s)")
print(f"Links: {gezaehlt} interne Ziele geprüft")
for h in hinweise:
    print("  ·", h)
if fehler:
    print(f"\n{len(fehler)} FEHLER:")
    for f in fehler:
        print("  ✗", f)
    sys.exit(1)
print("\nAlles in Ordnung.")
