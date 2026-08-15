import type { MaybeRefOrGetter } from "vue"
import { usePageSpec } from "./openadmin-spec"

export const useStat = (params: {
    sectionId: MaybeRefOrGetter<string>
    pageId: MaybeRefOrGetter<string>
    actionId: MaybeRefOrGetter<string | undefined>
}) => {
    const {} = usePageSpec({sectionId, pageId})
}