# Servicio del chat. Contexto de build = raíz del repo (comparte src/lib/buscador-config.mjs con el sitio).
#   Coolify: Base Directory "/", Dockerfile Location "/chat-api/Dockerfile", puerto 3000.
FROM node:22-alpine
WORKDIR /app
COPY src/lib/buscador-config.mjs ./src/lib/buscador-config.mjs
COPY chat-api/package.json chat-api/package-lock.json ./chat-api/
WORKDIR /app/chat-api
RUN npm ci --omit=dev
COPY chat-api/src ./src
ENV NODE_ENV=production DATA_DIR=/data PORT=3000
RUN mkdir -p /data && chown node:node /data
USER node
VOLUME /data
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1:3000/healthz >/dev/null || exit 1
CMD ["node", "src/server.mjs"]
