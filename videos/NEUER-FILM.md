# Neuer Film für die Mediathek „Foresight erklärt“

Kurzweg: In Claude Code im Repo sagen **„Neuer Film für die Mediathek“** (Skill `mediathek-neuer-film`)
und die Angaben unten mitgeben. Der Skill legt den Datensatz an, baut, prüft und hält vor dem Push an.

## 1. Was du lieferst

| Angabe | Beispiel (Film 1) | Hinweis |
|---|---|---|
| Titel (kurz, für H1 und Menü) | Was ist Zukunftsforschung? | Arbeitstitel steht in `pflege/videos/reihe.json` |
| Voller Name (für VideoObject und Sitemap) | Was ist Zukunftsforschung? Methoden, Grenzen und die Rolle von KI | |
| YouTube-ID | `lWqYWYmL73A` | erst nach dem Upload bekannt |
| mp4 auf pillkahn.de | `https://pillkahn.de/media/zukunftsforschung-1080p.mp4` | per FTP nach `/media/` auf All-Inkl, nicht ins Repo (GitHub-Grenze 100 MB) |
| Poster (JPG, 16:9, mind. 1280×720) | `videos/zukunftsforschung-poster.jpg` | kommt ins Repo |
| Untertitel (WebVTT, Deutsch) | `videos/zukunftsforschung.de.vtt` | kommt ins Repo |
| Kapitel mit Zeitmarken | 0:00 Was ist Zukunftsforschung? · 0:37 Woher das Fach kommt · … | wie in der YouTube-Beschreibung |
| Transkript, nach Kapiteln gegliedert | Text je Kapitel | Kapitelnamen = Überschriften |
| uploadDate | 2026-11-14 | Tag der Veröffentlichung auf YouTube |
| Dauer | 5:57 | in Sekunden umgerechnet: 357 |
| Kernaussage/Definition | „Zukunftsforschung ist …“ | wird der Antwortabsatz (40–60 Wörter) |
| Passende Leitseite für den Aufruf | `/#angebote` oder `/szenariofilme.html` | vorhandene Seite, kein mailto |
| Artikel, die auf den Film zeigen sollen | z. B. `blog/szenarioentwicklung-ki.html` | nur wo es inhaltlich passt |

## 2. Wo die Angaben landen

```
pflege/videos/
  reihe.json                       Reihenfolge der Reihe (Titel/Slug ggf. anpassen)
  filme/<slug>/film.json           Metadaten, Kapitel, Antwort, „Worum es geht“, Aufruf
  filme/<slug>/transkript.md       „## Kapitelname“ + Absätze
  build.py                         erzeugt alles Weitere
  pruefen.py                       prüft alles
```

Vorlage für `film.json`: `pflege/videos/filme/was-ist-zukunftsforschung/film.json`.
So sieht die fertige Seite mit Platzhaltern aus: `videos/_vorlage/index.html`
(noindex, nicht verlinkt, nicht in der Sitemap; wird bei jedem Lauf neu erzeugt).

## 3. Was der Lauf ändert

`python3 pflege/videos/build.py` erzeugt bzw. aktualisiert:

- `videos/<slug>/index.html`: neue Videoseite
- `videos/index.html`: neue Karte, „In Vorbereitung“ wird kürzer
- „Weiter in der Reihe“ auf **allen** Videoseiten (neuer Film verlinkt, „Als Nächstes“ rückt weiter)
- `index.html`: Startseitenabschnitt „Foresight erklärt“ zeigt den neuesten Film
- `sitemap.xml` (Block „Videos“) und `video-sitemap.xml`
- `llms.txt` (Abschnitt „Videos“)

Von Hand bzw. durch den Skill:

- je ein Satz mit Link in passenden Artikeln/Leitseiten. Bei Blogartikeln aus
  `pflege/blog/artikel.py` den Satz **dort** eintragen und `python3 pflege/blog/build.py .`
  sowie `python3 pflege/seo.py` laufen lassen, sonst überschreibt der nächste Blog-Lauf ihn.
- `CHANGELOG.md`-Eintrag beim Deploy

## 4. Prüfen und veröffentlichen

1. `python3 pflege/videos/pruefen.py` → „Alles in Ordnung.“
2. Lokale Vorschau (`python3 -m http.server 8000`), Player und Kapitelsprünge testen,
   bei 1440 und 390 px muss der Player ohne Scrollen sichtbar sein.
3. Commit, Push (GitHub Pages deployt), Live-Prüfung mit curl.
4. Search Console: URL-Prüfung der neuen Videoseite, Indexierung beantragen.
   Die video-sitemap.xml ist bereits eingereicht und wird neu gelesen.
