// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import type { Editor } from "@tiptap/vue-3"
import type { ShallowRef } from "vue"
import { ref, watch } from "vue"

export function useLinkImagePopovers(editor: ShallowRef<Editor | undefined>) {
	const linkPopoverOpen = ref(false)
	const linkUrl = ref("")

	watch(linkPopoverOpen, (open) => {
		if (open) linkUrl.value = (editor.value?.getAttributes("link").href as string | undefined) ?? ""
	})

	function applyLink() {
		const chain = editor.value?.chain().focus().extendMarkRange("link")
		if (!chain) return
		const url = linkUrl.value.trim()
		if (url) chain.setLink({ href: url }).run()
		else chain.unsetLink().run()
		linkPopoverOpen.value = false
	}

	function removeLink() {
		editor.value?.chain().focus().unsetLink().run()
		linkPopoverOpen.value = false
	}

	const imagePopoverOpen = ref(false)
	const imageUrl = ref("")
	const imageAlt = ref("")

	watch(imagePopoverOpen, (open) => {
		if (open) {
			imageUrl.value = ""
			imageAlt.value = ""
		}
	})

	function insertImage() {
		const src = imageUrl.value.trim()
		if (!src) return
		editor.value
			?.chain()
			.focus()
			.setImage({ src, alt: imageAlt.value.trim() || undefined })
			.run()
		imagePopoverOpen.value = false
	}

	return {
		linkPopoverOpen,
		linkUrl,
		applyLink,
		removeLink,
		imagePopoverOpen,
		imageUrl,
		imageAlt,
		insertImage,
	}
}
