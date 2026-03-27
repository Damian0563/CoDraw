<template>
	<div class="text-customizer container-fluid mx-auto p-3">
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
				<input type="text" class="form-control bg-dark text-light border-secondary" v-model="color"
					placeholder="#000000" style="max-width: 100px;" />
			</div>
		</div>

		<div class="mb-3">
			<label class="form-label text-light small">Background Color</label>
			<div class="d-flex align-items-center gap-2">
				<input type="color" class="form-control form-control-color bg-dark border-secondary" v-model="backgroundColor"
					title="Choose background color" />
				<input type="text" class="form-control bg-dark text-light border-secondary" v-model="backgroundColor"
					placeholder="transparent" style="max-width: 100px;" />
			</div>
		</div>

		<div class="mb-3">
			<label class="form-label text-light small">Text Style</label>
			<div class="btn-group w-100" role="group">
				<button type="button" class="btn btn-outline-warning" :class="{ active: isBold }" @click="isBold = !isBold"
					title="Bold">
					<font-awesome-icon :icon="['fas', 'bold']"></font-awesome-icon>
				</button>
				<button type="button" class="btn btn-outline-warning" :class="{ active: isItalic }"
					@click="isItalic = !isItalic" title="Italic">
					<font-awesome-icon :icon="['fas', 'italic']"></font-awesome-icon>
				</button>
				<button type="button" class="btn btn-outline-warning" :class="{ active: isUnderline }"
					@click="isUnderline = !isUnderline" title="Underline">
					<font-awesome-icon :icon="['fas', 'underline']"></font-awesome-icon>
				</button>
			</div>
		</div>
		<div class="mb-3">
			<label class="form-label text-light small">Line Height</label>
			<div class="input-group">
				<span class="input-group-text bg-dark text-light border-secondary">
					<font-awesome-icon :icon="['fas', 'arrows-up-down']"></font-awesome-icon>
				</span>
				<input type="number" class="form-control bg-dark text-light border-secondary" v-model="lineHeight" min="0.5"
					max="3" step="0.1" placeholder="1.5" />
			</div>
		</div>

		<div class="mb-3">
			<label class="form-label text-light small">Letter Spacing</label>
			<div class="input-group">
				<span class="input-group-text bg-dark text-light border-secondary">
					<font-awesome-icon :icon="['fas', 'text-width']"></font-awesome-icon>
				</span>
				<input type="number" class="form-control bg-dark text-light border-secondary" v-model="letterSpacing" min="-5"
					max="20" step="0.5" placeholder="0" />
				<span class="input-group-text bg-dark text-light border-secondary">px</span>
			</div>
		</div>

		<div class="mt-4">
			<button class="btn btn-warning w-100 mb-2" @click="applySettings">
				<font-awesome-icon :icon="['fas', 'check']" class="me-2"></font-awesome-icon>
				Apply Settings
			</button>
			<button class="btn btn-outline-light w-100" @click="resetSettings">
				<font-awesome-icon :icon="['fas', 'rotate-left']" class="me-2"></font-awesome-icon>
				Reset
			</button>
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
const isItalic = ref(false)
const isUnderline = ref(false)
const lineHeight = ref(1.5)
const letterSpacing = ref(0)
const emit = defineEmits(['update:textStyle'])

watch(() => props.textObject, (newVal) => {
	if (newVal) {
		fontSize.value = newVal.fontSize() || 16
		fontFamily.value = newVal.fontFamily() || 'Arial, sans-serif'
		color.value = newVal.fill() || '#000000'
		backgroundColor.value = newVal.fill() || 'transparent'
		const fontStyle = newVal.fontStyle() || 'normal'
		isBold.value = fontStyle.includes('bold')
		isItalic.value = fontStyle.includes('italic')
		const textDecoration = newVal.textDecoration() || 'none'
		isUnderline.value = textDecoration.includes('underline')
		lineHeight.value = newVal.lineHeight() || 1.5
		letterSpacing.value = newVal.letterSpacing() || 0
	}
}, { immediate: true })

const textStyle = computed(() => ({
	fontSize: `${fontSize.value}px`,
	fontFamily: fontFamily.value,
	color: color.value,
	backgroundColor: backgroundColor.value,
	fontWeight: isBold.value ? 'bold' : 'normal',
	fontStyle: isItalic.value ? 'italic' : 'normal',
	textDecoration: isUnderline.value ? 'underline' : 'none',
	lineHeight: lineHeight.value,
	letterSpacing: `${letterSpacing.value}px`
}))

function applySettings() {
	emit('update:textStyle', textStyle.value)
}

function resetSettings() {
	fontSize.value = 16
	fontFamily.value = 'Arial, sans-serif'
	color.value = '#000000'
	backgroundColor.value = 'transparent'
	isBold.value = false
	isItalic.value = false
	isUnderline.value = false
	lineHeight.value = 1.5
	letterSpacing.value = 0
}
</script>

<style scoped>
.text-customizer {
	width: 100%;
	height: 100%;
	display: flex;
	flex-direction: column;
	background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
	border-radius: 8px;
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

.btn-group .btn {
	flex: 1;
}
</style>
