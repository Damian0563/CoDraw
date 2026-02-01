<template>
  <div class="main-layout">
    <SiDebar/>
    <main class="main-content flex-grow-1">
      <RouterView />
      <h1 style="color:#ffc107">Welcome to CoDraw!</h1>
      <div class="mb-4">
        <h2 class="mb-4 text-start" style="color:#ffc107">My Projects</h2>
        <div id="projects" class="container">
          <div
            class="card create-project-card my text-center"
            @click="create()"
          >
            <div class="card-body d-flex flex-column align-items-center justify-content-center">
              <span class="create-icon">+</span>
              <h5 class="card-title mt-2 mb-0">Create Project</h5>
            </div>
          </div>
          <div
            v-for="(board, index) in boards"
            :key="index"
            class="card project-card text-center"
            @click="join(board.room)"
          >
            <div class="card-body d-flex flex-column">
							<font-awesome-icon v-if="images[board.room]" :icon="['fas', 'eye']" class="text-start" style="font-size: 0.8rem;padding:0.5rem ;color: #ffc107;"/>
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
      <div v-if="loading" class="spinner-overlay">
        <VueSpinnerTail size="60" color="orange" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { get_cookie } from '@/common';
import {BASE_URL} from '../common.js'
import SiDebar from './SiDebar.vue'
import {VueSpinnerTail} from 'vue3-spinners'
import {DateTime} from 'luxon'

const loading = ref(false)
const hover=ref({})
const csrf=get_cookie('csrftoken')
const boards = ref([])
const username = ref("")
const images = ref({})
async function get_username(){
  try{
    const data=await fetch(`${BASE_URL}/username`,{
      method:"GET",
      headers:{
        "X-CSRFToken":csrf
      },
      credentials:"include"
    })
    const response=await data.json()
    if(response.status==200) username.value=response.username
    else username.value="ERROR 404 NOT FOUND"
  }catch(e){
    console.error(e)
  }
}
async function status(){
  try {
    const data = await fetch(`${BASE_URL}/codraw/`, {
      method: 'GET',
      headers:{'X-CSRFToken':csrf},
      credentials: 'include'
    });
    const response = await data.json();
    if(response.status !== 200 &&  window.location.pathname !== '/'){
      window.location.href = '/';
    }
  } catch (e) {
    console.error(e);
  }
}

const get_boards = async()=>{
  try{
    const data=await fetch(`${BASE_URL}/codraw/get_boards`,{
      method:"POST",
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrf
      },
      body:JSON.stringify({
        "timezone":DateTime.local().zoneName
      }),
      credentials:"include"
    })
    const response=await data.json()
    boards.value=response.boards
		images.value=response.images
    hover.value=response.boards.map(()=>false)
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
      window.location.href=`${response.url}?origin=default`
    }
  }catch(e){
    console.error(e)
  }
}

async function create(){
  try{
    const data=await fetch(`${BASE_URL}/get_project_url`,{
        method:"GET",
        headers:{
          "Content-Type":'application/json',
          "X-CSRFToken":csrf
        },
        credentials:"include"
    })
    const response= await data.json()
    if(response.status===200){
      window.location.href=`${response.url}`
    }
    else{
      console.log('error')
    }
  }catch(e){
    console.error(e)
  }
}

onMounted(async() => {
  loading.value=true
  await Promise.all([
    status(),
    get_boards(),
    get_username()
  ])
  loading.value=false
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
  grid-template-columns: 1fr;
  gap: 1rem;
  width: 100%;
  padding: 0 0.5rem;
}

@media (min-width: 480px) {
  #projects {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    padding: 0;
		font-size: 0.4rem;
  }
}

@media (min-width: 640px) {
  #projects {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.1rem;
		padding: 0;
		font-size: 0.4rem;
  }
}

@media (min-width: 768px) {
  #projects {
    grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
    gap: 0.5rem;
		padding: 0;
		font-size: 0.9rem;
  }
}

@media (min-width: 1024px) {
  #projects {
    grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
    gap: 1rem;
  }
}

@media (min-width: 1280px) {
  #projects {
    grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
    gap: 1rem;
  }
}

.project-card,
.create-project-card {
  height: 12rem;
  min-height: 12rem;
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
  .create-project-card {
    height: 13rem;
    min-height: 13rem;
  }
}

@media (min-width: 640px) {
  .project-card,
  .create-project-card {
    height: 14rem;
    min-height: 14rem;
  }
}

@media (min-width: 768px) {
  .project-card,
  .create-project-card {
    height: 15rem;
    min-height: 15rem;
  }
}

.project-card:hover,
.create-project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
  border-color: #ffc107;
}

.project-card .card-body {
  height: 100%;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  color: #e5e7eb;
}

@media (min-width: 640px) {
  .project-card .card-body {
    padding: 1.25rem;
  }
}

 @media (min-width: 1024px) {
   .project-card .card-body {
     padding: 1.5rem;
   }
 }

.project-card .card-title {
  font-size: 0.9375rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #f9fafb;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (min-width: 640px) {
  .project-card .card-title {
    font-size: 1rem;
  }
}

.project-card .card-text {
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
  .project-card .card-text {
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
  flex-grow: 1;
  background: #111827;
  min-height: 0;
  padding: 1.5rem 1rem;
  display: flex;
  position: relative;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
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
