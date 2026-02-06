<template>
    <div class="d-flex flex-column min-vh-100">
        <div class="flex-grow-1 d-flex flex-column justify-content-center align-items-center mt-2 mb-3">
        <h1 class="my-4" style="color: yellow;">Password Restoration</h1>
        <Transition name="fade-slide">
            <div v-if="invalid" class="alert alert-danger text-center custom-alert p-2"
                role="alert"
                style="max-width: 70vw; width: 440px; position: fixed; top: 4rem; left: 50%; transform: translateX(-50%); z-index: 10000; font-size: 0.95rem; border-radius: 0.7rem; box-shadow: 0 2px 8px rgba(220,53,69,0.10); background: #222; border: 1.5px solid #dc3545;">
                <button @click="invalid=false" class="close-btn rounded-circle float-end" aria-label="Close" style="background-color: #dc3545; color: #fff; border: none; width: 1.5rem; height: 1.5rem; font-size: 1.1rem; margin-top: -0.3rem; margin-right: -0.3rem; line-height: 1.1rem;">&times;</button>
                <div class="alert-content" style="padding-top: 0.2rem;">
                    <strong style="color: #ffc107; font-size: 1rem;">{{ message }}</strong>
                    <div style="color: #fff; margin-top: 0.2rem; font-size: 0.92rem;">Please try again.</div>
                </div>
            </div>
        </Transition>
        <Transition name="fade-slide">
            <div v-if="updated" class="alert alert-success text-center custom-alert p-2"
                role="alert"
                style="max-width: 70vw; width: 440px; position: fixed; top: 4rem; left: 50%; transform: translateX(-50%); z-index: 10000; font-size: 0.95rem; border-radius: 0.7rem; box-shadow: 0 2px 8px rgba(40,167,69,0.10); background: #222; border: 1.5px solid #28a745;">
                <button @click="updated=false" class="close-btn rounded-circle float-end" aria-label="Close" style="background-color: #28a745; color: #fff; border: none; width: 1.5rem; height: 1.5rem; font-size: 1.1rem; margin-top: -0.3rem; margin-right: -0.3rem; line-height: 1.1rem;">&times;</button>
                <div class="alert-content" style="padding-top: 0.2rem;">
                    <strong style="color: #28a745; font-size: 1rem;">Password successfully updated!</strong>
                    <div style="color: #fff; margin-top: 0.2rem; font-size: 0.92rem;">You can now sign in with your new password. You will be redirected in 10 seconds to the sign in page.</div>
                </div>
            </div>
        </Transition>
        <div v-if="loading" class="spinner-overlay d-flex justify-content-center align-items-center">
            <VueSpinnerTail size="60" color="orange" />
        </div>
        <Transition name="fade-slide">
            <div class="container align-items-center w-25 mt-4 bg-white rounded p-4">
                <h2 class="text-center mb-5 text-black">Enter New Password</h2>
                <div class="input-group">
                    <input type="password" id="new" v-model="new_password" class="form-control bg-dark text-black bg-white border-secondary mb-3" placeholder="Enter new password" required/>
                    <font-awesome-icon :icon="['fas', 'eye']" class="input-icon mt-2 mx-2" style="cursor: pointer;" @click="togglePasswordVisibility('new_password')" />
                </div>
                <div class="input-group">
                    <input type="password" id="confirm" v-model="confirm_password" class="form-control bg-dark text-black bg-white border-secondary mb-3" placeholder="Confirm new password" required/>
                    <font-awesome-icon :icon="['fas', 'eye']" class="input-icon mt-2 mx-2" style="cursor: pointer;" @click="togglePasswordVisibility('confirm_password')" />
                </div>
                <div v-if="new_password===confirm_password && new_password.length>0">
                    <button @click="init()" class="btn btn-primary w-100 mt-2">Restore Password</button>
                </div>
                <div v-else>
                    <button disabled class="btn btn-secondary w-100 mt-2">Restore Password</button>
                    <label class="text-danger mt-2 d-block text-center">Passwords do not match.</label>
                </div>
            </div>
        </Transition>
        </div>
        <Footer />
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import {BASE_URL} from '../common.js'
import { get_cookie } from '@/common'
import {VueSpinnerTail} from 'vue3-spinners'
import Footer from '@/components/Footer.vue'
const message = ref('')
const invalid = ref(false)
const loading=ref(false);
const updated=ref(false);
const new_password=ref('');
const confirm_password=ref('');

function togglePasswordVisibility(field) {
    const inputField = field === 'new_password' ? document.querySelector('#new') : document.querySelector('#confirm');
    if (inputField.type === 'password') {
        inputField.type = 'text';
    } else {
        inputField.type = 'password';
    }
}

async function restorePassword(){
    try{
        loading.value=true;
        const code =new URL(window.location.href).pathname.split('/')[2]
        const data=await fetch(`${BASE_URL}/recover/${code}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': get_cookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify({
                new_password: new_password.value,
            })
        })
        const response=await data.json()
        return response.status===200
    }catch(err){
        loading.value=false;
        message.value="An error occurred. Please try again.";
        invalid.value=true;
    }
    loading.value=false;
}

const init=()=>{
    restorePassword().then((res)=>{
    loading.value=false;
    if(res){
        updated.value=true;
        setTimeout(()=>{
            window.location.href=`${window.location.origin}/signin`
        },10000)
    }else{
        message.value="Failed to update password. The recovery link may be invalid or expired.";
        invalid.value=true;
    }
    })
}



onMounted(()=>{
    loading.value=true;
    const code =ref(new URL(window.location.href).pathname.split('/')[2])
    async function isValid(){
        try{
            const data=await fetch(`${BASE_URL}/recover/${code.value}`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': get_cookie('csrftoken')
                },
                credentials: 'include'
            })
            const response=await data.json()
            return response.status===200
        }catch(err){
            window.location.href='/signin'
        }
    }
    isValid().then((res)=>{
        loading.value=false;
        if(!res){
            message.value="Recovery link is either invalid or expired."
            invalid.value=true;
        }
    })
})
</script>

<style>
.code-input {
    width: 5rem;
    height: 5rem;
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

.spinner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.8);
}
</style>
