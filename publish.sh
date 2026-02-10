#!/bin/bash

# QuietLink v1.0.0 发布脚本

echo "🚀 开始发布 QuietLink v1.0.0..."
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. 清理旧构建产物
echo "${YELLOW}📦 清理旧构建产物...${NC}"
rm -rf dist/ build/

# 2. 构建 Python 包
echo "${GREEN}🔨 构建 Python 包...${NC}"
uv run python -m build

# 检查构建是否成功
if [ ! -f "dist/quietlink-1.0.0-py3-none-any.whl" ]; then
    echo "${YELLOW}❌ 构建失败！${NC}"
    exit 1
fi

echo "${GREEN}✅ 构建成功！${NC}"
echo ""
ls -lh dist/
echo ""

# 3. 询问是否上传
read -p "是否上传到 PyPI？(y/n) " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "${GREEN}📦 上传到 PyPI...${NC}"
    uv run twine upload dist/*
    echo "${GREEN}✅ PyPI 发布完成！${NC}"
    echo "${YELLOW}📝 访问: https://pypi.org/project/quietlink/${NC}"
fi

echo ""
echo "${GREEN}🎉 发布完成！${NC}"
