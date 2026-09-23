<script setup>
const platformShare = [
  { label: 'PC', value: 3.5 },
  { label: 'PS5', value: 2.1 },
  { label: 'Xbox', value: 1.4 },
  { label: 'Switch', value: 1.2 },
]

const platformColumns = ['platform', 'copiesSold', 'share']

const platformRows = [
  { platform: 'PC', copiesSold: '3.5M', share: '43%' },
  { platform: 'PS5', copiesSold: '2.1M', share: '26%' },
  { platform: 'Xbox', copiesSold: '1.4M', share: '17%' },
  { platform: 'Switch', copiesSold: '1.2M', share: '15%' },
]
</script>

<template>
  <SStack gap="2.5em">
    <SStack gap="0.25em">
      <SHeading :level="1">Platforms</SHeading>
      <SText variant="body">Lifetime copies sold by platform, all titles combined.</SText>
    </SStack>

    <SGrid :columns="2" gap="2em">
      <SCard title="Copies Sold by Platform (millions)">
        <SDonutChart :data="platformShare" centerLabel="Copies Sold" />
      </SCard>
      <SCard title="Platform Breakdown">
        <STable :columns="platformColumns" :rows="platformRows" />
      </SCard>
    </SGrid>
  </SStack>
</template>
