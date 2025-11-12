<template>
  <div class="hero-background">
    <h1 class="hero-title">CoDraw</h1>
    <p class="hero-subtitle">
      CoDraw is a real-time collaborative drawing platform that lets you and your friends create, share, 
      and edit artwork together from anywhere. Experience seamless teamwork, intuitive tools, and instant updates 
      as you bring your creative ideas to life!
    </p>
    <router-link to="/signup">
      <button class="cta-btn mt-4">Start Drawing Now</button>
    </router-link>
  </div>

  <!-- Features -->
  <div class="features-section">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-3 mb-3" v-for="(feature, i) in features" :key="i">
          <div class="card feature-card h-100 bg-dark text-white shadow-lg">
            <div class="card-body text-center">
              <font-awesome-icon :icon="feature.icon" class="feature-icon" />
              <h5 class="card-title mt-3">{{ feature.title }}</h5>
              <p class="card-text">{{ feature.text }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <section id="about" href="#about" class="about-section">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-6 about-text">
          <h2 class="about-title">About CoDraw</h2>
          <p>
            CoDraw was built for creators who believe in collaboration. Whether you're sketching concepts, 
            storyboarding, or designing together, CoDraw makes teamwork feel effortless and fun.  
            <br /><br />
            With our real-time synchronization engine and a beautifully minimal interface, you can see every brushstroke 
            from your teammates the moment it happens — no refreshes, no lag, just instant creativity.  
            <br /><br />
            Our mission is simple: empower creativity by connecting people through shared imagination.
          </p>
          <router-link to="/learn-more">
            <button class="about-btn mt-3">Learn More</button>
          </router-link>
        </div>

        <div class="col-md-6 text-center about-visual">
          <img
            :src="logo"
            alt="Collaborative Drawing"
            class="about-image"
          />
        </div>
      </div>
    </div>
  </section>
  <footer class="footer-section">
    <div class="container text-center">
      <div class="row justify-content-center">
        <div class="col-md-4 mb-3 footer-brand">
          <h3 class="footer-title">CoDraw</h3>
          <p class="footer-desc">
            Collaborative drawing made simple, fast, and fun. Create together from anywhere.
          </p>
        </div>

        <div class="col-md-2 mb-3 footer-links">
          <h5>Explore</h5>
          <ul>
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/signup">Get Started</router-link></li>
          </ul>
        </div>

        <div class="col-md-3 mb-3 footer-social">
          <h5>Follow Us</h5>
          <div class="social-icons">
            <!-- <a href="https://github.com/Damian0563/CoDraw"><i class="fa-brands fa-github"></i></a> -->
            <a href="https://github.com/Damian0563/CoDraw"><font-awesome-icon :icon="['fab', 'github']" /></a>
          </div>
        </div>
      </div>

      <hr class="footer-divider" />
      <p class="footer-copy">
        © {{ new Date().getFullYear() }} CoDraw. All rights reserved.
      </p>
    </div>
  </footer>
</template>

<script>
import { get_cookie } from '@/common';
import { BASE_URL } from '../common.js';
import logo from '@/assets/logo.webp';

export default {
  name: "HeRo",
  data() {
    return {
      logo,
      features: [
        {
          title: "Modern and Slick",
          text: "A visually appealing interface designed for a seamless and enjoyable drawing experience.",
          icon:['fas', 'palette']
        },
        {
          title: "Performance Oriented",
          text: "Optimized for speed and responsiveness, ensuring smooth collaboration in real time.",
          icon: ['fas', 'bolt']
        },
        {
          title: "Intuitive Design",
          text: "Easy-to-use tools and layout, making creativity accessible for everyone.",
          icon: ['fas', 'lightbulb']
        }
      ]
    };
  },
  mounted() {
    this.check();
  },
  methods: {
    async check() {
      try {
        const csrf = get_cookie('csrftoken');
        const data = await fetch(`${BASE_URL}/home`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
          },
          credentials: 'include',
        });
        const response = await data.json();
        if (response.status === 300 && window.location.pathname !== '/codraw') {
          window.location.href = '/codraw';
        }
      } catch (e) {
        console.error(e);
      }
    },
  }
};
</script>

<style scoped>
.hero-background {
  background: linear-gradient(135deg, #000000, #111111, #0a0a0a);
  background-size: 400% 400%;
  animation: gradientMove 12s ease infinite;
  width: 100%;
  min-height: 50vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 3rem 2rem;
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

.hero-title {
  font-size: 4rem;
  font-weight: 700;
  letter-spacing: 2px;
  margin-bottom: 1rem;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 1s ease forwards;
}

.footer-section {
  background: linear-gradient(135deg, #000000, #0b0b0b, #111111);
  color: #d9d9d9;
  padding: 4rem 1rem 2rem 1rem;
  border-top: 2px solid rgba(255, 255, 0, 0.2);
  text-align: center;
}

.footer-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: yellow;
  margin-bottom: 0.8rem;
}

.footer-desc {
  font-size: 1rem;
  color: #bfbfbf;
  line-height: 1.6;
}

.footer-links h5 {
  color: yellow;
  margin-bottom: 0.8rem;
  font-weight: 600;
}

.footer-links ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin: 0.4rem 0;
}

.footer-links a {
  color: #d9d9d9;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: yellow;
}

.footer-social h5 {
  color: yellow;
  margin-bottom: 0.8rem;
  font-weight: 600;
}

.social-icons a {
  color: #d9d9d9;
  font-size: 3rem;
  margin: 0 0.5rem;
  transition: all 0.3s ease;
}

.social-icons a:hover {
  color: yellow;
  transform: scale(1.2);
}

.footer-divider {
  border-color: rgba(255, 255, 0, 0.2);
  margin: 2rem 0 1rem;
}

.footer-copy {
  color: #a8a8a8;
  font-size: 0.95rem;
}


.hero-subtitle {
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

/* --- CTA BUTTON --- */
.cta-btn {
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
}
.cta-btn:hover {
  background: linear-gradient(90deg, gold, yellow);
  box-shadow: 0 0 25px rgba(255, 255, 0, 0.6);
  transform: translateY(-3px);
}

/* --- FEATURES SECTION --- */
.features-section {
  background: linear-gradient(135deg, #000000, #111111, #0a0a0a) !important;
  padding: 4rem 1rem;
  overflow-x: hidden;
}
.feature-card {
  border: 2px solid rgba(255, 255, 0, 0.6);
  border-radius: 1rem;
  transition: all 0.4s ease;
  background: rgba(20, 20, 20, 0.9);
}
.feature-card:hover {
  box-shadow: 0 0 20px rgba(255, 255, 0, 0.4);
  transform: translateY(-8px) scale(1.05);
  border-color: yellow;
}
.feature-icon {
  font-size: 2.5rem;
  color: yellow;
  transition: transform 0.3s ease;
}
.feature-card:hover .feature-icon {
  transform: scale(1.2) rotate(5deg);
}

/* --- ABOUT SECTION --- */
.about-section {
  background: radial-gradient(circle at top left, #111, #000);
  color: white;
  padding: 6rem 1.5rem;
  overflow: hidden;
  position: relative;
}
.about-title {
  font-size: 2.6rem;
  font-weight: 700;
  color: yellow;
  margin-bottom: 1.5rem;
}
.about-text p {
  color: #d9d9d9;
  font-size: 1.1rem;
  line-height: 1.7;
}
.about-btn {
  background: linear-gradient(90deg, yellow, gold);
  color: black;
  font-weight: 600;
  padding: 0.8rem 2rem;
  border-radius: 50px;
  border: none;
  cursor: pointer;
  box-shadow: 0 0 12px rgba(255, 255, 0, 0.4);
  transition: all 0.3s ease;
}
.about-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 20px rgba(255, 255, 0, 0.6);
}
.about-image {
  width: 90%;
  max-width: 480px;
  border-radius: 1rem;
  box-shadow: 0 0 30px rgba(255, 255, 0, 0.2);
  transition: transform 0.5s ease;
}
.about-visual:hover .about-image {
  transform: scale(1.05) rotate(1deg);
}

@media (max-width: 768px) {
  .about-section {
    text-align: center;
  }
  .about-image {
    margin-top: 2rem;
  }
}
</style>
