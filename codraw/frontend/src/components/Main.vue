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
        <div id="projects" class="container">
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
                style="min-height: 14rem;min-width:14rem ;cursor: pointer;"
              >
                <div class="card-body d-flex flex-column text-white" id="created" style="height: 100%;">
                  <h5 class="card-title" style="font-weight:800;">{{ board.title }}</h5>
                  <p class="card-text" style="font-size: 0.8rem;">{{ board.description }}</p>
                </div>  
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="my-5 border rounded" style="background-color: #ffc107;width:100%;height: 100%;">
        <div class="text-center mb-4">
          <h2 class="fw-bold mt-4">Browse Public Projects</h2>
          <p class="text-muted">Find boards and ideas shared by the community</p>
        </div>
        <div class="row justify-content-center">
          <div class="col-md-6">
            <div class="input-group shadow-sm rounded">
              <input 
                type="text" 
                class="form-control border-0 p-3"
                placeholder="Search public boards..." 
                aria-label="Search public boards" 
              >
              <button class="btn btn-primary" type="button">
                <i class="bi bi-search"></i>
              </button>
            </div>
          </div>
        </div>

        <section id="results" class="mt-5">
        </section>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { get_cookie } from '@/common';
import url from '@/assets/logo.webp'
import toggle from '@/assets/sidebar.webp'
const csrf=get_cookie('csrftoken')
const sidebarOpen = ref(true)
const boards = ref([{}])
async function log_out(){
  try{
    const data=await fetch('http://localhost:8000/log_out',{
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

async function status(){
  try {
    const data = await fetch("http://localhost:8000/codraw", {
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
    const data=await fetch('http://localhost:8000/codraw/get_boards',{
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
    const data=await fetch("http://localhost:8000/load",{
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
    const data=await fetch('http://localhost:8000/get_project_url',{
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

onMounted(() => {
  status(),
  get_boards()
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

#created{
  transition: 0.5s ease-in-out;
}

#created:hover{
 background-color:#ffc107;
 color:black !important;
}

#out:hover{
  background-color: white;
  color: red;
}


.main-layout {
  display: flex;
  min-height: 100vh;
  width: 100vw;
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
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
}
</style>