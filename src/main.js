import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import SimpleVueComponents from 'simple-vue-components'
import 'simple-vue-components/style.css'

createApp(App).use(SimpleVueComponents).use(router).mount('#app')
