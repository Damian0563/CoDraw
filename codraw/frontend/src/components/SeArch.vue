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
								class="card result-card text-center bg-dark"
								style="height: 15rem; width: 15rem; cursor: pointer; position: relative;"
								@click="join(board.room)"
							>
								<div class="card-body d-flex flex-column txtcard" style="height: 100%;">
									<h5 class="card-title fw-bold mb-2">{{ board.title }}</h5>
									<p class="card-text small">{{ board.description }}</p>
									<footer
										class="mt-auto py-2 px-2"
										style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.05); border-top: 1px solid #ffc107;"
									>
										<div class="d-flex justify-content-between small">
											<span>Views: <span class="txtcard">{{ board.views }}</span></span>
											<span class="txtcard">{{ board.modified }}</span>
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
      window.location.href=`${response.url}`
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
.project-card, .result-card {
  transition: 0.3s ease-in-out;
  border: 1px solid #ffc10744;
  border-radius: 0.75rem;
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

.txtcard{
  color: #ffc107;
}
.main-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background: #181818;
}
.result-card:hover{
  background-color: white !important;
  color: #000 !important;
  transform: translateY(-4px);
  box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
  border-color: black;
  .txtcard{
    color: black;
  }
  .card-title{
    color: black;
  }
}
</style>
