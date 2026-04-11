#!/usr/bin/env node
import { spawn } from 'child_process'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const __dir = dirname(fileURLToPath(import.meta.url))
const root  = join(__dir, '..')
const [,, cmd = 'dev', ...args] = process.argv

const scripts = {
  dev:     ['astro', 'dev'],
  build:   ['sh', '-c', 'astro build && pagefind --site dist'],
  preview: ['astro', 'preview'],
  new:     ['node', join(__dir, 'mkdocx-new.js')],
}

const [bin, ...binArgs] = scripts[cmd] ?? ['astro', cmd]

spawn(bin, [...binArgs, ...args], {
  cwd: root,
  stdio: 'inherit',
  shell: process.platform === 'win32',
}).on('exit', code => process.exit(code ?? 0))
