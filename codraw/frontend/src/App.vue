<template>
  <NavBar msg="Welcome to Your Vue.js App"/>
  <HeRo v-if="$route.path === '/'" msg="test" />
  <router-view />
</template>

<script>
import NavBar from './components/Navbar.vue'
import HeRo from './components/Hero.vue'
export default {
  name: 'App',
  components: {
    NavBar,
    HeRo,
  }
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
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
}
</style>
