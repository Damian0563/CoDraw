import { io } from "socket.io-client";
import { reactive } from "vue";
export const state = reactive({
  connected: false,
});
const URL = process.env.NODE_ENV === "production" ? undefined : "http://localhost:3000";

export const socket = io(URL);