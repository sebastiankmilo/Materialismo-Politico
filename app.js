/* Lector estático · HTML5 vanilla */
(() => {
  "use strict";

  const D = window.SITE_DATA;
  if (!D) {
    document.body.innerHTML = "<p style='padding:2rem'>No se encontró data.js.</p>";
    return;
  }

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  const SECTIONS = ["texto", "vocabulario", "fuentes"];
  const THEME_LABELS = {
    ontologia: "Ontología",
    escolastica: "Escolástica",
    "materialismo-filosofico": "Materialismo filosófico",
    "fundamentos-materialismo-politico": "Fundamentos del materialismo político",
    "materialismo-historico": "Materialismo histórico",
  };

  const state = {
    vocabQuery: "",
    vocabSort: "az",
    vocabTable: "all",
    vocabThemes: new Set(),
    fuentesQuery: "",
    fuentesSort: "az",
    activeThemes: new Set(), // alias used by chips
  };

  /* ------------------------------------------------------------ utils */

  const norm = (s) =>
    (s || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();

  const themeLabel = (t) => THEME_LABELS[t] || t.replace(/-/g, " ");

  const collator = new Intl.Collator("es", { sensitivity: "base", numeric: true });

  function debounce(fn, ms) {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), ms);
    };
  }

  /* ------------------------------------------------------------ theme */

  function initTheme() {
    const saved = localStorage.getItem("lector-theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const theme = saved || (prefersDark ? "dark" : "light");
    document.documentElement.dataset.theme = theme;
  }

  function toggleTheme() {
    const cur = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = cur;
    localStorage.setItem("lector-theme", cur);
  }

  /* ------------------------------------------------------------ toast */

  let toastTimer;
  function toast(main, sub) {
    const el = $("#toast");
    el.innerHTML = "";
    el.append(document.createTextNode(main));
    if (sub) {
      const s = document.createElement("span");
      s.className = "toast-sub";
      s.textContent = sub;
      el.append(s);
    }
    el.hidden = false;
    requestAnimationFrame(() => el.classList.add("show"));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      el.classList.remove("show");
      setTimeout(() => (el.hidden = true), 300);
    }, 2600);
  }

  /* ------------------------------------------------------------ render: texto */

  function renderTexto() {
    $("#doc-title").textContent = D.meta.title || "Documento";
    $("#doc-author").textContent = D.meta.author || "—";

    const st = D.stats;
    $("#hero-stats").innerHTML = [
      `<span class="stat-pill"><b>${st.chapters}</b> capítulos</span>`,
      `<span class="stat-pill"><b>${st.verses}</b> versículos</span>`,
      `<span class="stat-pill"><b>${st.terms}</b> términos</span>`,
      `<span class="stat-pill"><b>${st.sources}</b> fuentes</span>`,
    ].join("");

    $("#texto-content").innerHTML = D.chapters
      .map(
        (c) => `
      <section class="chapter" id="cap-${c.num}" data-chapter="${c.num}">
        <h2><span class="chap-kicker">${c.num}.</span> ${escapeHtml(c.title)}</h2>
        ${c.html}
      </section>`
      )
      .join("");

    $("#chap-nav").innerHTML = D.chapters
      .map(
        (c) => `
      <a href="#cap-${c.num}" data-chapter="${c.num}">
        <span class="n">${c.num}</span>
        <span>${escapeHtml(c.title)}</span>
      </a>`
      )
      .join("");
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /* ------------------------------------------------------------ render: vocabulario */

  function vocabHaystack(e) {
    return norm(
      [
        e.term,
        e.definitionPlain,
        e.examplePlain,
        e.sourcePlain,
        e.themes.map(themeLabel).join(" "),
        e.citesText,
        e.date,
      ].join(" \n ")
    );
  }

  function sortVocab(list) {
    const arr = [...list];
    switch (state.vocabSort) {
      case "za":
        arr.sort((a, b) => collator.compare(b.term, a.term) || collator.compare(a.subindex, b.subindex));
        break;
      case "indice": {
        // Orden de aparición en el documento: capítulo → versículo.
        // Sin cita: al final. Mismo verso: subíndice y luego alfabético.
        const key = (e) =>
          e.primaryCite ? [e.primaryCite.ch, e.primaryCite.v] : [Infinity, Infinity];
        arr.sort((a, b) => {
          const [ca, va] = key(a);
          const [cb, vb] = key(b);
          if (ca !== cb) return ca - cb;
          if (va !== vb) return va - vb;
          return (
            (parseInt(a.index, 10) || 0) - (parseInt(b.index, 10) || 0) ||
            collator.compare(a.subindex, b.subindex) ||
            collator.compare(a.term, b.term)
          );
        });
        break;
      }
      case "tabla":
        arr.sort(
          (a, b) =>
            a.table - b.table ||
            (parseInt(a.index, 10) || 0) - (parseInt(b.index, 10) || 0) ||
            collator.compare(a.subindex, b.subindex) ||
            collator.compare(a.term, b.term)
        );
        break;
      case "tema":
        arr.sort(
          (a, b) =>
            collator.compare(
              (a.themes[0] || "").toLowerCase(),
              (b.themes[0] || "").toLowerCase()
            ) || collator.compare(a.term, b.term)
        );
        break;
      default:
        arr.sort((a, b) => collator.compare(a.term, b.term) || collator.compare(a.subindex, b.subindex));
    }
    return arr;
  }

  function filterVocab() {
    const tokens = norm(state.vocabQuery).split(/\s+/).filter(Boolean);
    let list = D.vocabulary.filter((e) => {
      if (state.vocabTable !== "all" && String(e.table) !== state.vocabTable) return false;
      if (state.vocabThemes.size && !e.themes.some((t) => state.vocabThemes.has(t))) return false;
      if (tokens.length) {
        const hay = vocabHaystack(e);
        if (!tokens.every((t) => hay.includes(t))) return false;
      }
      return true;
    });
    return sortVocab(list);
  }

  function renderThemeChips() {
    $("#theme-chips").innerHTML = D.themes
      .map(
        (t) => `
      <button type="button" class="theme-chip${state.vocabThemes.has(t) ? " active" : ""}" data-theme="${escapeHtml(t)}">
        ${escapeHtml(themeLabel(t))}
      </button>`
      )
      .join("");
  }

  function renderVocab() {
    const list = filterVocab();
    const grid = $("#vocab-grid");
    grid.innerHTML = list.map(vocabCardHtml).join("");
    $("#vocab-empty").hidden = list.length > 0;
    $("#vocab-count").textContent = list.length
      ? `Mostrando ${list.length} de ${D.vocabulary.length} fichas`
      : `0 de ${D.vocabulary.length} fichas`;
  }

  function vocabCardHtml(e) {
    const badges = [];
    badges.push(
      `<span class="badge badge-idx" title="Índice alfabético en su tabla">${escapeHtml(
        (e.index || "—") + (e.subindex && e.subindex !== "1" ? "." + e.subindex : "")
      )}</span>`
    );
    badges.push(
      `<span class="badge badge-table" title="${
        e.table === 1 ? "Vocabulario con definición" : "Palabras a tener en cuenta"
      }">T${e.table}</span>`
    );
    if (e.sinAcuerdo) {
      badges.push(`<span class="badge badge-warn" title="Definición pendiente de acuerdo">sin acuerdo</span>`);
    }

    const acept = e.subindex && e.subindex !== "1" ? ` <span class="badge badge-idx">acepción ${e.subindex}</span>` : "";

    const def = e.definition
      ? `<p class="def">${e.definition}</p>`
      : "";

    const example = e.example
      ? `<blockquote class="example"><span class="label">Ejemplo / cita</span>${e.example}</blockquote>`
      : "";

    let src = "";
    if (e.source) {
      src = `<div class="src-line"><span class="label">Fuente</span>${
        e.sourceIsCite ? e.source : `<span class="plain-src">${e.source}</span>`
      }</div>`;
    } else if (e.sourcePlain) {
      src = `<div class="src-line"><span class="label">Fuente</span><span class="plain-src">${escapeHtml(
        e.sourcePlain
      )}</span></div>`;
    }

    const tags = e.themes
      .map(
        (t) =>
          `<button type="button" class="tag" data-theme-jump="${escapeHtml(t)}" title="Filtrar por este tema">${escapeHtml(
            themeLabel(t)
          )}</button>`
      )
      .join("");

    return `
    <article class="vcard" id="${e.id}" data-table="${e.table}" data-themes="${escapeHtml(
      e.themes.join(" ")
    )}">
      <div class="vcard-head">
        <h3>${escapeHtml(e.term)}${acept}</h3>
        <div class="vcard-badges">${badges.join("")}</div>
      </div>
      ${def}
      ${example}
      ${src}
      <div class="vcard-meta">
        ${e.date ? `<time class="meta-date" datetime="${escapeHtml(e.date)}">${escapeHtml(e.date)}</time>` : ""}
        ${tags}
      </div>
    </article>`;
  }

  /* ------------------------------------------------------------ render: fuentes */

  function sortFuentes(list) {
    const arr = [...list];
    switch (state.fuentesSort) {
      case "za":
        arr.sort((a, b) => collator.compare(b.plain, a.plain));
        break;
      case "usos":
        arr.sort((a, b) => b.uses - a.uses || collator.compare(a.plain, b.plain));
        break;
      case "original":
        arr.sort((a, b) => parseInt(a.id.slice(2), 10) - parseInt(b.id.slice(2), 10));
        break;
      default:
        arr.sort((a, b) => collator.compare(a.plain, b.plain));
    }
    return arr;
  }

  function filterFuentes() {
    const tokens = norm(state.fuentesQuery).split(/\s+/).filter(Boolean);
    let list = D.sources.filter((s) => {
      if (!tokens.length) return true;
      const hay = norm([s.plain, s.citesText].join(" "));
      return tokens.every((t) => hay.includes(t));
    });
    return sortFuentes(list);
  }

  function renderFuentes() {
    const list = filterFuentes();
    $("#fuentes-list").innerHTML = list
      .map(
        (s) => `
      <article class="scard" id="${s.id}">
        <p class="ref">${s.html}</p>
        <div class="cites">
          ${
            s.cited
              ? `<span class="cites-label">Usada en</span>${s.chips}`
              : `<span class="uncited">— no citada en el cuerpo</span>`
          }
        </div>
      </article>`
      )
      .join("");
    $("#fuentes-empty").hidden = list.length > 0;
    $("#fuentes-count").textContent = list.length
      ? `Mostrando ${list.length} de ${D.sources.length} referencias`
      : `0 de ${D.sources.length} referencias`;
  }

  /* ------------------------------------------------------------ navigation */

  function showSection(name, { keepScroll = false } = {}) {
    for (const s of SECTIONS) {
      $("#sec-" + s).hidden = s !== name;
    }
    $$(".main-nav a").forEach((a) => {
      a.classList.toggle("active", a.dataset.nav === name);
    });
    if (!keepScroll) window.scrollTo({ top: 0, behavior: "auto" });
  }

  function clearLocated() {
    $$(".verse.located").forEach((el) => el.classList.remove("located"));
    $$(".vcard.located").forEach((el) => el.classList.remove("located"));
    $$(".scard.located").forEach((el) => el.classList.remove("located"));
  }

  function markActiveChapter(num) {
    $$("#chap-nav a").forEach((a) => {
      a.classList.toggle("active", a.dataset.chapter === String(num));
    });
  }

  function locateVerse(ch, v, { scroll = true } = {}) {
    const id = `v${ch}-${v}`;
    const anchor = document.getElementById(id);
    if (!anchor) {
      toast(`No existe ${ch}:${v}`);
      return false;
    }
    clearLocated();
    const key = `${ch}:${v}`;
    const parts = $$(`[data-verse="${key}"]`);
    parts.forEach((el) => el.classList.add("located"));
    markActiveChapter(ch);
    if (scroll) {
      anchor.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    const chap = D.chapters.find((c) => c.num === ch);
    toast(`${ch}:${v}`, chap ? chap.title : "");
    return true;
  }

  function locateEntry(id, { scroll = true } = {}) {
    const el = document.getElementById(id);
    if (!el) {
      toast("Ficha no visible (fuera del filtro actual)");
      return false;
    }
    clearLocated();
    el.classList.add("located");
    if (scroll) el.scrollIntoView({ behavior: "smooth", block: "center" });
    const term = el.querySelector("h3");
    toast("Vocabulario", term ? term.textContent : id);
    return true;
  }

  function locateSource(id, { scroll = true } = {}) {
    const el = document.getElementById(id);
    if (!el) {
      toast("Referencia no visible (fuera del filtro actual)");
      return false;
    }
    clearLocated();
    el.classList.add("located");
    if (scroll) el.scrollIntoView({ behavior: "smooth", block: "center" });
    toast("Fuentes");
    return true;
  }

  function ensureEntryVisible(id) {
    // Si la ficha está filtrada, limpiar filtres para poder mostrarla.
    const inData = D.vocabulary.some((e) => e.id === id);
    if (!inData) return false;
    const el = document.getElementById(id);
    if (el) return true;
    // reset filters
    state.vocabQuery = "";
    state.vocabTable = "all";
    state.vocabThemes.clear();
    $("#vocab-search").value = "";
    $("#vocab-table").value = "all";
    renderThemeChips();
    renderVocab();
    return !!document.getElementById(id);
  }

  function ensureSourceVisible(id) {
    const el = document.getElementById(id);
    if (el) return true;
    state.fuentesQuery = "";
    $("#fuentes-search").value = "";
    renderFuentes();
    return !!document.getElementById(id);
  }

  function handleHash({ initial = false } = {}) {
    const raw = location.hash.replace(/^#/, "");
    if (!raw) {
      showSection("texto", { keepScroll: !initial });
      return;
    }

    let m;
    if ((m = raw.match(/^v(\d+)-(\d+)$/))) {
      showSection("texto", { keepScroll: true });
      // si venimos de otra sección, asegurar scroll hacia el verso
      requestAnimationFrame(() => locateVerse(+m[1], +m[2]));
      return;
    }
    if ((m = raw.match(/^t-\d+$/))) {
      showSection("vocabulario", { keepScroll: true });
      requestAnimationFrame(() => {
        ensureEntryVisible(raw);
        locateEntry(raw);
      });
      return;
    }
    if ((m = raw.match(/^s-\d+$/))) {
      showSection("fuentes", { keepScroll: true });
      requestAnimationFrame(() => {
        ensureSourceVisible(raw);
        locateSource(raw);
      });
      return;
    }
    if (raw.startsWith("cap-")) {
      showSection("texto", { keepScroll: true });
      const el = document.getElementById(raw);
      if (el) {
        requestAnimationFrame(() => {
          clearLocated();
          el.scrollIntoView({ behavior: "smooth", block: "start" });
          markActiveChapter(el.dataset.chapter);
        });
      }
      return;
    }
    if (SECTIONS.includes(raw)) {
      showSection(raw);
      return;
    }
    showSection("texto", { keepScroll: true });
  }

  /* clics en enlaces internos: si el hash no cambia, forzar ubicación */
  function onDocumentClick(e) {
    const a = e.target.closest("a[href^='#']");
    if (!a) return;
    const href = a.getAttribute("href");
    if (!href || href === "#") return;

    const verseMatch = href.match(/^#v(\d+)-(\d+)$/);
    const termMatch = href.match(/^#t-\d+$/);
    const srcMatch = href.match(/^#s-\d+$/);

    if (verseMatch || termMatch || srcMatch) {
      e.preventDefault();
      const target = href.slice(1);
      if (location.hash === href) {
        // ya en ese hash: reubicar a mano
        if (verseMatch) {
          showSection("texto", { keepScroll: true });
          locateVerse(+verseMatch[1], +verseMatch[2]);
        } else if (termMatch) {
          showSection("vocabulario", { keepScroll: true });
          ensureEntryVisible(target);
          locateEntry(target);
        } else {
          showSection("fuentes", { keepScroll: true });
          ensureSourceVisible(target);
          locateSource(target);
        }
      } else {
        history.pushState(null, "", href);
        handleHash();
      }
      closeMenu();
      return;
    }

    // enlaces de sección / capítulos
    if (href.startsWith("#")) {
      const id = href.slice(1);
      if (SECTIONS.includes(id) || id.startsWith("cap-")) {
        e.preventDefault();
        if (location.hash === href) {
          handleHash();
        } else {
          history.pushState(null, "", href);
          handleHash();
        }
        closeMenu();
      }
    }
  }

  /* ------------------------------------------------------------ scroll spy */

  function initScrollSpy() {
    const chapters = $$(".chapter");
    if (!chapters.length || !("IntersectionObserver" in window)) return;
    const io = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((en) => en.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible.length) {
          markActiveChapter(visible[0].target.dataset.chapter);
        }
      },
      { rootMargin: "-20% 0px -65% 0px", threshold: 0 }
    );
    chapters.forEach((ch) => io.observe(ch));
  }

  /* ------------------------------------------------------------ menu móvil */

  function closeMenu() {
    $(".main-nav").classList.remove("open");
    $("#menu-toggle").setAttribute("aria-expanded", "false");
  }

  /* ------------------------------------------------------------ eventos */

  function bindEvents() {
    window.addEventListener("hashchange", () => handleHash());
    window.addEventListener("popstate", () => handleHash());
    document.addEventListener("click", onDocumentClick);

    $("#theme-toggle").addEventListener("click", toggleTheme);
    $("#menu-toggle").addEventListener("click", () => {
      const nav = $(".main-nav");
      const open = nav.classList.toggle("open");
      $("#menu-toggle").setAttribute("aria-expanded", String(open));
    });

    // vocabulario
    $("#vocab-search").addEventListener(
      "input",
      debounce((e) => {
        state.vocabQuery = e.target.value;
        renderVocab();
      }, 140)
    );
    $("#vocab-sort").addEventListener("change", (e) => {
      state.vocabSort = e.target.value;
      renderVocab();
    });
    $("#vocab-table").addEventListener("change", (e) => {
      state.vocabTable = e.target.value;
      renderVocab();
    });
    $("#vocab-clear").addEventListener("click", () => {
      state.vocabQuery = "";
      state.vocabTable = "all";
      state.vocabSort = "az";
      state.vocabThemes.clear();
      $("#vocab-search").value = "";
      $("#vocab-table").value = "all";
      $("#vocab-sort").value = "az";
      renderThemeChips();
      renderVocab();
    });

    $("#theme-chips").addEventListener("click", (e) => {
      const btn = e.target.closest("[data-theme]");
      if (!btn) return;
      const t = btn.dataset.theme;
      if (state.vocabThemes.has(t)) state.vocabThemes.delete(t);
      else state.vocabThemes.add(t);
      renderThemeChips();
      renderVocab();
    });

    $("#vocab-grid").addEventListener("click", (e) => {
      const tag = e.target.closest("[data-theme-jump]");
      if (!tag) return;
      const t = tag.dataset.themeJump;
      state.vocabThemes.clear();
      state.vocabThemes.add(t);
      renderThemeChips();
      renderVocab();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // fuentes
    $("#fuentes-search").addEventListener(
      "input",
      debounce((e) => {
        state.fuentesQuery = e.target.value;
        renderFuentes();
      }, 140)
    );
    $("#fuentes-sort").addEventListener("change", (e) => {
      state.fuentesSort = e.target.value;
      renderFuentes();
    });
    $("#fuentes-clear").addEventListener("click", () => {
      state.fuentesQuery = "";
      state.fuentesSort = "az";
      $("#fuentes-search").value = "";
      $("#fuentes-sort").value = "az";
      renderFuentes();
    });

    // atajo "/" para buscar
    document.addEventListener("keydown", (e) => {
      if (e.key === "/" && !e.metaKey && !e.ctrlKey) {
        const tag = (document.activeElement && document.activeElement.tagName) || "";
        if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
        e.preventDefault();
        const active = !$("#sec-vocabulario").hidden
          ? "#vocab-search"
          : !$("#sec-fuentes").hidden
          ? "#fuentes-search"
          : null;
        if (active) {
          $(active).focus();
        } else {
          history.pushState(null, "", "#vocabulario");
          handleHash();
          setTimeout(() => $("#vocab-search").focus(), 50);
        }
      }
      if (e.key === "Escape") closeMenu();
    });
  }

  /* ------------------------------------------------------------ init */

  function init() {
    initTheme();
    renderTexto();
    renderThemeChips();
    renderVocab();
    renderFuentes();
    bindEvents();
    initScrollSpy();
    handleHash({ initial: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
