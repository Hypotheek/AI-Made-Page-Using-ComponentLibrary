import { reactive } from 'vue'
import { releases } from './studioData.js'

const allTitles = releases.map((r) => r.title)
const releaseByTitle = Object.fromEntries(releases.map((r) => [r.title, r]))

export const filterState = reactive({
  selectedTitles: [...allTitles],
  dateFrom: '',
  dateTo: '',
})

export function isWithinRange(dateStr) {
  if (!dateStr) return true
  if (filterState.dateFrom && dateStr < filterState.dateFrom) return false
  if (filterState.dateTo && dateStr > filterState.dateTo) return false
  return true
}

export function matchesTitleFilters(title) {
  if (!filterState.selectedTitles.includes(title)) return false
  const release = releaseByTitle[title]
  return release ? isWithinRange(release.released) : true
}

export function resetFilters() {
  filterState.selectedTitles = [...allTitles]
  filterState.dateFrom = ''
  filterState.dateTo = ''
}
