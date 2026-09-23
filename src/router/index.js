import { createRouter, createWebHistory } from 'vue-router'
import OverviewPage from '../pages/OverviewPage.vue'
import ReleasesPage from '../pages/ReleasesPage.vue'
import ReviewsPage from '../pages/ReviewsPage.vue'
import CommunityPage from '../pages/CommunityPage.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Overview', component: OverviewPage },
    { path: '/releases', name: 'Releases', component: ReleasesPage },
    { path: '/reviews', name: 'Reviews', component: ReviewsPage },
    { path: '/community', name: 'Community', component: CommunityPage },
  ],
})
