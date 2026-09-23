<script setup>
import { computed } from 'vue'
import { revenueByTitle, revenueByPlatform, unitsShare, monthlyActivePlayers } from '../data/studioData.js'
import { matchesTitleFilters } from '../data/filters.js'

const filteredRevenueByTitle = computed(() => revenueByTitle.filter((r) => matchesTitleFilters(r.title)))
const filteredUnitsShare = computed(() => unitsShare.filter((u) => matchesTitleFilters(u.label)))

const totalRevenue = computed(() => filteredRevenueByTitle.value.reduce((sum, r) => sum + r.value, 0))
const totalUnits = computed(() => filteredUnitsShare.value.reduce((sum, u) => sum + u.value, 0))
const avgRevenuePerUnit = computed(() =>
  totalUnits.value ? (totalRevenue.value / totalUnits.value).toFixed(2) : '0.00'
)
const bestSeller = computed(() => {
  if (!filteredRevenueByTitle.value.length) return '—'
  return filteredRevenueByTitle.value.reduce((a, b) => (b.value > a.value ? b : a)).title
})

const salesKpis = computed(() => [
  { label: 'Filtered Revenue', value: `$${totalRevenue.value.toFixed(1)}M`, delta: null, trend: [] },
  { label: 'Filtered Units Sold', value: `${totalUnits.value.toFixed(1)}M`, delta: null, trend: [] },
  { label: 'Avg. Revenue / Unit', value: `$${avgRevenuePerUnit.value}`, delta: null, trend: [] },
  { label: 'Best Seller', value: bestSeller.value, delta: null, trend: [] },
])
</script>

<template>
  <SStack gap="2em">
    <SAutoGrid min-width="220px" gap="1em">
      <SKpiCard
        v-for="kpi in salesKpis"
        :key="kpi.label"
        :label="kpi.label"
        :value="kpi.value"
        :delta="kpi.delta"
        :trend="kpi.trend"
        up-is-good
      />
    </SAutoGrid>

    <SGrid :columns="2" gap="1em">
      <SCard title="Revenue by Title ($M)">
        <SEmpty v-if="!filteredRevenueByTitle.length" text="No titles match the current filters" />
        <SBarChart v-else :data="filteredRevenueByTitle" />
      </SCard>
      <SCard title="Revenue by Platform ($M)">
        <SText variant="body">Across all titles</SText>
        <SHorizontalBar :data="revenueByPlatform" />
      </SCard>
    </SGrid>

    <SGrid :columns="2" gap="1em">
      <SCard title="Units Sold Share (M)">
        <SEmpty v-if="!filteredUnitsShare.length" text="No titles match the current filters" />
        <SDonutChart v-else :data="filteredUnitsShare" center-label="Filtered Units" />
      </SCard>
      <SCard title="Monthly Active Players">
        <SText variant="body">Across all titles</SText>
        <SLineChart :data="monthlyActivePlayers" />
      </SCard>
    </SGrid>
  </SStack>
</template>
