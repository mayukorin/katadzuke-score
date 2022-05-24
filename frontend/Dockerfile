FROM node:12.14.1

WORKDIR /katadzuke-score/frontend
RUN npm install -g @vue/cli 
COPY  ./package*.json /katadzuke-score/frontend/
RUN npm install
COPY . .
RUN npm run build
EXPOSE 8080