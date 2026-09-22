<script setup>
import { ref } from 'vue'

const search = ref('')
const page = ref(1)

const recentCustomers = [
  { name: 'Ada L' },
  { name: 'Grace H' },
  { name: 'Alan T' },
  { name: 'Margaret H' },
  { name: 'Katherine J' },
]

const customerColumns = ['name', 'company', 'plan', 'status']
const customerRows = [
  { name: 'Ada Lovelace', company: 'Acme Corp', plan: 'Enterprise', status: '🟢 Active' },
  { name: 'Grace Hopper', company: 'Initech', plan: 'Pro', status: '🟢 Active' },
  { name: 'Alan Turing', company: 'Globex', plan: 'Enterprise', status: '🟢 Active' },
  { name: 'Margaret Hamilton', company: 'Umbrella Co', plan: 'Free', status: '🔴 Churned' },
  { name: 'Katherine Johnson', company: 'Soylent Inc', plan: 'Pro', status: '🟡 Trial' },
]
</script>

<template>
  <div>
    <SHeading :level="1">Customers</SHeading>

    <SGrid :columns="3" gap="1.25em">
      <SKpiCard label="Total customers" value="8,412" :delta="6.3" up-is-good />
      <SKpiCard label="New this month" value="312" :delta="14.7" up-is-good />
      <SKpiCard label="Churn rate" value="1.2%" :delta="-0.4" :up-is-good="false" />
    </SGrid>

    <SCard title="Recently active">
      <SAvatarGroup :avatars="recentCustomers" :max="5" size="40px" />
    </SCard>

    <SCard title="Support SLA compliance">
      <SMeter label="Tickets resolved within SLA" :max="100" :value="94" />
    </SCard>

    <SCard title="All customers">
      <SSearchInput v-model="search" placeholder="Search customers..." />
      <STable :columns="customerColumns" :rows="customerRows" />
      <SPagination v-model="page" :page-count="6" />
    </SCard>
  </div>
</template>
