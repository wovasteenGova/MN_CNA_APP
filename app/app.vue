<template>
  <UApp class="dark">
    <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <!-- Header -->
      <UContainer class="py-4 sm:py-8 px-4">
        <div class="text-center mb-6 sm:mb-8">
          <div class="inline-flex items-center justify-center w-12 h-12 sm:w-16 sm:h-16 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-2xl mb-3 sm:mb-4 shadow-lg">
            <UIcon name="i-heroicons-academic-cap" class="w-6 h-6 sm:w-8 sm:h-8 text-white" />
          </div>
          <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold bg-gradient-to-r from-teal-600 to-cyan-600 bg-clip-text text-transparent mb-2 px-2">
            Minnesota CNA Study App
          </h1>
          <p class="text-base sm:text-lg text-slate-600 dark:text-slate-300 mb-4 px-2">
            Master your Certified Nursing Assistant exam with confidence (10th edition Mosby's Textbook)
          </p>
          
          <!-- Home and Donate Buttons -->
          <div class="flex justify-center gap-3 sm:gap-4">
            <UButton
              @click="goBackToChapters"
              color="teal"
              variant="soft"
              size="lg"
              icon="i-heroicons-home"
              class="bg-gradient-to-r from-teal-100 to-cyan-100 hover:from-teal-200 hover:to-cyan-200 dark:from-teal-900/50 dark:to-cyan-900/50 text-teal-700 dark:text-teal-300 border-0 shadow-md hover:shadow-lg transition-all duration-200"
              :ui="{ rounded: 'rounded-full' }"
            >
              Home
            </UButton>
            
            <UButton
              @click="showDonationModal = true"
              color="amber"
              variant="soft"
              size="lg"
              icon="i-heroicons-heart"
              class="bg-gradient-to-r from-amber-100 to-yellow-100 hover:from-amber-200 hover:to-yellow-200 dark:from-amber-900/50 dark:to-yellow-900/50 text-amber-700 dark:text-amber-300 border-0 shadow-md hover:shadow-lg transition-all duration-200"
              :ui="{ rounded: 'rounded-full' }"
            >
              Donate
            </UButton>
          </div>
        </div>

      <!-- Chapter Selection -->
      <div v-if="!selectedChapter" class="space-y-8">
        <!-- Overall Progress Summary -->
        <UCard v-if="Object.keys(chapterProgress).length > 0" class="bg-gradient-to-r from-teal-50/80 to-cyan-50/80 dark:from-slate-800/90 dark:to-slate-700/90 backdrop-blur-sm border border-slate-200/50 dark:border-slate-600/50">
          <template #header>
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-lg">
                <UIcon name="i-heroicons-chart-bar" class="w-5 h-5 text-white" />
              </div>
              <h2 class="text-xl font-bold text-slate-800 dark:text-slate-100">Your Study Progress</h2>
            </div>
          </template>
          
          <div class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="text-center p-4 bg-white/60 dark:bg-slate-800/60 rounded-lg backdrop-blur-sm">
                <div class="text-3xl font-bold text-teal-600 dark:text-teal-400 mb-2">
                  {{ Object.keys(chapterProgress).length }}
                </div>
                <div class="text-sm font-medium text-slate-600 dark:text-slate-400">
                  Chapters Started
                </div>
              </div>
              
              <div class="text-center p-4 bg-white/60 dark:bg-slate-800/60 rounded-lg backdrop-blur-sm">
                <div class="text-3xl font-bold text-emerald-600 dark:text-emerald-400 mb-2">
                  {{ getTotalQuestionsStudied() }}
                </div>
                <div class="text-sm font-medium text-slate-600 dark:text-slate-400">
                  Questions Studied
                </div>
              </div>
              
              <div class="text-center p-4 bg-white/60 dark:bg-slate-800/60 rounded-lg backdrop-blur-sm">
                <div class="text-3xl font-bold text-amber-600 dark:text-amber-400 mb-2">
                  {{ getOverallAccuracy() }}%
                </div>
                <div class="text-sm font-medium text-slate-600 dark:text-slate-400">
                  Overall Accuracy
                </div>
              </div>
            </div>
            
            <div class="flex justify-center">
              <UButton
                @click="resetProgress"
                color="red"
                variant="soft"
                size="sm"
                icon="i-heroicons-arrow-path"
                class="text-red-600 dark:text-red-400"
              >
                Reset All Progress
              </UButton>
            </div>
          </div>
        </UCard>
        
        <div class="text-center">
          <h2 class="text-2xl font-semibold text-slate-800 dark:text-slate-100 mb-4">
            Select a Chapter to Study
          </h2>
          <p class="text-slate-600 dark:text-slate-300">
            Choose from the available CNA study chapters below
          </p>
        </div>

        <!-- Chapter Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 px-2 sm:px-0">
          <!-- Loading State -->
          <div v-if="chapters.length === 0" class="col-span-full text-center py-12">
            <UIcon name="i-heroicons-arrow-path" class="w-12 h-12 text-teal-500 animate-spin mx-auto mb-4" />
            <p class="text-slate-600 dark:text-slate-400">Loading chapters...</p>
          </div>
          
          <!-- Chapter Cards -->
          <UCard
            v-for="(chapter, index) in chapters"
            :key="index"
            @click="selectChapter(chapter)"
            class="cursor-pointer hover:shadow-2xl transition-all duration-300 hover:scale-105 hover:border-teal-300 dark:hover:border-teal-500 bg-white/80 dark:bg-slate-800/90 backdrop-blur-sm border border-slate-200/50 dark:border-slate-700/50"
            :ui="{ 
              body: { padding: 'p-4 sm:p-6' },
              header: { padding: 'p-4 sm:p-6 pb-3 sm:pb-4' }
            }"
          >
            <template #header>
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-lg sm:text-xl font-bold text-slate-800 dark:text-slate-100 leading-tight">
                  {{ chapter.chapter }}
                </h3>
                <UBadge color="teal" variant="soft" size="md" class="bg-gradient-to-r from-teal-100 to-cyan-100 dark:from-teal-900/50 dark:to-cyan-900/50 text-teal-700 dark:text-teal-300 border-0 text-xs sm:text-sm">
                  {{ chapter.questions.length }} questions
                </UBadge>
              </div>
              
              <!-- Progress Display -->
              <div class="space-y-3">
                <!-- Always show progress section, but different content based on progress -->
                <div v-if="getChapterProgressStats(chapter.chapter).studied > 0" class="space-y-2">
                  <!-- Big Bold Progress Percentage -->
                  <div class="text-center">
                    <div class="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-teal-600 to-cyan-600 bg-clip-text text-transparent mb-1">
                      {{ getChapterProgressStats(chapter.chapter).percentage }}%
                    </div>
                    <div class="text-xs sm:text-sm font-medium text-slate-600 dark:text-slate-400">
                      {{ getChapterProgressStats(chapter.chapter).studied }}/{{ chapter.questions.length }} questions studied
                    </div>
                  </div>
                  
                  <!-- Progress Bar -->
                  <div class="w-full bg-slate-200 dark:bg-slate-600 rounded-full h-3 overflow-hidden">
                    <div
                      class="bg-gradient-to-r from-teal-500 to-cyan-500 h-full rounded-full transition-all duration-500 ease-out"
                      :style="{ width: getChapterProgressStats(chapter.chapter).percentage + '%' }"
                    ></div>
                  </div>
                  
                  <!-- Accuracy Display -->
                  <div class="flex justify-center">
                    <div class="text-center px-3 py-1 bg-emerald-100 dark:bg-emerald-900/30 rounded-full">
                      <span class="text-sm font-semibold text-emerald-700 dark:text-emerald-300">
                        {{ getChapterProgressStats(chapter.chapter).accuracy }}% accuracy
                      </span>
                    </div>
                  </div>
                </div>
                
                <!-- No Progress State -->
                <div v-else class="text-center py-2">
                  <div class="text-2xl font-bold text-slate-400 dark:text-slate-500 mb-1">0%</div>
                  <div class="text-sm text-slate-500 dark:text-slate-400">Not started</div>
                </div>
              </div>
            </template>

            <div class="space-y-6">
              <div class="flex items-center space-x-2 text-slate-600 dark:text-slate-400">
                <UIcon name="i-heroicons-academic-cap" class="w-5 h-5 text-teal-600 dark:text-teal-400" />
                <p class="text-sm font-medium">
                  {{ getChapterProgressStats(chapter.chapter).studied > 0 ? 'Continue studying' : 'Ready to start studying' }}
                </p>
              </div>
              
              <div class="flex items-center justify-between">
                <UButton
                  color="teal"
                  variant="solid"
                  size="sm"
                  icon="i-heroicons-play"
                  class="font-semibold bg-gradient-to-r from-teal-600 to-cyan-600 hover:from-teal-700 hover:to-cyan-700 shadow-lg hover:shadow-xl transition-all duration-200"
                >
                  Start Studying
                </UButton>
                <UButton
                  color="slate"
                  variant="ghost"
                  size="sm"
                  icon="i-heroicons-information-circle"
                  class="text-slate-600 dark:text-slate-400 hover:text-teal-600 dark:hover:text-teal-400"
                >
                  Info
                </UButton>
              </div>
            </div>
          </UCard>
        </div>
      </div>

      <!-- Study Interface -->
      <div v-else class="space-y-8">
        <!-- Study Header -->
        <UCard class="bg-gradient-to-r from-teal-50/80 to-cyan-50/80 dark:from-slate-800/90 dark:to-slate-700/90 backdrop-blur-sm border border-slate-200/50 dark:border-slate-600/50">
          <template #header>
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 class="text-3xl font-bold text-slate-800 dark:text-slate-100">
                  {{ selectedChapter.chapter }}
                </h2>
                <p class="text-slate-600 dark:text-slate-300 mt-2 flex items-center space-x-2">
                  <UIcon name="i-heroicons-document-text" class="w-4 h-4 text-teal-600 dark:text-teal-400" />
                  <span>{{ currentQuestionIndex + 1 }} of {{ selectedChapter.questions.length }} questions</span>
                </p>
              </div>
              
              <!-- Study Mode Toggle -->
              <div class="mt-4 sm:mt-0">
                <div class="flex bg-white/80 dark:bg-slate-700/80 rounded-lg p-1 shadow-sm border border-slate-200/50 dark:border-slate-600/50 backdrop-blur-sm">
                  <UButton
                    @click="studyMode = 'flashcard'"
                    :color="studyMode === 'flashcard' ? 'teal' : 'slate'"
                    :variant="studyMode === 'flashcard' ? 'solid' : 'ghost'"
                    size="sm"
                    icon="i-heroicons-rectangle-stack"
                    :class="[
                      'font-medium transition-all duration-200',
                      studyMode === 'flashcard' ? 'bg-gradient-to-r from-teal-600 to-cyan-600 shadow-md' : 'text-slate-600 dark:text-slate-400'
                    ]"
                  >
                    Flashcards
                  </UButton>
                  <UButton
                    @click="studyMode = 'quiz'"
                    :color="studyMode === 'quiz' ? 'teal' : 'slate'"
                    :variant="studyMode === 'quiz' ? 'solid' : 'ghost'"
                    size="sm"
                    icon="i-heroicons-question-mark-circle"
                    :class="[
                      'font-medium transition-all duration-200',
                      studyMode === 'quiz' ? 'bg-gradient-to-r from-teal-600 to-cyan-600 shadow-md' : 'text-slate-600 dark:text-slate-400'
                    ]"
                  >
                    Quiz
                  </UButton>
                </div>
              </div>
            </div>
          </template>

          <div class="space-y-6">
            <!-- Progress Bar -->
            <div>
              <div class="flex justify-between text-sm font-medium text-slate-600 dark:text-slate-300 mb-3">
                <span class="flex items-center space-x-2">
                  <UIcon name="i-heroicons-chart-bar" class="w-4 h-4 text-teal-600 dark:text-teal-400" />
                  <span>Progress</span>
                </span>
                <span class="font-bold text-teal-600 dark:text-teal-400">
                  {{ progressPercentage }}% ({{ currentQuestionIndex + 1 }}/{{ selectedChapter.questions.length }})
                </span>
              </div>
              <!-- Custom Progress Bar -->
              <div class="w-full bg-slate-200 dark:bg-slate-600 rounded-full h-3 overflow-hidden shadow-inner">
                <div
                  class="bg-gradient-to-r from-teal-500 to-cyan-500 h-full rounded-full transition-all duration-500 ease-out shadow-sm"
                  :style="{ width: progressPercentage + '%' }"
                ></div>
              </div>
            </div>

            <!-- Study Components -->
            <UCard v-if="studyMode === 'flashcard'" class="bg-gradient-to-br from-teal-50/50 to-cyan-50/50 dark:from-slate-800/80 dark:to-slate-700/80 border-teal-200/50 dark:border-slate-600/50 backdrop-blur-sm">
              <template #header>
                <div class="flex items-center space-x-3">
                  <div class="p-2 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-lg">
                    <UIcon name="i-heroicons-rectangle-stack" class="w-5 h-5 text-white" />
                  </div>
                  <h3 class="text-2xl font-bold text-slate-800 dark:text-slate-100">Flashcard Mode</h3>
                </div>
              </template>

              <div class="space-y-6">
                <!-- Question Card - Always visible and clickable -->
                <UCard 
                  @click="toggleAnswer" 
                  class="bg-white/90 dark:bg-slate-800/90 shadow-lg cursor-pointer hover:shadow-2xl transition-all duration-300 hover:scale-[1.02] border border-slate-200/50 dark:border-slate-600/50 backdrop-blur-sm hover:border-teal-300 dark:hover:border-teal-500"
                >
                  <div class="p-8">
                    <div class="flex items-center justify-between mb-4">
                      <div class="flex items-center space-x-2">
                        <UIcon name="i-heroicons-question-mark-circle" class="w-5 h-5 text-teal-600 dark:text-teal-400" />
                        <h4 class="text-lg font-semibold text-slate-800 dark:text-slate-100">Question</h4>
                      </div>
                      <div class="text-sm text-slate-500 dark:text-slate-400 flex items-center space-x-1">
                        <UIcon name="i-heroicons-cursor-arrow-rays" class="w-4 h-4" />
                        <span>Click to {{ showAnswer ? 'hide' : 'reveal' }} answer</span>
                      </div>
                    </div>
                    <p class="text-lg text-slate-700 dark:text-slate-300 leading-relaxed">{{ currentQuestion?.question }}</p>
                  </div>
                </UCard>
                
                <!-- Answer Card - Only visible when clicked -->
                <Transition
                  enter-active-class="transition-all duration-300 ease-out"
                  enter-from-class="opacity-0 transform scale-95"
                  enter-to-class="opacity-100 transform scale-100"
                  leave-active-class="transition-all duration-200 ease-in"
                  leave-from-class="opacity-100 transform scale-100"
                  leave-to-class="opacity-0 transform scale-95"
                >
                  <UCard v-show="showAnswer" class="bg-gradient-to-br from-emerald-50/80 to-green-50/80 dark:from-emerald-900/30 dark:to-green-900/30 border-emerald-200/50 dark:border-emerald-700/50 shadow-lg backdrop-blur-sm">
                    <div class="p-8">
                      <div class="flex items-center space-x-2 mb-4">
                        <div class="p-1.5 bg-gradient-to-br from-emerald-500 to-green-600 rounded-lg">
                          <UIcon name="i-heroicons-check-circle" class="w-4 h-4 text-white" />
                        </div>
                        <h4 class="text-lg font-semibold text-emerald-800 dark:text-emerald-300">Answer</h4>
                      </div>
                      <p class="text-lg text-emerald-700 dark:text-emerald-300 leading-relaxed">{{ currentQuestion?.answer }}</p>
                    </div>
                  </UCard>
                </Transition>
              </div>
            </UCard>
            
            <UCard v-else class="bg-gradient-to-br from-amber-50/50 to-orange-50/50 dark:from-slate-800/80 dark:to-slate-700/80 border-amber-200/50 dark:border-slate-600/50 backdrop-blur-sm">
              <template #header>
                <div class="flex items-center space-x-3">
                  <div class="p-2 bg-gradient-to-br from-amber-500 to-orange-600 rounded-lg">
                    <UIcon name="i-heroicons-question-mark-circle" class="w-5 h-5 text-white" />
                  </div>
                  <h3 class="text-2xl font-bold text-slate-800 dark:text-slate-100">Quiz Mode</h3>
                </div>
              </template>

              <div class="space-y-6">
                <UCard class="bg-white/90 dark:bg-slate-800/90 shadow-lg backdrop-blur-sm border border-slate-200/50 dark:border-slate-600/50">
                  <div class="p-8">
                    <div class="flex items-center space-x-2 mb-4">
                      <UIcon name="i-heroicons-question-mark-circle" class="w-5 h-5 text-amber-600 dark:text-amber-400" />
                      <h4 class="text-lg font-semibold text-slate-800 dark:text-slate-100">Question</h4>
                    </div>
                    <p class="text-lg text-slate-700 dark:text-slate-300 leading-relaxed">{{ currentQuestion?.question }}</p>
                  </div>
                </UCard>
                
                <div class="space-y-4">
                  <h4 class="text-lg font-semibold text-slate-800 dark:text-slate-100 flex items-center space-x-2">
                    <UIcon name="i-heroicons-list-bullet" class="w-5 h-5 text-amber-600 dark:text-amber-400" />
                    <span>Answer Choices</span>
                  </h4>
                  <div class="grid gap-3">
                    <UCard 
                      v-for="(choice, index) in currentQuestion?.choices" 
                      :key="index" 
                      @click="selectQuizAnswer(choice)"
                      :class="[
                        'cursor-pointer transition-all duration-200 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm border border-slate-200/50 dark:border-slate-600/50',
                        !showResult ? 'hover:shadow-lg hover:scale-[1.02] hover:border-amber-300 dark:hover:border-amber-500' : '',
                        showResult && isChoiceCorrect(choice) ? 'border-emerald-400 bg-emerald-50/80 dark:bg-emerald-900/30 shadow-lg' : '',
                        showResult && choice === selectedAnswer && !isChoiceCorrect(choice) ? 'border-red-400 bg-red-50/80 dark:bg-red-900/30 shadow-lg' : '',
                        showResult && choice !== selectedAnswer && !isChoiceCorrect(choice) ? 'opacity-60' : ''
                      ]"
                    >
                      <div class="p-6">
                        <div class="flex items-center justify-between">
                          <div class="flex items-center space-x-4">
                            <UBadge 
                              :color="
                                showResult && isChoiceCorrect(choice) ? 'emerald' :
                                showResult && choice === selectedAnswer && !isChoiceCorrect(choice) ? 'red' :
                                'amber'
                              " 
                              variant="solid" 
                              size="lg" 
                              class="font-bold shadow-sm"
                            >
                              {{ String.fromCharCode(65 + index) }}
                            </UBadge>
                            <span class="text-lg text-slate-700 dark:text-slate-300 flex-1">{{ choice }}</span>
                          </div>
                          
                          <!-- Result Icons -->
                          <div v-if="showResult" class="flex items-center">
                            <UIcon 
                              v-if="isChoiceCorrect(choice)"
                              name="i-heroicons-check-circle" 
                              class="w-6 h-6 text-emerald-600 dark:text-emerald-400"
                            />
                            <UIcon 
                              v-else-if="choice === selectedAnswer"
                              name="i-heroicons-x-circle" 
                              class="w-6 h-6 text-red-600 dark:text-red-400"
                            />
                          </div>
                        </div>
                      </div>
                    </UCard>
                  </div>
                  
                  <!-- Result Message -->
                  <Transition
                    enter-active-class="transition-all duration-300 ease-out"
                    enter-from-class="opacity-0 transform scale-95"
                    enter-to-class="opacity-100 transform scale-100"
                    leave-active-class="transition-all duration-200 ease-in"
                    leave-from-class="opacity-100 transform scale-100"
                    leave-to-class="opacity-0 transform scale-95"
                  >
                    <UCard v-if="showResult" :class="[
                      'mt-4 backdrop-blur-sm shadow-lg',
                      isCorrectAnswer ? 'bg-emerald-50/80 dark:bg-emerald-900/30 border-emerald-200/50 dark:border-emerald-700/50' : 'bg-red-50/80 dark:bg-red-900/30 border-red-200/50 dark:border-red-700/50'
                    ]">
                      <div class="p-6 text-center">
                        <div class="flex items-center justify-center space-x-2 mb-2">
                          <div :class="[
                            'p-2 rounded-full',
                            isCorrectAnswer ? 'bg-emerald-500' : 'bg-red-500'
                          ]">
                            <UIcon 
                              :name="isCorrectAnswer ? 'i-heroicons-check-circle' : 'i-heroicons-x-circle'" 
                              class="w-6 h-6 text-white"
                            />
                          </div>
                          <h3 :class="[
                            'text-xl font-bold',
                            isCorrectAnswer ? 'text-emerald-800 dark:text-emerald-300' : 'text-red-800 dark:text-red-300'
                          ]">
                            {{ isCorrectAnswer ? 'Correct!' : 'Incorrect!' }}
                          </h3>
                        </div>
                        <p :class="[
                          'text-lg',
                          isCorrectAnswer ? 'text-emerald-700 dark:text-emerald-300' : 'text-red-700 dark:text-red-300'
                        ]">
                          {{ isCorrectAnswer ? 'Great job! You got it right.' : `The correct answer is: "${currentQuestion?.answer}"` }}
                        </p>
                      </div>
                    </UCard>
                  </Transition>
                </div>
              </div>
            </UCard>

            <!-- Navigation -->
            <div class="flex justify-between items-center pt-6">
              <UButton
                @click="goBackToChapters"
                color="slate"
                variant="soft"
                size="lg"
                icon="i-heroicons-arrow-left"
                class="font-semibold text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200"
              >
                Back to Chapters
              </UButton>
              
              <div class="flex space-x-4">
                <UButton
                  @click="previousQuestion"
                  :disabled="currentQuestionIndex === 0"
                  color="slate"
                  variant="outline"
                  size="lg"
                  icon="i-heroicons-chevron-left"
                  class="font-semibold border-slate-300 dark:border-slate-600"
                >
                  Previous
                </UButton>
                <UButton
                  @click="nextQuestion"
                  :disabled="currentQuestionIndex === selectedChapter.questions.length - 1"
                  color="teal"
                  size="lg"
                  icon="i-heroicons-chevron-right"
                  trailing
                  class="font-semibold bg-gradient-to-r from-teal-600 to-cyan-600 hover:from-teal-700 hover:to-cyan-700 shadow-lg hover:shadow-xl transition-all duration-200"
                >
                  Next
                </UButton>
              </div>
            </div>
          </div>
        </UCard>
      </div>
    </UContainer>
    
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
              <!-- PayPal - Disabled (Uncomment when ready) -->
              <!-- 
              UNCOMMENT THIS WHEN PAYPAL LINK IS READY:
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
              -->
              
              <!-- TEMPORARY DISABLED VERSION (DELETE WHEN READY) -->
              <button 
                @click="openDonationLink('paypal')"
                class="group p-6 bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-800/20 dark:to-slate-700/20 rounded-xl border-2 border-slate-200 dark:border-slate-600 opacity-60 cursor-not-allowed transition-all duration-200"
              >
                <div class="text-center">
                  <div class="w-12 h-12 mx-auto mb-3 bg-slate-400 rounded-lg flex items-center justify-center">
                    <span class="text-white font-bold text-lg">P</span>
                  </div>
                  <h4 class="font-semibold text-slate-600 dark:text-slate-400 mb-2">PayPal</h4>
                  <p class="text-sm text-slate-500 dark:text-slate-500">
                    Coming Soon...
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
  </UApp>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Set page title and force dark mode
useHead({
  title: 'MN CNA APP',
  meta: [
    { name: 'description', content: 'Minnesota CNA Study App - Master your Certified Nursing Assistant exam with confidence' }
  ],
  htmlAttrs: {
    class: 'dark'
  }
})

// Router
const router = useRouter()

// Reactive state
const chapters = ref([])
const selectedChapter = ref(null)
const currentQuestionIndex = ref(0)
const studyMode = ref('flashcard')
const userAnswers = ref({})
const isLoading = ref(true)
const showAnswer = ref(false)
const selectedAnswer = ref(null)
const showResult = ref(false)
const chapterProgress = ref({})
const showDonationModal = ref(false)

// Computed properties
const currentQuestion = computed(() => {
  if (!selectedChapter.value) return null
  return selectedChapter.value.questions[currentQuestionIndex.value]
})

const progressPercentage = computed(() => {
  if (!selectedChapter.value || selectedChapter.value.questions.length === 0) return 0
  return Math.round(((currentQuestionIndex.value + 1) / selectedChapter.value.questions.length) * 100)
})

const isCorrectAnswer = computed(() => {
  if (!currentQuestion.value || selectedAnswer.value === null) return null
  
  // Use the same logic as isChoiceCorrect for consistency
  return isChoiceCorrect(selectedAnswer.value)
})

// Progress tracking functions
const loadProgress = () => {
  if (typeof window !== 'undefined') {
    const savedProgress = localStorage.getItem('cna-study-progress')
    if (savedProgress) {
      try {
        const parsed = JSON.parse(savedProgress)
        chapterProgress.value = parsed
      } catch (e) {
        console.error('Error loading progress:', e)
        chapterProgress.value = {}
      }
    }
  }
}

const saveProgress = () => {
  if (process.client) {
    localStorage.setItem('cna-study-progress', JSON.stringify(chapterProgress.value))
  }
}

const updateProgress = (chapterName, questionIndex, isCorrect = null) => {
  if (!chapterProgress.value[chapterName]) {
    chapterProgress.value[chapterName] = {
      questionsStudied: new Set(),
      correctAnswers: new Set(),
      lastStudied: Date.now(),
      totalQuestions: selectedChapter.value?.questions.length || 0
    }
  }
  
  const progress = chapterProgress.value[chapterName]
  progress.questionsStudied.add(questionIndex)
  progress.lastStudied = Date.now()
  progress.totalQuestions = selectedChapter.value?.questions.length || 0
  
  if (isCorrect === true) {
    progress.correctAnswers.add(questionIndex)
  } else if (isCorrect === false) {
    progress.correctAnswers.delete(questionIndex)
  }
  
  // Convert Sets to Arrays for localStorage
  const progressToSave = {}
  Object.keys(chapterProgress.value).forEach(key => {
    const chapterData = chapterProgress.value[key]
    progressToSave[key] = {
      ...chapterData,
      questionsStudied: Array.from(chapterData.questionsStudied),
      correctAnswers: Array.from(chapterData.correctAnswers)
    }
  })
  
  if (typeof window !== 'undefined') {
    localStorage.setItem('cna-study-progress', JSON.stringify(progressToSave))
  }
}

const getChapterProgressStats = (chapterName) => {
  const progress = chapterProgress.value[chapterName]
  if (!progress) {
    return { studied: 0, correct: 0, total: 0, percentage: 0, accuracy: 0 }
  }
  
  const studied = Array.isArray(progress.questionsStudied) 
    ? progress.questionsStudied.length 
    : progress.questionsStudied?.size || 0
  const correct = Array.isArray(progress.correctAnswers) 
    ? progress.correctAnswers.length 
    : progress.correctAnswers?.size || 0
  const total = progress.totalQuestions || 0
  
  const stats = {
    studied,
    correct,
    total,
    percentage: total > 0 ? Math.round((studied / total) * 100) : 0,
    accuracy: studied > 0 ? Math.round((correct / studied) * 100) : 0
  }
  
  return stats
}

const getTotalQuestionsStudied = () => {
  let total = 0
  Object.values(chapterProgress.value).forEach(progress => {
    const studied = Array.isArray(progress.questionsStudied) 
      ? progress.questionsStudied.length 
      : progress.questionsStudied.size
    total += studied
  })
  return total
}

const getOverallAccuracy = () => {
  let totalStudied = 0
  let totalCorrect = 0
  
  Object.values(chapterProgress.value).forEach(progress => {
    const studied = Array.isArray(progress.questionsStudied) 
      ? progress.questionsStudied.length 
      : progress.questionsStudied.size
    const correct = Array.isArray(progress.correctAnswers) 
      ? progress.correctAnswers.length 
      : progress.correctAnswers.size
    
    totalStudied += studied
    totalCorrect += correct
  })
  
  return totalStudied > 0 ? Math.round((totalCorrect / totalStudied) * 100) : 0
}

const resetProgress = () => {
  if (confirm('Are you sure you want to reset all progress? This cannot be undone.')) {
    chapterProgress.value = {}
    if (typeof window !== 'undefined') {
      localStorage.removeItem('cna-study-progress')
    }
  }
}

const cleanupOldProgress = () => {
  // Remove progress for chapters that no longer exist
  const validChapterNames = chapters.value.map(c => c.chapter)
  const progressKeys = Object.keys(chapterProgress.value)
  
  progressKeys.forEach(chapterName => {
    if (!validChapterNames.includes(chapterName)) {
      console.log(`Removing progress for deleted chapter: ${chapterName}`)
      delete chapterProgress.value[chapterName]
    }
  })
  
  // Save cleaned progress
  if (typeof window !== 'undefined' && progressKeys.length > Object.keys(chapterProgress.value).length) {
    const progressToSave = {}
    Object.keys(chapterProgress.value).forEach(key => {
      const chapterData = chapterProgress.value[key]
      progressToSave[key] = {
        ...chapterData,
        questionsStudied: Array.isArray(chapterData.questionsStudied) 
          ? chapterData.questionsStudied 
          : Array.from(chapterData.questionsStudied),
        correctAnswers: Array.isArray(chapterData.correctAnswers) 
          ? chapterData.correctAnswers 
          : Array.from(chapterData.correctAnswers)
      }
    })
    localStorage.setItem('cna-study-progress', JSON.stringify(progressToSave))
  }
}


// Helper function to check if a choice is the correct answer
const isChoiceCorrect = (choice) => {
  if (!currentQuestion.value) return false
  
  const normalizeString = (str) => {
    return str
      .replace(/\s+/g, ' ')
      .replace(/[()]/g, '') // Remove parentheses
      .replace(/\btransfer\b/gi, '') // Remove "transfer" word
      .replace(/\bslightly\s+/gi, '') // Remove "slightly"
      .replace(/\bbehind\s+and\s+to\s+one\s+side/gi, 'beside') // Convert "behind and to one side" to "beside"
      .replace(/\bto\s+one\s+side/gi, 'beside')
      .trim()
      .toLowerCase()
  }
  
  const choiceNormalized = normalizeString(choice)
  const correctNormalized = normalizeString(currentQuestion.value.answer)
  
  // First try exact match
  if (choiceNormalized === correctNormalized) {
    return true
  }
  
  // Medical terminology exceptions - be more strict with medical terms
  const medicalTerms = [
    'serosanguineous', 'sanguineous', 'serous', 'purulent', 
    'excoriation', 'abrasion', 'laceration', 'contusion',
    'hematoma', 'ecchymosis', 'petechiae', 'macule', 'papule', 'vesicle', 'pustule',
    'edema', 'erythema', 'cyanosis', 'pallor', 'jaundice',
    'hypertension', 'hypotension', 'tachycardia', 'bradycardia',
    'dyspnea', 'apnea', 'tachypnea', 'bradypnea',
    'hyperthermia', 'hypothermia', 'pyrexia', 'febrile',
    'anorexia', 'nausea', 'vomiting', 'diarrhea', 'constipation',
    'incontinence', 'retention', 'dysuria', 'hematuria',
    'syncope', 'seizure', 'convulsion', 'tremor',
    'paralysis', 'paresis', 'spasticity', 'flaccidity',
    'dementia', 'delirium', 'confusion', 'disorientation',
    'depression', 'anxiety', 'agitation', 'lethargy',
    'infection', 'inflammation', 'sepsis', 'shock',
    'fracture', 'dislocation', 'sprain', 'strain',
    'ulcer', 'gangrene', 'necrosis', 'ischemia',
    'thrombosis', 'embolism', 'hemorrhage', 'bleeding',
    'anemia', 'leukemia', 'thrombocytopenia', 'coagulation',
    'diabetes', 'hypoglycemia', 'hyperglycemia', 'ketoacidosis',
    'pneumonia', 'bronchitis', 'asthma', 'copd',
    'myocardial', 'infarction', 'angina', 'arrhythmia',
    'stroke', 'cerebrovascular', 'transient', 'ischemic',
    'alzheimer', 'parkinson', 'multiple', 'sclerosis',
    'arthritis', 'osteoporosis', 'osteomyelitis', 'bursitis',
    'cancer', 'tumor', 'malignant', 'benign', 'metastasis',
    'chemotherapy', 'radiation', 'surgery', 'anesthesia',
    'medication', 'drug', 'dose', 'administration',
    'side', 'effect', 'adverse', 'reaction', 'allergy',
    'contraindication', 'interaction', 'toxicity', 'overdose',
    // Add stage numbers and time periods
    'stage', 'hour', 'minute', 'second', 'time', 'duration',
    'pathogen', 'non-pathogen', 'contamination', 'cross-contamination',
    'circumcised', 'uncircumcised', 'am', 'pm', 'day', 'care',
    'active', 'assistive', 'range', 'motion', 'exercise',
    'flexion', 'extension', 'dorsiflexion', 'hyperextension',
    'nrem', 'rem', 'sleep', 'gastritis', 'gastritiss'
  ]
  const hasMedicalTerms = medicalTerms.some(term => 
    choiceNormalized.includes(term) || correctNormalized.includes(term)
  )
  
  // For medical terms, only allow exact matches or very specific exceptions
  if (hasMedicalTerms) {
    // Specific algorithm exceptions for known problematic cases
    const exceptions = [
      // Handle gait belt variations
      { 
        choice: 'Apply a gait belt and walk slightly behind and to one side', 
        answer: 'Apply a gait (transfer) belt and walk slightly behind and to one side', 
        shouldMatch: true 
      },
      { 
        choice: 'Apply a gait belt', 
        answer: 'Apply a gait (transfer) belt', 
        shouldMatch: true 
      },
      { 
        choice: 'Apply a gait (transfer) belt and walk slightly behind and to one side', 
        answer: 'Apply a gait belt and walk slightly behind and to one side', 
        shouldMatch: true 
      },
      { 
        choice: 'Apply a gait (transfer) belt', 
        answer: 'Apply a gait belt', 
        shouldMatch: true 
      }
    ]
    
    // Check if this is an exception case
    const isException = exceptions.some(exception => 
      normalizeString(exception.choice) === choiceNormalized && 
      normalizeString(exception.answer) === correctNormalized
    )
    
    if (isException) {
      const exception = exceptions.find(ex => 
        normalizeString(ex.choice) === choiceNormalized && 
        normalizeString(ex.answer) === correctNormalized
      )
      return exception.shouldMatch
    }
    
    // For medical terms without exceptions, only allow exact matches
    return false
  }
  
  // For non-medical terms, use the original smart matching logic
  // Try partial containment match (but be more careful)
  const lengthRatio = Math.min(choiceNormalized.length, correctNormalized.length) / Math.max(choiceNormalized.length, correctNormalized.length)
  if (lengthRatio > 0.8) { // Only if strings are similar in length
    if (correctNormalized.includes(choiceNormalized) || choiceNormalized.includes(correctNormalized)) {
      return true
    }
  }
  
  // Smart matching: Check if first 3-5 significant words match
  const getSignificantWords = (str) => {
    return str.split(' ')
      .filter(word => word.length > 2 && !['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'way', 'she', 'use', 'her', 'man', 'oil', 'sit', 'set', 'run', 'eat', 'far', 'sea', 'eye', 'walk', 'apply'].includes(word))
      .slice(0, 5) // Take first 5 significant words
  }
  
  const choiceWords = getSignificantWords(choiceNormalized)
  const correctWords = getSignificantWords(correctNormalized)
  
  // Check if at least 80% of significant words match (higher threshold for non-medical terms)
  if (choiceWords.length > 0 && correctWords.length > 0) {
    const minLength = Math.min(choiceWords.length, correctWords.length)
    let matchingWords = 0
    
    choiceWords.slice(0, minLength).forEach((word, index) => {
      if (correctWords[index] && (word.includes(correctWords[index]) || correctWords[index].includes(word))) {
        matchingWords++
      }
    })
    
    const matchPercentage = matchingWords / minLength
    return matchPercentage >= 0.8 // 80% match threshold (more strict)
  }
  
  return false
}

// Methods
const selectChapter = (chapter) => {
  selectedChapter.value = chapter
  currentQuestionIndex.value = 0
  userAnswers.value = {}
  showAnswer.value = false // Reset answer visibility
  selectedAnswer.value = null
  showResult.value = false
}

const goBackToChapters = () => {
  selectedChapter.value = null
  currentQuestionIndex.value = 0
  userAnswers.value = {}
  showAnswer.value = false
  selectedAnswer.value = null
  showResult.value = false
}




const openDonationLink = (platform) => {
  // Real donation links
  const donationLinks = {
    paypal: null, // ADD YOUR PAYPAL LINK HERE WHEN READY: 'https://paypal.me/yourusername'
    venmo: 'https://venmo.com/code?user_id=2972961464123392287&created=1758939359',
    cashapp: 'https://cash.app/$WovaGova'
  }
  
  const link = donationLinks[platform]
  
  // Don't allow PayPal clicks until link is ready
  if (platform === 'paypal') {
    alert('PayPal link coming soon! Please use Venmo or Cash App for now.')
    return
  }
  
  if (link && typeof window !== 'undefined') {
    window.open(link, '_blank')
  }
  
  // Close the modal after clicking
  showDonationModal.value = false
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < selectedChapter.value.questions.length - 1) {
    currentQuestionIndex.value++
    showAnswer.value = false // Reset answer visibility
    selectedAnswer.value = null // Reset quiz answer
    showResult.value = false
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    showAnswer.value = false // Reset answer visibility
    selectedAnswer.value = null // Reset quiz answer
    showResult.value = false
  }
}

const toggleAnswer = () => {
  showAnswer.value = !showAnswer.value
  
  // Track progress when viewing answer in flashcard mode
  if (showAnswer.value && selectedChapter.value) {
    updateProgress(selectedChapter.value.chapter, currentQuestionIndex.value)
  }
}

const handleAnswer = (answer) => {
  userAnswers.value[currentQuestionIndex.value] = answer
}

const selectQuizAnswer = (choice) => {
  if (showResult.value) return // Prevent multiple selections
  
  selectedAnswer.value = choice
  showResult.value = true
  userAnswers.value[currentQuestionIndex.value] = choice
  
  // Track progress
  const isCorrect = isChoiceCorrect(choice)
  updateProgress(selectedChapter.value.chapter, currentQuestionIndex.value, isCorrect)
}

const loadData = async () => {
  isLoading.value = true
  try {
    const response = await fetch('/questions.json')
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    chapters.value = data
  } catch (error) {
    console.error('Error loading questions:', error)
    chapters.value = []
  } finally {
    isLoading.value = false
  }
}

// Initialize data
onMounted(async () => {
  // Force dark mode on all devices
  if (typeof window !== 'undefined') {
    document.documentElement.classList.add('dark')
    document.body.classList.add('dark')
  }
  
  await loadData()
  loadProgress()
  
  // Convert arrays back to Sets for progress tracking
  Object.keys(chapterProgress.value).forEach(chapterName => {
    const progress = chapterProgress.value[chapterName]
    if (Array.isArray(progress.questionsStudied)) {
      progress.questionsStudied = new Set(progress.questionsStudied)
    }
    if (Array.isArray(progress.correctAnswers)) {
      progress.correctAnswers = new Set(progress.correctAnswers)
    }
  })
  
  // Clean up progress for chapters that no longer exist
  cleanupOldProgress()
})
</script>

<style>
@import "tailwindcss";
@import "@nuxt/ui";

/* Basic styles for the CNA Study App */
.perspective-1000 {
  perspective: 1000px;
}

.transform-style-preserve-3d {
  transform-style: preserve-3d;
}

.backface-hidden {
  backface-visibility: hidden;
}

.rotate-y-180 {
  transform: rotateY(180deg);
}

/* Smooth transitions */
.transition-transform {
  transition: transform 0.7s ease-in-out;
}

/* Focus styles for accessibility */
[role="button"]:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* KBD styling */
kbd {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
}

/* Smooth transitions */
.transition-all {
  transition: all 0.2s ease-in-out;
}
</style>


