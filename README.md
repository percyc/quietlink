# WebRTC 局域网屏幕共享

基于 WebRTC 的纯局域网屏幕共享系统，无需互联网连接。

## 功能特点

- 📺 **屏幕共享**：主机端可共享整个屏幕或单个窗口
- 👁️ **实时观看**：客户端可实时观看共享内容
- 🔒 **房间隔离**：6位数字房间码，确保私密性
- ✅ **授权机制**：主机需手动批准客户端加入请求
- 📴 **纯内网运行**：无需 STUN/TURN 服务器，无需互联网

## 快速开始

```bash
./start.sh [端口] [https]
```

参数说明：
- `端口`：服务器端口，默认 8080
- `https`：可选，启用 HTTPS（自动生成自签名证书）

示例：
```bash
# HTTP 模式
./start.sh

# HTTPS 模式
./start.sh 8443 https
```

## 系统要求

- Python 3.8+
- [uv](https://github.com/astral-sh/uv)（自动安装）

## 使用说明

### 共享端（Host）

1. 打开浏览器访问 `http://<服务器IP>:8080/host.html`
2. 点击"开始屏幕共享"按钮
3. 系统生成6位房间码（如：123456）
4. 将房间码告知观看端
5. 收到加入请求时点击"同意"授权

### 观看端（Client）

1. 打开浏览器访问 `http://<服务器IP>:8080/client.html`
2. 输入房间码（如：123456）
3. 点击"加入"
4. 等待主机批准
5. 连接成功后即可观看共享屏幕

## 网络要求

**必须在同一局域网内**（同一网段，如 `192.168.1.x`）

WebRTC 在同一网段内可以直接通过本地 IP 建立连接，无需 STUN/TURN 服务器。

### 端口说明

| 端口 | 用途 | 说明 |
|------|------|------|
| 8080 | HTTP/WebSocket | 信令服务 |

## 故障排查

### 连接成功但视频黑屏

1. 检查浏览器控制台是否有 ICE 错误
2. 在 Firefox 地址栏输入 `about:webrtc` 查看详细日志
3. 确认两端在同一网段

### 客户端无法访问

1. 确认防火墙放行了 8080 端口：
   ```bash
   # Linux (iptables)
   sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
   ```

2. 检查 SELinux/AppArmor 设置

## 项目结构

```
.
├── main.py              # FastAPI 信令服务器
├── start.sh             # 启动脚本
├── static/
│   ├── host.html        # 共享端页面
│   └── client.html      # 观看端页面
└── pyproject.toml       # Python 依赖
```

## 技术栈

- **后端**：Python + FastAPI + WebSocket
- **前端**：原生 JavaScript + WebRTC API
- **依赖管理**：uv

## 许可证

MIT License