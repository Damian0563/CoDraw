<template>
  <div
    style="
      position: relative;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
    "
  >
    <div>
      <select v-model="tool">
        <option value="brush">Brush</option>
        <option value="eraser">Eraser</option>
      </select>
    </div>
    <v-stage
        :config="stageConfig"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
        @touchstart="handleMouseDown"
        @touchmove="handleMouseMove"
        @touchend="handleMouseUp"
         @contextmenu="handleContextMenu"
        style="overflow-x: hidden;overflow-y: hidden;"
        >
        <v-layer ref="layerRef">
            <v-image
            ref="imageRef"
            :config="imageConfig"
            />
        </v-layer>
    </v-stage>
  </div>
</template>

<script setup>
import { get_cookie } from '@/common';
const csrf = get_cookie('csrftoken');
console.log(csrf);
import { ref} from 'vue';

const tool = ref('brush');
const isDrawing = ref(false);
const lastPos = ref(null);
const imageRef = ref(null);
const layerRef = ref(null);
const isPanning = ref(false);
const stageConfig = {
  width: 4*document.documentElement.clientWidth,
  height: 4*document.documentElement.clientHeight,
  draggable: false
};
const handleContextMenu = (e) => {
  e.evt.preventDefault();
};
// create canvas element
const canvas = document.createElement('canvas');
canvas.width = stageConfig.width;
canvas.height = stageConfig.height;

// get context
const context = canvas.getContext('2d');
context.strokeStyle = '#fcfcfc';
context.lineJoin = 'round';
context.lineWidth = 5;

const imageConfig = {
  image: canvas,
  x: 0,
  y: 0
};

const handleMouseDown = (e) => {
  const stage = e.target.getStage();

  if (e.evt.button === 2) { // Right click
    isPanning.value = true;
    stage.draggable(true);
    stage.startDrag();
    lastPos.value = stage.getPointerPosition();
    return;
  }

  isDrawing.value = true;
  lastPos.value = stage.getPointerPosition();
};

const handleMouseUp = (e) => {
  isDrawing.value = false;
  if (isPanning.value) {
    const stage = e.target.getStage();
    stage.draggable(false);
    isPanning.value = false;
  }
};

const handleMouseMove = (e) => {
  if (!isDrawing.value) {
    return;
  }

  const ctx = context;
  const image = imageRef.value.getNode();
  const stage = e.target.getStage();

  ctx.globalCompositeOperation = tool.value === 'eraser' ? 'destination-out' : 'source-over';
  ctx.beginPath();

  const localPos = {
    x: lastPos.value.x - image.x(),
    y: lastPos.value.y - image.y(),
  };
  ctx.moveTo(localPos.x, localPos.y);

  const pos = stage.getPointerPosition();
  const newLocalPos = {
    x: pos.x - image.x(),
    y: pos.y - image.y(),
  };
  ctx.lineTo(newLocalPos.x, newLocalPos.y);
  ctx.closePath();
  ctx.stroke();

  lastPos.value = pos;
  layerRef.value.getNode().batchDraw();
};
</script>