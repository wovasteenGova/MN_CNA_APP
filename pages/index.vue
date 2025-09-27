<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-teal-50 p-8">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-slate-800 mb-4">Minnesota CNA Study App</h1>
        <p class="text-lg text-slate-600">Progress Dashboard</p>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const progress = ref({})

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

onMounted(() => {
  loadProgress()
})
</script>
