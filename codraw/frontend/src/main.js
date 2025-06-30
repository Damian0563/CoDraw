import { createApp } from 'vue'
import App from './App.vue'
import VueKonva from 'vue-konva';
import { createWebHistory, createRouter } from 'vue-router'

import SignIn from './components/SignIn.vue'
import SignUp from './components/SignUp.vue'
import HeRo from './components/Hero.vue'
import MaIn from './components/Main.vue'
import SeTtings from './components/SeTtings.vue'
import AccOunt from './components/AccOunt.vue'
import BoArd from './components/BoArd.vue'

const routes = [
  { path: '/', component: HeRo },
  { path: '/signup', component: SignUp },
  { path: '/signin', component: SignIn },
  { path: '/codraw', component: MaIn },
  { path: '/codraw/settings', component: SeTtings },
  { path: '/codraw/account', component: AccOunt },
  { path: '/board/:id/:room', component: BoArd },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


createApp(App).use(router).use(VueKonva).mount('#app')
