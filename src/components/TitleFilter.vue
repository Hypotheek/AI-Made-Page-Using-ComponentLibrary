<script setup>
import { ref, computed } from 'vue'
import { filterState } from '../data/filters.js'
import { releases } from '../data/studioData.js'

const search = ref('')
const allTitles = releases.map((r) => r.title)

const filteredOptions = computed(() =>
  allTitles
    .filter((t) => t.toLowerCase().includes(search.value.toLowerCase()))
    .map((t) => ({ label: t, value: t }))
)

function removeTitle(title) {
  filterState.selectedTitles = filterState.selectedTitles.filter((t) => t !== title)
}

function selectAll() {
  filterState.selectedTitles = [...allTitles]
}

function clearAll() {
  filterState.selectedTitles = []
}
</script>

<template>
  <SFormField label="Titles">
    <SPopover>
      <template #trigger>
        <SButton variant="secondary">
          Titles ({{ filterState.selectedTitles.length }}/{{ allTitles.length }})
        </SButton>
      </template>
      <SStack gap="0.75em">
        <SSearchInput v-model="search" placeholder="Search titles..." />
        <SCheckboxGroup v-model="filterState.selectedTitles" :options="filteredOptions" />
        <SFlex justify="space-between">
          <SButton variant="secondary" @click="selectAll">Select all</SButton>
          <SButton variant="secondary" @click="clearAll">Clear</SButton>
        </SFlex>
      </SStack>
    </SPopover>
    <SFlex v-if="filterState.selectedTitles.length && filterState.selectedTitles.length < allTitles.length" wrap gap="0.5em">
      <SChip v-for="t in filterState.selectedTitles" :key="t" closable @close="removeTitle(t)">{{ t }}</SChip>
    </SFlex>
  </SFormField>
</template>
