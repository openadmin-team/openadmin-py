<script setup lang="ts">
import { useOpenAdminSpec } from '@/composables/openadmin-spec';

const { data, isLoading } = useOpenAdminSpec()
</script>

<template>
	<h1>Hello</h1>
	{{ isLoading }}
	{{ data }}
</template>
