/**
 * @file            i18n/index.js
 * @description     多语言配置
 * @author          taichilei
 * @date            2025-04-17
 * @version         2.0.0
 */

import { createI18n } from 'vue-i18n'

// English modules
import enCommon from './en/common'
import enAuth from './en/auth'
import enDashboard from './en/dashboard'
import enCharts from './en/charts'
import enDiningArea from './en/diningArea'
import enDish from './en/dish'
import enFooter from './en/footer'
import enContactUs from './en/contactUs'
import enOrder from './en/order'
import enUser from './en/user'
import enNavigator from './en/navigator' // Added import for English navigator
// Chinese modules
import zhCommon from './zh/common'
import zhAuth from './zh/auth'
import zhDashboard from './zh/dashboard'
import zhCharts from './zh/charts'
import zhDiningArea from './zh/diningArea'
import zhDish from './zh/dish'
import zhFooter from './zh/footer'
import zhContactUs from './zh/contactUs'
import zhOrder from './zh/order'
import zhUser from './zh/user'
import zhNavigator from './zh/navigator' // Added import for Chinese navigator

const messages = {
  en: {
    common: enCommon,
    auth: enAuth,
    dashboard: enDashboard,
    charts: enCharts,
    diningArea: enDiningArea,
    dish: enDish,
    footer: enFooter,
    contactUs: enContactUs,
    order: enOrder,
    user: enUser,
    navigator: enNavigator, // Added navigator to English messages
  },
  zh: {
    common: zhCommon,
    auth: zhAuth,
    dashboard: zhDashboard,
    charts: zhCharts,
    diningArea: zhDiningArea,
    dish: zhDish,
    footer: zhFooter,
    contactUs: zhContactUs,
    order: zhOrder,
    user: zhUser,
    navigator: zhNavigator, // Added navigator to Chinese messages
  },
}

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: 'zh',
  fallbackLocale: 'en',
  messages,
})

export default i18n
