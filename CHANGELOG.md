# Changelog operation-zukunft.de

## 2026-11-23 – Mediathek: Film 3 „Der Pearl-Harbor-Effekt“

Commit `2253641`, live seit 2026-11-23. YouTube `Jy-NL_2-KJ0`. Rollback: `git revert 2253641`.

- Neu: `/videos/pearl-harbor-effekt/` mit eigenem Player, 6 Kapiteln, Untertiteln und Transkript
  (Wortlaut der Untertitel). mp4 auf `pillkahn.de/media/pearl-harbor-effekt-1080p.mp4` (Webfassung aus
  der Fassung ohne eingebrannte Untertitel, 29 MB). CTA auf den Workshop `/#pearl-harbor`.
- Reihe: als Film 3 eingeschoben; „Foresight mit Trends“ und „Wie KI Foresight verändert“ jetzt 4 und 5.
  Hinweis: Film 2 kündigt im Abspann „Foresight mit Trends“ als nächsten Film an.
- Übersicht, Startseite („Neueste Folge“), „Weiter in der Reihe“, `sitemap.xml`, `video-sitemap.xml`,
  `llms.txt` über den Generator; Linksätze in `schwache-signale-ki-agenten` und `flipped-foresight-methode`.
- Leitseiten: Der Blog-Generator baut sie mit und hätte die Angebotsnamen (Pearl Harbor, Sputnik) in
  ihr JSON-LD übernommen. Seit `66a06b5` legt `pflege/leitseiten/build.py` (`NAME_LEITSEITE`) dort die
  beschreibenden Namen fest; die neuen Namen stehen nur auf der Startseite (Entscheidung 23.11.2026).
- Live geprüft (curl): Seite, Übersicht, Poster, VTT (`text/vtt`), Sitemaps (`application/xml`) 200,
  mp4 206 `video/mp4`; Teaser auf der Startseite und beide Blog-Links live.

## 2026-11-23 – Angebotsnamen „Pearl Harbor“ und „Sputnik“

Commit `c28afe9`, live seit 2026-11-23. Rollback: `git revert c28afe9`, Sicherungs-Tag `pre-angebotsnamen-2026-11-23`.

- Startseite, Angebotskarten: Name als `<span class="pn-name">` in der bestehenden Überschrift (Titel wörtlich
  unverändert), darunter Erklärzeile `<p class="pn-zeile">`; Karten-IDs `#pearl-harbor` und `#sputnik`.
- Mail-Betreffs: „Anfrage Pearl Harbor – Orientierungsworkshop“, „Anfrage Sputnik – KI-Agenten“ (Body unverändert).
- JSON-LD: `name` der Services `#workshop`/`#agenten` in `pflege/seo.py` (LEISTUNGEN) auf
  „Pearl Harbor – …“ bzw. „Sputnik – …“.
- `style.css`: zwei Regeln `.pn-name`, `.pn-zeile`; `stats.html`: Bezeichnungen um den Namen ergänzt;
  `sitemap.xml`: `/` lastmod 2026-11-23. Zähler-Schlüssel unverändert.
- Offen: Die Leitseiten (foresight-mit-ki-agenten, zukunftsforschung, corporate-foresight) tragen die Services
  noch mit altem Namen; `pflege/leitseiten/build.py` übernimmt die Namen aus `seo.py` beim nächsten Lauf.
  Ihre Mail-Betreffs stehen fest im Generator und lauten noch wie vorher.
- Live geprüft (curl): `/`, `/stats`, `/sitemap.xml` 200; `pn-name` 2×, „Habor“ 0×; JSON-LD mit neuen Namen.

## 2026-11-22 – Leitseiten B–E: Szenariotechnik, Corporate Foresight, Szenarioentwicklung mit KI, Zukunftsforschung

Commit `62f0dc4` (Branch `leitseiten`, auf main übernommen), live seit 2026-11-22. Rollback: `git revert 62f0dc4`,
Sicherungs-Tag `pre-leitseiten-b-e-2026-11-22`. Damit ist der Auftrag „fünf Leitseiten“ (`AUFTRAG.md`) umgesetzt.

- Neu: `/szenariotechnik/` (mit Trichter-Grafik als Inline-SVG, acht Schritten, Musterfall VISEON AG),
  `/corporate-foresight/`, `/szenarioentwicklung-mit-ki/` (mit Tool-Überblick, Stand November 2026) und
  `/zukunftsforschung/` (Dach mit Methodenlandkarte). Quelltext je Seite unter `pflege/leitseiten/seiten/<slug>/`.
- `blog/corporate-foresight-ki.html` und `blog/szenarioentwicklung-ki.html` sind Weiterleitungsseiten auf die
  Leitseiten (Meta-Refresh 0 s, Canonical, kein `noindex`; Feld `ersetzt` in `seite.json`). Beide Artikel sind aus
  `pflege/blog/artikel.py` und `pflege/seo.py` entfernt, der Wortlaut steht in der Git-Historie (bis `8c4214f`).
  `posts.js`, `posts.json` und die Blogübersicht zeigen auf die Leitseiten; der Buchverweis „Trends und Szenarien“
  liegt jetzt auf B und D.
- Startseite: Title „Foresight mit KI für Unternehmen | Operation Zukunft“ (über `seo.py`), neuer Absatz
  `.hero-lead` unter der H1, fünf Karten in `#themen`, fünf Footer-Links.
- Linksätze mit dem Hauptbegriff als Ankertext: `warum-prognosen-scheitern`, `pictures-of-the-future`,
  `szenarien-als-film` (Szenariotechnik); `strategieplanung-ki`, `flipped-foresight-methode` (Corporate Foresight);
  `strategie-pakete.html` (beide). „Weiter im Thema“ auf allen fünf Leitseiten.
- JSON-LD: zusätzliche Service-Knoten in `pflege/leitseiten/build.py` (`LEISTUNGEN_ZUSATZ`): Strategie-Pakete mit
  Preisspanne 4.900–24.900 €, Szenariofilme und Vorträge ohne Preis.
- Fachquellen über Crossref und OpenAlex geprüft (Rohrbeck/Battistella/Huizingh 2015, Rohrbeck/Kum 2018,
  Ansoff 1975, Voros 2003, von Reibnitz 1992), Wack 1985 über die Seite der Harvard Business Review.
- `pflege/leitseiten/pruefen.py`: DOI-Links werden auf Auflösung geprüft (Verlage weisen curl ab).
- `sitemap.xml` (vier neue Leitseiten, die beiden Blog-URLs entfernt), `llms.txt` (fünf Zeilen unter
  „Leitseiten“), sieben neue Zähler-Bezeichnungen in `stats.html` (`leit-pakete`, `leit-szenariofilme`,
  `leit-vortrag`, `leit-person`, `leit-strategy-review`, `leit-vice-versa`, `sp-link-thema`).
- `style.css`: Schrittfolge (`ls-schrittfolge`), Grafik (`ls-grafik`), Karten (`ls-karten`), `.hero-lead`.
- `videos/NEUER-FILM.md` und Skill `mediathek-neuer-film` verweisen auf die Leitseiten statt auf die beiden Artikel.
- Live geprüft (curl): 21 URLs 200; alle fünf Leitseiten mit einer H1, Canonical auf sich selbst, 8 Knoten im
  JSON-LD, 6 Fragen und vier Links unter „Weiter im Thema“; beide Weiterleitungsseiten mit Refresh und Canonical;
  Startseite, Sitemap, `llms.txt`, Blogübersicht, Paketseite und alle fünf Linksätze ausgeliefert.
  15 URLs per IndexNow gemeldet.
- Folgeaufgaben in anderen Repos (nicht umgesetzt): je ein Link mit dem Hauptbegriff auf die passende Leitseite
  in pillkahn.de (dazu `llms.txt`), flipped-foresight.com, squawk.de, picturesoftomorrow.com, agentic-foresight.com.

## 2026-11-22 – Leitseite „Foresight mit KI-Agenten“

Commit `b493006` (Branch `leitseiten`, auf main übernommen), live seit 2026-11-22. Rollback: `git revert b493006`,
Sicherungs-Tag `pre-leitseiten-2026-11-22`. Auftrag: `AUFTRAG.md` (fünf Leitseiten, Stand 22.11.2026), Seite A von fünf.

- Neu: `/foresight-mit-ki-agenten/` – eine Seite für genau einen Suchbegriff: Antwortabsatz, Inhaltsverzeichnis,
  Hauptteil, Angebot (Workshop ab 1.500 €, Agenten auf Anfrage), Belege, sechs Häufige Fragen, Quellen.
  JSON-LD: WebPage, BreadcrumbList, FAQPage und die Service-Knoten der Startseite (`#workshop`, `#agenten`).
- Neu: `pflege/leitseiten/` – `build.py` (Generator), `pruefen.py` (Prüfung nach Schritt 6 des Auftrags, auch für
  den Bestand), Inhalt je Seite unter `seiten/<slug>/` (`seite.json`, `inhalt.html`). Eine Seite erscheint erst
  mit `"live": true` in Menü-Abschnitt, Footer, Sitemap und `llms.txt`.
- Startseite: Abschnitt `#themen` („Foresight zum Nachlesen“) zwischen Leistungen und Videos, generiert.
- Menüpunkt „Themen“ nach „Angebote“ in allen Menüvarianten (Hauptseiten, Videoseiten, neue und alte
  Blogartikel). Datenschutzseite: nur Menü, dabei „Pakete 2027“ nachgetragen.
- Footer-Link auf die Leitseite zwischen `<!-- THEMEN-LINKS -->` (Hauptseiten, Blog, Videoseiten).
- Linksätze mit Ankertext „Foresight mit KI-Agenten“ in `schwache-signale-ki-agenten`,
  `ki-agenten-einfuehren-fehler` (beide über `pflege/blog/artikel.py`) und `cluster.html`.
- `sitemap.xml` (Block „Leitseiten“), `llms.txt` (Abschnitt „Leitseiten“), 21 neue Zähler-Bezeichnungen in
  `stats.html` (`nav-themen`, `themen-karte`, `footer-thema`, `cluster-thema`, `leit-…`).
- `style.css`: Abschnitte 21 (Leitseiten, Präfix `ls-`) und 22 (Themen-Karten, Menü mit neun Einträgen).
  CSS-Cache-Buster `2026-11-22`; `seo.py` `HEUTE` = 2026-11-22.
- Pflege: Reihenfolge `pflege/blog/build.py .` (ruft Leitseiten- und Video-Generator selbst auf) →
  `pflege/seo.py` → `pflege/leitseiten/pruefen.py --links`.
- Live geprüft (curl): 16 URLs 200, Seite A mit einer H1, Canonical auf sich selbst und 8 Knoten im JSON-LD;
  `#themen`, Menü, Sitemap, `llms.txt`, Footer und Linksätze ausgeliefert. Fünf URLs per IndexNow gemeldet.
- Offen: Der SSRN-Link lässt sich nicht automatisch prüfen (Bot-Prüfung bei SSRN).

## 21.11.2026 — IndexNow-Schlüsseldatei

- `f1a8ac42c31a43c9a2be4aa8f3e7db39.txt` im Wurzelverzeichnis (Inhalt genau der Schlüssel, für Bing/IndexNow). Die Meldung läuft über OpenSEO.
  Die Datei nicht löschen oder umbenennen, sonst lehnt IndexNow künftige Meldungen ab (403).

## 2026-11-21 – Bücher verankern (Prompt 13)

Commit `ba5bec8` (Branch `buch-verankerung`, auf main übernommen), live seit 2026-11-21. Rollback: `git revert ba5bec8`.

- JSON-LD nur noch mit Verweisen auf die Book-Knoten von pillkahn.de (`@type`, `@id`, `name`), zentral in
  `pflege/seo.py` (`BUCH`, `buecher()`):
  - `…/trends-und-szenarien/#book`, `…/weisheit-der-roulettekugel/#book`, `…/the-automated-future/#book`,
    `…/publikationen/#flipped-foresight-buch`
  - Startseite: vollständige Book-Knoten entfernt (alte @id `#automated-future`), stattdessen `WebPage.mentions`
    mit allen vier Büchern; Organisation ohne Buchangaben
  - `citation` in sieben Blogartikeln (Feld `zitiert` in `SEITEN`) und auf beiden Videoseiten
    (Feld `weiterlesen` in `film.json`); `strategie-pakete.html`: `Service.subjectOf` → The Automated Future
- Sichtbar: je ein Linksatz in warum-prognosen-scheitern, szenarioentwicklung-ki, red-queen-effekt,
  dilemma-organisationen, lebenszyklus-innovationen (zwei), strategieplanung-ki, ki-agenten-einfuehren-fehler;
  Kasten „Zum Weiterlesen“ auf den Videoseiten; Satz zu den vier Büchern im Abschnitt „Über mich“;
  Satz auf der Paketseite; „Zum Buch“ in der Seitenleisten-Buchbox (Startseite, Cluster, Szenariofilme).
  Amazon-Links unverändert. abbruchkriterien-innovationsprojekte bewusst ohne Satz (Thema trägt es nicht).
- `llms.txt`: Abschnitt „Publikationen“ (Wortlaut wie pillkahn.de/llms.txt) statt der Pauschalzeile.
- Blogartikel ohne neues Änderungsdatum (Entscheidung 21.11.2026); Videoseiten `seite_stand` 2026-11-21.
- Zähler: `buch-ueber`, `buch-seitenleiste`, `sp-link-buch` in `stats.html`. CSS-Cache-Buster `2026-11-21d`.
- Live geprüft (curl): 13 geänderte Seiten und llms.txt 200, JSON-LD gültig, nur Verweise, alle vier @ids exakt.

## 2026-11-21 – Szenariofilme-Seite: Teaser

Commit `9a1866d`, live seit 2026-11-21. Rollback: `git revert 9a1866d`.

- `szenariofilme.html`: Teaser der vier Szenarien (wie im Startseiten-Band) neben „Was Sie erhalten“,
  Bildunterschrift „Die vier Szenarien des Beispiels in 20 Sekunden · KI-generiert, keine Prognose“.
  Desktop zwei gleich breite Spalten, mobil Teaser unter der Liste.
- Start erst bei Sichtbarkeit über das bestehende Kachel-Skript (Selektor um `.film-teaser video` erweitert).
- CSS-Cache-Buster `2026-11-21c` auf allen Seiten.
- Live geprüft (curl): Seite, Stylesheet, Teaser und Poster 200, neues Markup und Skript ausgeliefert.

## 2026-11-21 – Szenariofilm-Band mit Teaser

Commit `ac21ea6`, live seit 2026-11-21. Rollback: `git revert ac21ea6`.

- Startseite: Das Band „Szenarien als Film“ zeigt im linken Drittel einen Teaser
  (`videos/szenariofilme/szenarien-teaser.mp4`, 20,5 s, 960×540, ohne Ton, 1,9 MB): die vier
  Szenariofilme à gut 5 s mit Überblendung und Beschriftung „Szenario n/4 · Name“. Rechts Titel,
  zwei Sätze (aus `szenariofilme.html`), Beispielzeile und „Szenariofilme ansehen →“. Mobil Video oben.
- Ladeverhalten: `preload="none"`, Start erst bei Sichtbarkeit, Pause beim Wegscrollen (Inline-Skript,
  IntersectionObserver); bei „Bewegung reduzieren“ nur das Posterbild. Zähler unverändert `band-szenariofilm`.
- CSS-Cache-Buster `2026-11-21b`.
- Live geprüft: Teaser lädt erst beim Hinscrollen, spielt sichtbar, pausiert beim Wegscrollen.

## 2026-11-21 – Strategie-Pakete 2027 (Light, Safari, Navigator)

Commit `21c2083`, live seit 2026-11-21. Rollback: `git revert 21c2083`, Sicherungs-Tag `pre-strategie-pakete-2026-11-21`.

- Neu: `strategie-pakete.html` mit Kopf und Claim, drei Fragen, Grafik „So läuft Strategie Safari“
  (HTML/CSS, Etappen und Zeitleiste), Paketvergleich, FAQ und Anfrage. Ohne Blog-Leiste (volle Breite).
  JSON-LD von Hand: `Service` mit `OfferCatalog` und drei `Offer` (nicht in `seo.py`, Title 67 Zeichen).
- Black-Week-Aktion über `aktion.js` (Startseite und Paketseite): `[data-bw]` bis 18.12.2026,
  ab 19.12.2026 00:00 Uhr Berlin ausgeblendet, `[data-bw-nach]` eingeblendet.
- Startseite: Brückensatz ohne „Paketlösungen“, Band „Neu für 2027“ im Angebotsraster zwischen Brücke und Karten.
- Navigation „Pakete 2027“ auf Startseite, Cluster, Szenariofilme, Paketseite und (über den Generator) allen
  Videoseiten; `pflege/videos/build.py` kennt den Pfad. Zwischen 901 und 1100 px engerer Menüabstand.
- Steuerhinweis nur in `<span class="sp-steuer">zzgl. USt.</span>`: 4 Fundstellen (Paketseite 3, Startseite 1).
- Zähler: `track.js` zählt `utm_source=google-ads` auch ohne `utm_medium` als Google Ads; 11 neue
  Bezeichnungen in `stats.html`. CSS-Cache-Buster `2026-11-21`; `sitemap.xml` ergänzt.
- Live geprüft: Seiten 200, Band und Navigation verlinkt, „Paketlösungen“ weg; Testaufruf mit
  `?utm_source=google-ads` und Klick „Pakete vergleichen“ erscheinen in /stats (je 1 Testzählung).

## 2026-11-21 – Mediathek: Film 2 „Foresight mit Szenarien“

Commit `dfa0806`, live seit 2026-11-21. YouTube `S5p6pTU4SuE`.

- Neu: `/videos/foresight-mit-szenarien/` mit eigenem Player, 8 Kapiteln, Untertiteln und Transkript
  (Wortlaut der Untertitel). Die mp4 liegt auf `pillkahn.de/media/foresight-mit-szenarien-1080p.mp4`
  (Webfassung, 62 MB, 1,2 Mbit/s wie Film 1, ohne eingebrannte Untertitel). Bis zur Umstellung am selben Tag
  lief der Master `Video20_Foresight-mit-Szenarien_clean_1080p.mp4` (174 MB); er liegt weiter in `/media/`.
- Übersicht `/videos/`, Startseitenabschnitt, „Weiter in der Reihe“, `sitemap.xml`, `video-sitemap.xml`
  und `llms.txt` über den Generator aktualisiert.
- Linksätze in `szenarioentwicklung-ki` und `szenarien-als-film`.
- Live geprüft (curl): neue Seiten 200, Sitemaps als `application/xml`, VTT als `text/vtt`, mp4 206 `video/mp4`;
  Kapitelsprung in der Vorschau geprüft.

## 2026-11-20 – Kontakt: Telefon und robuster E-Mail-Weg

Commit `aeb4427`, live seit 2026-11-20. Rollback: `git revert aeb4427`, Sicherungs-Tag `pre-kontakt-2026-11-20`.

- Telefon `+49 152 3619 1599` (`tel:+4915236191599`) im Kontaktbereich der Startseite, im Footer und Impressum
  (Startseite, Cluster, Szenariofilme, Datenschutz, Videoseiten), unter dem CTA von `szenariofilme.html`
  und im JSON-LD der Organisation (über `pflege/seo.py`, daher auf allen Seiten mit Strukturdaten).
- Startseite: Direktkontakt-Block mit sichtbarer Adresse und „Adresse kopieren“ (Clipboard-API,
  sonst Markieren der Adresse); alle Anfrage-mailtos mit vorbefülltem Body, Betreffs unverändert.
- Zähler: neue Kennungen `telefon-kontakt`, `telefon-footer`, `telefon-szenariofilme`, `mail-direkt`,
  `mail-kopieren`; Bezeichnungen in `stats.html`. `track.js` unverändert (meldet jedes `data-track`).
- Datenschutz Abschnitt 4: „per E-Mail oder Telefon“, Telefonnummer bei den verarbeiteten Daten.
- `sitemap.xml`: `lastmod` der Startseite 2026-11-20; CSS-Cache-Buster `2026-11-20b`.
- Live geprüft: Seiten 200, `tel:`-Links vorhanden, Klick „Adresse kopieren“ erscheint in /stats.

## 2026-11-20 – Mediathek „Foresight erklärt“

Commit `9175342`, live seit 2026-11-20.

- Neu: `/videos/` (Übersicht der Reihe „Foresight erklärt“, Filme 2–4 als „In Vorbereitung“).
- Neu: `/videos/was-ist-zukunftsforschung/` – Film 1 mit eigenem `<video>`-Player (mp4 auf pillkahn.de/media/),
  Kapiteln, Untertiteln, Transkript, VideoObject mit Clips.
- `/blog/was-ist-zukunftsforschung.html` leitet per Meta-Refresh auf die Videoseite weiter.
- „Videos“ in Menü und Footer aller Seiten; Startseitenabschnitt „Foresight erklärt“;
  Linksätze in `warum-prognosen-scheitern`, `corporate-foresight-ki`, `flipped-foresight-methode`.
- Neu: `video-sitemap.xml` (in `robots.txt` eingetragen); `sitemap.xml` und `llms.txt` ergänzt.
- Pflege: Generator und Prüfung in `pflege/videos/`, Checkliste `videos/NEUER-FILM.md`,
  Skill `.claude/skills/mediathek-neuer-film/`.
- Live geprüft (curl): alle neuen URLs 200, Sitemaps als `application/xml`, mp4 206 `video/mp4`,
  Weiterleitung aktiv, `_vorlage` noindex.
