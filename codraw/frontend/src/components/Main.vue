<template>
  <div class="d-flex flex-column flex-shrink-0 p-3 text-bg-dark" style="width:20vw;height: 100%;">
    <div>
      <img :src='url' alt="logo" class="img-fluid mb-3" style="width: 100%; height: auto; border-radius: 50%;">
      
      <button class="button button-danger">Log out</button>
      
    </div>
  </div>


</template>
<script setup>
import { onMounted } from 'vue'
import url from '@/assets/logo.webp'

async function status(){
  try {
    const data = await fetch("http://localhost:8000/codraw", {
      method: 'GET',
      credentials: 'include'
    });
    const response = await data.json();
    console.log(response);
    if(response.status !== 200){
      window.location.href = '/';
    }
  } catch (e) {
    console.error(e);
  }
}

onMounted(() => {
  status()
})
</script>
<script>
export default {
  name: 'MaIn',
}
</script>

<style scoped>

</style>