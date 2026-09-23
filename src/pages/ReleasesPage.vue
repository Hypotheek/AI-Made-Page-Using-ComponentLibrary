<script setup>
import { ref, computed } from 'vue'

const allReleases = [
  { title: 'Awesome Quest', releaseDate: '2023-10-06', released: 'Oct 2023', genre: 'Action-Adventure', platforms: ['PC', 'PS5'], score: 78, copiesSold: 0.8 },
  { title: 'Awesome Kart', releaseDate: '2024-04-09', released: 'Apr 2024', genre: 'Racing', platforms: ['PC', 'PS5', 'Switch'], score: 82, copiesSold: 1.3 },
  { title: 'Awesome Arena', releaseDate: '2024-10-08', released: 'Oct 2024', genre: 'Fighting', platforms: ['PC', 'PS5', 'Xbox'], score: 75, copiesSold: 0.9 },
  { title: 'Awesome: The Game', releaseDate: '2025-04-11', released: 'Apr 2025', genre: 'Open-World Adventure', platforms: ['PC', 'PS5', 'Xbox', 'Switch'], score: 88, copiesSold: 2.1 },
  { title: 'Platformer (Awesome Edition)', releaseDate: '2025-10-10', released: 'Oct 2025', genre: 'Platformer', platforms: ['PC', 'Switch'], score: 91, copiesSold: 1.7 },
  { title: 'Skate The Awesome', releaseDate: '2026-04-07', released: 'Apr 2026', genre: 'Sports / Skateboarding', platforms: ['PC', 'PS5', 'Xbox', 'Switch'], score: 85, copiesSold: 1.4 },
]

const recentReleases = allReleases.slice(-3)

const platformOptions = [
  { label: 'PC', value: 'PC' },
  { label: 'PS5', value: 'PS5' },
  { label: 'Xbox', value: 'Xbox' },
  { label: 'Switch', value: 'Switch' },
]

const platformSearch = ref('')
const selectedPlatforms = ref([])

const filteredPlatformOptions = computed(() =>
  platformOptions.filter((option) =>
    option.label.toLowerCase().includes(platformSearch.value.toLowerCase())
  )
)

const dateFrom = ref('')
const dateTo = ref('')

const filteredReleases = computed(() =>
  allReleases.filter((release) => {
    const matchesPlatform =
      selectedPlatforms.value.length === 0 ||
      release.platforms.some((platform) => selectedPlatforms.value.includes(platform))
    const afterFrom = !dateFrom.value || release.releaseDate >= dateFrom.value
    const beforeTo = !dateTo.value || release.releaseDate <= dateTo.value
    return matchesPlatform && afterFrom && beforeTo
  })
)

const historyColumns = ['title', 'released', 'genre', 'platforms', 'score', 'copiesSold']

const historyRows = computed(() =>
  filteredReleases.value.map((release) => ({
    title: release.title,
    released: release.released,
    genre: release.genre,
    platforms: release.platforms.join(', '),
    score: release.score,
    copiesSold: `${release.copiesSold}M`,
  }))
)
</script>

<template>
  <SStack gap="2.5em">
    <SStack gap="0.25em">
      <SHeading :level="1">Releases</SHeading>
      <SText variant="body">Every Awesome Studios title, bi-yearly since 2022.</SText>
    </SStack>

    <SStack gap="1em">
      <SHeading :level="2">Most Recent Releases</SHeading>
      <SGrid :columns="3" gap="1em">
        <SCard v-for="release in recentReleases" :key="release.title" :title="release.title">
          <SStack gap="0.75em">
            <SText variant="body">{{ release.genre }} · Released {{ release.released }}</SText>
            <SInline gap="0.5em">
              <STag v-for="platform in release.platforms" :key="platform">{{ platform }}</STag>
            </SInline>
            <SStat label="Critic Score" :value="release.score" />
          </SStack>
        </SCard>
      </SGrid>
    </SStack>

    <SDivider />

    <SStack gap="1em">
      <SHeading :level="2">Full Release History</SHeading>

      <SFlex gap="2em" wrap align="start">
        <SFormField label="Filter by platform">
          <SStack gap="0.5em">
            <SSearchInput v-model="platformSearch" placeholder="Search platforms..." />
            <SCheckboxGroup v-model="selectedPlatforms" :options="filteredPlatformOptions" />
            <SWrap v-if="selectedPlatforms.length" gap="0.4em">
              <STag v-for="platform in selectedPlatforms" :key="platform">{{ platform }}</STag>
            </SWrap>
          </SStack>
        </SFormField>

        <SFormField label="Released from">
          <SDatePicker v-model="dateFrom" />
        </SFormField>

        <SFormField label="Released to">
          <SDatePicker v-model="dateTo" />
        </SFormField>
      </SFlex>

      <STable :columns="historyColumns" :rows="historyRows" />
    </SStack>
  </SStack>
</template>
