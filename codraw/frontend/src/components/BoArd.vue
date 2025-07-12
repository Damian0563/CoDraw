<template>
  <div
    style="
      position: relative;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
    "
  >
    <div v-if="showPopup" 
       style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.35); z-index: 100; display: flex; align-items: center; justify-content: center;">
      <div style="background: #23272f; color: #fff; padding: 32px 40px; border-radius: 16px; min-width: 320px; box-shadow: 0 8px 32px rgba(0,0,0,0.25); position: relative;">
      <button @click="showPopup = false" 
          style="position: absolute; top: 12px; right: 12px; background: transparent; border: none; color: #ccc; font-size: 20px; cursor: pointer;">
        ✕
      </button>
      <p>{{message}}</p>
      <button @click="showPopup = false"
          style="margin-top: 20px; background: #4f8cff; color: #fff; border: none; border-radius: 8px; padding: 8px 20px; font-size: 1rem; cursor: pointer;">
        Close
      </button>
      </div>
    </div>
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
      <input type="color" v-model="color">
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
        @click="check_save('save')"
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
      <button
        style="
          background: #f68608;
          color: #fff;
          border: none;
          border-radius: 8px;
          padding: 8px 20px;
          font-size: 1rem;
          cursor: pointer;
          transition: background 0.2s;
        "
        @click="clear_all()"
        >
        Clear all
      </button>
    </div>
    <div
      v-if="isVisible"
      style="
        position: absolute;
        top: 120px;
        left: 50%;
        transform: translateX(-50%);
        backdrop-filter: blur(16px);
        background: rgba(30, 30, 30, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        padding: 32px;
        display: flex;
        flex-direction: column;
        gap: 20px;
        z-index: 20;
        min-width: 30vw;
        max-width: 90vw;
        font-family: 'Segoe UI', Roboto, sans-serif;
        color: #fff;
      "
    >
      <button
        @click="isVisible = false"
        style="
          position: absolute;
          top: 12px;
          right: 12px;
          background: transparent;
          border: none;
          color: #ccc;
          font-size: 20px;
          cursor: pointer;
          transition: color 0.2s;
        "
      >
        ✕
      </button>

      <div style="display: flex; flex-direction: column; gap: 6px;">
        <label class="align-self-start">Title</label>
        <input
          v-model="title"
          type="text"
          placeholder="Enter title"
          style="
            padding: 10px 14px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
            font-size: 1rem;
            outline: none;
            transition: border 0.2s;
          "
        />
      </div>

      <div style="display: flex; flex-direction: column; gap: 6px;">
        <label class="align-self-start">Description</label>
        <textarea
          v-model="description"
          rows="3"
          placeholder="Enter description"
          style="
            padding: 10px 14px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
            font-size: 1rem;
            resize: vertical;
            outline: none;
            transition: border 0.2s;
            resize: none;
          "
        ></textarea>
      </div>

      <div style="display: flex; align-items: center; gap: 10px;">
        <label style="flex-shrink: 0;">Private</label>
        <label class="switch">
          <input 
            v-model="type" 
            type="checkbox" 
            :true-value="'private'" 
            :false-value="'public'" 
          />
          <span class="slider"></span>
        </label>

        <!-- <span>{{ type === 'Private' ? 'Private' : 'Public' }}</span> -->
      </div>

      <button
        @click="save_definetely()"
        style="
          background: #4f8cff;
          color: #fff;
          border: none;
          border-radius: 12px;
          padding: 12px;
          font-size: 1rem;
          font-weight: 500;
          cursor: pointer;
          transition: background 0.2s;
          transition: 0.5s ease-out;
        "
        class="save"
      >
        Save Details
      </button>
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
</template>

<script setup>
import { get_cookie } from '@/common';
const csrf = get_cookie('csrftoken');
import { onMounted, ref} from 'vue';
import { watch } from 'vue';
const stageRef = ref(null);
const isVisible=ref(false)
const showPopup=ref(false)
const color = ref("#ffffff")
const title=ref(null)
const message=ref(null)
const description=ref(null)
const type=ref('Public')
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
context.strokeStyle = color.value;
context.lineJoin = 'round';
context.lineWidth = width_slider.value;
context.lineCap = 'round';
context.lineJoin = 'round';

watch(color, (newColor) => {
  context.strokeStyle = newColor;
});
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
    await new Promise(resolve => requestAnimationFrame(resolve));
    const imageData = canvas.toDataURL("image/png");
    const data=await fetch('http://localhost:8000/codraw/save_new',{
      method:"POST",
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf},
      body:JSON.stringify({
        "project":room,
        "owner":owner,
        "payload":imageData,
        "title":title.value,
        "description":description.value,
        "type":type.value,
      })
    })
    const response=await data.json()
    isVisible.value=false
    if(response.status===200){
      showPopup.value=true
      message.value="Board saved successfully."
    }else{
      showPopup.value=true
      message.value="There was an error saving your board."
    }
  }catch(e){
    console.error(e)
  }
}

const check_save = async (mode) => {
  try{
    const parts = new URL(window.location.href).pathname.split('/');
    const room = parts[3];  // 'room_id
    const data=await fetch('http://localhost:8000/codraw/save_project',{
      method:"POST",
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf},
      body:JSON.stringify({
        "project":room,
        "payload":canvas.toDataURL()
      })
    })
    const response=await data.json()
    if(mode === 'save'){
      if(response.status===200){
        showPopup.value=true
        message.value="Board was successfully quick saved."
      }else{
      isVisible.value=true
      }
    }else if(mode=='load'){
      if(response.status===200){
        return true
      }
      return false
    }
    
  }catch(e){
    console.error(e)
  }
}
function leave(){
  localStorage.removeItem('storage')
  window.location.href='http://localhost:8081/codraw'
}

function clear_all(){
  localStorage.removeItem('storage')
  context.clearRect(0, 0, canvas.width, canvas.height);
  layerRef.value.getNode().clear();
  layerRef.value.getNode().batchDraw();
  // context.clearRect(0, 0, canvas.width, canvas.height);
  // layerRef.value.getNode().batchDraw();
}

window.addEventListener('resize', () => {
  const stage = stageRef.value?.getNode();
  const image = imageRef.value?.getNode();

  if (!stage || !image) return;

  // New viewport dimensions
  const newWidth = window.innerWidth;
  const newHeight = window.innerHeight;

  // Resize canvas element (backing image)
  canvas.width = newWidth * 4; // Keep your 4x scaling if needed
  canvas.height = newHeight * 4;

  // Resize Konva Stage
  stage.width(canvas.width);
  stage.height(canvas.height);

  // Resize Konva Image config
  image.width(canvas.width);
  image.height(canvas.height);

  // Redraw the image (to avoid flickering)
  image.getLayer().batchDraw();
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
  const stage = e.target.getStage();
  ctx.lineWidth=width_slider.value
  ctx.strokeStyle = color.value
  ctx.globalCompositeOperation = tool.value === 'eraser' ? 'destination-out' : 'source-over';
  ctx.beginPath();
  const prevPos = lastPos.value;
  const newPos = getRelativePointerPosition(stage);
  // const image = imageRef.value.getNode();
  // ctx.moveTo(prevPos.x - image.x(), prevPos.y - image.y());
  // ctx.lineTo(newPos.x - image.x(), newPos.y - image.y());
  ctx.moveTo(prevPos.x, prevPos.y);
  ctx.lineTo(newPos.x, newPos.y);
  ctx.stroke();
  ctx.closePath();

  lastPos.value = newPos;

  layerRef.value.getNode().batchDraw();
};

const get_details_and_load = async()=>{
  try{
    const parts = new URL(window.location.href).pathname.split('/');
    const room = parts[3];
    const data=await fetch('http://localhost:8000/codraw/get_details',{
      method:"POST",
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrf
      },
      credentials:"include",
      body:JSON.stringify({
        "project":room
      })
    })
    const response=await data.json()
    const imageUrl = response.canva;
    console.log(imageUrl)
    if (imageUrl) {
      const img = new Image();
      img.onload = () => {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(img, 0, 0, canvas.width, canvas.height);
        layerRef.value.getNode().batchDraw();
      };
      img.onerror = (e) => console.error("Image failed to load", e);
      img.src = imageUrl;
    }
  }catch(e){
    console.error(e)
  }
}

onMounted(async()=>{
  if(await check_save('load')){
    get_details_and_load()
  }else{
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
  }
})
setInterval(()=>autosave(),60000)
</script>

<style scoped>
.save:hover{
  background:#fff ;
  color: #4f8cff;
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
</style>