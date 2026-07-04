/* ============================================================
   OPERATION::ZUKUNFT — main.js
   Verhalten der Seite. Reines Vanilla-JS, kein Build-Schritt.
   Module:
     1. Blog-Leiste  — rendert aus posts.js (Datenquelle: George)
     2. Scroll-Reveal — filmische Einblendungen beim Scrollen
     3. Parallax     — sanfte Tiefe im Hero bei Mausbewegung
     4. Videos       — Lazy-Start, prefers-reduced-motion
     5. Navigation   — Scroll-Zustand & Mobilmenü
     6. Download-Counter (Abacus) — unverändert übernommen
   ============================================================ */
(function () {
    'use strict';

    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ---------- 1. Blog-Leiste aus posts.js ----------
       posts.js definiert das globale Array `posts`. Wir sortieren
       nach Datum absteigend, nehmen die neuesten 5 und rendern sie
       in die Sidebar. Fehlt die Datei oder ist das Array leer,
       erscheint ein dezenter Platzhalter — nie ein Fehler. */
    function renderBlog() {
        var container = document.getElementById('sidebar-posts');
        if (!container) return;

        var data = (typeof posts !== 'undefined' && Array.isArray(posts)) ? posts.slice() : [];

        if (data.length === 0) {
            container.innerHTML = '<p class="sidebar-placeholder">Neue Beiträge erscheinen in Kürze.</p>';
            return;
        }

        data.sort(function (a, b) {
            return String(b.datum || '').localeCompare(String(a.datum || ''));
        });

        var html = data.slice(0, 5).map(function (p) {
            var d = formatDate(p.datum);
            return '<a href="' + escapeAttr(p.url) + '" class="sidebar-post" target="_blank" rel="noopener">' +
                       '<span class="sidebar-post-title">' + escapeHtml(p.titel) + '</span>' +
                       '<span class="sidebar-post-date">' + d + '</span>' +
                       (p.teaser ? '<span class="sidebar-post-teaser">' + escapeHtml(p.teaser) + '</span>' : '') +
                   '</a>';
        }).join('');

        container.innerHTML = html;
    }

    /* ISO-Datum (2026-07-01) → deutsche Anzeige (01.07.2026) */
    function formatDate(iso) {
        if (!iso || !/^\d{4}-\d{2}-\d{2}/.test(iso)) return '';
        var p = iso.split('-');
        return p[2].slice(0, 2) + '.' + p[1] + '.' + p[0];
    }

    /* Minimale Absicherung gegen kaputtes Markup in den Daten */
    function escapeHtml(s) {
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
    function escapeAttr(s) {
        return escapeHtml(s).replace(/"/g, '&quot;');
    }

    /* ---------- 2. Scroll-Reveal ----------
       Alle Elemente mit .reveal blenden sich ein, sobald sie in den
       Viewport treten. Bei reduzierter Bewegung: sofort sichtbar. */
    function initReveal() {
        var els = document.querySelectorAll('.reveal');
        if (reducedMotion || !('IntersectionObserver' in window)) {
            els.forEach(function (el) { el.classList.add('visible'); });
            return;
        }
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
        els.forEach(function (el) { io.observe(el); });
    }

    /* ---------- 3. Parallax im Hero ----------
       Sanfte Tiefe bei Mausbewegung, über requestAnimationFrame
       entkoppelt — kein Layout-Thrashing, nur transform. */
    function initParallax() {
        if (reducedMotion) return;
        var hero = document.querySelector('.hero');
        var layers = document.querySelectorAll('.hero .parallax-layer');
        if (!hero || layers.length === 0) return;

        var targetX = 0, targetY = 0, curX = 0, curY = 0, raf = null;

        hero.addEventListener('mousemove', function (e) {
            var r = hero.getBoundingClientRect();
            targetX = (e.clientX - r.left) / r.width - 0.5;   // -0.5 … 0.5
            targetY = (e.clientY - r.top) / r.height - 0.5;
            if (!raf) raf = requestAnimationFrame(tick);
        });
        hero.addEventListener('mouseleave', function () {
            targetX = 0; targetY = 0;
            if (!raf) raf = requestAnimationFrame(tick);
        });

        function tick() {
            // weiches Nachziehen (Lerp) für filmische Trägheit
            curX += (targetX - curX) * 0.06;
            curY += (targetY - curY) * 0.06;
            layers.forEach(function (layer, i) {
                var depth = (i + 1) * 7; // hintere Ebenen bewegen sich stärker
                layer.style.transform =
                    'translate3d(' + (-curX * depth) + 'px,' + (-curY * depth) + 'px,0)';
            });
            if (Math.abs(targetX - curX) > 0.001 || Math.abs(targetY - curY) > 0.001) {
                raf = requestAnimationFrame(tick);
            } else {
                raf = null;
            }
        }
    }

    /* ---------- 4. Videos ----------
       Autoplay-Loops sind stumm und mit Poster hinterlegt.
       Bei prefers-reduced-motion: pausieren, Poster bleibt stehen.
       Videos außerhalb des Viewports werden pausiert (Akku/CPU). */
    function initVideos() {
        var videos = document.querySelectorAll('video[data-cinema]');
        if (videos.length === 0) return;

        if (reducedMotion) {
            videos.forEach(function (v) {
                v.removeAttribute('autoplay');
                v.pause();
            });
            return;
        }

        if ('IntersectionObserver' in window) {
            var io = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    var v = entry.target;
                    if (entry.isIntersecting) {
                        var p = v.play();
                        if (p && p.catch) p.catch(function () { /* Autoplay blockiert → Poster bleibt */ });
                    } else {
                        v.pause();
                    }
                });
            }, { threshold: 0.15 });
            videos.forEach(function (v) { io.observe(v); });
        }
    }

    /* ---------- 5. Navigation ---------- */
    function initNav() {
        var nav = document.querySelector('nav');
        var toggle = document.querySelector('.nav-toggle');
        var links = document.querySelector('.nav-links');

        // feine Trennlinie erst nach dem ersten Scrollen
        var onScroll = function () {
            if (nav) nav.classList.toggle('scrolled', window.scrollY > 24);
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();

        if (toggle && links) {
            toggle.addEventListener('click', function () {
                var open = links.classList.toggle('open');
                toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
            });
            // Menü schließt nach Klick auf einen Anker
            links.querySelectorAll('a').forEach(function (a) {
                a.addEventListener('click', function () {
                    links.classList.remove('open');
                    toggle.setAttribute('aria-expanded', 'false');
                });
            });
        }

        // Impressum-Toggle im Footer
        var impBtn = document.querySelector('.impressum-toggle');
        var imp = document.getElementById('impressum');
        if (impBtn && imp) {
            impBtn.addEventListener('click', function () {
                var open = imp.classList.toggle('open');
                impBtn.textContent = open ? 'Impressum ▲' : 'Impressum ▼';
                impBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
            });
        }
    }

    /* ---------- 6. Download-Counter (Abacus) ----------
       Unverändert von der Vorgängerseite übernommen.
       Zählt Downloads der Workbook-Basisversionen. */
    var COUNTER_NS = 'operation-zukunft.de';
    var COUNTERS = {
        'openclaw-basis': 'counter-openclaw-basis'
        // Workbook 2: 'strategie-basis': 'counter-strategie-basis',
        // Workbook 3: 'claude-basis':    'counter-claude-basis'
    };

    function loadCount(key, elemId) {
        fetch('https://abacus.jasoncameron.dev/get/' + COUNTER_NS + '/' + key)
            .then(function (r) { return r.ok ? r.json() : null; })
            .then(function (d) {
                var el = document.getElementById(elemId);
                if (el && d && typeof d.value === 'number') {
                    el.textContent = d.value.toLocaleString('de-DE');
                } else if (el) {
                    el.textContent = '0';
                }
            })
            .catch(function () {
                var el = document.getElementById(elemId);
                if (el) el.textContent = '–';
            });
    }

    window.trackDownload = function (key) {
        var elemId = COUNTERS[key];
        if (!elemId) return;
        fetch('https://abacus.jasoncameron.dev/hit/' + COUNTER_NS + '/' + key)
            .then(function (r) { return r.ok ? r.json() : null; })
            .then(function (d) {
                var el = document.getElementById(elemId);
                if (el && d && typeof d.value === 'number') {
                    el.textContent = d.value.toLocaleString('de-DE');
                }
            })
            .catch(function () { /* Download läuft trotzdem weiter */ });
    };

    /* ---------- Start ---------- */
    document.addEventListener('DOMContentLoaded', function () {
        renderBlog();
        initReveal();
        initParallax();
        initVideos();
        initNav();
        Object.keys(COUNTERS).forEach(function (key) {
            loadCount(key, COUNTERS[key]);
        });
    });
})();
