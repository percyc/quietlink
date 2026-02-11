# QuietLink v1.0.0 - WebRTC 局域网屏幕共享

基于 WebRTC 的纯局域网屏幕共享系统，支持音视频传输，无需互联网连接。

**[English](README_EN.md)** | [![PyPI version](https://badge.fury.io/py/percyc/quietlink.svg)](https://pypi.org/project/quietlink/) | [![Docker Hub](https://img.shields.io/docker/v/percyc/quietlink)](https://hub.docker.com/r/percyc/quietlink) | [![Demo](https://img.shields.io/badge/Demo-Live-green)](https://quietlink.onrender.com/)

## 在线体验

访问 [https://quietlink.onrender.com/](https://quietlink.onrender.com/) 体验在线 Demo。

## 安装方式

### 方式一：使用 PyPI 安装（推荐）

```bash
# 使用 pip 安装
pip install quietlink==1.0.0

# 或使用 uv 安装（更快）
uv pip install quietlink==1.0.0

# 启动服务（注意：现代浏览器要求 HTTPS 才能使用 WebRTC，如果不了解技术细节，请直接使用 HTTPS）
quietlink --port 8443 --https
quietlink --port 9000 --http
```

### 方式二：使用 Docker 部署

#### 单架构部署（快速）

```bash
# HTTPS 模式（推荐，现代浏览器要求）
docker run -d -p 8443:8443 \
  -e PORT=8443 \
  -e HTTPS=true \
  --name quietlink-https \
  percyc/quietlink:v1.0.0

# HTTP 模式（需要额外设置 HTTPS 代理）
docker run -d -p 8080:8080 \
  -e PORT=8080 \
  -e HTTPS=false \
  --name quietlink \
  percyc/quietlink:v1.0.0
```

#### 多架构部署（支持 AMD64 + ARM64）

```bash
# 使用 buildx 构建（首次需要启用）
docker buildx create --use

# 自动构建并推送多架构
docker buildx build --platform linux/amd64,linux/arm64 \
  -t percyc/quietlink:v1.0.0 \
  -t percyc/quietlink:latest \
  --push .

# 或直接拉取使用
docker run -d -p 8080:8080 \
  -e PORT=8080 \
  -e HTTPS=false \
  --name quietlink \
  percyc/quietlink:latest
```

#### 使用 Docker Compose

```bash
# 复制提供的 docker-compose.yml
docker-compose up -d

# 或自定义配置
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  quietlink:
    image: percyc/quietlink:latest
    container_name: quietlink
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
      - HTTPS=false
    restart: unless-stopped
EOF

docker-compose up -d
```

### 方式三：本地开发

```bash
# 克隆仓库
git clone https://github.com/percyc/quietlink.git
cd quietlink

# 使用 uv 同步依赖
uv sync

# 启动开发服务器（推荐 HTTPS 模式）
./start.sh 8443 https
# 或 HTTP 模式（需要额外设置 HTTPS 代理）
./start.sh 8080
```

---

## 功能特点

- 📺 **屏幕共享**：主机端可共享整个屏幕或单个窗口
- 🔊 **音频传输**：支持系统音频共享（Chrome/Edge），可选启用
- 👁️ **实时观看**：客户端可实时观看共享内容
- 🔒 **房间隔离**：6位数字房间码，确保私密性
- ✅ **授权机制**：主机需手动批准客户端加入请求
- 📴 **纯内网运行**：无需 STUN/TURN 服务器，无需互联网
- 📱 **移动端支持**：支持手机全屏观看，响应式设计
- 🎨 **美观界面**：现代化渐变设计，优秀的用户体验
- 🌐 **多架构支持**：Docker 镜像支持 AMD64 和 ARM64（Mac、树莓派等）
- 🔧 **简单部署**：PyPI 一键安装，Docker 秒级启动

---

## 命令行参数

```bash
quietlink [选项]

选项：
  -h, --help       显示帮助信息
  --port, -p PORT   服务器端口（默认: 8080）
  --https           启用 HTTPS 模式（自动生成自签名证书）

示例:
  quietlink                    在默认端口 8080 启动
  quietlink --port 9000        在端口 9000 启动
  quietlink --https             启用 HTTPS 模式
```

---

## 使用说明

### 共享端（Host）

1. 启动服务：`quietlink --port 8443 --https`
2. 打开浏览器访问 `https://<服务器IP>:8443/host.html`
3. 勾选"共享系统音频"（可选，默认关闭）
4. 点击"开始屏幕共享"按钮
5. 选择要共享的屏幕或窗口
6. 系统生成 6 位房间码（如：123456）
7. 将房间码告知观看端
8. 收到加入请求时点击"同意"授权

### 观看端（Client）

1. 打开浏览器访问 `https://<服务器IP>:8443/client.html`
2. 输入房间码（如：123456）
3. 点击"加入"
4. 等待主机批准
5. 连接成功后可以点击"开启声音"播放音频（如果主机共享了音频）
6. 支持全屏观看

### 重要提醒

现代浏览器（Chrome、Edge、Firefox 等）出于安全考虑，要求 **HTTPS 环境才能使用 WebRTC 功能**。如果您使用 HTTP 部署，将无法建立音视频连接，需要额外设置 HTTPS 代理。建议直接使用 HTTPS 模式部署以避免不必要的配置。

---

## 音频功能

### 主机端
- 默认不传输音频，保护隐私
- 勾选"共享系统音频"可启用音频传输
- Chrome/Edge 支持系统音频捕获
- Firefox 仅支持麦克风（不推荐）

### 客户端
- 默认静音，需要手动点击"开启声音"
- 可以随时点击静音/取消静音按钮控制音频
- 全屏模式下音频控制按钮仍然可用

### 注意事项
- 音频传输会增加网络带宽占用
- 首次使用时浏览器会请求音频权限
- 系统音频捕获需要用户明确授权

---

## 网络要求

**必须在同一局域网内**（同一网段，如 `192.168.1.x`）才能正常连接。

WebRTC 在同一网段内可以直接通过本地 IP 建立连接，无需 STUN/TURN 服务器。

---

## 端口说明

| 端口 | 用途 | 说明 |
|------|------|------|
| 8080 | HTTP/WebSocket | 信令服务和页面服务（需要额外 HTTPS 代理） |
| 8443 | HTTPS | 安全连接（推荐，现代浏览器必需） |

---

## 云端部署

项目支持 Render 部署。

### Render 部署

1. 连接 GitHub 仓库到 Render
2. 创建新的 Web Service
3. 选择 Python 环境，自动检测依赖
4. 部署完成获得 `https://<app-name>.onrender.com` 地址

**注意**：当前项目设计为局域网使用。在公网环境部署后，WebRTC P2P 连接需要额外的 STUN/TURN 服务器支持。公网部署仅供体验，建议在内网环境使用以获得最佳性能。

---

## 故障排查

### WebRTC 连接失败 / 视频黑屏

1. **首先确认是否使用 HTTPS**：现代浏览器要求 HTTPS 才能使用 WebRTC
2. 如果使用 HTTP，请改用 HTTPS 模式：`quietlink --port 8443 --https`
3. 检查浏览器控制台是否有 HTTPS 或 WebRTC 相关错误
4. 在 Firefox 地址栏输入 `about:webrtc` 查看详细日志
5. 确认两端在同一网段

### HTTP vs HTTPS 说明

- **HTTP**：仅适用于开发调试，需要额外设置 HTTPS 代理才能使用
- **HTTPS**：现代浏览器必须要求，自动生成自签名证书
- 如果您看到 "getUserMedia is not allowed in insecure contexts" 错误，说明需要 HTTPS

### 无声音

1. **主机端**：确认已勾选"共享系统音频"
2. **客户端**：点击"开启声音"按钮取消静音
3. 检查浏览器是否授予了音频播放权限
4. 确认使用的是 Chrome/Edge（支持系统音频）
5. 查看浏览器控制台是否有 `[Audio] Audio track received` 日志

### 音频捕获失败

1. 检查浏览器是否支持系统音频（Chrome/Edge）
2. 确认已授予音频捕获权限
3. 尝试刷新页面重新连接
4. 音频捕获失败不影响视频共享

### 客户端无法访问

1. 确认防火墙放行了 8080 端口
2. 检查 SELinux/AppArmor 设置
3. 确认在同一局域网内

### 全屏按钮不可见

1. 刷新页面重新加载
2. 检查浏览器是否支持全屏 API
3. 尝试点击视频区域触发全屏

---

## 项目结构

```
.
├── quietlink/              # Python 包
│   ├── __init__.py       # 包入口
│   ├── server.py         # FastAPI 应用
│   ├── cli.py            # 命令行工具
│   └── static/           # 静态文件
│       ├── index.html      # 主页
│       ├── host.html       # 共享端
│       └── client.html     # 观看端
├── pyproject.toml          # Python 依赖配置
├── Dockerfile             # Docker 构建文件
├── docker-compose.yml      # Docker 编排文件
├── start.sh              # 开发启动脚本
├── LICENSE               # MIT 许可证
├── README.md             # 项目文档
└── tests/                # 测试目录
```

---

## 技术栈

- **后端**：Python 3.14+ + FastAPI + WebSocket
- **前端**：原生 JavaScript + WebRTC API
- **依赖管理**：uv（现代 Python 包管理器）
- **音频编解码**：Opus（WebRTC 默认）
- **部署方式**：PyPI、Docker、本地开发
- **HTTPS**：自签名证书自动生成，现代浏览器要求

---

## 安全说明

- 音频默认禁用，保护用户隐私
- 房间码随机生成，防止暴力破解
- 主机需手动批准客户端加入
- 内网使用，无需暴露到公网
- 自动生成 HTTPS 证书，符合现代浏览器安全要求
- 如需公网部署，请配置强密码和有效的 HTTPS 证书

---

## 浏览器兼容性

| 功能 | Chrome/Edge | Firefox | Safari |
|------|-------------|---------|--------|
| 视频共享 | ✅ | ✅ | ✅ |
| 系统音频 | ✅ | ❌ | ⚠️ 限制 |
| 麦克风音频 | ✅ | ✅ | ✅ |
| 全屏播放 | ✅ | ✅ | ✅ |
| 移动端 | ✅ | ✅ | ✅ |
| HTTPS 要求 | ✅ 必须 | ✅ 必须 | ✅ 必须 |

### 重要说明
- 所有现代浏览器都要求在 **HTTPS 环境** 下才能使用 WebRTC 功能
- HTTP 仅适用于开发调试，生产环境请务必使用 HTTPS
- 自签名证书需要在浏览器中手动信任（通常会出现"您的连接不是私密连接"警告）

---

## 许可证

MIT License

---

## 相关链接

- **PyPI**：https://pypi.org/project/quietlink/
- **Docker Hub**：https://hub.docker.com/r/percyc/quietlink
- **GitHub**：https://github.com/percyc/quietlink
- **Demo**：https://quietlink.onrender.com/

---

## 更新日志

### v1.0.0 (2025-02-10)

- 🎉 首次发布
- ✅ 支持 PyPI 安装
- ✅ 支持 Docker 部署（AMD64 + ARM64）
- ✅ 支持命令行工具
- ✅ 优化的项目结构
- ✅ 完整的文档和示例

---

## 贡献

欢迎提交 Issue 和 Pull Request！
