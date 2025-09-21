<template class="bg-dark">
  <div v-if="loading" class="spinner-overlay">
    <VueSpinnerTail size="60" color="orange" />
  </div>

  <main class="flex-grow-1 text-white py-5">
    <RouterLink to="/codraw">
      <img :src="back" class="back" style="width:50px;height: 50px;">
    </RouterLink>
    <button class="bookmarks btn btn-primary">Bookmarks</button>
    <div class="container">
      <h2 class="fw-bold mb-5 text-center">{{ username }}'s Boards</h2>
      <div class="boards-wrapper mt-2">
        <!-- @click="join(board.room)" -->
        <div
          v-for="(board, index) in boards"
          :key="index"
          class="project-card"
        > 
          <div class="d-flex justify-content-end align-items-center gap-2">
            <img
              v-if="!edits[index]"
              :src="edit"
              @click="edits[index] = !edits[index]"
              style="width:20px;height:20px;cursor:pointer;"
            >
            <img
              v-else
              :src="save"
              @click="edits[index] = !edits[index]"
              style="width:20px;height:20px;cursor:pointer;"
            >
            <img
              :src="bin"
              style="width:20px;height:20px;cursor:pointer;"
            >
          </div>
          <div v-if="!edits[index]">
            <input
            class="form-control fw-bold mt-2 bg-dark text-white"
            v-model="board.title"
            @click.stop
            :placeholder="'Board Title'"
            readonly
            disabled
            />
            <input
            class="form-control small mt-3 bg-dark text-white"
            v-model="board.description"
            @click.stop
            :placeholder="'Board Description'"
            readonly
            disabled
            />
          </div>
          <div v-else>
            <input
            class="form-control fw-bold mt-2 bg-dark text-white"
            v-model="board.title"
            @click.stop
            :placeholder="'Board Title'"
            />
            <input
            class="form-control small mt-3 bg-dark text-white"
            v-model="board.description"
            @click.stop
            :placeholder="'Board Description'"
            />
          </div>
          <div class="card-body text-white position-relative flex-grow-1">
            <div class="d-flex flex-column align-items-start gap-1"
                style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.05); padding: 0.5rem;">
              <span class="fw-semibold text-warning" style="font-size: 0.85rem;">
                Views: <span class="text-white">{{ board.views }}</span>
              </span>
              <span class="fw-semibold text-warning" style="font-size: 0.85rem;">
                Last Modified: <span class="text-white">{{ board.modified }}</span>
              </span>
              <span class="fw-semibold text-warning" style="font-size: 0.85rem;">
                Visibility: <span class="text-white">{{ board.visibility }}</span>
              </span>
            </div>
          </div>
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
import back from '@/assets/goback.webp'
import bin from '@/assets/bin.webp'
import save from '@/assets/save.webp'
import edit from '@/assets/edit.webp'
const username=ref(null)
const pathParts = window.location.pathname.split('/');
username.value = pathParts[pathParts.length - 1];
const admin = ref(false)
const csrf = get_cookie('csrftoken')
const boards = ref([])
const loading = ref(true)
//const deletes=ref({})
const edits=ref({})


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
    edits.value=response.boards.map(()=>false)
  } catch (e) {
    console.error(e)
  }
}

/*
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
*/

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

.bookmarks{
  position: absolute;
  right:5%;
  top:50px;
  transition: 0.5s ease-in;
}

.back{
  position: absolute;
  left:5%;
  top:50px;
  transition: 0.5s ease-in;
}

.back:hover{
  transform: translateX(-15px);
}

/* Fixed-size cards */
.project-card {
  background: #1f1f1f;
  border: 1px solid #333;
  border-radius: 1rem;
  width: 400px;   /* fixed width */
  height: 350px;  /* fixed height */
  padding: 1rem;
  display: flex;
  flex-direction: column;
  /* justify-content:space-around; */
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.project-card:hover {
  box-shadow: 0 6px 16px rgba(0,0,0,0.4);
}

.spinner-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; z-index: 1000; background-color: rgba(0, 0, 0, 0.7); }

</style>
