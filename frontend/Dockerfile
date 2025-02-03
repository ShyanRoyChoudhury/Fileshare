# Frontend Build Stage
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm i
COPY . .
RUN npm run build

EXPOSE 5173
# CMD [ "npx", "serve", 'dist','-p', '5173' ]

# Serve with Nginx
FROM nginx:alpine
# Copy the built React app to Nginx's web server directory
COPY --from=build /app/dist /usr/share/nginx/html
# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]