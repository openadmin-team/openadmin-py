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
})
