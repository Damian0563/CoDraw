<template>
    <div class="d-block justify-content-center align-items-center mt-4">
        <h1 class="my-2" style="color: yellow;">Password Restoration</h1>
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
        <div v-if="loading" class="spinner-overlay d-flex justify-content-center align-items-center">
            <VueSpinnerTail size="60" color="orange" />
        </div>
        <div class="popup-card mt-4">
            <h4 class="mb-3 text-white mt-5">Enter Verification Code sent to <span style="color:yellow;font-weight: bold;margin-bottom: 4rem;">{{ mail }}</span></h4>
            <div class="d-flex justify-content-center mt-4 mb-3">
                <input maxlength="1" id="1" @input="handleInput(2)" v-model="zero" ref="ZeroInput" class="code-input" type="text" pattern="[0-9]*" inputmode="numeric" autocomplete="off" autofocus/>
                <input maxlength="1" id="2" @input="handleInput(3)" v-model="one" ref="OneInput" class="code-input" type="text" pattern="[0-9]*" inputmode="numeric" autocomplete="off"/>
                <input maxlength="1" id="3" @input="handleInput(4)" v-model="two" ref="TwoInput" class="code-input" type="text" pattern="[0-9]*" inputmode="numeric" autocomplete="off"/>
                <input maxlength="1" id="4" @input="handleInput(5)" v-model="three" ref="ThreeInput" class="code-input" type="text" pattern="[0-9]*" inputmode="numeric" autocomplete="off"/>
                <input maxlength="1" id="5" class="code-input" v-model="four" ref="FourInput" type="text" pattern="[0-9]*" inputmode="numeric"/>
            </div>
            <button class="btn btn-primary" @click="submitCode">Verify</button>
        </div>
    </div>

</template>

<script setup>
import { onMounted, ref } from 'vue'
import {BASE_URL} from '../common.js'
import { get_cookie } from '@/common'
import {VueSpinnerTail} from 'vue3-spinners'
const mail =ref(new URL(window.location.href).pathname.split('/')[2])
const zero = ref(null)
const one = ref(null)
const two = ref(null)
const three = ref(null)
const four = ref(null)
const message = ref('')
const invalid = ref(false)
//const ZeroInput = ref(null)
const OneInput = ref(null)
const TwoInput = ref(null)
const ThreeInput = ref(null)
const FourInput = ref(null)
const loading=ref(false);
function getCode() {
    return `${zero.value}${one.value}${two.value}${three.value}${four.value}`;
}
function handleInput(index){
  if(index === 2 && OneInput.value) OneInput.value.focus()
  if(index === 3 && TwoInput.value) TwoInput.value.focus()
  if(index === 4 && ThreeInput.value) ThreeInput.value.focus()
  if(index === 5 && FourInput.value) FourInput.value.focus()
}
async function submitCode(){
    try{
        const data=await fetch(`${BASE_URL}/restore_password/${mail.value}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': get_cookie('csrftoken')
            },
            body: JSON.stringify({
                code: getCode()
            }),
            credentials: 'include'
        })
        const response=await data.json()
        if(response.status===200){
            alert("Code verified! You may now reset your password.")
        }else{  
            alert("Invalid code. Please try again.")
        }
    }catch(err){
        console.log(err)
    }
}
onMounted(()=>{
    loading.value=true;
    const mail =ref(new URL(window.location.href).pathname.split('/')[2])
    async function isValid(){
        try{
            const data=await fetch(`${BASE_URL}/restore_password/${mail.value}`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': get_cookie('csrftoken')
                },
                credentials: 'include'
            })
            const response=await data.json()
            return response.status===200
        }catch(err){
            console.log(err)
            window.location.href='/signin'
        }
    }
    isValid().then((res)=>{
        loading.value=false;
        console.log(res)
        if(!res){
            message.value="Provided mail is not registered or is invalid."
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