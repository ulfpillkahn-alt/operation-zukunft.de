# Changelog operation-zukunft.de

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
