# Use an official Node image
FROM node:18

# Set working directory inside the container
WORKDIR /app

# Copy package manifest files first
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy all frontend code (all files in the current folder)
COPY . .

# Expose the Vite development server port
EXPOSE 5173

# Start the Vite development server
CMD ["npm", "run", "dev"]
