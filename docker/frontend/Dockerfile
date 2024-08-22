FROM node:18-alpine AS base
ARG ENV_NAME

# 1. Install dependencies only when needed
FROM base AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat tini bash
WORKDIR /app/deps/frontend

# Install dependencies based on the preferred package manager
COPY deps/frontend/package.json ./
COPY deps/frontend/yarn.lock ./
# fix the problem with sharp https://stackoverflow.com/a/77150832
RUN --mount=type=cache,target=/root/.yarn \
    YARN_CACHE_FOLDER=/root/.yarn \
    yarn --frozen-lockfile && npm rebuild --arch=x64 --platform=linux --libc=musl sharp

RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# USER nextjs

# set hostname to localhost
ENV HOSTNAME="0.0.0.0"

# server.js is created by next build from the standalone output
# https://nextjs.org/docs/pages/api-reference/next-config-js/output
ENTRYPOINT ["tini", "--"]
CMD ["bash", "/app/docker/frontend/serve.sh"]
