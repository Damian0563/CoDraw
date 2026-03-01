import { reactive } from 'vue';

export const BASE_URL = process.env.VUE_APP_BASE_URL;
export const WS_URL = process.env.VUE_APP_WS_URL;
export const GTAG = process.env.VUE_APP_GTAG;
export const GOOGLE_ID = process.env.VUE_APP_GOOGLE_ID;
export const wsConnections = reactive({});
function get_cookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
export { get_cookie };
