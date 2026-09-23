<script setup>
import { ref, computed } from 'vue'
import { recentReleases, reviewsByGame } from '../data/studio'

const gameTabs = recentReleases.map((r) => r.title)
const selectedGame = ref(gameTabs[0])

const activeReviews = computed(() => reviewsByGame[selectedGame.value])
</script>

<template>
  <SCard title="Player & Critic Reviews">
    <SStack gap="1em">
      <STabs v-model="selectedGame" :tabs="gameTabs" />

      <SList>
        <SListItem v-for="review in activeReviews" :key="review.name">
          <SFlex gap="1em" align="start">
            <SAvatar size="48px" :alt="review.name" />
            <SStack gap="0.5em">
              <SSpread align="center">
                <SText variant="body"><strong>{{ review.name }}</strong> &middot; {{ review.outlet }}</SText>
                <SRating :max="5" v-model="review.rating" />
              </SSpread>
              <SBlockquote>{{ review.quote }}</SBlockquote>
            </SStack>
          </SFlex>
        </SListItem>
      </SList>
    </SStack>
  </SCard>
</template>
