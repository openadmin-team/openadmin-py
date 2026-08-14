<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { AnyFieldApi } from "@tanstack/vue-form"
import { useRoute, useRouter } from "vue-router"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { useLoginForm } from "@/composables/auth"

const router = useRouter()
const route = useRoute()
const form = useLoginForm({
	onSuccess: () => {
		const { redirect } = route.query
		router.push(typeof redirect === "string" ? redirect : { name: "home" })
	},
})

function isInvalid(field: AnyFieldApi) {
	return field.state.meta.isTouched && !field.state.meta.isValid
}
</script>

<template>
	<div class="flex min-h-svh items-center justify-center p-6">
		<Card class="w-full max-w-sm">
			<CardHeader>
				<CardTitle>Login</CardTitle>
				<CardDescription>Enter your credentials to access your account</CardDescription>
			</CardHeader>
			<CardContent>
				<form @submit.prevent="form.handleSubmit">
					<FieldGroup>
						<form.Field name="username">
							<template #default="{ field }">
								<Field :data-invalid="isInvalid(field)">
									<FieldLabel :for="field.name">Username</FieldLabel>
									<Input
										:id="field.name"
										:name="field.name"
										:model-value="field.state.value"
										:aria-invalid="isInvalid(field)"
										autocomplete="username"
										@blur="field.handleBlur"
										@input="field.handleChange(($event.target as HTMLInputElement).value)"
									/>
									<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
								</Field>
							</template>
						</form.Field>
						<form.Field name="password">
							<template #default="{ field }">
								<Field :data-invalid="isInvalid(field)">
									<FieldLabel :for="field.name">Password</FieldLabel>
									<Input
										:id="field.name"
										:name="field.name"
										type="password"
										:model-value="field.state.value"
										:aria-invalid="isInvalid(field)"
										autocomplete="current-password"
										@blur="field.handleBlur"
										@input="field.handleChange(($event.target as HTMLInputElement).value)"
									/>
									<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
								</Field>
							</template>
						</form.Field>
						<Field>
							<Button type="submit">Login</Button>
						</Field>
					</FieldGroup>
				</form>
			</CardContent>
		</Card>
	</div>
</template>
