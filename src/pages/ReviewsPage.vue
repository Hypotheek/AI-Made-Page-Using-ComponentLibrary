<script setup>
import { ref } from 'vue'

const reviews = ref([
  {
    reviewer: 'Priya Nakamura',
    outlet: 'Pixel Weekly',
    game: 'Awesome: The Game',
    rating: 4,
    quote: 'Awesome: The Game reinvents the open world formula with a map that actually rewards curiosity instead of padding a checklist.',
  },
  {
    reviewer: 'Marcus Webb',
    outlet: 'GameSphere Daily',
    game: 'Awesome: The Game',
    rating: 4,
    quote: "A few pacing hiccups in the back half, but the first twenty hours are some of the tightest open-world design this year.",
  },
  {
    reviewer: 'Elena Vasquez',
    outlet: 'Indie Pulse',
    game: 'Platformer (Awesome Edition)',
    rating: 5,
    quote: 'Platformer (Awesome Edition) is proof the genre still has surprises left — every level teaches you a new trick and immediately trusts you with it.',
  },
  {
    reviewer: 'Tomás Ferreira',
    outlet: 'Retro & Beyond',
    game: 'Platformer (Awesome Edition)',
    rating: 5,
    quote: "The tightest jump physics I've felt since the genre's golden age. Awesome Studios clearly understands what made platformers great.",
  },
  {
    reviewer: 'Jade Whitmore',
    outlet: 'Ramp Culture',
    game: 'Skate The Awesome',
    rating: 4,
    quote: 'The trick system has real depth without drowning newcomers in menus. Skate The Awesome nails the balance.',
  },
  {
    reviewer: 'Sam Okoye',
    outlet: 'Pixel Weekly',
    game: 'Skate The Awesome',
    rating: 4,
    quote: "Servers could use work, but the core skating feels fantastic — easily Awesome Studios' most tactile game yet.",
  },
])
</script>

<template>
  <SStack gap="2.5em">
    <SStack gap="0.25em">
      <SHeading :level="1">Critic Reviews</SHeading>
      <SText variant="body">Press coverage across all Awesome Studios titles.</SText>
    </SStack>

    <SList>
      <SListItem v-for="(review, index) in reviews" :key="index">
        <SFlex gap="1em" align="start">
          <SAvatar :alt="review.reviewer" size="40px" />
          <SStack gap="0.4em">
            <SSpread align="center">
              <SText variant="body"><strong>{{ review.reviewer }}</strong> — {{ review.outlet }}</SText>
              <STag>{{ review.game }}</STag>
            </SSpread>
            <SRating :max="5" v-model="review.rating" />
            <SBlockquote>{{ review.quote }}</SBlockquote>
          </SStack>
        </SFlex>
      </SListItem>
    </SList>
  </SStack>
</template>
