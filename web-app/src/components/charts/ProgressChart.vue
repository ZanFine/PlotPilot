<template>
  <ChartWrapper :option="chartOption" :height="height" :aria-label="`进度图表 - ${completed} 完成，共 ${total}`" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ChartWrapper from './ChartWrapper.vue'
import type { EChartsOption } from 'echarts'

const props = withDefaults(defineProps<{
  completed: number
  total: number
  height?: string
}>(), {
  height: '300px'
})

const chartOption = computed<EChartsOption>(() => ({
  title: {
    text: `${props.completed}/${props.total}`,
    left: 'center',
    top: 'center',
    textStyle: {
      fontSize: 24,
      fontWeight: 'bold'
    }
  },
  series: [
    {
      type: 'pie',
      radius: ['60%', '80%'],
      avoidLabelOverlap: false,
      label: {
        show: false
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      data: [
        { value: props.completed, name: '已完成', itemStyle: { color: '#10b981' } },
        { value: props.total - props.completed, name: '未完成', itemStyle: { color: '#e5e7eb' } }
      ]
    }
  ],
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c} ({d}%)'
  }
}))
</script>
