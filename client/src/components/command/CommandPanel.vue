<script setup lang="ts">
import { useSpec } from '@/composables/openadmin-spec';

const { data } = useSpec();
</script>

<template>
    {{ data }}
</template>