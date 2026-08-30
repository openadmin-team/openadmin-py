import path from "node:path"
import { defineConfig } from "vite"
import tailwindcss from "@tailwindcss/vite"
import vue from "@vitejs/plugin-vue"

export default defineConfig({
	base: "./",
	plugins: [vue(), tailwindcss()],
	resolve: {
		alias: {
			"@": path.resolve(import.meta.dirname, "./src"),
		},
	},
	build: {
		outDir: path.resolve(import.meta.dirname, "../openadmin/__client__"),
		emptyOutDir: true,
	},
	server: {
		proxy: {
			"/api": {
				target: "http://localhost:8000/admin",
				changeOrigin: true,
			},
			"/auth": {
				target: "http://localhost:8000/admin",
				changeOrigin: true,
			},
			// component data endpoints, e.g. /{sectionId}/{pageId}/stat/{statId}
			// (excludes /src/... and /node_modules/... so dev-server source
			// requests, e.g. /src/components/table/Table.vue, aren't caught)
			"^/(?!src/|node_modules/|@vite/|@fs/|@id/)[^/]+/[^/]+/(stat|table|action|form|markdown|bar-chart|pie-chart)/[^/]+$":
				{
					target: "http://localhost:8000/admin",
					changeOrigin: true,
				},
		},
	},
})
