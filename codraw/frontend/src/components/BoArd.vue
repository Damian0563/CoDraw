<template>
  <div
    style="
      position: relative;
      width: 100vw;
      height: 100vh;
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
        <button @click="showPopup = false"
            style="position: absolute; top: 12px; right: 12px; background: transparent; border: none; color: #ccc; font-size: 20px; cursor: pointer;">
          ✕
        </button>
        <p>{{message}}</p>
        <button v-if="message!=='Are you sure you would like to clear the board? This action is irreversible.'" @click="showPopup = false" id="close_form"
            style="margin-top: 20px; background: #4f8cff; color: #fff; border: none; border-radius: 8px; padding: 8px 20px; font-size: 1rem; cursor: pointer;">
          Close
        </button>
        <button v-if="message==='Are you sure you would like to clear the board? This action is irreversible.'"
          @click="clearDefinetely()" id="confirm_clear"
          style="margin-top: 20px;background: green; color: #fff; border: none; border-radius: 8px; padding: 8px 20px; font-size: 1rem; cursor: pointer;">
          Confirm
        </button>
      </div>
      </div>
    </Transition>
    <div
      id="toolbar"
			:class="{'vertical-toolbar':windowWidth<800}"
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
				gap: 10px;
				z-index: 10;
      "
    >
      <font-awesome-icon :icon="['fas','undo']" class="feature-icon" @click="undo()"></font-awesome-icon>
      <font-awesome-icon :icon="['fas','redo']" class="feature-icon" @click="redo()"></font-awesome-icon>
      <button @click="motiv=!motiv" style="border-radius: 50%;padding: 1rem;border-color: #f68608;border-width: 5px;"
      :style="{ backgroundColor: motiv ? '#ffffff' : '#000000' }"
      ></button>
      <text style="color: white;">Brush Color</text>
      <input type="color" v-model="color">
			<font-awesome-icon :icon="['fas','hand']" @click="togglePane('$event')" class="feature-icon" :style="{color: paneToggler?'#0d6efd':'orange'}"></font-awesome-icon>
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
      <label style="color: #fff; font-size: 1rem; ">
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
        "
      >
      <span style="color: #fff; min-width: 32px; text-align: center;">{{ width_slider }}</span>
      <button
        id="save_btn"
        v-if="(admin || visitor) && MODE==='default'"
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
      v-if="admin"
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
        v-if="visitor && MODE!=='demo'"
        id="bookmark-btn"
        @click="toggleBookmark"
        class="mb-2"
        style="
        background: #4f8cff;
        color:#fff ;
        border: none;
        border-radius: 10px;
        padding: 10px 18px;
        font-size: 0.95rem;
        font-weight: 500;
        cursor: pointer;
        transition: ease-in-out 0.6s;
        height: 40px;
        "
				:style="{width:show_text?'200px':'unset'}"
      >
        <img :src="bookmarkIcon" decoding="async" loading="lazy" alt="Bookmark" style="width: 18px; height: 18px;" />
        <span v-if="show_text">{{ isBookmarked ? "Bookmarked" : "Bookmark" }}</span>
      </button>
      <button
        id="inv"
				v-if="MODE==='default'"
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
          height: 40px;
        "
				:style="{width:show_text?'200px':'unset'}"
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
          <div style="position: relative;">
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
                width: 100%;
                box-sizing: border-box;
              "
            />
            <span
              style="
                position: absolute;
                right: 10px;
                bottom: 6px;
                font-size: 0.75rem;
                color: #aaa;
                pointer-events: none;
              "
            >{{ (title && title.length) || 0 }}</span>
          </div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px;">
          <label class="align-self-start">Description</label>
            <div style="position: relative;">
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
              resize: none;
              outline: none;
              transition: border 0.2s;
              width: 100%;
              box-sizing: border-box;
              "
            ></textarea>
            <span
              style="
              position: absolute;
              right: 10px;
              bottom: 6px;
              font-size: 0.75rem;
              color: #aaa;
              pointer-events: none;
              "
            >{{ (description && description.length) || 0 }}</span>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
          <label style="flex-shrink: 0;">Private</label>
          <label class="switch">
            <input
              v-model="type"
              type="checkbox"
              :true-value="'Private'"
              :false-value="'Public'"
            />
            <span class="slider"></span>
          </label>
        </div>
        <button
          id="save_def"
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
            transition: 0.5s ease-out;
          "
          class="save"
        >
          Save Details
        </button>
      </div>
    </Transition>
    <div id="zoom">
      <label style="font-size: larger; cursor: pointer;width:2rem" @click="changeZoom('up')" >+</label>
      <img :src="zoom_ico" decoding="async" loading="lazy" alt="zoom" class="img-fluid" style="width:1.2rem;height: 1.2rem;">
      <input v-model="zoom" style="width: 60px; text-align: center;border-style: none;" disabled>
      <label style="font-size: larger; cursor: pointer;width:2rem" @click="changeZoom('down')">-</label>
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
import url from '@/assets/email.webp'
import zoom_ico from '@/assets/zoom.webp'
import { v4 as uuidv4 } from 'uuid'
import { get_cookie } from '@/common';
import {BASE_URL} from '../common.js'
import {WS_URL} from '../common.js'
import {VueSpinnerTail} from 'vue3-spinners'
import bookmarkIcon from '@/assets/star.webp'
const loading=ref(false)
const csrf = get_cookie('csrftoken');
import { onMounted, ref, onBeforeUnmount, computed, onUnmounted} from 'vue';
const currentLine = ref(null)
const MODE=new URL(window.location.href).pathname.split('/')[1]=='demo'?'demo':'default'
let drawFrameId = null
let lastWsSendTime = 0
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
const zoom=computed(()=>{return `${(zooming.value*100).toFixed(0)}%`})
const zooming= ref(1)
const lastPos = ref(null);
const imageRef = ref(null);
const layerRef = ref(null);
const isPanning = ref(false);
const motiv=ref(false)
const visitor=ref(true)
const stroke_history=ref([])
const history_index=ref(0)
const isBookmarked=ref(false);
const paneToggler=ref(false)
const room=ref(new URL(window.location.href).pathname.split('/')[3])

const check_visitor=async()=>{
	if(MODE==='demo'){
		visitor.value=true;
		return;
	}
	try{
		const data=await fetch(`${BASE_URL}/status`,{
			method:"GET",
			headers:{"X-CSRFToken":csrf},
			credentials:"include"
		})
		let response=await data.json()
		if(response.status===200 && response.user) visitor.value=true;
			else visitor.value=false;
	}catch(e){
		console.error(e)
	}
}

const togglePane=()=>{
	paneToggler.value = !paneToggler.value;
  const stage = stageRef.value.getNode();
  if (paneToggler.value) {
    isPanning.value = true;
    isDrawing.value = false;
    stage.draggable(true);
		stage.container().style.cursor = 'grab';
  } else {
    isPanning.value = false;
    stage.draggable(false);
		stage.container().style.cursor = 'default';
  }
}

const toggleBookmark=async()=>{
  const me=new URL(window.location.href).pathname.split("/")[2]
  try{
    const data=await fetch(`${BASE_URL}/bookmark/${room.value}`,{
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        "X-CSRFToken":csrf
      },
      credentials:"include",
      body:JSON.stringify({
        "user":me,
        "status":isBookmarked.value
      })
    })
    const response=await data.json()
    if(response.status===200 && response.bookmarked){
      isBookmarked.value=true;
    }else{
      isBookmarked.value=false;
    }
  }catch(e){
    isBookmarked.value=false;
  }
}

const check_book_mark=async()=>{
  const me=new URL(window.location.href).pathname.split("/")[2]
  try{
    const data=await fetch(`${BASE_URL}/is_bookmarked/${room.value}`,{
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        "X-CSRFToken":csrf
      },
      body:JSON.stringify({
        "user":me
      }),
      credentials:"include"
    })
    const response=await data.json();
    if(response.status===200 && response.bookmarked) isBookmarked.value=true;
    else isBookmarked.value=false;
  }catch(e){
    isBookmarked.value=false;
    console.error(e)
  }
}
const show_text = computed(() => windowWidth.value > 1300);
const stageConfig = {
  width: 2*document.documentElement.clientWidth,
  height: 2*document.documentElement.clientHeight,
  draggable: false
};

const ws=ref(null)
if(MODE==='default'){
	const rawUrl=WS_URL
	const cleanBase = rawUrl.endsWith('/') ? rawUrl.slice(0, -1) : rawUrl;
	const finalUrl = `${cleanBase}/${room.value}/`;
	ws.value = new WebSocket(finalUrl)
	ws.value.onopen = function() {
		ws.value.send(JSON.stringify({
			type: "sync-request",
			room: room.value
		}))
	}
	ws.value.onmessage = async(event) => {
		const data = JSON.parse(event.data);
		if (!data || !data.type) return;
		const layer = layerRef.value.getNode();
		if(data.type === "start") {
			const newLine = new Konva.Line({
				stroke: data.stroke,
				strokeWidth: data.width,
				globalCompositeOperation: data.operation,
				points: data.points,
				lineCap: "round",
				lineJoin: "round",
				tension:0.3
			});
			newLine._remote = true;
			layer.add(newLine);
			currentLine.value = newLine;
		} else if (data.type === "draw" && currentLine.value?._remote) {
			const points = currentLine.value.points();
			points.push(...data.points);
			currentLine.value.points(points);
			layer.batchDraw();
		}else if(data.type==="bg" && data.bg){
			background.value=data.bg
			motiv.value = data.bg === "#ffffff"
		}else if(data.type=="img"){
			const img = new window.Image();
			img.src = data.src;
			img.onload = () => {
				const konvaImg = new Konva.Image({
					id: data.id,
					image: img,
					x: data.x,
					y: data.y,
					width: data.width,
					height: data.height,
					draggable: false,
				});
				applyCrop(konvaImg);
				layer.add(konvaImg);
				layer.batchDraw();
			};
			img.onerror = () => console.error("Remote image failed to load", data.id);
		}else if(data.type==="history_update" && data.history){
			stroke_history.value=data.history
			history_index.value=data.index
		}else if(data.type==="undo") await undo();
		else if(data.type==="redo") redo();
		else if(data.type==="sync-request"){
			autosave()
			ws.value.send(JSON.stringify({
				type: "sync-response",
				context: localStorage.getItem(room.value)
			}))
		}else if(data.type==="sync-response"){
			if (!layerRef.value) {
				await nextTick();
			}
			if (data.context && layerRef.value) {
				await applyStateToLayer(data.context);
			}
		}
	};
}

const handleContextMenu = (e) => {
  e.evt.preventDefault();
};
const canvas = document.createElement('canvas');
canvas.width = stageConfig.width;
canvas.height = stageConfig.height;
const isSaved=ref(false)

const context = canvas.getContext('2d');
context.strokeStyle = color.value;
context.fillStyle=background.value
context.lineJoin = 'round';
context.lineWidth = Number(width_slider.value);
context.lineCap = 'round';
context.lineJoin = 'round';

watch(color, (newColor) => {
  context.strokeStyle = newColor;
});

function changeZoom(mode){
  const stage = stageRef.value.getNode();
  const scaleBy = 1.25;
  const oldScale = stage.scaleX();
  const direction = mode==="up"? 1 : -1;
  if(oldScale===1 && direction===-1) return;
  const newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy;
  zooming.value=newScale
  stage.scale({ x: newScale, y: newScale });
  stage.batchDraw();
}

const check_owner=async()=>{
  try{
    const parts = new URL(window.location.href).pathname.split('/');
    const owner = parts[2]; // 'user_id'
    const data=await fetch(`${BASE_URL}/codraw/check_owner`,{
      method:"POST",
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrf
      },
      credentials:"include",
      body:JSON.stringify({
        "owner":owner,
        "room":room.value
      })
    })
    const response=await data.json()
    if(response.status===200){
      admin.value=true
    }
  }catch(e){
    admin.value=false
    console.error(e)
  }
}

const copyInvitationLink = async () => {
  try {
		if(isSaved.value){
			await check_save('save')
		}
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

const load = async() => {
	let data=null;
	if(MODE==='demo'){
		data = localStorage.getItem("demo");
	}else{
		const parts = new URL(window.location.href).pathname.split('/')[3]
		data = localStorage.getItem(parts);
	}
  if (data) {
    await applyStateToLayer(data);
	}
};
const save_definetely = async()=>{
  try{
    loading.value=true
    if(!title.value){
      showPopup.value=true
      message.value="Please provide a title for your board."
    }
    if(title.value.length>66){
      showPopup.value=true
      message.value="The title length is to large, must be at most 60 characters."
    }
    if(description.value && description.value.length>170){
      showPopup.value=true
      message.value="The description length is to large, must be at most 100 characters."
    }
    const data=await fetch(`${BASE_URL}/codraw/save_new`,{
      method:"POST",
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf},
      body:JSON.stringify({
        "project":room.value,
        "title":title.value,
        "description":description.value,
        "type":type.value,
        "bg":background.value,
				"preview":getPreviewPicture(),
				"payload":JSON.stringify([{
					id:Date.now(),
					image:stageRef.value.getStage().toJSON()
				}])
      }),
      credentials:"include"
    })
    const response=await data.json()
    let flag=true
    isVisible.value=false
    if(response.status===200){
      flag=false
    }
    await new Promise(resolve => setTimeout(() => { loading.value = false; resolve(); }, 2000));
    if(!flag){
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


const MAX_HISTORY = 30;
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
	if(MODE==='default'){
		ws.value.send(JSON.stringify({
			type: "history_update",
			history: stroke_history.value,
			index: history_index.value
		}));
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

const checkSaveStatus=async()=>{
	const owner=new URL(window.location.href).pathname.split('/')[2]
	try{
		const data=await fetch(`${BASE_URL}/codraw/check_saved`,{
			method:"POST",
			headers:{
				'Content-Type':'application/json',
			},
			body:JSON.stringify({
				"project":room.value,
				"owner":owner
			})
		})
		const response=await data.json()
		isSaved.value=response.saved
	}catch(e){
		console.error(e)
		isSaved.value=false
	}
}

const getPreviewPicture = ()=>{
	const stage = stageRef.value.getStage();
  const layer = layerRef.value.getNode();
  const bgRect = new Konva.Rect({
    x: -stage.x() / stage.scaleX(),
    y: -stage.y() / stage.scaleY(),
    width: stage.width() / stage.scaleX(),
    height: stage.height() / stage.scaleY(),
    fill: background.value,
    listening: false,
  });
  layer.add(bgRect);
  bgRect.moveToBottom();
  const dataURL = stage.toDataURL({ pixelRatio: 2 });
  bgRect.destroy();
  layer.batchDraw();
	// const link = document.createElement('a');
	// link.download = 'my-drawing.png';
	// link.href = dataURL;
	// document.body.appendChild(link);
	// link.click();
	// document.body.removeChild(link);
  return dataURL;
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
			if(MODE==='default'){
				ws.value.send(JSON.stringify({
					type:"img",
					id: konvaImg.id(),
					src: e.target.result,
					x: konvaImg.x(),
					y: konvaImg.y(),
					width: konvaImg.width(),
					height: konvaImg.height(),
				}))
			}
      addToHistory()
  }
  reader.onloadstart= function() {
    console.error('Starting');
  };
  reader.onerror = function(event) {
    console.error('FileReader error:', event.target.error);
  };
  }
  reader.readAsDataURL(file)
}


const check_save = async (mode) => {
  try{
    loading.value=true
    if(mode==='save'){
      const data=await fetch(`${BASE_URL}/codraw/save_project`,{
        method:"POST",
        headers:{'Content-Type':'application/json','X-CSRFToken':csrf},
        body:JSON.stringify({
          "project":room.value,
          "payload": JSON.stringify(stageRef.value.getStage().toJSON()),
          "bg":background.value,
					"preview":getPreviewPicture()
        }),
        credentials:"include"
      })
      const response=await data.json()
      let flag=true;
      if(response.status===200){
        flag=false
      }
      await new Promise(resolve => setTimeout(() => { loading.value = false; resolve(); }, 2000));
      if(!flag){
        autosave()
        showPopup.value=true
        message.value="Board was successfully quick saved."
      }else isVisible.value=true
    }else if(mode==='load'){
      const data=await fetch(`${BASE_URL}/codraw/save_project`,{
        method:"POST",
        headers:{
          'Content-Type':'application/json',
        },
        body:JSON.stringify({
          "project":room.value,
        }),
      })
      const response=await data.json()
      if(response.status===200){
        return true
      }
			const autosaved=localStorage.getItem(room.value)
			if(autosaved){
				await applyStateToLayer(autosaved)
			}
      return false
    }
  }catch(e){
    console.error(e)
  }
}

function leave(){
	const parts = new URL(window.location.href).pathname.split('/')[3];
  localStorage.removeItem(parts)
  if(admin.value){
    window.location.href='/codraw'
  }else{
    window.location.href='/'
  }
}

function clearDefinetely(){
  showPopup.value=false
  message.value=""
  loading.value=true
	const parts = new URL(window.location.href).pathname.split('/')[3]
  localStorage.removeItem(parts)
  const layer=layerRef.value.getNode();
  layer.destroyChildren();
  layer.batchDraw();
  loading.value=false
}

function clear_all(){
  if(admin.value){
    showPopup.value=true;
    message.value="Are you sure you would like to clear the board? This action is irreversible.";
  }else{
    showPopup.value=true;
    message.value="You don't have neccessary permissions to clear the board."
  }
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
  const dataUrl = stage.toJSON();
  list.value = [{
    id: Date.now(),
    image: dataUrl
  }];
	if(MODE==='demo'){
		localStorage.setItem("demo", JSON.stringify(list.value));
	}else{
		const parts = new URL(window.location.href).pathname.split('/')[3]
		localStorage.setItem(parts, JSON.stringify(list.value));
	}
};

const imageConfig = {
  image: canvas,
  x: 0,
  y: 0,
  width: canvas.width,
  height: canvas.height
};
let lastCenter = null;
let lastDist = 0;
const handleMouseDown = (e) => {
	if (!e.evt.touches || e.evt.touches.length==1){
		const stage = e.target.getStage();
		if (e.evt.button === 2 || paneToggler.value) {
			isPanning.value = true;
			stage.draggable(true);
			stage.startDrag();
			lastPos.value = stage.getPointerPosition();
			return;
		}
		isDrawing.value = true;
		const pos = getRelativePointerPosition(stage);
		const newLine = new Konva.Line({
			stroke: tool.value === 'eraser' ? 'rgba(0,0,0,1)' : color.value,
			strokeWidth: Number(width_slider.value),
			globalCompositeOperation: tool.value === 'eraser' ? 'destination-out' : 'source-over',
			points: [pos.x, pos.y],
			lineCap: 'round',
			lineJoin: 'round',
			tension:0.3
		});
		if(MODE==='default'){
			ws.value.send(JSON.stringify({
				type: "start",
				stroke: color.value,
				width: Number(width_slider.value),
				operation: tool.value === 'eraser' ? 'destination-out' : 'source-over',
				points: [pos.x, pos.y]
			}))
		}
		layerRef.value.getNode().add(newLine);
		currentLine.value = newLine;
	}else if(e.evt.touches && e.evt.touches.length==2){
		if (e.evt.cancelable) {
			e.evt.preventDefault();
		}
		isDrawing.value = false;
    currentLine.value = null;
		const touch1 = e.evt.touches[0];
    const touch2 = e.evt.touches[1];
    lastDist = Math.sqrt(
      Math.pow(touch2.clientX - touch1.clientX, 2) +
      Math.pow(touch2.clientY - touch1.clientY, 2)
    );
    lastCenter = {
      x: (touch1.clientX + touch2.clientX) / 2,
      y: (touch1.clientY + touch2.clientY) / 2,
    };
	}
};

const handleMouseUp = (e) => {
  isDrawing.value = false;
  currentLine.value = null;
  lastDist = 0;
  lastCenter = null;
  addToHistory()
  if (isPanning.value) {
    const stage = e.target.getStage();
    stage.draggable(false);
    isPanning.value = false;
  }
  if (drawFrameId !== null) {
    cancelAnimationFrame(drawFrameId);
    drawFrameId = null;
    layerRef.value.getNode().batchDraw();
  }
};

const handleMouseMove = (e) => {
	if(!e.evt.touches || e.evt.touches.length==1){
		if (!isDrawing.value || !currentLine.value) return;
		const stage = e.target.getStage();
		const point = getRelativePointerPosition(stage);
		const points = currentLine.value.points();
		points.push(point.x, point.y);
		currentLine.value.points(points);
		const now = Date.now();
		if (now - lastWsSendTime >= 16 && MODE==='default') {
			lastWsSendTime = now;
			ws.value.send(JSON.stringify({
				type: "draw",
				points: [point.x, point.y]
			}));
		}
		if (drawFrameId === null) {
			drawFrameId = requestAnimationFrame(() => {
				layerRef.value.getNode().batchDraw();
				drawFrameId = null;
			});
		}
	}else if(e.evt.touches && e.evt.touches.length==2 && lastCenter){
		if (e.evt.cancelable) {
       e.evt.preventDefault();
    }
		const stage = stageRef.value.getNode();
    const touch1 = e.evt.touches[0];
    const touch2 = e.evt.touches[1];
    const dist = Math.sqrt(
      Math.pow(touch2.clientX - touch1.clientX, 2) +
      Math.pow(touch2.clientY - touch1.clientY, 2)
    );
    const newCenter = {
      x: (touch1.clientX + touch2.clientX) / 2,
      y: (touch1.clientY + touch2.clientY) / 2,
    };
    const pointTo = {
      x: (newCenter.x - stage.x()) / stage.scaleX(),
      y: (newCenter.y - stage.y()) / stage.scaleX(),
    };
    const scaleBy = dist / lastDist;
    const newScale = stage.scaleX() * scaleBy;
		if(newScale>0.05 && newScale<5){
			stage.scale({ x: newScale, y: newScale });
			const newPos = {
				x: newCenter.x - pointTo.x * newScale,
				y: newCenter.y - pointTo.y * newScale,
			};
			stage.position(newPos);
			stage.batchDraw();
		}
    lastDist = dist;
    lastCenter = newCenter;
  }
};

const handleStageResize = () => {
	windowWidth.value = window.innerWidth;
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
};

const applyStateToLayer = async (data) => {
  if (!data) return;
  const layer = layerRef.value?.getNode();
  if (!layer) {
    await nextTick();
    return applyStateToLayer(data);
  }
	const parsed = typeof data === 'string' ? JSON.parse(data) : data;
	let stageData = null;
	if (Array.isArray(parsed) && parsed[0]?.image) {
		stageData = typeof parsed[0].image === 'string' ? JSON.parse(parsed[0].image) : parsed[0].image;
	} else if (parsed.image) {
		stageData = typeof parsed.image === 'string' ? JSON.parse(parsed.image) : parsed.image;
	} else if (parsed.className === 'Stage' || parsed.children) {
		stageData = parsed;
	}
	if (!stageData) {
		return;
	}
	layer.destroyChildren();
	const savedChildren = stageData.children?.[0]?.children || [];
	const imagePromises = savedChildren.map(shapeJson => {
		if (shapeJson.className === "Image" && shapeJson.attrs.src) {
			return new Promise((resolve) => {
				const img = new window.Image();
				img.crossOrigin = "Anonymous";
				img.onload = () => {
					shapeJson.attrs.image = img;
					resolve();
				};
				img.onerror = () => {
					console.error("Failed to load image:", shapeJson.attrs.src);
					resolve();
				};
				img.src = shapeJson.attrs.src;
			});
		}
		return Promise.resolve();
	});
	await Promise.all(imagePromises);
	savedChildren.forEach(shapeJson => {
		const shape = Konva.Node.create(shapeJson);
		layer.add(shape);
		if (shape.className === 'Image') applyCrop(shape);
	});
	layer.batchDraw();
};

const get_details_and_load = async()=>{
  try{

		if(MODE==='default'){
			const data=await fetch(`${BASE_URL}/codraw/get_details`,{
				method:"POST",
				headers:{
					'Content-Type':'application/json',
				},
				body:JSON.stringify({
					"project":room.value
				})
			})
			const response=await data.json()
			const saved_json = response.canva;
			const bg = response.bg;
			const last_access=response.last
			if(bg){
				background.value=bg
				motiv.value = bg === "#ffffff"
			}
			const localData = localStorage.getItem(room.value);
			if (localData) {
				const parsedLocal = JSON.parse(localData);
				if (parsedLocal && parsedLocal[0] && parsedLocal[0].id > last_access) {
					await load();
					return;
				}
			}
			if(saved_json){
				await applyStateToLayer(saved_json)
			}
		}else if(MODE==='demo'){
			const localData = localStorage.getItem(room.value);
			if (localData) {
				const parsedLocal = JSON.parse(localData);
				if (parsedLocal && parsedLocal[0]) {
					await load();
					return;
				}
			}
		}
  }catch(e){
    console.error(e)
  }
}

const keyhandler=(event)=>{
  if (event.ctrlKey && event.key === 'z') {
    undo()
    if(MODE==='default'){
			ws.value.send(JSON.stringify({
				type: "undo"
			}))
		}
  }
  else if (event.ctrlKey && event.key === 'y') {
    redo()
		if(MODE==='default'){
			ws.value.send(JSON.stringify({
				type: "redo"
			}))
		}
  }
}

let autosaveInterval = null;
onMounted(async()=>{
  loading.value=true
  await nextTick();
  if(await check_save('load')){
    setTimeout(()=> get_details_and_load(),100)
  }
	if(MODE==='demo'){
		visitor.value=true;
	}else{
		await Promise.all([check_owner(),check_visitor(),checkSaveStatus()])
	}

  if(visitor.value && MODE!=='demo'){
    await check_book_mark();
  }
	autosaveInterval=setInterval(()=>autosave(),60000)
  window.addEventListener('keyup',keyhandler)
  const stage=stageRef.value.getNode();
  const scaleBy=1.25;
  stage.on('wheel', (e) => {
    e.evt.preventDefault();
    const oldScale=stage.scaleX();
    const pointer=stage.getPointerPosition();

    const mousePointTo = {
      x: (pointer.x - stage.x()) / oldScale,
      y: (pointer.y - stage.y()) / oldScale,
    };

    const direction = e.evt.deltaY > 0 ? 1 : -1;
    if(oldScale===1 && direction===-1) return;
    const newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy;
    zooming.value=newScale
    stage.scale({ x: newScale, y: newScale });
    const newPos = {
      x: pointer.x - mousePointTo.x * newScale,
      y: pointer.y - mousePointTo.y * newScale,
    };
    stage.position(newPos);
    stage.batchDraw();
  })
  window.addEventListener('resize', handleStageResize);
  window.addEventListener('paste', handlePaste)
  const preview = document.createElement('div');
  preview.id = 'preview';
  preview.style.position = 'absolute';
  preview.style.bottom = '5px';
  preview.style.left = '5px';
  preview.style.border = '5px solid #ffc107';
  preview.style.borderRadius="5%"
  preview.style.backgroundColor = 'lightgrey';
  document.body.appendChild(preview);
  const previewStage = new Konva.Stage({
    container: 'preview',
    width: window.innerWidth/8,
    height: window.innerHeight/8,
    scaleX: 1/32,
    scaleY: 1/32,
  });
  let layer=layerRef.value.getNode()
  let previewLayer = new Konva.Layer();
  const previewBg = new Konva.Rect({
    x: 0,
    y: 0,
    width: previewStage.width()*32,
    height: previewStage.height()*32,
    fill: background.value,
    listening: false,
  });
  previewStage.add(previewLayer);
  previewLayer.add(previewBg)
  watch(motiv,()=>{
    background.value = motiv.value ? "#ffffff" : "#000000"
    color.value= motiv.value ? "#000000":"#ffffff"
    previewBg.fill(background.value);
    previewLayer.batchDraw();
    if(MODE==='default' && ws.value.readyState===WebSocket.OPEN){
      ws.value.send(JSON.stringify({
        type: "bg",
        bg: background.value
      }))
    }
  },{immediate:true})
  function syncPreview() {
    const parsed = JSON.parse(stageRef.value.getStage().toJSON());
    previewLayer.destroyChildren();
    previewLayer.add(previewBg);
    parsed.children[0].children.forEach(shapeJson => {
      const shape = Konva.Node.create(shapeJson);
      previewLayer.add(shape);
    });
    previewLayer.draw();
  }
  loading.value=false;
  layer.on('add destroy change',syncPreview)
  syncPreview()
})
onBeforeUnmount(()=>{
  if(ws.value){
    ws.value.close()
  }
  loading.value=true
})
onUnmounted(()=>{
	clearInterval(autosaveInterval)
  window.removeEventListener('paste',handlePaste)
  window.removeEventListener("keyup",keyhandler)
  window.removeEventListener("resize",handleStageResize)
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
	#save_btn,#clearall,#exit{
		width:50px !important;
		font-size: 0.5rem !important;
		padding: 10px 10px !important;
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
	touch-action:none;
	-webkit-user-select:none;
	user-select:none;
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

@media(max-width:950px){
  #inv_div{
    top:140px !important;
    position: fixed !important;
  }
}

@media(max-width:800px){
	#inv_div{
		top:10px !important;
	}
}
#zoom{
  position: fixed;
  right:10px;
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
