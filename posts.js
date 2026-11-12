/* ============================================================
   OPERATION::ZUKUNFT — posts.js
   Datenquelle der Blog-Leiste (rechte Seitenleiste)
   ============================================================

   BETRIEBSANLEITUNG (für George bzw. den manuellen Betrieb)
   ---------------------------------------------------------
   Neuen Beitrag veröffentlichen — in drei Schritten:

     1. Neuen Eintrag GANZ OBEN in das Array `posts` einfügen
        (Reihenfolge ist aber nicht kritisch: die Seite sortiert
        selbst nach `datum` absteigend und zeigt die neuesten 5).

     2. Nur diese Datei (posts.js) hochladen — per FTP auf den
        Webspace oder per Commit/Push ins GitHub-Repo
        (ulfpillkahn-alt/operation-zukunft.de) — und die
        vorhandene Datei überschreiben.

     3. Fertig. Kein Eingriff in index.html, style.css oder
        main.js nötig — die Seite rendert die Leiste beim
        nächsten Aufruf automatisch neu.

   Format eines Eintrags:
     {
         titel:  "Überschrift des Beitrags",
         datum:  "2026-07-01",              // ISO-Format JJJJ-MM-TT
         teaser: "Ein bis zwei Sätze Anriss.",
         url:    "blog/mein-beitrag.html"   // relativ oder absolut
     }

   Hinweise:
   - Der zugehörige Artikel selbst liegt als HTML-Datei im
     Ordner /blog/ — auch er wird einfach mit hochgeladen.
   - Anführungszeichen im Titel/Teaser als \" maskieren oder
     typografische Zeichen („…") verwenden.
   - Nach dem letzten Eintrag darf ein Komma stehen, muss aber nicht.
   - Fällt die Datei aus oder ist das Array leer, zeigt die Seite
     einen dezenten Platzhalter — sie bricht nicht.
   ============================================================ */

const posts = [
    {
        titel: "Szenarien als Film",
        datum: "2026-11-12",
        teaser: "Warum bewegte Bilder Zukunftsszenarien greifbar machen – und wie KI die Produktion verändert.",
        url: "blog/szenarien-als-film.html"
    },
    {
        titel: "Technologiereife richtig einschätzen",
        datum: "2026-10-01",
        teaser: "Wie Unternehmen die Reife neuer Technologien realistisch bewerten und Fehlinvestitionen vermeiden.",
        url: "blog/technologiereife-einschaetzen.html"
    },
    {
        titel: "Abbruchkriterien für Innovationsprojekte",
        datum: "2026-09-01",
        teaser: "Warum Unternehmen an gescheiterten Projekten festhalten – und wie Abbruchkriterien helfen.",
        url: "blog/abbruchkriterien-innovationsprojekte.html"
    },
    {
        titel: "Flipped Foresight erklärt",
        datum: "2026-08-01",
        teaser: "Warum sich die Arbeitsteilung zwischen Mensch und Maschine in der Szenarioarbeit umkehrt.",
        url: "blog/flipped-foresight-methode.html"
    },
    {
        titel: "KI-Agenten einführen: fünf Fehler",
        datum: "2026-07-01",
        teaser: "Fünf Fehler, die Agenten-Pilotprojekte scheitern lassen – und wie Sie sie vermeiden.",
        url: "blog/ki-agenten-einfuehren-fehler.html"
    },
    {
        titel: "Schwache Signale mit KI-Agenten",
        datum: "2026-06-01",
        teaser: "Wie KI-Agenten Trend- und Technologiemonitoring rund um die Uhr übernehmen.",
        url: "blog/schwache-signale-ki-agenten.html"
    },
    {
        titel: "Szenarioentwicklung mit KI",
        datum: "2026-05-01",
        teaser: "Wie Maschinen Rohszenarien und Konsistenzprüfung übernehmen – und warum der Workshop trotzdem bleibt.",
        url: "blog/szenarioentwicklung-ki.html"
    },
    {
        titel: "Corporate Foresight mit KI",
        datum: "2026-04-01",
        teaser: "Welche Foresight-Aufgaben Maschinen übernehmen – und wo der Mensch unersetzlich bleibt.",
        url: "blog/corporate-foresight-ki.html"
    },
    {
        titel: "Einstein würde OpenClaw nutzen",
        datum: "2026-03-01",
        teaser: "Ein augenzwinkernder Gedankenversuch: Warum Albert Einstein der ultimative OpenClaw-Nutzer gewesen wäre.",
        url: "blog/einstein-openclaw.html"
    },
    {
        titel: "Der Hype um OpenClaw – gerechtfertigt?",
        datum: "2026-02-01",
        teaser: "OpenClaw ist ein autonomer KI-Agent, der echte Aufgaben auf dem Rechner ausführt. Was steckt hinter dem Hype?",
        url: "blog/hype-openclaw.html"
    },
    {
        titel: "Strategieplanung mit KI",
        datum: "2025-09-01",
        teaser: "Warum große Strategieabteilungen ein Auslaufmodell sind und wie KI-Agenten die Unternehmensführung verändern.",
        url: "blog/strategieplanung-ki.html"
    },
    {
        titel: "Das Dilemma von Organisationen",
        datum: "2025-06-01",
        teaser: "Organisationen stellen die smartesten Leute ein, um ihnen dann zu erklären, was zu tun ist. Warum das Innovation verhindert.",
        url: "blog/dilemma-organisationen.html"
    },
    {
        titel: "Der Lebenszyklus von Innovationen",
        datum: "2025-02-01",
        teaser: "Vom Durchbruch zum Marketing-Versprechen: Wie Innovationen ihren Biss verlieren.",
        url: "blog/lebenszyklus-innovationen.html"
    },
    {
        titel: "Der Red-Queen-Effekt",
        datum: "2019-05-10",
        teaser: "Warum Unternehmen immer schneller laufen müssen, um stehenzubleiben.",
        url: "blog/red-queen-effekt.html"
    },
    {
        titel: "Pictures of the Future",
        datum: "2017-11-20",
        teaser: "Wie systematisch entwickelte Zukunftsbilder Strategien schärfen. Erfahrungen aus der Praxis.",
        url: "blog/pictures-of-the-future.html"
    },
    {
        titel: "Warum Prognosen scheitern",
        datum: "2016-03-15",
        teaser: "Das Grundproblem der Zukunftsforschung: Keine Theorie, keine Grundlage.",
        url: "blog/warum-prognosen-scheitern.html"
    }
];
