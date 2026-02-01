<template>
	<aside
		class="sidebar d-flex flex-column flex-shrink-0 p-3 text-bg-dark"
		:class="{ 'sidebar-collapsed': !sidebarOpen, 'sidebar-overlay': isMobile && sidebarOpen }"
	>
		<div class="sidebar-header d-flex flex-column align-items-center mb-4">
			<img loading="lazy" alt="sidebar" decoding="async" class="toggle mb-3 align-self-end" @click="isMobile ? sidebarOpen = !sidebarOpen : sidebarOpen = !sidebarOpen" :class="{'align-self-center':!sidebarOpen}" :src="toggle" style="cursor: pointer; width: 2rem; height: 2rem;"/>
			<img :src="url" alt="logo" loading="lazy" decoding="async" class="logo mb-4 img-fluid rounded rounded-circle" style="max-height: 20vh;"/>
			<RouterLink :to="`/codraw`" class="nav-link rounded-3 p-3 account-link mb-3 text-center modern-tile" :class="{'active-tile': onPage['/codraw']}">
				<font-awesome-icon class="mx-2 tile-icon" :icon="['fas','home']"></font-awesome-icon>
				<span class="tile-text">Start Page</span>
			</RouterLink>
			<RouterLink :to="`/codraw/account/${username}`" class="nav-link rounded-3 p-3 account-link mb-3 text-center modern-tile" :class="{'active-tile': onPage['/codraw/account']}">
				<font-awesome-icon class="mx-2 tile-icon" :icon="['fas','user']"></font-awesome-icon>
				<span class="tile-text">My Account</span>
			</RouterLink>
			<RouterLink :to="`/codraw/search`" class="nav-link rounded-3 p-3 account-link mb-3 text-center modern-tile" :class="{'active-tile': onPage['/codraw/search']}">
				<font-awesome-icon class="mx-2 tile-icon" :icon="['fas','search']"></font-awesome-icon>
				<span class="tile-text">Search</span>
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
const isMobile = ref(false)
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
function checkMobile() {
	isMobile.value = window.innerWidth <= 500
}

function closeSidebarOnOverlayClick(event) {
	if (isMobile.value && sidebarOpen.value) {
		const sidebar = event.target.closest('.sidebar')
		if (!sidebar) {
			sidebarOpen.value = false
		}
	}
}

onMounted(async() => {
	loading.value=true
	checkCurrentPage()
	checkMobile()
  await get_username()
	
	// Listen for window resize
	window.addEventListener('resize', checkMobile)
	// Close sidebar when clicking outside on mobile
	window.addEventListener('click', closeSidebarOnOverlayClick)
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
.modern-tile {
  width: 100%;
  background: linear-gradient(145deg, #2a2a2a, #1a1a1a);
  border: 1px solid rgba(255, 193, 7, 0.2);
  color: #ffffff;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: 0.95rem;
  letter-spacing: 0.3px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.modern-tile::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 193, 7, 0.1), transparent);
  transition: left 0.5s ease;
}

.modern-tile:hover::before {
  left: 100%;
}

.modern-tile:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 193, 7, 0.25);
  border-color: rgba(255, 193, 7, 0.5);
  background: linear-gradient(145deg, #3a3a3a, #2a2a2a);
}

.modern-tile:active {
  transform: translateY(0);
  box-shadow: 0 2px 12px rgba(255, 193, 7, 0.2);
}

.active-tile {
  background: linear-gradient(145deg, #ffc107, #ffb300) !important;
  color: #1a1a1a !important;
  border-color: #ffc107 !important;
  box-shadow: 0 4px 16px rgba(255, 193, 7, 0.4);
}

.active-tile .tile-icon {
  color: #1a1a1a;
}

.tile-icon {
  font-size: 1.1rem;
  width: 20px;
  text-align: center;
}

.tile-text {
  transition: all 0.3s ease;
}

.modern-tile:hover .tile-text {
  font-weight: 600;
}

/* Mobile overlay mode */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  z-index: 1000;
  transition: none !important;
}

.sidebar-overlay .sidebar-header {
  width: 100%;
  max-width: 280px;
  margin: 0 auto;
}

/* Add overlay backdrop */
.sidebar-overlay::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: -1;
}

.sidebar-collapsed .nav-link,
.sidebar-collapsed .btn,
.sidebar-collapsed .settings-link,
.sidebar-collapsed .account-link {
  display: none !important;
}

/* Close sidebar when clicking overlay on mobile */
.sidebar-overlay::after {
  content: '';
  position: fixed;
  top: 0;
  left: 280px;
  right: 0;
  bottom: 0;
  z-index: 999;
}

#out{
  transition: 0.6s ease-in-out;
  background: linear-gradient(145deg, #dc3545, #c82333);
  border: none;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(220, 53, 69, 0.3);
}
#out:hover{
  background: linear-gradient(145deg, #ffffff, #f8f9fa);
  color: #dc3545;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.2);
}

</style>
