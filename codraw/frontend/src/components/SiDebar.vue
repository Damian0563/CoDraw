<template>
	<aside
		class="sidebar d-flex flex-column flex-shrink-0 p-3 text-bg-dark"
		:class="{ 'sidebar-collapsed': !sidebarOpen }"
	>
		<div class="sidebar-header d-flex flex-column align-items-center mb-4">
			<img loading="lazy" alt="sidebar" decoding="async" class="toggle mb-3 align-self-end" @click="sidebarOpen = !sidebarOpen" :class="{'align-self-center':!sidebarOpen}" :src="toggle" style="cursor: pointer; width: 2rem; height: 2rem;"/>
			<img :src="url" alt="logo" loading="lazy" decoding="async" class="logo mb-4 img-fluid rounded rounded-circle" style="max-height: 20vh;"/>
			<RouterLink :to="`/codraw`" class="nav-link rounded p-2 account-link mb-4  text-center" style="width:170px" :style="{'background-color':onPage['/codraw']?'#ffc107':'linear-gradient(135deg, #181818 80%, #222 100%)'}">
				<font-awesome-icon class="mx-2" :icon="['fas','home']"></font-awesome-icon>Start Page
			</RouterLink>
			<RouterLink :to="`/codraw/account/${username}`" class="nav-link rounded p-2 account-link mb-4 text-center" style="width:170px" :style="{'background-color':onPage['/codraw/account']?'#ffc107':'linear-gradient(135deg, #181818 80%, #222 100%)'}">
				<font-awesome-icon class="mx-2" :icon="['fas','user']"></font-awesome-icon>My Account
			</RouterLink>
			<RouterLink :to="`/codraw/search`" class="nav-link rounded p-2 account-link mb-4 text-center" style="width:170px" :style="{'background-color':onPage['/codraw/search']?'#ffc107':'linear-gradient(135deg, #181818 80%, #222 100%)'}">
				<font-awesome-icon class="mx-2" :icon="['fas','search']"></font-awesome-icon>Search
			</RouterLink>
			<button class="btn btn-danger" @click="log_out()" id="out">Log out</button>
		</div>
	</aside>
</template>

<script setup>
import {BASE_URL} from '@/common'
import toggle from '@/assets/sidebar.webp'
const loading = ref(false)

import url from '@/assets/logo.webp'
import { get_cookie } from '@/common';
import {ref, onMounted} from 'vue'
const csrf=get_cookie('csrftoken')
const sidebarOpen = ref(false)
const username = ref("")
const onPage={
	'/codraw':false,
	'/codraw/search':false,
	'/codraw/account':false,
}

function checkCurrentPage(){
	const path=window.location.pathname
	if(path==="/codraw") onPage['/codraw']=true
	else if(path==="/codraw/search") onPage['/codraw/search']=true
	else if(path.startsWith("/codraw/account")) onPage['/codraw/account']=true
}

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
onMounted(async() => {
	loading.value=true
	checkCurrentPage()
  await get_username()
	loading.value=false
})


</script>

<style scoped>
.sidebar {
  height: auto;
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

#out{
  transition: 0.6s ease-in-out;
}
#out:hover{
  background-color: white;
  color: red;
}

</style>
