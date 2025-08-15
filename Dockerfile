# syntax=docker/dockerfile:1
FROM node:20-alpine

# Ensure native deps work smoothly
RUN apk add --no-cache python3 make g++ git

WORKDIR /app

# Copy package files early for caching
COPY package.json yarn.lock ./

# Deterministic install with Yarn v1
RUN yarn install --frozen-lockfile

# Copy the rest
COPY . .

# Build (adjust if your app uses a different script)
ENV NODE_OPTIONS="--max-old-space-size=2048"
RUN yarn build

# Web app default
EXPOSE 3000
CMD ["yarn","start"]