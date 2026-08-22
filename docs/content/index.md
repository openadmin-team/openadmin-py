---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "OpenAdmin"
  text: "Admin panel for python"
  tagline: Build admin dashboards as FastAPI routes — stats, tables, charts, and actions, all in pure Python using any orm and api.
  actions:
    - theme: brand
      text: What is OpenAdmin?
      link: /introduction/what-is-openadmin
    - theme: alt
      text: Getting Started
      link: /introduction/getting-started

features:
  - icon: 📊
    title: Stats, Tables & Charts
    details: Single-value stats, paginated searchable tables, and bar/pie charts — each just a decorated FastAPI endpoint.
  - icon: 📝
    title: Forms & Actions
    details: Structured forms and one-off action buttons that submit to your own endpoints, with typed parameters inferred automatically.
  - icon: 🔌
    title: FastAPI-native
    details: A page is a router, a widget is an endpoint. Full dependency injection, OpenAPI docs, and middleware compatibility for free.
---

