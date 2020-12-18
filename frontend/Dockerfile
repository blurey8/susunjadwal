FROM node:15.4.0-buster

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm install react-scripts -g

COPY . ./

CMD ["npm", "start"]