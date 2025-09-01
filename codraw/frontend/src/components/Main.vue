<template>
  <div class="main-layout">
    <aside
      class="sidebar d-flex flex-column flex-shrink-0 p-3 text-bg-dark"
      :class="{ 'sidebar-collapsed': !sidebarOpen }"
    >
      <div class="sidebar-header d-flex flex-column align-items-center mb-4">
        <img class="toggle mb-3 align-self-end" @click="sidebarOpen = !sidebarOpen" :class="{'align-self-center':!sidebarOpen}" :src="toggle" style="cursor: pointer; width: 2rem; height: 2rem;"/>
        <img :src="url" alt="logo" class="logo mb-3 img-fluid rounded rounded-circle" style="max-height: 20vh;"/>
        <RouterLink to="/codraw/account" class="nav-link account-link mb-2 w-100 text-center">
          My Account
        </RouterLink>
        <RouterLink to="/codraw/settings" class="nav-link settings-link mb-2 w-100 text-center">
          Settings
        </RouterLink>
        <button class="btn btn-danger w-100" @click="log_out()" id="out">Log out</button>
      </div>
    </aside>
    <main class="main-content flex-grow-1">
      <RouterView />
      <h1>Welcome to CoDraw!</h1>
      <div class="mb-4">
        <h2 class="mb-4 text-start">My Projects</h2>
        <!-- <div id="projects" class="container">
          <div class="row g-4 w-100 mx-0 justify-content-center">
            <div :class="boards.length < 3 ? 'col-12 col-md-6 col-xl-4' : 'col-12 col-lg-4 col-xl-3'">
              <div class="card create-project-card text-center bg-dark" @click="create()" style="min-height: 14rem;min-width:14rem;cursor: pointer;">
                <div class="card-body d-flex flex-column align-items-center justify-content-center" style="height: 100%;">
                  <span style="font-size: 3rem; color: #ffc107;">+</span>
                  <h5 class="card-title mt-2 mb-0" style="color:#ffc107">Create Project</h5>
                </div>
              </div>
            </div>
            <div
              v-for="(board, index) in boards"
              :key="index"
              :class="boards.length < 3 ? 'col-12 col-md-6 col-xl-4' : 'col-12 col-lg-4 col-xl-3'"
            >
              <div
                class="card create-project-card text-center bg-dark"
                @click="join(board.room)"
                style="min-height: 14rem;min-width:14rem ;cursor: pointer;position: relative;"
              >
                <div class="card-body d-flex flex-column text-white" id="created" style="height: 100%;">
                  <h5 class="card-title fw-bold">{{ board.title }}</h5>
                  <p class="card-text" style="font-size: 0.8rem;">{{ board.description }}</p>
                  <footer style="font-size: 0.7rem;position: absolute; bottom: 0; left: 0; right: 0;">Visibility: {{ board.visibility }}</footer>
                </div>  
              </div>
            </div>
          </div>
        </div> -->
        <div id="projects" class="container">
          <div 
            class="card create-project-card text-center bg-dark" 
            @click="create()" 
            style="min-height: 14rem; min-width: 14rem; cursor: pointer;"
          >
            <div class="card-body d-flex flex-column align-items-center justify-content-center" style="height: 100%;">
              <span style="font-size: 3rem; color: #ffc107;">+</span>
              <h5 class="card-title mt-2 mb-0" style="color:#ffc107">Create Project</h5>
            </div>
          </div>
          <div
            v-for="(board, index) in boards"
            :key="index"
            class="card create-project-card text-center bg-dark"
            @click="join(board.room)"
            style="min-height: 14rem; min-width: 14rem; cursor: pointer; position: relative;"
          >
            <div class="card-body d-flex flex-column text-white" id="created" style="height: 100%;">
              <h5 class="card-title fw-bold">{{ board.title }}</h5>
              <p class="card-text" style="font-size: 0.8rem;">{{ board.description }}</p>
              <footer style="font-size: 0.7rem; position: absolute; bottom: 0; left: 0; right: 0;">
                Visibility: {{ board.visibility }}
              </footer>
            </div>
          </div>
        </div>
      </div>
      <div v-if="loading" class="spinner-overlay">
        <VueSpinnerTail size="60" color="orange" />
      </div>
      <div class="my-5 border rounded justify-content-center" style="background-color: #ffc107;width:100%;height: auto;">
        <div class="text-center mb-4">
          <h2 class="fw-bold mt-4">Browse Public Projects</h2>
          <p class="text-muted">Find boards and ideas shared by the community</p>
        </div>
        <div class="row justify-content-center">
          <div class="col-md-6 col-sm-8 col-7">
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
            <div class="row g-4">
              <div
                v-for="(board, index) in popular"
                :key="index"
                :class="popular.length < 3 ? 'col-12 col-md-6 col-xl-4' : 'col-12 col-lg-4 col-xl-3'"
              >
                <div
                  class="card create-project-card text-center bg-dark"
                  @click="join(board.room)"
                  style="min-height: 12rem;min-width:10rem ;cursor: pointer;position: relative;"
                >
                  <div class="card-body d-flex flex-column text-white" id="shown" style="height: 100%;">
                    <h5 class="card-title fw-bold">{{ board.title }}</h5>
                    <p class="card-text" style="font-size: 0.8rem;">{{ board.description }}</p>
                    <footer class="d-flex flex-column py-2" style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.05); border-top: 1px solid #ffc107;">
                      <div class="d-flex align-items-center gap-2 mx-2 mb-2">
                        <span class="fw-semibold text-warning">Owner:</span>
                        <a :href="`/codraw/user/${board.owner}`" style="color:#ff4f4f !important;">{{ board.owner }}</a>
                      </div>
                      <div class="d-flex align-items-center gap-2 mx-2">
                        <input class="form-control form-control-sm" readonly disabled :value="'Views: ' + board.views" style="width:150px;"/>
                        <input class="form-control form-control-sm" readonly disabled :value="board.modified" style="width: 150px;"/>
                      </div>
                    </footer>
                  </div>  
                </div>
              </div>
              <div v-if="popular.length===0" class="justify-content-center" style="min-height: 12rem;">
                <text>No results found :(</text>
              </div>
            </div>
          </div>
        </section>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { get_cookie } from '@/common';
import {DateTime} from 'luxon'
import url from '@/assets/logo.webp'
import toggle from '@/assets/sidebar.webp'
import {BASE_URL} from '../common.js'
import {VueSpinnerTail} from 'vue3-spinners'
const loading = ref(false)
const csrf=get_cookie('csrftoken')
const sidebarOpen = ref(true)
const boards = ref([])
const popular=ref([])
const input=ref('')
async function log_out(){
  try{
    const data=await fetch(`${BASE_URL}/log_out`,{
      method:"POST",
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf},
      credentials:"include"
    })
    const response=await data.json()
    if(response.status===200){
      window.location.href='/'
    }
  }catch(e){
    console.error(e)
  }
}

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
      //console.log(popular.value.length, popular.value)
    }
    loading.value=false
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
      method:"GET",
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrf
      },
      credentials:"include"
    })
    const response=await data.json()
    boards.value=response.boards
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

onMounted(async() => {
  loading.value=true
  await Promise.all([
    status(),
    get_boards(),
    load_popular()
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
#out{
  transition: 0.6s ease-in-out;
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

#out:hover{
  background-color: white;
  color: red;
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
.sidebar {
  height: 100vh;
  min-width: 240px;
  max-width: 20vw;
  background: linear-gradient(135deg, #181818 80%, #222 100%);
  border-right: 2px solid #ffc107;
  transition: width 0.3s, padding 0.3s, min-width 0.3s, max-width 0.3s;
  z-index: 10;
}
.sidebar-collapsed {
  min-width: 60px !important;
  max-width: 60px !important;
  padding-left: 0.5rem !important;
  padding-right: 0.5rem !important;
}
.logo {
  transition: max-width 0.3s, opacity 0.3s;
}
.sidebar-collapsed .logo {
  max-width: 40px;
  opacity: 0.7;
}
.sidebar-collapsed .nav-link,
.sidebar-collapsed .btn,
.sidebar-collapsed .settings-link,
.sidebar-collapsed .account-link {
  display: none !important;
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