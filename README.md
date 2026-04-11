# mkdocx

Minimal markdown documentation builder. Write docs in markdown, get a fast static site — no Astro knowledge required.

## Install

```sh
pip install artifacts-keyring
pip install mkdocx --index-url https://centiro.pkgs.visualstudio.com/_packaging/Internal_Python/pypi/simple/ --extra-index-url https://pypi.org/simple/
```

## Usage

From your project root:

```sh
mkdocx init       # scaffold docs/ in the current project
mkdocx dev        # start local dev server (localhost:4321)
mkdocx build      # build for production
mkdocx preview    # preview the production build
mkdocx deploy gs://my-bucket  # build and deploy to GCS
mkdocx clean      # remove the working directory
```

On first run, mkdocx will offer to scaffold a `docs/` directory if none exists.

## Docs structure

Only two things belong in your repo:

```
docs/
├── mkdocx.config.js        # site name, nav, footer
└── src/
    └── content/
        └── docs/
            └── *.md        # your markdown pages
```

The rendering engine (Astro, components, styles) is bundled inside the package and managed automatically.

## Config

```js
// docs/mkdocx.config.js
export default {
  name: 'my-project',
  description: '',
  nav: [
    { label: 'docs', href: '/docs/getting-started' },
  ],
  footer: [],
}
```

## Page frontmatter

```md
---
title: Getting started
description: Welcome to the docs.
order: 1
---
```
