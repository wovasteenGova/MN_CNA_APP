<template>
  <div class="p-8">
    <h1 class="text-4xl font-bold mb-4">Test Page</h1>
    <p class="mb-4">This is a simple test page to check if routing works.</p>
    <NuxtLink to="/" class="text-blue-500 underline">Back to Home</NuxtLink>
  </div>
</template>

<script setup>
useHead({
  title: 'Test Page - MN CNA APP'
})
</script>
