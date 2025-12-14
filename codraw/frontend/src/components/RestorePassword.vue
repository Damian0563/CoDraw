<template>
    <div class="d-block justify-content-center align-items-center mt-4">
        <h1 class="my-2" style="color: yellow;">Password Restoration</h1>
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
import { ref } from 'vue'
import {BASE_URL} from '../common.js'
import { get_cookie } from '@/common'
const mail =ref(new URL(window.location.href).pathname.split('/')[2])
const zero = ref(null)
const one = ref(null)
const two = ref(null)
const three = ref(null)
const four = ref(null)
const ZeroInput = ref(null)
const OneInput = ref(null)
const TwoInput = ref(null)
const ThreeInput = ref(null)
const FourInput = ref(null)
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
</style>