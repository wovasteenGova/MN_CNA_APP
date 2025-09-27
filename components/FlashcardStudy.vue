<template>
  <div class="max-w-4xl mx-auto px-2 sm:px-4">
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- Question Counter -->
      <div class="bg-gray-50 px-4 sm:px-6 py-3 sm:py-4 border-b">
        <div class="flex justify-between items-center">
          <span class="text-sm font-medium text-gray-600">
            Question {{ questionNumber }} of {{ totalQuestions }}
          </span>
          <button
            @click="shuffleQuestions"
            class="text-sm text-blue-600 hover:text-blue-800 font-medium px-2 py-1 rounded hover:bg-blue-50"
            title="Shuffle questions"
          >
            🔀 <span class="hidden sm:inline">Shuffle</span>
          </button>
        </div>
      </div>

      <!-- Flashcard -->
      <div class="relative h-80 sm:h-96 perspective-1000">
        <div
          ref="cardRef"
          class="relative w-full h-full transition-transform duration-700 transform-style-preserve-3d cursor-pointer"
          :class="{ 'rotate-y-180': isFlipped }"
          @click="flipCard"
          role="button"
          tabindex="0"
          @keydown.enter="flipCard"
          @keydown.space.prevent="flipCard"
          :aria-label="isFlipped ? 'Question side' : 'Answer side'"
        >
          <!-- Question Side -->
          <div
            class="absolute inset-0 w-full h-full backface-hidden bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center p-4 sm:p-6 md:p-8"
          >
            <div class="text-center max-w-2xl">
              <div class="mb-4 sm:mb-6">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 mb-4">
                  Question
                </span>
              </div>
              <h2 class="text-lg sm:text-xl md:text-2xl font-semibold text-gray-900 leading-relaxed">
                {{ question.question }}
              </h2>
              <div class="mt-6 sm:mt-8">
                <p class="text-sm text-gray-600">
                  Tap the card to reveal the answer
                </p>
                <div class="mt-4">
                  <span class="inline-flex items-center px-4 py-2 rounded-lg bg-white bg-opacity-50 text-gray-700 text-sm font-medium">
                    👆 Click to flip
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Answer Side -->
          <div
            class="absolute inset-0 w-full h-full backface-hidden rotate-y-180 bg-gradient-to-br from-green-50 to-green-100 flex items-center justify-center p-8"
          >
            <div class="text-center max-w-2xl">
              <div class="mb-6">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 mb-4">
                  Answer
                </span>
              </div>
              <h2 class="text-xl md:text-2xl font-semibold text-gray-900 leading-relaxed">
                {{ question.answer }}
              </h2>
              <div class="mt-8">
                <p class="text-sm text-gray-600">
                  Click the card to see the question again
                </p>
                <div class="mt-4">
                  <span class="inline-flex items-center px-4 py-2 rounded-lg bg-white bg-opacity-50 text-gray-700 text-sm font-medium">
                    👆 Click to flip back
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="bg-gray-50 px-6 py-4 border-t">
        <div class="flex justify-between items-center">
          <div class="flex space-x-3">
            <button
              @click="$emit('previous')"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              ← Previous
            </button>
            <button
              @click="$emit('next')"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Next →
            </button>
          </div>
          
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-600">Keyboard shortcuts:</span>
            <kbd class="px-2 py-1 text-xs font-semibold text-gray-800 bg-gray-200 border border-gray-300 rounded">Space</kbd>
            <span class="text-xs text-gray-500">to flip</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

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
const emit = defineEmits(['next', 'previous'])

// Reactive state
const isFlipped = ref(false)
const cardRef = ref(null)

// Methods
const flipCard = () => {
  isFlipped.value = !isFlipped.value
}

const shuffleQuestions = () => {
  // This would be handled by the parent component
  // For now, just flip back to question side
  isFlipped.value = false
}

// Reset flip state when question changes
watch(() => props.question, () => {
  isFlipped.value = false
})

// Keyboard navigation
const handleKeydown = (event) => {
  if (event.key === 'ArrowLeft') {
    emit('previous')
  } else if (event.key === 'ArrowRight') {
    emit('next')
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

