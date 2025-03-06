FROM node:16

WORKDIR /star-burger/frontend

COPY package*.json ./

RUN npm ci

COPY . .

RUN chown -R node:node /star-burger/frontend/bundles

USER node
