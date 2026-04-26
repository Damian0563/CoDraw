<template>
	<Transition name="fade-slide">
		<div v-if="invalid" class="pop">
			<div :style="contentStyle"
				style="background: #23272f; color: #fff; padding: 32px 40px; border-radius: 16px; min-width: 320px; box-shadow: 0 8px 32px rgba(0,0,0,0.25); position: relative;">
				<button @click="close"
					style="position: absolute; top: 12px; right: 12px; background: transparent; border: none; color: #ccc; font-size: 20px; cursor: pointer;">
					✕
				</button>
				<p style="white-space: pre-line; text-align: left; line-height: 1.6;">{{ props.message }}</p>
				<div v-if="$slots.buttons" style="display: flex; gap: 10px; margin-top: 20px; justify-content: center;">
					<slot name="buttons"></slot>
				</div>
				<button v-else @click="close"
					style="margin-top: 20px; background: #4f8cff; color: #fff; border: none; border-radius: 8px; padding: 8px 20px; font-size: 1rem; cursor: pointer;">
					Close
				</button>
			</div>
		</div>
	</Transition>
</template>


<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue'
const props = defineProps({
	message: String,
	invalid: Boolean,
	top: {
		type: String,
		default: '0'
	}
})
const emit = defineEmits(['close'])
const invalid = ref(false)
watch(() => props.invalid, (newValue) => {
	invalid.value = newValue
})
const close = () => {
	invalid.value = false
	emit('close')
}
</script>

<style scoped>
.fade-slide-enter-from,
.fade-slide-leave-to {
	opacity: 0;
	transform: translateY(-20px);
}

.fade-slide-enter-active,
.fade-slide-leave-active {
	transition: opacity 0.4s ease-in-out, transform 0.4s ease-in-out;
}

.fade-slide-enter-to,
.fade-slide-leave-from {
	opacity: 1;
	transform: translateY(0);
}

.pop {
	position: fixed;
	top: 0;
	left: 0;
	width: 100vw;
	height: 100vh;
	background: rgba(0,0,0,0.35);
	z-index: 100;
	display: flex;
	align-items: center;
	justify-content: center;
}
</style>
