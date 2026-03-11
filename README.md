# Page Mart

A single static HTML page bookmark manager with tabbed organization, custom styling, and local storage persistence.

## Installation

Download `page-mart.html` locally and open it in your browser. No server, no install.

---

## Overview

page-mart is a self-contained, offline-first bookmark manager that runs entirely in the browser. No server, no dependencies fetched at runtime — React and all libraries are inlined. All user data is persisted in `localStorage` as JSON.

---

## Tech Stack

- **Single static `page-mart.html`** — no build step, no server required
- **React** (inlined, production build)
- **Babel standalone** (inlined, for JSX in-browser transpilation)
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
          "col": 0,
          "width": 260,
          "height": null,
          "links": [
            {
              "id": "uuid",
              "label": "GitHub",
              "url": "https://github.com",
              "icon": "https://github.com/favicon.ico",
              "order": 0
            }
          ],
          "boxes": [
            {
              "id": "uuid",
              "name": "Sub-box",
              "color": "#7B68EE",
              "order": 0,
              "minimized": false,
              "links": [],
              "boxes": []
            }
          ]
        }
      ]
    }
  ]
}
```

### Field reference

| Entity | Field | Description |
|--------|-------|-------------|
| Tab | `id` | Stable UUID |
| | `name` | Display name |
| | `color` | Hex color string |
| | `order` | Position in tab bar |
| | `boxes` | Array of top-level boxes |
| Box | `id` | Stable UUID |
| | `name` | Display name |
| | `color` | Hex color string |
| | `order` | Position within its column |
| | `col` | Column index (0-based) within the tab |
| | `width` | Width in px (default 260); shared across all boxes in a column |
| | `height` | Height in px, or `null` for auto |
| | `links` | Array of link objects |
| | `boxes` | Array of nested sub-box objects |
| Sub-box | Same as Box minus `col`, `width`, `height` | |
| | `minimized` | Whether the sub-box is collapsed |
| Link | `id` | Stable UUID |
| | `label` | Display name |
| | `url` | Destination URL |
| | `icon` | Favicon URL (auto-fetched or custom) |
| | `order` | Position within its box |

---

## Features

### Tabs
- Multiple tabs displayed as a top navigation bar
- Each tab has: name, color (color picker), order
- Add / rename / recolor / reorder / delete tabs

### Boxes
- Each tab contains boxes organized in resizable columns
- Each box has: name, color, order, column assignment, width, height
- Add / rename / recolor / reorder / delete boxes
- Drag to reorder within a column or move to another column
- Drag a box header onto a tab to move it to that tab
- Resize width and height via the bottom-right drag handle
- All boxes in the same column share the same width

### Sub-boxes
- Each box can contain nested sub-boxes in a tray at the bottom
- Sub-boxes support: name, color, minimize/expand, links, drag-to-reorder
- Sub-boxes can be dragged out to become top-level boxes (adopts column width)
- Top-level boxes can be dragged onto another box to nest them

### Links
- Each box (or sub-box) contains links
- Each link has: label, URL, icon (auto-fetched favicon or custom URL), order
- Add / edit / reorder / delete links
- Clicking a link opens it in a new tab

### UI Interactions
- Inline editing for names and labels (click to edit)
- Color pickers for tab and box colors
- Drag-to-reorder for tabs, boxes, sub-boxes, and links
- Links can be dragged between boxes
- Boxes can be dragged between columns and tabs
- All mutations are immediately persisted to localStorage

---

## Settings Popup

Accessible via a gear icon (fixed position).

### Export
- Serialize current state to JSON
- Copy JSON to clipboard with one click

### Import
- Paste previously exported JSON
- "Load" button validates and replaces current state
- Warns user that this will overwrite existing data

---

## File Structure

```
page-mart/
├── index.html          # Development version (loads libs from lib/)
├── page-mart.html      # Self-contained distributable (all libs inlined)
├── build.py            # Build script — generates page-mart.html from index.html
├── README.md
└── lib/
    ├── react.development.js
    ├── react.production.min.js
    ├── react-dom.development.js
    ├── react-dom.production.min.js
    └── babel.min.js
```

---

## Build

To regenerate `page-mart.html` after editing `index.html`:

```bash
python3 build.py
```

This script:
1. Reads `index.html`
2. Replaces the `lib/` script tags with inlined production-minified builds of React, ReactDOM, and Babel
3. Minifies the CSS and collapses HTML whitespace
4. Writes the result to `page-mart.html`

No dependencies required beyond Python 3 (stdlib only).

---

## UX / Design Notes

- Clean, minimal UI — focus on usability over decoration
- Tab bar at the top; active tab is highlighted
- Boxes are displayed as cards in a multi-column layout
- Links are listed inside each box with icon + label
- Box/sub-box actions (add link, add sub-box, delete) appear on header hover
- Settings gear icon fixed to bottom-right corner
- All dialogs/popups are modals (no page navigation)

---

## Constraints & Decisions

- **No build step** — `index.html` works by opening directly in a browser (dev mode)
- **No CDN dependencies** — all JS libs stored locally under `lib/`
- **No backend** — 100% client-side
- **Single file distribution** — `page-mart.html` is fully self-contained
- Data survives page refresh via localStorage; export/import provides portability

---

## Out of Scope

- Sync across devices
- User accounts / auth
