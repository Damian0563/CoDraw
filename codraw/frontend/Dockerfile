FROM node:20-alpine AS builder
WORKDIR /app
ARG VUE_APP_BASE_URL
ARG VUE_APP_WS_URL
ARG VUE_APP_GTAG
ARG VUE_APP_GOOGLE_ID
ENV VUE_APP_BASE_URL=${VUE_APP_BASE_URL}
ENV VUE_APP_WS_URL=${VUE_APP_WS_URL}
ENV VUE_APP_GTAG=${VUE_APP_GTAG}
ENV VUE_APP_GOOGLE_ID=${VUE_APP_GOOGLE_ID}
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
