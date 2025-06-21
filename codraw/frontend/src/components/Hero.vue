<template>
      
    <div class="hero-background p-5 col-lg-4" :style="`background-color: black;height:60vh`">
        <h1 class="hero-title" style="color: white;">
            CoDraw<br>
        </h1>
        <p style="color: white;">
            CoDraw is a real-time collaborative drawing platform that lets you and your friends create, share, and edit artwork together from anywhere. Experience seamless teamwork, intuitive tools, and instant updates as you bring your creative ideas to life together!
        </p>
    </div>
    <div style="background-color: black;overflow-x: hidden;margin-top: 2%;">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-3 mb-3">
            <div class="card h-100 bg-dark text-white shadow-lg" id="card" style="border-color: yellow;">
              <div class="card-body text-center">
                <h5 class="card-title">Modern and Slick</h5>
                <p class="card-text">A visually appealing interface designed for a seamless and enjoyable drawing experience.</p>
              </div>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="card h-100 bg-dark text-white shadow-lg" id="card" style="border-color: yellow;">
              <div class="card-body text-center">
                <h5 class="card-title">Performance Oriented</h5>
                <p class="card-text">Optimized for speed and responsiveness, ensuring smooth collaboration in real time.</p>
              </div>
            </div>
          </div>
          <div class="col-md-3 mb-3">
            <div class="card h-100 bg-dark text-white shadow-lg" id="card" style="border-color: yellow;">
              <div class="card-body text-center">
                <h5 class="card-title">Intuitive Design</h5>
                <p class="card-text">Easy-to-use tools and layout, making creativity accessible for everyone.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

</template>


<script>
  export default {
      name: "HeRo",
      props: {
          msg: String
      },
      mounted() {
        this.check();
      },
      methods: {
        async check() {
          try {
            const data = await fetch("http://localhost:8000/home", {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json'
              },
              credentials: 'include',
            });
            const response = await data.json();
            console.log(response);
            if (response.status === 300) {
              window.location.href = '/codraw';
            }
          } catch (e) {
            console.error(e);
          }
        }
      }
  }
</script>

<style scoped>
.hero-background {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  width: 100%; /* Changed from 100vw to 100% to prevent overflow */
  margin-left: 0; /* Remove negative margins */
  margin-right: 0;
  border: none;
  box-shadow: 0 4px 24px rgba(0,0,0,0.25);
  padding: 0 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  position: relative;
  overflow: hidden;
}
.hero-title {
  text-align: center;
  padding-top: 6vh;
  font-size: 4rem;
  color: #fff;
  font-weight: 600;
  letter-spacing: 2px;
  text-shadow: 0 2px 16px rgba(0,0,0,0.5);
  margin-bottom: 1.5rem;
}
.hero-background p {
  text-align: center;
  font-size: 1.35rem;
  color: #e0e0e0;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
  text-shadow: 0 1px 8px rgba(0,0,0,0.3);
}
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.2rem;
    padding-top: 3vh;
  }
  .hero-background {
    min-height: 40vh;
    padding: 0 1rem;
  }
  .hero-background p {
    font-size: 1rem;
  }
}

#card{
  transition: ease-in 0.6s;
}
#card:hover{
  transform: scale(1.1);
}

.card {
  transition: transform 0.2s, box-shadow 0.2s;
  will-change: transform;
  /* Prevents the card from being clipped by parent */
  z-index: 1;
}
.card:hover {
  transform: translateY(-8px) scale(1.03);
  box-shadow: 0 8px 32px rgba(255, 255, 0, 0.25), 0 4px 24px rgba(0,0,0,0.35);
}
/* Add padding to the row to prevent cards from being clipped at the top */
.row.justify-content-center {
  padding-top: 16px;
  padding-bottom: 16px;
}
/* Ensure parent containers allow overflow */
.container, .row.justify-content-center {
  overflow: visible !important;
}
</style>