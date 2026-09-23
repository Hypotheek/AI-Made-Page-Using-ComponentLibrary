// Placeholder data for the Awesome Studios dashboards.
// All figures are illustrative, not real studio data.

export const releases = [
  { title: 'Awesome Quest', genre: 'RPG', released: '2014-04-02', platforms: 'PC', rating: 7.2 },
  { title: 'Awesome Kart', genre: 'Racing', released: '2016-05-19', platforms: 'PC, PlayStation', rating: 7.6 },
  { title: 'The Awesome Chronicles', genre: 'RPG', released: '2018-06-21', platforms: 'PC, PlayStation, Xbox', rating: 8.0 },
  { title: 'Awesome Arena', genre: 'Fighting', released: '2020-07-14', platforms: 'PC, PlayStation, Xbox, Switch', rating: 7.5 },
  { title: 'Awesome: The Game', genre: 'Action-Adventure', released: '2022-09-15', platforms: 'PC, PlayStation, Xbox', rating: 8.4 },
  { title: 'Platformer (Awesome Edition)', genre: 'Platformer', released: '2024-03-10', platforms: 'PC, Switch', rating: 7.9 },
  { title: 'Skate The Awesome', genre: 'Sports', released: '2026-06-01', platforms: 'PC, PlayStation, Xbox, Switch', rating: 8.7 },
]

export const recentReleases = releases.slice(-3)

export const overviewKpis = [
  { label: 'Games Released', value: releases.length, trend: releases.map((r) => r.rating) },
  { label: 'Average Critic Score', value: '8.3 / 10', delta: 5, trend: [7.6, 7.8, 7.9, 8.0, 8.4, 7.9, 8.7] },
  { label: 'Years Active', value: 12, trend: [] },
  { label: 'Latest Release Score', value: '8.7 / 10', delta: 10, trend: [7.9, 8.7] },
]

export const ratingHistoryChart = releases.map((r) => ({ label: r.title, value: r.rating }))

export const genreDistributionChart = Object.entries(
  releases.reduce((acc, r) => {
    acc[r.genre] = (acc[r.genre] || 0) + 1
    return acc
  }, {}),
).map(([label, value]) => ({ label, value }))

export const reviewsByGame = {
  'Awesome: The Game': [
    {
      name: 'Mia Chen',
      outlet: 'GameSphere',
      rating: 4,
      quote: "A confident debut that finally makes 'Awesome' live up to its name.",
    },
    {
      name: 'Jordan Blake',
      outlet: 'Player One Weekly',
      rating: 4.5,
      quote: 'Awesome Studios nails the fundamentals here, combat feels tight and the world begs to be explored.',
    },
  ],
  'Platformer (Awesome Edition)': [
    {
      name: 'Sam Patel',
      outlet: 'PixelPress',
      rating: 4,
      quote: 'Charming and tight platforming, though a few levels overstay their welcome.',
    },
    {
      name: 'Riley Nguyen',
      outlet: 'IndieBit',
      rating: 3.5,
      quote: 'A solid, if familiar, entry that platformer fans will still enjoy.',
    },
  ],
  'Skate The Awesome': [
    {
      name: 'Casey Morgan',
      outlet: 'RampReport',
      rating: 5,
      quote: 'The best skating game the studio has ever shipped, the physics feel incredible.',
    },
    {
      name: 'Taylor Reyes',
      outlet: 'Player One Weekly',
      rating: 4.5,
      quote: "Awesome Studios' most ambitious release yet, and it sticks the landing.",
    },
  ],
}

export const communityKpis = [
  { label: 'Monthly Active Players', value: '128k', delta: 8, trend: [96, 101, 108, 115, 121, 128] },
  { label: 'Total Revenue', value: '$11.5M', delta: 6, trend: [8.4, 8.9, 9.6, 10.2, 10.9, 11.5] },
  { label: 'Avg Session Length', value: '46 min', trend: [] },
  { label: 'Wishlist Adds (30d)', value: '34.2k', delta: 15, trend: [21, 24, 27, 29, 31, 34] },
]

export const monthlyActivePlayersChart = [
  { label: 'Apr', value: 96000 },
  { label: 'May', value: 101000 },
  { label: 'Jun', value: 108000 },
  { label: 'Jul', value: 115000 },
  { label: 'Aug', value: 121000 },
  { label: 'Sep', value: 128000 },
]

export const revenueByPlatformChart = [
  { label: 'PC', value: 4.2 },
  { label: 'PlayStation', value: 3.1 },
  { label: 'Xbox', value: 2.4 },
  { label: 'Switch', value: 1.8 },
]
