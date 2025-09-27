<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-teal-50 to-cyan-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
    <!-- Header -->
    <UContainer class="py-4 sm:py-8 px-4">
      <div class="text-center mb-6 sm:mb-8">
        <div class="inline-flex items-center justify-center w-12 h-12 sm:w-16 sm:h-16 bg-gradient-to-br from-amber-500 to-yellow-600 rounded-2xl mb-3 sm:mb-4 shadow-lg">
          <UIcon name="i-heroicons-heart" class="w-6 h-6 sm:w-8 sm:h-8 text-white" />
        </div>
        <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold bg-gradient-to-r from-amber-600 to-yellow-600 bg-clip-text text-transparent mb-2 px-2">
          Support the Developer
        </h1>
        <p class="text-base sm:text-lg text-slate-600 dark:text-slate-300 mb-4 px-2">
          Help keep this CNA study app free and continuously improved
        </p>
        
        <!-- Back to Home Button -->
        <div class="flex justify-center">
          <NuxtLink to="/">
            <UButton
              color="teal"
              variant="soft"
              size="lg"
              icon="i-heroicons-arrow-left"
              class="bg-gradient-to-r from-teal-100 to-cyan-100 hover:from-teal-200 hover:to-cyan-200 dark:from-teal-900/50 dark:to-cyan-900/50 text-teal-700 dark:text-teal-300 border-0 shadow-md hover:shadow-lg transition-all duration-200"
              :ui="{ rounded: 'rounded-full' }"
            >
              Back to App
            </UButton>
          </NuxtLink>
        </div>
      </div>

      <!-- Donation Card -->
      <div class="max-w-4xl mx-auto">
        <UCard class="bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm border border-slate-200/50 dark:border-slate-700/50 shadow-2xl">
          <template #header>
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-gradient-to-br from-amber-500 to-yellow-600 rounded-lg">
                <UIcon name="i-heroicons-heart" class="w-5 h-5 text-white" />
              </div>
              <h2 class="text-xl font-bold text-slate-800 dark:text-slate-100">Choose Your Donation Method</h2>
            </div>
          </template>
          
          <div class="space-y-6">
            <div class="text-center">
              <p class="text-slate-600 dark:text-slate-300 mb-4">
                If this CNA study app has helped you in your journey, consider supporting its development! 
                Your donation helps keep the app free and continuously improved.
              </p>
              <div class="inline-flex items-center px-4 py-2 bg-teal-50 dark:bg-teal-900/30 rounded-lg">
                <UIcon name="i-heroicons-academic-cap" class="w-5 h-5 text-teal-600 dark:text-teal-400 mr-2" />
                <span class="text-sm font-medium text-teal-700 dark:text-teal-300">
                  Help future CNAs succeed! 🎓
                </span>
              </div>
            </div>
            
            <!-- Donation Options -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6">
              <!-- PayPal -->
              <div 
                @click="openDonationLink('paypal')"
                class="cursor-pointer group p-6 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-xl border-2 border-blue-200 dark:border-blue-700 hover:border-blue-300 dark:hover:border-blue-600 transition-all duration-200 hover:scale-105 hover:shadow-lg"
              >
                <div class="text-center">
                  <div class="w-12 h-12 mx-auto mb-3 bg-blue-600 rounded-lg flex items-center justify-center group-hover:bg-blue-700 transition-colors">
                    <span class="text-white font-bold text-lg">P</span>
                  </div>
                  <h4 class="font-semibold text-slate-800 dark:text-slate-100 mb-2">PayPal</h4>
                  <p class="text-sm text-slate-600 dark:text-slate-400">
                    Secure & widely accepted
                  </p>
                </div>
              </div>
              
              <!-- Venmo -->
              <div 
                @click="openDonationLink('venmo')"
                class="cursor-pointer group p-6 bg-gradient-to-br from-sky-50 to-cyan-100 dark:from-sky-900/20 dark:to-cyan-800/20 rounded-xl border-2 border-sky-200 dark:border-sky-700 hover:border-sky-300 dark:hover:border-sky-600 transition-all duration-200 hover:scale-105 hover:shadow-lg"
              >
                <div class="text-center">
                  <div class="w-12 h-12 mx-auto mb-3 bg-sky-600 rounded-lg flex items-center justify-center group-hover:bg-sky-700 transition-colors">
                    <span class="text-white font-bold text-lg">V</span>
                  </div>
                  <h4 class="font-semibold text-slate-800 dark:text-slate-100 mb-2">Venmo</h4>
                  <p class="text-sm text-slate-600 dark:text-slate-400">
                    Quick & easy mobile payments
                  </p>
                </div>
              </div>
              
              <!-- Cash App -->
              <div 
                @click="openDonationLink('cashapp')"
                class="cursor-pointer group p-6 bg-gradient-to-br from-green-50 to-emerald-100 dark:from-green-900/20 dark:to-emerald-800/20 rounded-xl border-2 border-green-200 dark:border-green-700 hover:border-green-300 dark:hover:border-green-600 transition-all duration-200 hover:scale-105 hover:shadow-lg"
              >
                <div class="text-center">
                  <div class="w-12 h-12 mx-auto mb-3 bg-green-600 rounded-lg flex items-center justify-center group-hover:bg-green-700 transition-colors">
                    <span class="text-white font-bold text-lg">$</span>
                  </div>
                  <h4 class="font-semibold text-slate-800 dark:text-slate-100 mb-2">Cash App</h4>
                  <p class="text-sm text-slate-600 dark:text-slate-400">
                    Simple cash transfers
                  </p>
                </div>
              </div>
            </div>
            
            <div class="text-center pt-4 border-t border-slate-200 dark:border-slate-700">
              <p class="text-sm text-slate-500 dark:text-slate-400">
                Every contribution, big or small, is deeply appreciated! ❤️
              </p>
            </div>
          </div>
        </UCard>
      </div>
    </UContainer>
  </div>
</template>

<script setup>
// Set page title
useHead({
  title: 'Donate - MN CNA APP',
  meta: [
    { name: 'description', content: 'Support the Minnesota CNA Study App development - Help keep it free for future CNAs!' }
  ]
})



const openDonationLink = (platform) => {
  // You can replace these with your actual donation links
  const donationLinks = {
    paypal: 'https://paypal.me/yourusername', // Replace with your PayPal.me link
    venmo: 'https://venmo.com/u/yourusername', // Replace with your Venmo username
    cashapp: 'https://cash.app/$yourusername'  // Replace with your Cash App username
  }
  
  const link = donationLinks[platform]
  if (link && typeof window !== 'undefined') {
    window.open(link, '_blank')
  }
}
</script>
