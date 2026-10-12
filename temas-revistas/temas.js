/* Galería de temas: lee ../api/temas-revista/index.json y dibuja tarjetas con textContent (nunca innerHTML). */
(function () {
    'use strict';
    var BASE = new URL('../api/temas-revista/', window.location.href);
    var estado = document.getElementById('temas-estado');
    var grilla = document.getElementById('temas-grilla');

    // Solo rutas relativas dentro de /api/temas-revista/: ignora URLs absolutas o con "..".
    function rutaSegura(ruta) {
        if (typeof ruta !== 'string' || /^[a-z][a-z0-9+.-]*:|^\/|\\|\.\./i.test(ruta)) { return null; }
        var u = new URL(ruta, BASE);
        return u.origin === BASE.origin && u.pathname.indexOf(BASE.pathname) === 0 ? u.href : null;
    }

    function el(tag, clase, texto) {
        var n = document.createElement(tag);
        if (clase) { n.className = clase; }
        if (texto !== undefined) { n.textContent = texto; }
        return n;
    }

    function formatoBytes(b) {
        return b > 1048576 ? (b / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(b / 1024)) + ' KB';
    }

    function tarjeta(t) {
        var zip = rutaSegura(t.zip);
        var mini = rutaSegura(t.miniatura);
        if (!zip) { return null; }
        var card = el('article', 'tema-card');
        if (mini) {
            var img = el('img', 'tema-card__img');
            img.src = mini;
            img.alt = 'Vista previa del tema ' + t.nombre;
            img.loading = 'lazy';
            img.width = 600;
            img.height = 424;
            card.appendChild(img);
        }
        var cuerpo = el('div', 'tema-card__body');
        cuerpo.appendChild(el('h3', 'tema-card__titulo', t.nombre));
        cuerpo.appendChild(el('p', 'tema-card__meta', 'por ' + t.autor + ' · v' + t.version + ' · ' + formatoBytes(t.bytes)));
        cuerpo.appendChild(el('p', 'tema-card__desc', t.descripcion));
        var etiquetas = el('ul', 'tema-card__tags');
        (t.etiquetas || []).forEach(function (e) { etiquetas.appendChild(el('li', null, e)); });
        cuerpo.appendChild(etiquetas);
        if (t.premium) {
            cuerpo.appendChild(el('p', 'tema-card__premium', 'Tema premium'));
        } else {
            var a = el('a', 'seo-button', 'Descargar ZIP');
            a.href = zip;
            a.setAttribute('download', '');
            a.rel = 'noopener';
            cuerpo.appendChild(a);
        }
        var det = el('details', 'tema-card__huella');
        det.appendChild(el('summary', null, 'Verificar archivo (SHA-256)'));
        det.appendChild(el('code', null, t.sha256));
        cuerpo.appendChild(det);
        card.appendChild(cuerpo);
        return card;
    }

    fetch(new URL('index.json', BASE).href, { credentials: 'omit', cache: 'no-cache' })
        .then(function (r) { if (!r.ok) { throw new Error('HTTP ' + r.status); } return r.json(); })
        .then(function (idx) {
            var temas = (idx && Array.isArray(idx.temas)) ? idx.temas : [];
            var n = 0;
            temas.forEach(function (t) {
                var c = tarjeta(t);
                if (c) { grilla.appendChild(c); n += 1; }
            });
            estado.textContent = n ? '' : 'Todavía no hay temas publicados. ¡Volvé pronto!';
            if (!n) { return; }
            estado.hidden = true;
        })
        .catch(function () {
            estado.textContent = 'No pudimos cargar la galería. Probá de nuevo en unos minutos.';
        });
})();
