# Favicon, title, and head

Every page this skill produces ships a real favicon, a real title, and a complete head block. A default favicon and a title reading `Home` are the two cheapest signals that something is unfinished, and they are visible before the page even loads.

---

## 1. Designing the favicon mark

**Derive it from the signature element.** The favicon is the design compressed to 16 pixels. If the page has a signature device — a diagram, a typographic move, a material, a form — the favicon is its smallest possible statement.

**The tell to avoid:** the brand's first letter, white, in a rounded square, on a purple-blue gradient. This is the single most recognizable AI-generated favicon. A letterform can work, but it has to be a *specific* letterform — a real cut of type, drawn as a path, at a size and weight chosen for 16px — not a system font centered in a box.

### What survives at 16px

The favicon is designed at 16px and drawn at 512. Everything below follows from that.

| Rule | Why |
|---|---|
| One shape, or two at most | Three shapes become mud |
| Stroke width ≥ 8% of the viewBox (≥40 units at 512) | Thinner strokes vanish |
| No text beyond two characters | Three letters are unreadable |
| No gradients with low internal contrast | They flatten to a single blur |
| No fine detail below ~24 units at 512 | It disappears |
| Silhouette must read with fills removed | If the outline is unrecognizable, the mark is too complex |
| Contrast ≥ 3:1 against both white and dark browser chrome | Tabs have two backgrounds |

**Test it.** Render at 16px and look. If it needs squinting, simplify. Repeat until it doesn't.

### Sources for a mark

Take the characteristic form from the subject's world: an instrument's dial, a tool's profile, a material's cross-section, a diagram's core relationship, a species' silhouette, a notation glyph, an aperture, a joint, a wave, a route. Almost anything beats a letter in a box.

### The three variants

1. **`favicon.svg`** — the primary, with an embedded `prefers-color-scheme: dark` media query so it adapts to browser chrome without a second file.
2. **`icon-mono.svg`** — single-path, `fill="currentColor"`, for Safari pinned tabs and any monochrome context.
3. **`icon-maskable.png`** — Android adaptive icons crop to a circle. All meaningful content must sit inside the centered 80% safe zone; the outer 10% on each side gets cut.

### Dark-mode SVG pattern

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <style>
    :root { --bg: #0B4F6C; --fg: #FDFCFA; }
    @media (prefers-color-scheme: dark) {
      :root { --bg: #FDFCFA; --fg: #0B4F6C; }
    }
  </style>
  <rect width="512" height="512" rx="96" fill="var(--bg)"/>
  <path d="..." fill="var(--fg)"/>
</svg>
```

Keep the SVG under ~2KB. Inline the styles; no external references, no embedded rasters.

---

## 2. Generating the files

```bash
python3 scripts/favicon.py --svg mark.svg --name "Product Name" \
  --theme "#0B4F6C" --background "#FDFCFA" --out ./public
```

Emits `favicon.svg`, `icon-mono.svg`, `site.webmanifest`, and `head-snippet.html`. It rasterizes PNGs when `cairosvg` or `rsvg-convert` is present and prints the exact fallback command when neither is.

`--check` renders a 16px ASCII preview so you can see whether the mark survives before shipping it.

---

## 3. Page titles

The title is read in a tab strip 12 characters wide, in search results, and aloud by screen readers. Write it for all three.

**Pattern:** `Specific thing — Brand`, em dash, brand last, under 60 characters.

**Front-load the distinctive word.** Tabs truncate from the right, so the first two or three words are all most users ever see.

| Page | Title |
|---|---|
| Home | `Ashfield — Field notes for working botanists` |
| Product | `Specimen log — Ashfield` |
| Article | `Why herbarium sheets outlast databases — Ashfield` |
| Dashboard | `Collections · Ashfield` |
| Error | `Page not found — Ashfield` |

Avoid: `Home | Brand` · the brand name alone · `Welcome to Brand` · keyword stuffing · title-cased sentences.

For app screens with state, put the state first: `(3) Inbox — Ashfield`. For long-running operations, reflect progress: `Uploading 40% — Ashfield`.

---

## 4. The head block

```html
<!-- Identity -->
<title>Specimen log — Ashfield</title>
<meta name="description" content="Under 155 characters. Say what the page is
      and why someone would open it. This is ad copy, not a summary — it is
      often the only thing a searcher reads.">
<link rel="canonical" href="https://example.com/specimen-log">

<!-- Icons -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="mask-icon" href="/icon-mono.svg" color="#0B4F6C">
<link rel="manifest" href="/site.webmanifest">

<!-- Theme -->
<meta name="theme-color" content="#FDFCFA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0B1512" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">

<!-- Social -->
<meta property="og:type" content="website">
<meta property="og:title" content="Specimen log — Ashfield">
<meta property="og:description" content="…">
<meta property="og:image" content="https://example.com/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://example.com/specimen-log">
<meta name="twitter:card" content="summary_large_image">

<!-- Viewport — note: no user-scalable=no -->
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

`viewport-fit=cover` is required for `env(safe-area-inset-*)` to do anything.

### The OG image

1200×630. Design it — do not screenshot the hero. It renders at roughly 300px wide in most feeds, so type must be large and the composition simple. Include the product name; assume no other context reaches the viewer. A missing OG image renders every share as a gray rectangle, which is a real distribution cost.

---

## 5. Technical SEO that is also good UI

These overlap almost entirely with accessibility and structure, which is why they belong here rather than in a separate concern.

- **One `<h1>` per page**, and it says what the page is. Heading levels descend without skipping.
- **Descriptive link text.** "Read the methodology" beats "click here" for both crawlers and screen readers.
- **Real `alt` text.** Describe function, not appearance: `alt="Pressed fern specimen mounted on herbarium sheet"`, not `alt="image"`.
- **Semantic landmarks:** `<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`.
- **Clean URLs:** lowercase, hyphenated, no query strings for canonical content.
- **JSON-LD** for content with a real schema type — `Article`, `Product`, `Organization`, `BreadcrumbList`, `FAQPage`. Only where the type genuinely applies; invented structured data is a liability.
- **`sitemap.xml` and `robots.txt`**, both actually correct.
- **Core Web Vitals are UX metrics.** LCP under 2.5s, CLS under 0.1, INP under 200ms. The image-dimensions and font-loading rules in `interface-guidelines.md` §5 are what move them.
- **Server-render meaningful content.** A page that is an empty div until hydration is invisible to crawlers and slow for users.

For content strategy, keyword research, and off-page work, that is a separate discipline — this skill covers the parts that live in the markup.
