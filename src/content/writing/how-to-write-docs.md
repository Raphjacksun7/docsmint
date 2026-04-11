---
title: How to write documentation that works
date: "2026-04-11"
description: The system, the style, and the rules we follow when writing with mkdocx.
author: mkdocx
---

## Structure first

Every page should answer three questions, in order: what is it, why does it exist, how do you use it.

Skip the why if it’s obvious. Never skip the what.

Starting with usage before context forces the reader to reconstruct intent. Most won’t.

If you can’t describe what a page covers in one clear sentence, the page isn’t ready yet.

Files live in `src/content/docs/`. Subdirectories define sidebar sections. Filenames become URLs. Use `kebab-case`.

Use `order` in frontmatter to control position. Increment by 10 to leave room.

---

## Write less

Remove anything that doesn’t carry weight.

Common patterns to cut:
“you can”, “this allows you to”, “in order to”, “it’s worth noting”

What remains is usually the sentence you meant to write.

Short paragraphs. One idea each. Space between them.

Avoid hedging. “Consider” is enough.

---

## Components have rules

**Callout** — use when context would be lost inline. Once or twice per page is usually enough.

**Tooltip** — for jargon. Keep it to one sentence.

**FileTree** — show structure. Keep it minimal. Directories open by default.

**Tabs** — for alternatives only (pnpm / npm / pip). Not for structuring content.

**Collapsible** (`<details>`) — for optional or interrupting content. If everything is collapsible, nothing is.

---

## Code blocks always have a language

Every code block should declare its language.

If your example includes triple backticks, use four backticks for the outer fence. The parser is literal.

---

## The sidebar is a contract

Each item in the sidebar sets an expectation.

Only include pages that are complete and useful.
Avoid placeholders — they break trust faster than missing pages.

---

## llms.txt

mkdocx provides a machine-readable reference at `/llms.txt`.

It defines components, structure, and conventions.

If you’re using an LLM, point it there first.
It exists so you don’t have to restate the system each time.

---

Good documentation teaches.

It helps readers understand what to do.
It helps systems understand how to do it.

The goal is the same.
