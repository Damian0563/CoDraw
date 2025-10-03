<template>
  <NavBar v-if="$route.path.substring(0,7) !== '/codraw' && $route.path.substring(0,6)!=='/board'"/>
  <router-view/>
</template>

<script>
import NavBar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    NavBar,
  }
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  /* overflow-y: scroll;
  scrollbar-width: none; Firefox */
}


#app {
  font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  font-size: 1.2rem;
}
html, body, #app {
  height: 100%;
  min-height: 100vh;
  background: black;
  overflow-y: auto !important;
  scrollbar-width: thin !important;
}
</style>
