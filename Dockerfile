FROM node:8.15.0
WORKDIR /src
COPY package.json package-lock.json /src/
RUN npm ci
COPY .git /src/.git
