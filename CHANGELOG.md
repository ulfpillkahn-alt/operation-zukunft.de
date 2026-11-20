# Changelog operation-zukunft.de

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
