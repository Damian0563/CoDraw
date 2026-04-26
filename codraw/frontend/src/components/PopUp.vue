<template>
	<Transition name="fade-slide">
		<div v-if="invalid" class="pop">
			<div
				style="background: #23272f; color: #fff; padding: 32px 40px; border-radius: 16px; min-width: 320px; box-shadow: 0 8px 32px rgba(0,0,0,0.25); position: relative; overflow: hidden;">
				<button @click="close"
					style="position: absolute; top: 12px; right: 12px; background: transparent; border: none; color: #ccc; font-size: 20px; cursor: pointer;">
					✕
				</button>
				<p style="white-space: pre-line; text-align: left; line-height: 1.6;">{{ props.message }}</p>
				<div v-if="$slots.buttons" style="display: flex; gap: 10px; margin-top: 20px; justify-content: center;">
					<slot name="buttons"></slot>
				</div>
				<div style="position: absolute; bottom: 0; left: 0; background:#ffc107;height:12px" :style="widthStyle"></div>
			</div>
		</div>
	</Transition>
</template>


<script setup>
import { ref, watch, defineProps, defineEmits, onUnmounted, computed } from 'vue'
const props = defineProps({
	message: String,
	invalid: Boolean,
	autoClose: Boolean
})
const emit = defineEmits(['close'])
const invalid = ref(false)
const width = ref(0)
const DURATION = 10000
let interval
watch(() => props.invalid, (newValue) => {
	invalid.value = newValue
	if (newValue && props.autoClose) {
		const start = Date.now()
		width.value = 0
		clearInterval(interval)
		interval = setInterval(() => {
			const elapsed = Date.now() - start
			width.value = Math.min(elapsed / DURATION, 1)
			if (width.value >= 1) {
				clearInterval(interval)
				close()
			}
		}, 10)
	} else {
		clearInterval(interval)
		width.value = 0
	}
})

const widthStyle = computed(() => {
	return {
		width: (width.value * 100) + '%'
	}
})

const close = () => {
	invalid.value = false
	clearInterval(interval)
	emit('close')
}

onUnmounted(() => {
	clearInterval(interval)
})
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
	background: rgba(0, 0, 0, 0.35);
	z-index: 100;
	display: flex;
	align-items: center;
	justify-content: center;
}
</style>
