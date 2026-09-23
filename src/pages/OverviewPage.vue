<script setup>
const kpis = [
  {
    label: 'Total Games Released',
    value: 6,
    period: 'since 2022 (studio founded)',
    trend: [1, 2, 3, 4, 5, 6],
  },
  {
    label: 'Lifetime Copies Sold',
    value: '8.2M',
    delta: -18,
    period: 'latest vs previous title',
    trend: [0.8, 1.3, 0.9, 2.1, 1.7, 1.4],
    upIsGood: true,
  },
  {
    label: 'Avg Critic Score',
    value: 83,
    delta: 2,
    period: 'latest title vs studio avg',
    trend: [78, 82, 75, 88, 91, 85],
    upIsGood: true,
  },
  {
    label: 'Next Release',
    value: 'Oct 2026',
    period: 'bi-yearly cadence',
  },
  {
    label: 'Critic Reviews',
    value: 6,
    period: 'across 6 press outlets',
  },
]

const salesData = [
  { label: 'Awesome Quest', value: 0.8 },
  { label: 'Awesome Kart', value: 1.3 },
  { label: 'Awesome Arena', value: 0.9 },
  { label: 'Awesome: The Game', value: 2.1 },
  { label: 'Platformer (Awesome Edition)', value: 1.7 },
  { label: 'Skate The Awesome', value: 1.4 },
]

const scoreData = [
  { label: 'Awesome Quest', value: 78 },
  { label: 'Awesome Kart', value: 82 },
  { label: 'Awesome Arena', value: 75 },
  { label: 'Awesome: The Game', value: 88 },
  { label: 'Platformer (Awesome Edition)', value: 91 },
  { label: 'Skate The Awesome', value: 85 },
]
</script>

<template>
  <SStack gap="2.5em">
    <SStack gap="0.25em">
      <SHeading :level="1">Awesome Studios</SHeading>
      <SText variant="body">Bi-yearly release performance across all titles since 2022.</SText>
    </SStack>

    <SAutoGrid minWidth="220px" gap="1em">
      <SKpiCard v-for="kpi in kpis" :key="kpi.label" v-bind="kpi" />
    </SAutoGrid>

    <SDivider />

    <SGrid :columns="2" gap="2em">
      <SCard title="Copies Sold per Release (millions)">
        <SBarChart :data="salesData" />
      </SCard>
      <SCard title="Critic Score Trend">
        <SLineChart :data="scoreData" />
      </SCard>
    </SGrid>
  </SStack>
</template>
