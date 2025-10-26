FROM node:25-alpine3.21
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm","run","serve"]