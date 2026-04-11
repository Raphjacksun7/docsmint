---
title: Writing content
description: Markdown, frontmatter fields, and file organization.
order: 3
---

mkdocx uses standard markdown with MDX extensions. Docs live in `src/content/docs/`. Writing (blog posts) lives in `src/content/writing/`.

## Frontmatter

Every file begins with YAML frontmatter.

**Docs pages:**

```yaml
---
title: Page title
description: Short description for metadata.
order: 1
---
```

**Writing posts:**

```yaml
---
title: Post title
date: "2026-04-10"
description: Short description.
---
```

| Field | Required for | Purpose |
|-------|-------------|---------|
| `title` | docs, writing | Page heading and browser title |
| `description` | docs, writing | Meta description |
| `order` | docs | Sidebar sort position. Lower = first |
| `date` | writing | Publication date. Determines sort order |

## Headings

Use `##` for sections, `###` for subsections. `#` is reserved — mkdocx uses the `title` frontmatter field as the page title.

## Code blocks

Wrap in triple backticks with a language tag:

```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

Supported: `python`, `javascript`, `typescript`, `bash`, `sql`, `yaml`, `go`, `rust`, `json`, and many more.

## Collapsible sections

Use `<details>` and `<summary>` for expandable content. Content starts collapsed by default.

```html
<details>
<summary>Full output</summary>

Your content here. Supports markdown, code blocks, and tables.

</details>
```

Add the `open` attribute to start expanded:

```html
<details open>
<summary>Benchmark results</summary>

| Run | Latency |
|-----|---------|
| p50 | 12ms    |
| p99 | 47ms    |

</details>
```

Use collapsible sections for long outputs, optional reference material, or troubleshooting steps that would interrupt the reading flow.

## File organization

Files in `src/content/docs/` map directly to URLs. Files in subdirectories create section groups in the sidebar.

```
src/content/docs/
├── getting-started.md     → /docs/getting-started
├── configuration.md       → /docs/configuration
└── guides/
    ├── custom-theme.md    → /docs/guides/custom-theme
    └── deployment.md      → /docs/guides/deployment
```

Pages in subdirectories appear under a labeled section header in the sidebar. A `guides/` directory produces a **guides** section heading above its pages.

Without subdirectory:
```
getting-started
configuration
custom-theme
deployment
```

With subdirectory:
```
getting-started
configuration

guides
  custom-theme
  deployment
```

Sort order within each section is controlled by the `order` frontmatter field.
