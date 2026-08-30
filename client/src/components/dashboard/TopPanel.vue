<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { Icon } from "@iconify/vue"
import { computed } from "vue"
import { useRoute } from "vue-router"
import CommandPanel from "@/components/command/CommandPanel.vue"
import CommandTrigger from "@/components/command/CommandTrigger.vue"
import ThemeToggle from "@/components/dashboard/ThemeToggle.vue"
import {
	Breadcrumb,
	BreadcrumbItem,
	BreadcrumbList,
	BreadcrumbPage,
	BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { usePageSpec } from "@/composables/openadmin-page"
import { useSectionSpec } from "@/composables/openadmin-section"
import { useForm } from "@/composables/openadmin-form"
import { useColor } from "@/composables/colors"

const route = useRoute()

const sectionId = computed(() => route.params.sectionId as string)
const pageId = computed(() => route.params.pageId as string)
const formId = computed(() => (route.params.formId || "") as string)

const { data: section } = useSectionSpec({ sectionId })
const { page } = usePageSpec({ sectionId, pageId })
const { form } = useForm({ sectionId, pageId, formId })
const { style } = useColor(() => form.value?.color || "slate")
</script>

<template>
	<header class="flex h-14 shrink-0 items-center gap-2 border-b px-4">
		<SidebarTrigger />
		<Separator orientation="vertical" class="mr-2 h-4" />
		<Breadcrumb v-if="section && page">
			<BreadcrumbList>
				<BreadcrumbItem>
					<span class="text-muted-foreground">{{ section.name }}</span>
				</BreadcrumbItem>
				<BreadcrumbSeparator />
				<BreadcrumbItem>
					<BreadcrumbPage class="flex items-center gap-1.5">
						<Icon v-if="page.icon" :icon="`lucide:${page.icon}`" />
						{{ page.name }}
					</BreadcrumbPage>
				</BreadcrumbItem>

				<BreadcrumbSeparator v-if="form" />
				<BreadcrumbItem v-if="form">
					<BreadcrumbPage class="flex items-center gap-1.5">
						<Icon v-if="form.icon" :icon="`lucide:${form.icon}`" :class="style.text" />
						{{ form.name }}
					</BreadcrumbPage>
				</BreadcrumbItem>
			</BreadcrumbList>
		</Breadcrumb>
		<CommandTrigger class="ml-auto" />
		<ThemeToggle />
	</header>
	<CommandPanel />
</template>
