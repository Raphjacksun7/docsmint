---
title: Deploying
description: Deploy mkdocx with Node.js, Python, Docker, or GCP.
order: 5
---

mkdocx builds to static HTML. Deploy it anywhere that serves files.

## Build

```bash
pnpm build
# npm run build
# mkdocx build
```

Output goes to `dist/` — HTML pages, CSS/JS bundles, and Pagefind search indexes.

## Node.js

Serve `dist/` with any static file server. The `serve` package works well.

```bash
# One-time
npx serve dist

# Or install globally
pnpm add -g serve
serve dist
```

For production, serve `dist/` from a Node.js process:

```javascript
import express from 'express'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const app = express()
const dir = join(dirname(fileURLToPath(import.meta.url)), 'dist')
app.use(express.static(dir))
app.listen(3000)
```

Preview the production build locally with the built-in Astro server:

```bash
pnpm preview     # http://localhost:3000
npm run preview
```

## Python

The `mkdocx` pip package includes a CLI that wraps all build and deploy commands.

```bash
pip install mkdocx
```

```bash
mkdocx dev              # dev server at localhost:4321
mkdocx build            # production build → dist/
mkdocx preview          # preview build locally
mkdocx deploy <bucket>  # build + sync to GCS bucket
```

`mkdocx deploy` runs `pnpm build` then syncs `dist/` to a Google Cloud Storage bucket via `gsutil rsync`.

```bash
mkdocx deploy gs://your-docs
```

The CLI auto-detects the project root by walking up from the current directory until it finds `mkdocx.config.js`.

## Docker

Build a container image using a two-stage Dockerfile: Node.js builder + nginx server.

```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

```bash
docker build -t my-docs .
docker run -p 8080:80 my-docs
```

## GCP Cloud Storage

Build and sync to a public GCS bucket.

```bash
# Create bucket
gsutil mb gs://your-docs/

# Build and upload
pnpm build
gsutil -m rsync -r -d dist/ gs://your-docs/

# Make public
gsutil iam ch allUsers:objectViewer gs://your-docs
```

Enable Cloud CDN and point a domain at the static IP. Invalidate cache on each deploy:

```bash
gcloud compute cdn-cache-keys invalidate \
  --global --resource=cdn-resource-name
```

For automated deploys with Cloud Build:

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/docs', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/docs']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'docs',
           '--image', 'gcr.io/$PROJECT_ID/docs',
           '--region', 'us-central1']
```
