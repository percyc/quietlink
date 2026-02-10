# QuietLink 发布指南

## 🌏 国内网络优化

### 方案 1：使用清华镜像源（推荐）

Dockerfile 已配置清华镜像源：
```dockerfile
ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 方案 2：手动构建（备用）

如果拉包失败，手动上传依赖：

```bash
# 1. 本地导出依赖
uv pip compile -o requirements.txt

# 2. 构建时手动安装
# 在 Dockerfile 中添加：
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 方案 3：使用阿里云镜像

修改 Dockerfile 的镜像源：
```dockerfile
ENV UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
```

---

## 🔒 Docker HTTPS 支持

### 方式 1：环境变量（推荐）

```bash
# HTTP 模式
docker run -d -p 8080:8080 \
  -e PORT=8080 \
  -e HTTPS=false \
  percyc/quietlink:latest

# HTTPS 模式
docker run -d -p 8443:8443 \
  -e PORT=8443 \
  -e HTTPS=true \
  percyc/quietlink:latest
```

### 方式 2：Docker Compose

使用 `docker-compose.yml`：

```bash
# HTTP 模式
docker-compose -f docker-compose.yml up -d quietlink

# HTTPS 模式
docker-compose up -d quietlink-https
```

### 方式 3：自定义配置

创建 `docker-compose.override.yml`：

```yaml
version: '3.8'
services:
  quietlink:
    image: percyc/quietlink:latest
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
      - HTTPS=false
    volumes:
      - ./data:/app/data
```

---

## 🚀 发布命令（优化版）

### PyPI 发布

```bash
# 方式 1：直接上传
uv run twine upload dist/*

# 方式 2：使用国内镜像测试
uv run twine upload --repository-url https://test.pypi.org/simple/ dist/*

# 方式 3：多线程上传（加速）
uv run twine upload --verbose dist/*
```

### Docker Hub 发布

```bash
# 1. 登录
docker login

# 2. 构建（已优化国内镜像）
docker build -t percyc/quietlink:0.1.0 .

# 3. 测试 HTTPS
docker run -d -p 8443:8443 \
  -e PORT=8443 \
  -e HTTPS=true \
  --name quietlink-test \
  percyc/quietlink:0.1.0

# 4. 推送
docker push percyc/quietlink:0.1.0
docker tag percyc/quietlink:0.1.0 percyc/quietlink:latest
docker push percyc/quietlink:latest
```

---

## 📋 国内可用镜像源

| 镜像源 | 地址 | 说明 |
|---------|------|------|
| 清华大学 | https://pypi.tuna.tsinghua.edu.cn/simple/ | 稳定快速 |
| 阿里云 | https://mirrors.aliyun.com/pypi/simple/ | 国内推荐 |
| 华为云 | https://mirrors.huaweicloud.com/repository/pypi/simple/ | 企业推荐 |
| 豆瓣 | https://pypi.douban.com/simple/ | 备用 |

---

## 🔧 本地构建加速

如果 Docker 构建慢，使用本地缓存：

```bash
# 创建本地缓存
docker build --build-arg BUILDKIT_INLINE_CACHE=1 \
  -t percyc/quietlink:0.1.0 .

# 或使用 BuildKit
DOCKER_BUILDKIT=1 docker build -t percyc/quietlink:0.1.0 .
```

---

## 🐛 问题排查

### uv sync 失败

```bash
# 清除缓存重试
uv cache clean
uv sync --no-dev

# 或使用 pip
pip install -r <(uv pip compile)
```

### Docker 推送慢

```bash
# 使用多架构并行构建
docker buildx build --platform linux/amd64,linux/arm64 \
  -t percyc/quietlink:0.1.0 \
  --push .

# 压缩镜像层
docker build --no-cache --squash -t percyc/quietlink:0.1.0 .
```

---

## ✅ 优化总结

- ✅ **Docker 支持 HTTPS**：通过环境变量控制
- ✅ **国内镜像源**：使用清华镜像加速
- ✅ **Docker Compose**：提供 HTTP/HTTPS 两种模式
- ✅ **本地缓存**：支持离线构建
