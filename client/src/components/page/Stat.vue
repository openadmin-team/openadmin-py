<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { useIconColor } from "@/composables/colors"
import { Button } from "@/components/ui/button"
import { Icon } from "@iconify/vue"
import { useStat } from "@/composables/openadmin-stat";

const props = defineProps<{
	sectionId: string
	pageId: string
	statId: string
}>()
const { stat } = useStat({
	sectionId: props.sectionId,
	pageId: props.pageId,
	statId: props.statId,
})
const { style } = useIconColor(() => stat.value?.color || "slate")
</script>

<template>
	{{ stat }}
    {{ style }}
</template>