<script setup lang="ts">
import { useIconColor } from '@/composables/colors';
import type { ActionComponent } from '@/schemas/action';
import { Button } from "@/components/ui/button"
import { Icon } from "@iconify/vue"

const props = defineProps<{
    action: ActionComponent
}>()

const { style } = useIconColor(() => props.action.color ?? 'slate')
</script>

<template>
    <Button
        size="sm"
        variant="outline"
	>
        <Icon v-if="action.icon" :icon="`lucide:${action.icon}`" :class="style.text" />
        {{ action.name }}
    </Button>
</template>