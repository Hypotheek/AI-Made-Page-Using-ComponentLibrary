<script setup>
import { computed } from 'vue'
import { overviewKpis, revenueByTitle, monthlyActivePlayers, releases } from '../data/studioData.js'
import { matchesTitleFilters } from '../data/filters.js'

const filteredRevenueByTitle = computed(() => revenueByTitle.filter((r) => matchesTitleFilters(r.title)))
const filteredReleases = computed(() => releases.filter((r) => matchesTitleFilters(r.title)))
</script>

<template>
  <SStack gap="2em">
    <SAutoGrid min-width="220px" gap="1em">
      <SKpiCard
        v-for="kpi in overviewKpis"
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
      <SCard title="Monthly Active Players">
        <SLineChart :data="monthlyActivePlayers" />
      </SCard>
    </SGrid>

    <SCard title="At a Glance">
      <SEmpty v-if="!filteredReleases.length" text="No titles match the current filters" />
      <SGrid v-else :columns="3" gap="1em">
        <SFlex v-for="r in filteredReleases" :key="r.title" justify="space-between" align="center">
          <SText variant="body"><strong>{{ r.title }}</strong></SText>
          <SBadge variant="success">{{ r.status }}</SBadge>
        </SFlex>
      </SGrid>
    </SCard>
  </SStack>
</template>
