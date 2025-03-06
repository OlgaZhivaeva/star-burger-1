FROM node:16

WORKDIR /star-burger/frontend

COPY package*.json ./

RUN npm ci

COPY . .

RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
