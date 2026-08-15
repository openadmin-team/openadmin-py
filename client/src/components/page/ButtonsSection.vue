<script setup lang="ts">
import type { ActionComponent } from '@/schemas/action';
import type { FormComponent } from '@/schemas/form';

defineProps<{
    actions: ActionComponent[],
    forms: FormComponent[],
}>()
</script>

<template>
    <section>
        {{ actions }}
    {{ forms }}
    </section>
</template>