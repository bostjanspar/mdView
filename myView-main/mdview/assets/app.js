(function () {
  "use strict";

  const openFolderBtn = document.getElementById("open-folder-btn");
  const treePaneToggleBtn = document.getElementById("tree-pane-toggle-btn");
  const flipPanesBtn = document.getElementById("flip-panes-btn");
  const treePane = document.getElementById("tree-pane");
  const contentArea = document.getElementById("content-area");
  const rawView = document.getElementById("raw-view");
  const renderedView = document.getElementById("rendered-view");
  const emptyState = document.getElementById("empty-state");
  const viewModeInputs = document.querySelectorAll(".view-mode-input");
  const fontInputs = document.querySelectorAll(".font-choice-input");
  const FONT_STACKS = {
    "jetbrains-mono": '"JetBrains Mono", "Cascadia Mono"',
    "cascadia-mono": '"Cascadia Mono", "JetBrains Mono"',
    "system-mono": ""
  };

  let currentFileContent = null;
  let currentMode = "raw";
  let currentFont = "jetbrains-mono";
  let panesFlipped = false;

  function api() {
    return window.pywebview.api;
  }

  function setActiveMode(mode) {
    viewModeInputs.forEach(function (input) {
      input.checked = input.value === mode;
    });
  }

  function setActiveFont(font) {
    fontInputs.forEach(function (input) {
      input.checked = input.value === font;
    });
  }

  function applyFontVar(font) {
    document.documentElement.style.setProperty(
      "--font-family-mono",
      FONT_STACKS.hasOwnProperty(font) ? FONT_STACKS[font] : FONT_STACKS["jetbrains-mono"]
    );
  }

  function switchToFont(font) {
    api()
      .set_font(font)
      .then(function () {
        currentFont = font;
        applyFontVar(font);
        setActiveFont(font);
      });
  }

  function renderRaw(lines) {
    rawView.innerHTML = "";
    lines.forEach(function (text, index) {
      const line = document.createElement("div");
      line.className = "raw-line";

      const number = document.createElement("span");
      number.className = "raw-line-number";
      number.textContent = String(index + 1);

      const content = document.createElement("span");
      content.className = "raw-line-text";
      content.textContent = text;

      line.appendChild(number);
      line.appendChild(content);
      rawView.appendChild(line);
    });
  }

  function renderRendered(html) {
    renderedView.innerHTML = html;
  }

  function showView() {
    contentArea.classList.toggle("both-mode", currentMode === "both");
    contentArea.classList.toggle("flipped", panesFlipped);
    flipPanesBtn.hidden = currentMode !== "both";
    if (currentFileContent === null) {
      emptyState.hidden = false;
      rawView.hidden = true;
      renderedView.hidden = true;
      return;
    }
    emptyState.hidden = true;
    rawView.hidden = currentMode === "rendered";
    renderedView.hidden = currentMode === "raw";
  }

  function topmostRawLine() {
    const children = rawView.children;
    for (let i = 0; i < children.length; i++) {
      if (children[i].offsetTop >= rawView.scrollTop) {
        return i + 1;
      }
    }
    return children.length;
  }

  function topmostRenderedLine() {
    const elements = renderedView.querySelectorAll("[data-line]");
    for (let i = 0; i < elements.length; i++) {
      if (elements[i].offsetTop >= renderedView.scrollTop) {
        return Number(elements[i].dataset.line.split("-")[0]);
      }
    }
    return null;
  }

  function captureScrollPosition() {
    if (currentFileContent === null) {
      return null;
    }
    if (currentMode === "raw") {
      return { mode: "raw", line: topmostRawLine() };
    }
    if (currentMode === "rendered") {
      return { mode: "rendered", line: topmostRenderedLine() };
    }
    return null;
  }

  function restoreScrollPosition(position, totalLines) {
    if (!position) {
      return;
    }
    if (position.mode === "raw") {
      const line = Math.min(position.line, Math.max(totalLines, 1));
      const target = rawView.children[line - 1];
      if (target) {
        rawView.scrollTop = target.offsetTop;
      }
      return;
    }
    if (position.mode === "rendered") {
      const elements = Array.from(renderedView.querySelectorAll("[data-line]"));
      let target = null;
      for (const el of elements) {
        const start = Number(el.dataset.line.split("-")[0]);
        if (start >= position.line) {
          target = el;
          break;
        }
      }
      if (!target && elements.length > 0) {
        target = elements[elements.length - 1];
      }
      if (target) {
        renderedView.scrollTop = target.offsetTop;
      }
    }
  }

  function applyLoadedFile(fileContent, path) {
    if (fileContent.error) {
      currentFileContent = null;
      emptyState.textContent = fileContent.error;
      showView();
      return;
    }
    emptyState.textContent = "No file open.";
    currentFileContent = fileContent;
    renderRaw(fileContent.lines);
    renderRendered(fileContent.rendered_html);
    showView();
    if (window.mdviewTree) {
      window.mdviewTree.applySelection(fileContent.expanded, path);
    }
    if (currentMode === "both" && window.mdviewSync) {
      window.mdviewSync.realign();
    }
  }

  function switchToMode(mode) {
    api()
      .set_view_mode(mode)
      .then(function () {
        currentMode = mode;
        setActiveMode(mode);
        showView();
        if (window.mdviewSync) {
          if (currentMode === "both") {
            window.mdviewSync.attach();
            window.mdviewSync.realign();
          } else {
            window.mdviewSync.detach();
          }
        }
      });
  }

  function isTextInputFocused() {
    const el = document.activeElement;
    if (!el) {
      return false;
    }
    return el.tagName === "INPUT" || el.tagName === "TEXTAREA" || el.isContentEditable;
  }

  openFolderBtn.addEventListener("click", function () {
    api()
      .open_folder()
      .then(function (session) {
        if (session.root) {
          emptyState.textContent = "No file open.";
        }
      });
  });

  viewModeInputs.forEach(function (input) {
    input.addEventListener("change", function () {
      if (input.checked) {
        switchToMode(input.value);
      }
    });
  });

  setActiveFont(currentFont);

  window.addEventListener("pywebviewready", function () {
    api()
      .get_font()
      .then(function (font) {
        currentFont = font;
        applyFontVar(font);
        setActiveFont(font);
      });
  });

  fontInputs.forEach(function (input) {
    input.addEventListener("change", function () {
      if (input.checked) {
        switchToFont(input.value);
      }
    });
  });

  treePaneToggleBtn.addEventListener("click", function () {
    const nowHidden = !treePane.hidden;
    treePane.hidden = nowHidden;
    treePaneToggleBtn.setAttribute("aria-pressed", String(!nowHidden));
  });

  flipPanesBtn.addEventListener("click", function () {
    panesFlipped = !panesFlipped;
    contentArea.classList.toggle("flipped", panesFlipped);
  });

  const SHORTCUT_MODES = { "1": "raw", "2": "rendered", "3": "both" };

  document.addEventListener("keydown", function (event) {
    if (event.key === "F11") {
      event.preventDefault();
      window.pywebview.api.toggle_fullscreen();
      return;
    }
    if (!event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }
    const mode = SHORTCUT_MODES[event.key];
    if (!mode || isTextInputFocused()) {
      return;
    }
    event.preventDefault();
    switchToMode(mode);
  });

  window.mdview = {
    applyLoadedFile: applyLoadedFile,
    topmostRawLine: topmostRawLine,
    topmostRenderedLine: topmostRenderedLine,
    onFileReloaded: function (fileContent) {
      if (fileContent.error) {
        currentFileContent = null;
        emptyState.textContent = fileContent.error;
        showView();
        return;
      }
      const position = captureScrollPosition();
      currentFileContent = fileContent;
      renderRaw(fileContent.lines);
      renderRendered(fileContent.rendered_html);
      showView();
      restoreScrollPosition(position, fileContent.lines.length);
      if (currentMode === "both" && window.mdviewSync) {
        window.mdviewSync.realign();
      }
    },
    onFileDeleted: function () {
      currentFileContent = null;
      emptyState.textContent = "File no longer available.";
      showView();
    },
    onTreeReady: function (payload) {
      if (window.mdviewTree) {
        window.mdviewTree.render(payload);
      }
    },
  };
})();
