<template>
  <div class="not-found-background">
    <div class="not-found-content">
      <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="not-found-icon" />
      <h1 class="not-found-title">404 - Page Not Found</h1>
      <p class="not-found-text">
        Oops! The page you're looking for doesn't exist. It might have been moved, deleted, or you entered the wrong URL.
      </p>
      <router-link to="/" class="not-found-btn" aria-label="Go back to home">
        Go Home
      </router-link>
    </div>
  </div>
	<FoOter />
</template>

<script>
import FoOter from './Footer.vue'

export default {
  name: 'NotFound',
  components: {
    FoOter
  }
}
</script>

<style scoped>
.not-found-background {
  background: linear-gradient(135deg, #000000, #111111, #0a0a0a);
  background-size: 400% 400%;
  animation: gradientMove 12s ease infinite;
  width: 100%;
  min-height: 55vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 3rem 2rem 0 2rem;
  color: white;
  text-align: center;
  position: relative;
  overflow: hidden;
}

@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.not-found-content {
  max-width: 700px;
  width: 100%;
}

.not-found-icon {
  font-size: 4rem;
  color: yellow;
  filter: drop-shadow(0 0 15px rgba(255, 255, 0, 0.5));
  margin-bottom: 1rem;
}

.not-found-title {
  font-size: 4rem;
  font-weight: 700;
  letter-spacing: 2px;
  margin-bottom: 1rem;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 1s ease forwards;
}

.not-found-text {
  font-size: 1.3rem;
  max-width: 700px;
  line-height: 1.6;
  color: #e0e0e0;
  margin-bottom: 2rem;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 1s ease forwards;
  animation-delay: 0.3s;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.not-found-btn {
  background: linear-gradient(90deg, yellow, gold);
  color: black;
  font-weight: 600;
  padding: 0.9rem 2.4rem;
  border-radius: 50px;
  border: none;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(255, 255, 0, 0.4);
  transition: all 0.3s ease;
  font-size: 1.1rem;
  text-decoration: none;
}

.not-found-btn:hover {
  background: linear-gradient(90deg, gold, yellow);
  box-shadow: 0 0 25px rgba(255, 255, 0, 0.6);
  transform: translateY(-3px);
}

@media (max-width: 768px) {
  .not-found-title {
    font-size: 3rem;
  }
  .not-found-text {
    font-size: 1.1rem;
  }
  .not-found-icon {
    font-size: 3rem;
  }
}
</style>
