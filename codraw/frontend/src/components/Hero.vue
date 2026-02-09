<template>
  <div class="hero-background">
    <h1 class="hero-title">CoDraw</h1>
    <div class="d-flex align-items-center justify-content-center gap-5 flex-wrap">
      <font-awesome-icon :icon="['fa','paintbrush']" class="feature-icon secondary-floating-icon"/>
      <font-awesome-icon :icon="['fa','feather-pointed']" class="feature-icon hero-floating-icon"/>
      <p class="hero-subtitle mb-0 mx-2">
        <span ref="typewriterText" class="typewriter-text"></span>
        <span class="cursor">|</span>
      </p>
      <font-awesome-icon :icon="['fa','pencil']" class="feature-icon hero-floating-icon"/>
      <font-awesome-icon :icon="['fa','paint-roller']" class="feature-icon secondary-floating-icon"/>
    </div>
    <router-link to="/signup" aria-label="Go to sign up">
      <button class="cta-btn mt-4" aria-label="Start drawing">Start Drawing Now</button>
    </router-link>
  </div>
  <div class="features-section">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-3 mb-3" v-for="(feature, i) in features" :key="i">
          <div class="card feature-card h-100 bg-dark text-white shadow-lg scroll-reveal" :style="{ transitionDelay: i * 150 + 'ms' }">
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
  <section class="about-sec container text-center my-5 scroll-reveal" aria-label="Our mission">
    <text class="about-title">No subscriptions, no hidden fees</text><text class="about-text" style="font-size: 2.5rem;">- just free for everyone, forever with at most respect to privacy.</text>
  </section>
  <section id="about" href="#about" class="about-sec" aria-label="About codraw">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-6 about-text scroll-reveal">
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
          <router-link to="/learn-more#learn-more" aria-label="Learn More">
            <button class="about-btn mt-3" aria-label="Learn More">Learn More</button>
          </router-link>
        </div>
        <div class="col-md-6 text-center about-visual scroll-reveal" style="transition-delay: 200ms;">
          <img
            :src="logo"
            alt="Collaborative Drawing"
            class="about-image"
						loading="lazy"
						decoding="async"
          />
        </div>
      </div>
    </div>
  </section>

  <section aria-label="Demo" class="my-3 d-flex flex-column justify-content-center text-center align-items-center scroll-reveal" style="color:yellow;font-size: 1.5rem;font-weight: 700;width:100%;overflow: hidden;">
    Take a look at our minimalistic demo to experience CoDraw and its awesome capabilities in action!
		<router-link :to="getDemoPath()" aria-label="Go to full demo">
			<button class="demo-btn mt-4" aria-label="Try Full Demo">Try Full Demo</button>
		</router-link>
  </section>
  <section class="faq-section" aria-label="Frequently Asked Questions">
    <div class="container">
      <h2 class="faq-title text-center mb-5 scroll-reveal">Frequently Asked Questions</h2>
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="accordion" id="faqAccordion">
            <div class="accordion-item faq-item scroll-reveal" v-for="(faq, index) in faqs" :key="index" :style="{ transitionDelay: index * 100 + 'ms' }">
              <h2 class="accordion-header" :id="'heading' + index">
                <button class="accordion-button faq-button" type="button" data-bs-toggle="collapse"
                        :data-bs-target="'#collapse' + index" :aria-expanded="index === 0 ? 'true' : 'false'"
                        :aria-controls="'collapse' + index">
                  {{ faq.question }}
                </button>
              </h2>
              <div :id="'collapse' + index" class="accordion-collapse collapse"
                   :class="{ 'show': index === 0 }" :aria-labelledby="'heading' + index"
                   data-bs-parent="#faqAccordion">
                <div class="accordion-body faq-body">
                  {{ faq.answer }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <FoOter />
</template>

<script>
import { get_cookie } from '@/common';
import { v4 as uuidv4 } from 'uuid'
import { BASE_URL } from '../common.js';
import logo from '@/assets/logo.webp';
import FoOter from './Footer.vue';

export default {
  name: "HeRo",
  components: {
    FoOter
  },
  data() {
    return {
      logo,
      fullText: "CoDraw is a real-time collaborative drawing platform that lets you and your friends create, share, and edit artwork together from anywhere. Experience seamless teamwork, intuitive tools, and instant updates as you bring your creative ideas to life!",
      typewriterIndex: 0,
      typewriterTimeout: null,
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
      ],
      faqs: [
        {
          question: "Is CoDraw really free forever?",
          answer: "Yes! CoDraw is completely free with no subscriptions, hidden fees, or premium features. We believe creativity should be accessible to everyone."
        },
        {
          question: "How many people can collaborate on a single drawing?",
          answer: "CoDraw supports real-time collaboration for multiple users. There's no strict limit - you can invite as many friends as you'd like to join your drawing session."
        },
        {
          question: "Do I need to create an account to use CoDraw?",
          answer: "While you can try our demo without an account, creating one allows you to save your drawings, create private rooms, and collaborate with others."
        },
        {
          question: "What browsers does CoDraw support?",
          answer: "CoDraw works on all modern browsers including Chrome, Firefox, Safari, and Edge. We recommend using the latest version for the best experience."
        },
        {
          question: "Can I use CoDraw on mobile devices?",
          answer: "Yes! CoDraw is fully responsive and works great on tablets and mobile devices. Touch controls are optimized for drawing on smaller screens."
        }
      ]
    };
  },
  mounted() {
    this.check();
    this.startTypewriter();
    this.initScrollReveal();
  },
  beforeUnmount() {
    if (this.typewriterTimeout) {
      clearTimeout(this.typewriterTimeout);
    }
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
		getDemoPath(){
			return `/demo/${uuidv4()}?origin=home`
		},
    startTypewriter() {
      const typeNextChar = () => {
        if (this.typewriterIndex < this.fullText.length && this.$refs.typewriterText) {
          this.$refs.typewriterText.textContent += this.fullText.charAt(this.typewriterIndex);
          this.typewriterIndex++;
          this.typewriterTimeout = setTimeout(typeNextChar, 30);
        }
      };
      this.typewriterTimeout = setTimeout(typeNextChar, 800);
    },
    initScrollReveal() {
      const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
      };
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            observer.unobserve(entry.target);
          }
        });
      }, observerOptions);

      const elements = document.querySelectorAll('.scroll-reveal');
      elements.forEach(el => observer.observe(el));
    },
  }
};
</script>

<style scoped>
.accordion-button:focus {
	outline: none;
	box-shadow: none;
}
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

.hero-subtitle {
  font-size: 1.3rem;
  max-width: 700px;
  line-height: 1.6;
  color: #e0e0e0;
  margin-bottom: 2rem;
  min-height: 100px;
}

.typewriter-text {
  display: inline;
}

.cursor {
  display: inline-block;
  color: yellow;
  font-weight: 100;
  animation: blink 0.7s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0px); }
}

.hero-floating-icon {
  font-size: 4rem;
  color: yellow;
  filter: drop-shadow(0 0 15px rgba(255, 255, 0, 0.5));
  animation: float 3s ease-in-out infinite;
}

.secondary-floating-icon {
  font-size: 3rem;
  color: gold;
  filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.5));
  animation: float 4s ease-in-out infinite;
  animation-delay: 1.5s;
}

@media (max-width: 768px) {
  .hero-floating-icon {
    font-size: 3rem;
    margin-top: 1rem;
  }
  .hero-subtitle {
    text-align: center;
  }
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scroll-reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.scroll-reveal.revealed {
  opacity: 1;
  transform: translateY(0);
}

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

.features-section {
  background: linear-gradient(135deg, #000000, #111111, #0a0a0a) !important;
  padding: 4rem 1rem;
  overflow-x: hidden;
}
.feature-card {
  border: 2px solid rgba(255, 255, 0, 0.6);
  border-radius: 1rem;
  transition: all 0.4s ease;
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

.about-section {
  background: radial-gradient(circle at top left, #111, #000);
  color: white;
  padding: 6rem 1.5rem;
  overflow: hidden;
  position: relative;
}

.about-sec {
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

.demo-btn {
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
  margin-top: 2rem;
}
.demo-btn:hover {
  background: linear-gradient(90deg, gold, yellow);
  box-shadow: 0 0 25px rgba(255, 255, 0, 0.6);
  transform: translateY(-3px);
}

.faq-section {
  background: linear-gradient(135deg, #000000, #111111, #0a0a0a);
  padding: 6rem 1.5rem;
  color: white;
}

.faq-title {
  font-size: 2.6rem;
  font-weight: 700;
  color: yellow;
  margin-bottom: 3rem;
}

.faq-item {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid rgba(255, 255, 0, 0.3);
  border-radius: 1rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.faq-item:hover {
  border-color: yellow;
  box-shadow: 0 0 15px rgba(255, 255, 0, 0.2);
}

.faq-button {
  background: transparent;
  color: yellow;
  font-weight: 600;
  font-size: 1.1rem;
  border: none;
  padding: 1.2rem 1.5rem;
  transition: all 0.3s ease;
}

.faq-button:not(.collapsed) {
  color: gold;
  background: rgba(255, 255, 0, 0.1);
}

.faq-button:hover {
  background: rgba(255, 255, 0, 0.05);
}

.faq-button::after {
  filter: brightness(0) invert(1) sepia(1) saturate(100) hue-rotate(45deg);
}

.faq-body {
  color: #e0e0e0;
  font-size: 1rem;
  line-height: 1.6;
  padding: 1rem 1.5rem;
}

.accordion-collapse {
  border-radius: 0 0 1rem 1rem;
}

@media (max-width: 768px) {
  .about-section {
    text-align: center;
  }
  .about-image {
    margin-top: 2rem;
  }
  .faq-title {
    font-size: 2rem;
  }
  .faq-button {
    font-size: 1rem;
    padding: 1rem;
  }
}
</style>
