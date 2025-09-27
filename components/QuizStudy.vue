<template>
  <div class="max-w-4xl mx-auto px-2 sm:px-4">
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- Question Counter -->
      <div class="bg-gray-50 px-4 sm:px-6 py-3 sm:py-4 border-b">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 sm:gap-0">
          <span class="text-sm font-medium text-gray-600">
            Question {{ questionNumber }} of {{ totalQuestions }}
          </span>
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-600 hidden sm:inline">Mode:</span>
            <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-800">
              Multiple Choice
            </span>
          </div>
        </div>
      </div>

      <!-- Question -->
      <div class="p-4 sm:p-6 md:p-8">
        <div class="mb-6 sm:mb-8">
          <h2 class="text-lg sm:text-xl md:text-2xl font-semibold text-gray-900 leading-relaxed mb-4 sm:mb-6">
            {{ question.question }}
          </h2>
        </div>

        <!-- Answer Choices -->
        <div class="space-y-2 sm:space-y-3">
          <label
            v-for="(choice, index) in shuffledChoices"
            :key="index"
            :class="[
              'block p-3 sm:p-4 rounded-lg border-2 cursor-pointer transition-all duration-200',
              getChoiceClasses(choice, index)
            ]"
            @click="selectAnswer(choice)"
            role="button"
            tabindex="0"
            @keydown.enter="selectAnswer(choice)"
            @keydown.space.prevent="selectAnswer(choice)"
            :aria-label="`Answer option ${index + 1}: ${choice}`"
          >
            <div class="flex items-center">
              <input
                type="radio"
                :name="`question-${questionNumber}`"
                :value="choice"
                :checked="selectedAnswer === choice"
                class="sr-only"
                :aria-describedby="`choice-${index}`"
              />
              <div class="flex-shrink-0 mr-3 sm:mr-4">
                <div
                  :class="[
                    'w-5 h-5 sm:w-6 sm:h-6 rounded-full border-2 flex items-center justify-center text-xs sm:text-sm font-semibold',
                    getRadioClasses(choice)
                  ]"
                >
                  <span v-if="showFeedback && choice === question.answer" class="text-white">✓</span>
                  <span v-else-if="showFeedback && selectedAnswer === choice && choice !== question.answer" class="text-white">✗</span>
                  <span v-else-if="selectedAnswer === choice && !showFeedback" class="text-white">✓</span>
                  <span v-else class="text-gray-400">{{ String.fromCharCode(65 + index) }}</span>
                </div>
              </div>
              <div class="flex-1">
                <p
                  :id="`choice-${index}`"
                  :class="[
                    'text-sm sm:text-base font-medium leading-relaxed',
                    selectedAnswer === choice ? 'text-white' : 'text-gray-900'
                  ]"
                >
                  {{ choice }}
                </p>
              </div>
            </div>
          </label>
        </div>

        <!-- Answer Feedback -->
        <div v-if="showFeedback" class="mt-6 p-4 rounded-lg" :class="feedbackClasses">
          <div class="flex items-start">
            <div class="flex-shrink-0 mr-3">
              <span v-if="isCorrect" class="text-green-500 text-xl">✓</span>
              <span v-else class="text-red-500 text-xl">✗</span>
            </div>
            <div>
              <h3 :class="['font-semibold', isCorrect ? 'text-green-800' : 'text-red-800']">
                {{ isCorrect ? 'Correct!' : 'Incorrect' }}
              </h3>
              <p :class="['text-sm mt-1', isCorrect ? 'text-green-700' : 'text-red-700']">
                {{ isCorrect ? 'Great job!' : `The correct answer is: ${question.answer}` }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="bg-gray-50 px-4 sm:px-6 py-4 border-t">
        <div class="flex flex-col sm:flex-row justify-between items-center gap-4 sm:gap-0">
          <div class="flex space-x-2 sm:space-x-3 w-full sm:w-auto">
            <button
              @click="$emit('previous')"
              class="flex-1 sm:flex-initial inline-flex items-center justify-center px-3 sm:px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              ← Previous
            </button>
            <button
              @click="$emit('next')"
              class="flex-1 sm:flex-initial inline-flex items-center justify-center px-3 sm:px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Next →
            </button>
          </div>
          
          <div class="flex flex-col sm:flex-row items-center gap-3 sm:gap-4 w-full sm:w-auto">
            <button
              v-if="!showFeedback && selectedAnswer"
              @click="checkAnswer"
              class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Check Answer
            </button>
            <div class="hidden lg:flex items-center space-x-2">
              <span class="text-sm text-gray-600">Keyboard shortcuts:</span>
              <kbd class="px-2 py-1 text-xs font-semibold text-gray-800 bg-gray-200 border border-gray-300 rounded">A-D</kbd>
              <span class="text-xs text-gray-500">to select</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

// Props
const props = defineProps({
  question: {
    type: Object,
    required: true
  },
  questionNumber: {
    type: Number,
    required: true
  },
  totalQuestions: {
    type: Number,
    required: true
  }
})

// Emits
const emit = defineEmits(['next', 'previous', 'answer-selected'])

// Reactive state
const selectedAnswer = ref('')
const showFeedback = ref(false)
const shuffledChoices = ref([])

// Computed properties
const isCorrect = computed(() => {
  return selectedAnswer.value === props.question.answer
})

const feedbackClasses = computed(() => {
  return isCorrect.value
    ? 'bg-green-50 border border-green-200'
    : 'bg-red-50 border border-red-200'
})

// Methods
const shuffleArray = (array) => {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

const selectAnswer = (choice) => {
  selectedAnswer.value = choice
  emit('answer-selected', choice)
}

const checkAnswer = () => {
  showFeedback.value = true
}

const getChoiceClasses = (choice, index) => {
  if (!selectedAnswer.value) {
    return 'border-gray-200 hover:border-blue-300 hover:bg-blue-50'
  }
  
  // If feedback is shown, highlight the correct answer in green
  if (showFeedback.value && choice === props.question.answer) {
    return 'border-green-500 bg-green-500 text-white'
  }
  
  // If feedback is shown and this is the selected (but wrong) answer
  if (showFeedback.value && selectedAnswer.value === choice && choice !== props.question.answer) {
    return 'border-red-500 bg-red-500 text-white'
  }
  
  // If this is the selected answer but no feedback yet
  if (selectedAnswer.value === choice && !showFeedback.value) {
    return 'border-blue-500 bg-blue-500 text-white'
  }
  
  return 'border-gray-200 bg-gray-50'
}

const getRadioClasses = (choice) => {
  if (!selectedAnswer.value) {
    return 'border-gray-300 bg-white'
  }
  
  // If feedback is shown, highlight the correct answer in green
  if (showFeedback.value && choice === props.question.answer) {
    return 'border-green-600 bg-green-600'
  }
  
  // If feedback is shown and this is the selected (but wrong) answer
  if (showFeedback.value && selectedAnswer.value === choice && choice !== props.question.answer) {
    return 'border-red-600 bg-red-600'
  }
  
  // If this is the selected answer but no feedback yet
  if (selectedAnswer.value === choice && !showFeedback.value) {
    return 'border-blue-600 bg-blue-600'
  }
  
  return 'border-gray-300 bg-gray-100'
}

// Initialize shuffled choices
const initializeChoices = () => {
  shuffledChoices.value = shuffleArray(props.question.choices)
}

// Reset state when question changes
watch(() => props.question, () => {
  selectedAnswer.value = ''
  showFeedback.value = false
  initializeChoices()
}, { immediate: true })

// Keyboard navigation
const handleKeydown = (event) => {
  if (event.key >= 'a' && event.key <= 'd') {
    const index = event.key.charCodeAt(0) - 97
    if (index < shuffledChoices.value.length) {
      selectAnswer(shuffledChoices.value[index])
    }
  } else if (event.key === 'ArrowLeft') {
    emit('previous')
  } else if (event.key === 'ArrowRight') {
    emit('next')
  } else if (event.key === 'Enter' && selectedAnswer.value && !showFeedback.value) {
    checkAnswer()
  }
}

// Add keyboard listeners
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

