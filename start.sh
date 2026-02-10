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

# 使用 quietlink CLI 启动
echo ""
uv run quietlink --port "${1:-8080}" $([ "$2" = "https" ] && echo "--https")
