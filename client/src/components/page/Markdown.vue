<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import DOMPurify from "dompurify"
import { marked } from "marked"
import { computed } from "vue"
import { Skeleton } from "@/components/ui/skeleton"
import { useMarkdown } from "@/composables/openadmin-markdown"

const props = defineProps<{
	sectionId: string
	pageId: string
	markdownId: string
}>()

const { content, isLoading } = useMarkdown({
	sectionId: props.sectionId,
	pageId: props.pageId,
	markdownId: props.markdownId,
})

const html = computed(() => {
	if (!content.value) return ""
	return DOMPurify.sanitize(marked.parse(content.value, { async: false, gfm: true }))
})
</script>

<template>
	<div v-if="isLoading" class="flex w-full max-w-[37em] flex-col gap-3">
		<Skeleton class="h-5 w-2/3" />
		<Skeleton class="h-4 w-full" />
		<Skeleton class="h-4 w-full" />
		<Skeleton class="h-4 w-5/6" />
	</div>
	<div v-else class="typeset typeset-docs max-w-[37em]" v-html="html" />
</template>
