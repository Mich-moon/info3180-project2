import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


const app = createApp(App)

// 2. Assign the global variable before mounting
app.config.globalProperties.$logged_in = false

app.use(router)

app.mount('#app')
