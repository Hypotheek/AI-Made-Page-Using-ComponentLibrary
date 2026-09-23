<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const pageTabs = ['Overview', 'Releases', 'Reviews', 'Community']

const activeTab = computed({
  get: () => route.name,
  set: (name) => router.push({ name }),
})
</script>

<template>
  <SNavbar title="Awesome Studios">
    <SBadge variant="default">Bi-yearly releases</SBadge>
  </SNavbar>

  <SContainer>
    <SPad size="2em">
      <SStack gap="2em">
        <STabs v-model="activeTab" :tabs="pageTabs" />

        <router-view />
      </SStack>
    </SPad>
  </SContainer>
</template>
