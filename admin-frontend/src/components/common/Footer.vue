<template>
  <footer class="footer">
    <div class="footer-content">
      <p>{{ t('footer.copyright') }}</p>
      <ul>
        <li>
          <a href="/privacy-policy">{{ t('footer.privacyPolicy') }}</a>
        </li>
        <li>
          <a href="/terms-of-service">{{ t('footer.termsOfService') }}</a>
        </li>
        <li>
          <a href="/contact">{{ t('footer.contactUs') }}</a>
        </li>
      </ul>
      <div class="social-media">
        <a href="https://facebook.com"
          ><i class="fab fa-facebook" style="color: #3b5998; font-size: 24px"></i
        ></a>
        <a href="https://twitter.com"
          ><i class="fab fa-twitter" style="color: #1da1f2; font-size: 24px"></i
        ></a>
        <a href="https://linkedin.com"
          ><i class="fab fa-linkedin" style="color: #0077b5; font-size: 24px"></i
        ></a>
        <a href="https://instagram.com"
          ><i class="fab fa-instagram" style="color: #e4405f; font-size: 24px"></i
        ></a>
        <a href="https://youtube.com"
          ><i class="fab fa-youtube" style="color: #ff0000; font-size: 24px"></i
        ></a>
        <a href="https://github.com"
          ><i class="fab fa-github" style="color: #333; font-size: 24px"></i
        ></a>
      </div>
    </div>
  </footer>
</template>

<script setup>
  import { useI18n } from 'vue-i18n'
  const { t } = useI18n()
</script>

<style>
  .footer {
    background-color: #f8f9fa; /* 浅色背景 */
    color: #333; /* 深色文字 */
    padding: 20px;
    text-align: left;
  }

  .footer-content {
    display: flex;
    justify-content: space-between; /* 使内容横向排列 */
    align-items: center;
  }

  .footer-content p {
    margin: 0;
  }

  .footer-content ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex; /* 使用 flexbox 使菜单项横向排列 */
  }

  .footer-content ul li {
    margin-right: 20px;
  }

  .footer-content a {
    color: #333;
    text-decoration: none;
  }

  .footer-content a:hover {
    color: #007bff; /* 悬停效果 */
  }

  .social-media a {
    margin: 0 10px;
    color: #333;
  }

  .social-media a:hover {
    color: #007bff; /* 社交媒体链接的悬停效果 */
  }
</style>
