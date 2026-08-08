export function humanize(name: string): string {
  const words = name.replace(/[_-]+/g, ' ').trim()
  if (!words) return name
  return words.charAt(0).toUpperCase() + words.slice(1)
}
