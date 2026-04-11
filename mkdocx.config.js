/** @type {import('./src/types').MkdocxConfig} */
export default {
  name: 'mkdocx',
  description: 'Minimal markdown documentation builder. Write docs. Get a clean site.',
  nav: [
    { label: 'docs',    href: '/docs/getting-started' },
    { label: 'writing', href: '/writing' },
  ],
  footer: [
    { label: 'Code Source', href: 'https://github.com' },
  ],
  // Date display format. Uses Intl.DateTimeFormat options.
  dateFormat: { year: 'numeric', month: 'short', day: 'numeric' },
  dateLocale: 'en-US',
}
