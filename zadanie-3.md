po pierwszym prompcie:

# Obraz bazowy Node.js
FROM node:22-alpine

# Katalog roboczy
WORKDIR /app

# Kopiowanie plików zależności
COPY package*.json ./

# Instalacja zależności
RUN npm install

# Kopiowanie kodu aplikacji
COPY . .

# Port aplikacji
EXPOSE 3000

# Uruchomienie aplikacji
CMD ["npm", "start"]

po drugim:

# Obraz bazowy Node.js 18
FROM node:18

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie plików package.json i package-lock.json
COPY package.json package-lock.json ./

# Instalacja zależności
RUN npm install

# Kopiowanie pozostałych plików aplikacji
COPY . .

# Wystawienie portu 3000
EXPOSE 3000

# Uruchomienie aplikacji
CMD ["npm", "start"]
