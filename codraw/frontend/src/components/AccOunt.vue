<template>
  <div v-if="loading" class="spinner-overlay">
    <VueSpinnerTail size="60" color="orange" />
  </div>

  <main class="flex-grow-1 bg-dark text-white py-5">
    <div class="container">
      <h2 class="fw-bold mb-4 text-center">{{ username }}'s Boards</h2>

      <div class="boards-wrapper">
        <div
          v-for="(board, index) in boards"
          :key="index"
          class="project-card"
          @click="join(board.room)"
        >
          <h5 class="card-title fw-bold mt-2">{{ board.title }}</h5>
          <p class="card-text small">{{ board.description }}</p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { get_cookie } from '@/common';
import { DateTime } from 'luxon';
import { onMounted, ref } from 'vue';
import { BASE_URL } from '../common.js';
import { VueSpinnerTail } from 'vue3-spinners';
const username=ref(null)
const pathParts = window.location.pathname.split('/');
username.value = pathParts[pathParts.length - 1];
const admin = ref(false)
const csrf = get_cookie('csrftoken')
const boards = ref([])
const loading = ref(true)


const get_status=async()=>{

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
  } catch (e) {
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

onMounted(async () => {
  loading.value = true;
  let result=get_status();
  admin.value=result[0]
  await get_boards();
  loading.value = false;
})
</script>

<style scoped>
/* Wrapper: flexbox grid with wrapping */
.boards-wrapper {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
}

/* Fixed-size cards */
.project-card {
  background: #1f1f1f;
  border: 1px solid #333;
  border-radius: 1rem;
  width: 240px;   /* fixed width */
  height: 180px;  /* fixed height */
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;

  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.project-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.4);
}

.spinner-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; z-index: 1000; background-color: rgba(0, 0, 0, 0.7); }

</style>
