<template>
  <ChartWrapper :option="chartOption" :height="height" :aria-label="`${title} - 趋势图表`" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ChartWrapper from './ChartWrapper.vue'
import type { EChartsOption } from 'echarts'

interface TrendData {
  date: string
  value: number
}

const props = withDefaults(defineProps<{
  data: TrendData[]
  title?: string
  height?: string
}>(), {
  title: '趋势图',
  height: '400px'
})

const chartOption = computed<EChartsOption>(() => ({
  title: {
    text: props.title,
    left: 'center'
  },
  xAxis: {
    type: 'category',
    data: props.data.map(d => d.date)
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      type: 'line',
      data: props.data.map(d => d.value),
      smooth: true,
      itemStyle: {
        color: '#667eea'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
            { offset: 1, color: 'rgba(102, 126, 234, 0.05)' }
          ]
        }
      }
    }
  ],
  tooltip: {
    trigger: 'axis'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  }
}))
</script>
