(function () {
  "use strict";

  const rawView = document.getElementById("raw-view");
  const renderedView = document.getElementById("rendered-view");

  function api() {
    return window.pywebview.api;
  }

  const toast = document.getElementById("toast");
  let toastTimer = null;

  function showToast(message) {
    toast.textContent = message;
    toast.hidden = false;
    if (toastTimer) {
      clearTimeout(toastTimer);
    }
    toastTimer = setTimeout(function () {
      toast.hidden = true;
    }, 1800);
  }

  function copyReference(start, end) {
    api()
      .copy_reference(start, end)
      .then(function (text) {
        if (text) {
          showToast("Copied reference");
        }
      });
  }

  function copyReferenceWithContent(start, end) {
    api()
      .copy_reference_with_content(start, end)
      .then(function (text) {
        if (text) {
          showToast("Copied reference with content");
        }
      });
  }

  function copyPlainText() {
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) {
      return;
    }
    const text = selection.toString();
    if (!text) {
      return;
    }
    api()
      .copy_plain_text(text)
      .then(function (result) {
        if (result) {
          showToast("Copied");
        }
      });
  }

  function containerOf(node) {
    if (node && rawView.contains(node)) {
      return "raw";
    }
    if (node && renderedView.contains(node)) {
      return "rendered";
    }
    return null;
  }

  function rawLineNumber(node) {
    let el = node.nodeType === Node.TEXT_NODE ? node.parentElement : node;
    while (el && el !== rawView && !el.classList.contains("raw-line")) {
      el = el.parentElement;
    }
    if (!el || el === rawView) {
      return null;
    }
    return Array.prototype.indexOf.call(rawView.children, el) + 1;
  }

  function renderedLineRange(node) {
    let el = node.nodeType === Node.TEXT_NODE ? node.parentElement : node;
    while (el && el !== renderedView && !el.hasAttribute("data-line")) {
      el = el.parentElement;
    }
    if (!el || el === renderedView) {
      return null;
    }
    const [start, end] = el.dataset.line.split("-").map(Number);
    return { start: start, end: end };
  }

  function resolveSelectionRange(pane, selection) {
    if (pane === "raw") {
      const anchorLine = rawLineNumber(selection.anchorNode);
      const focusLine = rawLineNumber(selection.focusNode);
      if (anchorLine === null || focusLine === null) {
        return null;
      }
      return { start: Math.min(anchorLine, focusLine), end: Math.max(anchorLine, focusLine) };
    }
    const anchorRange = renderedLineRange(selection.anchorNode);
    const focusRange = renderedLineRange(selection.focusNode);
    if (!anchorRange || !focusRange) {
      return null;
    }
    return {
      start: Math.min(anchorRange.start, focusRange.start),
      end: Math.max(anchorRange.end, focusRange.end),
    };
  }

  function currentRange() {
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) {
      return null;
    }
    const pane = containerOf(selection.anchorNode);
    if (!pane) {
      return null;
    }
    return resolveSelectionRange(pane, selection);
  }

  function handleCopyReference(event) {
    const range = currentRange();
    if (!range) {
      return;
    }
    event.preventDefault();
    copyReference(range.start, range.end);
  }

  function handleCopyWithContent(event) {
    const range = currentRange();
    if (!range) {
      return;
    }
    event.preventDefault();
    copyReferenceWithContent(range.start, range.end);
  }

  document.addEventListener("keydown", function (event) {
    if (!event.ctrlKey || event.key.toLowerCase() !== "c") {
      return;
    }
    if (event.shiftKey) {
      handleCopyWithContent(event);
    } else {
      handleCopyReference(event);
    }
  });

  const contentArea = document.getElementById("content-area");
  const contextMenu = document.getElementById("copy-context-menu");

  function hideContextMenu() {
    contextMenu.hidden = true;
  }

  function showContextMenu(x, y, range) {
    const items = contextMenu.querySelectorAll("[data-action]");
    items.forEach(function (item) {
      item.classList.toggle("disabled", !range);
    });
    contextMenu.style.left = x + "px";
    contextMenu.style.top = y + "px";
    contextMenu.dataset.start = range ? String(range.start) : "";
    contextMenu.dataset.end = range ? String(range.end) : "";
    contextMenu.hidden = false;
  }

  contentArea.addEventListener("contextmenu", function (event) {
    event.preventDefault();
    showContextMenu(event.clientX, event.clientY, currentRange());
  });

  contextMenu.addEventListener("click", function (event) {
    const item = event.target.closest("[data-action]");
    hideContextMenu();
    if (!item || item.classList.contains("disabled")) {
      return;
    }
    if (item.dataset.action === "copy-plain") {
      copyPlainText();
      return;
    }
    const start = Number(contextMenu.dataset.start);
    const end = Number(contextMenu.dataset.end);
    if (!start || !end) {
      return;
    }
    if (item.dataset.action === "reference") {
      copyReference(start, end);
    } else if (item.dataset.action === "reference-content") {
      copyReferenceWithContent(start, end);
    }
  });

  document.addEventListener("click", function (event) {
    if (!contextMenu.contains(event.target)) {
      hideContextMenu();
    }
  });
  document.addEventListener("scroll", hideContextMenu, true);
})();
