<template>
  <nav class="navbar navbar-expand-lg navbar-dark hero-background shadow p-3" style="background-color: black !important;">
    <div class="container-fluid">
      <RouterLink class="navbar-brand d-flex align-items-center" to="/">
        <img :src="imageUrl" alt="logo" loading="lazy" decoding="async" height="60" class="me-2" />
        <span>CoDraw</span>
      </RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" style="background-color: black; max-width: 80vw;">
        <div class="offcanvas-header border-bottom border-secondary">
          <h5 class="offcanvas-title text-white" id="offcanvasNavbarLabel">Menu</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0 d-flex flex-column flex-lg-row align-items-center">
            <li class="nav-item my-2 my-lg-0 mx-2">
              <RouterLink class="btn w-100" to="/signup" id="sign" style="border-color: yellow; color: yellow;" @click="navigateAndClose">Sign up</RouterLink>
            </li>
            <li class="nav-item my-2 my-lg-0 mx-2">
              <RouterLink class="btn btn-outline-light w-100" id="sing" to="/signin" @click="navigateAndClose">Sign in</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>
<script setup>
import imageUrl from '@/assets/logo.webp'

const navigateAndClose = () => {
  const offcanvas = document.getElementById('offcanvasNavbar')
  // eslint-disable-next-line no-undef
  const bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvas)
  if (bsOffcanvas) {
    bsOffcanvas.hide()
  }
}
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
