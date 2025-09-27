<template>
  <UApp>
    <NuxtPage />
  </UApp>
</template>

<script setup>
// Set global page title
useHead({
  title: 'MN CNA APP',
  meta: [
    { name: 'description', content: 'Minnesota CNA Study App - Master your Certified Nursing Assistant exam with confidence' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' },
    { name: 'format-detection', content: 'telephone=no' }
  ]
})
</script>
