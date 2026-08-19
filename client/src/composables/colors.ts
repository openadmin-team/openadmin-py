// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import type { Color } from "@/schemas/color"
import { computed, toValue, type MaybeRefOrGetter } from "vue"

export const useColor = (color: MaybeRefOrGetter<Color>) => {
	const style = computed(() => COLOR_STYLES[toValue(color)])

	return {
		style,
	}
}

const COLOR_STYLES = {
	slate: {
		dot: "bg-slate-500",
		text: "text-slate-600 dark:text-slate-400",
	},
	gray: {
		dot: "bg-gray-500",
		text: "text-gray-600 dark:text-gray-400",
	},
	zinc: {
		dot: "bg-zinc-500",
		text: "text-zinc-600 dark:text-zinc-400",
	},
	neutral: {
		dot: "bg-neutral-500",
		text: "text-neutral-600 dark:text-neutral-400",
	},
	stone: {
		dot: "bg-stone-500",
		text: "text-stone-600 dark:text-stone-400",
	},
	red: {
		dot: "bg-red-500",
		text: "text-red-600 dark:text-red-400",
	},
	orange: {
		dot: "bg-orange-500",
		text: "text-orange-600 dark:text-orange-400",
	},
	amber: {
		dot: "bg-amber-500",
		text: "text-amber-600 dark:text-amber-400",
	},
	yellow: {
		dot: "bg-yellow-500",
		text: "text-yellow-600 dark:text-yellow-400",
	},
	lime: {
		dot: "bg-lime-500",
		text: "text-lime-600 dark:text-lime-400",
	},
	green: {
		dot: "bg-green-500",
		text: "text-green-600 dark:text-green-400",
	},
	emerald: {
		dot: "bg-emerald-500",
		text: "text-emerald-600 dark:text-emerald-400",
	},
	teal: {
		dot: "bg-teal-500",
		text: "text-teal-600 dark:text-teal-400",
	},
	cyan: {
		dot: "bg-cyan-500",
		text: "text-cyan-600 dark:text-cyan-400",
	},
	sky: {
		dot: "bg-sky-500",
		text: "text-sky-600 dark:text-sky-400",
	},
	blue: {
		dot: "bg-blue-500",
		text: "text-blue-600 dark:text-blue-400",
	},
	indigo: {
		dot: "bg-indigo-500",
		text: "text-indigo-600 dark:text-indigo-400",
	},
	violet: {
		dot: "bg-violet-500",
		text: "text-violet-600 dark:text-violet-400",
	},
	purple: {
		dot: "bg-purple-500",
		text: "text-purple-600 dark:text-purple-400",
	},
	fuchsia: {
		dot: "bg-fuchsia-500",
		text: "text-fuchsia-600 dark:text-fuchsia-400",
	},
	pink: {
		dot: "bg-pink-500",
		text: "text-pink-600 dark:text-pink-400",
	},
	rose: {
		dot: "bg-rose-500",
		text: "text-rose-600 dark:text-rose-400",
	},
	black: {
		dot: "bg-neutral-900 dark:bg-white",
		text: "text-neutral-900 dark:text-white",
	},
	white: {
		dot: "bg-white border border-neutral-300 dark:border-neutral-600",
		text: "text-neutral-500 dark:text-neutral-400",
	},
} as const satisfies Record<Color, { dot: string; text: string }>
