<template>
	<div style="
      position: relative;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
    ">
		<div v-if="loading" class="spinner-overlay">
			<VueSpinnerTail size="60" color="orange" />
		</div>
		<Transition name="fade-slide">
			<div v-if="showPopup"
				style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.35); z-index: 100; display: flex; align-items: center; justify-content: center;">
				<div
					style="background: #23272f; color: #fff; padding: 32px 40px; border-radius: 16px; min-width: 320px; box-shadow: 0 8px 32px rgba(0,0,0,0.25); position: relative;">
					<button @click="showPopup = false"
						style="position: absolute; top: 12px; right: 12px; background: transparent; border: none; color: #ccc; font-size: 20px; cursor: pointer;">
						✕
					</button>
					<p>{{ message }}</p>
					<button v-if="message !== 'Are you sure you would like to clear the board? This action is irreversible.'"
						@click="showPopup = false" id="close_form"
						style="margin-top: 20px; background: #4f8cff; color: #fff; border: none; border-radius: 8px; padding: 8px 20px; font-size: 1rem; cursor: pointer;">
						Close
					</button>
					<button v-if="message === 'Are you sure you would like to clear the board? This action is irreversible.'"
						@click="clearDefinetely(true)" id="confirm_clear"
						style="margin-top: 20px;background: green; color: #fff; border: none; border-radius: 8px; padding: 8px 20px; font-size: 1rem; cursor: pointer;">
						Confirm
					</button>
				</div>
			</div>
		</Transition>
		<div id="toolbar" :class="{ 'vertical-toolbar': windowWidth < 800 }" style="
				position: absolute;
				top: 12px;
				left: 3%;
				background: rgba(30, 30, 30, 0.85);
				border-radius: 16px;
				box-shadow: 0 4px 24px rgba(0,0,0,0.18);
				padding: 20px 32px;
				display: flex;
				align-items: center;
				gap: 10px;
				z-index: 10;
      ">
			<font-awesome-icon :icon="['fas', 'undo']" class="feature-icon" @click="undoWithBroadcast()"></font-awesome-icon>
			<font-awesome-icon :icon="['fas', 'redo']" class="feature-icon" @click="redoWithBroadcast()"></font-awesome-icon>
			<button @click="motiv = !motiv" style="border-radius: 50%;padding: 1rem;border-color: #f68608;border-width: 5px;"
				:style="{ backgroundColor: motiv ? '#ffffff' : '#000000' }"></button>
			<text style="color: white;">Brush Color</text>
			<input type="color" v-model="color">
			<font-awesome-icon :icon="['fas', 'hand']" @click="togglePane('$event')" class="feature-icon"
				:style="{ color: paneToggler ? '#0d6efd' : 'orange' }"></font-awesome-icon>
			<select v-model="tool" style="
          background: #23272f;
          color: #fff;
          border: none;
          border-radius: 8px;
          padding: 8px 16px;
          font-size: 1rem;
          outline: none;
          cursor: pointer;
        ">
				<option value="brush">Brush</option>
				<option value="eraser">Eraser</option>
			</select>
			<input type="range" v-model="width_slider" min="1" max="10" style="
          accent-color: #4f8cff;
          width: 60px;
      ">
			<span style="color: #fff; min-width: 32px; text-align: center;">{{ width_slider }}</span>
			<label aria-label="upload" title="upload image" @click="uploadImage" style="cursor: pointer;">
				<svg xmlns="http://www.w3.org/2000/svg" width="32" height="16" fill="#ffc107" class="bi bi-upload"
					viewBox="0 0 16 16">
					<path
						d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5" />
					<path
						d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708z" />
				</svg>
				<input type="file" id="upload" style="display:none">
			</label>
			<div style="display: flex; align-items: center;cursor: pointer;">
				<img width="24" height="24" loading="async" decoding="lazy" @click="toggleShapeSelector"
					src="https://img.icons8.com/external-tal-revivo-filled-tal-revivo/24/external-assorted-shape-tool-selector-for-designing-application-text-filled-tal-revivo.png"
					alt="external-assorted-shape-tool-selector-for-designing-application-text-filled-tal-revivo" />
			</div>
			<button id="save_btn" v-if="(admin || visitor) && MODE === 'default'" @click="check_save('save')" style="
          background: #4f8cff;
          color: #fff;
          border: none;
          border-radius: 8px;
          padding: 8px 20px;
          font-size: 1rem;
          cursor: pointer;
          transition: ease-in-out 0.6s;
        ">Save</button>
			<button @click="leave()" id="exit" style="
        background: #ff4f4f;
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-size: 1rem;
        cursor: pointer;
        transition: ease-in-out 0.6s;
      ">Exit</button>
			<button id="clearall" v-if="admin || MODE === 'demo'" style="
        background: #f68608;
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-size: 1rem;
        cursor: pointer;
        transition: ease-in-out 0.6s;
      " @click="clear_all()">
				Clear all
			</button>
		</div>
		<Transition name="fade-slide">
			<div v-if="showShapeSelector"
				style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.35); z-index: 100; display: flex; align-items: center; justify-content: center;">
				<div
					style="background: #23272f; color: #fff; padding: 32px 40px; border-radius: 16px; min-width: 320px; box-shadow: 0 8px 32px rgba(0,0,0,0.25); position: relative;">
					<button @click="showShapeSelector = false"
						style="position: absolute; top: 12px; right: 12px; background: transparent; border: none; color: white; font-size: 20px; cursor: pointer;">
						✕
					</button>
					<p>Select a Shape</p>
					<div class="row">
						<div class="col-3">
							<font-awesome-icon :icon="['fas', 'text-height']" class="feature-icon" alt="text" ara-label="text"
								@click="createShape('text')"></font-awesome-icon>
						</div>
						<div class="col-3">
							<font-awesome-icon :icon="['fas', 'arrow-up-long']" class="feature-icon" alt="arrow" ara-label="arrow"
								@click="createShape('arrow')"></font-awesome-icon>
						</div>
						<div class="col-3">
							<font-awesome-icon :icon="['fas', 'circle']" class="feature-icon" alt="circle" ara-label="circle"
								@click="createShape('circle')"></font-awesome-icon>
						</div>
						<div class="col-3">
							<font-awesome-icon :icon="['fas', 'square']" class="feature-icon" alt="square" ara-label="square"
								@click="createShape('square')"></font-awesome-icon>
						</div>
					</div>
				</div>
			</div>
		</Transition>
		<div id="inv_div" style="position: absolute; top: 12px; right: 1rem; z-index: 10;">
			<button v-if="visitor && MODE !== 'demo'" id="bookmark-btn" @click="toggleBookmark" class="mb-2" style="
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
        " :style="{ width: show_text ? '200px' : 'unset' }">
				<img :src="bookmarkIcon" decoding="async" loading="lazy" alt="Bookmark" style="width: 18px; height: 18px;" />
				<span v-if="show_text">{{ isBookmarked ? "Bookmarked" : "Bookmark" }}</span>
			</button>
			<button id="inv" @click="copyInvitationLink" style="
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
        " :style="{ width: show_text ? '200px' : 'unset' }">
				<img :src="url" alt="Copy" style="width: 18px; height: 18px;" />
				<span v-if="show_text">Copy invitation link</span>
			</button>
		</div>
		<Transition name="fade-slide">
			<div v-if="isVisible" style="
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
        ">
				<button @click="isVisible = false" style="
            position: absolute;
            top: 12px;
            right: 12px;
            background: transparent;
            border: none;
            color: #ccc;
            font-size: 20px;
            cursor: pointer;
            transition: color 0.2s;
          ">
					✕
				</button>
				<div style="display: flex; flex-direction: column; gap: 6px;">
					<label class="align-self-start">Title</label>
					<div style="position: relative;">
						<input v-model="title" type="text" placeholder="Enter title" style="
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
              " />
						<span style="
                position: absolute;
                right: 10px;
                bottom: 6px;
                font-size: 0.75rem;
                color: #aaa;
                pointer-events: none;
              ">{{ (title && title.length) || 0 }}</span>
					</div>
				</div>
				<div style="display: flex; flex-direction: column; gap: 6px;">
					<label class="align-self-start">Description</label>
					<div style="position: relative;">
						<textarea v-model="description" rows="3" placeholder="Enter description" style="
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
              "></textarea>
						<span style="
              position: absolute;
              right: 10px;
              bottom: 6px;
              font-size: 0.75rem;
              color: #aaa;
              pointer-events: none;
              ">{{ (description && description.length) || 0 }}</span>
					</div>
				</div>
				<div style="display: flex; align-items: center; gap: 10px;">
					<label style="flex-shrink: 0;">Private</label>
					<label class="switch">
						<input v-model="type" type="checkbox" :true-value="'Private'" :false-value="'Public'" />
						<span class="slider"></span>
					</label>
				</div>
				<button id="save_def" @click="save_definetely()" style="
            background: #4f8cff;
            color: #fff;
            border: none;
            border-radius: 12px;
            padding: 12px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: 0.5s ease-out;
          " class="save">
					Save Details
				</button>
			</div>
		</Transition>
		<div id="zoom">
			<label style="font-size: small; cursor: pointer;width:1.5rem" @click="changeZoom('up')">+</label>
			<img :src="zoom_ico" decoding="async" loading="lazy" alt="zoom" class="img-fluid"
				style="width:1rem;height: 1rem;">
			<input v-model="zoom" style="width: 60px; text-align: center;border-style: none;font-size: 0.7rem;" disabled>
			<label style="font-size:small; cursor: pointer;width:1.5rem" @click="changeZoom('down')">-</label>
		</div>
		<div class="board-wrapper" :style="{ backgroundColor: motiv ? '#ffffff' : '#000000' }">
			<v-stage ref="stageRef" :config="stageConfig" @mousedown="handleMouseDown" @mousemove="handleMouseMove"
				@mouseup="handleMouseUp" @wheel="handleMouseWheel" @touchstart="handleMouseDown" @touchmove="handleMouseMove"
				@touchend="handleMouseUp" @contextmenu="handleContextMenu" @click="(e) => handleStageClick(e)"
				style="overflow-x: hidden;overflow-y: hidden;border: none !important;">
				<v-layer ref="layerRef">
					<v-image ref="imageRef" :config="imageConfig" />
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
import { BASE_URL } from '../common.js'
import { WS_URL } from '../common.js'
import { VueSpinnerTail } from 'vue3-spinners'
import bookmarkIcon from '@/assets/star.webp'
const loading = ref(false)
const csrf = get_cookie('csrftoken');
import { onMounted, ref, onBeforeUnmount, computed, onUnmounted } from 'vue';
const currentLine = ref(null)
const MODE = new URL(window.location.href).pathname.split('/')[1] == 'demo' ? 'demo' : 'default'
let drawFrameId = null
let lastWsSendTime = 0
import Konva from 'konva';
import { watch } from 'vue';
import { nextTick } from 'vue';
const stageRef = ref(null);
const windowWidth = ref(window.innerWidth);
const admin = ref(false)
const isVisible = ref(false)
const showPopup = ref(false)
const color = ref("#ffffff")
const background = ref("#000000")
const title = ref(null)
const message = ref(null)
const description = ref(null)
const type = ref('Public')
const tool = ref('brush');
const isDrawing = ref(false);
const width_slider = ref(5);
const list = ref([])
const zoom = computed(() => { return `${(zooming.value * 100).toFixed(0)}%` })
const zooming = ref(1)
const lastPos = ref(null);
const imageRef = ref(null);
const layerRef = ref(null);
const isPanning = ref(false);
const motiv = ref(false)
const visitor = ref(true)
const stroke_history = ref([])
const history_index = ref(0)
const isBookmarked = ref(false);
const paneToggler = ref(false)
const showShapeSelector = ref(false)
const texts = []
const room = ref(new URL(window.location.href).pathname.split('/')[3])
if (MODE === 'demo') {
	room.value = new URL(window.location.href).pathname.split('/')[2]
}
const responded = ref(false)
const origin = new URL(window.location.href).searchParams.get('origin')
const transformers = []
const deleteButtons = []

const createShape = (shapeName) => {
	const fill = color.value
	switch (shapeName) {
		case 'text': {
			const maintext = new Konva.Text({
				x: window.innerWidth / 2,
				y: window.innerHeight / 2,
				id: uuidv4(),
				width: 220,
				height: 80,
				fill: fill,
				fontSize: 32,
				fontFamily: 'Caveat',
				text: 'Write text here',
				align: 'center',
				verticalAlign: 'middle',
				draggable: true,
				name: 'mainText',
			});
			texts.push(maintext.id())
			maintext.setAttr('originalFontSize', 32);
			maintext.setAttr('originalWidth', 220);
			maintext.setAttr('originalHeight', 80);
			const previewtext = new Konva.Text({
				x: window.innerWidth / 2,
				y: window.innerHeight / 2,
				id: maintext.id(),
				width: 220,
				height: 80,
				fill: fill,
				fontSize: 32,
				fontFamily: 'Caveat',
				text: 'Write text here',
				align: 'center',
				verticalAlign: 'middle',
				draggable: true,
			});
			previewtext.setAttr('originalFontSize', 32);
			previewtext.setAttr('originalWidth', 220);
			previewtext.setAttr('originalHeight', 80);
			maintext.on('dragmove', () => {
				previewtext.position(maintext.position());
				previewLayer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "text",
						newpos: maintext.position(),
						id: maintext.id(),
					}));
				}
			});
			maintext.on('dragstart', () => {
				stageRef.value.getNode().container().style.cursor = 'grabbing';
			});
			maintext.on('dragend', () => {
				stageRef.value.getNode().container().style.cursor = 'default';
			});
			maintext.on('mouseenter', () => {
				stageRef.value.getNode().container().style.cursor = 'grab';
			});
			maintext.on('mouseleave', () => {
				stageRef.value.getNode().container().style.cursor = 'default';
			});
			maintext.on("dblclick", (e) => {
				e.evt.stopPropagation();
				handleTextClick(e.target);
			})
			previewtext.on('dragmove', () => {
				maintext.position(previewtext.position());
				layerRef.value.getNode().batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "text",
						newpos: previewtext.position(),
						id: previewtext.id(),
					}));
				}
			});
			previewtext.on('dblclick', (e) => {
				e.evt.stopPropagation();
				handleTextClick(maintext);
				document.getElementById("textarea").remove()
			});
			layerRef.value.getNode().add(maintext);
			previewLayer.add(previewtext);
			previewtext.moveToTop();
			maintext.moveToTop();
			if (ws.value && ws.value.readyState === WebSocket.OPEN) {
				ws.value.send(JSON.stringify({
					type: "shape",
					shapeType: "text",
					id: maintext.id(),
					x: maintext.x(),
					y: maintext.y(),
					width: maintext.width(),
					height: maintext.height(),
					fill: maintext.fill(),
					text: maintext.text(),
					fontSize: maintext.fontSize(),
					fontFamily: maintext.fontFamily(),
					align: maintext.align(),
					verticalAlign: maintext.verticalAlign()
				}));
			}
			break;
		}
		case 'arrow': {
			const arrow = new Konva.Arrow({
				x: window.innerWidth / 2,
				y: window.innerHeight / 2,
				id: uuidv4(),
				points: [200, 200, 0, 0],
				stroke: fill,
				strokeWidth: width_slider.value,
				pointerLength: 20,
				pointerWidth: 20,
				fill: fill,
				draggable: true,
			});
			const previewArrow = new Konva.Arrow({
				x: window.innerWidth / 2,
				y: window.innerHeight / 2,
				id: arrow.id(),
				points: [200, 200, 0, 0],
				stroke: fill,
				strokeWidth: width_slider.value,
				pointerLength: 20,
				pointerWidth: 20,
				fill: fill,
				draggable: true,
			});
			arrow.on('dragmove', () => {
				previewArrow.position(arrow.position());
				previewLayer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "arrow",
						newpos: arrow.position(),
						id: arrow.id(),
					}));
				}
			});
			previewArrow.on('dragmove', () => {
				arrow.position(previewArrow.position());
				layerRef.value.getNode().batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "arrow",
						newpos: previewArrow.position(),
						id: previewArrow.id(),
					}));
				}
			});
			layerRef.value.getNode().add(arrow);
			previewLayer.add(previewArrow);
			arrow.moveToTop();
			previewArrow.moveToTop();
			if (ws.value && ws.value.readyState === WebSocket.OPEN) {
				ws.value.send(JSON.stringify({
					type: "shape",
					shapeType: "arrow",
					id: arrow.id(),
					x: arrow.x(),
					y: arrow.y(),
					points: arrow.points(),
					stroke: arrow.stroke(),
					strokeWidth: arrow.strokeWidth(),
					pointerLength: arrow.pointerLength(),
					pointerWidth: arrow.pointerWidth(),
					fill: arrow.fill()
				}));
			}
			break;
		}
		case 'circle': {
			const circle = new Konva.Circle({
				x: window.innerWidth / 2,
				y: window.innerHeight / 2,
				id: uuidv4(),
				radius: 100,
				fill: fill,
				stroke: motiv.value === '#000000' ? 'white' : 'black',
				strokeWidth: width_slider.value,
				draggable: true,
			});
			const previewCircle = new Konva.Circle({
				x: window.innerWidth / 2,
				y: window.innerHeight / 2,
				id: circle.id(),
				radius: 100,
				fill: fill,
				stroke: motiv.value === '#000000' ? 'white' : 'black',
				strokeWidth: width_slider.value,
				draggable: true,
			});
			circle.on('dragmove', () => {
				previewCircle.position(circle.position());
				previewLayer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "circle",
						newpos: circle.position(),
						id: circle.id(),
					}));
				}
			});
			previewCircle.on('dragmove', () => {
				circle.position(previewCircle.position());
				layerRef.value.getNode().batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "circle",
						newpos: previewCircle.position(),
						id: previewCircle.id(),
					}));
				}
			});
			layerRef.value.getNode().add(circle);
			previewLayer.add(previewCircle);
			circle.moveToTop();
			previewCircle.moveToTop();
			if (ws.value && ws.value.readyState === WebSocket.OPEN) {
				ws.value.send(JSON.stringify({
					type: "shape",
					shapeType: "circle",
					id: circle.id(),
					x: circle.x(),
					y: circle.y(),
					radius: circle.radius(),
					fill: circle.fill(),
					stroke: circle.stroke(),
					strokeWidth: circle.strokeWidth()
				}));
			}
			break;
		}
		case 'square': {
			const square = new Konva.Rect({
				x: window.innerWidth / 2,
				y: window.innerHeight / 2,
				id: uuidv4(),
				width: 100,
				height: 100,
				fill: fill,
				stroke: motiv.value === '#000000' ? 'white' : 'black',
				strokeWidth: width_slider.value,
				draggable: true,
			});
			const previewSquare = new Konva.Rect({
				x: window.innerWidth / 2,
				y: window.innerHeight / 2,
				id: square.id(),
				width: 100,
				height: 100,
				fill: fill,
				stroke: motiv.value === '#000000' ? 'white' : 'black',
				strokeWidth: width_slider.value,
				draggable: true,
			});
			square.on('dragmove', () => {
				previewSquare.position(square.position());
				previewLayer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "square",
						newpos: square.position(),
						id: square.id(),
					}));
				}
			});
			previewSquare.on('dragmove', () => {
				square.position(previewSquare.position());
				layerRef.value.getNode().batchDraw();
			});
			layerRef.value.getNode().add(square);
			previewLayer.add(previewSquare);
			square.moveToTop();
			previewSquare.moveToTop();
			if (ws.value && ws.value.readyState === WebSocket.OPEN) {
				ws.value.send(JSON.stringify({
					type: "shape",
					shapeType: "square",
					id: square.id(),
					x: square.x(),
					y: square.y(),
					width: square.width(),
					height: square.height(),
					fill: square.fill(),
					stroke: square.stroke(),
					strokeWidth: square.strokeWidth()
				}));
			}
			break;
		}
		default:
			break;
	}
	showShapeSelector.value = false
}

const handleTextClick = (konvaText) => {
	const layer = layerRef.value.getNode();
	if (!layer || !konvaText) return;
	konvaText.draggable(false);
	const tr = new Konva.Transformer({
		nodes: [konvaText],
		borderStroke: "#ffc107",
		borderDash: [5, 5],
		borderStrokeWidth: 1,
		borderDashOffset: 0,
		borderJoinStyle: "round",
		scalingEnabled: true,
		enabledAnchors: ["top-left", "top-right", "bottom-left", "bottom-right"],
		keepRatio: true,
		keepRatioByExpanding: true,
		rotateEnabled: false,
		boundBoxFunc: (oldBox, newBox) => {
			if (newBox.width < 5 || newBox.height < 5) {
				return oldBox;
			}
			return newBox;
		},
	});
	layer.add(tr);
	layer.batchDraw();
	transformers.push(tr);
	konvaText.hide();
	const stage = stageRef.value.getNode();
	const textPosition = konvaText.getAbsolutePosition();
	const stageBox = stage.container().getBoundingClientRect();
	const scale = stage.scaleX();
	if (document.getElementById("textarea")) document.getElementById("textarea").remove()
	const textarea = document.createElement("textarea");
	textarea.id = "textarea"
	textarea.dataset.textId = konvaText.id();
	document.body.appendChild(textarea);
	textarea.value = konvaText.text();
	textarea.style.position = 'absolute';
	textarea.style.top = (stageBox.top + textPosition.y * scale + 18) + 'px';
	textarea.style.left = (stageBox.left + textPosition.x * scale) + 'px';
	const textScaleX = konvaText.scaleX() || 1;
	const textScaleY = konvaText.scaleY() || 1;
	textarea.style.width = (konvaText.width() * textScaleX * scale) + 'px';
	textarea.style.height = (konvaText.height() * textScaleY * scale) + 'px';
	textarea.style.fontSize = (konvaText.fontSize() * textScaleX * scale) + 'px';
	textarea.style.fontFamily = konvaText.fontFamily();
	textarea.style.color = konvaText.fill();
	textarea.style.backgroundColor = 'transparent';
	textarea.style.border = 'none';
	textarea.style.outline = 'none';
	textarea.style.resize = 'none';
	textarea.style.textAlign = konvaText.align();
	textarea.style.lineHeight = '1';
	textarea.style.padding = '0';
	textarea.style.margin = '0';
	textarea.style.verticalAlign = 'middle';
	textarea.style.display = 'flex';
	textarea.style.alignItems = 'center';
	textarea.style.justifyContent = 'center';
	textarea.style.whiteSpace = 'pre-wrap';
	textarea.style.overflow = 'hidden';
	textarea.style.transform = 'translate(0, 0)';
	textarea.style.boxSizing = 'border-box';
	textarea.focus();
	textarea.addEventListener('keyup', () => {
		requestAnimationFrame(() => {
			const scaleX = konvaText.scaleX() || 1;
			const scaleY = konvaText.scaleY() || 1;
			const currentWidth = konvaText.width() * scaleX;
			const currentHeight = konvaText.height() * scaleY;
			const textBeforeCursor = textarea.value.substring(0, textarea.selectionStart);
			const lastNewlineIndex = textBeforeCursor.lastIndexOf('\n');
			const textToMeasure = lastNewlineIndex >= 0
				? textBeforeCursor.substring(lastNewlineIndex + 1)
				: textBeforeCursor;
			const tempText = new Konva.Text({
				text: textarea.value,
				fontSize: konvaText.fontSize(),
				fontFamily: konvaText.fontFamily(),
				width: konvaText.width(),
				align: konvaText.align(),
				verticalAlign: konvaText.verticalAlign()
			});
			const tempTextForCursor = new Konva.Text({
				text: textToMeasure,
				fontSize: konvaText.fontSize(),
				fontFamily: konvaText.fontFamily(),
				width: konvaText.width(),
				align: konvaText.align(),
				verticalAlign: konvaText.verticalAlign()
			});
			const newTextWidth = tempText.width() * scaleX;
			const newTextHeight = tempText.height() * scaleY;
			const cursorLineWidth = tempTextForCursor.width() * scaleX;
			if (newTextWidth > currentWidth || newTextHeight > currentHeight || cursorLineWidth < currentWidth) {
				const newWidth = lastNewlineIndex >= 0
					? Math.max(konvaText.width(), tempTextForCursor.width())
					: Math.max(konvaText.width(), tempText.width());
				const heightMargin = 20;
				konvaText.width(newWidth);
				konvaText.height(tempText.height() + heightMargin);
				textarea.style.width = newWidth * scaleX + 'px';
				textarea.style.height = (tempText.height() + heightMargin) * scaleY + 'px';
				tr.nodes([konvaText]);
				tr.forceUpdate();
				layer.batchDraw();
			}
			tempText.destroy();
			tempTextForCursor.destroy();
		});
	});
	const getDeleteButtonPos = () => {
		const scaleX = konvaText.scaleX() || 1;
		return { x: konvaText.x() + konvaText.width() * scaleX - 15, y: konvaText.y() - 15 };
	};
	const initialPos = getDeleteButtonPos();
	const deleteGroup = new Konva.Group({
		x: initialPos.x,
		y: initialPos.y,
		opacity: 0,
		listening: true
	});
	const deleteCircle = new Konva.Circle({
		radius: 12,
		fill: '#dc3545',
		stroke: '#ffffff',
		strokeWidth: 2,
		shadowColor: '#000',
		shadowBlur: 6,
		shadowOffset: { x: 0, y: 2 },
		shadowOpacity: 0.3
	});
	const deleteIcon = new Konva.Path({
		data: 'M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6',
		stroke: '#fff',
		strokeWidth: 2,
		strokeLineCap: 'round',
		strokeLineJoin: 'round',
		scaleX: 0.8,
		scaleY: 0.8,
		x: -8,
		y: -8
	});
	deleteGroup.add(deleteCircle);
	deleteGroup.add(deleteIcon);
	deleteGroup.on('click', (e) => {
		e.evt.stopPropagation();
		deleteImage(konvaText, tr, deleteGroup);
	});
	deleteGroup.on('mouseenter', () => {
		deleteCircle.fill('#c82333');
		stageRef.value.getNode().container().style.cursor = 'pointer';
		layer.batchDraw();
	});
	deleteGroup.on('mouseleave', () => {
		deleteCircle.fill('#dc3545');
		stageRef.value.getNode().container().style.cursor = 'default';
		layer.batchDraw();
	});
	deleteButtons.push(deleteGroup);
	layer.add(deleteGroup);
	deleteGroup.to({
		opacity: 1,
		duration: 0.2
	});
	const updateDeleteButtonPosition = () => {
		const pos = getDeleteButtonPos();
		deleteGroup.x(pos.x);
		deleteGroup.y(pos.y);
	};

	const updateTextareaPosition = () => {
		const textarea = document.getElementById("textarea");
		if (!textarea) return;
		const stage = stageRef.value.getNode();
		const stageBox = stage.container().getBoundingClientRect();
		const stageScale = stage.scaleX();
		const textPosition = konvaText.getAbsolutePosition();
		const scaleX = konvaText.scaleX() || 1;
		const scaleY = konvaText.scaleY() || 1;
		const origWidth = konvaText.getAttr('originalWidth') || 220;
		const origHeight = konvaText.getAttr('originalHeight') || 80;
		const origFontSize = konvaText.getAttr('originalFontSize') || 32;
		const newWidth = origWidth * scaleX;
		const newHeight = origHeight * scaleY;
		const newFontSize = origFontSize * scaleX;
		textarea.style.top = (stageBox.top + textPosition.y * stageScale + 20) + 'px';
		textarea.style.left = (stageBox.left + textPosition.x * stageScale) + 'px';
		textarea.style.width = newWidth * stageScale + 'px';
		textarea.style.height = newHeight * stageScale + 'px';
		textarea.style.fontSize = newFontSize * stageScale + 'px';
	};
	const buffer = []
	textarea.addEventListener('keydown', e => {
		buffer.push(e.key)
		if (lastWsSendTime !== 0 && Date.now() - lastWsSendTime < 16) return
		if (ws.value && ws.value.readyState === WebSocket.OPEN) {
			ws.value.send(JSON.stringify({
				type: "text-modify",
				text: textarea.value,
				id: konvaText.id(),
				keys: buffer.join('')
			}));
		}
	})
	konvaText.on('dragmove', () => {
		updateDeleteButtonPosition();
		const stage = stageRef.value.getNode();
		stage.container().style.cursor = 'grab';
		const previewTextToDrag = previewLayer.findOne(`#${konvaText.id()}`);
		if (previewTextToDrag) {
			previewTextToDrag.position(konvaText.position());
			previewLayer.batchDraw();
		}
	});
	tr.on('transform', () => {
		updateDeleteButtonPosition();
		updateTextareaPosition();
		const previewTextToResize = previewLayer.findOne(`#${konvaText.id()}`);
		const scaleX = konvaText.scaleX() || 1;
		const scaleY = konvaText.scaleY() || 1;
		const origFontSize = konvaText.getAttr('originalFontSize') || 32;
		const origWidth = konvaText.getAttr('originalWidth') || 220;
		const origHeight = konvaText.getAttr('originalHeight') || 80;
		const newFontSize = origFontSize * scaleX;
		const newWidth = origWidth * scaleX;
		const newHeight = origHeight * scaleY;
		if (previewTextToResize) {
			previewTextToResize.x(konvaText.x());
			previewTextToResize.y(konvaText.y());
			previewTextToResize.fontSize(newFontSize);
			previewTextToResize.width(newWidth);
			previewTextToResize.height(newHeight);
			previewTextToResize.scaleX(1);
			previewTextToResize.scaleY(1);
			previewLayer.batchDraw();
		}
		if (ws.value && ws.value.readyState === WebSocket.OPEN) {
			ws.value.send(JSON.stringify({
				type: "resize-shape",
				id: konvaText.id(),
				x: konvaText.x(),
				y: konvaText.y(),
				width: newWidth,
				height: newHeight,
				fontSize: newFontSize,
			}));
		}
	})
	tr.on('transformend', () => {
		updateTextareaPosition();
	})
	layer.draw();
};


const handleDblClick = (e) => {
	const konvaImg = e.target;
	const layer = layerRef.value.getNode();
	if (!layer || !konvaImg) return;
	const tr = new Konva.Transformer({
		nodes: [konvaImg],
		borderStroke: "#ffc107",
		borderDash: [5, 5],
		borderStrokeWidth: 1,
		borderDashOffset: 0,
		borderJoinStyle: "round",
		scalingEnabled: true,
		enabledAnchors: ["top-left", "top-right", "bottom-left", "bottom-right"],
		keepRatio: true,
		keepRatioByExpanding: true,
		rotateEnabled: false,
		boundBoxFunc: (oldBox, newBox) => {
			if (newBox.width < 5 || newBox.height < 5) {
				return oldBox;
			}
			return newBox;
		},
	});
	disableTransformers();
	transformers.push(tr);
	layer.add(tr);
	const getDeleteButtonPos = () => {
		const scaleX = konvaImg.scaleX() || 1;
		return { x: konvaImg.x() + konvaImg.width() * scaleX - 15, y: konvaImg.y() - 15 };
	};
	const initialPos = getDeleteButtonPos();
	const deleteGroup = new Konva.Group({
		x: initialPos.x,
		y: initialPos.y,
		opacity: 0,
		listening: true
	});
	const deleteCircle = new Konva.Circle({
		radius: 14,
		fill: '#dc3545',
		stroke: '#ffffff',
		strokeWidth: 2,
		shadowColor: '#000',
		shadowBlur: 6,
		shadowOffset: { x: 0, y: 2 },
		shadowOpacity: 0.3
	});
	const deleteIcon = new Konva.Path({
		data: 'M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6',
		stroke: '#fff',
		strokeWidth: 2,
		strokeLineCap: 'round',
		strokeLineJoin: 'round',
		scaleX: 0.8,
		scaleY: 0.8,
		x: -8,
		y: -8
	});
	deleteGroup.add(deleteCircle);
	deleteGroup.add(deleteIcon);
	deleteGroup.on('click', (e) => {
		e.evt.stopPropagation();
		deleteImage(konvaImg, tr, deleteGroup);
	});
	deleteGroup.on('mouseenter', () => {
		deleteCircle.fill('#c82333');
		stageRef.value.getNode().container().style.cursor = 'pointer';
		layer.batchDraw();
	});
	deleteGroup.on('mouseleave', () => {
		deleteCircle.fill('#dc3545');
		stageRef.value.getNode().container().style.cursor = 'default';
		layer.batchDraw();
	});
	deleteButtons.push(deleteGroup);
	layer.add(deleteGroup);
	deleteGroup.to({
		opacity: 1,
		duration: 0.2
	});
	const updateDeleteButtonPosition = () => {
		const pos = getDeleteButtonPos();
		deleteGroup.x(pos.x);
		deleteGroup.y(pos.y);
	};

	tr.on('transform', () => {
		updateDeleteButtonPosition();
		layer.batchDraw();
		const previewImageToResize = previewLayer.findOne(`#${konvaImg.id()}`);
		if (previewImageToResize) {
			previewImageToResize.x(konvaImg.x());
			previewImageToResize.y(konvaImg.y());
			previewImageToResize.width(konvaImg.width() * konvaImg.scaleX());
			previewImageToResize.height(konvaImg.height() * konvaImg.scaleY());
			previewImageToResize.scaleX(1);
			previewImageToResize.scaleY(1);
			previewLayer.draw();
		}
		if (ws.value && ws.value.readyState === WebSocket.OPEN) {
			ws.value.send(JSON.stringify({
				type: "img_resize",
				id: konvaImg.id(),
				x: konvaImg.x(),
				y: konvaImg.y(),
				width: konvaImg.width() * konvaImg.scaleX(),
				height: konvaImg.height() * konvaImg.scaleY()
			}));
		}
	});
	layer.draw();
}

const deleteImage = (imageNode, transformer, deleteBtn) => {
	const layer = layerRef.value.getNode();
	if (!layer) return;
	const imageId = imageNode.id();
	if (texts.includes(imageId)) texts.splice(texts.indexOf(imageId), 1)
	if (document.getElementById("textarea")) document.getElementById("textarea").remove()
	imageNode.destroy();
	if (transformer) {
		transformer.destroy();
	}
	if (deleteBtn) {
		deleteBtn.destroy();
	}
	const trIndex = transformers.indexOf(transformer);
	if (trIndex > -1) {
		transformers.splice(trIndex, 1);
	}
	const btnIndex = deleteButtons.indexOf(deleteBtn);
	if (btnIndex > -1) {
		deleteButtons.splice(btnIndex, 1);
	}
	layer.batchDraw();
	const previewImage = previewLayer.findOne(`#${imageId}`);
	if (previewImage) {
		previewImage.destroy();
		previewLayer.batchDraw();
	}
	if (ws.value && ws.value.readyState === WebSocket.OPEN) {
		ws.value.send(JSON.stringify({
			type: "img_delete",
			id: imageId
		}));
	}
	addToHistory();
}

const disableTransformers = () => {
	for (const transformer of transformers) {
		transformer.destroy();
	}
	for (const btn of deleteButtons) {
		btn.destroy();
	}
	transformers.length = 0;
	deleteButtons.length = 0;
}

const finishTextEditing = () => {
	const textarea = document.getElementById("textarea");
	if (!textarea || !textarea.dataset.textId) return;
	const layer = layerRef.value.getNode();
	const konvaText = layer.findOne(`#${textarea.dataset.textId}`);
	if (konvaText) {
		konvaText.text(textarea.value);
		layer.draw();
		document.body.removeChild(textarea);
		konvaText.show();
	}
	texts.forEach(konvaTextId => {
		const found = layer.findOne(`#${konvaTextId}`);
		if (found) {
			found.draggable(true);
			found.show()
		}
		const previewText = previewLayer.findOne(`#${konvaTextId}`);
		if (previewText) {
			previewText.text(konvaText.text());
			previewLayer.draw();
			previewText.draggable(true);
			previewText.show()
		}
	})
	disableTransformers();
}

const handleStageClick = (e) => {
	const target = e.target;
	if (target && (target.className === 'Transformer' || target.getParent()?.className === 'Transformer')) {
		return;
	}
	finishTextEditing();
}

const check_visitor = async () => {
	if (MODE === 'demo') {
		visitor.value = true;
		return;
	}
	try {
		const data = await fetch(`${BASE_URL}/status`, {
			method: "GET",
			headers: { "X-CSRFToken": csrf },
			credentials: "include"
		})
		let response = await data.json()
		if (response.status === 200 && response.user) visitor.value = true;
		else visitor.value = false;
	} catch (e) {
		console.error(e)
	}
}

const togglePane = () => {
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

const toggleShapeSelector = () => {
	showShapeSelector.value = !showShapeSelector.value;
}

const toggleBookmark = async () => {
	const me = new URL(window.location.href).pathname.split("/")[2]
	try {
		const data = await fetch(`${BASE_URL}/bookmark/${room.value}`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrf
			},
			credentials: "include",
			body: JSON.stringify({
				"user": me,
				"status": isBookmarked.value
			})
		})
		const response = await data.json()
		if (response.status === 200 && response.bookmarked) {
			isBookmarked.value = true;
		} else {
			isBookmarked.value = false;
		}
	} catch (e) {
		isBookmarked.value = false;
	}
}

const check_book_mark = async () => {
	const me = new URL(window.location.href).pathname.split("/")[2]
	try {
		const data = await fetch(`${BASE_URL}/is_bookmarked/${room.value}`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrf
			},
			body: JSON.stringify({
				"user": me
			}),
			credentials: "include"
		})
		const response = await data.json();
		if (response.status === 200 && response.bookmarked) isBookmarked.value = true;
		else isBookmarked.value = false;
	} catch (e) {
		isBookmarked.value = false;
	}
}
const show_text = computed(() => windowWidth.value > 1300);
const stageConfig = {
	width: 2 * document.documentElement.clientWidth,
	height: 2 * document.documentElement.clientHeight,
	draggable: false
};

const ws = ref(null)
const rawUrl = WS_URL
const cleanBase = rawUrl.endsWith('/') ? rawUrl.slice(0, -1) : rawUrl;
const finalUrl = `${cleanBase}/${room.value}/`;
ws.value = new WebSocket(finalUrl)
ws.value.onopen = function () {
	ws.value.send(JSON.stringify({
		type: "sync-request",
		room: room.value
	}))
}
ws.value.onmessage = async (event) => {
	const data = JSON.parse(event.data);
	if (!data || !data.type) return;
	const layer = layerRef.value.getNode();
	if (data.type === "start") {
		const isEraserRemote = data.operation === 'destination-out';
		const mainLineConfig = {
			stroke: data.stroke,
			strokeWidth: data.width,
			globalCompositeOperation: data.operation,
			points: data.points,
			lineCap: "round",
			lineJoin: "round",
			tension: 0.5
		};
		const previewLineConfig = {
			stroke: isEraserRemote ? background.value : data.stroke,
			strokeWidth: data.width,
			globalCompositeOperation: data.operation,
			points: data.points,
			lineCap: "round",
			lineJoin: "round",
			tension: 0.5
		};
		const mainLine = new Konva.Line(mainLineConfig);
		const previewLine = new Konva.Line(previewLineConfig);
		mainLine._remote = true;
		previewLine._remote = true;
		layer.add(mainLine);
		mainLine.moveToTop();
		previewLayer.add(previewLine);
		previewLine.moveToTop();
		currentLine.value = { main: mainLine, preview: previewLine, _remote: true };
	} else if (data.type === "draw" && currentLine.value?._remote) {
		const mainPoints = currentLine.value.main.points();
		mainPoints.push(...data.points);
		currentLine.value.main.points(mainPoints);
		const previewPoints = currentLine.value.preview.points();
		previewPoints.push(...data.points);
		currentLine.value.preview.points(previewPoints);
		layer.batchDraw();
		previewLayer.batchDraw();
	} else if (data.type === "bg" && data.bg) {
		background.value = data.bg
		motiv.value = data.bg === "#ffffff"
	} else if (data.type == "img") {
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
			konvaImg.on('dblclick', handleDblClick);
			layer.add(konvaImg);
			const previewImg = new Konva.Image({
				id: data.id,
				image: img,
				x: data.x,
				y: data.y,
				width: data.width,
				height: data.height,
			});
			previewLayer.add(previewImg);
			previewLayer.batchDraw();
			layer.batchDraw();
		};
		img.onerror = () => console.error("Remote image failed to load", data.id);
	} else if (data.type === "img_delete" && data.id) {
		const imageToDelete = layer.findOne(`#${data.id}`);
		if (imageToDelete) {
			const tr = transformers.find(t => t.nodes().includes(imageToDelete));
			const btn = deleteButtons.find(b => {
				const btnX = b.x();
				const btnY = b.y();
				const imgX = imageToDelete.x();
				const imgY = imageToDelete.y();
				const imgWidth = imageToDelete.width();
				return Math.abs(btnX - (imgX + imgWidth - 15)) < 5 && Math.abs(btnY - (imgY - 15)) < 5;
			});
			const previewImage = previewLayer.findOne(`#${data.id}`);
			if (previewImage) {
				previewImage.destroy();
			}
			imageToDelete.destroy();
			if (tr) {
				tr.destroy();
				const trIndex = transformers.indexOf(tr);
				if (trIndex > -1) transformers.splice(trIndex, 1);
			}
			if (btn) {
				btn.destroy();
				const btnIndex = deleteButtons.indexOf(btn);
				if (btnIndex > -1) deleteButtons.splice(btnIndex, 1);
			}
			layer.batchDraw();
			previewLayer.draw();
		}
	} else if (data.type === "img_resize" && data.id) {
		const imageToResize = layer.findOne(`#${data.id}`);
		const previewImageToResize = previewLayer.findOne(`#${data.id}`);
		if (imageToResize) {
			imageToResize.x(data.x);
			imageToResize.y(data.y);
			imageToResize.width(data.width);
			imageToResize.height(data.height);
			imageToResize.scaleX(1);
			imageToResize.scaleY(1);
			const tr = transformers.find(t => t.nodes().includes(imageToResize));
			if (tr) {
				tr.forceUpdate();
			}
			const btn = deleteButtons.find(b => {
				const btnX = b.x();
				const btnY = b.y();
				const imgX = imageToResize.x();
				const imgY = imageToResize.y();
				const imgWidth = imageToResize.width();
				return Math.abs(btnX - (imgX + imgWidth - 15)) < 5 && Math.abs(btnY - (imgY - 15)) < 5;
			});
			if (btn) {
				btn.x(data.x + data.width - 15);
				btn.y(data.y - 15);
			}
			layer.batchDraw();
		}
		if (previewImageToResize) {
			previewImageToResize.x(data.x);
			previewImageToResize.y(data.y);
			previewImageToResize.width(data.width);
			previewImageToResize.height(data.height);
			previewImageToResize.scaleX(1);
			previewImageToResize.scaleY(1);
			previewLayer.draw();
		}
	} else if (data.type === "history_update" && data.history) {
		stroke_history.value = data.history
		history_index.value = data.index
	} else if (data.type === "undo") {
		await undo();
	} else if (data.type === "redo") redo();
	else if (data.type === "sync-request") {
		autosave()
		if (ws.value && ws.value.readyState === WebSocket.OPEN) {
			const storageKey = MODE === 'demo' ? 'demo' : room.value;
			ws.value.send(JSON.stringify({
				type: "sync-response",
				context: localStorage.getItem(storageKey)
			}))
		}
	} else if (data.type === "sync-response") {
		responded.value = true
		if (!layerRef.value) {
			await nextTick();
		}
		if (data.context && layerRef.value) {
			await applyStateToLayer(data.context);
		}
	} else if (data.type === "clearall") {
		clearDefinetely(false) //prevent recursive ws calls
	} else if (data.type === "shape" && data.shapeType) {
		const layer = layerRef.value.getNode();
		let shape;
		let previewShape;
		const shapeConfig = {
			id: data.id,
			x: data.x,
			y: data.y,
			draggable: true,
		};
		if (data.shapeType === 'text') {
			Object.assign(shapeConfig, {
				width: data.width,
				height: data.height,
				fill: data.fill,
				fontSize: data.fontSize,
				fontFamily: data.fontFamily,
				text: data.text,
				align: data.align,
				verticalAlign: data.verticalAlign,
			});
			shape = new Konva.Text(shapeConfig);
			shape.setAttr('originalFontSize', data.fontSize);
			shape.setAttr('originalWidth', data.width);
			shape.setAttr('originalHeight', data.height);
			previewShape = new Konva.Text({ ...shapeConfig });
			previewShape.setAttr('originalFontSize', data.fontSize);
			previewShape.setAttr('originalWidth', data.width);
			previewShape.setAttr('originalHeight', data.height);
			shape.on('dragmove', () => {
				previewShape.position(shape.position());
				previewLayer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "text",
						newpos: shape.position(),
						id: shape.id(),
					}));
				}
			});
			previewShape.on('dragmove', () => {
				shape.position(previewShape.position());
				layer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "text",
						newpos: previewShape.position(),
						id: previewShape.id(),
					}));
				}
			});
			shape.on('dblclick', (e) => {
				e.evt.stopPropagation();
				handleTextClick(shape);
			});
			previewShape.on('dblclick', (e) => {
				e.evt.stopPropagation();
				handleTextClick(shape);
			});
		} else if (data.shapeType === 'arrow') {
			Object.assign(shapeConfig, {
				points: data.points,
				stroke: data.stroke,
				strokeWidth: data.strokeWidth,
				pointerLength: data.pointerLength,
				pointerWidth: data.pointerWidth,
				fill: data.fill,
			});
			shape = new Konva.Arrow(shapeConfig);
			previewShape = new Konva.Arrow({ ...shapeConfig });
			shape.on('dragmove', () => {
				previewShape.position(shape.position());
				previewLayer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "arrow",
						newpos: shape.position(),
						id: shape.id(),
					}));
				}
			});
			previewShape.on('dragmove', () => {
				shape.position(previewShape.position());
				layer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "arrow",
						newpos: previewShape.position(),
						id: previewShape.id(),
					}));
				}
			});
		} else if (data.shapeType === 'circle') {
			Object.assign(shapeConfig, {
				radius: data.radius,
				fill: data.fill,
				stroke: data.stroke,
				strokeWidth: data.strokeWidth,
			});
			shape = new Konva.Circle(shapeConfig);
			previewShape = new Konva.Circle({ ...shapeConfig });
			shape.on('dragmove', () => {
				previewShape.position(shape.position());
				previewLayer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "circle",
						newpos: shape.position(),
						id: shape.id(),
					}));
				}
			});
			previewShape.on('dragmove', () => {
				shape.position(previewShape.position());
				layer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "circle",
						newpos: previewShape.position(),
						id: previewShape.id(),
					}));
				}
			});
		} else if (data.shapeType === 'square') {
			Object.assign(shapeConfig, {
				width: data.width,
				height: data.height,
				fill: data.fill,
				stroke: data.stroke,
				strokeWidth: data.strokeWidth,
			});
			shape = new Konva.Rect(shapeConfig);
			previewShape = new Konva.Rect({ ...shapeConfig });
			shape.on('dragmove', () => {
				previewShape.position(shape.position());
				previewLayer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "square",
						newpos: shape.position(),
						id: shape.id(),
					}));
				}
			});
			previewShape.on('dragmove', () => {
				shape.position(previewShape.position());
				layer.batchDraw();
				if (ws.value && ws.value.readyState === WebSocket.OPEN) {
					ws.value.send(JSON.stringify({
						type: "shape-drag",
						shapeType: "square",
						newpos: previewShape.position(),
						id: previewShape.id(),
					}));
				}
			});
		}
		if (shape && previewShape) {
			layer.add(shape);
			previewLayer.add(previewShape);
			shape.moveToTop();
			previewShape.moveToTop();
			layer.batchDraw();
			previewLayer.batchDraw();
			if (data.shapeType === 'text') {
				texts.push(data.id);
			}
		}
	} else if (data.type === "shape-drag" && data.shapeType && data.id) {
		const layer = layerRef.value.getNode();
		const shape = layer.findOne(`#${data.id}`);
		const previewShape = previewLayer.findOne(`#${data.id}`);
		if (shape) {
			shape.position(data.newpos);
			layer.batchDraw();
		}
		if (previewShape) {
			previewShape.position(data.newpos);
			previewLayer.batchDraw();
		}
	} else if (data.type === "resize-shape" && data.id) {
		const layer = layerRef.value.getNode();
		const shape = layer.findOne(`#${data.id}`);
		const previewShape = previewLayer.findOne(`#${data.id}`);
		if (shape) {
			shape.x(data.x);
			shape.y(data.y);
			if (data.fontSize) {
				shape.setAttr('originalFontSize', data.fontSize);
				shape.fontSize(data.fontSize);
			}
			if (data.width) {
				shape.setAttr('originalWidth', data.width);
				shape.width(data.width);
			}
			if (data.height) {
				shape.setAttr('originalHeight', data.height);
				shape.height(data.height);
			}
			shape.scaleX(1);
			shape.scaleY(1);
			const tr = transformers.find(t => t.nodes().includes(shape));
			if (tr) {
				tr.forceUpdate();
			}
			layer.batchDraw();
		}
		if (previewShape) {
			previewShape.x(data.x);
			previewShape.y(data.y);
			if (data.fontSize) {
				previewShape.fontSize(data.fontSize);
			}
			if (data.width) {
				previewShape.width(data.width);
			}
			if (data.height) {
				previewShape.height(data.height);
			}
			previewShape.scaleX(1);
			previewShape.scaleY(1);
			previewLayer.batchDraw();
		}
	} else if (data.type === "text-modify" && data.id) {
		const layer = layerRef.value.getNode();
		const shape = layer.findOne(`#${data.id}`);
		const previewShape = previewLayer.findOne(`#${data.id}`);
		if (shape) {
			shape.text(data.text);
			layer.batchDraw();
		}
		if (previewShape) {
			previewShape.text(data.text);
			previewLayer.batchDraw();
		}
	}
};
const handleContextMenu = (e) => {
	e.evt.preventDefault();
};
const canvas = document.createElement('canvas');
canvas.width = stageConfig.width;
canvas.height = stageConfig.height;
const isSaved = ref(false)

const context = canvas.getContext('2d');
context.strokeStyle = color.value;
context.fillStyle = background.value
context.lineJoin = 'round';
context.lineWidth = Number(width_slider.value);
context.lineCap = 'round';
context.lineJoin = 'round';
const preview = document.createElement('div');
preview.id = 'preview';
preview.style.position = 'absolute';
preview.style.bottom = '5px';
preview.style.left = '5px';
preview.style.border = '5px solid #ffc107';
preview.style.borderRadius = "5%"
preview.style.backgroundColor = background.value;
document.body.appendChild(preview);
const previewStage = new Konva.Stage({
	container: 'preview',
	width: window.innerWidth / 8,
	height: window.innerHeight / 8,
	scaleX: 1 / 32,
	scaleY: 1 / 32,
});

let previewLayer = new Konva.Layer();
const previewBg = new Konva.Rect({
	x: 0,
	y: 0,
	width: previewStage.width() * 32,
	height: previewStage.height() * 32,
	fill: background.value,
	listening: false,
});
previewStage.add(previewLayer);
previewLayer.add(previewBg)

watch(color, (newColor) => {
	context.strokeStyle = newColor;
});
watch(motiv, () => {
	background.value = motiv.value ? "#ffffff" : "#000000"
	color.value = motiv.value ? "#000000" : "#ffffff"
	previewBg.fill(background.value);
	preview.style.backgroundColor = background.value;
	previewLayer.batchDraw();
	if (ws.value && ws.value.readyState === WebSocket.OPEN) {
		ws.value.send(JSON.stringify({
			type: "bg",
			bg: background.value
		}))
	}
}, { immediate: true })

function changeZoom(mode) {
	const scrolles = [50, 75, 100, 125, 150, 175, 200]
	const stage = stageRef.value.getNode();
	const oldScale = stage.scaleX() * 100;
	const direction = mode === "up" ? 1 : -1;
	if ((oldScale === 50 && direction === -1) || (oldScale === 200 && direction === 1)) return;
	const newScale = scrolles[scrolles.indexOf(oldScale) + direction] / 100;
	zooming.value = newScale
	stage.scale({ x: newScale, y: newScale });
	stage.batchDraw();
}

const handleMouseWheel = (e) => {
	e.evt.preventDefault();
	changeZoom(e.evt.deltaY > 0 ? "up" : "down")
}

const check_owner = async () => {
	try {
		const parts = new URL(window.location.href).pathname.split('/');
		const owner = parts[2];
		const data = await fetch(`${BASE_URL}/codraw/check_owner`, {
			method: "POST",
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrf
			},
			credentials: "include",
			body: JSON.stringify({
				"owner": owner,
				"room": room.value
			})
		})
		const response = await data.json()
		if (response.status === 200) {
			admin.value = true
		}
	} catch (e) {
		admin.value = false
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
		showPopup.value = true;
		message.value = "Failed to copy the link.";
	}
};

const load = async () => {
	let data = null;
	if (MODE === 'demo') {
		data = localStorage.getItem("demo");
	} else {
		const parts = new URL(window.location.href).pathname.split('/')[3]
		data = localStorage.getItem(parts);
	}
	if (data) {
		await applyStateToLayer(data);
	}
};
const save_definetely = async () => {
	try {
		loading.value = true
		if (!title.value) {
			showPopup.value = true
			message.value = "Please provide a title for your board."
		}
		if (title.value.length > 66) {
			showPopup.value = true
			message.value = "The title length is to large, must be at most 60 characters."
		}
		if (description.value && description.value.length > 170) {
			showPopup.value = true
			message.value = "The description length is to large, must be at most 100 characters."
		}
		const formData = new FormData();
		formData.append("project", room.value);
		formData.append("title", title.value);
		formData.append("description", description.value);
		formData.append(
			"payload",
			JSON.stringify([{
				id: Date.now(),
				image: stageRef.value.getStage().toJSON()
			}])
		);
		formData.append("bg", background.value);
		formData.append("preview", getPreviewPicture());
		formData.append("type", type.value);
		const data = await fetch(`${BASE_URL}/codraw/save_new`, {
			method: "POST",
			headers: {
				'X-CSRFToken': csrf
			},
			body: formData,
			credentials: "include"
		});
		const response = await data.json()
		let flag = true
		isVisible.value = false
		if (response.status === 200) {
			flag = false
		}
		await new Promise(resolve => setTimeout(() => { loading.value = false; resolve(); }, 2000));
		if (!flag) {
			showPopup.value = true
			message.value = "Board saved successfully."
			isSaved.value = true
			autosave()
		} else {
			showPopup.value = true
			message.value = "There was an error saving your board."
		}
	} catch (e) {
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
	if (ws.value && ws.value.readyState === WebSocket.OPEN) {
		ws.value.send(JSON.stringify({
			type: "history_update",
			history: stroke_history.value,
			index: history_index.value
		}));
	}
}

const undo = async () => {
	if (history_index.value < 0) return;
	const layer = layerRef.value.getNode();
	const children = layer.children || [];
	const lastChild = children[children.length - 1];
	if (lastChild) lastChild.destroy();
	const previewChildren = previewLayer.children || [];
	const lastPreviewChild = previewChildren[previewChildren.length - 1];
	if (lastPreviewChild) lastPreviewChild.destroy();
	disableTransformers();
	history_index.value--;
	previewLayer.batchDraw();
	layer.batchDraw();
}

const redo = () => {
	if (history_index.value >= stroke_history.value.length - 1) return;
	else {
		history_index.value++;
		const layer = layerRef.value.getNode()
		if (!stroke_history.value[history_index.value]) return;
		const history = JSON.parse(stroke_history.value[history_index.value])
		if (history) {
			if (history.className === "Image") {
				const image = new window.Image()
				image.src = history.attrs.src
				image.onload = () => {
					const konvaImg = new Konva.Image({
						id: history.attrs.id || uuidv4(),
						image: image,
						x: history.attrs.x,
						y: history.attrs.y,
						width: history.attrs.width || image.width,
						height: history.attrs.height || image.height,
						draggable: false,
						src: history.attrs.src
					});
					applyCrop(konvaImg)
					konvaImg.setAttr("src", history.attrs.src);
					konvaImg.on('dblclick', handleDblClick);
					layer.add(konvaImg);
					const previewImg = new Konva.Image({
						id: konvaImg.id(),
						image: image,
						x: history.attrs.x,
						y: history.attrs.y,
						width: history.attrs.width || image.width,
						height: history.attrs.height || image.height,
					});
					previewLayer.add(previewImg);
					previewLayer.batchDraw();
					layer.draw();
				}
				image.onerror = () => {
					console.error("Failed to load image for redo");
				}
			} else {
				const KonvaNodeMain = Konva.Node.create(history)
				const KonvaNodePreview = Konva.Node.create(history)
				layer.add(KonvaNodeMain)
				previewLayer.add(KonvaNodePreview)
				previewLayer.draw()
				layer.draw()
			}

		}
	}
	disableTransformers();
}

const undoWithBroadcast = async () => {
	await undo();
	if (ws.value && ws.value.readyState === WebSocket.OPEN) {
		ws.value.send(JSON.stringify({
			type: "undo"
		}));
	}
}

const redoWithBroadcast = () => {
	redo();
	if (ws.value && ws.value.readyState === WebSocket.OPEN) {
		ws.value.send(JSON.stringify({
			type: "redo"
		}));
	}
}

const checkSaveStatus = async () => {
	const owner = new URL(window.location.href).pathname.split('/')[2]
	try {
		const data = await fetch(`${BASE_URL}/codraw/check_saved`, {
			method: "POST",
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				"project": room.value,
				"owner": owner
			})
		})
		const response = await data.json()
		isSaved.value = response.saved
	} catch (e) {
		console.error(e)
		isSaved.value = false
	}
}

const dataURLtoBlob = (dataURL) => {
	const byteString = atob(dataURL.split(',')[1]);
	const mimeString = dataURL.split(',')[0].split(':')[1].split(';')[0];
	const ab = new ArrayBuffer(byteString.length);
	const ia = new Uint8Array(ab);
	for (let i = 0; i < byteString.length; i++) {
		ia[i] = byteString.charCodeAt(i);
	}
	return new Blob([ab], { type: mimeString });
};

const getPreviewPicture = () => {
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
	return dataURL;
}


const processImageFile = (file, x, y) => {
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
				x: x,
				y: y,
				width: img.width,
				height: img.height,
				draggable: false,
				src: e.target.result
			});
			applyCrop(konvaImg);
			const layer = layerRef.value.getNode();
			konvaImg.setAttr("src", e.target.result);
			konvaImg.on('dblclick', handleDblClick);
			layer.add(konvaImg);
			const previewImg = new Konva.Image({
				id: konvaImg.id(),
				image: img,
				x: x,
				y: y,
				width: img.width,
				height: img.height,
			});
			previewLayer.add(previewImg);
			previewLayer.batchDraw();
			layer.draw();
			if (ws.value && ws.value.readyState === WebSocket.OPEN) {
				ws.value.send(JSON.stringify({
					type: "img",
					id: konvaImg.id(),
					src: e.target.result,
					x: konvaImg.x(),
					y: konvaImg.y(),
					width: konvaImg.width(),
					height: konvaImg.height(),
				}));
			}
			addToHistory();
		};
	};
	reader.readAsDataURL(file);
};

const handlePaste = (event) => {
	event.preventDefault();
	const stage = stageRef.value?.getNode?.();
	if (!stage) return;
	const pointer = stage.getPointerPosition();
	let point;
	if (pointer) {
		point = getRelativePointerPosition(stage);
	} else {
		const visibleWidth = window.innerWidth / stage.scaleX();
		const visibleHeight = window.innerHeight / stage.scaleY();
		const centerX = (-stage.x() / stage.scaleX()) + visibleWidth / 2;
		const centerY = (-stage.y() / stage.scaleY()) + visibleHeight / 2;
		point = { x: centerX, y: centerY };
	}
	const clipboardData = event.clipboardData;
	if (!clipboardData || clipboardData.files.length === 0) {
		return;
	}
	const file = clipboardData.files[0];
	processImageFile(file, point.x, point.y);
};


const check_save = async (mode) => {
	try {
		loading.value = true
		if (mode === 'save') {
			if (!isSaved.value) {
				loading.value = false
				isVisible.value = true
				return false
			}
			const formData = new FormData();
			const previewBlob = dataURLtoBlob(getPreviewPicture());
			formData.append("project", room.value);
			formData.append("payload", JSON.stringify(stageRef.value.getStage().toJSON()));
			formData.append("bg", background.value);
			formData.append("preview", previewBlob, `${room.value}.webp`);
			const data = await fetch(`${BASE_URL}/codraw/save_project`, {
				method: "POST",
				headers: {
					'X-CSRFToken': csrf
				},
				body: formData,
				credentials: "include"
			});
			const response = await data.json()
			let flag = true;
			if (response.status === 200) {
				flag = false
			}
			await new Promise(resolve => setTimeout(() => { loading.value = false; resolve(); }, 2000));
			if (!flag) {
				autosave()
				showPopup.value = true
				message.value = "Board was successfully quick saved."
			} else isVisible.value = true
		} else if (mode === 'load') {
			if (MODE === 'demo') {
				const autosaved = localStorage.getItem("demo")
				if (autosaved && !responded.value) {
					await applyStateToLayer(autosaved)
				}
				return false
			}
			const data = await fetch(`${BASE_URL}/codraw/load_project`, {
				method: "POST",
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					"project": room.value,
				}),
			})
			const response = await data.json()
			if (response.status === 200) {
				return true
			}
			const autosaved = localStorage.getItem(MODE === 'demo' ? 'demo' : room.value)
			if (autosaved && !responded.value) {
				await applyStateToLayer(autosaved)
			}
			return false
		}
	} catch (e) {
		console.error(e)
	}
}

function leave() {
	const parts = new URL(window.location.href).pathname.split('/')[3];
	localStorage.removeItem(parts)
	if (origin === 'default') {
		window.location.href = '/codraw'
	} else if (origin.startsWith("search")) {
		window.location.href = `/codraw/${origin}`
	} else if (origin.startsWith("account")) {
		window.location.href = `/codraw/${origin}`
	}
	else {
		window.location.href = '/'
	}
}

function clearDefinetely(native) {
	showPopup.value = false
	message.value = ""
	loading.value = true
	if (MODE === 'demo') {
		localStorage.removeItem("demo")
	} else {
		const parts = new URL(window.location.href).pathname.split('/')[3]
		localStorage.removeItem(parts)
	}
	const layer = layerRef.value.getNode();
	layer.destroyChildren();
	previewLayer.destroyChildren();
	disableTransformers();
	layer.batchDraw();
	previewLayer.batchDraw();
	if (ws.value && ws.value.readyState === WebSocket.OPEN && native) {
		ws.value.send(JSON.stringify({
			type: "clearall"
		}));
	}
	loading.value = false
}

function clear_all() {
	if (admin.value || MODE === 'demo') {
		showPopup.value = true;
		message.value = "Are you sure you would like to clear the board? This action is irreversible.";
	} else {
		showPopup.value = true;
		message.value = "You don't have neccessary permissions to clear the board."
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
	if (MODE === 'demo') {
		localStorage.setItem("demo", JSON.stringify(list.value));
	} else {
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
	if (!e.evt.touches || e.evt.touches.length == 1) {
		const stage = e.target.getStage();
		if (e.evt.button === 2 || paneToggler.value) {
			stage.container().style.cursor = 'grab';
			isPanning.value = true;
			stage.draggable(true);
			stage.startDrag();
			lastPos.value = stage.getPointerPosition();
			return;
		}
		if (e.target !== stage && (e.target.draggable() || e.target.getParent()?.draggable())) {
			return;
		}
		isDrawing.value = true;
		stage.container().style.cursor = 'default';
		const pos = getRelativePointerPosition(stage);
		const isEraser = tool.value === 'eraser';
		const mainStrokeColor = isEraser ? 'rgba(0,0,0,1)' : color.value;
		const previewStrokeColor = isEraser ? 'rgba(0,0,0,1)' : color.value;
		const mainLineConfig = {
			stroke: mainStrokeColor,
			strokeWidth: Number(width_slider.value),
			globalCompositeOperation: isEraser ? 'destination-out' : 'source-over',
			points: [pos.x, pos.y],
			lineCap: 'round',
			lineJoin: 'round',
			tension: 0.5
		};
		const previewLineConfig = {
			stroke: previewStrokeColor,
			strokeWidth: Number(width_slider.value),
			globalCompositeOperation: isEraser ? 'destination-out' : 'source-over',
			points: [pos.x, pos.y],
			lineCap: 'round',
			lineJoin: 'round',
			tension: 0.5
		};
		const mainLine = new Konva.Line(mainLineConfig);
		const previewLine = new Konva.Line(previewLineConfig);
		previewLayer.add(previewLine);
		previewLine.moveToTop();
		if (ws.value && ws.value.readyState === WebSocket.OPEN) {
			ws.value.send(JSON.stringify({
				type: "start",
				stroke: color.value,
				width: Number(width_slider.value),
				operation: tool.value === 'eraser' ? 'destination-out' : 'source-over',
				points: [pos.x, pos.y]
			}));
		}
		const mainLayer = layerRef.value.getNode();
		mainLayer.add(mainLine);
		mainLine.moveToTop();
		previewLayer.draw()
		currentLine.value = { main: mainLine, preview: previewLine };
	} else if (e.evt.touches && e.evt.touches.length == 2) {
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
		previewLayer.batchDraw();
	}
};

const handleMouseMove = (e) => {
	if (!e.evt.touches || e.evt.touches.length == 1) {
		if (!isDrawing.value || !currentLine.value) return;
		const stage = e.target.getStage();
		const point = getRelativePointerPosition(stage);
		const mainPoints = currentLine.value.main.points();
		mainPoints.push(point.x, point.y);
		currentLine.value.main.points(mainPoints);
		const previewPoints = currentLine.value.preview.points();
		previewPoints.push(point.x, point.y);
		currentLine.value.preview.points(previewPoints);
		const now = Date.now();
		if (now - lastWsSendTime >= 16 && ws.value && ws.value.readyState === WebSocket.OPEN) {
			lastWsSendTime = now;
			ws.value.send(JSON.stringify({
				type: "draw",
				points: [point.x, point.y]
			}));
		}
		if (drawFrameId === null) {
			drawFrameId = requestAnimationFrame(() => {
				layerRef.value.getNode().batchDraw();
				previewLayer.batchDraw();
				drawFrameId = null;
			});
		}
	} else if (e.evt.touches && e.evt.touches.length == 2 && lastCenter) {
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
		if (newScale > 0.05 && newScale < 5) {
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
	disableTransformers();
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
					resolve();
				};
				img.src = shapeJson.attrs.src;
			});
		}
		return Promise.resolve();
	});
	await Promise.all(imagePromises);
	savedChildren.forEach(shapeJson => {
		const previewShape = Konva.Node.create(shapeJson);
		const mainShape = Konva.Node.create(shapeJson);
		previewLayer.add(previewShape);
		layer.add(mainShape);
		if (mainShape.className === 'Image') {
			applyCrop(mainShape);
			mainShape.on('dblclick', handleDblClick);
		}
	});
	previewLayer.batchDraw();
	layer.batchDraw();
};

const get_details_and_load = async () => {
	try {
		if (MODE === 'default') {
			const data = await fetch(`${BASE_URL}/codraw/get_details`, {
				method: "POST",
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					"project": room.value
				})
			})
			const response = await data.json()
			const saved_json = response.canva;
			const bg = response.bg;
			const last_access = response.last
			if (bg) {
				background.value = bg
				motiv.value = bg === "#ffffff"
			}
			const localData = localStorage.getItem(room.value);
			if (localData && localData.length > saved_json.length) {
				const parsedLocal = JSON.parse(localData);
				if (parsedLocal && parsedLocal[0] && parsedLocal[0].id > last_access) {
					await load();
					return;
				}
			}
			if (saved_json) {
				await applyStateToLayer(saved_json)
			}
		} else if (MODE === 'demo') {
			const localData = localStorage.getItem(room.value);
			if (localData) {
				const parsedLocal = JSON.parse(localData);
				if (parsedLocal && parsedLocal[0]) {
					await load();
					return;
				}
			}
		}
	} catch (e) {
		console.error(e)
	}
}

const handleFiles = (event) => {
	const stage = stageRef.value?.getNode?.();
	if (!stage) return;
	const files = event.target.files;
	if (!files || files.length === 0) return;
	const visibleWidth = window.innerWidth / stage.scaleX();
	const visibleHeight = window.innerHeight / stage.scaleY();
	const centerX = (-stage.x() / stage.scaleX()) + visibleWidth / 2;
	const centerY = (-stage.y() / stage.scaleY()) + visibleHeight / 2;
	Array.from(files).forEach((file, index) => {
		if (file.type.startsWith('image/')) {
			const offsetX = (index % 3) * 30;
			const offsetY = Math.floor(index / 3) * 30;
			processImageFile(file, centerX + offsetX, centerY + offsetY);
		}
	});
	event.target.value = '';
}

const keyhandler = async (event) => {
	if (event.ctrlKey && (event.key === 'z' || event.key === 'Z')) {
		event.preventDefault();
		await undo()
		if (ws.value && ws.value.readyState === WebSocket.OPEN) {
			ws.value.send(JSON.stringify({
				type: "undo"
			}))
		}
	}
	else if (event.ctrlKey && (event.key === 'y' || event.key === 'Y')) {
		event.preventDefault();
		redo()
		if (ws.value && ws.value.readyState === WebSocket.OPEN) {
			ws.value.send(JSON.stringify({
				type: "redo"
			}))
		}
	}
}

let autosaveInterval = null;

const waitForSync = () => new Promise(resolve => {
	const check = setInterval(() => {
		if (responded.value) {
			clearInterval(check);
			resolve();
		}
	}, 100);
	setTimeout(() => { clearInterval(check); resolve(); }, 5000);
});

onMounted(async () => {
	loading.value = true
	await nextTick();
	await waitForSync();
	if (await check_save('load')) {
		if (!responded.value) {
			get_details_and_load()
		}
	}
	if (MODE === 'demo') {
		visitor.value = true;
	} else {
		await Promise.all([check_owner(), check_visitor(), checkSaveStatus()])
	}
	if (visitor.value && MODE !== 'demo') {
		await check_book_mark();
	}
	autosaveInterval = setInterval(() => autosave(), 60000)
	window.addEventListener('keydown', keyhandler)
	window.addEventListener('resize', handleStageResize);
	window.addEventListener('paste', handlePaste)
	const inputElement = document.getElementById("upload");
	inputElement.addEventListener("change", handleFiles);
	loading.value = false;
})
onBeforeUnmount(() => {
	if (ws.value) {
		ws.value.close()
	}
	loading.value = true
})
onUnmounted(() => {
	clearInterval(autosaveInterval)
	window.removeEventListener('paste', handlePaste)
	window.removeEventListener("keydown", keyhandler)
	window.removeEventListener("resize", handleStageResize)
	const inputElement = document.getElementById("upload");
	if (inputElement) {
		inputElement.removeEventListener("change", handleFiles);
	}
})
</script>

<style>
html,
body {
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

@media(max-width:800px) {
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

	#save_btn,
	#clearall,
	#exit {
		width: 50px !important;
		font-size: 0.5rem !important;
		padding: 10px 10px !important;
	}
}

.feature-icon {
	font-size: 1.25rem;
	color: orange;
	transition: transform 0.3s ease;
}

#confirm_clear {
	background-color: green !important;
	transition: 0.3s ease !important;
}

#confirm_clear:hover {
	background-color: #00cc00 !important;
}

.feature-icon:hover {
	transform: scale(1.2) rotate(5deg);
}

.fade-slide-enter-from,
.fade-slide-leave-to {
	opacity: 0;
	transform: translateY(-20px);
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
	touch-action: none;
	-webkit-user-select: none;
	user-select: none;
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

.save:hover {
	background: #fff;
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
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
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

input:checked+.slider {
	background-color: #4f8cff;
}

input:checked+.slider::before {
	transform: translateX(18px);
}

@media(max-width:1500px) {
	#toolbar {
		font-size: 0.8rem;
		gap: 10px;
	}
}

@media(max-width:1330px) {
	#toolbar {
		left: 2% !important;
	}

	#inv {
		right: 0.5rem;
		font-size: 0.5rem;
	}
}

@media(max-width:1150px) {
	#toolbar {
		gap: 5px !important;
	}
}

@media(max-width:950px) {
	#inv_div {
		top: 140px !important;
		position: fixed !important;
	}
}

@media(max-width:800px) {
	#inv_div {
		top: 10px !important;
	}
}

#zoom {
	position: fixed;
	right: 10px;
	bottom: 10px;
	background-color: white;
	z-index: 10;
}


#inv:hover,
#bookmark-btn:hover,
#save_btn:hover,
#save_def:hover,
#close_form:hover {
	background: #fff !important;
	color: #4f8cff !important;
}

#exit:hover {
	background: #fff !important;
	color: #ff4f4f !important;
}

#clearall:hover {
	background: #fff !important;
	color: #f68608 !important;
}
</style>
