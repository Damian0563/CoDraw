<template>
	<div class="main-layout">
		<SiDebar />
		<main class="main-content flex-grow-1">
			<RouterView />
			<h1 style="color:#ffc107" class="mb-4">Welcome to CoDraw!</h1>
			<div class="mb-4">
				<div id="projects" class="container">
					<div class="card create-project-card my text-center" @click="create()">
						<div class="card-body d-flex flex-column align-items-center justify-content-center">
							<span class="create-icon">+</span>
							<h5 class="card-title mt-2 mb-0">Create Project</h5>
						</div>
					</div>
					<div v-for="(board, index) in boards" :key="index" class="card project-card text-center"
						@click="join(board.room)">
						<div class="card-body d-flex flex-column card-with-preview">
							<div class="preview-section" v-if="images[board.room] && !previewing[board.room]">
								<div class="preview-image-container">
									<img :src="images[board.room]" class="preview-image" alt="Preview of board" loading="lazy"
										decoding="async" />
								</div>
								<!-- <font-awesome-icon :icon="['fas', 'eye-slash']" class="preview-toggle text-start" -->
								<!-- 	@click="togglePreview($event, board.room)" title="Hide preview" /> -->
							</div>
							<div class="content-section">
								<h5 class="card-title fw-bold mb-2">{{ board.title }}</h5>
								<p class="card-text small">{{ board.description }}</p>
								<footer class="card-footer">
									<div class="text-start small">
										<span>Visibility: <span>{{ board.visibility }}</span></span>
									</div>
									<div class="d-flex justify-content-between small ">
										<span>Views: <span>{{ board.views }}</span></span>
									</div>
									<div class="text-start small">
										<span>{{ board.modified }}</span>
									</div>
								</footer>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div v-if="loading" class="spinner-overlay">
				<VueSpinnerTail size="60" color="orange" />
			</div>
		</main>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { get_cookie } from '@/common';
import { BASE_URL } from '../common.js'
import SiDebar from './SiDebar.vue'
import { VueSpinnerTail } from 'vue3-spinners'
import { DateTime } from 'luxon'

const loading = ref(false)
const csrf = get_cookie('csrftoken')
const boards = ref([])
const username = ref("")
const images = ref({})
const previewing = ref({})
async function get_username() {
	try {
		const data = await fetch(`${BASE_URL}/username`, {
			method: "GET",
			headers: {
				"X-CSRFToken": csrf
			},
			credentials: "include"
		})
		const response = await data.json()
		if (response.status == 200) username.value = response.username
		else username.value = "ERROR 404 NOT FOUND"
	} catch (e) {
		console.error(e)
	}
}
async function status() {
	try {
		const data = await fetch(`${BASE_URL}/codraw/`, {
			method: 'GET',
			headers: { 'X-CSRFToken': csrf },
			credentials: 'include'
		});
		const response = await data.json();
		if (response.status !== 200 && window.location.pathname !== '/') {
			window.location.href = '/';
		}
	} catch (e) {
		console.error(e);
	}
}

const get_boards = async () => {
	try {
		const data = await fetch(`${BASE_URL}/codraw/get_boards`, {
			method: "POST",
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrf
			},
			body: JSON.stringify({
				"timezone": DateTime.local().zoneName
			}),
			credentials: "include"
		})
		const response = await data.json()
		boards.value = response.boards
		images.value = response.images
		previewing.value = response.boards.reduce((acc, board) => {
			acc[board.room] = false
			return acc
		}, {})
	} catch (e) {
		console.error(e)
	}
}
//
// const togglePreview = (event, room) => {
// 	event.stopPropagation()
// 	previewing.value[room] = !previewing.value[room]
// }

async function join(room) {
	try {
		const data = await fetch(`${BASE_URL}/load`, {
			"method": "POST",
			"headers": {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrf
			},
			credentials: "include",
			body: JSON.stringify({
				"room": room
			})
		})
		const response = await data.json()
		if (response.status === 200) {
			window.location.href = `${response.url}?origin=default`
		}
	} catch (e) {
		console.error(e)
	}
}

async function create() {
	try {
		const data = await fetch(`${BASE_URL}/get_project_url`, {
			method: "GET",
			headers: {
				"Content-Type": 'application/json',
				"X-CSRFToken": csrf
			},
			credentials: "include"
		})
		const response = await data.json()
		if (response.status === 200) {
			window.location.href = `${response.url}?origin=default`
		}
		else {
			console.log('error')
		}
	} catch (e) {
		console.error(e)
	}
}

onMounted(async () => {
	loading.value = true
	await Promise.all([
		status(),
		get_boards(),
		get_username()
	])
	loading.value = false
})
</script>

<script>
export default {
	name: 'MaIn',
}
</script>

<style scoped>
#projects {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
	gap: 1.25rem;
	width: 100%;
	min-width: 0;
	padding: 0;
	justify-items: stretch;
	align-items: stretch;
}

@media (max-width: 479px) {
	#projects {
		padding: 0 0.25rem;
		grid-template-columns: repeat(auto-fill, minmax(18rem, 1fr));
	}
}

@media (min-width: 480px) {
	#projects {
		grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
		gap: 1.25rem;
		padding: 0;
		font-size: 0.4rem;
	}
}

@media (min-width: 640px) {
	#projects {
		grid-template-columns: repeat(auto-fill, minmax(22rem, 1fr));
		gap: 1.25rem;
		padding: 0;
		font-size: 0.4rem;
	}
}

@media (min-width: 768px) and (max-width: 991px) {
	#projects {
		grid-template-columns: 1fr;
		gap: 1.25rem;
		padding: 0;
		font-size: 0.9rem;
		max-width: 28rem;
		margin: 0 auto;
	}
}

@media (min-width: 992px) {
	#projects {
		grid-template-columns: repeat(auto-fill, minmax(22rem, 1fr));
		gap: 1.25rem;
		padding: 0;
		font-size: 0.9rem;
	}
}

@media (min-width: 1024px) {
	#projects {
		grid-template-columns: repeat(auto-fill, 24rem);
		gap: 1.5rem;
	}
}

@media (min-width: 1280px) {
	#projects {
		grid-template-columns: repeat(auto-fill, 24rem);
		gap: 1.5rem;
	}
}

@media (min-width: 1600px) {
	#projects {
		grid-template-columns: repeat(auto-fill, 26rem);
		gap: 1.5rem;
	}
}

@media (min-width: 1920px) {
	#projects {
		grid-template-columns: repeat(auto-fill, 28rem);
		gap: 1.5rem;
	}
}


.project-card,
.create-project-card {
	height: 22rem;
	min-height: 22rem;
	min-width: 0;
	max-width: 100%;
	cursor: pointer;
	transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
	border: 1px solid #374151;
	border-radius: 0.75rem;
	background: #1f2937;
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
	width: 100%;
	overflow: hidden;
	box-sizing: border-box;
	position: relative;
	contain: layout style paint;
}

@media (min-width: 480px) {

	.project-card,
	.create-project-card {
		height: 23rem;
		min-height: 23rem;
	}
}

@media (min-width: 640px) {

	.project-card,
	.create-project-card {
		height: 24rem;
		min-height: 24rem;
	}
}

@media (min-width: 768px) {

	.project-card,
	.create-project-card {
		height: 25rem;
		min-height: 25rem;
	}
}

.project-card:hover,
.create-project-card:hover {
	transform: translateY(-2px);
	box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
	border-color: #ffc107;
}

.card-footer {
	margin-top: auto;
	padding-top: 0.75rem;
	border-top: 1px solid #374151;
}

@media (min-width: 640px) {
	.card-footer {
		padding-top: 1rem;
	}
}

.card-footer span {
	color: #9ca3af;
	font-size: 0.7rem;
}

@media (min-width: 480px) {
	.card-footer span {
		font-size: 0.725rem;
	}
}

@media (min-width: 640px) {
	.card-footer span {
		font-size: 0.8125rem;
	}
}

.card-footer span span {
	color: #d1d5db;
	font-weight: 500;
}

.create-project-card .card-body {
	height: 100%;
}

.create-icon {
	font-size: 3rem;
	color: #ffc107;
	font-weight: 300;
	line-height: 1;
}

@media (min-width: 480px) {
	.create-icon {
		font-size: 3.25rem;
	}
}

@media (min-width: 640px) {
	.create-icon {
		font-size: 3.5rem;
	}
}

@media (min-width: 768px) {
	.create-icon {
		font-size: 3.75rem;
	}
}

@media (min-width: 1024px) {
	.create-icon {
		font-size: 4rem;
	}
}

.create-project-card .card-title {
	font-size: 0.875rem;
	font-weight: 500;
	color: #9ca3af;
	margin-top: 0.5rem;
}

@media (min-width: 640px) {
	.create-project-card .card-title {
		font-size: 0.9375rem;
		margin-top: 0.75rem;
	}
}

.create-project-card:hover .card-title {
	color: #ffc107;
}

.spinner-overlay {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
	z-index: 1000;
	background-color: rgba(0, 0, 0, 0.7);
}

.main-layout {
	display: flex;
	min-height: 100vh;
	width: 100%;
	background: #111827;
}

.main-content {
	flex: 1;
	background: #111827;
	padding: 1.5rem 1rem;
	overflow-y: auto;
}



.preview-toggle.preview-active {
	color: white;
}

.preview-image {
	max-width: 100%;
	max-height: calc(100% - 3rem);
	width: 100%;
	height: auto;
	object-fit: contain;
	flex-shrink: 1;
}

.card-with-preview {
	display: flex;
	flex-direction: column;
	height: 100%;
	padding: 0;
}

.preview-section {
	flex: 1 1 auto;
	display: flex;
	flex-direction: column;
	min-height: 0;
	padding: 0.25rem 0.5rem;
	position: relative;
}

.preview-section .preview-image-container {
	flex: 1;
	display: flex;
	align-items: center;
	justify-content: center;
	overflow: hidden;
	min-height: 0;
	width: 100%;
}

.preview-section .preview-image {
	max-width: 100%;
	max-height: 100%;
	width: 100%;
	height: 100%;
	object-fit: contain;
}

.preview-section .preview-toggle {
	position: absolute;
	top: 0.25rem;
	right: 0.25rem;
	font-size: 0.75rem;
	padding: 0.35rem;
	color: #ffc107;
	cursor: pointer;
	z-index: 10;
	background: rgba(31, 41, 55, 0.8);
	border-radius: 0.25rem;
}

.content-section {
	flex-shrink: 0;
	padding: 0.75rem;
	background: #1f2937;
	border-top: 1px solid #374151;
}

.content-section .card-title {
	font-size: 1rem;
	font-weight: 600;
	margin-bottom: 0.25rem;
	color: #f9fafb;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.content-section .card-text {
	font-size: 0.875rem;
	color: #9ca3af;
	line-height: 1.3;
	margin-bottom: 0.5rem;
	display: -webkit-box;
	-webkit-line-clamp: 1;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

.content-section .card-footer {
	margin-top: 0;
	padding-top: 0.5rem;
	border-top: 1px solid #374151;
}

@media (min-width: 640px) {
	.main-content {
		padding: 2rem 1.5rem;
	}
}

@media (min-width: 768px) {
	.main-content {
		padding: 2.25rem 1.75rem;
	}
}

@media (min-width: 1024px) {
	.main-content {
		padding: 2.5rem 2rem;
	}
}
</style>
