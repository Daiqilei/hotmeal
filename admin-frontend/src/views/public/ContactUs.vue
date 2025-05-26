<template>
  <div class="contact-us">
    <h1>Contact Us</h1>
    <p>
      {{ t('contactUs.description') }}
      {{ emailAddress }}}
    </p>
  </div>
</template>

<script setup>
  import { useI18n } from 'vue-i18n'
  const { t } = useI18n()

  const emailAddress = 'daiqilei233@gmail.com'
</script>

<style>
  .contact-us {
    text-align: center;
  }
</style>
