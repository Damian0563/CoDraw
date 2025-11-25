<template>
  <div class="container">
    <img
      :src="logo"
      alt="CoDraw Logo"
      class="img-fluid my-4 rounded"
      style="max-height: 200px;"
    >
    <h1 class="text-white mt-4">About CoDraw</h1>

  </div>
</template>


<script>
import logo from '@/assets/logo.webp';
export default {
  name: "LearnMore",
  data() {
    return {
      logo,
    };
  },
};
</script>