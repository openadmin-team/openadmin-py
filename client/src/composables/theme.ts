// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { useDark, useToggle } from "@vueuse/core"

export const isDark = useDark({ storageKey: "theme" })
export const toggleDark = useToggle(isDark)
