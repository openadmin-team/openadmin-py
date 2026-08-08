const DANGEROUS_TAGS = new Set(['SCRIPT', 'IFRAME', 'OBJECT', 'EMBED', 'STYLE'])

/** Minimal DOM-based sanitizer: strips script-like tags, event handler attrs, and javascript: URLs. */
export function sanitizeHtml(html: string): string {
  const doc = new DOMParser().parseFromString(html, 'text/html')

  const walk = (node: Element) => {
    for (const child of Array.from(node.children)) {
      if (DANGEROUS_TAGS.has(child.tagName)) {
        child.remove()
        continue
      }
      for (const attr of Array.from(child.attributes)) {
        const name = attr.name.toLowerCase()
        const value = attr.value.trim().toLowerCase()
        if (name.startsWith('on') || value.startsWith('javascript:')) {
          child.removeAttribute(attr.name)
        }
      }
      walk(child)
    }
  }

  walk(doc.body)
  return doc.body.innerHTML
}
