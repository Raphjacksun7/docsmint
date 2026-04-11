---
title: Reference
description: CLI commands, config schema, frontmatter fields, and component API.
order: 6
---

## CLI

### Node.js

```bash
pnpm dev              # dev server at http://localhost:4321
pnpm build            # production build → dist/
pnpm preview          # preview build at http://localhost:3000
```

Options for `dev`: `--port <n>`, `--host` (expose on network).

### Python

```bash
mkdocx dev [--port <n>]   # dev server
mkdocx build              # production build → dist/
mkdocx preview            # preview build locally
mkdocx deploy <bucket>    # build + sync to GCS bucket
```

The CLI walks up from the current directory to find `mkdocx.config.js`.

## Config schema

```typescript
interface MkdocxConfig {
  name: string
  description: string
  nav?: { label: string; href: string }[]
  footer?: { label: string; href: string }[]
  siteUrl?: string
  dateFormat?: Intl.DateTimeFormatOptions
  dateLocale?: string
}
```

All fields except `name` and `description` are optional.

## Frontmatter

**Docs:**

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `title` | string | yes | Page heading and browser title |
| `description` | string | no | Meta description |
| `order` | number | no | Sidebar sort position. Lower = first. Default: 99 |

**Writing:**

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `title` | string | yes | Post heading and browser title |
| `date` | string (YYYY-MM-DD) | yes | Publication date. Determines sort order |
| `description` | string | no | Meta description |
| `author` | string | no | Author name |

## Component API

### `<Callout type?>`

| Prop | Type | Default |
|------|------|---------|
| `type` | `"note" \| "warning" \| "tip"` | `"note"` |

### `<Tooltip tip>`

| Prop | Type | Required |
|------|------|----------|
| `tip` | string | yes |

### `<FileTree>`

No props. Slot content is a markdown list. Two spaces per indent level. Wrap filenames in `**` to highlight.

Directories (items with nested children) are collapsible on click.

### `<Tabs labels>`

| Prop | Type | Required |
|------|------|----------|
| `labels` | `string[]` | yes |

`labels` must have the same length as the number of `<Tab>` children.

### `<Tab>`

No props. Slot wrapper for a single tab panel. Must be a direct child of `<Tabs>`.

### `<Image src alt ...>`

| Prop | Type | Required |
|------|------|----------|
| `src` | `string \| ImageMetadata` | yes |
| `alt` | string | yes |
| `width` | number | no |
| `height` | number | no |
| `caption` | string | no |

Local images (from `src/assets/`) are optimized at build time. Remote and public images are served as-is with lazy loading.

## Build output

```
dist/
├── index.html
├── docs/
│   └── getting-started/
│       └── index.html
├── writing/
│   └── hello-world/
│       └── index.html
├── _astro/          ← CSS + JS bundles (content-hashed)
├── sitemap.xml
└── pagefind/        ← full-text search index
```

## Performance

Static HTML served over a global CDN. No server-side rendering.

- Lighthouse: 95+
- FCP: < 500ms
- Total JS: < 50KB
