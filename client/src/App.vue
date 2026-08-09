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
