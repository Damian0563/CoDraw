<template>
  <div
    style="
      position: relative;
      width: 80vw;
      height: 90vh;
      overflow: hidden;
    "
  >
    <div v-if="loading" class="spinner-overlay">
      <VueSpinnerTail size="60" color="orange" />
    </div>
    <Transition name="fade-slide">
      <div v-if="showPopup"
        style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.35); z-index: 100; display: flex; align-items: center; justify-content: center;">
        <div style="background: #23272f; color: #fff; padding: 32px 40px; border-radius: 16px; min-width: 320px; box-shadow: 0 8px 32px rgba(0,0,0,0.25); position: relative;">
					<button @click="showPopup = false" aria-label="close pop up"
							style="position: absolute; top: 12px; right: 12px; background: transparent; border: none; color: #ccc; font-size: 20px; cursor: pointer;">
						✕
					</button>
					<p>{{message}}</p>
					<button v-if="message!=='Are you sure you would like to clear the board? This action is irreversible.'" aria-label="close" @click="showPopup = false" id="close_form"
						style="margin-top: 20px; background: #4f8cff; color: #fff; border: none; border-radius: 8px; padding: 8px 20px; font-size: 1rem; cursor: pointer;">
						Close
					</button>
        </div>
      </div>
    </Transition>
    <div
      id="toolbar"
			:class="{ 'vertical-toolbar': windowWidth < 800 }"
      style="
      position: absolute;
      top: 32px;
      left: 5%;
      background: rgba(30, 30, 30, 0.85);
      border-radius: 16px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.18);
      padding: 20px 32px;
      display: flex;
      align-items: center;
      gap: 20px;
      z-index: 10;
      "
    >
      <font-awesome-icon :icon="['fas','undo']" aria-label="Undo" class="feature-icon" @click="undo()"></font-awesome-icon>
      <font-awesome-icon :icon="['fas','redo']" aria-label="Redo" class="feature-icon" @click="redo()"></font-awesome-icon>
      <button aria-label="change motiv" @click="motiv=!motiv" style="border-radius: 50%;padding: 1rem;border-color: #f68608;border-width: 5px;"
      :style="{ backgroundColor: motiv ? '#ffffff' : '#000000' }"
      ></button>
      <text style="color: white;">Brush Color</text>
      <input type="color" aria-label="select color" v-model="color">
      <select
        v-model="tool"
				aria-label="tool selector(brush/eraser)"
        style="
          background: #23272f;
          color: #fff;
          border: none;
          border-radius: 8px;
          padding: 8px 16px;
          font-size: 1rem;
          outline: none;
          cursor: pointer;
        "
      >
        <option value="brush">Brush</option>
        <option value="eraser">Eraser</option>
      </select>
      <label style="color: #fff; font-size: 1rem; margin-right: 8px;">
        Line Width
      </label>
      <input
        type="range"
        v-model="width_slider"
				aria-label="Line width selector"
        min="1"
        max="20"
        style="
          accent-color: #4f8cff;
          width: 60px;
          margin-right: 8px;
        "
      >
      <span style="color: #fff; min-width: 32px; text-align: center;">{{ width_slider }}</span>
      </div>
    <div
      class="board-wrapper"
      :style="{ backgroundColor: motiv ? '#ffffff' : '#000000' }"
    >
      <v-stage
          ref="stageRef"
          :config="stageConfig"
          @mousedown="handleMouseDown"
          @mousemove="handleMouseMove"
          @mouseup="handleMouseUp"
          @touchstart="handleMouseDown"
          @touchmove="handleMouseMove"
          @touchend="handleMouseUp"
          @contextmenu="handleContextMenu"
          style="overflow-x: hidden;overflow-y: hidden;border: none !important;"
          >
          <v-layer ref="layerRef">
              <v-image
                ref="imageRef"
                :config="imageConfig"
              />
          </v-layer>
      </v-stage>
    </div>
  </div>
</template>

<script setup>
import { v4 as uuidv4 } from 'uuid'
import {VueSpinnerTail} from 'vue3-spinners'
const loading=ref(false)
import { onMounted, ref, onBeforeUnmount, onUnmounted} from 'vue';
const currentLine = ref(null)
import Konva from 'konva';
import { watch } from 'vue';
const stageRef = ref(null);
const windowWidth = ref(window.innerWidth);
const showPopup=ref(false)
const color = ref("#ffffff")
const background=ref("#000000")
const message=ref(null)
const tool = ref('brush');
const isDrawing = ref(false);
const width_slider=ref(5);
const list=ref([])
const lastPos = ref(null);
const imageRef = ref(null);
const layerRef = ref(null);
const isPanning = ref(false);
const motiv=ref(true)
const stroke_history=ref([])
const history_index=ref(0)
const stageConfig = {
  width: 4*document.documentElement.clientWidth,
  height: 4*document.documentElement.clientHeight,
  draggable: false
};

const handleContextMenu = (e) => {
  e.evt.preventDefault();
};
const canvas = document.createElement('canvas');
canvas.width = stageConfig.width;
canvas.height = stageConfig.height;

const context = canvas.getContext('2d');
context.strokeStyle = color.value;
context.fillStyle=background.value
context.lineJoin = 'round';
context.lineWidth = width_slider.value;
context.lineCap = 'round';
context.lineJoin = 'round';

watch(color, (newColor) => {
  context.strokeStyle = newColor;
});

function getCrop(image, size) {
  const width = size.width;
  const height = size.height;
  const aspectRatio = width / height;
  let newWidth;
  let newHeight;
  const imageRatio = image.width / image.height;
  if (aspectRatio >= imageRatio) {
    newWidth = image.width;
    newHeight = image.width / aspectRatio;
  } else {
    newWidth = image.height * aspectRatio;
    newHeight = image.height;
  }
  let x = 0;
  let y = 0;
  x = (image.width - newWidth) / 2;
  y = (image.height - newHeight) / 2
  return {
    cropX: x,
    cropY: y,
    cropWidth: newWidth,
    cropHeight: newHeight,
  };
}

function applyCrop(imgNode) {
  const image = imgNode.image();
  if (!image) return;
  const crop = getCrop(image, {
    width: imgNode.width(),
    height: imgNode.height()
  });
  imgNode.setAttrs(crop);
}


const MAX_HISTORY = 10;
function addToHistory() {
  const layer = layerRef.value.getNode();
  if (!layer) return;
  const children = layer.children || [];
  const lastChild = children[children.length - 1];
  if (!lastChild) return;
  const childConfig = lastChild.toJSON();
  if (history_index.value < stroke_history.value.length - 1) {
    stroke_history.value = stroke_history.value.slice(0, history_index.value + 1);
  }
  stroke_history.value.push(childConfig);
  history_index.value = stroke_history.value.length - 1;
  if (stroke_history.value.length > MAX_HISTORY) {
    stroke_history.value.shift();
    history_index.value = Math.max(0, history_index.value - 1);
  }
}

const undo=async()=>{
  if (history_index.value < 0) return;
  const layer = layerRef.value.getNode();
  const children = layer.children || [];
  const lastChild = children[children.length - 1];
  if (lastChild) lastChild.destroy();
  history_index.value--;
  layer.batchDraw();
}

const redo=()=>{
  if(history_index.value==MAX_HISTORY-1) return
  else{
    history_index.value++;
    const layer=layerRef.value.getNode()
    if(!stroke_history.value[history_index.value]) return;
    const history=JSON.parse(stroke_history.value[history_index.value])
    if (history){
      if(history.className==="Image"){
        const image = new window.Image()
        image.src=history.attrs.src
        image.onload = () => {
          const konvaImg = new Konva.Image({
            id: uuidv4(),
            image: image,
            x: history.attrs.x,
            y: history.attrs.y,
            width: image.width,
            height: image.height,
            draggable: false,
            src: history.attrs.src
          });
          applyCrop(konvaImg)
          konvaImg.setAttr("src", history.attrs.src);
          layer.add(konvaImg);
          layer.draw();
        }
      }else{
        const KonvaNode= Konva.Node.create(history)
        layer.add(KonvaNode)
        layer.draw()
      }
    }
  }
}
const handlePaste = (event) => {
  event.preventDefault();
  const stage = stageRef.value?.getNode?.();
  if (!stage) return;
  const pointer = stage.getPointerPosition() || { x: stage.width() / 2, y: stage.height() / 2 };
  const point = getRelativePointerPosition(stage, pointer);
  const clipboardData = event.clipboardData;
  if (!clipboardData || clipboardData.files.length === 0) {
    return;
  }
  const file = clipboardData.files[0];
  if (!file.type.startsWith('image/')) {
    return;
  }
  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new window.Image();
    img.src = e.target.result;
    img.onload = () => {
      const konvaImg = new Konva.Image({
        id: uuidv4(),
        image: img,
        x: point.x,
        y: point.y,
        width: img.width,
        height: img.height,
        draggable: false,
        src: e.target.result
      });
      applyCrop(konvaImg)
      const layer = layerRef.value.getNode();
      konvaImg.setAttr("src", e.target.result);
      layer.add(konvaImg);
      layer.draw();
      addToHistory()
  }
  }
  reader.readAsDataURL(file)
}

const getRelativePointerPosition = (stage) => {
  const transform = stage.getAbsoluteTransform().copy();
  transform.invert();
  const pos = stage.getPointerPosition();
  return transform.point(pos);
};
const autosave = () => {
  const stage = stageRef.value?.getNode?.();
  if (!stage) return;
  const dataUrl = stage.toDataURL();
  list.value = [{
    id: Date.now(),
    image: dataUrl
  }];
  localStorage.setItem('storage', JSON.stringify(list.value));
};

const imageConfig = {
  image: canvas,
  x: 0,
  y: 0,
  width: canvas.width,
  height: canvas.height
};
const handleMouseDown = (e) => {
  const stage = e.target.getStage();
  if (e.evt.button === 2) {
    isPanning.value = true;
    stage.draggable(true);
    stage.startDrag();
    lastPos.value = stage.getPointerPosition();
    return;
  }
  isDrawing.value = true;
  const pos = getRelativePointerPosition(stage);
  const newLine = new Konva.Line({
    stroke: color.value,
    strokeWidth: width_slider.value,
    globalCompositeOperation: tool.value === 'eraser' ? 'destination-out' : 'source-over',
    points: [pos.x, pos.y],
    lineCap: 'round',
    lineJoin: 'round'
  });
  layerRef.value.getNode().add(newLine);
  currentLine.value = newLine;
};

const handleMouseUp = (e) => {
  isDrawing.value = false;
  currentLine.value = null;
  addToHistory()
  if (isPanning.value) {
    const stage = e.target.getStage();
    stage.draggable(false);
    isPanning.value = false;
  }
};

const handleMouseMove = (e) => {
  if (!isDrawing.value || !currentLine.value) return;
  const stage = e.target.getStage();
  const point = getRelativePointerPosition(stage);
  const newPoints = currentLine.value.points().concat([point.x, point.y]);
  currentLine.value.points(newPoints);
  layerRef.value.getNode().batchDraw();
};

const keyhandler=(event)=>{
  if (event.ctrlKey && event.key === 'z') {
    undo()
  }
  else if (event.ctrlKey && event.key === 'y') {
    redo()
  }
}

const onResize = () => {
  windowWidth.value = window.innerWidth;
};

onMounted(async()=>{
  loading.value=true
  window.addEventListener('keyup',keyhandler)
  let resizeTimeout = null;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      const stage = stageRef.value?.getNode();
      const image = imageRef.value?.getNode();
      if (!stage || !image) return;
      const newWidth = window.innerWidth;
      const newHeight = window.innerHeight;
      canvas.width = newWidth * 4;
      canvas.height = newHeight * 4;
      stage.width(canvas.width);
      stage.height(canvas.height);
      image.width(canvas.width);
      image.height(canvas.height);
      const layer = image.getLayer();
      if (layer) layer.batchDraw();
    }, 100);
  });
  window.addEventListener('resize', onResize);
  window.addEventListener('paste', handlePaste)
  watch(motiv,()=>{
    background.value = motiv.value ? "#ffffff" : "#000000"
    color.value= motiv.value ? "#000000":"#ffffff"
  },{immediate:true})
  loading.value=false;
})
setInterval(()=>autosave(),60000)
onBeforeUnmount(()=>{
  loading.value=true
})
onUnmounted(()=>{
  window.removeEventListener('paste',handlePaste)
  window.removeEventListener("keyup",keyhandler)
  window.removeEventListener("resize",onResize)
})
</script>

<style>
html, body {
  margin: 0;
  height: 100%;
  overflow: hidden !important;
}
</style>

<style scoped>
.vertical-toolbar {
	justify-content: center;
  flex-direction: column !important;
  padding: 15px 15px !important;
}
#toolbar {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 20px;
}
@media(max-width:800px){
	#toolbar {
		justify-content: center;
    flex-direction: column;
    align-items: center;
    padding: 20px 20px;
		top: 50% !important;
		transform: translateY(-90%) !important;
		max-width: 70px;
    left: 10px;
  }
  #toolbar input[type="range"] {
    width: 50px !important;
  }
	#toolbar select {
		margin-top: 8px !important;
		font-size: 1rem !important;
		border-radius: 4px !important;
		width: 50px !important;
	}
}

.feature-icon {
  font-size: 1.25rem;
  color: orange;
  transition: transform 0.3s ease;
}

#confirm_clear{
  background-color: green !important;
  transition: 0.3s ease !important;
}

#confirm_clear:hover{
  background-color: #00cc00 !important;
}

.feature-icon:hover {
  transform: scale(1.2) rotate(5deg);
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform:translateY(-20px);
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
.board-wrapper {
  width: 100%;
  height: 100%;
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

.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0;
  right: 0; bottom: 0;
  background-color: #ccc;
  transition: 0.3s;
  border-radius: 34px;
}

.slider::before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  top: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #4f8cff;
}

input:checked + .slider::before {
  transform: translateX(18px);
}

@media(max-width:1500px) {
  #toolbar{
    font-size: 0.8rem;
    gap:10px;
  }
}
@media(max-width:1330px){
  #toolbar{
    left:2% !important;
  }
  #inv{
    right:0.5rem;
    font-size: 0.5rem;
  }
}
@media(max-width:1150px){
  #toolbar{
    gap: 5px !important;
  }
}

@media(max-width:1000px){
  #inv_div{
    top:140px !important;
    position: fixed !important;
  }
}
#zoom{
  position: fixed;
  right:40px;
  bottom:10px;
  background-color: white;
  z-index: 10;
}


#inv:hover,#bookmark-btn:hover,#save_btn:hover,#save_def:hover,#close_form:hover{
  background: #fff !important;
  color:#4f8cff !important;
}
#exit:hover{
  background:#fff!important;
  color:#ff4f4f !important;
}
#clearall:hover{
  background:#fff !important;
  color:#f68608 !important;
}
</style>
