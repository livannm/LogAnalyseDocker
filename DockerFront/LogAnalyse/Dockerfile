FROM node:16.15-alpine

RUN mkdir -p /home/app

ENV ENV_BACKEND_URI=http://127.0.0.1:5000

COPY . /home/app

WORKDIR home/app/

RUN npm install -g @angular/cli

RUN npm install

RUN npm run build --prod

EXPOSE 4200

CMD ["ng","serve","--host","0.0.0.0"]