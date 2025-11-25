<template>
  <nav class="navbar navbar-expand-lg navbar-dark hero-background shadow p-3" style="background-color: black !important;">
    <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvas" aria-controls="offcanvas" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="offcanvas offcanvas-end mx-2" style="background-color: black;" tabindex="-1" id="offcanvas" aria-labelledby="offcanvasLabel">
      <div class="offcanvas-body">
        <RouterLink class="navbar-brand d-flex align-items-center" to="/">
          <img :src="imageUrl" alt="logo" loading="lazy" decoding="async" height="90" class="me-3" />
          <span>CoDraw</span>
        </RouterLink>
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0 d-flex flex-row align-items-center">
          <li class="nav-item mx-2">
            <RouterLink class="btn me-2" to="/signup" id="sign" style="border-color: yellow;color: yellow;">Sign up</RouterLink>
          </li> 
          <li class="nav-item mx-2">
            <RouterLink class="btn btn-outline-light" id="sing" to="/signin">Sign in</RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import imageUrl from '@/assets/logo.webp'
</script>
<script>
export default {
  name: 'NavBar',
  props: {
    msg: String
  }
}
</script>

<style scoped>
  .hero-background {
    background: linear-gradient(135deg, #000000, #111111, #0a0a0a) !important;
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  #sign,#sing{
    transition: ease-in-out 0.5s;
  }
  #sing:hover{
    transform: scale(1.1);
  }
  #sign:hover{
    transform: scale(1.1);
    color: black !important;
    background-color: yellow !important;
    border-color:white !important;
  }
</style>
