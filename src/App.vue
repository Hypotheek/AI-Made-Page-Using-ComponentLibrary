<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const tabs = ['Overview', 'Releases', 'Reviews', 'Players']

function tabFromHash() {
  const h = decodeURIComponent(window.location.hash.slice(1))
  return tabs.includes(h) ? h : tabs[0]
}

const activeTab = ref(tabFromHash())

function onHashChange() {
  activeTab.value = tabFromHash()
}

onMounted(() => window.addEventListener('hashchange', onHashChange))
onUnmounted(() => window.removeEventListener('hashchange', onHashChange))

watch(activeTab, (val) => {
  if (decodeURIComponent(window.location.hash.slice(1)) !== val) {
    window.location.hash = val
  }
})

const subtitles = {
  Overview: 'Company-wide performance across the three most recent releases.',
  Releases: 'Release cadence, roadmap, and title-by-title breakdown.',
  Reviews: 'Critic reception across recent releases.',
  Players: 'Engagement, retention, and audience breakdown.',
}

// ---------- Overview ----------
const kpis = [
  { label: 'Total Revenue', value: '$85.4M', delta: 18, period: 'vs prior half', trend: [22, 26, 28, 31, 38, 44] },
  { label: 'Copies Sold', value: '2.15M', delta: 9, period: 'vs prior half', trend: [1.2, 1.4, 1.6, 1.8, 2.0, 2.15] },
  { label: 'Monthly Active Players', value: '480K', delta: 22, period: 'vs prior half', trend: [280, 310, 340, 390, 430, 480] },
  { label: 'Average Rating', value: '4.3 / 5', delta: 2, period: 'vs prior half', trend: [4.1, 4.1, 4.2, 4.2, 4.3, 4.3] },
]

const revenueByHalf = [
  { label: 'H1 2024', value: 9 },
  { label: 'H2 2024', value: 14 },
  { label: 'H1 2025', value: 22 },
  { label: 'H2 2025', value: 31 },
  { label: 'H1 2026', value: 38 },
  { label: 'H2 2026', value: 44 },
]

const revenueByGame = [
  { label: 'Awesome: The Game', value: 54, releasedDate: '2025-08-15' },
  { label: 'Platformer (Awesome Edition)', value: 19, releasedDate: '2026-02-10' },
  { label: 'Skate The Awesome', value: 12, releasedDate: '2026-08-20' },
]

const copiesByPlatform = [
  { label: 'PC', value: 1.1 },
  { label: 'PlayStation', value: 0.85 },
  { label: 'Xbox', value: 0.6 },
  { label: 'Switch', value: 0.4 },
]

// ---------- Releases ----------
const releaseColumns = ['title', 'released', 'platforms', 'copiesSold', 'revenue', 'rating']

const releases = [
  {
    title: 'Skate The Awesome',
    released: 'Aug 2026',
    releasedDate: '2026-08-20',
    platforms: 'PS5, Xbox, PC',
    copiesSold: '310K',
    revenue: '$12M',
    rating: '4.1 / 5',
  },
  {
    title: 'Platformer (Awesome Edition)',
    released: 'Feb 2026',
    releasedDate: '2026-02-10',
    platforms: 'Switch, PC',
    copiesSold: '640K',
    revenue: '$19M',
    rating: '4.3 / 5',
  },
  {
    title: 'Awesome: The Game',
    released: 'Aug 2025',
    releasedDate: '2025-08-15',
    platforms: 'PC, PS5, Xbox',
    copiesSold: '1.2M',
    revenue: '$54M',
    rating: '4.6 / 5',
  },
]

const allTitles = releases.map((r) => r.title)

const roadmapSteps = [
  { title: 'Awesome: The Game', description: 'Launched Aug 2025' },
  { title: 'Platformer (Awesome Edition)', description: 'Launched Feb 2026' },
  { title: 'Skate The Awesome', description: 'Launched Aug 2026' },
  { title: 'Untitled Awesome Project', description: 'Targeting Feb 2027' },
]

const nextReleaseTarget = new Date('2027-02-15T00:00:00Z').getTime()

// ---------- Reviews ----------
const reviews = [
  {
    title: 'Awesome: The Game',
    releasedDate: '2025-08-15',
    tier: 'Universal Acclaim',
    tagColor: 'green',
    score: 91,
    critics: [
      {
        reviewer: 'Maria Chen',
        outlet: 'GameSpire',
        rating: 5,
        quote: 'A genre-defining triumph, deep systems wrapped in gorgeous art direction.',
      },
      {
        reviewer: 'Devon Ruiz',
        outlet: 'PixelPress',
        rating: 4,
        quote: "Occasional pacing issues can't dampen an otherwise phenomenal ride.",
      },
    ],
  },
  {
    title: 'Platformer (Awesome Edition)',
    releasedDate: '2026-02-10',
    tier: 'Generally Favorable',
    tagColor: 'blue',
    score: 82,
    critics: [
      {
        reviewer: 'Sam Okafor',
        outlet: 'JumpButton',
        rating: 4,
        quote: 'Precise, joyful platforming with clever level design throughout.',
      },
      {
        reviewer: 'Priya Nair',
        outlet: 'RetroWire',
        rating: 4,
        quote: "A loving tribute to the genre's classics, with just enough new ideas.",
      },
    ],
  },
  {
    title: 'Skate The Awesome',
    releasedDate: '2026-08-20',
    tier: 'Mixed or Average',
    tagColor: 'gray',
    score: 74,
    critics: [
      {
        reviewer: 'Jonah Lee',
        outlet: 'BoardCred',
        rating: 3,
        quote: 'Fun trick tech held back by a shallow career mode.',
      },
      {
        reviewer: 'Maria Chen',
        outlet: 'GameSpire',
        rating: 4,
        quote: 'The best skating feels this generation, even if the content is thin.',
      },
    ],
  },
]

// ---------- Filters (Titles + Release Date Range) ----------
const titleSearch = ref('')
const selectedTitles = ref(allTitles.slice())

const titleOptions = computed(() =>
  allTitles
    .filter((t) => t.toLowerCase().includes(titleSearch.value.toLowerCase()))
    .map((t) => ({ label: t, value: t }))
)

const dateFrom = ref('2025-01-01')
const dateTo = ref('2026-12-31')

function inRange(dateStr) {
  return dateStr >= dateFrom.value && dateStr <= dateTo.value
}

const filteredReleases = computed(() =>
  releases.filter((r) => selectedTitles.value.includes(r.title) && inRange(r.releasedDate))
)

const filteredReviews = computed(() =>
  reviews.filter((g) => selectedTitles.value.includes(g.title) && inRange(g.releasedDate))
)

const filteredRevenueByGame = computed(() =>
  revenueByGame.filter((g) => selectedTitles.value.includes(g.label) && inRange(g.releasedDate))
)

function resetFilters() {
  titleSearch.value = ''
  selectedTitles.value = allTitles.slice()
  dateFrom.value = '2025-01-01'
  dateTo.value = '2026-12-31'
}

// ---------- Players ----------
const playerKpis = [
  { label: 'Monthly Active Players', value: '480K', delta: 22, period: 'vs prior half', trend: [280, 310, 340, 390, 430, 480] },
  { label: 'Daily Active Players', value: '96K', delta: 15, period: 'vs prior half', trend: [58, 64, 71, 80, 88, 96] },
  { label: 'Avg Session Length', value: '38 min', delta: 5, period: 'vs prior half', trend: [31, 33, 34, 35, 37, 38] },
  { label: 'Day-30 Retention', value: '47%', delta: 6, period: 'vs prior half', trend: [36, 38, 40, 42, 45, 47] },
]

const playersByRegion = [
  { label: 'North America', value: 190 },
  { label: 'Europe', value: 150 },
  { label: 'Asia-Pacific', value: 110 },
  { label: 'Latin America', value: 30 },
]

const engagementProfile = [
  { label: 'Combat', value: 82 },
  { label: 'Exploration', value: 74 },
  { label: 'Social', value: 65 },
  { label: 'Customization', value: 70 },
  { label: 'Progression', value: 88 },
]

const heatmapRowLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const heatmapColLabels = ['9a', '12p', '3p', '6p', '9p']
const heatmapData = [
  [2, 3, 4, 6, 7],
  [2, 3, 4, 6, 7],
  [2, 3, 4, 6, 8],
  [2, 3, 4, 7, 8],
  [3, 3, 5, 8, 9],
  [4, 5, 6, 9, 10],
  [4, 5, 6, 9, 9],
]
</script>

<template>
  <div style="max-width: 1100px; margin: 0 auto; padding: 2em; display: flex; flex-direction: column; gap: 2em;">
    <div style="display: flex; align-items: center; gap: 1em;">
      <SHeading :level="1">Awesome Studios</SHeading>
      <SChip>Bi-yearly release cadence</SChip>
    </div>

    <STabs v-model="activeTab" :tabs="tabs" />
    <SText variant="body">{{ subtitles[activeTab] }}</SText>

    <SCard title="Filters">
      <SGrid :columns="2" gap="1.5em">
        <SFormField label="Titles" hint="Search and check the titles to include">
          <div style="display: flex; flex-direction: column; gap: 0.5em;">
            <SSearchInput v-model="titleSearch" placeholder="Search titles..." />
            <SCheckboxGroup v-model="selectedTitles" :options="titleOptions" />
          </div>
        </SFormField>
        <SFormField label="Release Date Range" hint="Limits releases, reviews, and revenue by title">
          <div style="display: flex; align-items: center; gap: 0.75em;">
            <SDatePicker v-model="dateFrom" />
            <SText variant="body">to</SText>
            <SDatePicker v-model="dateTo" />
          </div>
        </SFormField>
      </SGrid>
      <div style="margin-top: 1em;">
        <SButton variant="secondary" @click="resetFilters">Reset filters</SButton>
      </div>
    </SCard>

    <template v-if="activeTab === 'Overview'">
      <SGrid :columns="4" gap="1em">
        <SKpiCard
          v-for="kpi in kpis"
          :key="kpi.label"
          :label="kpi.label"
          :value="kpi.value"
          :delta="kpi.delta"
          :period="kpi.period"
          :trend="kpi.trend"
          up-is-good
        />
      </SGrid>

      <SGrid :columns="2" gap="1em">
        <SCard title="Revenue by Release Half">
          <SLineChart :data="revenueByHalf" />
        </SCard>
        <SCard title="Revenue Share by Title ($M)">
          <SDonutChart v-if="filteredRevenueByGame.length" :data="filteredRevenueByGame" center-label="Revenue ($M)" />
          <SEmpty v-else text="No titles match the current filters" />
        </SCard>
      </SGrid>

      <SCard title="Copies Sold by Platform (M)">
        <SBarChart :data="copiesByPlatform" />
      </SCard>
    </template>

    <template v-else-if="activeTab === 'Releases'">
      <SCard title="Release Roadmap">
        <SVerticalSteps :model-value="3" :steps="roadmapSteps" />
      </SCard>

      <SGrid :columns="2" gap="1em">
        <SCard title="Most Recent Releases">
          <STable v-if="filteredReleases.length" :columns="releaseColumns" :rows="filteredReleases" />
          <SEmpty v-else text="No releases match the current filters" />
        </SCard>
        <SCard title="Next Release Countdown">
          <div style="display: flex; flex-direction: column; gap: 0.5em;">
            <SText variant="body">Untitled Awesome Project, targeting Feb 2027</SText>
            <SCountdown :target="nextReleaseTarget" />
          </div>
        </SCard>
      </SGrid>
    </template>

    <template v-else-if="activeTab === 'Reviews'">
      <SCard title="Critic Reviews">
        <SGrid v-if="filteredReviews.length" :columns="3" gap="1.5em">
          <div v-for="game in filteredReviews" :key="game.title" style="display: flex; flex-direction: column; gap: 0.75em;">
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 0.5em;">
              <SText variant="body"><strong>{{ game.title }}</strong></SText>
              <STag :color="game.tagColor">{{ game.tier }}</STag>
            </div>
            <SGauge label="Critic Score" :value="game.score" :max="100" unit="/100" />
            <div
              v-for="critic in game.critics"
              :key="critic.outlet"
              style="display: flex; gap: 0.75em; align-items: flex-start; border-top: 1px solid #e5e7eb; padding-top: 0.75em;"
            >
              <SAvatar :alt="critic.reviewer" size="36px" />
              <div style="display: flex; flex-direction: column; gap: 0.25em;">
                <div style="display: flex; align-items: center; gap: 0.5em; flex-wrap: wrap;">
                  <SText variant="body"><strong>{{ critic.reviewer }}</strong></SText>
                  <SText variant="body">{{ critic.outlet }}</SText>
                </div>
                <SRating :max="5" :model-value="critic.rating" />
                <SText variant="body">&ldquo;{{ critic.quote }}&rdquo;</SText>
              </div>
            </div>
          </div>
        </SGrid>
        <SEmpty v-else text="No reviews match the current filters" />
      </SCard>
    </template>

    <template v-else-if="activeTab === 'Players'">
      <SGrid :columns="4" gap="1em">
        <SKpiCard
          v-for="kpi in playerKpis"
          :key="kpi.label"
          :label="kpi.label"
          :value="kpi.value"
          :delta="kpi.delta"
          :period="kpi.period"
          :trend="kpi.trend"
          up-is-good
        />
      </SGrid>

      <SGrid :columns="2" gap="1em">
        <SCard title="Monthly Active Players by Region (K)">
          <SHorizontalBar :data="playersByRegion" />
        </SCard>
        <SCard title="Day-30 Retention">
          <div style="display: flex; align-items: center; justify-content: center; padding: 1em;">
            <SRadialProgress :value="47" size="140px">47%</SRadialProgress>
          </div>
        </SCard>
      </SGrid>

      <SGrid :columns="2" gap="1em">
        <SCard title="Player Engagement Profile">
          <SRadarChart :data="engagementProfile" :max="100" />
        </SCard>
        <SCard title="Weekly Engagement Heatmap">
          <SHeatmap :data="heatmapData" :row-labels="heatmapRowLabels" :col-labels="heatmapColLabels" />
        </SCard>
      </SGrid>
    </template>
  </div>
</template>
