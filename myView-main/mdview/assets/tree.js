(function () {
  "use strict";

  const treeRoot = document.getElementById("tree-root");
  const treeEmptyState = document.getElementById("tree-empty-state");

  let lastTree = null;
  let expandedPaths = new Set();
  let selectedPath = null;

  function api() {
    return window.pywebview.api;
  }

  function buildNode(node) {
    const li = document.createElement("li");
    li.className = "tree-node " + (node.is_dir ? "tree-dir" : "tree-file");
    li.dataset.path = node.path;

    const row = document.createElement("div");
    row.className = "tree-row";
    if (node.path === selectedPath) {
      row.classList.add("selected");
    }

    const toggle = document.createElement("span");
    toggle.className = "tree-toggle";
    if (node.is_dir) {
      toggle.textContent = expandedPaths.has(node.path) ? "▾" : "▸";
    }
    row.appendChild(toggle);

    const label = document.createElement("span");
    label.className = "tree-label";
    label.textContent = node.name;
    row.appendChild(label);

    li.appendChild(row);

    if (node.is_dir) {
      const childList = document.createElement("ul");
      childList.className = "tree-children";
      childList.hidden = !expandedPaths.has(node.path);
      (node.children || []).forEach(function (child) {
        childList.appendChild(buildNode(child));
      });
      li.appendChild(childList);

      row.addEventListener("click", function () {
        toggleDirectory(node.path, li, toggle, childList);
      });
    } else {
      row.addEventListener("click", function () {
        selectFile(node.path);
      });
    }

    return li;
  }

  function toggleDirectory(path, _li, toggle, childList) {
    const nowExpanded = childList.hidden;
    childList.hidden = !nowExpanded;
    toggle.textContent = nowExpanded ? "▾" : "▸";
    if (nowExpanded) {
      expandedPaths.add(path);
    } else {
      expandedPaths.delete(path);
    }
    api().toggle_expanded(path);
  }

  function selectFile(path) {
    api()
      .load_file(path)
      .then(function (fileContent) {
        window.mdview.applyLoadedFile(fileContent, path);
      });
  }

  function rebuild() {
    treeRoot.innerHTML = "";
    const children = (lastTree && lastTree.children) || [];
    if (children.length === 0) {
      treeEmptyState.textContent = lastTree ? "No markdown files found." : "No folder open.";
      treeEmptyState.hidden = false;
      treeRoot.hidden = true;
      return;
    }
    treeEmptyState.hidden = true;
    treeRoot.hidden = false;
    children.forEach(function (child) {
      treeRoot.appendChild(buildNode(child));
    });
  }

  function render(payload) {
    lastTree = payload.tree;
    expandedPaths = new Set(payload.expanded || []);
    selectedPath = payload.open_file || null;
    rebuild();
  }

  function applySelection(expandedList, selected) {
    expandedPaths = new Set(expandedList || []);
    selectedPath = selected || null;
    rebuild();
  }

  window.mdviewTree = {
    render: render,
    applySelection: applySelection,
  };
})();
