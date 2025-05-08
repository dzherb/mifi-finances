FROM node:alpine AS build
WORKDIR /app
COPY package.json package.json
RUN npm install

ARG BACKEND_SERVER_HOST
ARG BACKEND_SERVER_PORT
ENV VITE_BACKEND_SERVER_HOST=$BACKEND_SERVER_HOST
ENV VITE_BACKEND_SERVER_PORT=$BACKEND_SERVER_PORT

COPY . .
RUN npm run build

FROM alpine
COPY --from=build /app/dist /tmp_static

CMD mv /tmp_static/* /static && rm -rf /tmp_static