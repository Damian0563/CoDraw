<template>
  <div style="background-color: black;">
    <img :src='url' class="img-fluid border rounded-circle border-danger-subtle" style="width:10vw;height: auto;margin-top:2% ;">
  </div>
  <div v-if="invalid" class="alert alert-danger text-center custom-alert p-2"
       role="alert"
       style="max-width: 70vw; width: 440px; position: fixed; top: 4rem; left: 50%; transform: translateX(-50%); z-index: 10000; font-size: 0.95rem; border-radius: 0.7rem; box-shadow: 0 2px 8px rgba(220,53,69,0.10); background: #222; border: 1.5px solid #dc3545;">
    <button @click="invalid=false" class="close-btn rounded-circle float-end" aria-label="Close" style="background-color: #dc3545; color: #fff; border: none; width: 1.5rem; height: 1.5rem; font-size: 1.1rem; margin-top: -0.3rem; margin-right: -0.3rem; line-height: 1.1rem;">&times;</button>
    <div class="alert-content" style="padding-top: 0.2rem;">
      <strong style="color: #ffc107; font-size: 1rem;">{{ message }}</strong>
      <div style="color: #fff; margin-top: 0.2rem; font-size: 0.92rem;">Please try again.</div>
    </div>
  </div>
  <div v-if="visible" class="overlay">
    <div class="popup-card">
      <button @click="visible=false" class="close-btn rounded-circle float-end" aria-label="Close" style="background-color: red;color: white;">&times;</button><br><br>
      <h4 class="mb-3">Enter Verification Code</h4>
      <div class="d-flex justify-content-center mb-3">
        <input maxlength="1" id="1" @input="handleInput(2)" ref="ZeroInput" v-model="zero" class="code-input" type="text" pattern="[0-9]*" inputmode="numeric"/>
        <input maxlength="1" id="2" @input="handleInput(3)" v-model="one" class="code-input" type="text" pattern="[0-9]*" inputmode="numeric" ref="OneInput"/>
        <input maxlength="1" id="3" @input="handleInput(4)" v-model="two" ref="TwoInput" class="code-input" type="text" pattern="[0-9]*" inputmode="numeric"/>
        <input maxlength="1" id="4" @input="handleInput(5)" v-model="three" ref="ThreeInput" class="code-input" type="text" pattern="[0-9]*" inputmode="numeric"/>
        <input maxlength="1" id="5" class="code-input" v-model="four" ref="FourInput" type="text" pattern="[0-9]*" inputmode="numeric"/>
      </div>
      <button class="btn btn-primary w-100" @click="verifyCode">Verify</button>
    </div>
  </div>
  <div class="d-flex justify-content-center pt-5" style="background-color: black; min-height: 40vh;">
    <div class="card p-3 shadow-lg" style="max-width: 400px; width: 100%; background: white; border: none; min-height: unset;">
      <h2 class="text-center mb-3 text-black">Sign Up</h2>
      <form @submit="SignUp">
        <div class="mb-2">
          <label for="username" class="form-label text-black text-start w-100">Username</label>
          <input v-model="username" type="text" class="form-control bg-dark text-white border-secondary" id="username" placeholder="Enter username" style="color: white;">
        </div>
        <div class="mb-2">
          <label for="email" class="form-label text-black text-start w-100">Email address</label>
          <input v-model="mail" type="email" class="form-control bg-dark text-white border-secondary" id="email" placeholder="Enter email">
        </div>
        <div class="mb-2">
          <label for="password" class="form-label text-black text-start w-100">Password</label>
          <input v-model="password" type="password" class="form-control bg-dark text-white border-secondary" id="password" placeholder="Enter password">
        </div>
        <button id="sign" class="btn btn-success w-100 mt-2" type="submit" style="background-color: yellow;color: black;">Sign Up</button>
      </form>
      <div class="text-center mt-2">
        <span class="text-secondary">Already have an account?</span>
        <RouterLink to="/signin" class="ms-2 text-info">Sign In</RouterLink>
      </div>
    </div>  
  </div>
</template>
<script setup>
import { ref } from 'vue'
import url from '@/assets/logo.webp'
let visible=ref(false)
let invalid=ref(false)
let message=ref('')
const username = ref('')
const password = ref('')
const mail = ref('')
const ZeroInput = ref(null)
const OneInput = ref(null)
const TwoInput = ref(null)
const ThreeInput = ref(null)
const FourInput = ref(null)

async function SignUp(e) {
  e.preventDefault()
  const username_input=username.value
  const password_input= password.value
  const mail_input=mail.value
  try{
    const data = await fetch("http://localhost:8000/create",{
      method:"POST",
      headers:{"Content-Type":'application/json'},
      body:JSON.stringify({
        "username":username_input,
        "mail":mail_input,
        "password":password_input
      })
    })
    const response=await data.json()
    if(response.status===200){
      visible.value=true
      ZeroInput.value.focus()
    }else{
      invalid.value=true
      message.value="Account already registered under this email. Did you forget your password?"
    }

  } catch (e) {
    console.error(e)
  }
}
function handleInput(index){
  if(index === 2 && OneInput.value) OneInput.value.focus()
  if(index === 3 && TwoInput.value) TwoInput.value.focus()
  if(index === 4 && ThreeInput.value) ThreeInput.value.focus()
  if(index === 5 && FourInput.value) FourInput.value.focus()
}
const zero = ref('')
const one = ref('')
const two = ref('')
const three = ref('')
const four = ref('')

// Helper to get the code string when needed
function getCode() {
  return `${zero.value}${one.value}${two.value}${three.value}${four.value}`;
}

async function verifyCode(){
  const username_input=username.value
  const mail_input=mail.value
  const data=await fetch('http://localhost:8000/verify',{
    method:"POST",
    headers:{
      'Content-Type':'application/json'
    },
    body:JSON.stringify({
      "username":username_input,
      "mail":mail_input,
      "code":getCode(),
    })
  })
  const response=await data.json()
  if(response.status===200){
    const jwt=response.jwt
    console.log(jwt)
    // window.location.href = '/signin'
  } else {
    visible.value=false
    invalid.value=true
    zero.value = ''
    one.value = ''
    two.value = ''
    three.value = ''
    four.value = ''
    message.value = "Invalid verification code. Please try again- new verification code has been sent.";
  }
}
</script>

<style scoped>
.card {
  background: linear-gradient(135deg, #181818 80%, #222 100%);
  color: #fff;
  border-radius: 1.5rem;
  border: 2px solid #ffc107;
  box-shadow: 0 8px 32px rgba(0,0,0,0.35), 0 2px 8px rgba(255,255,0,0.08);
  padding: 2rem 1.5rem;
  margin-top: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
  box-shadow: 0 12px 36px rgba(255, 255, 0, 0.18), 0 8px 32px rgba(0,0,0,0.45);
}
.card h2 {
  color: #ffc107;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 1.2rem;
}
.card label {
  color: #ffc107;
  font-weight: 500;
}
.card input {
  background: #222;
  color: #fff;
  border: 1.5px solid #ffc107;
  border-radius: 0.5rem;
  margin-bottom: 0.7rem;
}
.card input:focus {
  border-color: #007bff;
  background: #333;
}
#sign {
  background: linear-gradient(90deg, #ffe066 60%, #ffd700 100%);
  color: #181818;
  font-weight: 700;
  border: none;
  border-radius: 0.7rem;
  box-shadow: 0 2px 8px rgba(255,255,0,0.08);
  transition: background 0.2s, color 0.2s, transform 0.2s;
}
#sign:hover {
  background: #007bff !important;
  color: #fff !important;
  transform: scale(1.05);
}
input::placeholder {
  color: #ccc !important;
  opacity: 1;
}
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.popup-card {
  background: linear-gradient(135deg, #181818 80%, #222 100%);
  color: #fff;
  padding: 2.5rem 2rem 2rem 2rem;
  border-radius: 1.5rem;
  box-shadow: 0 8px 32px rgba(0,0,0,0.45), 0 2px 8px rgba(255,255,0,0.10);
  min-width: 320px;
  max-width: 90vw;
  text-align: center;
  border: 2px solid #ffc107;
}
.popup-card h4 {
  color: #ffc107;
  font-weight: 700;
  margin-bottom: 1.5rem;
}
.code-input {
  width: 2.5rem;
  height: 2.5rem;
  margin: 0 0.3rem;
  font-size: 2rem;
  text-align: center;
  border: 2px solid #ffc107;
  border-radius: 8px;
  background: #222;
  color: #fff;
  outline: none;
  transition: border 0.2s, background 0.2s;
}
.code-input:focus {
  border-color: #007bff;
  background: #333;
}
.popup-card .btn-primary {
  background: linear-gradient(90deg, #ffe066 60%, #ffd700 100%);
  color: #181818;
  font-weight: 700;
  border: none;
  border-radius: 0.7rem;
  box-shadow: 0 2px 8px rgba(255,255,0,0.08);
  transition: background 0.2s, color 0.2s, transform 0.2s;
  margin-top: 1.2rem;
}
.popup-card .btn-primary:hover {
  background: #007bff !important;
  color: #fff !important;
  transform: scale(1.05);
}
</style>