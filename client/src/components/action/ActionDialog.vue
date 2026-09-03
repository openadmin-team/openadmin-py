<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { Icon } from "@iconify/vue"
import { computed, ref, watch } from "vue"
import { Button } from "@/components/ui/button"
import { Dialog, DialogClose, DialogContent, DialogFooter } from "@/components/ui/dialog"
import { FieldGroup } from "@/components/ui/field"
import { Spinner } from "@/components/ui/spinner"
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
	initialValues?: Record<string, unknown>
}>()

const open = defineModel<boolean>("open", { default: false })

const { action, dataForm, isPending } = useActionForm({
	sectionId: props.sectionId,
	pageId: props.pageId,
	actionId: props.actionId,
	initialValues: props.initialValues,
	onSuccess: () => {
		open.value = false
	},
})

const fields = computed<FieldDef[]>(() => [
	...fieldsOfSchema(action.value?.query, "query"),
	...fieldsOfSchema(action.value?.body, "body"),
	...fieldsOfSchema(action.value?.form, "form"),
])

// Row/bulk actions prefill fields from the selected row's data (see
// DataTableDropDown's `initialValues`). Those fields are already filled in
// and rarely need editing, so they're collapsed out of the form to keep the
// modal short — a single toggle expands them back in if they do.
function isPrefilled(key: string): boolean {
	const value = props.initialValues?.[key]
	if (value === undefined || value === null || value === "") return false
	if (Array.isArray(value) && value.length === 0) return false
	return true
}

const revealed = ref(false)

const hiddenCount = computed(
	() => (revealed.value ? 0 : fields.value.filter((f) => isPrefilled(f.key)).length),
)

watch(open, (value) => {
	if (!value) {
		dataForm.reset()
		revealed.value = false
	}
})
</script>

<template>
	<Dialog v-if="action" v-model:open="open">
		<DialogContent>
			<form @submit.prevent="dataForm.handleSubmit">
				<FieldGroup v-if="fields.length" class="grid grid-cols-1 gap-y-4 py-4">
					<dataForm.Field v-for="f in fields" :key="f.key" :name="f.key">
						<template #default="{ field }">
							<template v-if="revealed || !isPrefilled(f.key)">
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
						</template>
					</dataForm.Field>
					<Button
						v-if="hiddenCount"
						type="button"
						variant="ghost"
						size="sm"
						class="justify-self-start text-muted-foreground"
						@click="revealed = true"
					>
						<Icon icon="lucide:eye" class="size-4" />
						Show {{ hiddenCount }} prefilled field{{ hiddenCount > 1 ? "s" : "" }}
					</Button>
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
