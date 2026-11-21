/* ============================================================
   OPERATION::ZUKUNFT — aktion.js
   Black-Week-Aktion der Strategie-Pakete (bis einschließlich
   18.12.2026). Ab 19.12.2026, 00:00 Uhr Berliner Zeit:
   alle [data-bw] ausblenden, alle [data-bw-nach] einblenden.
   Ohne JavaScript bleibt der Aktionsstand sichtbar (akzeptiert).
   Eingebunden auf index.html und strategie-pakete.html.
   ============================================================ */
(function () {
    'use strict';
    var ENDE = Date.parse('2026-12-19T00:00:00+01:00');

    function anwenden() {
        if (!(Date.now() >= ENDE)) return;
        var i, alt = document.querySelectorAll('[data-bw]'),
            neu = document.querySelectorAll('[data-bw-nach]');
        for (i = 0; i < alt.length; i++) alt[i].hidden = true;
        for (i = 0; i < neu.length; i++) neu[i].hidden = false;
    }
    window.ozAktion = anwenden;   // für den Test in der Konsole

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', anwenden);
    } else {
        anwenden();
    }
})();
