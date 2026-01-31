<template>
	<div v-if="loading" class="spinner-overlay">
		<VueSpinnerTail size="60" color="orange" />
	</div>
	<div class="main-layout">
		<SiDebar/>
		<div class="flex-grow-1 d-flex justify-content-center align-items-start p-3 p-md-5">
			<div class="my-5 border rounded justify-content-center" style="background-color: #ffc107;width:90%;height: 110vh;">
				<div class="text-center mb-4">
					<h2 class="fw-bold mt-4">Browse Public Projects</h2>
					<p class="text-muted">Find boards and ideas shared by the community</p>
				</div>
				<div class="row justify-content-center mx-2">
					<div class="col-md-6 col-sm-10 col-12">
						<div class="input-group shadow-sm rounded mx-2">
							<input
								type="text"
								class="form-control border-0 p-3"
								placeholder="Search public boards..."
								aria-label="Search public boards"
								v-model="input"
								@keyup.enter="search(input)"
							>
							<button class="btn btn-primary" type="button" @click="search(input)">
								<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
									class="bi bi-search" viewBox="0 0 16 16">
									<path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001l3.85 3.85a1
										1 0 0 0 1.415-1.415l-3.85-3.85zm-5.242
										1.656a5.5 5.5 0 1 1 0-11 5.5
										5.5 0 0 1 0 11z"/>
								</svg>
							</button>
						</div>
					</div>
				</div>
				<section id="results" class="my-4 mx-3">
					<div class="container">
						<div class="row g-1 justify-content-start gap-2">
							<div
								v-for="(board, index) in popular"
								:key="index"
								:class="popular.length < 3 ? 'col-12 col-md-6 col-xl-4' : 'col-12 col-lg-4 col-xl-3'"
								class="card result-card project-card text-center"
								style="height: 20rem; width: 18rem; cursor: pointer; position: relative;"
								@click="join(board.room)"
							>
								<div class="card-body d-flex flex-column" style="height: 100%;">
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
											Owner: <a :href="`/codraw/account/${board.owner}`" @click.stop style="color:#ff4f4f !important;">{{ board.owner }}</a>
										</div>
									</footer>
								</div>
							</div>
							<div v-if="popular.length===0" class="justify-content-center" style="min-height: 12rem;">
								<text>No results found :(</text>
							</div>
						</div>
					</div>
				</section>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { get_cookie } from '@/common';
import {DateTime} from 'luxon'
import {BASE_URL} from '@/common'
import SiDebar from './SiDebar.vue'
import {VueSpinnerTail} from 'vue3-spinners'
const loading = ref(false)
const popular=ref([])
const input=ref('')
const csrf=get_cookie('csrftoken')

async function search(sentence){
  try{
    loading.value=true;
    const data=await fetch(`${BASE_URL}/search`,{
      method:"POST",
      headers:{"Content-Type":"application/json","X-CSRFToken":csrf},
      credentials:"include",
      body:JSON.stringify({
        "query":sentence,
        "timezone":DateTime.local().zoneName
      })
    })
    const response=await data.json()
    if(response.status===200){
      popular.value=JSON.parse(response.boards)
    }
    loading.value=false
  }catch(e){
    console.error(e)
  }
}

async function load_popular(){
  try{
    const data=await fetch(`${BASE_URL}/get_popular`,{
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        "X-CSRFToken":csrf
      },
      body:JSON.stringify({
        "timezone":DateTime.local().zoneName
      }),
      credentials:"include"
    })
    const response=await data.json()
    popular.value=response.boards
  }catch(e){
    console.error(e)
  }
}

async function join(room){
  try{
    const data=await fetch(`${BASE_URL}/load`,{
      "method":"POST",
      "headers":{
        'Content-Type':'application/json',
        'X-CSRFToken':csrf
      },
      credentials:"include",
      body:JSON.stringify({
        "room":room
      })
    })
    const response=await data.json()
    if(response.status===200){
      window.location.href=`${response.url}?origin=search`
    }
  }catch(e){
    console.error(e)
  }
}

onMounted(async() => {
  loading.value=true
  await load_popular()
  loading.value=false
})
</script>


<style scoped>
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
    height: 20rem;
    min-height: 20rem;
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
.result-card:hover{
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
  border-color: #ffc107;
}
</style>
