<script setup>
import { ref, computed } from 'vue'
import { releases } from '../data/studio'

const genreOptions = [...new Set(releases.map((r) => r.genre))].sort().map((g) => ({ label: g, value: g }))

const genreSearch = ref('')
const selectedGenres = ref([])
const dateFrom = ref('')
const dateTo = ref('')

const filteredGenreOptions = computed(() =>
  genreOptions.filter((o) => o.label.toLowerCase().includes(genreSearch.value.toLowerCase())),
)

const filteredReleases = computed(() =>
  releases.filter((r) => {
    const genreMatch = selectedGenres.value.length === 0 || selectedGenres.value.includes(r.genre)
    const fromMatch = !dateFrom.value || r.released >= dateFrom.value
    const toMatch = !dateTo.value || r.released <= dateTo.value
    return genreMatch && fromMatch && toMatch
  }),
)

const releaseColumns = ['Title', 'Genre', 'Released', 'Platforms', 'Rating']
const releaseRows = computed(() =>
  filteredReleases.value.map((r) => ({
    Title: r.title,
    Genre: r.genre,
    Released: r.released,
    Platforms: r.platforms,
    Rating: `${r.rating} / 10`,
  })),
)

const genreDistribution = computed(() => {
  const counts = {}
  for (const r of filteredReleases.value) counts[r.genre] = (counts[r.genre] || 0) + 1
  return Object.entries(counts).map(([label, value]) => ({ label, value }))
})

function clearFilters() {
  genreSearch.value = ''
  selectedGenres.value = []
  dateFrom.value = ''
  dateTo.value = ''
}
</script>

<template>
  <SStack gap="2em">
    <SCard title="Filters">
      <SStack gap="1.5em">
        <SFormField label="Genre">
          <SStack gap="0.5em">
            <SSearchInput v-model="genreSearch" placeholder="Search genres..." />
            <SCheckboxGroup v-model="selectedGenres" :options="filteredGenreOptions" />
          </SStack>
        </SFormField>

        <SFormField label="Release Date Range">
          <SFlex gap="1.5em" wrap>
            <SStack gap="0.25em">
              <SLabel>From</SLabel>
              <SDatePicker v-model="dateFrom" />
            </SStack>
            <SStack gap="0.25em">
              <SLabel>To</SLabel>
              <SDatePicker v-model="dateTo" />
            </SStack>
          </SFlex>
        </SFormField>

        <SButton @click="clearFilters">Clear filters</SButton>
      </SStack>
    </SCard>

    <SCard title="Full Release History">
      <STable v-if="releaseRows.length" :columns="releaseColumns" :rows="releaseRows" />
      <SEmpty v-else text="No releases match the selected filters" />
    </SCard>

    <SCard title="Releases by Genre">
      <SDonutChart v-if="genreDistribution.length" :data="genreDistribution" centerLabel="Games" />
      <SEmpty v-else text="No releases match the selected filters" />
    </SCard>
  </SStack>
</template>
