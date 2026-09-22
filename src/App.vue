<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const navTabs = ['Overview', 'Sales', 'Customers', 'Settings']

const activeNav = computed({
  get: () => route.name,
  set: (name) => router.push({ name }),
})

const periodOptions = [
  { label: 'Last 7 days', value: '7d' },
  { label: 'Last 30 days', value: '30d' },
  { label: 'Last 90 days', value: '90d' },
]
const period = ref('30d')
</script>

<template>
  <div>
    <SNavbar title="Awesome Dashboard">
      <SSelect v-model="period" :options="periodOptions" />
      <SStatusDot label="Live" status="online" />
      <SAvatar alt="User avatar" size="36px" />
    </SNavbar>

    <div>
      <STabs v-model="activeNav" :tabs="navTabs" />

      <router-view />
    </div>
  </div>
</template>
