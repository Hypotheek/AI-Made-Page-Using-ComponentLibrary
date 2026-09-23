<script setup>
import { overviewKpis, ratingHistoryChart, recentReleases } from '../data/studio'

const releaseColumns = ['Title', 'Genre', 'Released', 'Rating']
const recentReleaseRows = recentReleases.map((r) => ({
  Title: r.title,
  Genre: r.genre,
  Released: r.released,
  Rating: `${r.rating} / 10`,
}))
</script>

<template>
  <SStack gap="2em">
    <SGrid :columns="4" gap="1em">
      <SKpiCard
        v-for="kpi in overviewKpis"
        :key="kpi.label"
        :label="kpi.label"
        :value="kpi.value"
        :delta="kpi.delta ?? null"
        :trend="kpi.trend"
      />
    </SGrid>

    <SCard title="Rating by Release (All Time)">
      <SBarChart :data="ratingHistoryChart" />
    </SCard>

    <SCard title="Most Recent Releases">
      <STable :columns="releaseColumns" :rows="recentReleaseRows" />
    </SCard>
  </SStack>
</template>
