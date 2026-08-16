<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'
import { FlexRender, useTable as useTanStackTable } from '@tanstack/vue-table'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { features, type DataTableFeatures } from '@/lib/data-table'

const props = defineProps<{
  columns: ColumnDef<DataTableFeatures, TData>[]
  data: TData[]
}>()

const table = useTanStackTable({
  features,
  get data() { return props.data },
  get columns() { return props.columns },
})
</script>