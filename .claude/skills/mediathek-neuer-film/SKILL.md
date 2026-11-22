---
name: mediathek-neuer-film
description: Bindet einen neuen Film der Reihe „Foresight erklärt“ in die Mediathek von operation-zukunft.de ein (Videoseite, Übersicht, Startseite, Sitemaps, llms.txt, „Weiter in der Reihe“, Linksätze in passenden Artikeln). Trigger: „neuer Film für die Mediathek“, „Video X in die Mediathek“, „Film 2/3/4 veröffentlichen“, „neues Video auf operation-zukunft.de einbinden“.
---

# Neuer Film in die Mediathek „Foresight erklärt“

Arbeitet im Repo von operation-zukunft.de. Grundlage: `videos/NEUER-FILM.md` (Checkliste) und der
Generator `pflege/videos/build.py`. Die Videoseiten werden NIE von Hand geschrieben, nur über die Daten
in `pflege/videos/filme/<slug>/`.

## Regeln

- Keine erfundenen Fakten, Zahlen oder Zitate. Alle Texte (Antwortabsatz, „Worum es geht“, Kartensatz,
  Beschreibung) nur aus Transkript und Bestand verdichten. Neue Formulierungen im Bericht zum Gegenlesen markieren.
- Kein YouTube-iframe (Cookies). Player = eigenes `<video>`, mp4 liegt auf pillkahn.de/media/.
- Nur veröffentlichte Filme bekommen eine Seite. Keine Platzhalterseiten.
- Eigener Branch (`film-<slug>`), kein Push und kein Deploy ohne ausdrückliches OK.
- JSON-LD-@ids: Person https://pillkahn.de/#person, Organisation https://operation-zukunft.de/#organization,
  Reihe https://operation-zukunft.de/videos/#reihe (kommt aus `pflege/seo.py` und `build.py`, nicht ändern).

## Ablauf

1. **Angaben einsammeln** (Tabelle in `videos/NEUER-FILM.md`). Fehlt etwas, gezielt nachfragen.
   YouTube-Beschreibung oder Skript des Films sind gute Quellen für Kapitel und Transkript.
   Beim Skill `profandprompt-video-produktion` entstehen Skript, Kapitel und Untertitel. Dort nachsehen, falls angegeben.
2. **Dateien prüfen**, bevor etwas gebaut wird:
   - `curl -sI -r 0-1 <mp4-URL>` → 206 und `video/mp4`; Dauer bei Bedarf mit `ffprobe` aus der URL lesen
   - Poster (JPG 16:9, ≥ 1280×720) und VTT liegen in `videos/`; die VTT beginnt mit `WEBVTT`
3. **Datensatz anlegen**:
   - `pflege/videos/filme/<slug>/film.json`: Muster ist `filme/was-ist-zukunftsforschung/film.json`.
     `seitentitel` ≤ 60 Zeichen (Form „<Titel> – Video | Operation Zukunft“), `meta_description` ≤ 155,
     `antwort` 40–60 Wörter mit dem Kernsatz in `<strong>`, `worum_es_geht` 3–5 Sätze,
     `dauer_sekunden` als Zahl, `seite_stand` = heute. `alte_url` nur, wenn der Film vorher woanders stand.
   - `pflege/videos/filme/<slug>/transkript.md`: je Kapitel `## <Kapitelname>` + Absätze.
     Kapitelnamen gleich wie in `kapitel`.
   - Slug und Titel in `pflege/videos/reihe.json` an den Film anpassen (Reihenfolge nicht ändern,
     außer der Auftrag sagt es).
4. **Bauen**: `python3 pflege/videos/build.py`. Der Generator ändert Videoseite, Übersicht,
   „Weiter in der Reihe“ auf allen Videoseiten, Startseitenabschnitt, `sitemap.xml`,
   `video-sitemap.xml`, `llms.txt`.
5. **Linksätze** (je ein Satz, nur wo es inhaltlich passt): Szenarien → Leitseite `szenarioentwicklung-mit-ki`,
   `blog/szenarien-als-film.html`, ggf. `szenariofilme.html`; Trends → `blog/schwache-signale-ki-agenten.html`,
   `blog/technologiereife-einschaetzen.html`; KI und Foresight → Leitseite `corporate-foresight`,
   `blog/flipped-foresight-methode.html`, `cluster.html`. Erst den Artikel lesen, dann entscheiden.
   Leitseiten liegen unter `pflege/leitseiten/seiten/<slug>/inhalt.html` (Videohinweis über das Feld `video` in `seite.json`).
   Artikel aus `pflege/blog/artikel.py` dort ändern und danach `python3 pflege/blog/build.py .`,
   `python3 pflege/seo.py` und noch einmal `python3 pflege/videos/build.py` laufen lassen.
6. **Prüfen**:
   - `python3 pflege/videos/pruefen.py` muss „Alles in Ordnung.“ melden.
   - Ein zweiter Lauf aller drei Generatoren darf keine Datei mehr ändern (Idempotenz).
   - Lokale Vorschau: `.claude/launch.json` → `mediathek-vorschau` (Port 8000). Neue Videoseite bei 1440×900
     und 390×844 ansehen: Der Player muss ohne Scrollen sichtbar sein. Einen Kapitellink klicken und prüfen,
     dass `currentTime` springt.
7. **Bericht und Haltepunkt**: Änderungen je Datei, alle neuen Texte zum Gegenlesen, offene Punkte.
   Dann auf OK warten.
8. **Nach OK**: Commit, Push auf `main` (GitHub Pages), Live-Prüfung mit curl (neue Seite 200,
   `/videos/` 200, `video-sitemap.xml` 200 als XML), Eintrag in `CHANGELOG.md`.
   Erinnern: URL-Prüfung der neuen Seite in der Google Search Console; in YouTube Studio die erste Zeile
   der Beschreibung auf die Videoseite setzen, den Film in die Playlist „Foresight erklärt“ aufnehmen und
   den Abspann des Vorgängerfilms auf den neuen Film zeigen lassen.
