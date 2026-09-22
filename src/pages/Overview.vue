<script setup>
const revenueTrend = [3, 5, 4, 8, 7, 11, 9, 12]
const usersTrend = [10, 12, 11, 14, 16, 15, 18, 20]
const ordersTrend = [4, 4, 6, 5, 7, 6, 8, 7]
const churnTrend = [2, 3, 2, 2, 1, 2, 1, 1]

const revenueByMonth = [
  { label: 'Jan', value: 4200 },
  { label: 'Feb', value: 6800 },
  { label: 'Mar', value: 5400 },
  { label: 'Apr', value: 7300 },
  { label: 'May', value: 8100 },
  { label: 'Jun', value: 9600 },
]

const trafficBySource = [
  { label: 'Organic', value: 4300 },
  { label: 'Referral', value: 1800 },
  { label: 'Social', value: 2100 },
  { label: 'Paid', value: 1500 },
]

const plansBreakdown = [
  { label: 'Free', value: 420 },
  { label: 'Pro', value: 210 },
  { label: 'Enterprise', value: 95 },
]

const orderColumns = ['id', 'customer', 'amount', 'status']
const orderRows = [
  { id: '#3021', customer: 'Ada Lovelace', amount: '$482.00', status: '🟢 Paid' },
  { id: '#3020', customer: 'Grace Hopper', amount: '$129.50', status: '🟡 Pending' },
  { id: '#3019', customer: 'Alan Turing', amount: '$998.00', status: '🟢 Paid' },
  { id: '#3018', customer: 'Margaret Hamilton', amount: '$64.20', status: '🔴 Refunded' },
  { id: '#3017', customer: 'Katherine Johnson', amount: '$310.00', status: '🟢 Paid' },
]

const activity = [
  { label: 'New order #3021 from Ada Lovelace', date: 'Just now' },
  { label: 'Server deployment completed', date: '2h ago' },
  { label: 'Payout of $12,400 sent', date: '5h ago' },
  { label: 'New signup: Katherine Johnson', date: 'Yesterday' },
]
</script>

<template>
  <div>
    <SHeading :level="1">Overview</SHeading>

    <SGrid :columns="4" gap="1.25em">
      <SKpiCard label="Revenue" value="$48.2k" :delta="12" :trend="revenueTrend" up-is-good />
      <SKpiCard label="Active Users" value="8,412" :delta="8.4" :trend="usersTrend" up-is-good />
      <SKpiCard label="Orders" value="1,204" :delta="3.1" :trend="ordersTrend" up-is-good />
      <SKpiCard label="Churn" value="1.2%" :delta="-0.4" :trend="churnTrend" :up-is-good="false" />
    </SGrid>

    <SGrid :columns="2" gap="1.25em">
      <SCard title="Revenue over time">
        <SLineChart :data="revenueByMonth" />
      </SCard>
      <SCard title="Plan breakdown">
        <SDonutChart :data="plansBreakdown" center-label="Total" />
      </SCard>
    </SGrid>

    <SGrid :columns="2" gap="1.25em">
      <SCard title="Traffic by source">
        <SBarChart :data="trafficBySource" />
      </SCard>
      <SCard title="Recent activity">
        <STimeline :items="activity">
          <template #default="{ item }">
            <SText>{{ item.label }} — {{ item.date }}</SText>
          </template>
        </STimeline>
      </SCard>
    </SGrid>

    <SCard title="Recent orders">
      <STable :columns="orderColumns" :rows="orderRows" />
    </SCard>

    <SGrid :columns="3" gap="1.25em">
      <SCard title="Storage used">
        <SProgress :value="72" />
      </SCard>
      <SCard title="Monthly goal">
        <SProgress :value="48" />
      </SCard>
      <SCard title="Support tickets closed">
        <SProgress :value="91" />
      </SCard>
    </SGrid>
  </div>
</template>
