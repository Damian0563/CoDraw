const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: ['vue3-spinners'],
  devServer: {
    port: 8000,
    host: '0.0.0.0', // Necessary for Docker to bind correctly
  },
})
