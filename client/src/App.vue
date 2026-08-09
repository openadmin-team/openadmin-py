<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { useOpenAdminSpec } from "@/composables/openadmin-spec"

const { data, isLoading, error } = useOpenAdminSpec()
</script>

<template>
	<h1>Hello</h1>
	{{ isLoading }}
	{{ JSON.stringify(data) }}
	{{ error?.message }}
</template>
