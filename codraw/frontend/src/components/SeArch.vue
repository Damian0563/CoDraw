<template>
	<div v-if="loading" class="spinner-overlay">
		<VueSpinnerTail size="60" color="orange" />
	</div>
	<div class="main-layout">
		<SiDebar />
		<div class="flex-grow-1 d-flex justify-content-center align-items-start p-2 p-md-3">
			<div class="search-container border rounded justify-content-between flex-column"
				style="background-color: #ffc107;width:90%;min-height: 100vh;">
				<div class="text-center py-2">
					<h2 class="fw-bold mb-1">Browse Public Projects</h2>
					<p class="text-muted small mb-2">Find boards and ideas shared by the community</p>
				</div>
				<div class="row justify-content-center mx-2 mb-2">
					<div class="col-md-6 col-sm-10 col-12">
						<div class="input-group shadow-sm rounded mx-2">
							<input type="text" class="form-control border-0 p-3 minput" placeholder="Search public boards..."
								aria-label="Search public boards" v-model="input" @keyup.enter="search(input)">
								<button class="btn btn-primary" type="button" @click="search(input)">
									<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
										class="bi bi-search" viewBox="0 0 16 16">
										<path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001l3.85 3.85a1
									1 0 0 0 1.415-1.415l-3.85-3.85zm-5.242
									1.656a5.5 5.5 0 1 1 0-11 5.5
									5.5 0 0 1 0 11z" />
									</svg>
								</button>
						</div>
					</div>
				</div>
				<section id="results" class="mx-auto flex-grow-1">
					<div class="container mx-auto">
						<div class="row justify-content-center gap-2">
						<div v-for="(board, index) in popular" :key="index"
							:class="popular.length < 3 ? 'col-12 col-md-6 col-xl-4' : 'col-12 col-lg-4 col-xl-3'"
							class="card result-card project-card text-center"
							style="height: 22rem; width: 18rem; cursor: pointer; position: relative; overflow: hidden;" @click="join(board.room)">
							<div class="card-body d-flex flex-column card-with-preview" style="height: 100%; padding: 0;">
								<div class="preview-section">
									<div class="preview-image-container">
										<img :src="board.image" class="preview-image" alt="Preview of board" loading="lazy"
											decoding="async" v-if="board.image" />
										<div class="preview-image-container" v-else>
											<div class="text-center">
												<h5 class="card-title fw-bold mb-0" style="color: #ffc107; font-size: 0.875rem;">No Preview Available</h5>
											</div>
										</div>
									</div>
								</div>
								<div class="content-section">
									<h5 class="card-title fw-bold mb-2">{{ board.title }}</h5>
									<p class="card-text small">{{ board.description }}</p>
									<footer class="card-footer">
										<div class="text-start small">
											<span>Visibility: <span>Public</span></span>
										</div>
										<div class="d-flex justify-content-between small">
											<span>Views: <span>{{ board.views }}</span></span>
											<span>{{ board.modified }}</span>
										</div>
										<div class="text-start small">
											<span>Owner: <a :href="`/codraw/account/${board.owner}`" @click.stop
													style="color:#ff4f4f !important;">{{ board.owner }}</a></span>
										</div>
									</footer>
								</div>
							</div>
						</div>
							<div v-if="popular.length === 0" class="justify-content-center w-100 py-5">
								<text>No results found :(</text>
							</div>
						</div>
					</div>
				</section>
				<div class="d-flex justify-content-center mt-2 align-items-center gap-2 pagination-controls">
					<button class="btn btn-primary pagination-btn" :disabled="currentpage <= 1 || loading"
						@click="currentpage--; search(input)">
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
							<path fill-rule="evenodd"
								d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z" />
						</svg>
						Prev
					</button>
					<span class="pagination-info">Page {{ currentpage }}</span>
					<button class="btn btn-primary pagination-btn" :disabled="loading || popular.length < max_boards"
						@click="currentpage++; search(input)"> Next
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
							<path fill-rule="evenodd"
								d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z" />
						</svg>
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { get_cookie } from '@/common';
import { DateTime } from 'luxon'
import { BASE_URL } from '@/common'
import SiDebar from './SiDebar.vue'
import { VueSpinnerTail } from 'vue3-spinners'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const popular = ref([])
const input = ref('')
const csrf = get_cookie('csrftoken')
const currentpage = ref(1)
const max_boards = 10

async function search(sentence) {
	try {
		loading.value = true;
		if (sentence.length !== 0) {
			router.push({ path: '/codraw/search', query: { q: sentence, page: currentpage.value } })
			const data = await fetch(`${BASE_URL}/search`, {
				method: "POST",
				headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
				credentials: "include",
				body: JSON.stringify({
					"query": sentence,
					"timezone": DateTime.local().zoneName,
					"page": currentpage.value
				})
			})
			const response = await data.json()
			if (response.boards.length === 0) {
				popular.value = []
			}
			if (response.status === 200 && response.boards) {
				popular.value = JSON.parse(response.boards)
			}
		} else {
			await load_popular()
		}
		loading.value = false
	} catch (e) {
		loading.value = false
	}
}

async function load_popular() {
	try {
		router.push({ path: '/codraw/search', query: { page: currentpage.value } })
		const data = await fetch(`${BASE_URL}/get_popular`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrf
			},
			body: JSON.stringify({
				"timezone": DateTime.local().zoneName,
				"page": currentpage.value
			}),
			credentials: "include"
		})
		const response = await data.json()
		if (response.boards.length === 0) {
			popular.value = []
		} else {
			popular.value = response.boards
		}
	} catch (e) {
		console.error(e)
	}
}

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
			window.location.href = `${response.url}?origin=search?page=${currentpage.value}?q=${input.value}`
		}
	} catch (e) {
		console.error(e)
	}
}

onMounted(async () => {
	loading.value = true
	const query = route.query
	if (query.q) {
		input.value = query.q
		currentpage.value = parseInt(query.page) || 1
		await search(input.value)
	} else {
		await load_popular()
	}
	loading.value = false
})
</script>


<style scoped>
.minput:focus {
	outline: none;
	box-shadow: none;
}

.search-container {
	display: flex;
	flex-direction: column;
	justify-content: space-between;
}

.project-card,
.result-card {
	height: 16rem;
	min-height: 16rem;
	cursor: pointer;
	transition: all 0.2s ease;
	border: 1px solid #374151;
	border-radius: 0.75rem;
	background: #1f2937;
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
	width: 100%;
}

@media (min-width: 480px) {

	.project-card,
	.result-card {
		height: 17rem;
		min-height: 17rem;
	}
}

@media (min-width: 640px) {

	.project-card,
	.result-card {
		height: 18rem;
		min-height: 18rem;
	}
}

@media (min-width: 768px) {

	.project-card,
	.result-card {
		height: 22rem;
		min-height: 22rem;
	}
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
	background-color: rgba(255, 255, 255, 0.8);
}

.result-card .card-body {
	height: 100%;
	padding: 1rem;
	display: flex;
	flex-direction: column;
	color: #e5e7eb;
}

@media (min-width: 640px) {
	.result-card .card-body {
		padding: 1.25rem;
	}
}

@media (min-width: 1024px) {
	.result-card .card-body {
		padding: 1.5rem;
	}
}

.result-card .card-title {
	font-size: 0.9375rem;
	font-weight: 600;
	margin-bottom: 0.5rem;
	color: #f9fafb;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

@media (min-width: 640px) {
	.result-card .card-title {
		font-size: 1rem;
	}
}

.result-card .card-text {
	font-size: 0.8125rem;
	color: #9ca3af;
	line-height: 1.4;
	flex-grow: 1;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

@media (min-width: 640px) {
	.result-card .card-text {
		font-size: 0.875rem;
	}
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

.main-layout {
	display: flex;
	min-height: 100vh;
	width: 100%;
	background: #181818;
}

.result-card:hover {
	transform: translateY(-2px);
	box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
	border-color: #ffc107;
}

.pagination-controls {
	padding: 0.75rem;
}

.pagination-btn {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0.5rem 1rem;
	background: #374151;
	border: 1px solid #4b5563;
	color: #e5e7eb;
	font-weight: 500;
	transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
	background: #ffc107;
	border-color: #ffc107;
	color: #1f2937;
}

.pagination-btn:disabled {
	opacity: 0.4;
	cursor: not-allowed;
	background: #374151;
	border-color: #4b5563;
}

.pagination-info {
	color: #9ca3af;
	font-size: 0.9rem;
	padding: 0 1rem;
}

#results {
	height: auto
}

.card-with-preview {
	display: flex;
	flex-direction: column;
	height: 100%;
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
	min-height: 4rem;
	width: 100%;
}

.preview-section .preview-image {
	max-width: 100%;
	max-height: 100%;
	width: 100%;
	height: 100%;
	object-fit: contain;
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
</style>
