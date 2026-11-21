# Changelog operation-zukunft.de

## 2026-11-21 – Mediathek: Film 2 „Foresight mit Szenarien“

Commit `dfa0806`, live seit 2026-11-21. YouTube `S5p6pTU4SuE`.

- Neu: `/videos/foresight-mit-szenarien/` mit eigenem Player, 8 Kapiteln, Untertiteln und Transkript
  (Wortlaut der Untertitel). Die mp4 liegt auf `pillkahn.de/media/Video20_Foresight-mit-Szenarien_clean_1080p.mp4`
  (174 MB, ohne eingebrannte Untertitel). Eine Webfassung mit 62 MB liegt im Produktionsordner, Umstellung optional.
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
