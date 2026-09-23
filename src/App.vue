<script setup>
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const navItems = [
  { label: 'Overview', path: '/' },
  { label: 'Releases', path: '/releases' },
  { label: 'Reviews', path: '/reviews' },
  { label: 'Platforms', path: '/platforms' },
]

function go(path) {
  if (route.path !== path) router.push(path)
}
</script>

<template>
  <SNavbar title="Awesome Studios">
    <SInline gap="1.5em">
      <SLink v-for="item in navItems" :key="item.path" :href="item.path" @click.prevent="go(item.path)">
        <strong v-if="route.path === item.path">{{ item.label }}</strong>
        <template v-else>{{ item.label }}</template>
      </SLink>
    </SInline>
  </SNavbar>

  <SContainer>
    <SPad size="2em">
      <router-view />
    </SPad>
  </SContainer>
</template>
