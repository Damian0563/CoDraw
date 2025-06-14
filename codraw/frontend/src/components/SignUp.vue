<template>
  <div style="background-color: black;">
    <img :src='url' class="img-fluid border rounded-circle border-danger-subtle" style="width:10vw;height: auto;margin-top:2% ;">
  </div>
  <div class="d-flex justify-content-center pt-5" style="background-color: black; min-height: 40vh;">
    <div class="card p-3 shadow-lg" style="max-width: 400px; width: 100%; background: white; border: none; min-height: unset;">
      <h2 class="text-center mb-3 text-black">Sign Up</h2>
      <form>
        <div class="mb-2">
          <label for="username" class="form-label text-black text-start w-100">Username</label>
          <input type="text" class="form-control bg-dark text-white border-secondary" id="username" placeholder="Enter username" style="color: white;">
        </div>
        <div class="mb-2">
          <label for="email" class="form-label text-black text-start w-100">Email address</label>
          <input type="email" class="form-control bg-dark text-white border-secondary" id="email" placeholder="Enter email">
        </div>
        <div class="mb-2">
          <label for="password" class="form-label text-black text-start w-100">Password</label>
          <input type="password" class="form-control bg-dark text-white border-secondary" id="password" placeholder="Enter password">
        </div>
        <button type="submit" class="btn btn-success w-100 mt-2" @click="SignUp()" style="background-color: yellow;color: black;">Sign Up</button>
      </form>
      <div class="text-center mt-2">
        <span class="text-secondary">Already have an account?</span>
        <RouterLink to="/signin" class="ms-2 text-info">Sign In</RouterLink>
      </div>
    </div>  
  </div>
</template>
<script setup>
import url from '@/assets/logo.webp'
</script>
<script>
export default{
    name:"SignUp",
    methods:{
      SignUp(){

      }
    }
}
</script>

<style scoped>
input::placeholder {
  color: #ccc !important;
  opacity: 1;
}
</style>