/* ============================================================
   OPERATION::ZUKUNFT — track.js
   Besucherzähler: Besuche, Herkunft, Klicks, Sichtkontakt.

   Seit 12.11.2026 meldet die Seite an einen eigenen Zähler auf
   pillkahn.de (api/oz/visits.php, Webspace bei all-inkl) statt an
   den Fremddienst abacus.jasoncameron.dev. GitHub Pages führt kein
   PHP aus, deshalb steht der Zähler dort und nicht hier.

   Übertragen werden nur: der Referrer (der Server behält davon
   ausschließlich den Hostnamen), feste Kennungen geklickter
   Schaltflächen und der Hostname angeklickter externer Links.
   Keine Cookies, keine IP-Speicherung, keine vollständigen URLs.
   Ein sessionStorage-Merker verhindert Doppelzählungen und
   verfällt mit dem Tab. Auswertung: /stats.html (unverlinkt).
   ============================================================ */
(function () {
    'use strict';

    var lokal = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
    var ENDPUNKT = lokal
        ? 'http://127.0.0.1:8782/api/oz/visits.php'      // Testlauf: php -S auf Port 8782
        : 'https://pillkahn.de/api/oz/visits.php';
    window.OZ_ZAEHLER = ENDPUNKT;                        // stats.html und main.js lesen hier

    /* Auf der Statistikseite selbst wird nichts gezählt */
    if (/\/stats(\.html)?$/.test(location.pathname)) return;

    function senden(felder) {
        var koerper;
        try { koerper = new URLSearchParams(felder); } catch (e) { return; }
        try {
            // sendBeacon überlebt das Verlassen der Seite und braucht kein CORS
            if (navigator.sendBeacon && navigator.sendBeacon(ENDPUNKT, koerper)) return;
        } catch (e) { /* weiter mit fetch */ }
        try {
            fetch(ENDPUNKT, { method: 'POST', body: koerper, keepalive: true, mode: 'no-cors' })
                .catch(function () {});
        } catch (e) { /* dann ohne Zählung */ }
    }
    window.ozZaehlen = senden;

    function einmalJeSitzung(merker) {
        try {
            if (sessionStorage.getItem(merker)) return false;
            sessionStorage.setItem(merker, '1');
            return true;
        } catch (e) {
            return false;            // lieber gar nicht als doppelt zählen
        }
    }

    /* ---------- 1. Besuch mit Herkunft ----------
       Besuche aus Google-Anzeigen bekommen die eigene Herkunft
       „google-ads". Ohne diese Unterscheidung stünden sie als „google.com"
       neben der unbezahlten Suche, und es ließe sich nicht sagen, was eine
       Kampagne gebracht hat. Erkannt wird die Anzeige an der Klick-Kennung,
       die Google an die Zieladresse hängt (gclid, bei Apple-Geräten gbraid
       oder wbraid), ersatzweise an utm_source=google mit utm_medium=cpc.
       Geprüft wird nur, OB eine Kennung da ist — ihr Wert wird weder
       gelesen noch übertragen. Der Zähler behält von „quelle" ohnehin nur
       den Hostnamen, deshalb die Schreibweise als Adresse. */
    function ausAnzeige() {
        try {
            var p = new URLSearchParams(location.search);
            if (p.has('gclid') || p.has('gbraid') || p.has('wbraid')) return true;
            return /google/i.test(p.get('utm_source') || '') &&
                   /^(cpc|ppc|paid)$/i.test(p.get('utm_medium') || '');
        } catch (e) {
            return false;
        }
    }
    if (einmalJeSitzung('oz-besuch')) {
        senden({ aktion: 'besuch', quelle: ausAnzeige() ? 'https://google-ads/' : (document.referrer || '') });
    }

    /* ---------- 2. Klicks ----------
       Schaltflächen mit data-track melden ihre Kennung; Beiträge der
       Blog-Leiste als „blog-beitrag"; übrige externe Links ihren
       Hostnamen, mailto-Links „e-mail". Anker und interne Links nicht. */
    function kennung(ziel) {
        var el = ziel.closest('[data-track]');
        if (el) return el.getAttribute('data-track');
        if (ziel.closest('#sidebar-posts a')) return 'blog-beitrag';
        var a = ziel.closest('a[href]');
        if (!a) return '';
        var href = a.getAttribute('href') || '';
        if (/^mailto:/i.test(href)) return 'e-mail';
        var u;
        try { u = new URL(a.href, location.href); } catch (e) { return ''; }
        if (!/^https?:$/.test(u.protocol)) return '';
        var host = u.hostname.replace(/^www\./, '');
        return host === location.hostname.replace(/^www\./, '') ? '' : host;
    }
    document.addEventListener('click', function (ev) {
        if (!ev.target || !ev.target.closest) return;
        var k = kennung(ev.target);
        if (k) senden({ aktion: 'klick', ziel: k });
    }, true);

    /* ---------- 3. Sichtkontakt Angebotskarten ----------
       Einmal je Sitzung, sobald 15 % des Blocks im Bild sind (mobil ist
       der Block höher als der Bildschirm, ein Drittel wäre kaum erreichbar). */
    function initSicht() {
        var ziel = document.getElementById('angebote');
        if (!ziel || !('IntersectionObserver' in window)) return;
        try { if (sessionStorage.getItem('oz-sicht-angebote')) return; } catch (e) { return; }
        var io = new IntersectionObserver(function (eintraege) {
            eintraege.forEach(function (e) {
                if (!e.isIntersecting) return;
                io.disconnect();
                if (einmalJeSitzung('oz-sicht-angebote')) senden({ aktion: 'sicht', ziel: 'angebote' });
            });
        }, { threshold: 0.15 });
        io.observe(ziel);
    }

    /* ---------- 4. Start des Erklärfilms (szenariofilme.html) ---------- */
    function initFilm() {
        var film = document.getElementById('film-erklaer');
        if (!film) return;
        var gezaehlt = false;
        film.addEventListener('play', function () {
            if (gezaehlt) return;
            gezaehlt = true;
            senden({ aktion: 'klick', ziel: 'szenariofilm-play' });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { initSicht(); initFilm(); });
    } else {
        initSicht(); initFilm();
    }
})();
