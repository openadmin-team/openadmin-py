<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { Icon } from "@iconify/vue"
import { computed, ref, watch } from "vue"
import { Button } from "@/components/ui/button"
import {
	Dialog,
	DialogClose,
	DialogContent,
	DialogDescription,
	DialogFooter,
	DialogHeader,
	DialogTitle,
	DialogTrigger,
} from "@/components/ui/dialog"
import { FieldGroup } from "@/components/ui/field"
import { Spinner } from "@/components/ui/spinner"
import { useColor } from "@/composables/colors"
import { useActionForm } from "@/composables/openadmin-action"
import FieldArray from "./FieldArray.vue"
import FieldBool from "./FieldBool.vue"
import FieldDate from "./FieldDate.vue"
import FieldDateTime from "./FieldDateTime.vue"
import { fieldsOfSchema, type FieldDef } from "./field"
import FieldFile from "./FieldFile.vue"
import FieldFileArray from "./FieldFileArray.vue"
import FieldNumeric from "./FieldNumeric.vue"
import FieldSelect from "./FieldSelect.vue"
import FieldString from "./FieldString.vue"

const props = defineProps<{
	sectionId: string
	pageId: string
	actionId: string
}>()

const open = ref(false)

const { action, dataForm, isPending } = useActionForm({
	sectionId: props.sectionId,
	pageId: props.pageId,
	actionId: props.actionId,
	onSuccess: () => {
		open.value = false
	},
})
const { style } = useColor(() => action.value?.color || "slate")

const fields = computed<FieldDef[]>(() => [
	...fieldsOfSchema(action.value?.query, "query"),
	...fieldsOfSchema(action.value?.body, "body"),
	...fieldsOfSchema(action.value?.form, "form"),
])

watch(open, (value) => {
	if (!value) dataForm.reset()
})
</script>

<template>
	<Dialog v-if="action" v-model:open="open">
		<DialogTrigger as-child>
			<Button size="sm" variant="outline">
				<Icon v-if="action.icon" :icon="`lucide:${action.icon}`" :class="style.text" />
				{{ action.name }}
			</Button>
		</DialogTrigger>
		<DialogContent>
			<form @submit.prevent="dataForm.handleSubmit">
				<DialogHeader>
					<DialogTitle>{{ action.name }}</DialogTitle>
					<DialogDescription v-if="action.description">{{ action.description }}</DialogDescription>
				</DialogHeader>
				<FieldGroup v-if="fields.length" class="grid grid-cols-1 gap-y-4 py-4">
					<dataForm.Field v-for="f in fields" :key="f.key" :name="f.key">
						<template #default="{ field }">
							<FieldBool v-if="f.boolean" :field="field" :def="f" />
							<FieldDate v-else-if="f.date" :field="field" :def="f" />
							<FieldDateTime v-else-if="f.datetime" :field="field" :def="f" />
							<FieldArray v-else-if="f.array" :field="field" :def="f" />
							<FieldFile v-else-if="f.file" :field="field" :def="f" />
							<FieldFileArray v-else-if="f.fileArray" :field="field" :def="f" />
							<FieldSelect v-else-if="f.select" :field="field" :def="f" />
							<FieldNumeric v-else-if="f.numeric" :field="field" :def="f" />
							<FieldString v-else :field="field" :def="f" />
						</template>
					</dataForm.Field>
				</FieldGroup>
				<DialogFooter>
					<DialogClose as-child>
						<Button type="button" variant="outline">Cancel</Button>
					</DialogClose>
					<Button type="submit" :disabled="isPending">
						<Spinner v-if="isPending" />
						{{ action.name }}
					</Button>
				</DialogFooter>
			</form>
		</DialogContent>
	</Dialog>
</template>
