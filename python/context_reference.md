# mkdocx framework reference

mkdocx is a minimal documentation builder. Users write markdown. mkdocx handles the rendering engine (Astro, Tailwind, Pagefind search, syntax highlighting). The pip package bundles the entire Astro template — users never touch it.

## Project structure

The only files that belong in the repo:

```
docs/
├── mkdocx.config.js          ← site config
└── src/
    └── content/
        ├── docs/
        │   └── *.md / *.mdx  ← documentation pages
        └── writing/
            └── *.md           ← blog posts / engineering notes (optional)
```

`docs/.mkdocx/` is generated automatically (gitignored). Never edit it.

## mkdocx.config.js — all options

```javascript
export default {
  // Required
  name: 'project-name',          // nav header + page titles
  description: 'short text',     // homepage + meta description

  // Navigation
  nav: [                         // top nav links
    { label: 'docs',    href: '/docs/getting-started' },
    { label: 'writing', href: '/writing' },
    { label: 'github',  href: 'https://github.com/...' },
  ],
  footer: [                      // footer links, same structure as nav
    { label: 'GitHub', href: 'https://github.com/...' },
  ],

  // Optional
  siteUrl: 'https://docs.example.com',  // canonical URL for sitemap
  dateLocale: 'en-US',                  // BCP 47 locale for writing dates
  dateFormat: {                         // Intl.DateTimeFormat options
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  },
  // dateFormat examples:
  // { year: 'numeric', month: 'short', day: 'numeric' }  → "Apr 11, 2026"
  // { year: 'numeric', month: '2-digit', day: '2-digit' } → "04/11/2026"
  // { year: 'numeric', month: 'long', day: 'numeric' }   → "April 11, 2026"
}
```

## Frontmatter

**Docs pages** (`src/content/docs/*.md` or `.mdx`):

```yaml
---
title: Page title          # required — page heading + <title>
description: Short text    # optional — meta description
order: 1                   # optional — sidebar sort. lower = first. default 99
---
```

**Writing posts** (`src/content/writing/*.md`):

```yaml
---
title: Post title          # required
date: "2026-04-11"         # required — ISO 8601, determines sort order
description: Short text    # optional
author: Name               # optional — displayed below date
---
```

## Components (MDX only — import at top of .mdx file)

### Callout

```mdx
import Callout from '../../components/Callout.astro'

<Callout>Default note.</Callout>
<Callout type="warning">Destructive action.</Callout>
<Callout type="tip">Helpful shortcut.</Callout>
```

Props: `type?: "note" | "warning" | "tip"` — default `"note"`.

### Tooltip

```mdx
import Tooltip from '../../components/Tooltip.astro'

The <Tooltip tip="Full definition here">term</Tooltip> means something.
```

Props: `tip: string` — required.

### FileTree

```mdx
import FileTree from '../../components/FileTree.astro'

<FileTree>
- src/
  - **highlighted-file.ts**
  - other-file.ts
- package.json
</FileTree>
```

Two spaces per indent level. `**filename**` highlights. Directories collapse on click. No props — content is slot.

### Tabs + Tab

```mdx
import Tabs from '../../components/Tabs.astro'
import Tab from '../../components/Tab.astro'

<Tabs labels={["Option A", "Option B"]}>
<Tab>
Content for A.
</Tab>
<Tab>
Content for B.
</Tab>
</Tabs>
```

`labels` array length must match number of `<Tab>` children.

### Mermaid

```mdx
import Mermaid from '../../components/Mermaid.astro'

<Mermaid code={`
flowchart LR
  A[Start] --> B[End]
`} />
```

Props: `code: string` — required. Supports all Mermaid diagram types. Theme-aware.

### Image

```mdx
import Image from '../../components/Image.astro'

<Image src={import('./diagram.png')} alt="Alt text" caption="Optional caption" />
```

Local images from `src/assets/` are optimized at build time.

### Collapsible (native HTML — no import)

```html
<details>
<summary>Section title</summary>

Content here. Supports markdown.

</details>
```

Add `open` attribute to start expanded.

## CLI commands

```
mkdocx init               scaffold docs/ in the current project
mkdocx dev [--port N]     dev server at localhost:4321
mkdocx build              production build → docs/.mkdocx/dist/
mkdocx preview            preview production build locally
mkdocx clean              remove docs/.mkdocx/ (force reinstall on next run)
mkdocx context            generate this LLM context file
```

## URL routing

```
docs/src/content/docs/getting-started.md  → /docs/getting-started
docs/src/content/docs/guides/deploy.md    → /docs/guides/deploy
docs/src/content/writing/first-post.md    → /writing/first-post
```

Subdirectories in `docs/` create labeled section headers in the sidebar.

## Writing style — transfa aesthetic

All documentation must follow this style:

- Direct. No preamble. Start with the fact, not context about the fact.
- No "In this guide", "Welcome to", "Let's explore". Just the content.
- Short sentences. Dense information.
- Use tables for reference material. Use code blocks for anything runnable.
- `##` for sections. `###` for subsections. Never use `#` — mkdocx renders the frontmatter title.
- No trailing summaries or "you've learned" sections.
- Monospace-aesthetic: prefer technical precision over warmth.
- Example of the style in practice:

```markdown
## Installation

Run from your project root:

\`\`\`bash
pip install mkdocx
mkdocx init
\`\`\`

On first run, mkdocx installs Node.js dependencies automatically.
```

Not:

```markdown
## Getting Started with Installation

Welcome! In this section, we'll walk you through the installation process.
To get started, you'll need to run the following command...
```

## What good docs look like

A complete mkdocx documentation site for a software project has:

1. `getting-started.md` — install, first run, what it does in 2 minutes
2. `configuration.md` — every config option with type + example
3. One page per major concept/subsystem (e.g. `pipelines.md`, `schedules.md`)
4. `reference.md` — CLI flags, schema tables, error codes
5. Optional: `writing/` posts for architectural decisions, release notes, changelogs

Each page: complete but minimal. No padding. If a section needs 3 sentences, write 3 sentences.
