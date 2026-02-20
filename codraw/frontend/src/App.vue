<template>
	<NavBar v-if="$route.meta.showNav"/>
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
  background: linear-gradient(180deg, #0a0a0f 0%, #0d0d15 50%, #0a0a0f 100%);
  overflow-y: auto !important;
  scrollbar-width: thin !important;
}
</style>
