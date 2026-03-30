<template>
  <ChartWrapper :option="chartOption" :height="height" :aria-label="`关系图表 - ${nodes.length} 个节点，${links.length} 个连接`" @click="handleNodeClick" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ChartWrapper from './ChartWrapper.vue'
import type { EChartsOption } from 'echarts'

interface GraphNode {
  id: string
  name: string
  category?: number
}

interface GraphLink {
  source: string
  target: string
  value?: number
}

const props = withDefaults(defineProps<{
  nodes: GraphNode[]
  links: GraphLink[]
  categories?: string[]
  height?: string
}>(), {
  height: '600px',
  categories: () => []
})

const emit = defineEmits<{
  nodeClick: [node: GraphNode]
}>()

const chartOption = computed<EChartsOption>(() => ({
  series: [
    {
      type: 'graph',
      layout: 'force',
      data: props.nodes,
      links: props.links,
      categories: props.categories.map((name, index) => ({ name })),
      roam: true,
      label: {
        show: true,
        position: 'right'
      },
      force: {
        repulsion: 100,
        edgeLength: 150
      },
      emphasis: {
        focus: 'adjacency',
        lineStyle: {
          width: 3
        }
      }
    }
  ],
  tooltip: {
    formatter: (params: any) => {
      if (params.dataType === 'node') {
        return `${params.data.name}`
      }
      return `${params.data.source} → ${params.data.target}`
    }
  }
}))

const handleNodeClick = (params: any) => {
  if (params.dataType === 'node') {
    emit('nodeClick', params.data)
  }
}
</script>
