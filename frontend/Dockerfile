# Use Node.js for building the frontend
FROM node:18

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose port used by Vite
EXPOSE 5173

# Start the frontend app
CMD ["npm", "run", "dev"]
