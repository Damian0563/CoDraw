<template class="bg-dark">
  <div v-if="loading" class="spinner-overlay">
    <VueSpinnerTail size="60" color="orange" />
  </div>

  <main class="flex-grow-1 text-white py-5">
    <RouterLink to="/codraw">
      <img :src="back" class="back" style="width:50px;height: 50px;">
    </RouterLink>
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
            <div v-if="admin" class="w-100">
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
                  @click="edits[index] = !edits[index];resave(boards[index]);boards[index].modified='Just now'"
                  style="width:20px;height:20px;cursor:pointer;"
                >
                <img
                  :src="bin"
                  @click="delete_board(boards[index].room);boards.splice(index,1)"
                  style="width:20px;height:20px;cursor:pointer;"
                >
              </div>
              <div v-if="!edits[index]">
                <input class="form-control fw-bold mt-2 bg-dark text-white" v-model="board.title" @click.stop :placeholder="'Board Title'" readonly disabled />
                <input class="form-control small mt-3 bg-dark text-white" v-model="board.description" @click.stop :placeholder="'Board Description'" readonly disabled />
              </div>
              <div v-else>
                <input class="form-control fw-bold mt-2 bg-white text-dark" v-model="board.title" @click.stop :placeholder="'Board Title'" />
                <input class="form-control small mt-3 bg-white text-dark" v-model="board.description" @click.stop :placeholder="'Board Description'" />
              </div>
            </div>
            <div v-else class="w-100">
              <input class="form-control fw-bold mt-2 bg-dark text-white" v-model="board.title" @click.stop :placeholder="'Board Title'" readonly disabled/>
              <input class="form-control small mt-3 bg-dark text-white" v-model="board.description" @click.stop :placeholder="'Board Description'" readonly disabled />
            </div>
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
    <div class="container mt-5" v-if="admin"> 
      <h1>Bookmarks</h1>
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
const admin = ref(false)
const csrf = get_cookie('csrftoken')
const boards = ref([])
const loading = ref(true)
const edits=ref({})
const bookmarks=ref([])

const delete_board=async(room)=>{
  try{
    const data=await fetch(`${BASE_URL}/delete/${room}`,{
      method:"GET",
      headers:{"X-CSRFToken":csrf},
      credentials:"include"
    })
    const response=await data.json()
    if(response.status===200) console.log("Board deleted successfully")
    else console.log("Board not deleted successfully")
  }catch(e){
    console.error(e)
  }
}

const get_bookmarks=async(username)=>{
  try{
    const data=await fetch(`${BASE_URL}/get_bookmarks/${username}/${DateTime.local().zoneName}`,{
      method:"GET",
      headers:{
        "X-CSRFToken":csrf
      },
      credentials:"include"
    })
    const response=await data.json()
    if(response.status===200) bookmarks.value=response.bookmarks
    else bookmarks.value=[]
  }catch(e){
    console.error(e)
    bookmarks.value=[]
  }
}

const resave=async(board)=>{
  loading.value=true;
  if(board.original_description!==board.description || board.original_title!==board.title){
    try{
      const data=await fetch(`${BASE_URL}/codraw/update/${board.room}`,{
        method:"POST",
        headers:{
          "Content-Type":"application/json",
          "X-CSRFToken":csrf
        },
        credentials:"include",
        body:JSON.stringify({
          "title":board.title,
          "description":board.description,
          "timezone":DateTime.local().zoneName
        })
      })
      const response=await data.json()
      if(response.status===200) console.log("board saved successfully")
      else console.log("board saved unsuccessfully")
    }catch(e){
      console.error(e)
    }
  }
  loading.value=false;
}

const get_status=async(curr_user)=>{
  try{
    const data=await fetch(`${BASE_URL}/username`,{
      method:"GET",
      headers:{
        "X-CSRFToken":csrf
      },
      credentials:"include"
    })
    const response=await data.json()
    let user2=""
    if(response.status==200) user2=response.username
    else user2="ERROR 404 NOT FOUND"
    return user2===curr_user
  }catch(e){
    console.error(e)
  }
}

const get_boards = async (username) => {
  try {
    const data = await fetch(`${BASE_URL}/codraw/boards/${username}`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf
      },
      body: JSON.stringify({
        "timezone": DateTime.local().zoneName,
      }),
      credentials: "include"
    })
    const response = await data.json()
    boards.value = response.boards.map(b => ({
      ...b,
      original_title: b.title,
      original_description: b.description
    }))
    console.log(response)
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
  const pathParts = window.location.pathname.split('/');
  username.value = pathParts[pathParts.length - 1];
  admin.value=await get_status(username.value);
  await get_boards(username.value);
  await get_bookmarks(username.value)
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
