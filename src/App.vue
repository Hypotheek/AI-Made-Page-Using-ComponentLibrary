<script setup>
import { ref, computed } from 'vue'
import OverviewView from './views/OverviewView.vue'
import SalesView from './views/SalesView.vue'
import ReleasesView from './views/ReleasesView.vue'
import CommunityView from './views/CommunityView.vue'
import TitleFilter from './components/TitleFilter.vue'
import DateRangeFilter from './components/DateRangeFilter.vue'

const routes = {
  overview: { component: OverviewView, label: 'Overview', title: 'Overview' },
  sales: { component: SalesView, label: 'Sales & Revenue', title: 'Sales & Revenue' },
  releases: { component: ReleasesView, label: 'Releases', title: 'Releases' },
  community: { component: CommunityView, label: 'Community & Reviews', title: 'Community & Reviews' },
}

function routeFromHash() {
  const key = window.location.hash.replace('#/', '')
  return routes[key] ? key : 'overview'
}

const currentRoute = ref(routeFromHash())

window.addEventListener('hashchange', () => {
  currentRoute.value = routeFromHash()
})

function navigate(key) {
  window.location.hash = `#/${key}`
  currentRoute.value = key
}

const sidebarItems = Object.entries(routes).map(([value, r]) => ({ label: r.label, value }))
const currentView = computed(() => routes[currentRoute.value].component)
const currentTitle = computed(() => routes[currentRoute.value].title)
</script>

<template>
  <SFlex align="stretch">
    <SSidebar :items="sidebarItems" :model-value="currentRoute" @update:model-value="navigate" />

    <SFill>
      <SPad size="2em">
        <SStack gap="2em">
          <SFlex justify="space-between" align="center" wrap>
            <div>
              <SHeading :level="1">Awesome Studios</SHeading>
              <SText variant="body">{{ currentTitle }} dashboard &mdash; bi-yearly video game releases</SText>
            </div>
            <SBadge variant="success">Bi-yearly release cadence</SBadge>
          </SFlex>

          <SCard title="Filters">
            <SFlex gap="2em" wrap align="start">
              <TitleFilter />
              <DateRangeFilter />
            </SFlex>
          </SCard>

          <component :is="currentView" />
        </SStack>
      </SPad>
    </SFill>
  </SFlex>
</template>
