<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow p-3">
    <a class="navbar-brand d-flex align-items-center" href="#">
      <img :src="imageUrl" alt="logo" height="70" class="me-3" />
      <span>CoDraw</span>
    </a>
    <ul class="navbar-nav ms-auto mb-2 mb-lg-0 d-flex flex-row align-items-center">
      <li class="nav-item mx-2">
        <a class="nav-link" href="#">About</a>
      </li>
      <li class="nav-item mx-2">
        <RouterLink class="btn btn-success me-2" to="/signup">Sign up</RouterLink>
      </li>
      <li class="nav-item mx-2">
        <RouterLink class="btn btn-outline-light" to="/signin">Sign in</RouterLink>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import imageUrl from '@/assets/logo.webp'
</script>
<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
