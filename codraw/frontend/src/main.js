import { createApp } from 'vue'
import App from './App.vue'
import VueKonva from 'vue-konva';
import { createWebHistory, createRouter } from 'vue-router'

import SignIn from './components/SignIn.vue'
import SignUp from './components/SignUp.vue'
import HeRo from './components/Hero.vue'
import MaIn from './components/Main.vue'
import AccOunt from './components/AccOunt.vue'
import BoArd from './components/BoArd.vue'
import RestorePassword from './components/RestorePassword.vue'
import DemoBoard from './components/DemoBoard.vue'
import LearnMore from './components/LearnMore.vue';
import NotFound from './components/NotFound.vue'
import SeArch from './components/SeArch.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createGtag } from "vue-gtag"
import { faPalette, faHome, faBolt, faLightbulb, faUndo, faRedo, faSearch, faUser, faEye, faPencil, faFeatherPointed, faPaintBrush, faPaintRoller, faHand, faExclamationTriangle } from '@fortawesome/free-solid-svg-icons'
import { faGithub } from '@fortawesome/free-brands-svg-icons'
library.add(faPalette, faHome, faBolt, faLightbulb, faUndo, faRedo, faSearch, faExclamationTriangle, faUser, faEye, faPencil, faFeatherPointed, faPaintBrush, faPaintRoller, faGithub, faHand)

const routes = [
	{ path: '/', component: HeRo, meta: { showNav: true } },
	{ path: '/signup', component: SignUp, meta: { showNav: true } },
	{ path: '/signin', component: SignIn, meta: { showNav: true } },
	{ path: '/codraw', component: MaIn, meta: { showNav: false } },
	{ path: '/codraw/search', component: SeArch, meta: { showNav: false } },
	{ path: '/codraw/account/:username', component: AccOunt, meta: { showNav: false } },
	{ path: '/board/:id/:room', component: BoArd, meta: { showNav: false } },
	{ path: '/demo', component: DemoBoard, meta: { showNav: false } },
	{ path: '/learn-more', component: LearnMore, meta: { showNav: true } },
	{ path: '/recover/:code', component: RestorePassword, meta: { showNav: true } },
	{ path: '/:pathMatch(.*)*', component: NotFound, meta: { showNav: true } }
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

createApp(App).use(router).use(createGtag, { config: { "id": "G-QW19P198KB" }, router }).use(VueKonva).component('font-awesome-icon', FontAwesomeIcon).mount('#app')
