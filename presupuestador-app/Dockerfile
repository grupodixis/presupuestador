FROM node:24-alpine

WORKDIR /app
ENV NODE_ENV=production
ENV PORT=4177

COPY server.js ./server.js
COPY public ./public
COPY README.md ./README.md

RUN mkdir -p /app/data
EXPOSE 4177

CMD ["node", "server.js"]
