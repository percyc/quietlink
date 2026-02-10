FROM python:3.14-slim

WORKDIR /app

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 配置国内镜像源
ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/

# 复制所有必需文件（配置、许可证、代码）
COPY pyproject.toml uv.lock LICENSE ./
COPY quietlink/ ./quietlink/

# 安装依赖（现在代码目录已存在）
RUN uv sync --no-dev

# 暴露端口（HTTP 和 HTTPS）
EXPOSE 8080 8443

# 环境变量：HTTPS 模式
ENV HTTPS=false
ENV PORT=8080

# 创建启动脚本（处理环境变量）
RUN echo '#!/bin/sh\n\
if [ "$HTTPS" = "true" ]; then\n\
    exec uv run quietlink --port $PORT --https\n\
else\n\
    exec uv run quietlink --port $PORT\n\
fi\n' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# 启动命令
CMD ["/app/entrypoint.sh"]