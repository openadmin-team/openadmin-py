import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  srcDir: "../content",
  
  title: "OpenAdmin",
  description: "Admin panel for python",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Introduction', link: '/introduction/what-is-openadmin' },
      { text: 'Components', link: '/components/' },
      { text: 'Auth', link: '/auth/' },
      { text: 'Cookbook', link: '/cookbook/implementing-auth' }
    ],

    sidebar: [
      {
        text: 'Introduction',
        items: [
          { text: 'What is OpenAdmin?', link: '/introduction/what-is-openadmin' },
          { text: 'Getting Started', link: '/introduction/getting-started' }
        ]
      },
      {
        text: 'Components',
        items: [
          { text: 'Overview', link: '/components/' },
          { text: 'Stat', link: '/components/stat' },
          { text: 'Table', link: '/components/table' },
          { text: 'Form', link: '/components/form' },
          { text: 'Action', link: '/components/action' },
          { text: 'Markdown', link: '/components/markdown' },
          { text: 'Bar Chart', link: '/components/bar-chart' },
          { text: 'Pie Chart', link: '/components/pie-chart' },
          { text: 'Area Chart', link: '/components/area-chart' },
          { text: 'Line Chart', link: '/components/line-chart' }
        ]
      },
      {
        text: 'Auth',
        items: [
          { text: 'Password Authentication', link: '/auth/' }
        ]
      },
      {
        text: 'Cookbook',
        items: [
          { text: 'Implementing Auth', link: '/cookbook/implementing-auth' },
          { text: 'Implementing a Table', link: '/cookbook/implementing-table' },
          { text: 'Implementing a Form with a Reference', link: '/cookbook/implementing-form-with-reference' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/openadmin-team/openadmin-py' }
    ]
  }
})
