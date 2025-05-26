/**
 * @file            src/stores/appStore.js
 * @description
 * @author          taichilei
 * @date            2025-05-03
 * @version         1.0.0
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore(
  'app',
  () => {
    const language = ref('zh')
    const theme = ref('light')
    const isLoading = ref(false)

    function setLanguage(lang) {
      language.value = lang
    }

    function toggleTheme() {
      theme.value = theme.value === 'light' ? 'dark' : 'light'
    }

    function setLoading(status) {
      isLoading.value = status
    }

    return {
      language,
      theme,
      isLoading,
      setLanguage,
      toggleTheme,
      setLoading,
    }
  },
  {
    persist: true,
  },
)
