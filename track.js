/* ============================================================
   OPERATION::ZUKUNFT — track.js
   Herkunft und Klicks als reine Summenzähler (Abacus).

   Warum so und nicht wie auf pillka.hn:
   Dort läuft ein eigenes Server-Skript bei all-inkl. GitHub Pages
   führt keinen Server-Code aus, gezählt wird über abacus.jasoncameron.dev.
   Abacus kann Schlüssel nicht auflisten — die Statistikseite kann nur
   lesen, was sie namentlich kennt. Deshalb zählen wir ausschließlich
   gegen die festen Listen unten; alles Unbekannte wird zu „andere".

   Datenschutz: keine Cookies, keine Kennungen, keine vollständigen
   URLs. Gespeichert werden ausschließlich monatliche Summen. Aus dem
   Referrer wird nur der Hostname gelesen und sofort auf eine Kategorie
   abgebildet. Der sessionStorage-Merker verhindert Doppelzählung der
   Herkunft und verfällt mit der Browser-Sitzung.

   Schlüsselformat (Monat im Namen, weil Abacus-Zähler kumulativ sind):
     ref-JJJJ-MM-<kategorie>      z. B. ref-2026-11-google
     click-JJJJ-MM-<wert>         z. B. click-2026-11-angebot-workshop
   ============================================================ */
(function () {
    'use strict';

    /* ---------- Listen: einzige Quelle, stats.html liest sie hier ---------- */
    window.OZ_TRACK = {
        refs: ['direkt','google','bing','duckduckgo','ecosia','chatgpt','perplexity','claude','gemini',
               'linkedin','x','meta','xing','youtube',
               'pillka-hn','pillkahn-de','pillkahn-com','picturesoftomorrow','questionsoftomorrow',
               'squawk','beatles-cluster','nowplus10','flipped-foresight','foresight-review',
               'innovation-review','technology-review','andere'],
        clicks: ['angebot-workshop','angebot-agenten','angebot-cluster',
                 'beratung-agenten','beratung-workshop','vortrag','forschung',
                 'kontakt-workshop','kontakt-agenten','kontakt-vortrag','kontakt-forschung',
                 'nav-cluster','cluster-zurueck-angebote','blog-beitrag','logbuch-extern','datenschutz',
                 'band-szenariofilm','szenariofilm-anfrage','szenariofilm-play'],
        /* Sichtkontakt: Seit dem Problemblock (07.11.2026) stehen die
           Angebotskarten unter der Falz. Ohne diesen Zähler liesse sich
           nicht unterscheiden, ob Besucher die Angebote gar nicht sehen
           oder sie sehen und sich dagegen entscheiden. */
        views: ['angebote']
    };

    /* Lokale Tests verfälschen die echten Zahlen nicht */
    var isLocal = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
    window.OZ_TRACK.ns = isLocal ? 'oz-test.local' : 'operation-zukunft.de';

    /* Erfassungsbeginn — die Statistikseite zeigt ihn an */
    window.OZ_TRACK.start = '2026-11';

    /* Tag als JJJJ-MM-TT und Monat als JJJJ-MM — beides in UTC, weil
       main.js die Tagesbalken (visits-JJJJ-MM-TT) ebenso bildet. Nur so
       meinen Balken und Detailzahlen denselben Tag. */
    window.OZ_TRACK.day = function (d) {
        return (d || new Date()).toISOString().slice(0, 10);
    };
    window.OZ_TRACK.month = function (d) {
        return window.OZ_TRACK.day(d).slice(0, 7);
    };

    /* ---------- Herkunft: Hostname → Kategorie ----------
       Reine Funktion, damit sie einzeln prüfbar ist:
         OZ_TRACK.refFrom('https://www.google.de/')  →  'google'
       Rückgabe null heißt: nicht zählen (eigene Domain). */
    window.OZ_TRACK.refFrom = function (referrer) {
        var host;
        if (!referrer) return 'direkt';
        try {
            host = new URL(referrer).hostname.toLowerCase().replace(/^www\./, '');
        } catch (e) {
            return 'andere';
        }
        if (!host) return 'direkt';

        // eigene Domain: interne Navigation, nicht zählen
        if (host === 'operation-zukunft.de') return null;

        // Suchmaschinen und Assistenten — gemini vor google prüfen
        if (host === 'gemini.google.com') return 'gemini';
        if (host === 'google' || host.indexOf('google.') === 0) return 'google';
        if (host === 'bing.com') return 'bing';
        if (host === 'duckduckgo.com') return 'duckduckgo';
        if (host === 'ecosia.org') return 'ecosia';
        if (host === 'chatgpt.com' || host === 'chat.openai.com') return 'chatgpt';
        if (host === 'perplexity.ai') return 'perplexity';
        if (host === 'claude.ai') return 'claude';

        // soziale Netzwerke
        if (host === 'linkedin.com' || host === 'lnkd.in') return 'linkedin';
        if (host === 't.co' || host === 'x.com' || host === 'twitter.com') return 'x';
        if (host === 'facebook.com' || host === 'l.facebook.com' ||
            host === 'instagram.com' || host === 'l.instagram.com') return 'meta';
        if (host === 'xing.com') return 'xing';
        if (host === 'youtube.com') return 'youtube';

        // eigene Domains (Punkt → Bindestrich)
        if (host === 'pillka.hn') return 'pillka-hn';
        if (host === 'pillkahn.de') return 'pillkahn-de';
        if (host === 'pillkahn.com') return 'pillkahn-com';
        if (host === 'picturesoftomorrow.com') return 'picturesoftomorrow';
        if (host === 'questionsoftomorrow.com') return 'questionsoftomorrow';
        if (host === 'squawk.de') return 'squawk';
        if (host === 'beatles-cluster.de') return 'beatles-cluster';
        if (host === 'nowplus10.com') return 'nowplus10';
        if (host === 'flipped-foresight.com') return 'flipped-foresight';
        if (host === 'foresight-review.com') return 'foresight-review';
        if (host === 'innovation-review.com') return 'innovation-review';
        if (host === 'technology-review.com') return 'technology-review';

        return 'andere';
    };

    /* Auf der Statistikseite selbst wird nichts gezählt — sie bindet diese
       Datei nur ein, um die Listen oben zu teilen (keine zweite Kopie). */
    var p = location.pathname;
    if (/\/stats(\.html)?$/.test(p)) return;

    /* ---------- Zählen ----------
       Jedes Ereignis wird zweimal gezählt: einmal auf den Monat, einmal
       auf den Tag. Der Monatszähler dient der Statistikseite als Index
       (welche Kategorien kommen überhaupt vor), der Tageszähler liefert
       die Aufschlüsselung hinter dem jeweiligen Balken. */
    function hitRaw(key) {
        try {
            fetch('https://abacus.jasoncameron.dev/hit/' + window.OZ_TRACK.ns + '/' + key,
                  { keepalive: true, mode: 'cors' })
                .catch(function () { /* still */ });
        } catch (e) { /* still */ }
    }
    function hit(praefix, wert) {
        hitRaw(praefix + window.OZ_TRACK.month() + '-' + wert);
        hitRaw(praefix + window.OZ_TRACK.day() + '-' + wert);
    }

    /* Herkunft: einmal je Browser-Sitzung.
       Lässt sich sessionStorage nicht lesen (privater Modus, blockierte
       Speicher), zählen wir lieber gar nicht als doppelt. */
    function countRef() {
        try {
            if (sessionStorage.getItem('oz-ref')) return;
        } catch (e) {
            return;
        }
        var cat = window.OZ_TRACK.refFrom(document.referrer);
        if (!cat) return;                       // eigene Domain
        try { sessionStorage.setItem('oz-ref', cat); } catch (e) { return; }
        hit('ref-', cat);
    }

    /* Klicks: ein delegierter Listener, kein Eingriff in die Navigation.
       keepalive sorgt dafür, dass die Anfrage auch beim Seitenwechsel
       noch rausgeht. */
    function initClicks() {
        document.addEventListener('click', function (ev) {
            var el = ev.target && ev.target.closest ? ev.target.closest('[data-track]') : null;
            var value = null;

            if (el) {
                var v = el.getAttribute('data-track');
                if (window.OZ_TRACK.clicks.indexOf(v) !== -1) value = v;
            } else if (ev.target && ev.target.closest) {
                // Blog-Leiste: die Links erzeugt main.js, deshalb hier abgefangen
                var post = ev.target.closest('#sidebar-posts a');
                if (post) value = 'blog-beitrag';
            }

            if (value) hit('click-', value);
        }, true);
    }

    /* Sichtkontakt: zählt einmal je Sitzung, sobald die Angebotskarten
       zu einem Drittel im Bild stehen. Kein Scroll-Listener, der
       IntersectionObserver kostet nichts. */
    function initViews() {
        if (!('IntersectionObserver' in window)) return;
        var ziel = document.getElementById('angebote');
        if (!ziel) return;
        try { if (sessionStorage.getItem('oz-view-angebote')) return; } catch (e) { return; }

        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (!e.isIntersecting) return;
                io.disconnect();
                try { sessionStorage.setItem('oz-view-angebote', '1'); } catch (err) { return; }
                hit('view-', 'angebote');
            });
            /* Niedrige Schwelle mit Absicht: einspaltig (Mobil) ist der
               Block höher als der Bildschirm, ein Drittel wäre dort kaum
               erreichbar. 15 % heißt verlässlich „ins Bild gekommen". */
        }, { threshold: 0.15 });
        io.observe(ziel);
    }

    /* Start des Erklärfilms auf szenariofilme.html: einmal je Seitenaufruf.
       Nur dieses eine Video — die vier stummen Kachel-Videos starten von
       selbst und würden den Zähler sonst mit jedem Scrollen hochtreiben. */
    function initFilm() {
        var film = document.getElementById('film-erklaer');
        if (!film) return;
        var gezaehlt = false;
        film.addEventListener('play', function () {
            if (gezaehlt) return;
            gezaehlt = true;
            hit('click-', 'szenariofilm-play');
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { countRef(); initClicks(); initViews(); initFilm(); });
    } else {
        countRef(); initClicks(); initViews(); initFilm();
    }
})();
