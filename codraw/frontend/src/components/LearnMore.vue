<template>
  <div class="learn-more-container" id="learn-more">
    <div class="content-wrapper">
      <img
        :src="logo"
        alt="CoDraw Logo"
        class="learn-more-logo"
      >
      <h1 class="learn-more-title">About CoDraw</h1>
      <section class="learn-more-section">
        <p class="learn-more-text">
          CoDraw is an innovative platform designed to facilitate collaborative drawing and creativity. Whether you're an artist looking to share your work or someone who enjoys doodling with friends, CoDraw provides the perfect space to connect and create together.
        </p>
        <p class="learn-more-text">
          Our mission is to bring people together through art, fostering a community where creativity knows no bounds. With a variety of tools and features, CoDraw makes it easy for users of all skill levels to participate in collaborative projects.
        </p>
        <p class="learn-more-text">
          Join us today and start creating amazing artwork with others! If you are interested in contributing to the development of CoDraw, check out our <a href="https://github.com/Damian0563/CoDraw" class="github-link">GitHub</a>
        </p>
      </section>
    </div>
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

<style scoped>
.learn-more-container {
  background: linear-gradient(135deg, #000000, #111111, #0a0a0a);
  background-size: 400% 400%;
  animation: gradientMove 12s ease infinite;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 120px 2rem 4rem 2rem;
  color: white;
}

@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.content-wrapper {
  max-width: 800px;
  text-align: center;
}

.learn-more-logo {
  max-height: 200px;
  border-radius: 1rem;
  box-shadow: 0 0 30px rgba(255, 255, 0, 0.2);
  transition: transform 0.5s ease;
  margin-bottom: 2rem;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 1s ease forwards;
}

.learn-more-logo:hover {
  transform: scale(1.05) rotate(1deg);
}

.learn-more-title {
  font-size: 3rem;
  font-weight: 700;
  color: yellow;
  margin-bottom: 2rem;
  letter-spacing: 2px;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 1s ease forwards;
  animation-delay: 0.2s;
}

.learn-more-section {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 1s ease forwards;
  animation-delay: 0.4s;
}

.learn-more-text {
  color: #e0e0e0;
  font-size: 1.2rem;
  line-height: 1.8;
  margin-bottom: 1.5rem;
}

.github-link {
  color: yellow;
  font-weight: 600;
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.github-link:hover {
  color: gold;
  border-bottom-color: gold;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .learn-more-container {
    padding: 2rem 1rem;
  }

  .learn-more-title {
    font-size: 2rem;
  }

  .learn-more-text {
    font-size: 1rem;
  }

  .learn-more-logo {
    max-height: 150px;
  }
}
</style>
