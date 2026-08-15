<script setup lang="ts">
import { useIconColor } from '@/composables/colors';
import type { Action } from '@/schemas/action';
import { Button } from "@/components/ui/button"
import { Icon } from "@iconify/vue"

const props = defineProps<{
    action: Action
}>()

const { style } = useIconColor('amber')
</script>

<template>
    <Button
        size="sm"
        :variant="action.color === 'red' ? 'destructive' : 'outline'"
        :class="style.text"
	>
        <Icon v-if="action.icon" :icon="action.icon" />
        {{ action.name }}
    </Button>
</template>