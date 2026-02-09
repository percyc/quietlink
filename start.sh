#!/bin/bash

# WebRTC Screen Share 启动脚本

echo "🚀 启动 WebRTC 局域网屏幕共享服务器..."
echo ""

# 进入项目目录
cd "$(dirname "$0")"

# 检查uv是否安装，未安装则安装
if ! command -v uv &> /dev/null; then
    echo "📦 安装 uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# 同步依赖
echo "📦 同步依赖..."
uv sync

# 获取端口参数或使用默认值
PORT=${1:-8080}

# 检查HTTPS模式
if [ "$2" = "https" ]; then
    echo "🔒 启用HTTPS模式"
    # 创建证书目录
    mkdir -p certs
    if [ ! -f "certs/cert.pem" ] || [ ! -f "certs/key.pem" ]; then
        echo "📜 生成自签名证书..."
        openssl req -x509 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
    fi
    echo ""
    echo "⚠️  首次访问时会提示证书不受信任，点击高级 → 继续访问"
fi

# 设置协议
if [ "$2" = "https" ]; then
    PROTOCOL="https"
else
    PROTOCOL="http"
fi

echo ""
echo "✅ 准备启动服务器..."
echo "📡 服务器地址: ${PROTOCOL}://localhost:$PORT"
echo ""
echo "🔗 访问链接："
echo "   共享端: ${PROTOCOL}://localhost:$PORT/host.html"
echo "   观看端: ${PROTOCOL}://localhost:$PORT/client.html"
echo ""
echo "💡 局域网访问（替换为你的IP）:"
echo "   ${PROTOCOL}://$(hostname -I | awk '{print $1}'):$PORT/host.html"
echo ""

# 启动服务器
if [ "$2" = "https" ]; then
    # 检查证书是否存在
    mkdir -p certs
    if [ ! -f "certs/cert.pem" ] || [ ! -f "certs/key.pem" ]; then
        echo "📜 生成自签名证书..."
        openssl req -x509 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
    fi
    uv run uvicorn main:app --host 0.0.0.0 --port "$PORT" --reload --ssl-certfile certs/cert.pem --ssl-keyfile certs/key.pem
else
    uv run uvicorn main:app --host 0.0.0.0 --port "$PORT" --reload
fi
