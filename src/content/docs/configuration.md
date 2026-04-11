---
title: Configuration
description: mkdocx.config.js full reference.
order: 2
---

mkdocx reads a single config file: `mkdocx.config.js` at your project root.

## Basic structure

```javascript
/** @type {import('./src/types').MkdocxConfig} */
export default {
  name: 'Your Project',
  description: 'Short description for metadata.',
  nav: [
    { label: 'docs',    href: '/docs/getting-started' },
    { label: 'writing', href: '/writing' },
  ],
  footer: [
    { label: 'GitHub', href: 'https://github.com/your/repo' },
  ],
}
```

## Options

### `name`

Project name. Used in page titles, the nav header, and metadata.

```javascript
name: 'mkdocx'
```

### `description`

Short description. Appears in site metadata and the homepage.

```javascript
description: 'Minimal markdown documentation builder.'
```

### `nav`

Top navigation links. Array of `{ label, href }` objects. Internal and external links both work. Omit to show only the site name.

```javascript
nav: [
  { label: 'docs',    href: '/docs/getting-started' },
  { label: 'writing', href: '/writing' },
  { label: 'github',  href: 'https://github.com' },
]
```

### `footer`

Footer links. Same structure as `nav`.

```javascript
footer: [
  { label: 'GitHub',  href: 'https://github.com' },
  { label: 'License', href: '/license' },
  { label: 'Contact', href: 'mailto:hello@example.com' },
]
```

### `siteUrl`

Canonical URL for sitemaps and social metadata.

```javascript
siteUrl: 'https://your-docs.com'
```

### `dateFormat`

Controls how dates appear on writing posts. Accepts `Intl.DateTimeFormat` options.

```javascript
dateFormat: { year: 'numeric', month: 'short', day: 'numeric' }
// renders: "Apr 10, 2026"
```

```javascript
dateFormat: { year: 'numeric', month: '2-digit', day: '2-digit' }
// renders: "04/10/2026"
```

Default: `{ year: 'numeric', month: 'short', day: 'numeric' }`.

### `dateLocale`

BCP 47 locale string for date formatting. Pairs with `dateFormat`.

```javascript
dateLocale: 'en-US'   // "Apr 10, 2026"
dateLocale: 'fr-FR'   // "10 avr. 2026"
dateLocale: 'ja-JP'   // "2026年4月10日"
```

Default: `'en-US'`.

## Astro config

`astro.config.mjs` controls build behavior. The two files work together — `mkdocx.config.js` is for site content, `astro.config.mjs` is for build tooling.

```javascript
export default defineConfig({
  site: 'https://your-docs.com',
  integrations: [mdx(), sitemap()],
  markdown: { syntaxHighlight: false },
})
```

See the [Astro docs](https://docs.astro.build) for all available options.
