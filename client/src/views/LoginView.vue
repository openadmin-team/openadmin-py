<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { computed, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useLogin } from "@/composables/auth"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"

const router = useRouter()
const route = useRoute()

const username = ref("")
const password = ref("")

const login = useLogin()

const errorMessage = computed(() => {
	if (!login.error.value) return null
	return login.error.value.status === 401
		? "Invalid username or password"
		: login.error.value.message
})

function onSubmit() {
	login.mutate(
		{ username: username.value, password: password.value },
		{
			onSuccess: () => {
				const redirect = typeof route.query.redirect === "string" ? route.query.redirect : "/"
				router.push(redirect)
			},
		},
	)
}
</script>

<template>
	<div class="flex min-h-svh items-center justify-center bg-background px-4">
		<Card class="w-full max-w-sm">
			<CardHeader>
				<CardTitle>Sign in</CardTitle>
				<CardDescription>Enter your credentials to access the admin panel</CardDescription>
			</CardHeader>
			<CardContent>
				<form class="grid gap-6" @submit.prevent="onSubmit">
					<FieldGroup>
						<Field>
							<FieldLabel for="username">Username</FieldLabel>
							<Input
								id="username"
								v-model="username"
								autocomplete="username"
								:aria-invalid="Boolean(errorMessage)"
								required
							/>
						</Field>
						<Field>
							<FieldLabel for="password">Password</FieldLabel>
							<Input
								id="password"
								v-model="password"
								type="password"
								autocomplete="current-password"
								:aria-invalid="Boolean(errorMessage)"
								required
							/>
						</Field>
						<FieldError v-if="errorMessage">{{ errorMessage }}</FieldError>
						<Button type="submit" :disabled="login.isPending.value" class="w-full">
							{{ login.isPending.value ? "Signing in…" : "Sign in" }}
						</Button>
					</FieldGroup>
				</form>
			</CardContent>
		</Card>
	</div>
</template>
