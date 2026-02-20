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
              <RouterLink class="btn btn-signup w-100" to="/signup" @click="navigateAndClose">Sign up</RouterLink>
            </li>
            <li class="nav-item my-2 my-lg-0 mx-2">
              <RouterLink class="btn btn-signin w-100" to="/signin" @click="navigateAndClose">Sign in</RouterLink>
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
    background: linear-gradient(180deg, #0a0a0f 0%, #0d0d15 50%, #0a0a0f 100%) !important;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .hero-background::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, rgba(255, 215, 0, 0.3));
  }
  .btn-signup, .btn-signin {
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.02em;
    border-radius: 8px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-transform: uppercase;
    border: 2px solid transparent;
  }

  .btn-signup {
    background: linear-gradient(135deg, #facc15 0%, #eab308 100%);
    color: #000;
    border-color: #facc15;
    box-shadow: 0 4px 14px rgba(250, 204, 21, 0.4);
  }

  .btn-signup:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(250, 204, 21, 0.6);
    background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
    border-color: #eab308;
    color: #000;
  }

  .btn-signup:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(250, 204, 21, 0.3);
  }

  .btn-signin {
    background: transparent;
    color: #fff;
    border: 2px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10px);
  }

  .btn-signin:hover {
    transform: translateY(-2px);
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.8);
    box-shadow: 0 4px 14px rgba(255, 255, 255, 0.15);
    color: #fff;
  }

  .btn-signin:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2);
  }

  .btn-signup:active, .btn-signin:active {
    transform: translateY(0);
  }
</style>
