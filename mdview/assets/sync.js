(function () {
  "use strict";

  const rawView = document.getElementById("raw-view");
  const renderedView = document.getElementById("rendered-view");

  let syncing = false;
  let attached = false;

  function withSyncGuard(fn) {
    syncing = true;
    fn();
    requestAnimationFrame(function () {
      syncing = false;
    });
  }

  function syncRenderedToRaw() {
    if (syncing) {
      return;
    }
    const line = window.mdview.topmostRenderedLine();
    if (line === null) {
      return;
    }
    const index = Math.min(Math.max(line, 1), Math.max(rawView.children.length, 1)) - 1;
    const target = rawView.children[index];
    if (!target) {
      return;
    }
    withSyncGuard(function () {
      rawView.scrollTop = target.offsetTop;
    });
  }

  function syncRawToRendered() {
    if (syncing) {
      return;
    }
    const line = window.mdview.topmostRawLine();
    const elements = renderedView.querySelectorAll("[data-line]");
    let target = null;
    for (let i = 0; i < elements.length; i++) {
      const el = elements[i];
      const [start, end] = el.dataset.line.split("-").map(Number);
      if (line >= start && line <= end) {
        target = el;
        break;
      }
      if (start > line) {
        break;
      }
      target = el;
    }
    if (!target && elements.length > 0) {
      target = elements[0];
    }
    if (!target) {
      return;
    }
    withSyncGuard(function () {
      renderedView.scrollTop = target.offsetTop;
    });
  }

  function onRenderedScroll() {
    syncRenderedToRaw();
  }

  function onRawScroll() {
    syncRawToRendered();
  }

  function detach() {
    renderedView.removeEventListener("scroll", onRenderedScroll);
    rawView.removeEventListener("scroll", onRawScroll);
    attached = false;
  }

  function attach() {
    detach();
    renderedView.addEventListener("scroll", onRenderedScroll);
    rawView.addEventListener("scroll", onRawScroll);
    attached = true;
  }

  function realign() {
    if (!attached) {
      return;
    }
    syncRenderedToRaw();
  }

  window.mdviewSync = {
    attach: attach,
    detach: detach,
    realign: realign,
  };
})();
