# --- Build Stage ---
FROM node:20-alpine AS build

WORKDIR /app

# Copy package management files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Declare build-time environment arguments (Vite needs these during build)
ARG VITE_API_URL
ARG VITE_SUPABASE_URL
ARG VITE_SUPABASE_ANON_KEY

# Set them as environment variables so Vite build compiles them in
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_SUPABASE_URL=$VITE_SUPABASE_URL
ENV VITE_SUPABASE_ANON_KEY=$VITE_SUPABASE_ANON_KEY

# Build the project
RUN npm run build

# --- Production Stage ---
FROM nginx:alpine

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build output from build stage to Nginx html folder
COPY --from=build /app/dist /usr/share/nginx/html

# Cloud Run defaults to 8080. Nginx is configured to listen on 8080 in nginx.conf
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
