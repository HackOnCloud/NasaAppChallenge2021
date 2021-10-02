FROM node:14.17.6-alpine as builder

ARG NODE_ENV=production
ENV NODE_ENV production

WORKDIR /
COPY package*.json ./

RUN npm install
COPY . ./

RUN npm run build
EXPOSE 3000
CMD [ "npm", "start" ]
