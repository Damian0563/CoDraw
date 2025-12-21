<template>
  <Transition name="fade-slide">
    <div v-if="invalid" class="alert alert-danger text-center custom-alert p-2"
       role="alert"
       style="max-width: 70vw; width: 440px; position: fixed; top: 4rem; left: 50%; transform: translateX(-50%); z-index: 10000; font-size: 0.95rem; border-radius: 0.7rem; box-shadow: 0 2px 8px rgba(220,53,69,0.10); background: #222; border: 1.5px solid #dc3545;">
    <button @click="invalid=false" class="close-btn rounded-circle float-end" aria-label="Close" style="background-color: #dc3545; color: #fff; border: none; width: 1.5rem; height: 1.5rem; font-size: 1.1rem; margin-top: -0.3rem; margin-right: -0.3rem; line-height: 1.1rem;">&times;</button>
    <div class="alert-content" style="padding-top: 0.2rem;">
      <strong style="color: #ffc107; font-size: 1rem;">{{ message }}</strong>
    </div>
    </div>
  </Transition>
  <div v-if="loading" class="spinner-overlay d-flex justify-content-center align-items-center">
    <VueSpinnerTail size="60" color="orange" />
  </div>
  <Transition name="fade-slide">
    <div v-if="recovery" class="recovery-container" role="alert" style="max-width: 80vw; width: 500px; position: fixed; top: 8rem; left: 50%; transform: translateX(-50%); z-index: 5000; font-size: 0.95rem; border-radius: 0.7rem; box-shadow: 0 2px 8px rgba(220,53,69,0.10); background: #222; border: 1.5px solid #dc3545;">
      <button @click="recovery=false" class="close-btn rounded-circle float-end" aria-label="Close" style="background-color: #dc3545; color: #fff; border: none; width: 1.5rem; height: 1.5rem; font-size: 1.1rem; margin-top: -0.3rem; margin-right: -0.3rem; line-height: 1.1rem;">&times;</button>
      <h2 class="mt-3" style="color: yellow;font-weight: bold;">Input your email, recovery link will be sent to you!</h2>
      <form 
        class="mb-3 needs-validation" 
        :class="{ 'was-validated': validated }" 
        novalidate 
        @submit.prevent="sendReset"
      >
        <label for="emailInput" class="form-label text-muted small">Email Address</label>
        <input 
          type="email" 
          class="form-control form-control-lg mb-3" 
          placeholder="e.g. name@example.com"
          required
          v-model="name_or_mail"
        />
        <div class="invalid-feedback mb-2">
          Please specify a valid email address.
        </div>  
        <button type="submit" class="btn btn-primary btn-lg w-100 shadow-sm mt-3">
          Send Recovery Link
        </button>
      </form>
    </div>
  </Transition>
  <div class="d-flex justify-content-center pt-5 mb-5" style="background-color: black; min-height: 40vh;">
    <div class="card p-3 shadow-lg w-50" style="max-width: 700px; width: 100%; background: white; border: none; min-height: unset;">
      <h2 class="text-center mb-3 text-black">Sign In</h2>
      <form ref="formRef" @submit="SignIn" class="needs-validation" novalidate>
        <div class="mb-2">
          <label for="email" class="form-label text-black text-start w-100">Email address</label>
          <input type="email" v-model="name_or_mail" class="form-control bg-dark text-white border-secondary" id="email" placeholder="Enter email" required>
          <div class="invalid-feedback">
            Please specify email.
          </div>
        </div>
        <div class="mb-2">
          <label for="password" class="form-label text-black text-start w-100">Password</label>
          <input type="password" v-model="password" class="form-control bg-dark text-white border-secondary" id="password" placeholder="Enter password" required>
          <div class="invalid-feedback">
            Please specify password.
          </div>
        </div>
        <div class="form-check d-flex align-items-center mb-3 w-100 flex-wrap" style="padding: 0 !important;gap: 2rem;">
          <label class="form-check-label text-black fw-medium mb-0" for="rememberMe">
            Remember me
          </label>
          <input type="checkbox" ref="ticked" @click="ticked=!ticked" id="rememberMe" style="accent-color:#ffc107;margin: 0 !important;width:1.25rem;height:1.25rem;">
        </div>
        <button id="sign" type="submit" class="btn btn-success w-50 mt-2" style="background-color: yellow;color: black;">Sign In</button>
      </form>
      <div class="text-center mt-2">
        <span class="text-secondary">Do not have an account?</span>
        <RouterLink to="/signup" class="ms-2 text-info">Sign up</RouterLink>
      </div>
      <div class="text-center mt-2">
        <text @click="recovery=true" class="ms-2 text-info" style="cursor: pointer;">Forgot your password?</text>
      </div>
    </div>  
  </div>
  <FoOter />
</template>

<script setup>
import { ref } from 'vue'
import { get_cookie } from '@/common'
import {BASE_URL} from '../common.js'
import {VueSpinnerTail} from 'vue3-spinners'
import FoOter from './Footer.vue'

let message = ref('')
let invalid = ref(false)
let ticked= ref(false)
const loading=ref(false);
const name_or_mail = ref('')
const password = ref('')
const validated = ref(false);
const recovery=ref(false);
const formRef = ref(null);


async function sendReset(event){
  try{
    
    recovery.value=true;
    const form = event.currentTarget;
    validated.value = true;
    if (!form.checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }
    recovery.value=false;
    loading.value=true;
    const data=await fetch(`${BASE_URL}/restore_password/${name_or_mail.value}`, {
        method: 'GET',
        headers: {
          'X-CSRFToken': get_cookie('csrftoken')
        },
        credentials: 'include'
    })
    const response=await data.json()
    return response.status===200
  }catch(e){
    console.error(e)
    recovery.value=false;
    invalid.value = true
    message.value = 'An error occurred while sending reset email. Are you sure the email is correct?'
    loading.value=false;
  }finally{
    invalid.value = true;
    message.value="Recovery link sent, its validity is 5 minutes! Please check your email.";
    loading.value=false;
  }
}

async function SignIn(e){
  e.preventDefault()
  const form = formRef.value;
  form.classList.add('was-validated')
  if (!form.checkValidity()) {
    e.stopPropagation()
    return;
  }
  loading.value=true;
  try{
    const csrf=get_cookie('csrftoken')
    const data = await fetch(`${BASE_URL}/signin`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken':csrf
      },
      credentials: 'include',
      body: JSON.stringify({
        "mail": name_or_mail.value,
        "password": password.value,
        "remember": ticked.value
      })
    });
    const response = await data.json();
    if(response.status===200){
      window.location.href = '/codraw';
    }else{
      invalid.value = true;
      message.value ='Invalid credentials. Please try again.';
    }
    loading.value=false;
  }catch(e){
    console.error(e)
    invalid.value = true
    message.value = 'An error occurred while signing in.'
    loading.value=false;  
  }
}
async function status(){
  try {
    const csrf=get_cookie('csrftoken')
    const data = await fetch(`${BASE_URL}/signin`, {
      method: 'GET',
      headers:{'X-CSRFToken':csrf},
      credentials: 'include'
    });
    const response = await data.json();
    if (response.status === 300) {
      window.location.href = '/codraw';
    } 
  } catch (e) {
    console.error(e);
  }
}
status();
</script>
<style scoped>
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform:translateY(-20px);
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.4s ease-in-out, transform 0.4s ease-in-out;
}

.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform:translateY(0);
}

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

.recovery-container {
  max-width: 400px;
  padding: 2rem;
  text-align: center;
  font-family: sans-serif;
}
</style>