# ============================================
# Stage 1: 基础镜像
# ============================================
FROM 127.0.0.1:5000/docker.io/oven/bun:1 AS base
WORKDIR /usr/src/app

# ============================================
# Stage 2: 安装依赖
# ============================================
FROM base AS deps

# 仅复制依赖描述文件
COPY package.json bun.lock bunfig.toml ./

# 安装所有依赖（包含 devDependencies，构建阶段需要）
RUN bun install --frozen-lockfile

# ============================================
# Stage 3: 构建
# ============================================
FROM base AS build

# 复制依赖
COPY --from=deps /usr/src/app/node_modules ./node_modules

# 复制源代码
COPY . .

# 执行构建
RUN bun vite build

# ============================================
# Stage 4: 最终运行镜像
# ============================================
FROM 127.0.0.1:5000/docker.io/library/nginx

# 基础配置
ENV SERVER_PORT=80
ENV SERVER_ROOT=/var/www

# 安全配置：关闭目录列表
ENV SERVER_DIRECTORY_LISTING=false

# 性能配置：开启 gzip/brotli 压缩
ENV SERVER_COMPRESSION=true

# 日志级别
ENV SERVER_LOG_LEVEL=warn

# 删除默认的 nginx 配置
RUN rm /etc/nginx/conf.d/default.conf

# 复制自定义 nginx 配置文件
COPY nginx.conf /etc/nginx/nginx.conf

# 从构建阶段复制构建产物
COPY --from=build /usr/src/app/dist /var/www

# 给 nginx 用户赋予文件读取权限
RUN chown -R nginx:nginx /var/www && \
    chmod -R 755 /var/www

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

EXPOSE 80

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"]

