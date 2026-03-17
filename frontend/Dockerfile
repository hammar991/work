# use the official Bun image
# see all versions at https://hub.docker.com/r/oven/bun/tags
FROM 127.0.0.1:5000/docker.io/oven/bun:1 AS base
WORKDIR /usr/src/app

# install dependencies into temp directory
# this will cache them and speed up future builds
FROM base AS install
RUN mkdir -p /temp/dev
COPY package.json bun.lock bunfig.toml /temp/dev/
RUN cd /temp/dev && bun install --frozen-lockfile

# install with --production (exclude devDependencies)
RUN mkdir -p /temp/prod
COPY package.json bun.lock /temp/prod/
RUN cd /temp/prod && bun install --frozen-lockfile --production

# copy node_modules from temp directory
# then copy all (non-ignored) project files into the image
FROM base AS prerelease
COPY --from=install /temp/dev/node_modules node_modules
COPY . .

# [optional] tests & build
ENV NODE_ENV=production
RUN bun vite build

# copy production dependencies and source code into final image
# 使用 static-web-server 镜像（Rust 编写，约 3MB）
FROM 127.0.0.1:5000/docker.io/joseluisq/static-web-server:2

# 设置服务端口
ENV SERVER_PORT=80
# 设置网页根目录
ENV SERVER_ROOT=/var/www
# 启用目录列表（可选）
ENV SERVER_DIRECTORY_LISTING=true
# 启用压缩
ENV SERVER_COMPRESSION=true
# 日志级别
ENV SERVER_LOG_LEVEL=info

# 复制静态文件到容器
COPY dist/ /var/www/

# 暴露端口
EXPOSE 80
