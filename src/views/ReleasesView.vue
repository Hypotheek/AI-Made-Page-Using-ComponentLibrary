<script setup>
import { computed } from 'vue'
import { releases, releaseSteps, tableColumns, toTableRows } from '../data/studioData.js'
import { filterState, matchesTitleFilters } from '../data/filters.js'

const filteredReleases = computed(() => releases.filter((r) => matchesTitleFilters(r.title)))
const filteredSteps = computed(() => releaseSteps.filter((s) => matchesTitleFilters(s.title)))
const tableRows = computed(() => toTableRows(filteredReleases.value))
</script>

<template>
  <SStack gap="2em">
    <SCard title="Release Roadmap">
      <SEmpty v-if="!filteredSteps.length" text="No releases match the current filters" />
      <SVerticalSteps v-else :model-value="filteredSteps.length - 1" :steps="filteredSteps" />
    </SCard>

    <SCard title="Recent Releases">
      <SEmpty v-if="!filteredReleases.length" text="No releases match the current filters" />
      <SGrid v-else :columns="3" gap="1em">
        <SCard v-for="r in filteredReleases" :key="r.title" :title="r.title">
          <SStack gap="0.5em">
            <SFlex justify="space-between" align="center">
              <SBadge variant="success">{{ r.status }}</SBadge>
              <SText variant="body">{{ r.tagline }}</SText>
            </SFlex>
            <SText variant="body">{{ r.genre }}</SText>
            <SText variant="body">{{ r.platforms }}</SText>
            <SFlex justify="space-between" align="center">
              <SRating :model-value="r.userRating" :max="5" />
              <SText variant="body">{{ r.userRating }} ({{ r.reviewCount }} reviews)</SText>
            </SFlex>
            <SFlex justify="space-between">
              <SStat label="Released" :value="r.released" />
              <SStat label="Units Sold" :value="r.units" />
              <SStat label="Metascore" :value="r.metascore" />
            </SFlex>
          </SStack>
        </SCard>
      </SGrid>
    </SCard>

    <SCard title="Release Summary">
      <SEmpty v-if="!tableRows.length" text="No releases match the current filters" />
      <STable v-else :columns="tableColumns" :rows="tableRows" />
    </SCard>
  </SStack>
</template>
