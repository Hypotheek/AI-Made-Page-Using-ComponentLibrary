<script setup>
import { filterState } from '../data/filters.js'

function clearRange() {
  filterState.dateFrom = ''
  filterState.dateTo = ''
}
</script>

<template>
  <SFormField label="Release Date Range" hint="Filters releases and reviews">
    <SFlex gap="0.5em" align="center" wrap>
      <SDatePicker v-model="filterState.dateFrom" />
      <SText variant="body">to</SText>
      <SDatePicker v-model="filterState.dateTo" />
      <SButton variant="secondary" @click="clearRange">Clear</SButton>
    </SFlex>
  </SFormField>
</template>
