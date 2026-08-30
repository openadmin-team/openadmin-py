<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import type { AttachmentMediaVariants } from "."
import { cn } from "@/lib/utils"
import { attachmentMediaVariants } from "."

const props = defineProps<{
	class?: HTMLAttributes["class"]
	variant?: AttachmentMediaVariants["variant"]
}>()
</script>

<template>
	<div
		data-slot="attachment-media"
		:data-variant="variant"
		:class="cn(attachmentMediaVariants({ variant }), props.class)"
	>
		<slot />
	</div>
</template>
