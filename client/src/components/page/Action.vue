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
        :variant="action.color === 'red' ? 'destructive' : 'outline'"
        :class="style.text"
	>
        <Icon v-if="action.icon" :icon="action.icon" />
        {{ action.name }}
    </Button>
</template>