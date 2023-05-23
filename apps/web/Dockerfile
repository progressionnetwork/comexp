FROM node:18 as builder
WORKDIR /app
COPY package.json ./

RUN yarn
COPY . ./
RUN yarn build

FROM nginx:latest
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]