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
      id="toolbar"
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
      <text style="color: white;">Brush Color</text>
      <input type="color" v-model="color">
      <text style="color: white;">Background Color</text>
      <input type="color" v-model="background">
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
        max="20"
        style="
          accent-color: #4f8cff;
          width: 60px;
          margin-right: 8px;
        "
      >
      <span style="color: #fff; min-width: 32px; text-align: center;">{{ width_slider }}</span>
      <button
        id="save_btn"
        @click="check_save('save')"
        style="
          background: #4f8cff;
          color: #fff;
          border: none;
          border-radius: 8px;
          padding: 8px 20px;
          font-size: 1rem;
          cursor: pointer;
          transition: ease-in-out 0.6s;
        "
      >Save</button>
      <button
      @click="leave()"
      id="exit"
      style="
        background: #ff4f4f;
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-size: 1rem;
        cursor: pointer;
        transition: ease-in-out 0.6s;
      "
      >Exit</button>
      <button
        id="clearall"
        style="
          background: #f68608;
          color: #fff;
          border: none;
          border-radius: 8px;
          padding: 8px 20px;
          font-size: 1rem;
          cursor: pointer;
          transition: ease-in-out 0.6s;
        "
        @click="clear_all()"
        >
        Clear all
      </button>
    </div>
    <div id="inv_div" style="position: absolute; top: 32px; right: 1rem; z-index: 10;">
      <button
        id="inv"
        @click="copyInvitationLink"
        style="
          display: flex;
          align-items: center;
          gap: 8px;
          background: #4f8cff;
          color: #fff;
          border: none;
          border-radius: 10px;
          padding: 10px 18px;
          font-size: 0.95rem;
          font-weight: 500;
          cursor: pointer;
          transition: ease-in-out 0.6s;
        "
      >
        <img :src="url" alt="Copy" style="width: 18px; height: 18px;" />
        <span v-if="show_text">Copy invitation link</span>
      </button>
    </div>
    <Transition name="fade-slide">
      <div
        v-if="isVisible"
        style="
          position: absolute;
          top: 150px;
          left: 35%;
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
          transition: ease-in-out 0.6s;
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
    </Transition>

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
import url from '@/assets/email.webp'
import { get_cookie } from '@/common';
const csrf = get_cookie('csrftoken');
import { onMounted, ref, onBeforeUnmount, computed} from 'vue';
const currentLine = ref(null)
import Konva from 'konva';
import { watch } from 'vue';
import { nextTick } from 'vue';
const stageRef = ref(null);
const windowWidth = ref(window.innerWidth);
const admin=ref(false)
const isVisible=ref(false)
const showPopup=ref(false)
const color = ref("#ffffff")
const background=ref("#000000")
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

const show_text = computed(() => windowWidth.value > 1330);
const stageConfig = {
  width: 4*document.documentElement.clientWidth,
  height: 4*document.documentElement.clientHeight,
  draggable: false
};

const ws=ref(null)
const room=ref(new URL(window.location.href).pathname.split('/')[3])
ws.value = new WebSocket(`ws://localhost:8000/ws/socket/${room.value}/`)
ws.value.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (!data || !data.type) return;

  const layer = layerRef.value.getNode();

  if (data.type === "start") {
    const newLine = new Konva.Line({
      stroke: data.stroke,
      strokeWidth: data.width,
      globalCompositeOperation: data.operation,
      points: data.points,
      lineCap: "round",
      lineJoin: "round"
    });
    newLine._remote = true;
    layer.add(newLine);
    currentLine.value = newLine;
  } else if (data.type === "draw" && currentLine.value?._remote) {
    const newPoints = currentLine.value.points().concat(data.points);
    currentLine.value.points(newPoints);
    layer.batchDraw();
  }
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
context.fillStyle=background.value
context.lineJoin = 'round';
context.lineWidth = width_slider.value;
context.lineCap = 'round';
context.lineJoin = 'round';

watch(color, (newColor) => {
  context.strokeStyle = newColor;
});

const check_owner=async()=>{
  try{
    const parts = new URL(window.location.href).pathname.split('/');
    const owner = parts[2]; // 'user_id'
    // const room = parts[3];  // 'room_id
    const data=await fetch("http://localhost:8000/codraw/check_owner",{
      method:"POST",
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrf
      },
      credentials:"include",
      body:JSON.stringify({
        "owner":owner
      })
    })
    const response=await data.json()
    if(response.status===200){
      admin.value=true
    }
  }catch(e){
    console.error(e)
  }
}

const copyInvitationLink = async () => {
  try {
    const link = window.location.href;
    await navigator.clipboard.writeText(link);
    showPopup.value = true;
    message.value = "Invitation link copied to clipboard!";
  } catch (err) {
    console.error("Failed to copy: ", err);
    showPopup.value = true;
    message.value = "Failed to copy the link.";
  }
};

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
    const data=await fetch('http://localhost:8000/codraw/save_new',{
      method:"POST",
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf},
      body:JSON.stringify({
        "project":room,
        "owner":owner,
        "payload":JSON.stringify(stageRef.value.getStage().toJSON()),
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
      autosave()
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
    if(mode==='save'){
      const data=await fetch('http://localhost:8000/codraw/save_project',{
        method:"POST",
        headers:{'Content-Type':'application/json','X-CSRFToken':csrf},
        body:JSON.stringify({
          "project":room,
          "payload": JSON.stringify(stageRef.value.getStage().toJSON())
        })
      })
      const response=await data.json()
      if(response.status===200){
        autosave()
        showPopup.value=true
        message.value="Board was successfully quick saved."
      }else{
        isVisible.value=true
      }
    }else if(mode==='load'){
      const data=await fetch('http://localhost:8000/codraw/save_project',{
        method:"POST",
        headers:{'Content-Type':'application/json','X-CSRFToken':csrf},
        body:JSON.stringify({
          "project":room,
        })
      })
      const response=await data.json()
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
const getRelativePointerPosition = (stage) => {
  const transform = stage.getAbsoluteTransform().copy();
  transform.invert();
  const pos = stage.getPointerPosition();
  return transform.point(pos);
};
const autosave = () => {
  // Save the canvas as a data URL (image)
  const stage = stageRef.value?.getNode?.();
  if (!stage) return;
  const dataUrl = stage.toDataURL();
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
  ws.value.send(JSON.stringify({
    type: "start",
    stroke: color.value,
    width: width_slider.value,
    operation: tool.value === 'eraser' ? 'destination-out' : 'source-over',
    points: [pos.x, pos.y]
  }))
  layerRef.value.getNode().add(newLine);
  currentLine.value = newLine;
};

const handleMouseUp = (e) => {
  isDrawing.value = false;
  currentLine.value = null;
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
  ws.value.send(JSON.stringify({
    type: "draw",
    points: [point.x, point.y]
  }));
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
    const saved_json = response.canva;
    if (saved_json) {
      const parsed = JSON.parse(saved_json);
      const layer = layerRef.value.getNode(); //
      layer.destroyChildren();
      parsed.children[0].children.forEach(shapeJson => {
        const shape = Konva.Node.create(shapeJson);
        layer.add(shape);
      });
      layer.draw();
    }
  }catch(e){
    console.error(e)
  }
}

onMounted(async()=>{
  await nextTick(); 
  load()
  if(await check_save('load')){
    setTimeout(()=> get_details_and_load(),100)
  }
  await check_owner()
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
  const onResize = () => {
    windowWidth.value = window.innerWidth;
  };
  window.addEventListener('resize', onResize); 
  //onBeforeUnmount(() => window.removeEventListener('resize', onResize));
})
setInterval(()=>autosave(),60000)
onBeforeUnmount(()=>{
  if(ws.value){
    ws.value.close()
  }
})

</script>

<style scoped>
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform:translateY(-20px);
}

/* The "leave" state, when the modal is about to disappear */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.4s ease-in-out, transform 0.4s ease-in-out;
}

/* The "active" state, when the modal is fully visible and in its final position */
.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform:translateY(0);
}

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

#inv:hover,#save_btn:hover{
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