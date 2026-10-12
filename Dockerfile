# --- build: Astro -> dist/ ---
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY astro.config.mjs tsconfig.json ./
COPY public ./public
COPY src ./src
# INCLUDE_DRAFTS=1 solo en staging: publica borradores con noindex. En producción queda en 0.
ARG INCLUDE_DRAFTS=0
ENV INCLUDE_DRAFTS=$INCLUDE_DRAFTS
# URL pública del servicio de chat (vacía = el chat responde con el buscador local, sin IA)
ARG PUBLIC_CHAT_URL=
ENV PUBLIC_CHAT_URL=$PUBLIC_CHAT_URL
RUN npm run build

# --- runtime: nginx ---
FROM nginx:1.27-alpine
RUN rm -f /etc/nginx/conf.d/default.conf && mkdir -p /etc/nginx/snippets
COPY deploy/security-headers.conf /etc/nginx/snippets/security-headers.conf
COPY deploy/nginx.conf /etc/nginx/conf.d/site.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1
