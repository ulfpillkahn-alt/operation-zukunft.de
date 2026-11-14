#!/usr/bin/env python3
"""
pflege/seo.py — Kopf, Strukturdaten und Fuß für operation-zukunft.de

Setzt den Cluster-Standard um (CLUSTER-STANDARD.md im Repo von pillkahn.de).
Läuft nur lokal; auf GitHub Pages wird ganz normales statisches HTML
ausgeliefert. Wiederholbar: Ein zweiter Lauf ändert nichts.

Je Seite:
  1. entfernt title, description, keywords, author, canonical, og:*, article:*,
     twitter:* und setzt einen vollständigen Block direkt hinter <meta viewport>
  2. ersetzt alle JSON-LD-Blöcke durch EINEN @graph vor </head>
  3. Fuß: pillkahn.com als Personenlink raus, „Ein Projekt von Prof. Dr. Ulf
     Pillkahn" → pillkahn.de rein; nackte Domainlinks im Fuß entfernen
  4. Cache-Buster für style.css

Aufruf im Repo-Root:   python3 pflege/seo.py
Bricht ab, wenn ein Title > 60 oder eine Description > 155 Zeichen hat.
"""

import html
import json
import os
import re
import sys

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://operation-zukunft.de"
HEUTE = "2026-11-11"
CSS_VERSION = "2026-11-11b"

# ------------------------------------------------------------------ Kanon
PERSON_ID = "https://pillkahn.de/#person"
ORG_ID = "https://operation-zukunft.de/#organization"
SITE_ID = "https://operation-zukunft.de/#website"

# Schlanker Personenknoten — der vollständige lebt auf pillkahn.de.
PERSON = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": "Ulf Pillkahn",
    "honorificPrefix": "Prof. Dr.",
    "url": "https://pillkahn.de/",
    "worksFor": {"@id": ORG_ID},
}

# Werte aus dem bisherigen @graph (PR #1) übernommen; neu sind nur die
# kanonische @id, founder per @id auf pillkahn.de und der Wegfall von sameAs
# (dort stand mit picturesoftomorrow.com eine eigene Domain).
ORG = {
    "@type": "ProfessionalService",
    "@id": ORG_ID,
    "name": "Operation Zukunft",
    "url": "https://operation-zukunft.de/",
    "logo": "https://operation-zukunft.de/videos/hero-poster.jpg",
    "image": "https://operation-zukunft.de/videos/hero-poster.jpg",
    "description": ("Beratung für Corporate Foresight, strategische Frühaufklärung und "
                    "KI-gestützte Strategieentwicklung; Aufbau und Betrieb von KI-Agenten "
                    "für Agentic und Continuous Foresight."),
    "founder": {"@id": PERSON_ID},
    "email": "info@operation-zukunft.de",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Maxhofstraße 28",
        "postalCode": "81475",
        "addressLocality": "München",
        "addressCountry": "DE",
    },
    "areaServed": ["DE", "AT", "CH"],
    "knowsAbout": [
        "Corporate Foresight", "Strategische Vorausschau", "Strategische Frühaufklärung",
        "KI-Frühwarnsysteme", "Agentic Foresight", "Continuous Foresight",
        "Szenarioentwicklung", "KI-gestützte Strategieentwicklung", "KI-Agenten",
        "Innovationsmanagement",
    ],
}

SITE = {
    "@type": "WebSite",
    "@id": SITE_ID,
    "url": "https://operation-zukunft.de/",
    "name": "Operation Zukunft",
    "inLanguage": "de-DE",
    "about": {"@id": ORG_ID},
    "publisher": {"@id": ORG_ID},
    "author": {"@id": PERSON_ID},
}

LEISTUNGEN = [
    {
        "@type": "Service",
        "@id": "https://operation-zukunft.de/#workshop",
        "name": "Orientierungsworkshop: KI für Innovation und Foresight",
        "serviceType": "Beratung",
        "description": ("Standortbestimmung zum KI-Einsatz in Innovation und Foresight: halb- "
                        "oder ganztägiger Workshop mit dem Führungs- oder Innovationsteam, vor Ort "
                        "oder remote. Ergebnis: priorisierte Einsatzfelder, ein Fahrplan zur "
                        "Befähigung der Teams und ein konkreter nächster Schritt."),
        "url": "https://operation-zukunft.de/#angebote",
        "areaServed": ["DE", "AT", "CH"],
        "provider": {"@id": ORG_ID},
        "offers": {
            "@type": "Offer",
            "priceCurrency": "EUR",
            "priceSpecification": {
                "@type": "PriceSpecification",
                "minPrice": 1500,
                "priceCurrency": "EUR",
                "valueAddedTaxIncluded": False,
            },
        },
    },
    {
        "@type": "Service",
        "@id": "https://operation-zukunft.de/#agenten",
        "name": "KI-Agenten für Innovation und Foresight",
        "serviceType": "Aufbau und Betrieb von KI-Agenten",
        "description": ("Konzeption, Aufbau, Inbetriebnahme und laufender Betrieb eines "
                        "Agenten-Systems für Recherche, Trendbeobachtung, Frühaufklärung und "
                        "Szenarien – Continuous Foresight statt einmaliger Studie."),
        "url": "https://operation-zukunft.de/#angebote",
        "areaServed": ["DE", "AT", "CH"],
        "provider": {"@id": ORG_ID},
    },
]

# Dieselben @ids wie auf pillkahn.de/publikationen/, damit Google beide
# Fundstellen als dasselbe Werk zusammenführt.
BUECHER = [
    {
        "@type": "Book",
        "@id": "https://pillkahn.de/publikationen/#automated-future",
        "name": "The Automated Future",
        "author": {"@id": PERSON_ID},
        "isbn": "9798254694953",
        "description": ("Wie KI Foresight, Strategieplanung und Innovationsmanagement "
                        "revolutioniert. Mit Kapitel zu OpenClaw."),
        "inLanguage": "de",
        "bookFormat": "https://schema.org/Paperback",
    },
    {
        "@type": "Book",
        "@id": "https://pillkahn.de/publikationen/#flipped-foresight-buch",
        "name": "Flipped Foresight",
        "alternateName": "Flipped Foresight – Wie Maschinen Zukünfte entwerfen und Menschen entscheiden",
        "author": {"@id": PERSON_ID},
        "description": ("Wie Maschinen Zukünfte entwerfen und Menschen entscheiden. KI-gestützte "
                        "Szenarioarbeit: Referenzmodell mit 4 Phasen und 5 Prinzipien, "
                        "Szenario-Engine zum Nachbauen."),
        "creativeWorkStatus": "Erscheint 2026",
        "inLanguage": "de",
    },
]

HERO = {"url": DOMAIN + "/videos/hero-poster.jpg", "w": 1920, "h": 1080,
        "alt": "Operation Zukunft – Foresight und KI-Agenten"}
CLUSTER_BILD = {"url": DOMAIN + "/videos/cluster-poster.jpg", "w": 1920, "h": 1080,
                "alt": "Das Agenten-Cluster von Operation Zukunft"}
FILM_BILD = {"url": DOMAIN + "/videos/szenariofilme/szenariofilm-poster.jpg", "w": 1920, "h": 1080,
             "alt": "Szenarien als Film"}

# ------------------------------------------------------------------ Seiten
# title/desc None = bisherigen Wert aus der Datei behalten
SEITEN = [
    {"datei": "index.html", "pfad": "/", "title": None, "desc": None,
     "og": "website", "bild": HERO, "art": "start"},
    {"datei": "cluster.html", "pfad": "/cluster.html", "title": None,
     "desc": ("Fünf Mac Minis, fünf KI-Agenten: Recherche, Szenarien und Veröffentlichung im "
              "Dauerbetrieb – der laufende Proof of Concept für Foresight-Agenten."),
     "og": "website", "bild": CLUSTER_BILD, "art": "seite"},
    {"datei": "szenariofilme.html", "pfad": "/szenariofilme.html", "title": None,
     "desc": ("Szenarien als Film: vier Zukünfte, vier kurze Filme, ein direkter Vergleich. "
              "Für Strategieworkshops, Führungskreise und interne Kommunikation."),
     "og": "website", "bild": FILM_BILD, "art": "seite"},
    {"datei": "blog/dilemma-organisationen.html",
     "title": "Das Innovationsdilemma in Organisationen | Operation Zukunft",
     "desc": ("Organisationen stellen die smartesten Leute ein, um ihnen dann zu erklären, was "
              "zu tun ist. Warum das Innovation verhindert und was KI-Agenten ändern.")},
    {"datei": "blog/einstein-openclaw.html",
     "title": "Warum Einstein OpenClaw genutzt hätte | Operation Zukunft",
     "desc": ("Ein Gedankenversuch: Warum Albert Einstein der ultimative OpenClaw-Nutzer gewesen "
              "wäre – und was das über den Umgang mit Komplexität verrät.")},
    {"datei": "blog/hype-openclaw.html",
     "title": "Der Hype um OpenClaw – gerechtfertigt? | Operation Zukunft",
     "desc": ("OpenClaw ist ein autonomer KI-Agent, gesteuert über WhatsApp oder Telegram, der "
              "echte Aufgaben auf dem Rechner ausführt. Funktionen und Einordnung.")},
    {"datei": "blog/lebenszyklus-innovationen.html",
     "title": "Der Lebenszyklus von Innovationen | Operation Zukunft",
     "desc": None},
    {"datei": "blog/pictures-of-the-future.html",
     "title": "Pictures of the Future: Zukunftsbilder | Operation Zukunft",
     "desc": ("Die Pictures-of-the-Future-Methodik: Wie Unternehmen Zukunftsbilder entwickeln "
              "und für ihre Strategie nutzen. Erfahrungen aus der Praxis bei Siemens.")},
    {"datei": "blog/red-queen-effekt.html",
     "title": "Der Red-Queen-Effekt in Unternehmen | Operation Zukunft",
     "desc": ("Warum Unternehmen trotz ständiger Innovation nicht vorankommen – und wie man dem "
              "Hamsterrad der inkrementellen Verbesserung entkommt.")},
    {"datei": "blog/strategieplanung-ki.html",
     "title": "KI in der Strategieplanung | Operation Zukunft",
     "desc": ("Wie KI-Agenten die Strategieplanung verändern: von der jährlichen "
              "PowerPoint-Schlacht zum permanenten Echtzeit-Prozess.")},
    {"datei": "blog/warum-prognosen-scheitern.html",
     "title": "Warum Prognosen scheitern | Operation Zukunft",
     "desc": None},
    {"datei": "blog/index.html", "pfad": "/blog/", "title": None, "desc": None,
     "og": "website", "bild": HERO, "art": "seite"},
    {"datei": "blog/corporate-foresight-ki.html", "veroeffentlicht": "2026-04-01",
     "title": None, "desc": None},
    {"datei": "blog/szenarioentwicklung-ki.html", "veroeffentlicht": "2026-05-01",
     "title": None, "desc": None},
    {"datei": "blog/schwache-signale-ki-agenten.html", "veroeffentlicht": "2026-06-01",
     "title": None, "desc": None},
    {"datei": "blog/ki-agenten-einfuehren-fehler.html", "veroeffentlicht": "2026-07-01",
     "title": None, "desc": None},
    {"datei": "blog/flipped-foresight-methode.html", "veroeffentlicht": "2026-08-01",
     "title": None, "desc": None},
    {"datei": "blog/abbruchkriterien-innovationsprojekte.html", "veroeffentlicht": "2026-09-01",
     "title": None, "desc": None},
    {"datei": "blog/technologiereife-einschaetzen.html", "veroeffentlicht": "2026-10-01",
     "title": None, "desc": None},
    {"datei": "blog/szenarien-als-film.html", "veroeffentlicht": "2026-11-12",
     "title": None, "desc": None},
    {"datei": "blog/was-ist-zukunftsforschung.html", "veroeffentlicht": "2026-11-14",
     "title": None, "desc": None,
     # Video 19 (ProfAndPrompt), selbst gehostet auf pillkahn.de, zusätzlich auf YouTube
     "zusatz": [{"@type": "VideoObject", "@id": "https://operation-zukunft.de/blog/was-ist-zukunftsforschung.html#video", "name": "Was ist Zukunftsforschung? Methoden, Grenzen und die Rolle von KI", "description": "Zukunftsforschung ist die wissenschaftliche Untersuchung möglicher, wahrscheinlicher und wünschbarer Zukünfte – mit dem Ziel, heute bessere Entscheidungen zu treffen. Das Video erklärt die drei Philosophien des Fachs (Vorhersagen, Erkunden, Gestalten), seine Grenzen und die Rolle von KI.", "thumbnailUrl": "https://operation-zukunft.de/videos/zukunftsforschung-poster.jpg", "uploadDate": "2026-11-14", "duration": "PT5M57S", "contentUrl": "https://pillkahn.de/media/zukunftsforschung-1080p.mp4", "embedUrl": "https://www.youtube.com/embed/lWqYWYmL73A", "sameAs": "https://www.youtube.com/watch?v=lWqYWYmL73A", "inLanguage": "de", "transcript": "Niemand kann die Zukunft verlässlich vorhersagen. Kein Experte, kein Algorithmus, keine Glaskugel. Und trotzdem gibt es eine Wissenschaft, die sich mit nichts anderem beschäftigt. Ich bin Prof. Dr. Ulf Pillkahn von Operation Zukunft. Meine Kurzdefinition: Zukunftsforschung ist die wissenschaftliche Untersuchung möglicher, wahrscheinlicher und wünschbarer Zukünfte – mit dem Ziel, heute bessere Entscheidungen zu treffen. Zukünfte, im Plural. In diesem Wort steckt das ganze Fach. Es gibt nicht die eine Zukunft, die auf uns wartet. Es gibt viele. Der Begriff ist jünger, als man denkt: 1943 prägt der Politologe Ossip Flechtheim im amerikanischen Exil das Wort Futurologie. Seine Aufgaben: voraussagen, gestalten, kritisieren. Danach geht es schnell. In Kalifornien denkt die RAND Corporation über das Undenkbare nach, und Herman Kahn holt ein Wort aus der Filmwelt in die Strategie: Szenario. In Frankreich begründet Gaston Berger la prospective: nach vorn schauen, um heute zu handeln. Und Robert Jungk holt die Zukunft mit seinen Zukunftswerkstätten zu den Bürgern. Aus diesen Wurzeln wachsen drei Philosophien. Sie unterscheiden sich vor allem in einer Frage: Was ist die Zukunft eigentlich? Erste Antwort: Die Zukunft ist eine Fortsetzung der Gegenwart. Wer die Muster kennt, kann sie berechnen. Das ist die Welt der Prognose. Ihr Gegenstand: das Wahrscheinliche. Ihre Werkzeuge: Trendextrapolation, mathematische Modelle, die Delphi-Methode mit ihren Expertenrunden. Heute auch Superforecasting. Stark, wo Systeme stabil sind. Blind am Wendepunkt. Zweite Antwort: Die Zukunft ist offen. Es gibt viele, und keine lässt sich ausrechnen. Das ist die Welt der Szenarien. Ihr Gegenstand: das Mögliche. Szenariotechnik, Wild Cards, Cross-Impact-Analysen. So hat Shell die Ölkrise von 1973 durchgespielt, bevor sie kam. Nicht vorhergesagt. Durchgespielt. Dritte Antwort: Die Zukunft wird gemacht. Sie ist keine Landschaft, die man erkundet, sondern ein Haus, das man baut. Ihr Gegenstand: das Wünschbare. Hier arbeitet man mit Visionen und Backcasting: vom gewünschten Ziel rückwärts bis zum ersten Schritt heute. Und mit Workshops, in denen Betroffene selbst entwerfen. Das eigentliche Problem sind selten die Methoden, sondern die Verwechslung. Wer ein Szenario liest wie eine Prognose, hat beides missverstanden. Wer eine Vision für einen Plan hält, auch. Warum ist Zukunftsforschung so schwer? Weil ihr Gegenstand nicht existiert. Es gibt keine Daten aus der Zukunft. Kein Labor, kein Archiv, keine Messung. Für eine Wissenschaft ist das unbequem: Eine Aussage über 2040 kann heute niemand bestätigen oder widerlegen. Prüfen lässt sie sich erst, wenn es zu spät ist. Karl Popper hat daraus ein hartes Argument gemacht: Wenn wir nicht wissen können, was wir morgen wissen werden, können wir auch den Lauf der Geschichte nicht vorhersagen. Dazu kommt: Zukunftsaussagen verändern die Zukunft. Eine ernst genommene Warnung verhindert, wovor sie warnt. Eine Prophezeiung, an die alle glauben, erfüllt sich selbst. Und die Experten? Philip Tetlock hat zwanzig Jahre lang ihre Prognosen gesammelt. Viele lagen kaum besser als der Zufall, die bekanntesten oft am deutlichsten daneben. Deshalb misst sich gute Zukunftsforschung nicht an Treffern, sondern an Qualität: Sind die Annahmen offengelegt? Ist das Bild in sich stimmig? Ist der Weg dorthin nachvollziehbar? Genau hier beginnt das Problem der Unternehmen. Erstens: Sie berichten in Quartalen, Zukunftsforschung denkt in Jahrzehnten. Zwei Uhren, zwei Takte. Zweitens: Foresight liefert keine Zahl fürs Budget, sondern Optionen. Und Optionen passen schlecht in eine Tabelle mit einer einzigen Zeile für das nächste Jahr. Drittens: Ihr Ertrag ist unsichtbar. Der größte Erfolg ist die Krise, die nicht eintritt, weil man vorbereitet war. Dafür bekommt niemand einen Bonus. Und viertens fehlt oft der Anschluss an Entscheidungen. Die Studie ist brillant, die Präsentation gelungen. Die Manager nicken höflich. Und planen weiter wie bisher. Lohnt sich das trotzdem? René Rohrbeck und Ménès Kum haben 83 Unternehmen sieben Jahre lang verfolgt. Die gut vorbereiteten waren um ein Drittel profitabler, ihr Börsenwert wuchs um 200 Prozent stärker als der Durchschnitt. Vorbereitet sein heißt nicht, recht zu haben. Es heißt, eine Überraschung schon einmal durchdacht zu haben. Und sich deshalb schneller anpassen zu können als die anderen. Und jetzt kommt KI ins Spiel. Sie liest in Stunden, wofür ein Team Monate braucht: Studien, Patente, schwache Signale. Sie entwirft Szenarien und prüft sie auf Widersprüche. Aber sie hat eine Schwäche: Sie liefert das Wahrscheinliche. Den Mittelwert dessen, was schon oft gesagt wurde. Und Zukunftsforschung lebt gerade von der Abweichung. Deshalb drehe ich die Arbeitsteilung um. Ich nenne das Flipped Foresight: Die Maschine entwirft die Breite, Hunderte Zukünfte. Der Mensch prüft, wählt aus und entscheidet. So wird aus dem Foresight-Projekt, das sechs Monate dauert und dann im Regal steht, ein laufender Prozess. Dauerbeobachtung statt Studie. Die Zukunft lässt sich nicht vorhersagen. Aber man kann vorbereitet sein. Wie das in deinem Unternehmen aussehen kann, zeige ich auf operation-zukunft.de.", "author": {"@id": "https://pillkahn.de/#person"}, "publisher": {"@id": "https://operation-zukunft.de/#organization"}, "hasPart": [{"@type": "Clip", "name": "Was ist Zukunftsforschung?", "startOffset": 0, "endOffset": 37, "url": "https://operation-zukunft.de/blog/was-ist-zukunftsforschung.html?t=0"}, {"@type": "Clip", "name": "Woher das Fach kommt", "startOffset": 37, "endOffset": 75, "url": "https://operation-zukunft.de/blog/was-ist-zukunftsforschung.html?t=37"}, {"@type": "Clip", "name": "Drei Philosophien", "startOffset": 75, "endOffset": 166, "url": "https://operation-zukunft.de/blog/was-ist-zukunftsforschung.html?t=75"}, {"@type": "Clip", "name": "Warum Zukunftsforschung so schwer ist", "startOffset": 166, "endOffset": 230, "url": "https://operation-zukunft.de/blog/was-ist-zukunftsforschung.html?t=166"}, {"@type": "Clip", "name": "Warum Unternehmen sich schwertun", "startOffset": 230, "endOffset": 272, "url": "https://operation-zukunft.de/blog/was-ist-zukunftsforschung.html?t=230"}, {"@type": "Clip", "name": "Lohnt sich Foresight?", "startOffset": 272, "endOffset": 296, "url": "https://operation-zukunft.de/blog/was-ist-zukunftsforschung.html?t=272"}, {"@type": "Clip", "name": "Die Rolle von KI", "startOffset": 296, "endOffset": 341, "url": "https://operation-zukunft.de/blog/was-ist-zukunftsforschung.html?t=296"}, {"@type": "Clip", "name": "Fazit", "startOffset": 341, "endOffset": 352, "url": "https://operation-zukunft.de/blog/was-ist-zukunftsforschung.html?t=341"}]}]},
]
for s in SEITEN:
    if s["datei"].startswith("blog/"):
        s.setdefault("pfad", "/" + s["datei"])
        s.setdefault("og", "article")
        s.setdefault("bild", HERO)
        s.setdefault("art", "blog")

# Nur Fuß und Cache-Buster (noindex-Seiten, Inhalt bleibt unberührt)
NUR_FUSS = ["datenschutz.html", "stats.html"]


# ------------------------------------------------------------------ Bausteine
def alt_wert(text, muster):
    m = re.search(muster, text, re.S)
    return html.unescape(m.group(1).strip()) if m else None


def kopfblock(s, title, desc, url):
    e = lambda t: html.escape(t, quote=True)
    b = s["bild"]
    z = [
        f'    <title>{e(title)}</title>',
        f'    <meta name="description" content="{e(desc)}">',
        f'    <link rel="canonical" href="{url}">',
        f'    <meta property="og:type" content="{s["og"]}">',
        '    <meta property="og:site_name" content="Operation Zukunft">',
        '    <meta property="og:locale" content="de_DE">',
        f'    <meta property="og:url" content="{url}">',
        f'    <meta property="og:title" content="{e(title)}">',
        f'    <meta property="og:description" content="{e(desc)}">',
        f'    <meta property="og:image" content="{b["url"]}">',
        f'    <meta property="og:image:width" content="{b["w"]}">',
        f'    <meta property="og:image:height" content="{b["h"]}">',
        f'    <meta property="og:image:alt" content="{e(b["alt"])}">',
    ]
    if s["og"] == "article":
        z.append(f'    <meta property="article:published_time" content="{s["veroeffentlicht"]}">')
        z.append('    <meta property="article:author" content="https://pillkahn.de/">')
    z += [
        '    <meta name="twitter:card" content="summary_large_image">',
        '    <meta name="twitter:creator" content="@Ulf_Pillkahn">',
        f'    <meta name="twitter:title" content="{e(title)}">',
        f'    <meta name="twitter:description" content="{e(desc)}">',
        f'    <meta name="twitter:image" content="{b["url"]}">',
        f'    <meta name="twitter:image:alt" content="{e(b["alt"])}">',
    ]
    return "\n".join(z)


def graph(s, title, desc, url):
    seite = {
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": title,
        "description": desc,
        "inLanguage": "de-DE",
        "isPartOf": {"@id": SITE_ID},
        "about": {"@id": ORG_ID},
        "dateModified": HEUTE,
    }
    knoten = [PERSON, ORG, SITE]
    if s["art"] == "start":
        seite["mainEntity"] = {"@id": ORG_ID}
        knoten += [seite] + LEISTUNGEN + BUECHER
    elif s["art"] == "seite":
        knoten.append(seite)
    elif s["art"] == "blog":
        # Inhalt unverändert: dateModified bleibt das Erscheinungsdatum
        seite["dateModified"] = s["veroeffentlicht"]
        artikel = {
            "@type": "BlogPosting",
            "@id": url + "#article",
            "headline": s["headline"],
            "description": desc,
            "url": url,
            "mainEntityOfPage": {"@id": url + "#webpage"},
            "isPartOf": {"@id": SITE_ID},
            "datePublished": s["veroeffentlicht"],
            "dateModified": s["veroeffentlicht"],
            "inLanguage": "de-DE",
            "image": HERO["url"],
            "author": {"@id": PERSON_ID},
            "publisher": {"@id": ORG_ID},
        }
        knoten += [seite, artikel] + s.get("zusatz", [])
    daten = {"@context": "https://schema.org", "@graph": knoten}
    text = json.dumps(daten, ensure_ascii=False, indent=2)
    text = "\n".join("    " + z for z in text.splitlines())
    return ('    <!-- Strukturdaten: generiert von pflege/seo.py nach dem Cluster-Standard -->\n'
            '    <script type="application/ld+json">\n' + text + '\n    </script>\n')


# Ganzer Satz als Link: übernimmt so den Stil der übrigen Fußlinks auch in den
# Blogbeiträgen, die jeweils eigenes CSS mitbringen.
FUSS_HINWEIS = '<a href="https://pillkahn.de/">Ein Projekt von Prof. Dr. Ulf Pillkahn</a>'


def fuss(t):
    """Im <footer>: Personenlink auf pillkahn.de, nackte Domainlinks raus."""
    def ersetzen(m):
        f = m.group(0)
        f = re.sub(r'<a href="https?://(?:www\.)?pillkahn\.com/?"[^>]*>pillkahn\.com</a>',
                   FUSS_HINWEIS, f)
        f = re.sub(r'<span class="cluster-hinweis">.*?</span>', FUSS_HINWEIS, f)
        f = re.sub(r'\n?[ \t]*<a href="https?://(?:www\.)?'
                   r'(picturesoftomorrow\.com|innovation-review\.de|pillkahn\.cloud)/?"[^>]*>'
                   r'\1</a>', '', f)
        return f
    return re.sub(r"<footer.*?</footer>", ersetzen, t, flags=re.S)


def css(t):
    return re.sub(r'(style\.css)\?v=[0-9a-z-]+', r'\1?v=' + CSS_VERSION, t)


# ------------------------------------------------------------------ Lauf
def main():
    zu_lang = []
    for s in SEITEN:
        p = os.path.join(BASIS, s["datei"])
        t = open(p, encoding="utf-8").read()
        kopf = t[:t.index("</head>")]

        title = s["title"] or alt_wert(kopf, r"<title>(.*?)</title>")
        desc = s["desc"] or alt_wert(kopf, r'<meta name="description" content="([^"]*)"')
        if len(title) > 60:
            zu_lang.append(f'{s["datei"]}: Title {len(title)}')
        if len(desc) > 155:
            zu_lang.append(f'{s["datei"]}: Description {len(desc)}')
        if s["art"] == "blog":
            s["headline"] = re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S).group(1)).strip()
            s["headline"] = html.unescape(re.sub(r"\s+", " ", s["headline"]))
            # Neue Beiträge bringen das Datum in SEITEN mit, alte tragen es im Graph
            if "veroeffentlicht" not in s:
                s["veroeffentlicht"] = re.search(r'"datePublished":\s*"([^"]+)"', kopf).group(1)
        s["_title"], s["_desc"] = title, desc
    if zu_lang:
        sys.exit("Zu lang:\n  " + "\n  ".join(zu_lang))

    for s in SEITEN:
        p = os.path.join(BASIS, s["datei"])
        t = open(p, encoding="utf-8").read()
        kopf, rest = t[:t.index("</head>")], t[t.index("</head>"):]
        url = DOMAIN + s["pfad"]

        # 1. alte Metadaten und Strukturdaten raus
        for muster in [r"<title>.*?</title>",
                       r'<meta name="(?:description|keywords|author)"[^>]*>',
                       r'<link rel="canonical"[^>]*>',
                       r'<meta property="(?:og|article):[^"]*"[^>]*>',
                       r'<meta name="twitter:[^"]*"[^>]*>',
                       r'<!-- Strukturdaten: generiert[^\n]*-->',
                       r'<script type="application/ld\+json">.*?</script>']:
            kopf = re.sub(r"\n?[ \t]*" + muster, "", kopf, flags=re.S)
        # 2. neuen Block hinter viewport, Graph vor </head>
        vp = re.search(r'<meta name="viewport"[^>]*>', kopf)
        kopf = kopf[:vp.end()] + "\n" + kopfblock(s, s["_title"], s["_desc"], url) + kopf[vp.end():]
        kopf = kopf.rstrip() + "\n" + graph(s, s["_title"], s["_desc"], url)
        t = kopf + rest
        # 3. Fuß, 4. CSS
        t = css(fuss(t))
        open(p, "w", encoding="utf-8").write(t)
        print(f'  {s["datei"]:38s} Title {len(s["_title"]):2d}  Desc {len(s["_desc"]):3d}')

    for d in NUR_FUSS:
        p = os.path.join(BASIS, d)
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(css(fuss(t)))
        print(f"  {d:38s} nur Fuß und Cache-Buster")


if __name__ == "__main__":
    main()
