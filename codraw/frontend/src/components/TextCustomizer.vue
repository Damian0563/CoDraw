<template>
	<div class="modal-backdrop" @click="emit('close')">
		<div class="text-customizer" @click.stop>
			<button class="close-btn justify-content-end" @click="emit('close')">&times;</button>
			<h5 class="text-light mb-3">Text Settings</h5>
			<div class="mb-3">
				<label class="form-label text-light small">Font Size</label>
				<div class="input-group">
					<span class="input-group-text bg-dark text-light border-secondary">
						<font-awesome-icon :icon="['fas', 'text-height']"></font-awesome-icon>
					</span>
					<input type="number" class="form-control bg-dark text-light border-secondary" v-model="fontSize" min="8"
						max="144" placeholder="16" />
					<span class="input-group-text bg-dark text-light border-secondary">px</span>
				</div>
			</div>
			<div class="mb-3">
				<label class="form-label text-light small">Font Family</label>
				<div class="input-group">
					<span class="input-group-text bg-dark text-light border-secondary">
						<font-awesome-icon :icon="['fas', 'font']"></font-awesome-icon>
					</span>
					<select class="form-select bg-dark text-light border-secondary" v-model="fontFamily">
						<option value="Arial, sans-serif">Arial</option>
						<option value="'Times New Roman', serif">Times New Roman</option>
						<option value="'Courier New', monospace">Courier New</option>
						<option value="Georgia, serif">Georgia</option>
						<option value="Verdana, sans-serif">Verdana</option>
						<option value="Tahoma, sans-serif">Tahoma</option>
						<option value="'Trebuchet MS', sans-serif">Trebuchet MS</option>
						<option value="Impact, sans-serif">Impact</option>
						<option value="'Comic Sans MS', cursive">Comic Sans MS</option>
						<option value="'Open Sans', sans-serif">Open Sans</option>
						<option value="'Roboto', sans-serif">Roboto</option>
					</select>
				</div>
			</div>
			<div class="mb-3">
				<label class="form-label text-light small">Color</label>
				<div class="d-flex align-items-center gap-2">
					<input type="color" class="form-control form-control-color bg-dark border-secondary" v-model="color"
						title="Choose text color" />
					<input type="text" class="form-control bg-dark text-light border-secondary color-text" v-model="color"
						placeholder="#000000" />
				</div>
			</div>
			<div class="mb-3">
				<label class="form-label text-light small">Background Color</label>
				<div class="d-flex align-items-center gap-2">
					<input type="color" class="form-control form-control-color bg-dark border-secondary" v-model="backgroundColor"
						title="Choose background color" />
					<input type="text" class="form-control bg-dark text-light border-secondary color-text"
						v-model="backgroundColor" placeholder="transparent" />
				</div>
			</div>
			<div class="mt-4">
				<button class="btn btn-outline-light w-100" @click="resetSettings">
					<font-awesome-icon :icon="['fas', 'rotate-left']" class="me-2"></font-awesome-icon>
					Reset
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, defineEmits, defineProps, watch } from 'vue'
const props = defineProps({
	textObject: {
		type: Object,
		default: null
	}
})
const fontSize = ref(16)
const fontFamily = ref('Arial, sans-serif')
const color = ref('#000000')
const backgroundColor = ref('transparent')
const isBold = ref(false)
const emit = defineEmits(['update:textStyle', 'close'])

watch(() => props.textObject, (newVal) => {
	if (newVal) {
		fontSize.value = newVal.fontSize() || 16
		fontFamily.value = newVal.fontFamily() || 'Arial, sans-serif'
		color.value = newVal.fill() || '#000000'
		backgroundColor.value = newVal.fill() || 'transparent'
		const fontStyle = newVal.fontStyle() || 'normal'
		isBold.value = fontStyle.includes('bold')
		// if (textStyle.value)
		// 	emit('update:textStyle', textStyle.value)
	}
}, { immediate: true })

const textStyle = computed(() => ({
	fontSize: `${fontSize.value}px`,
	fontFamily: fontFamily.value,
	color: color.value,
	backgroundColor: backgroundColor.value,
	fontWeight: isBold.value ? 'bold' : 'normal',
}))

console.log(textStyle.value)

function resetSettings() {
	fontSize.value = 16
	fontFamily.value = 'Arial, sans-serif'
	color.value = '#000000'
	backgroundColor.value = 'transparent'
	isBold.value = false
}
</script>

<style scoped>
.modal-backdrop {
	position: fixed;
	top: 12%;
	left: 3%;
	width: 340px;
	background: rgba(0, 0, 0, 0.35);
	z-index: 50;
	display: flex;
	border-radius: 16px;
	height: fit-content
}

.text-customizer {
	position: relative;
	align-items: center;
	justify-content: center;
	padding: 24px;
	flex-direction: column;
	background: #23272f;
	border-radius: 16px;
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
	z-index: 51;
}

.close-btn {
	position: absolute;
	top: 12px;
	right: 12px;
	background: transparent;
	border: none;
	color: #ccc;
	font-size: 24px;
	cursor: pointer;
	line-height: 1;
	padding: 0;
	transition: color 0.2s;
}

.close-btn:hover {
	color: #fff;
}

.form-label {
	font-weight: 500;
	margin-bottom: 0.3rem;
}

.form-control:focus,
.form-select:focus {
	background-color: #2a2a2a;
	border-color: #ffc107;
	color: #ffffff;
	box-shadow: 0 0 0 0.2rem rgba(255, 193, 7, 0.25);
}

.btn-outline-warning {
	background-color: transparent;
	border-color: #ffc107;
	color: #ffc107;
}

.btn-outline-warning:hover,
.btn-outline-warning.active {
	background-color: #ffc107;
	color: #1a1a1a;
}

.input-group-text {
	min-width: 40px;
	justify-content: center;
}

.form-control-color {
	width: 50px;
	height: 38px;
	padding: 0.25rem;
	cursor: pointer;
}

.color-text {
	max-width: 100px;
}

.btn-group .btn {
	flex: 1;
}
</style>
