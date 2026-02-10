# QuietLink - WebRTC 局域网屏幕共享 - 项目上下文

## 项目概述

这是一个基于 WebRTC 的纯局域网屏幕共享系统，支持音视频传输，无需互联网连接。项目采用前后端分离架构，后端使用 FastAPI 提供 WebSocket 信令服务，前端使用原生 JavaScript + WebRTC API 实现音视频通信。

### 主要特性
- 屏幕共享：主机端可共享整个屏幕或单个窗口
- 音频传输：支持系统音频共享（Chrome/Edge），可选启用
- 房间隔离：6位数字房间码，确保私密性
- 授权机制：主机需手动批准客户端加入请求
- 纯内网运行：无需 STUN/TURN 服务器，无需互联网
- 移动端支持：支持手机全屏观看，响应式设计

## 技术栈

### 后端
- **Python 3.14+**：主要编程语言
- **FastAPI**：Web 框架，提供 HTTP 和 WebSocket 服务
- **Uvicorn**：ASGI 服务器
- **WebSockets**：实时双向通信
- **CORS**：跨域资源共享配置

### 前端
- **原生 JavaScript**：不使用任何前端框架
- **WebRTC API**：浏览器原生音视频通信 API
- **HTML5/CSS3**：现代 Web 技术
- **响应式设计**：支持桌面和移动设备

### 依赖管理
- **uv**：现代 Python 包管理器，类似 pip 但更快更可靠

## 项目结构

```
quietlink/
├── main.py              # FastAPI 信令服务器（478行）
├── start.sh             # 启动脚本，自动安装依赖和生成证书
├── pyproject.toml       # Python 依赖配置
├── uv.lock              # 依赖锁定文件
├── README.md            # 项目文档
├── .gitignore           # Git 忽略配置
├── certs/               # SSL 证书目录（已加入 .gitignore）
│   ├── cert.pem         # SSL 证书文件
│   └── key.pem          # SSL 私钥文件
└── static/
    ├── host.html        # 共享端页面（788行）
    └── client.html      # 观看端页面（688行）
```

## 核心架构

### 信令流程
1. **主机创建房间**：连接 `/ws/host` WebSocket，生成6位房间码
2. **客户端加入**：连接 `/ws/client/{room_code}`，获得8位客户端 ID
3. **请求授权**：主机收到加入请求，显示在"待处理请求"列表
4. **批准加入**：主机同意后，发送 `join_approved` 消息
5. **WebRTC 连接**：开始 SDP 协商（offer/answer）和 ICE 候选交换
6. **音视频传输**：建立 P2P 连接，开始流传输

### 关键类和函数

#### main.py
- **ConnectionManager**：管理 WebSocket 连接和房间状态
  - `create_room()`: 创建新房间
  - `join_room()`: 客户端加入房间
  - `authorize_client()`: 授权客户端
  - `get_host()`: 获取主机连接
  - `get_client()`: 获取客户端连接

#### host.html
- `startScreenShare()`: 开始屏幕共享，调用 `getDisplayMedia()`
- `stopScreenShare()`: 停止共享，清理资源
- `approveClient()`: 批准客户端加入
- `rejectClient()`: 拒绝客户端加入
- `disconnectClient()`: 断开指定客户端
- `createPeerConnection()`: 创建 WebRTC 连接
- `goHome()`: 返回主页

#### client.html
- `joinRoom()`: 加入房间
- `handleOffer()`: 处理主机发送的 offer
- `handleIceCandidate()`: 处理 ICE 候选
- `toggleMute()`: 切换静音状态
- `toggleFullscreen()`: 切换全屏
- `goHome()`: 返回主页

## 构建和运行

### 启动服务器

```bash
# HTTP 模式（默认端口 8080）
./start.sh

# 指定端口
./start.sh 9000

# HTTPS 模式（自动生成自签名证书）
./start.sh 8443 https

# 完整参数
./start.sh 9000 https
```

### 依赖管理

```bash
# 同步依赖（自动在 start.sh 中执行）
uv sync

# 添加新依赖
uv add package-name

# 移除依赖
uv remove package-name
```

### 开发模式

```bash
# 使用 uv 直接运行（支持热重载）
uv run uvicorn main:app --host 0.0.0.0 --port 8080 --reload

# HTTPS 模式
uv run uvicorn main:app --host 0.0.0.0 --port 8443 --ssl-certfile certs/cert.pem --ssl-keyfile certs/key.pem
```

## 开发约定

### 代码风格
- **Python**：遵循 PEP 8 规范
- **JavaScript**：使用现代 ES6+ 语法
- **HTML/CSS**：使用语义化标签，CSS 使用渐变设计风格
- **注释**：代码注释简洁，重点说明"为什么"而非"是什么"

### WebSocket 消息格式

所有消息均为 JSON 格式：

```javascript
// 客户端加入请求
{
  "type": "join_request",
  "client_id": "a1b2c3d4"
}

// 主机批准
{
  "type": "join_approve",
  "client_id": "a1b2c3d4"
}

// SDP Offer
{
  "type": "offer",
  "client_id": "a1b2c3d4",
  "sdp": "...",
  "sdpType": "offer"
}

// ICE 候选
{
  "type": "ice_candidate",
  "target": "client",  // 或 "host"
  "client_id": "a1b2c3d4",
  "candidate": "...",
  "sdpMid": "...",
  "sdpMLineIndex": 0
}
```

### 测试要点
- **局域网测试**：确保两端在同一网段
- **跨浏览器测试**：Chrome/Edge/Firefox/Safari
- **移动端测试**：iOS/Android 浏览器
- **音频功能**：Chrome/Edge 支持系统音频，Firefox 不支持
- **HTTPS 测试**：测试自签名证书的信任问题

### 已知限制
- 必须在同一局域网内（无 STUN/TURN 支持）
- Firefox 不支持系统音频捕获
- iOS Safari 对全屏 API 有特殊处理
- 首次访问 HTTPS 需要信任自签名证书

## 调试技巧

### 浏览器调试
- Chrome: `chrome://webrtc-internals`
- Firefox: `about:webrtc`
- 控制台查看 `[WS]`、`[WebRTC]`、`[Audio]` 前缀的日志

### 常见问题
1. **视频黑屏**：检查 ICE 候选是否正确交换
2. **无声音**：确认主机启用音频，客户端取消静音
3. **连接失败**：确认在同一网段，防火墙放行端口
4. **全屏问题**：检查 z-index 和 pointer-events

### 日志关键词
- `[WS]`: WebSocket 消息
- `[WebRTC]`: WebRTC 连接状态
- `[Audio]`: 音频相关
- `[Video]`: 视频相关
- `[ICE]`: ICE 连接状态

## 安全考虑

- 音频默认禁用，保护隐私
- 房间码随机生成（6位数字）
- 主机需手动批准客户端加入
- SSL 证书存放在 `certs/` 目录（已加入 .gitignore）
- CORS 配置允许所有 origins（仅局域网使用）
- 如需公网部署，需配置 HTTPS 和认证机制

## 移动端特殊处理

### iOS Safari
- 使用 `webkitEnterFullscreen()` 进入全屏
- 监听 `webkitbeginfullscreen`/`webkitendfullscreen` 事件
- 视频元素需要 `playsinline` 和 `webkit-playsinline` 属性

### Android Chrome
- 标准全屏 API 支持
- 音频自动播放策略更宽松

### 响应式断点
- 768px：平板设备
- 480px：手机竖屏
- 360px：小屏手机

## 未来改进方向

- [ ] 添加音量滑块控制
- [ ] 支持多个客户端同时观看
- [ ] 添加视频质量设置
- [ ] 支持录制功能
- [ ] 添加聊天功能
- [ ] 支持文件传输
- [ ] 添加屏幕标注功能