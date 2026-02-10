FROM python:3.14-slim

WORKDIR /app

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装依赖（移除 --frozen，允许重新解析依赖）
RUN uv sync --no-dev

# 复制应用代码
COPY quietlink/ ./quietlink/

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["uv", "run", "quietlink", "--port", "8080"]