FROM node:20

WORKDIR /app

COPY package.json .

RUN npm install

COPY src ./src
COPY proto ./proto

EXPOSE 50051

CMD ["npm", "start"]
