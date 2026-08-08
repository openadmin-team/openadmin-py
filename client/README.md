# OpenAdmin client

A generic Vue 3 + TypeScript frontend for the OpenAdmin FastAPI library. It reads `GET /admin/spec.json` and renders sections, pages, and components (stats, tables, forms, actions, markdown, bar/pie charts) purely from that spec — no code here is specific to any one admin panel.

## Develop

```
bun install
bun run dev
```

The dev server proxies `/admin` to `http://localhost:8000` (see `vite.config.ts`), so run the example backend (`make dev/run` from the repo root) alongside it.

## Build

```
bun run build
```

Outputs to `dist/`, which `AdminPanel` serves directly at its mount path (e.g. `/admin/`) via its static-file fallback.
