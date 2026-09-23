<script setup>
import { communityKpis, monthlyActivePlayersChart, revenueByPlatformChart } from '../data/studio'
</script>

<template>
  <SStack gap="2em">
    <SGrid :columns="4" gap="1em">
      <SKpiCard
        v-for="kpi in communityKpis"
        :key="kpi.label"
        :label="kpi.label"
        :value="kpi.value"
        :delta="kpi.delta ?? null"
        :trend="kpi.trend"
      />
    </SGrid>

    <SCard title="Monthly Active Players">
      <SLineChart :data="monthlyActivePlayersChart" />
    </SCard>

    <SCard title="Revenue by Platform ($M)">
      <SDonutChart :data="revenueByPlatformChart" centerLabel="Revenue" />
    </SCard>
  </SStack>
</template>
