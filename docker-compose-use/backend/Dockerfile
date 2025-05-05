FROM node:8.1

WORKDIR /backend

COPY package*.json ./

RUN npm install

COPY . .

CMD ["node", "app"]