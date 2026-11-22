# AUFTRAG – operation-zukunft.de: fünf Leitseiten (Stand 22.11.2026)

So startest du: Claude-App → Claude Code → Repo von operation-zukunft.de öffnen → diese Datei als `AUFTRAG.md` ins Repo legen → Nachricht: „Lies AUFTRAG.md und arbeite ihn ab.“

Dieser Auftrag ersetzt `oz-leitseite-ki-agenten.md` vom 16.11.2026.

---

## Ziel

operation-zukunft.de bekommt fünf Leitseiten. Jede besitzt genau einen Suchbegriff, beantwortet ihn besser als die heutigen Treffer und führt zu einem konkreten Angebot. Gemessen wird an Google-Position und an Nennungen in KI-Antworten (ChatGPT, Google AI Overview).

Warum so (Messung 20.–22.11.2026):
- Kein Reichweitenbegriff steht in den Top 40. Nur der Blogartikel `/blog/corporate-foresight-ki.html` rankt (Platz 11 „foresight mit ki-agenten“, Platz 23 „foresight mit ki“).
- KI-Antworten auf Anbieterfragen zitieren Leistungsseiten, die das Angebot im Titel tragen, keine Blogartikel. Tool-Fragen werden aus Übersichten beantwortet.
- Die Treffer für „szenarioentwicklung mit ki“ und „foresight mit ki-agenten“ sind schwach und teils themenfremd. Dort ist Platz 1–3 realistisch.

## Die fünf Seiten (verbindliche Begriffszuteilung)

| # | URL | Hauptbegriff | Nebenbegriffe | Angebot auf der Seite |
|---|---|---|---|---|
| A | `/foresight-mit-ki-agenten/` | Foresight mit KI-Agenten | Foresight mit Agenten, KI-Agenten für Corporate Foresight, Trendmonitoring mit KI-Agenten | KI-Agenten für Innovation und Foresight (Preis auf Anfrage), Orientierungsworkshop |
| B | `/szenariotechnik/` | Szenariotechnik | Szenarioanalyse, Szenarioplanung, Szenario-Methode, Szenariotrichter | Strategie-Pakete (Szenarioset), Szenariofilme |
| C | `/corporate-foresight/` | Corporate Foresight | Corporate Foresight mit KI, Strategic Foresight, strategische Frühaufklärung, Foresight-Methoden, Foresight-Beratung | Strategie-Pakete 2027 (Light, Safari, Navigator), Orientierungsworkshop |
| D | `/szenarioentwicklung-mit-ki/` | Szenarioentwicklung mit KI | Szenarien mit KI entwickeln, Szenarioplanung mit KI, Tools für Szenarioentwicklung mit KI | Strategie-Pakete, Szenariofilme, Verweis picturesoftomorrow.com |
| E | `/zukunftsforschung/` | Zukunftsforschung | Zukunftsforschung für Unternehmen, strategische Vorausschau, Methoden der Zukunftsforschung | Vorträge, Orientierungsworkshop |

Die Startseite besitzt „Foresight mit KI“ (siehe Schritt 4).

Begriffe, die anderen Domains gehören, werden höchstens einmal genannt und dorthin verlinkt: „Agentic Foresight“ → agentic-foresight.com · „Szenariogenerierung mit KI“ → picturesoftomorrow.com · „Zukunftsforscher“ → pillkahn.de · „Trendradar“ → squawk.de · „Flipped Foresight“ → flipped-foresight.com.

Abgrenzung untereinander: B erklärt die klassische Methode. D erklärt nur, was KI daran ändert, und verweist für die Methode auf B. C erklärt die Verankerung im Unternehmen und verweist für Methoden auf B und D. A erklärt Agenten als Betriebsform und verweist für den Bauplan auf agentic-foresight.com. E ist das Dach und verlinkt A–D als Methodenlandkarte. Kein Absatz steht auf zwei Seiten.

## Arbeitsregeln

1. Keine erfundenen Fakten, Kunden, Zahlen, Zitate oder Leistungen. Preise und Leistungsumfang nur wörtlich aus `index.html` und `strategie-pakete.html`. Die Black-Week-Konditionen kommen nicht auf die Leitseiten.
2. Fachinhalt: allgemein anerkanntes Lehrbuchwissen ist erlaubt. Positionen von Prof. Dr. Ulf Pillkahn nur aus vorhandenen Texten (dieses Repo, pillkahn.de, flipped-foresight.com, picturesofthefuture.de, SSRN-Paper). Fehlt etwas, kommt es in die Liste „Fragen an Prof“ – nicht raten.
3. Jeder neue Fließtext wird im Bericht vollständig zum Gegenlesen ausgegeben.
4. Ton der bestehenden Seite: Deutsch, Sie-Anrede, sachlich, keine Floskeln, keine Superlative.
5. Branch `leitseiten`. Kein Push, kein Deploy ohne mein ausdrückliches OK.
6. Kein Eingriff in DNS, Impressum, Datenschutz. Kein Formular, kein Tracking, kein YouTube-Player (cookiefreie Linie). Kontakt wie im Bestand: mailto mit vorbelegtem Betreff, Telefon, „Adresse kopieren“.
7. JSON-LD: Person-@id `https://pillkahn.de/#person`, Organisation-@id `https://operation-zukunft.de/#organization`. Bücher nur als Verweis auf die Book-@id auf pillkahn.de, und nur, wenn die Buchseite mit 200 antwortet.
8. Keine Platzhalterseiten. Verlinkt wird nur, was live ist.
9. An jedem STOPP anhalten und berichten.

## Aufbau jeder Leitseite (Vorlage)

Reihenfolge im Dokument:
1. Brotkrumen (Start › Seitentitel).
2. H1 mit dem Hauptbegriff am Anfang. Genau eine H1.
3. Antwortabsatz, 40–60 Wörter: Definition, für sich allein verständlich und zitierfähig.
4. Autorenzeile: „Prof. Dr. Ulf Pillkahn“ (Link pillkahn.de) und sichtbares „Zuletzt aktualisiert: TT.MM.JJJJ“.
5. Inhaltsverzeichnis mit Sprungmarken.
6. Hauptteil mit H2/H3, 1.500–2.200 Wörter (B bis 2.500). Jede H2 beginnt mit einem Satz, der die Überschrift direkt beantwortet. Wo es passt: nummerierte Schritte, eine Vergleichstabelle.
7. Belegblock: Werkzeug aus dem Cluster, Buch, Paper oder Musterfall – je mit sprechendem Ankertext.
8. Videohinweis, falls eine Videoseite existiert: Vorschaubild, zwei Sätze, Link auf die Videoseite. Kein zweites VideoObject, kein Transkript.
9. Angebotsblock „So arbeiten wir damit“: die Leistung aus der Tabelle oben mit Preis, falls einer auf der Website steht, und Kontaktaufruf.
10. Häufige Fragen: 5–6 echte Suchfragen, Antworten je 2–4 Sätze.
11. Block „Weiter im Thema“: Links auf die anderen live geschalteten Leitseiten.
12. Quellen: nur tatsächlich verwendete.

Kopf: Title ≤ 60 Zeichen (nachzählen), Meta-Description ≤ 155 Zeichen, Canonical auf sich selbst, Open Graph, Twitter Card, alt-Texte.

JSON-LD als ein `@graph`: WebPage (`about`, `author` → Person-@id, `publisher` → Organisation-@id, `dateModified`), BreadcrumbList, FAQPage, Service (`provider` → Organisation-@id; `offers` nur bei Preis auf der Website). Buchbezug über `citation`.

## Vorgaben je Seite

**A – Foresight mit KI-Agenten**
- Title: „Foresight mit KI-Agenten – Operation Zukunft“. H1: „Foresight mit KI-Agenten“.
- H2: Was ein Foresight-Agent ist (Abgrenzung Chatbot, Agent, Multi-Agenten-System) · Wo Agenten im Foresight-Prozess arbeiten (Scanning, Verdichtung, Szenarien, Bildebene, Monitoring; je ein Link auf squawk.de, questionsoftomorrow.com, picturesoftomorrow.com) · Arbeitsteilung Mensch und Maschine (Flipped Foresight) · Grenzen und Risiken · Wie Operation Zukunft damit arbeitet · Den Bauplan ansehen (agentic-foresight.com) · Häufige Fragen.
- Quellen: Fröhling, Giaconia, Bogucka, Quercia (2026), https://arxiv.org/abs/2602.08565 (vor Verwendung abrufen und Aussage am Abstract prüfen) · Flipped-Foresight-Paper, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7322758.
- Zubringer: `/blog/schwache-signale-ki-agenten.html`, `/blog/ki-agenten-einfuehren-fehler.html`, `cluster.html`.

**B – Szenariotechnik**
- Title: „Szenariotechnik: Schritte und Beispiel | Operation Zukunft“. H1: „Szenariotechnik: Methode, Schritte und Beispiel“.
- H2: Was Szenariotechnik ist · Wann sie sinnvoll ist (Abgrenzung zur Prognose) · Der Szenariotrichter · Die Schritte (nummeriert) · Beispiel VISEON AG (Musterfall von picturesofthefuture.de, nur dortige Angaben, Link) · Typische Fehler · Was KI an der Methode ändert (kurz, Link auf D) · Das Buch zur Methode („Trends und Szenarien als Werkzeuge zur Strategieentwicklung“, Link Buchseite pillkahn.de) · Häufige Fragen.
- Videohinweis: `/videos/foresight-mit-szenarien/`.
- Zubringer: `/blog/warum-prognosen-scheitern.html`, `/blog/pictures-of-the-future.html`, `/blog/szenarien-als-film.html`.

**C – Corporate Foresight**
- Title: „Corporate Foresight mit KI – Beratung | Operation Zukunft“. H1: „Corporate Foresight: Definition, Prozess und Einführung mit KI“.
- H2: Was Corporate Foresight ist · Was es leisten soll · Der Prozess (Beobachten, Deuten, Szenarien, Strategie) · Methoden im Überblick (Links auf B, D, squawk.de) · Einführung im Unternehmen in Schritten · Was KI übernimmt und was beim Menschen bleibt · Typische Missverständnisse · Beratung und Pakete · Häufige Fragen.
- Der Inhalt von `/blog/corporate-foresight-ki.html` geht in diese Seite ein (siehe Schritt 4).
- Zubringer: `/blog/strategieplanung-ki.html`, `/blog/flipped-foresight-methode.html`.

**D – Szenarioentwicklung mit KI**
- Title: „Szenarioentwicklung mit KI: Ablauf, Tools, Grenzen“. H1: „Szenarioentwicklung mit KI: Ablauf, Werkzeuge und Grenzen“.
- H2: Was sich durch KI ändert · Der Ablauf Schritt für Schritt (wo KI arbeitet, wo der Mensch entscheidet) · Grenzen (Neigung zum Mittelweg, Quellenlage, Scheinpräzision) · Warum der Workshop bleibt · Tools für Szenarioentwicklung mit KI – ein Überblick · So arbeitet Operation Zukunft · Häufige Fragen.
- Tool-Überblick: Tabelle nach Kategorien (Foresight-Plattformen, Sprachmodelle, Szenario-Software, eigene Werkzeuge im Cluster). Fremde Tools nur mit einem Satz, der auf der Herstellerseite am Tag des Schreibens nachprüfbar ist, mit Link und „Stand: Monat Jahr“. Keine Wertung, keine Preise. Kandidaten zum Prüfen: Futures Platform, ITONICS, FIBRES, Shaping Tomorrow, ScMI, 4strat. Eigene: picturesoftomorrow.com, vice-versa.de, questionsoftomorrow.com.
- Der Inhalt von `/blog/szenarioentwicklung-ki.html` geht in diese Seite ein (siehe Schritt 4).

**E – Zukunftsforschung**
- Title: „Zukunftsforschung für Unternehmen | Operation Zukunft“. H1: „Zukunftsforschung für Unternehmen: Methoden, Nutzen, Grenzen“.
- H2: Was Zukunftsforschung ist · Was sie kann und was nicht · Zukunftsforschung, Trendforschung, Corporate Foresight – die Unterschiede (Tabelle) · Methodenlandkarte (Karten auf A–D und squawk.de) · Woran man seriöse Zukunftsforschung erkennt · Welche Rolle KI spielt · Wer dahinter steht (Prof. Dr. Ulf Pillkahn, Link pillkahn.de mit Ankertext „Zukunftsforscher Prof. Dr. Ulf Pillkahn“, Bücher) · Häufige Fragen.
- Videohinweis: `/videos/was-ist-zukunftsforschung/`. Die Videoseite bleibt unverändert und behält die Frage „Was ist Zukunftsforschung?“; die Leitseite übernimmt nichts aus dem Transkript.

## Schritte

**1. Bestandsaufnahme und Gliederungen.** Repo-Struktur, wie Navigation und Footer eingebunden sind, vorhandenes JSON-LD, Stand der Buchverweise (ist Auftrag 13 schon umgesetzt?), alle Stellen, die auf die beiden Blogartikel aus C und D verlinken. Prüfe per Abruf: die drei Buchseiten auf pillkahn.de, agentic-foresight.com, picturesofthefuture.de, die Videoseiten. Liefere für alle fünf Seiten: Gliederung bis H3, Antwortabsatz im Entwurf, FAQ-Fragen, Title und Description mit Zeichenzahl, und die Liste „Fragen an Prof“. STOPP.

**2. Vorlage und Seite A.** Vorlage nach dem Abschnitt „Aufbau“ bauen, Seite A vollständig schreiben. Lokale Vorschau, Screenshots bei 1440 und 390 px. Bericht mit dem gesamten Text. STOPP.

**3. Einbindung, Teil 1 – danach Veröffentlichung A.**
- Startseite: neuer Abschnitt `#themen` („Themen“) mit einer Karte je live geschalteter Leitseite; Menüpunkt „Themen“ → `index.html#themen` auf allen Seiten; Footer-Links auf die live geschalteten Leitseiten.
- Zubringer-Artikel von A: je ein Satz im Text mit Ankertext „Foresight mit KI-Agenten“.
- `sitemap.xml` (lastmod), `llms.txt` (Abschnitt „Leitseiten“, je eine Zeile).
- Prüfen wie in Schritt 6. Nach meinem OK: Commit, Push, Live-Check. STOPP.

**4. Seiten B, C, D, E und Einbindung, Teil 2.**
- Seiten in dieser Reihenfolge schreiben.
- Blogartikel `/blog/corporate-foresight-ki.html` und `/blog/szenarioentwicklung-ki.html`: brauchbare Passagen in C bzw. D einarbeiten. Danach wird jede der beiden Dateien eine schlanke Weiterleitungsseite nach dem Muster von `/blog/was-ist-zukunftsforschung.html` (Meta-Refresh 0 Sekunden, Canonical auf die Leitseite, sichtbarer Link, kein `noindex`). Blogübersicht: Einträge bleiben, zeigen auf die Leitseiten. Alle internen Links und die Sitemap umstellen. Buchverweise aus Auftrag 13, die auf diesen Artikeln lagen, wandern auf die Leitseiten.
- Startseite: Title „Foresight mit KI für Unternehmen | Operation Zukunft“; im ersten Absatz unter der H1 kommt „Foresight mit KI“ wörtlich vor. H1 und Aufbau bleiben. `#themen`, Footer und „Weiter im Thema“ auf allen Leitseiten vervollständigen.
- Zubringer-Artikel je Seite verlinken (ein Satz, Ankertext = Hauptbegriff). `strategie-pakete.html` verlinkt B und C.
- `sitemap.xml`, `llms.txt` ergänzen.

**5. Bericht.** Änderungen je Datei, alle neuen Texte, offene Punkte, Folgeaufgaben für andere Repos (pillkahn.de: llms.txt und Verweise auf die Leitseiten; flipped-foresight.com, squawk.de, picturesoftomorrow.com, agentic-foresight.com: je ein Link mit dem Hauptbegriff als Ankertext auf die passende Leitseite). STOPP.

**6. Prüfen (vor jedem Push).** Per Skript: JSON-LD jeder geänderten Seite gültig und @id-Verweise konsistent · genau eine H1 · Title- und Description-Längen · Wortzahl je Seite · kein Absatz über 40 Wörter doppelt auf zwei Seiten · alle internen und externen Links antworten mit 200 · jeder Hauptbegriff steht in Title, H1, Antwortabsatz und URL genau der Seite, der er gehört.

**7. Nach meinem OK: Veröffentlichung B–E.** Commit, Push, Live-Check mit curl (200, JSON-LD live, Weiterleitungsseiten, sitemap.xml, llms.txt). Neue und geänderte URLs per IndexNow melden, falls der Schlüssel aus Auftrag 11 im Repo liegt. Eintrag in `CHANGELOG.md`. Zum Schluss: Liste aller neuen URLs und Schritt für Schritt mit Klickpfad, wie ich jede in der Google Search Console per URL-Prüfung zur Indexierung einreiche.
