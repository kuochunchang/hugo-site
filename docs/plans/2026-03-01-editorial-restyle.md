# Editorial Restyle Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restyle the Hugo PaperMod site to match the warm editorial aesthetic of daily-news-report — warm beige palette, Newsreader/Outfit fonts, rust accent, light-only mode.

**Architecture:** Override PaperMod via Hugo's standard extension points: `assets/css/extended/` for CSS overrides and `layouts/partials/extend_head.html` for Google Fonts injection. Config changes in `hugo.toml` to disable dark mode toggle.

**Tech Stack:** Hugo, PaperMod theme, CSS custom properties, Google Fonts

---

### Task 1: Disable dark mode and configure light-only theme

**Files:**
- Modify: `hugo.toml`

**Step 1: Add disableThemeToggle and force light theme**

In `hugo.toml`, under `[params]`, add:

```toml
disableThemeToggle = true
defaultTheme = "light"
```

(Change `defaultTheme` from `"auto"` to `"light"`)

**Step 2: Verify config**

Run: `cat hugo.toml`
Expected: `disableThemeToggle = true` and `defaultTheme = "light"` present under `[params]`

**Step 3: Commit**

```bash
git add hugo.toml
git commit -m "style: disable dark mode, force light theme"
```

---

### Task 2: Add Google Fonts via extend_head partial

**Files:**
- Create: `layouts/partials/extend_head.html`

**Step 1: Create the extend_head partial**

Create `layouts/partials/extend_head.html` with:

```html
<!-- Google Fonts: Newsreader (headings) + Outfit (body) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
```

**Step 2: Verify file exists at correct path**

Run: `cat layouts/partials/extend_head.html`
Expected: Google Fonts link tags present

**Step 3: Commit**

```bash
git add layouts/partials/extend_head.html
git commit -m "style: add Google Fonts (Newsreader + Outfit)"
```

---

### Task 3: Override CSS variables — color palette and fonts

**Files:**
- Create: `assets/css/extended/editorial-theme.css`

**Step 1: Create the CSS override file**

Create `assets/css/extended/editorial-theme.css` with the following content. This is the core of the restyle — it overrides PaperMod's CSS variables to use the daily-news-report palette and fonts:

```css
/* ═══════════════════════════════════════════════════════
   Editorial Theme Override for PaperMod
   Matches daily-news-report warm editorial aesthetic
   ═══════════════════════════════════════════════════════ */

/* — Custom properties for editorial colors — */
:root {
    --color-link: #BB4A28;
    --color-link-hover: #943A20;
    --color-accent-bg: #FFF7ED;
    --color-quote-bg: #FFFBF5;
    --color-surface-warm: #FEFCF9;
    --color-text-muted: #9C9590;
    --color-border-light: #F0EBE4;

    --font-heading: "Newsreader", Georgia, "PingFang TC", "Microsoft JhengHei",
        "Noto Serif CJK TC", serif;
    --font-body: "Outfit", -apple-system, BlinkMacSystemFont, "PingFang TC",
        "Microsoft JhengHei", "Noto Sans CJK TC", sans-serif;

    --shadow-card: 0 1px 3px rgba(28,25,23,0.04), 0 4px 12px rgba(28,25,23,0.03);
    --shadow-hover: 0 2px 8px rgba(28,25,23,0.08), 0 8px 24px rgba(28,25,23,0.05);
}

/* — Override PaperMod theme variables — */
:root {
    --gap: 24px;
    --content-gap: 20px;
    --nav-width: 1024px;
    --main-width: 768px;
    --header-height: 60px;
    --footer-height: 60px;
    --radius: 8px;

    /* Warm editorial palette */
    --theme: #F8F5F0;
    --entry: #FFFFFF;
    --primary: #1A1A1A;
    --secondary: #6B6460;
    --tertiary: #E8E2DB;
    --content: #2A2724;
    --code-block-bg: #2A2724;
    --code-bg: #F0EDE8;
    --border: #E8E2DB;
    color-scheme: light;
}

/* Force dark theme to same warm light values (disable dark) */
:root[data-theme="dark"] {
    --theme: #F8F5F0;
    --entry: #FFFFFF;
    --primary: #1A1A1A;
    --secondary: #6B6460;
    --tertiary: #E8E2DB;
    --content: #2A2724;
    --code-block-bg: #2A2724;
    --code-bg: #F0EDE8;
    --border: #E8E2DB;
    color-scheme: light;
}

[data-theme="dark"] .list {
    background: var(--theme);
}

/* ═══ Global typography ═══ */
body {
    font-family: var(--font-body);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}

/* ═══ Header / Navigation ═══ */
.nav {
    line-height: var(--header-height);
}

.logo a {
    font-family: var(--font-heading);
    font-weight: 600;
    letter-spacing: -0.02em;
}

#menu a {
    font-family: var(--font-body);
    font-weight: 500;
    font-size: 15px;
    letter-spacing: 0.01em;
    transition: color 0.15s ease;
}

#menu a:hover {
    color: var(--color-link);
}

#menu .active {
    color: var(--color-link);
    border-bottom-color: var(--color-link);
}

/* ═══ Home info section ═══ */
.home-info .entry-content {
    font-family: var(--font-body);
    color: var(--secondary);
    font-size: 15px;
    line-height: 1.6;
}

/* ═══ Post entry cards ═══ */
.post-entry {
    background: var(--entry);
    border: 1px solid var(--border);
    border-left: 3px solid var(--color-link);
    border-radius: var(--radius);
    box-shadow: var(--shadow-card);
    transition: box-shadow 0.25s ease, border-color 0.25s ease, transform 0.1s;
}

.post-entry:hover {
    box-shadow: var(--shadow-hover);
}

.first-entry {
    border-left: 3px solid var(--color-link);
    box-shadow: var(--shadow-card);
}

.first-entry:hover {
    box-shadow: var(--shadow-hover);
}

.entry-header h2 {
    font-family: var(--font-heading);
    font-weight: 600;
    letter-spacing: -0.015em;
    line-height: 1.3;
}

.first-entry .entry-header h1 {
    font-family: var(--font-heading);
    font-weight: 600;
    letter-spacing: -0.025em;
}

.entry-content {
    font-family: var(--font-body);
    color: var(--secondary);
    line-height: 1.625;
}

.entry-footer {
    color: var(--color-text-muted);
}

/* ═══ Post single — title & meta ═══ */
.post-title {
    font-family: var(--font-heading);
    font-weight: 600;
    letter-spacing: -0.025em;
    line-height: 1.2;
}

.post-meta {
    color: var(--color-text-muted);
    font-size: 0.875rem;
    letter-spacing: 0.02em;
}

.breadcrumbs {
    color: var(--color-text-muted);
}

.breadcrumbs a {
    color: var(--color-link);
}

/* ═══ Post content typography ═══ */
.post-content {
    font-family: var(--font-body);
    color: var(--content);
    line-height: 1.625;
    font-size: 16px;
}

.post-content h1,
.post-content h2,
.post-content h3,
.post-content h4,
.post-content h5,
.post-content h6 {
    font-family: var(--font-heading);
    font-weight: 600;
    letter-spacing: -0.015em;
}

.post-content h2 {
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--color-border-light);
}

/* Links in post content */
.post-content a {
    color: var(--color-link);
    box-shadow: none;
    text-decoration: none;
    transition: color 0.15s ease;
}

.post-content a:hover {
    color: var(--color-link-hover);
    text-decoration: underline;
    text-underline-offset: 2px;
    text-decoration-thickness: 1px;
}

/* Blockquotes */
.post-content blockquote {
    border-inline-start: 3px solid var(--color-link);
    background: var(--color-quote-bg);
    padding: 1rem 1.25rem;
    border-radius: 0 var(--radius) var(--radius) 0;
    color: var(--secondary);
    font-style: italic;
}

/* Horizontal rules */
.post-content hr {
    background: none;
    height: 0;
    margin: 2.5rem 0;
    border: none;
}

.post-content hr::after {
    content: "\00b7  \00b7  \00b7";
    display: block;
    text-align: center;
    color: var(--color-text-muted);
    font-size: 1rem;
    letter-spacing: 0.5em;
}

/* Tables */
.post-content table th {
    background: var(--theme);
    font-weight: 600;
    color: var(--color-text-muted);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.post-content table:not(.highlighttable, .highlight table, .gist .highlight) td {
    border-bottom-color: var(--color-border-light);
}

.post-content table:not(.highlighttable, .highlight table, .gist .highlight) tr:nth-child(even) td {
    background: var(--color-surface-warm);
}

.post-content table:not(.highlighttable, .highlight table, .gist .highlight) tbody tr:hover td {
    background: var(--color-accent-bg);
}

/* Inline code */
.post-content code {
    background: var(--code-bg);
    border-radius: 4px;
    font-size: 0.86em;
}

/* Code blocks */
.post-content pre code {
    background: var(--code-block-bg) !important;
    border-radius: var(--radius);
}

/* Lists */
.post-content li {
    margin-top: 6px;
    line-height: 1.625;
}

/* ═══ Tags ═══ */
.post-tags a {
    background: var(--color-accent-bg);
    border: 1px solid var(--color-border-light);
    color: var(--color-link);
    font-size: 13px;
    font-weight: 500;
    transition: all 0.15s ease;
}

.post-tags a:hover {
    background: var(--color-link);
    color: #FFFFFF;
    border-color: var(--color-link);
}

/* ═══ TOC ═══ */
.toc {
    border: 1px solid var(--color-border-light);
    background: var(--color-surface-warm);
}

[data-theme="dark"] .toc {
    background: var(--color-surface-warm);
}

.toc a:hover {
    color: var(--color-link);
    box-shadow: none;
    text-decoration: underline;
}

/* ═══ Pagination ═══ */
.pagination a {
    background: var(--color-link);
    color: #FFFFFF;
}

.pagination a:hover {
    opacity: 0.9;
}

.paginav a:hover {
    background: var(--color-accent-bg);
    color: var(--color-link);
}

/* ═══ Footer ═══ */
.footer {
    color: var(--color-text-muted);
    font-size: 0.75rem;
    letter-spacing: 0.02em;
}

.footer a {
    color: var(--color-link);
    border-bottom: none;
}

.footer a:hover {
    text-decoration: underline;
    text-underline-offset: 2px;
}

/* Scroll-to-top button */
.top-link {
    background: var(--color-link);
}

.top-link svg {
    color: #FFFFFF;
}

.top-link,
.top-link svg {
    filter: none;
}

/* ═══ Archive page ═══ */
.archive-year {
    font-family: var(--font-heading);
}

/* ═══ Search ═══ */
#searchResults .post-entry {
    border-left: 3px solid var(--color-link);
}

/* ═══ Page list background override ═══ */
.list {
    background: var(--theme);
}

/* ═══ Anchor links ═══ */
h1:hover .anchor,
h2:hover .anchor,
h3:hover .anchor,
h4:hover .anchor,
h5:hover .anchor,
h6:hover .anchor {
    color: var(--color-link);
}
```

**Step 2: Verify file exists**

Run: `ls -la assets/css/extended/editorial-theme.css`
Expected: File exists with non-zero size

**Step 3: Start Hugo dev server and visually verify**

Run: `hugo server`
Expected: Site renders with warm beige background, Newsreader headings, Outfit body text, rust accent color

**Step 4: Commit**

```bash
git add assets/css/extended/editorial-theme.css
git commit -m "style: add editorial theme CSS overrides

Warm beige palette, Newsreader headings, Outfit body,
rust accent color matching daily-news-report aesthetic"
```

---

### Task 4: Final visual verification

**Step 1: Run Hugo dev server**

Run: `hugo server`
Open `http://localhost:1313` in browser

**Step 2: Verify checklist**

- [ ] Background is warm beige (#F8F5F0), not white
- [ ] Headings use Newsreader serif font
- [ ] Body text uses Outfit sans-serif font
- [ ] Post cards have left rust border accent
- [ ] Links are rust colored (#BB4A28)
- [ ] No dark mode toggle button visible
- [ ] Tags have warm accent background
- [ ] Blockquotes have rust left border
- [ ] Code blocks have warm dark background
- [ ] Footer text is muted
- [ ] Navigation menu items have editorial styling
