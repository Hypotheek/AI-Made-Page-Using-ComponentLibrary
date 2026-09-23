<script setup>
import { computed } from 'vue'
import { reviews, releases } from '../data/studioData.js'
import { filterState, isWithinRange } from '../data/filters.js'

const filteredReviews = computed(() =>
  reviews.filter((r) => filterState.selectedTitles.includes(r.title) && isWithinRange(r.date))
)

const filteredReleases = computed(() => releases.filter((r) => filterState.selectedTitles.includes(r.title)))

const avgUserRating = computed(() => {
  if (!filteredReviews.value.length) return '—'
  return (filteredReviews.value.reduce((sum, r) => sum + r.rating, 0) / filteredReviews.value.length).toFixed(1)
})

const avgCriticScore = computed(() => {
  if (!filteredReleases.value.length) return '—'
  return (
    filteredReleases.value.reduce((sum, r) => sum + Number(r.metascore), 0) / filteredReleases.value.length
  ).toFixed(1)
})

const verifiedPct = computed(() => {
  if (!filteredReviews.value.length) return '0%'
  const verified = filteredReviews.value.filter((r) => r.verified).length
  return `${Math.round((100 * verified) / filteredReviews.value.length)}%`
})

const communityKpis = computed(() => [
  { label: 'Avg. User Rating', value: `${avgUserRating.value} / 5`, delta: null, trend: [] },
  { label: 'Avg. Critic Score', value: avgCriticScore.value, delta: null, trend: [] },
  { label: 'Total Reviews', value: String(filteredReviews.value.length), delta: null, trend: [] },
  { label: 'Verified Purchases', value: verifiedPct.value, delta: null, trend: [] },
])

const ratingDistribution = computed(() =>
  [5, 4, 3, 2, 1].map((star) => ({
    label: `${star} star${star > 1 ? 's' : ''}`,
    value: filteredReviews.value.filter((r) => r.rating === star).length,
  }))
)
</script>

<template>
  <SStack gap="2em">
    <SAutoGrid min-width="220px" gap="1em">
      <SKpiCard
        v-for="kpi in communityKpis"
        :key="kpi.label"
        :label="kpi.label"
        :value="kpi.value"
        :delta="kpi.delta"
        :trend="kpi.trend"
        up-is-good
      />
    </SAutoGrid>

    <SCard title="Rating Distribution">
      <SEmpty v-if="!filteredReviews.length" text="No reviews match the current filters" />
      <SHorizontalBar v-else :data="ratingDistribution" />
    </SCard>

    <SCard title="Player Reviews">
      <SEmpty v-if="!filteredReviews.length" text="No reviews match the current filters" />
      <SGrid v-else :columns="2" gap="1em">
        <SCard v-for="(review, i) in filteredReviews" :key="i">
          <SStack gap="0.5em">
            <SFlex justify="space-between" align="center">
              <SFlex gap="0.75em" align="center">
                <SAvatar size="36px" :alt="review.initials" />
                <div>
                  <SText variant="body"><strong>{{ review.reviewer }}</strong></SText>
                  <SText variant="body">{{ review.title }} &middot; {{ review.platform }}</SText>
                </div>
              </SFlex>
              <SBadge v-if="review.verified" variant="success">Verified Purchase</SBadge>
            </SFlex>
            <SRating :model-value="review.rating" :max="5" />
            <SBlockquote>{{ review.quote }}</SBlockquote>
            <SText variant="body">{{ review.date }}</SText>
          </SStack>
        </SCard>
      </SGrid>
    </SCard>
  </SStack>
</template>
