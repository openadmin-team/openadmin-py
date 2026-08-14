<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->
<script setup lang="ts">
import "vue-sonner/style.css"
import { Toaster } from "@/components/ui/sonner"
</script>

<template>
	<main>
		<RouterView />
		<Toaster />
	</main>
</template>
