<template>
  <div class="container mb-5">
    <img
      :src="logo"
      alt="CoDraw Logo"
      class="img-fluid my-4 rounded"
      style="max-height: 200px;"
    >
    <h1 class="text-white mt-4">About CoDraw</h1>
    <section class="mt-3">
      <p class="text-white">
        CoDraw is an innovative platform designed to facilitate collaborative drawing and creativity. Whether you're an artist looking to share your work or someone who enjoys doodling with friends, CoDraw provides the perfect space to connect and create together.
      </p>
      <p class="text-white">
        Our mission is to bring people together through art, fostering a community where creativity knows no bounds. With a variety of tools and features, CoDraw makes it easy for users of all skill levels to participate in collaborative projects.
      </p>
      <p class="text-white">
        Join us today and start creating amazing artwork with others! If you arre intrested in contributing to the development of CoDraw, check out our <a href="https://github.com/Damian0563/CoDraw" class="text-yellow">Github</a>
      </p>
    </section>
  </div>
  <FoOter/>
</template>


<script>
import logo from '@/assets/logo.webp';
import FoOter from './Footer.vue';
export default {
  name: "LearnMore",
  components: {
    FoOter
  },
  data() {
    return {
      logo,
    };
  },
};
</script>