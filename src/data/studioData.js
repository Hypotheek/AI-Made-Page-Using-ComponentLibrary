export const overviewKpis = [
  { label: 'Lifetime Revenue', value: '$412.6M', delta: 18, trend: [210, 240, 265, 300, 340, 385, 412] },
  { label: 'Total Units Sold', value: '7.3M', delta: 9, trend: [4.1, 4.6, 5.2, 5.9, 6.4, 6.9, 7.3] },
  { label: 'Avg. Critic Score', value: '87.7', delta: 2, trend: [82, 83, 85, 84, 86, 87, 88] },
  { label: 'Avg. User Rating', value: '4.6 / 5', delta: 4, trend: [4.1, 4.2, 4.3, 4.4, 4.5, 4.5, 4.6] },
  { label: 'Active Players (30d)', value: '1.24M', delta: 5, trend: [0.95, 1.01, 1.24, 1.15, 1.08, 1.19, 1.24] },
]

export const revenueByTitle = [
  { label: 'Awesome', title: 'Awesome: The Game', value: 168 },
  { label: 'Platformer', title: 'Platformer (Awesome Edition)', value: 121 },
  { label: 'Skate', title: 'Skate The Awesome', value: 96 },
]

export const revenueByPlatform = [
  { label: 'PlayStation', value: 152 },
  { label: 'PC', value: 104 },
  { label: 'Xbox', value: 98 },
  { label: 'Switch', value: 58.6 },
]

export const unitsShare = [
  { label: 'Awesome: The Game', value: 3.1 },
  { label: 'Platformer (Awesome Edition)', value: 2.4 },
  { label: 'Skate The Awesome', value: 1.8 },
]

export const monthlyActivePlayers = [
  { label: 'Apr', value: 950000 },
  { label: 'May', value: 1010000 },
  { label: 'Jun', value: 1080000 },
  { label: 'Jul', value: 1150000 },
  { label: 'Aug', value: 1190000 },
  { label: 'Sep', value: 1240000 },
]

export const releases = [
  {
    title: 'Skate The Awesome',
    tagline: 'Latest release',
    genre: 'Sports / Skating',
    platforms: 'PS5, Xbox Series X|S, PC',
    released: '2026-03-14',
    units: '1.8M',
    metascore: '84',
    status: 'Live',
    userRating: 4.4,
    reviewCount: '18.2k',
  },
  {
    title: 'Platformer (Awesome Edition)',
    tagline: 'Previous release',
    genre: 'Platformer',
    platforms: 'Switch, PC',
    released: '2025-09-10',
    units: '2.4M',
    metascore: '88',
    status: 'Live',
    userRating: 4.7,
    reviewCount: '26.5k',
  },
  {
    title: 'Awesome: The Game',
    tagline: 'Flagship title',
    genre: 'Action-Adventure',
    platforms: 'PS5, Xbox, PC, Switch',
    released: '2025-03-05',
    units: '3.1M',
    metascore: '91',
    status: 'Live',
    userRating: 4.7,
    reviewCount: '41.3k',
  },
]

export const releaseSteps = [
  { title: 'Awesome: The Game', description: 'Flagship launch — 2025-03-05' },
  { title: 'Platformer (Awesome Edition)', description: 'Second release — 2025-09-10' },
  { title: 'Skate The Awesome', description: 'Latest release — 2026-03-14' },
]

export const tableColumns = ['Title', 'Release Date', 'Platforms', 'Genre', 'Metascore', 'User Rating', 'Units Sold']
export function toTableRows(releaseList) {
  return releaseList.map((r) => ({
    Title: r.title,
    'Release Date': r.released,
    Platforms: r.platforms,
    Genre: r.genre,
    Metascore: r.metascore,
    'User Rating': `${r.userRating} / 5`,
    'Units Sold': r.units,
  }))
}

export const reviews = [
  {
    reviewer: 'Jordan M.',
    initials: 'JM',
    title: 'Skate The Awesome',
    platform: 'PS5',
    rating: 5,
    date: '2026-03-22',
    quote: "The trick system finally feels next-gen. Best skating game since the genre's golden age.",
    verified: true,
  },
  {
    reviewer: 'Priya K.',
    initials: 'PK',
    title: 'Skate The Awesome',
    platform: 'PC',
    rating: 4,
    date: '2026-04-02',
    quote: 'Gorgeous city map and killer soundtrack, but online lobbies still need work.',
    verified: true,
  },
  {
    reviewer: 'Sam T.',
    initials: 'ST',
    title: 'Platformer (Awesome Edition)',
    platform: 'Switch',
    rating: 5,
    date: '2025-09-18',
    quote: 'Tight controls and the level design is pure joy. A masterclass in platforming.',
    verified: true,
  },
  {
    reviewer: 'Alex R.',
    initials: 'AR',
    title: 'Awesome: The Game',
    platform: 'PC',
    rating: 5,
    date: '2025-03-20',
    quote: 'Still the best in the series years later. The remaster holds up beautifully.',
    verified: true,
  },
  {
    reviewer: 'Morgan L.',
    initials: 'ML',
    title: 'Awesome: The Game',
    platform: 'Xbox',
    rating: 4,
    date: '2025-04-05',
    quote: 'Incredible story and world, though pacing sags a bit in act two.',
    verified: false,
  },
]
