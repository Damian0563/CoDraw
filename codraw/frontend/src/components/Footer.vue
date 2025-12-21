<template>
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
export default {
  name: "FoOter",
};
</script>
<style scoped>
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
</style>