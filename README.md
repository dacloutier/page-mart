# Page Mart

A single static HTML page bookmark manager with tabbed organization, custom styling, and local storage persistence.

## Installation Instructions
Download the minified version called page-mart.html locally, open it in your favourite browser.

---

## Overview

page-mart is a self-contained, offline-first bookmark manager that runs entirely in the browser. No server, no dependencies fetched at runtime — React and all libraries are stored locally. All user data is persisted in `localStorage` as JSON.

---

## Tech Stack

- **Single static `index.html`** — no build step, no server required
- **React** (locally stored, e.g. `react.development.js` + `react-dom.development.js`)
- **Babel standalone** (for JSX in-browser transpilation, locally stored)
- **localStorage** for persistence
- No backend, no network calls

---

## Data Model

```json
{
  "tabs": [
    {
      "id": "uuid",
      "name": "Work",
      "color": "#4A90D9",
      "order": 0,
      "boxes": [
        {
          "id": "uuid",
          "name": "Dev Tools",
          "color": "#F5A623",
          "order": 0,
          "links": [
            {
              "id": "uuid",
              "label": "GitHub",
              "url": "https://github.com",
              "icon": "https://github.com/favicon.ico",
              "order": 0
            }
          ]
        }
      ]
    }
  ]
}
```

### Notes
- All entities have a stable `id` (UUID) and an `order` field for user-defined ordering.
- Icons are stored as URLs (favicon URLs by default, user-editable).
- Colors are stored as hex strings.

---

## Features

### Tabs
- 1..n tabs displayed as a top navigation bar
- Each tab has: name, color (color picker), order
- Add / rename / recolor / reorder / delete tabs

### Boxes
- Each tab contains 1..n boxes displayed in a grid/flow layout
- Each box has: name, color (color picker), order
- Add / rename / recolor / reorder / delete boxes within a tab

### Links
- Each box contains 0..n links
- Each link has: label, URL, icon (auto-fetched favicon or custom URL), order
- Add / edit / reorder / delete links within a box
- Clicking a link opens it in a new tab

### UI Interactions
- Inline editing for names and labels (click to edit)
- Color pickers for tab and box colors
- Drag-to-reorder for tabs, boxes, and links (or up/down buttons as fallback)
- All mutations are immediately persisted to localStorage

---

## Settings Popup

Accessible via a gear icon (fixed position).

### Export
- Serialize current state to JSON
- Copy JSON to clipboard with one click

### Import
- Text area where user can paste previously exported JSON
- "Load" button validates and replaces current state
- Warns user that this will overwrite existing data

---

## File Structure

```
page-mart/
├── index.html          # The entire app
├── README.md
└── lib/
    ├── react.development.js
    ├── react-dom.development.js
    └── babel.min.js
```

---

## UX / Design Notes

- Clean, minimal UI — focus on usability over decoration
- Tab bar at the top; active tab is highlighted
- Boxes are displayed as cards in a responsive grid
- Links are listed inside each box with icon + label
- Color choices should inform background or border of tab/box headers
- Settings gear icon fixed to bottom-right corner
- All dialogs/popups are modals (no page navigation)

---

## Constraints & Decisions

- **No build step** — must work by opening `index.html` directly in a browser
- **No CDN dependencies** — all JS libs stored locally under `lib/`
- **No backend** — 100% client-side
- **Single file app logic** — all app code lives in `index.html` (or a single `app.js` loaded from it)
- Data survives page refresh via localStorage; export/import provides portability

---

## Out of Scope (v1)

- Sync across devices
- User accounts / auth

---

## Stretch Goals

- **Drag-to-reorder** for tabs, boxes, and links
- **Truly self-contained single file** — minify and inline all JS libs (React, ReactDOM, Babel) directly into `index.html` as `<script>` blocks, eliminating the `lib/` folder entirely. The result is one file you can copy anywhere and open in a browser.

---

## Part 2 

A new version built on top of v1 .

### Requirement 1 — Drag-to-reorder (full)

- Tabs, boxes, and links are all drag-and-drop reorderable.
- **Cross-container moves supported:**
  - Links can be dragged between boxes.
  - Boxes can be dragged between tabs (drag box header onto a tab in the tab bar to move it there).

### Requirement 2 — Resizable boxes

- Each box is user-resizable (width and height).
- Dimensions (`width`, `height`) are stored per box in the localStorage data structure.
- Resizing a box pushes/reflows surrounding boxes (standard flex/grid reflow).
- Default size is the same as v1 (260px wide); user resize overrides it.

### Requirement 3 — Link hover preview + inline viewer

- **Hover** over a link shows a tooltip-style iframe preview of the page (after a short delay).
- **Middle-click** on a link opens an inline preview panel (iframe) anchored to the top-right corner of the viewport.
  - Panel has two buttons:
    - **×** — close the preview panel.
    - **[]** — open the previewed URL in a new browser tab.
- Only one inline preview panel is open at a time.
