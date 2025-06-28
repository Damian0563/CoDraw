import { createApp } from 'vue'
import App from './App.vue'
import VueKonva from 'vue-konva';
import { createWebHistory, createRouter } from 'vue-router'

import SignIn from './components/SignIn.vue'
import SignUp from './components/SignUp.vue'

const routes = [
  { path: '/signup', component: SignUp },
  { path: '/signin', component: SignIn },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


createApp(App).use(router).use(VueKonva).mount('#app')
