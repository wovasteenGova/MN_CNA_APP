<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-teal-50 to-cyan-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
    <UContainer class="py-8">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-2xl mb-4 shadow-lg">
          <UIcon name="i-heroicons-academic-cap" class="w-8 h-8 text-white" />
        </div>
        <h1 class="text-4xl font-bold bg-gradient-to-r from-teal-600 to-cyan-600 bg-clip-text text-transparent mb-2">Minnesota CNA Study App</h1>
        <p class="text-lg text-slate-600 dark:text-slate-300 mb-8">Master your Certified Nursing Assistant exam with confidence</p>
        
        <!-- Navigation Buttons -->
        <div class="flex justify-center gap-4 mb-8">
          <NuxtLink to="/app">
            <UButton color="teal" size="xl" icon="i-heroicons-academic-cap">
              Start Studying
            </UButton>
          </NuxtLink>
          <UButton 
            @click="showDonationModal = true"
            color="amber" 
            variant="soft" 
            size="xl" 
            icon="i-heroicons-heart"
          >
            Donate
          </UButton>
        </div>
      </div>
      
      <!-- Progress Summary -->
      <div v-if="Object.keys(progress).length > 0" class="bg-white rounded-lg shadow-lg p-6 mb-8">
        <h2 class="text-2xl font-bold text-slate-800 mb-6">Your Study Progress</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div class="text-center p-4 bg-teal-50 rounded-lg">
            <div class="text-3xl font-bold text-teal-600 mb-2">{{ Object.keys(progress).length }}</div>
            <div class="text-sm font-medium text-slate-600">Chapters Started</div>
          </div>
          
          <div class="text-center p-4 bg-emerald-50 rounded-lg">
            <div class="text-3xl font-bold text-emerald-600 mb-2">{{ totalQuestionsStudied }}</div>
            <div class="text-sm font-medium text-slate-600">Questions Studied</div>
          </div>
          
          <div class="text-center p-4 bg-amber-50 rounded-lg">
            <div class="text-3xl font-bold text-amber-600 mb-2">{{ overallAccuracy }}%</div>
            <div class="text-sm font-medium text-slate-600">Overall Accuracy</div>
          </div>
        </div>
        
        <!-- Individual Chapter Progress -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-slate-800">Chapter Progress</h3>
          <div v-for="(chapterData, chapterName) in progress" :key="chapterName" 
               class="bg-slate-50 rounded-lg p-4">
            <div class="flex justify-between items-center mb-2">
              <h4 class="font-medium text-slate-800">{{ chapterName }}</h4>
              <span class="text-sm text-teal-600 font-medium">
                {{ getChapterStats(chapterData).percentage }}%
              </span>
            </div>
            
            <div class="w-full bg-slate-200 rounded-full h-2 mb-2">
              <div class="bg-teal-500 h-2 rounded-full transition-all duration-300"
                   :style="{ width: getChapterStats(chapterData).percentage + '%' }">
              </div>
            </div>
            
            <div class="flex justify-between text-xs text-slate-500">
              <span>{{ getChapterStats(chapterData).studied }}/{{ chapterData.totalQuestions }} studied</span>
              <span>{{ getChapterStats(chapterData).accuracy }}% accuracy</span>
            </div>
          </div>
        </div>
        
        <div class="flex justify-center space-x-4 mt-6">
          <button @click="createTestData" 
                  class="px-4 py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600">
            Create Test Data
          </button>
          <button @click="clearProgress" 
                  class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600">
            Clear Progress
          </button>
        </div>
      </div>
      
      <div v-else class="bg-white rounded-lg shadow-lg p-6 text-center">
        <p class="text-slate-600 mb-4">No progress data found. Start studying to see your progress!</p>
        <button @click="createTestData" 
                class="px-4 py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600">
          Create Test Data
        </button>
      </div>
      
      <div class="text-center mt-8">
        <a href="/app" class="px-6 py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 font-medium">
          Go to Study App
        </a>
      </div>
    </div>
    
    <!-- Custom Donation Modal -->
    <div 
      v-if="showDonationModal" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4"
      @click="showDonationModal = false"
    >
      <!-- Modal Backdrop -->
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>
      
      <!-- Modal Content -->
      <div 
        class="relative bg-white dark:bg-slate-800 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
        @click.stop
      >
        <!-- Modal Header -->
        <div class="flex items-center justify-between p-6 border-b border-slate-200 dark:border-slate-700">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-gradient-to-br from-amber-500 to-yellow-600 rounded-lg">
              <UIcon name="i-heroicons-heart" class="w-5 h-5 text-white" />
            </div>
            <h2 class="text-xl font-bold text-slate-800 dark:text-slate-100">Support the Developer</h2>
          </div>
          <button
            @click="showDonationModal = false"
            class="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-full transition-colors"
          >
            <UIcon name="i-heroicons-x-mark" class="w-5 h-5 text-slate-500 dark:text-slate-400" />
          </button>
        </div>
        
        <!-- Modal Body -->
        <div class="p-6 space-y-6">
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
          
          <div class="text-center">
            <h3 class="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-4">
              Choose Your Preferred Donation Method
            </h3>
            
            <!-- Donation Options -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <!-- PayPal -->
              <button 
                @click="openDonationLink('paypal')"
                class="group p-6 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-xl border-2 border-blue-200 dark:border-blue-700 hover:border-blue-300 dark:hover:border-blue-600 transition-all duration-200 hover:scale-105 hover:shadow-lg"
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
              </button>
              
              <!-- Venmo -->
              <button 
                @click="openDonationLink('venmo')"
                class="group p-6 bg-gradient-to-br from-sky-50 to-cyan-100 dark:from-sky-900/20 dark:to-cyan-800/20 rounded-xl border-2 border-sky-200 dark:border-sky-700 hover:border-sky-300 dark:hover:border-sky-600 transition-all duration-200 hover:scale-105 hover:shadow-lg"
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
              </button>
              
              <!-- Cash App -->
              <button 
                @click="openDonationLink('cashapp')"
                class="group p-6 bg-gradient-to-br from-green-50 to-emerald-100 dark:from-green-900/20 dark:to-emerald-800/20 rounded-xl border-2 border-green-200 dark:border-green-700 hover:border-green-300 dark:hover:border-green-600 transition-all duration-200 hover:scale-105 hover:shadow-lg"
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
              </button>
            </div>
          </div>
          
          <div class="text-center pt-4 border-t border-slate-200 dark:border-slate-700">
            <p class="text-sm text-slate-500 dark:text-slate-400">
              Every contribution, big or small, is deeply appreciated! ❤️
            </p>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const progress = ref({})
const showDonationModal = ref(false)

const totalQuestionsStudied = computed(() => {
  let total = 0
  Object.values(progress.value).forEach(chapterData => {
    const studied = Array.isArray(chapterData.questionsStudied) 
      ? chapterData.questionsStudied.length 
      : chapterData.questionsStudied?.size || 0
    total += studied
  })
  return total
})

const overallAccuracy = computed(() => {
  let totalStudied = 0
  let totalCorrect = 0
  
  Object.values(progress.value).forEach(chapterData => {
    const studied = Array.isArray(chapterData.questionsStudied) 
      ? chapterData.questionsStudied.length 
      : chapterData.questionsStudied?.size || 0
    const correct = Array.isArray(chapterData.correctAnswers) 
      ? chapterData.correctAnswers.length 
      : chapterData.correctAnswers?.size || 0
    
    totalStudied += studied
    totalCorrect += correct
  })
  
  return totalStudied > 0 ? Math.round((totalCorrect / totalStudied) * 100) : 0
})

const getChapterStats = (chapterData) => {
  const studied = Array.isArray(chapterData.questionsStudied) 
    ? chapterData.questionsStudied.length 
    : chapterData.questionsStudied?.size || 0
  const correct = Array.isArray(chapterData.correctAnswers) 
    ? chapterData.correctAnswers.length 
    : chapterData.correctAnswers?.size || 0
  const total = chapterData.totalQuestions || 0
  
  return {
    studied,
    correct,
    total,
    percentage: total > 0 ? Math.round((studied / total) * 100) : 0,
    accuracy: studied > 0 ? Math.round((correct / studied) * 100) : 0
  }
}

const loadProgress = () => {
  if (typeof window !== 'undefined') {
    const savedProgress = localStorage.getItem('cna-study-progress')
    if (savedProgress) {
      try {
        progress.value = JSON.parse(savedProgress)
        console.log('Loaded progress:', progress.value)
      } catch (e) {
        console.error('Error loading progress:', e)
        progress.value = {}
      }
    }
  }
}

const createTestData = () => {
  const testProgress = {
    'Mental Health': {
      questionsStudied: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
      correctAnswers: [0, 1, 3, 5, 7, 8],
      lastStudied: Date.now(),
      totalQuestions: 37
    },
    'Data Collection': {
      questionsStudied: [0, 1, 2, 3, 4],
      correctAnswers: [0, 2, 4],
      lastStudied: Date.now(),
      totalQuestions: 33
    },
    'Infection Control': {
      questionsStudied: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
      correctAnswers: [0, 1, 2, 4, 6, 7, 8, 10, 12, 14],
      lastStudied: Date.now(),
      totalQuestions: 118
    }
  }
  
  progress.value = testProgress
  
  if (typeof window !== 'undefined') {
    localStorage.setItem('cna-study-progress', JSON.stringify(testProgress))
  }
}

const clearProgress = () => {
  if (confirm('Are you sure you want to clear all progress?')) {
    progress.value = {}
    if (typeof window !== 'undefined') {
      localStorage.removeItem('cna-study-progress')
    }
  }
}

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
  
  // Close the modal after clicking
  showDonationModal.value = false
}

onMounted(() => {
  loadProgress()
})
</script>
