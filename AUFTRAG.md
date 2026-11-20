# AUFTRAG – operation-zukunft.de: Mediathek „Foresight erklärt“ (Stand 20.11.2026)

So startest du: Claude-App → Claude Code → Repo von operation-zukunft.de öffnen → Nachricht: „Lies AUFTRAG.md und arbeite ihn ab.“

## Ziel

operation-zukunft.de bekommt eine Mediathek unter `/videos/` mit der Reihe „Foresight erklärt“. Jeder Film hat eine eigene Videoseite, auf der der Film die Hauptsache ist. Google zeigt Videos nur noch für solche Seiten in den Video-Ergebnissen; ein Video, das in einem Blogartikel einen Text ergänzt, zählt nicht.

Reihe (Arbeitstitel):

1. Was ist Zukunftsforschung? (fertig, YouTube-ID `lWqYWYmL73A`, heute im Blogartikel `/blog/was-ist-zukunftsforschung.html`)
2. Foresight mit Szenarien (in Produktion)
3. Foresight mit Trends (geplant)
4. Wie KI Foresight verändert (geplant)

In diesem Lauf wird nur Film 1 veröffentlicht. Für die Filme 2–4 entsteht eine Vorlage, damit jeder neue Film später ein kurzer Lauf ist. Keine leeren Seiten oder Platzhalterseiten für Filme, die es noch nicht gibt.

## Bestand (gemessen 20.11.2026)

* `/blog/was-ist-zukunftsforschung.html`: H1 „Was ist Zukunftsforschung? Methoden, Grenzen und die Rolle von KI“, eigener `<video>`-Player mit `contentUrl` https://pillkahn.de/media/zukunftsforschung-1080p.mp4, Poster `/videos/zukunftsforschung-poster.jpg`, Untertitel `/videos/zukunftsforschung.de.vtt`, Kapitel (0:00, 0:37, 1:15, 2:46, 3:50, 4:32, 4:56, 5:41), Transkript in H3-Abschnitten, VideoObject mit `hasPart`/`Clip` und `embedUrl` YouTube. Problem: Der Player steht weit unten im Dokument (nach dem Text), die Seite ist ein Artikel mit Video, keine Videoseite.
* Hauptmenü: Angebote · Beratung · Buch & Workbooks · Über mich · Das Cluster · Kontakt. Kein Menüpunkt „Videos“.
* `/videos/` liefert 404. Im Ordner `/videos/` liegen heute schon Dateien (hero-loop.mp4, cluster-loop.mp4, szenariofilme/…, Poster, VTT). Diese Dateien bleiben unverändert an ihrem Ort, die neuen Seiten kommen als Unterordner daneben.
* Hosting GitHub Pages: keine .htaccess, keine Server-Weiterleitung, Dateien über 100 MB werden abgelehnt. Die Filmdateien bleiben deshalb auf pillkahn.de (All-Inkl).
* `/szenariofilme.html` ist eine Angebotsseite (Szenariofilm als Leistung) und bleibt, wie sie ist.

## Arbeitsregeln

1. Keine erfundenen Fakten, Zahlen oder Zitate. Texte nur aus dem Bestand (Transkript, Artikel, Leitseiten). Neue Fließtexte kurz halten und im Bericht markieren.
2. Neuer Branch `mediathek`. Kein Push, kein Deploy ohne mein ausdrückliches OK.
3. Kein YouTube-Player einbetten (setzt Cookies; die Seite kommt ohne Einwilligungsbanner aus). Player = eigenes `<video>` mit Poster, Untertiteln und `preload="none"`, darunter ein normaler Link „Auf YouTube ansehen“.
4. JSON-LD: Person-@id https://pillkahn.de/#person, Organisation-@id https://operation-zukunft.de/#organization (wie im Bestand).
5. Haltepunkte nach Schritt 1 und nach Schritt 5.

## Schritte

### 1. Bestandsaufnahme (Haltepunkt)

Repo-Struktur, Build (statisch?), wie Navigation und Footer eingebunden sind (je Seite kopiert oder Include), alle Stellen, die auf `/blog/was-ist-zukunftsforschung.html` verlinken (Startseite, Blogübersicht, andere Artikel, llms.txt, sitemap.xml). Vorschlag für das Layout der Videoseite (Skizze in Worten). STOPP.

### 2. Videoseite Film 1: `/videos/was-ist-zukunftsforschung/`

* Reihenfolge auf der Seite: Brotkrumen (Videos › Was ist Zukunftsforschung?) · H1 · Player sofort darunter, im ersten Bildschirm, volle Inhaltsbreite · ein Antwortabsatz von 40–60 Wörtern (zitierfähige Definition, aus dem Bestand) · „Auf YouTube ansehen“ · Kapitel als klickbare Liste (springen per JavaScript im Player an die Stelle) · „Worum es geht“ (3–5 Sätze) · vollständiges Transkript (aus dem Blogartikel übernehmen, H3-Gliederung behalten) · „Weiter in der Reihe“ (nur veröffentlichte Filme verlinken; für 2–4 eine Zeile „Als Nächstes: Foresight mit Szenarien“ ohne Link) · Aufruf zum passenden Angebot auf operation-zukunft.de (vorhandene Seite, kein mailto).
* Title ≤ 60 Zeichen: „Was ist Zukunftsforschung? – Video | Operation Zukunft“ (prüfen, ggf. kürzen). Eigene Meta-Description ≤ 155 Zeichen.
* JSON-LD als @graph: WebPage (mainEntity → VideoObject) · VideoObject (alle Felder aus dem Bestand übernehmen: name, description, thumbnailUrl, uploadDate, duration, contentUrl, embedUrl, hasPart/Clip mit allen Kapiteln; dazu `inLanguage: "de"`, `transcript` mit dem Transkripttext oder Verweis, `creator`/`author` → Person-@id, `publisher` → Organisation-@id, `isPartOf` → CreativeWorkSeries „Foresight erklärt“) · BreadcrumbList.
* Canonical auf sich selbst, Open Graph mit `og:type` video.other und `og:video` (contentUrl), Twitter Card.

### 3. Mediathek-Übersicht `/videos/`

* H1 „Foresight erklärt – Videos“, Einleitung 2–3 Sätze (wer erklärt was, für wen).
* Eine Karte je veröffentlichtem Film: Vorschaubild, Titel, Dauer, ein Satz, Link auf die Videoseite. Darunter Zeile „In Vorbereitung: Foresight mit Szenarien · Foresight mit Trends · Wie KI Foresight verändert“ (ohne Links, ohne Termine).
* Link zum YouTube-Kanal https://www.youtube.com/@profandprompt.
* JSON-LD: CollectionPage + CreativeWorkSeries „Foresight erklärt“ (`@id` https://operation-zukunft.de/videos/#reihe) mit `hasPart` auf die VideoObject-@ids, ItemList, BreadcrumbList.

### 4. Umzug, Verlinkung, Dateien

* Alter Blogartikel: Server-Weiterleitung ist auf GitHub Pages nicht möglich. Deshalb wird `/blog/was-ist-zukunftsforschung.html` eine schlanke Weiterleitungsseite: `<meta http-equiv="refresh" content="0; url=https://operation-zukunft.de/videos/was-ist-zukunftsforschung/">`, Canonical auf die neue URL, `noindex` nicht setzen, ein sichtbarer Link als Rückfall. Google wertet eine sofortige Meta-Weiterleitung wie eine dauerhafte. Transkript und VideoObject dort entfernen (kein doppelter Inhalt).
* Alle internen Links aus Schritt 1 auf die neue URL umstellen. Blogübersicht: Eintrag bleibt, zeigt aber auf die Videoseite.
* Hauptmenü auf allen Seiten: Punkt „Videos“ → `/videos/` (vor „Das Cluster“). Footer: Link „Videos“.
* Startseite: kleiner Abschnitt „Foresight erklärt“ mit Vorschaubild des neuesten Films und Link auf `/videos/` (Platz nach Bestand vorschlagen).
* Leitseiten und Artikel, in denen Zukunftsforschung, Szenarien, Trends oder KI und Foresight Thema sind: je ein Satz mit Link auf die passende Videoseite, nur wo es inhaltlich passt (Liste im Bericht).
* `sitemap.xml`: neue URLs mit lastmod, alte Blog-URL entfernen. Neue Datei `video-sitemap.xml` nach Google-Schema (`video:thumbnail_loc`, `video:title`, `video:description`, `video:content_loc` = pillkahn.de-mp4, `video:player_loc` = YouTube-Embed, `video:duration` in Sekunden, `video:publication_date`), in robots.txt als zweite `Sitemap:`-Zeile.
* `llms.txt`: Abschnitt „Videos“ mit Übersicht und Film 1 (je eine Zeile Beschreibung).

### 5. Vorlage für die nächsten Filme (Haltepunkt danach)

* `videos/_vorlage/index.html` (nicht in Sitemap, `noindex`, vom Build ausgeschlossen bzw. nicht verlinkt) mit allen Platzhaltern.
* `videos/NEUER-FILM.md`: Checkliste, was ich für einen neuen Film liefern muss (Titel, YouTube-ID, Dateiname der mp4 auf pillkahn.de/media/, Poster, VTT, Kapitel mit Zeitmarken, Transkript, uploadDate, Dauer, passende Leitseite) und welche Dateien der Lauf ändert (Videoseite, Übersicht, Startseitenabschnitt, sitemap.xml, video-sitemap.xml, llms.txt, „Weiter in der Reihe“ auf allen Videoseiten).
* Prüfen: JSON-LD aller geänderten Seiten mit einem Skript parsen (gültig, @id-Verweise konsistent, VideoObject vollständig), video-sitemap.xml gegen das Schema prüfen, alle Links prüfen, Player und Kapitelsprünge in der lokalen Vorschau testen, Screenshots bei 1440 und 390 px (Player muss auf beiden ohne Scrollen sichtbar sein).
* Bericht: Änderungen je Datei, alle neuen Texte zum Gegenlesen, Offene Punkte. STOPP.

### 6. Nach meinem OK: Commit, Push, Deploy

Live-Prüfung mit curl: `/videos/` und `/videos/was-ist-zukunftsforschung/` 200, alte Blog-URL liefert die Weiterleitungsseite, sitemap.xml und video-sitemap.xml 200 mit XML-Content-Type, robots.txt enthält beide Sitemap-Zeilen, `https://pillkahn.de/media/zukunftsforschung-1080p.mp4` antwortet 200 bzw. 206 auf Range-Anfrage. Eintrag in `CHANGELOG.md`. Zum Schluss Schritt für Schritt mit Klickpfad: video-sitemap.xml in der Google Search Console und in den Bing Webmaster Tools einreichen, URL-Prüfung für die neue Videoseite, und wo ich im Bericht „Videoseiten“ der Search Console später sehe, ob das Video indexiert ist.

## Folgeaufträge (nicht in diesem Lauf)

* pillkahn.de: Abschnitt „Videos“ mit Hinweis (Vorschaubild, zwei Sätze, Link auf die Videoseite), kein zweites VideoObject, kein Transkript. Kommt in den Lauf „Kleinigkeiten pillkahn.de“.
* Satelliten, sobald die Filme da sind: Szenarien → vice-versa.de, picturesoftomorrow.com · Trends → squawk.de · KI und Foresight → agentic-foresight.com, questionsoftomorrow.com.
* YouTube (Prof in YouTube Studio): Playlist „Foresight erklärt“, erste Zeile jeder Beschreibung = Link auf die Videoseite, Abspann auf den nächsten Film.
