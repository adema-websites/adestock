(function () {
  'use strict';

  var data = null;
  var container = document.getElementById('tutorial-chapters');
  if (!container) return;

  function getLang() {
    if (window.ADEi18n && typeof window.ADEi18n.detectLang === 'function') {
      return window.ADEi18n.detectLang();
    }
    return 'es';
  }

  function pick(textByLang, lang) {
    if (!textByLang) return '';
    return textByLang[lang] || textByLang.es || '';
  }

  function renderVideo(chapter, lang) {
    if (chapter.video) {
      return (
        '<div class="video-placeholder">' +
          '<iframe width="100%" height="315" src="' + chapter.video + '" title="' + pick(chapter.videoTitle, lang) + '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>' +
        '</div>'
      );
    }

    return (
      '<div class="video-placeholder">' +
        '<div class="video-placeholder-text">' +
          '<i class="fab fa-youtube"></i>' +
          '<span>' + pick(chapter.videoLabel, lang) + '</span>' +
        '</div>' +
      '</div>'
    );
  }

  function renderChapter(chapter, lang) {
    var html =
      '<article id="' + chapter.id + '" class="tutorial-card">' +
        '<div class="tutorial-header">' +
          '<h2>' + pick(chapter.title, lang) + '</h2>' +
        '</div>' +
        '<div class="tutorial-content">' +
          '<div class="objective">' +
            '<strong>' + (lang === 'en' ? 'Objective:' : lang === 'pt' ? 'Objetivo:' : 'Objetivo:') + '</strong> ' + pick(chapter.objective, lang) +
          '</div>';

    var steps = chapter.steps ? (chapter.steps[lang] || chapter.steps.es || []) : [];
    if (steps.length) {
      html += '<h3>' + (lang === 'en' ? 'Step by step:' : lang === 'pt' ? 'Passo a passo:' : 'Paso a paso:') + '</h3>';
      html += '<ol class="step-list">';
      steps.forEach(function (step) {
        html += '<li>' + step + '</li>';
      });
      html += '</ol>';
    }

    if (chapter.result) {
      html +=
        '<div class="expected-result">' +
          '<strong>' + (lang === 'en' ? 'Expected result:' : lang === 'pt' ? 'Resultado esperado:' : 'Resultado esperado:') + '</strong> ' + pick(chapter.result, lang) +
        '</div>';
    }

    html += renderVideo(chapter, lang);
    html += '</div></article>';
    return html;
  }

  function renderAll() {
    if (!data || !data.chapters) return;
    var lang = getLang();
    container.innerHTML = data.chapters.map(function (chapter) {
      return renderChapter(chapter, lang);
    }).join('');
  }

  fetch('tutoriales/chapters/index.json')
    .then(function (response) { return response.json(); })
    .then(function (manifest) {
      var entries = manifest && manifest.chapters ? manifest.chapters : [];
      return Promise.all(entries.map(function (entry) {
        return fetch(entry.file).then(function (response) { return response.json(); });
      }));
    })
    .then(function (chapters) {
      data = { chapters: chapters };
      renderAll();
    })
    .catch(function () {
      container.innerHTML = '';
    });

  document.addEventListener('adestock:langchange', renderAll);
})();
