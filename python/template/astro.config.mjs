// @ts-check
import { defineConfig } from 'astro/config'
import tailwindcss from '@tailwindcss/vite'
import mdx from '@astrojs/mdx'
import sitemap from '@astrojs/sitemap'
import rehypePrettyCode from 'rehype-pretty-code'
import rehypeExternalLinks from 'rehype-external-links'
import { cleanInlineCodeIntegration } from './plugins/clean-inline-code.mjs'
import path from 'path'
import fs from 'fs'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

/**
 * Vite plugin — resolves ../../components/* imports from user content files.
 *
 * User content lives at docs/src/content/ (real path). When Vite processes
 * an .mdx file there, it uses the real path. A relative import like
 * ../../components/Callout.astro resolves to docs/src/components/ which
 * doesn't exist. This plugin intercepts those and redirects to the template's
 * own src/components/ — keeping docs/ clean.
 */
function mkdocxComponentsResolver() {
  const templateComponents = path.resolve(__dirname, 'src/components')
  return {
    name: 'mkdocx-components-resolver',
    resolveId(source, importer) {
      if (!importer || !source.startsWith('.')) return null
      const match = source.match(/components\/(.+)$/)
      if (!match) return null
      const resolved = path.resolve(path.dirname(importer), source)
      if (!fs.existsSync(resolved)) {
        const templatePath = path.resolve(templateComponents, match[1])
        if (fs.existsSync(templatePath)) return templatePath
      }
      return null
    },
  }
}

/** @type {import('rehype-pretty-code').Options} */
const prettyCodeOptions = {
  theme: 'github-dark',
  keepBackground: true,
}

const rehypePlugins = [
  [rehypePrettyCode, prettyCodeOptions],
  [rehypeExternalLinks, { target: '_blank', rel: ['noopener', 'noreferrer'] }],
]

export default defineConfig({
  site: 'https://docs.example.com',
  integrations: [
    mdx({ rehypePlugins }),
    sitemap(),
    cleanInlineCodeIntegration(),
  ],
  markdown: {
    rehypePlugins,
    syntaxHighlight: false,
  },
  vite: {
    plugins: [tailwindcss(), mkdocxComponentsResolver()],
    build: {
      rollupOptions: {
        external: ['/pagefind/pagefind.js'],
      },
    },
  },
})
