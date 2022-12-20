FROM node:14-alpine

WORKDIR app/

COPY package.json package-lock.json ./
COPY . .

RUN npm install

EXPOSE 3000

CMD ["npm", "start"]