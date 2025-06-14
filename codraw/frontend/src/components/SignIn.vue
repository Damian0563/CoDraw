<template>
  <div style="background-color: black;">
    <img :src='url' class="img-fluid border rounded-circle" style="width:10vw;height: auto;margin-top:2%; border-color: yellow;">
  </div>
  <div class="d-flex justify-content-center pt-5" style="background-color: black; min-height: 40vh;">
    <div class="card p-3 shadow-lg" style="max-width: 400px; width: 100%; background: white; border: none; min-height: unset;">
      <h2 class="text-center mb-3 text-black">Sign In</h2>
      <form>
        <div class="mb-2">
          <label for="email" class="form-label text-black text-start w-100">Email address</label>
          <input type="email" class="form-control bg-dark text-white border-secondary" id="email" placeholder="Enter email">
        </div>
        <div class="mb-2">
          <label for="password" class="form-label text-black text-start w-100">Password</label>
          <input type="password" class="form-control bg-dark text-white border-secondary" id="password" placeholder="Enter password">
        </div>
        <button type="submit" class="btn btn-success w-100 mt-2" style="background-color: yellow;color: black;">Sign Up</button>
      </form>
      <div class="text-center mt-2">
        <span class="text-secondary">Do not have an account?</span>
        <RouterLink to="/signup" class="ms-2 text-info">Sign up</RouterLink>
      </div>
    </div>  
  </div>
</template>

<script setup>
import url from '@/assets/logo.webp'
</script>

<script>
export default{
    name:"SignIn",
    props:{
        msg:String
    }
}
</script>
<style scoped>
input::placeholder {
  color: #ccc !important; /* or any light color you prefer */
  opacity: 1;
}
</style>