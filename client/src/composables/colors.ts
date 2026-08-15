// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import type { Color } from "@/schemas/color"
import { computed, toValue, type MaybeRefOrGetter } from "vue"

export const useIconColor = (color: MaybeRefOrGetter<Color>) => {
    const style = computed(() => COLOR_STYLES[toValue(color)])

    return {
        style,
    }
}

const COLOR_STYLES = {
	slate: {
		dot: "bg-slate-500",
		badge: "bg-slate-100 text-slate-700 dark:bg-slate-500/15 dark:text-slate-300",
		text: "text-slate-600 dark:text-slate-400",
	},
	gray: {
		dot: "bg-gray-500",
		badge: "bg-gray-100 text-gray-700 dark:bg-gray-500/15 dark:text-gray-300",
		text: "text-gray-600 dark:text-gray-400",
	},
	zinc: {
		dot: "bg-zinc-500",
		badge: "bg-zinc-100 text-zinc-700 dark:bg-zinc-500/15 dark:text-zinc-300",
		text: "text-zinc-600 dark:text-zinc-400",
	},
	neutral: {
		dot: "bg-neutral-500",
		badge: "bg-neutral-100 text-neutral-700 dark:bg-neutral-500/15 dark:text-neutral-300",
		text: "text-neutral-600 dark:text-neutral-400",
	},
	stone: {
		dot: "bg-stone-500",
		badge: "bg-stone-100 text-stone-700 dark:bg-stone-500/15 dark:text-stone-300",
		text: "text-stone-600 dark:text-stone-400",
	},
	red: {
		dot: "bg-red-500",
		badge: "bg-red-100 text-red-700 dark:bg-red-500/15 dark:text-red-300",
		text: "text-red-600 dark:text-red-400",
	},
	orange: {
		dot: "bg-orange-500",
		badge: "bg-orange-100 text-orange-700 dark:bg-orange-500/15 dark:text-orange-300",
		text: "text-orange-600 dark:text-orange-400",
	},
	amber: {
		dot: "bg-amber-500",
		badge: "bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300",
		text: "text-amber-600 dark:text-amber-400",
	},
	yellow: {
		dot: "bg-yellow-500",
		badge: "bg-yellow-100 text-yellow-700 dark:bg-yellow-500/15 dark:text-yellow-300",
		text: "text-yellow-600 dark:text-yellow-400",
	},
	lime: {
		dot: "bg-lime-500",
		badge: "bg-lime-100 text-lime-700 dark:bg-lime-500/15 dark:text-lime-300",
		text: "text-lime-600 dark:text-lime-400",
	},
	green: {
		dot: "bg-green-500",
		badge: "bg-green-100 text-green-700 dark:bg-green-500/15 dark:text-green-300",
		text: "text-green-600 dark:text-green-400",
	},
	emerald: {
		dot: "bg-emerald-500",
		badge: "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300",
		text: "text-emerald-600 dark:text-emerald-400",
	},
	teal: {
		dot: "bg-teal-500",
		badge: "bg-teal-100 text-teal-700 dark:bg-teal-500/15 dark:text-teal-300",
		text: "text-teal-600 dark:text-teal-400",
	},
	cyan: {
		dot: "bg-cyan-500",
		badge: "bg-cyan-100 text-cyan-700 dark:bg-cyan-500/15 dark:text-cyan-300",
		text: "text-cyan-600 dark:text-cyan-400",
	},
	sky: {
		dot: "bg-sky-500",
		badge: "bg-sky-100 text-sky-700 dark:bg-sky-500/15 dark:text-sky-300",
		text: "text-sky-600 dark:text-sky-400",
	},
	blue: {
		dot: "bg-blue-500",
		badge: "bg-blue-100 text-blue-700 dark:bg-blue-500/15 dark:text-blue-300",
		text: "text-blue-600 dark:text-blue-400",
	},
	indigo: {
		dot: "bg-indigo-500",
		badge: "bg-indigo-100 text-indigo-700 dark:bg-indigo-500/15 dark:text-indigo-300",
		text: "text-indigo-600 dark:text-indigo-400",
	},
	violet: {
		dot: "bg-violet-500",
		badge: "bg-violet-100 text-violet-700 dark:bg-violet-500/15 dark:text-violet-300",
		text: "text-violet-600 dark:text-violet-400",
	},
	purple: {
		dot: "bg-purple-500",
		badge: "bg-purple-100 text-purple-700 dark:bg-purple-500/15 dark:text-purple-300",
		text: "text-purple-600 dark:text-purple-400",
	},
	fuchsia: {
		dot: "bg-fuchsia-500",
		badge: "bg-fuchsia-100 text-fuchsia-700 dark:bg-fuchsia-500/15 dark:text-fuchsia-300",
		text: "text-fuchsia-600 dark:text-fuchsia-400",
	},
	pink: {
		dot: "bg-pink-500",
		badge: "bg-pink-100 text-pink-700 dark:bg-pink-500/15 dark:text-pink-300",
		text: "text-pink-600 dark:text-pink-400",
	},
	rose: {
		dot: "bg-rose-500",
		badge: "bg-rose-100 text-rose-700 dark:bg-rose-500/15 dark:text-rose-300",
		text: "text-rose-600 dark:text-rose-400",
	},
	black: {
		dot: "bg-neutral-900 dark:bg-white",
		badge: "bg-neutral-900/10 text-neutral-900 dark:bg-white/15 dark:text-white",
		text: "text-neutral-900 dark:text-white",
	},
	white: {
		dot: "bg-white border border-neutral-300 dark:border-neutral-600",
		badge:
			"bg-white text-neutral-700 border border-neutral-200 dark:bg-neutral-800 dark:text-neutral-200 dark:border-neutral-700",
		text: "text-neutral-500 dark:text-neutral-400",
	},
} as const satisfies Record<Color, { dot: string; badge: string; text: string }>