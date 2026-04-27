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
import LearnMore from './components/LearnMore.vue';
import NotFound from './components/NotFound.vue'
import SeArch from './components/SeArch.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createGtag } from "vue-gtag"
import { faTextHeight, faMicrophoneSlash, faMicrophone, faPhoneSlash, faPhone, faCircle, faFont, faRotateLeft, faSquare, faBookOpen, faArrowUpLong, faPalette, faHome, faBolt, faLightbulb, faUndo, faRedo, faSearch, faUser, faEye, faPencil, faFeatherPointed, faPaintBrush, faPaintRoller, faHand, faExclamationTriangle, faLink, faBookmark, faTrash, faExpand, faCompress } from '@fortawesome/free-solid-svg-icons'
import { faGithub } from '@fortawesome/free-brands-svg-icons'
library.add(faPalette, faMicrophoneSlash, faMicrophone, faPhoneSlash, faPhone, faCircle, faFont, faRotateLeft, faTextHeight, faBookOpen, faArrowUpLong, faSquare, faHome, faBolt, faLightbulb, faUndo, faRedo, faSearch, faExclamationTriangle, faUser, faEye, faPencil, faFeatherPointed, faPaintBrush, faPaintRoller, faGithub, faHand, faLink, faBookmark, faTrash, faExpand, faCompress)

const routes = [
	{ path: '/', component: HeRo, meta: { showNav: true, canonical: true } },
	{ path: '/signup', component: SignUp, meta: { showNav: true } },
	{ path: '/signin', component: SignIn, meta: { showNav: true } },
	{ path: '/codraw', component: MaIn, meta: { showNav: false } },
	{ path: '/codraw/search', component: SeArch, meta: { showNav: false } },
	{ path: '/codraw/account/:username', component: AccOunt, meta: { showNav: false } },
	{ path: '/board/:id/:room', component: BoArd, meta: { showNav: false } },
	{ path: '/demo/:room', component: BoArd, meta: { showNav: false } },
	{ path: '/learn-more', component: LearnMore, meta: { showNav: true } },
	{ path: '/recover/:code', component: RestorePassword, meta: { showNav: true } },
	{ path: '/:pathMatch(.*)*', component: NotFound, meta: { showNav: true } }
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

const BASE_URL = 'https://codrawapp.com'
router.afterEach((to) => {
	window.scrollTo({ top: 0, behavior: 'instant' });
	let canonicalUrl = BASE_URL + to.path;
	if (canonicalUrl.length > 1 && canonicalUrl.endsWith('/')) {
		canonicalUrl = canonicalUrl.slice(0, -1);
	}
	let link = document.querySelector('link[rel="canonical"]');
	if (!link) {
		link = document.createElement('link');
		link.rel = 'canonical';
		document.head.appendChild(link);
	}
	link.setAttribute('href', canonicalUrl);
});

createApp(App)
	.use(router)
	.use(
		createGtag({
			tagId: process.env.VUE_APP_GTAG,
			config: {
				params: {
					debug_mode: true,
					app_name: "CoDraw"
				}
			},
			pageTracker: {
				router,
				useScreenview: true
			}
		})
	)
	.use(VueKonva)
	.component('font-awesome-icon', FontAwesomeIcon)
	.mount('#app');
