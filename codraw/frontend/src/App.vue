<template>
  <NavBar v-if="$route.path.substring(0,7) !== '/codraw'" />
  <HeRo v-if="$route.path === '/'" msg="test" />
  <router-view />
  <SignIn v-if="$route.path === '/signin'" />
  <SignUp v-if="$route.path === '/signup'" />
  <MaIn v-if="$route.path === '/codraw'"/>
  <SeTtings v-if="$route.path==='/codraw/settings'" />
  <AccOunt v-if="$route.path==='/codraw/account'" />
</template>

<script>
import NavBar from './components/Navbar.vue'
import HeRo from './components/Hero.vue'
import MaIn from './components/Main.vue'
import SeTtings from './components/SeTtings.vue'
import AccOunt from './components/AccOunt.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    HeRo,
    MaIn,
    SeTtings,
    AccOunt
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
  background: black;
}
</style>
