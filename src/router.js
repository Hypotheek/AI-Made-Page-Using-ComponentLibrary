import { createRouter, createWebHistory } from 'vue-router'
import OverviewPage from './pages/OverviewPage.vue'
import ReleasesPage from './pages/ReleasesPage.vue'
import ReviewsPage from './pages/ReviewsPage.vue'
import PlatformsPage from './pages/PlatformsPage.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'overview', component: OverviewPage },
    { path: '/releases', name: 'releases', component: ReleasesPage },
    { path: '/reviews', name: 'reviews', component: ReviewsPage },
    { path: '/platforms', name: 'platforms', component: PlatformsPage },
  ],
})
