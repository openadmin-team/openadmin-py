<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { computed } from "vue"
import { RouterLink, useRoute } from "vue-router"
import ThemeToggle from "@/components/dashboard/ThemeToggle.vue"
import {
	Breadcrumb,
	BreadcrumbItem,
	BreadcrumbLink,
	BreadcrumbList,
	BreadcrumbPage,
	BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { useOpenAdminPageSpec, useOpenAdminSectionSpec } from "@/composables/openadmin-spec"
import { cn } from "@/lib/utils"
import { Icon } from "@iconify/vue";

const route = useRoute()

const sectionId = computed(() => route.params.sectionId as string)
const pageId = computed(() => route.params.pageId as string)

const section = useOpenAdminSectionSpec({sectionId: sectionId.value})
const page = useOpenAdminPageSpec({sectionId: sectionId.value, pageId: pageId.value})
</script>

<template>	
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
	</header>
</template>
