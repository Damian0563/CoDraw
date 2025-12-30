const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
	transpileDependencies: ['vue3-spinners'],
	devServer: {
		port: 8001,
		host: '0.0.0.0',
	},
	// devServer: {
	//   port: 8000,
	//   host: '0.0.0.0',
	//   allowedHosts: ['codrawapp.com', 'www.codrawapp.com', '34.116.244.111'],
	//   client: {
	//     webSocketURL: 'wss://codrawapp.com/ws',
	//   },
	//   headers: {
	//     "Access-Control-Allow-Origin": "*",
	//   }
	// }
})
