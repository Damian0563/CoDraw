<template>
  <div class="main-layout">
    <SiDebar/>
    <main class="main-content flex-grow-1">
      <RouterView />
      <h1>Welcome to CoDraw!</h1>
      <div class="mb-4">
        <h2 class="mb-4 text-start">My Projects</h2>
        <div id="projects" class="container">
          <div
            class="card create-project-card my text-center bg-dark"
            @click="create()"
            style="height: 14rem; width: 14rem; cursor: pointer;"
          >
            <div class="card-body d-flex flex-column align-items-center justify-content-center" style="height: 100%;">
              <span style="font-size: 3rem; color: #ffc107;">+</span>
              <h5 class="card-title mt-2 mb-0" style="color:#ffc107">Create Project</h5>
            </div>
          </div>
          <div
            v-for="(board, index) in boards"
            :key="index"
            class="card project-card text-center bg-dark"
            style="min-height: 14rem; min-width: 14rem; cursor: pointer; position: relative;"
            @click="join(board.room)"
          >
            <div class="card-body d-flex flex-column text-white" style="height: 100%;">
              <h5 class="card-title fw-bold txtcard mb-2">{{ board.title }}</h5>
              <p class="card-text txtcard small">{{ board.description }}</p>
              <footer
                class="mt-auto py-2 px-2"
                style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.05); border-top: 1px solid #ffc107;"
              >
                <div class="d-flex justify-content-between small">
                  <span class="txtcard">Views: <span class="txtcard">{{ board.views }}</span></span>
                  <span class="txtcard">{{ board.modified }}</span>
                </div>
                <div class="text-start small txtcard">
                  Visibility: <span class="txtcard">{{ board.visibility }}</span>
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
    const data = await fetch(`${BASE_URL}/codraw`, {
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
      window.location.href=`${response.url}`
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
.project-card {
  transition: 0.3s ease-in-out;
  border: 1px solid #ffc10744;
  border-radius: 0.75rem;
}


.txtcard{
  color: #ffc107;
}

.project-card:hover {
  background-color: #ffc107 !important;
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

.project-card .card-title {
  font-size: 1.1rem;
}

.project-card .card-text {
  font-size: 0.85rem;
}


.my {
  width: 14rem; /* lock width */
  max-width: 20rem; /* prevents expansion */
}
#created,#shown{
  transition: 0.5s ease-in-out;
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
#shown:hover{
  background-color:#0d6efd;
  color:white !important;
}

#created:hover{
 background-color:#ffc107;
 color:black !important;
}



#projects {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(14rem, 1fr));
  gap: 1.5rem; /* same as Bootstrap g-4 */
  justify-items: center; /* center cards within each column */
}

.main-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background: #181818;
}
.main-content {
  flex-grow: 1;
  background: #fff;
  min-height: 0;
  padding: 2.5rem 2rem;
  display: flex;
  position: relative;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
}
</style>
