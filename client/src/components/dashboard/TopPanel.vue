<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
// import { computed } from "vue"
// import { RouterLink, useRoute } from "vue-router"
// import ThemeToggle from "@/components/dashboard/ThemeToggle.vue"
// import {
// 	Breadcrumb,
// 	BreadcrumbItem,
// 	BreadcrumbLink,
// 	BreadcrumbList,
// 	BreadcrumbPage,
// 	BreadcrumbSeparator,
// } from "@/components/ui/breadcrumb"
// import { Separator } from "@/components/ui/separator"
// import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
// import { useOpenAdminSpec } from "@/composables/openadmin-spec"
// import { colorStyle } from "@/lib/colors"
// import { findFormComponent, findPage } from "@/lib/spec-utils"
// import { cn } from "@/lib/utils"

// const route = useRoute()
// const { data: spec } = useOpenAdminSpec()

// const location = computed(() => {
// 	const { sectionId, pageId } = route.params
// 	if (!spec.value || typeof sectionId !== "string" || typeof pageId !== "string") return null
// 	return findPage(spec.value, sectionId, pageId)
// })

// const formLocation = computed(() => {
// 	const { sectionId, pageId, formId } = route.params
// 	if (
// 		!spec.value ||
// 		typeof sectionId !== "string" ||
// 		typeof pageId !== "string" ||
// 		typeof formId !== "string"
// 	) {
// 		return null
// 	}
// 	return findFormComponent(spec.value, sectionId, pageId, formId)
// })
</script>

<template>
	<!-- 	
			<header class="flex h-14 shrink-0 items-center gap-2 border-b px-4">
				<SidebarTrigger />
				<Separator orientation="vertical" class="mr-2 h-4" />
				<Breadcrumb v-if="location">
					<BreadcrumbList>
						<BreadcrumbItem>
							<span class="text-muted-foreground">{{ location.section.name }}</span>
						</BreadcrumbItem>
						<BreadcrumbSeparator />
						<BreadcrumbItem>
							<BreadcrumbLink v-if="formLocation" as-child>
								<RouterLink
									:to="{
										name: 'page',
										params: { sectionId: location.section.id, pageId: location.page.id },
									}"
								>
									{{ location.page.name }}
								</RouterLink>
							</BreadcrumbLink>
							<BreadcrumbPage v-else>{{ location.page.name }}</BreadcrumbPage>
						</BreadcrumbItem>
						<template v-if="formLocation">
							<BreadcrumbSeparator />
							<BreadcrumbItem>
								<BreadcrumbPage class="flex items-center gap-1.5">
									<DynamicIcon
										v-if="formLocation.component.icon"
										:name="formLocation.component.icon"
										:class="cn('size-3.5', colorStyle(formLocation.component.color).text)"
									/>
									{{ formLocation.component.name }}
								</BreadcrumbPage>
							</BreadcrumbItem>
						</template>
					</BreadcrumbList>
				</Breadcrumb>
				<ThemeToggle class="ml-auto" />
			</header> -->
</template>
