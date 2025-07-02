<template>
  <div
    style="
      position: relative;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
    "
  >
    <div
      style="
      position: absolute;
      top: 32px;
      left: 50%;
      transform: translateX(-50%);
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
      <select
      v-model="tool"
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
      min="1"
      max="50"
      style="
        accent-color: #4f8cff;
        width: 120px;
        margin-right: 8px;
      "
      >
      <span style="color: #fff; min-width: 32px; text-align: center;">{{ width_slider }}</span>
      <button
        @click="check_save()"
        style="
          background: #4f8cff;
          color: #fff;
          border: none;
          border-radius: 8px;
          padding: 8px 20px;
          font-size: 1rem;
          cursor: pointer;
          transition: background 0.2s;
        "
      >Save</button>
      <button
      @click="leave()"
      style="
        background: #ff4f4f;
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-size: 1rem;
        cursor: pointer;
        transition: background 0.2s;
      "
      >Exit</button>
    </div>
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
import { onMounted, ref} from 'vue';
const stageRef = ref(null);
const tool = ref('brush');
const isDrawing = ref(false);
const width_slider=ref(5);
const list=ref([])
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
context.save();
context.strokeStyle = 'red';
context.lineWidth = 2;
context.strokeRect(0, 0, canvas.width, canvas.height);
context.restore();
context.strokeStyle = '#fcfcfc';
context.lineJoin = 'round';
context.lineWidth = width_slider.value;

const load = () => {
  const data = localStorage.getItem('storage');
  if (data) {
    list.value = JSON.parse(data);
    // Draw the last saved image onto the canvas
    if (list.value.length > 0) {
      const lastImage = new window.Image();
      lastImage.src = list.value[list.value.length - 1].image;
      lastImage.onload = () => {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(lastImage, 0, 0);
        layerRef.value.getNode().batchDraw();
      };
    }
  }
};
const save_definetely = async()=>{
  try{
    const parts = new URL(window.location.href).pathname.split('/');
    const owner = parts[2]; // 'user_id'
    const room = parts[3];  // 'room_id
    const data=await fetch('http://localhost:8000/codraw/save_project',{
      method:"POST",
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf},
      body:JSON.stringify({
        "project":room,
        "owner":owner,
        "payload":canvas.toDataURL()
      })
    })
    const response=await data.json()
    console.log(response.status)
  }catch(e){
    console.error(e)
  }
}

const check_save = async () => {
  try{
    // const first_slash=window.location.href.indexOf('board')
    // const second_slash=window.location.href.lastIndexOf('/')
    // const room=window.location.href.slice(second_slash,window.location.href.length)
    // const owner=window.location.href.substring(first_slash,second_slash)
    const parts = new URL(window.location.href).pathname.split('/');
    const room = parts[3];  // 'room_id
    const data=await fetch('http://localhost:8000/codraw/save_project',{
      method:"POST",
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf},
      body:JSON.stringify({
        "project":room,
      })
    })
    const response=await data.json()
    if(response.status===200){
      console.log('saved successfuly')
    }else{
      //show up form with form and title that triggers save_def
      save_definetely()
    }
  }catch(e){
    console.error(e)
  }
}
function leave(){
  localStorage.removeItem('storage')
  window.location.href='http://localhost:8081/codraw'
}

window.addEventListener('resize', () => {
  const stage=stageRef.value.getNode()
  const newWidth = window.innerWidth;
  const newHeight = window.innerHeight;

  canvas.width = newWidth;
  canvas.height = newHeight;

  stage.width(newWidth);
  stage.height(newHeight);
  
  stage.draw();
});
const getRelativePointerPosition = (stage) => {
  const transform = stage.getAbsoluteTransform().copy();
  transform.invert();
  const pos = stage.getPointerPosition();
  return transform.point(pos);
};
const autosave = () => {
  // Save the canvas as a data URL (image)
  const dataUrl = canvas.toDataURL();
  // Store the image data and a timestamp/id in the list
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

  if (e.evt.button === 2) { // Right click
    isPanning.value = true;
    stage.draggable(true);
    stage.startDrag();
    lastPos.value = stage.getPointerPosition();
    return;
  }

  isDrawing.value = true;
  lastPos.value = getRelativePointerPosition(stage)
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
  ctx.lineWidth=width_slider.value
  ctx.globalCompositeOperation = tool.value === 'eraser' ? 'destination-out' : 'source-over';
  ctx.beginPath();
  const prevPos = lastPos.value;
  const newPos = getRelativePointerPosition(stage);

  ctx.moveTo(prevPos.x - image.x(), prevPos.y - image.y());
  ctx.lineTo(newPos.x - image.x(), newPos.y - image.y());
  ctx.stroke();
  ctx.closePath();

  lastPos.value = newPos;

  layerRef.value.getNode().batchDraw();
};

onMounted(()=>{
  load();
  const stage = stageRef.value.getNode(); // get Konva Stage
  const scaleBy = 1.05;
  stage.on('wheel', (e) => {
    e.evt.preventDefault();

    const oldScale = stage.scaleX();
    const pointer = stage.getPointerPosition();

    const mousePointTo = {
      x: (pointer.x - stage.x()) / oldScale,
      y: (pointer.y - stage.y()) / oldScale,
    };

    const direction = e.evt.deltaY > 0 ? 1 : -1;
    if(oldScale===1 && direction===-1) return;
    const newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy;
    
    stage.scale({ x: newScale, y: newScale });

    const newPos = {
      x: pointer.x - mousePointTo.x * newScale,
      y: pointer.y - mousePointTo.y * newScale,
    };

    stage.position(newPos);
    stage.batchDraw();
  });
})
setInterval(()=>autosave(),60000)
</script>