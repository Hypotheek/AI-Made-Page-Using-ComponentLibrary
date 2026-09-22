<script setup>
const salesTrend = [8, 9, 7, 11, 13, 12, 15, 17]
const dealsTrend = [2, 3, 3, 4, 3, 5, 6, 5]

const salesByMonth = [
  { label: 'Jan', value: 12000 },
  { label: 'Feb', value: 15800 },
  { label: 'Mar', value: 14100 },
  { label: 'Apr', value: 18900 },
  { label: 'May', value: 21200 },
  { label: 'Jun', value: 24700 },
]

const salesByRegion = [
  { label: 'North America', value: 48200 },
  { label: 'Europe', value: 31400 },
  { label: 'APAC', value: 22100 },
  { label: 'LatAm', value: 9800 },
]

const dealColumns = ['deal', 'rep', 'value', 'stage']
const dealRows = [
  { deal: 'Acme Corp', rep: 'Ada Lovelace', value: '$24,000', stage: '🟢 Closed Won' },
  { deal: 'Initech', rep: 'Grace Hopper', value: '$9,500', stage: '🟡 Negotiation' },
  { deal: 'Globex', rep: 'Alan Turing', value: '$41,000', stage: '🟢 Closed Won' },
  { deal: 'Umbrella Co', rep: 'Margaret Hamilton', value: '$6,200', stage: '🔴 Closed Lost' },
  { deal: 'Soylent Inc', rep: 'Katherine Johnson', value: '$17,800', stage: '🟡 Negotiation' },
]
</script>

<template>
  <div>
    <SHeading :level="1">Sales</SHeading>

    <SGrid :columns="3" gap="1.25em">
      <SKpiCard label="Sales this quarter" value="$106.8k" :delta="18.2" :trend="salesTrend" up-is-good />
      <SKpiCard label="Deals closed" value="34" :delta="9.5" :trend="dealsTrend" up-is-good />
      <SKpiCard label="Avg. deal size" value="$3,140" :delta="4.1" up-is-good />
    </SGrid>

    <SGrid :columns="2" gap="1.25em">
      <SCard title="Sales over time">
        <SLineChart :data="salesByMonth" />
      </SCard>
      <SCard title="Sales by region">
        <SBarChart :data="salesByRegion" />
      </SCard>
    </SGrid>

    <SCard title="Pipeline">
      <STable :columns="dealColumns" :rows="dealRows" />
    </SCard>
  </div>
</template>
