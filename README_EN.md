# QuietLink v1.0.0 - WebRTC Local Area Network Screen Sharing

A WebRTC-based pure LAN screen sharing system with audio/video transmission support, no internet connection required.

[中文](README.md) | [![PyPI version](https://badge.fury.io/py/percyc/quietlink.svg)](https://pypi.org/project/quietlink/) | [![Docker Hub](https://img.shields.io/docker/v/percyc/quietlink)](https://hub.docker.com/r/percyc/quietlink) | [![Demo](https://img.shields.io/badge/Demo-Live-green)](https://quietlink.onrender.com/)

## Online Demo

Visit [https://quietlink.onrender.com/](https://quietlink.onrender.com/) to try the online demo.

## Features

- 📺 **Screen Sharing**: Host can share entire screen or single window
- 🔊 **Audio Transmission**: Supports system audio sharing (Chrome/Edge), optional enable
- 👁️ **Real-time Viewing**: Clients can watch shared content in real-time
- 🔒 **Room Isolation**: 6-digit room code ensures privacy
- ✅ **Authorization Mechanism**: Host manually approves client join requests
- 📴 **Pure Intranet Operation**: No STUN/TURN servers needed, no internet required
- 📱 **Mobile Support**: Supports fullscreen viewing on phones, responsive design
- 🎨 **Beautiful UI**: Modern gradient design, excellent user experience
- 🌐 **Multi-architecture Support**: Docker images support AMD64 and ARM64 (Mac, Raspberry Pi, etc.)
- 🔧 **Simple Deployment**: One-click installation via PyPI, instant Docker startup

## Installation Methods

### Method 1: Install via PyPI (Recommended)

```bash
# Install with pip
pip install quietlink==1.0.0

# Or use uv for faster installation
uv pip install quietlink==1.0.0

# Start service (note: modern browsers require HTTPS for WebRTC, use HTTPS if unsure)
quietlink --port 8443 --https
quietlink --port 9000 --http
```

### Method 2: Docker Deployment

#### Single Architecture Deployment (Quick)

```bash
# Pull and run
docker run -d -p 8443:8443 \
  -e PORT=8443 \
  -e HTTPS=true \
  --name quietlink-https \
  percyc/quietlink:v1.0.0

# HTTP mode (requires additional HTTPS proxy)
docker run -d -p 8080:8080 \
  -e PORT=8080 \
  -e HTTPS=false \
  --name quietlink \
  percyc/quietlink:v1.0.0
```

#### Multi-architecture Deployment (Supports AMD64 + ARM64)

```bash
# Use buildx to build (first-time setup required)
docker buildx create --use

# Automatically build and push multi-architecture
docker buildx build --platform linux/amd64,linux/arm64 \
  -t percyc/quietlink:v1.0.0 \
  -t percyc/quietlink:latest \
  --push .

# Or pull and use directly
docker run -d -p 8080:8080 \
  -e PORT=8080 \
  -e HTTPS=false \
  --name quietlink \
  percyc/quietlink:latest
```

#### Use Docker Compose

```bash
# Copy provided docker-compose.yml
docker-compose up -d

# Or customize configuration
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  quietlink:
    image: percyc/quietlink:latest
    container_name: quietlink
    ports:
      - "8443:8443"
    environment:
      - PORT=8443
      - HTTPS=true
    restart: unless-stopped
EOF

docker-compose up -d
```

### Method 3: Local Development

```bash
# Clone repository
git clone https://github.com/percyc/quietlink.git
cd quietlink

# Sync dependencies with uv
uv sync

# Start development server (recommended HTTPS mode)
./start.sh 8443 https
# Or HTTP mode (requires additional HTTPS proxy)
./start.sh 8080
```

---

## Command Line Arguments

```bash
quietlink [options]

Options:
  -h, --help       Show help information
  --port, -p PORT   Server port (default: 8080)
  --https           Enable HTTPS mode (auto-generate self-signed certificate)

Examples:
  quietlink                    Start on default port 8080
  quietlink --port 9000        Start on port 9000
  quietlink --https             Enable HTTPS mode
```

---

### Important Note

Modern browsers (Chrome, Edge, Firefox, etc.) require **HTTPS environment to use WebRTC functionality** due to security policies. If you use HTTP deployment, you will not be able to establish audio/video connections without setting up an additional HTTPS proxy. We recommend using HTTPS mode directly to avoid unnecessary configuration.

## Cloud Deployment

The project supports Render deployment.

### Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Select Python environment, dependencies will be auto-detected
4. After deployment, you'll get a `https://<app-name>.onrender.com` address

**Note**: This project is designed for LAN use. When deployed to public networks, WebRTC P2P connections require additional STUN/TURN server support. Public deployment is for demonstration purposes only; for best performance, use in LAN environment.

## System Requirements

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) (modern Python package manager)

## Usage

### Host (Sharing Side)

1. Open browser and visit `https://<server-ip>:8443/host.html`
2. Check "Share System Audio" (optional, disabled by default)
3. Click "Start Screen Sharing" button
4. Select screen or window to share
5. System generates a 6-digit room code (e.g., 123456)
6. Share the room code with viewers
7. Click "Approve" to authorize when receiving join requests

### Client (Viewing Side)

1. Open browser and visit `https://<server-ip>:8443/client.html`
2. Enter room code (e.g., 123456)
3. Click "Join"
4. Wait for host approval
5. After connection, click "Enable Audio" to play audio (if host shared audio)
6. Supports fullscreen viewing

### Important Reminder

Modern browsers (Chrome, Edge, Firefox, etc.) require **HTTPS environment to use WebRTC functionality** due to security policies. If you use HTTP deployment, you will not be able to establish audio/video connections without setting up an additional HTTPS proxy. We recommend using HTTPS mode directly to avoid unnecessary configuration.

## Audio Features

### Host Side
- Audio transmission is disabled by default to protect privacy
- Check "Share System Audio" to enable audio transmission
- Chrome/Edge support system audio capture
- Firefox only supports microphone (not recommended)

### Client Side
- Muted by default, need to manually click "Enable Audio"
- Can click mute/unmute button to control audio anytime
- Audio controls remain available in fullscreen mode

### Notes
- Audio transmission increases network bandwidth usage
- Browser will request audio permissions on first use
- System audio capture requires explicit user authorization

## Network Requirements

**Must be within the same LAN** (same network segment, e.g., `192.168.1.x`) for normal connection.

WebRTC can establish direct connections via local IP within the same network segment without STUN/TURN servers.

## Port Configuration

| Port | Usage | Description |
|------|-------|-------------|
| 8080 | HTTP/WebSocket | Signaling service and page service (requires additional HTTPS proxy) |
| 8443 | HTTPS | Secure connection (recommended, required by modern browsers) |

## Troubleshooting

### WebRTC Connection Failed / Black Screen

1. **First confirm you're using HTTPS**: Modern browsers require HTTPS for WebRTC functionality
2. If using HTTP, switch to HTTPS mode: `./start.sh 8443 https`
3. Check browser console for HTTPS or WebRTC related errors
4. Enter `about:webrtc` in Firefox address bar for detailed logs
5. Confirm both ends are on the same network segment

### HTTP vs HTTPS Explanation

- **HTTP**: Only suitable for development debugging, requires additional HTTPS proxy to work
- **HTTPS**: Required by modern browsers, auto-generates self-signed certificates
- If you see "getUserMedia is not allowed in insecure contexts" error, you need HTTPS

### No Audio

1. **Host side**: Confirm "Share System Audio" is checked
2. **Client side**: Click "Enable Audio" button to unmute
3. Check if browser granted audio playback permission
4. Confirm using Chrome/Edge (supports system audio)
5. Check browser console for `[Audio] Audio track received` logs

### Audio Capture Failed

1. Check if browser supports system audio (Chrome/Edge)
2. Confirm audio capture permission is granted
3. Try refreshing page to reconnect
4. Audio capture failure doesn't affect video sharing

### Client Cannot Access

1. Confirm firewall allows port 8080:
   ```bash
   # Linux (iptables)
   sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
   ```

2. Check SELinux/AppArmor settings

### Fullscreen Button Not Visible

1. Refresh page to reload
2. Check if browser supports fullscreen API
3. Try clicking video area to trigger fullscreen

## Project Structure

```
.
├── quietlink/              # Python package
│   ├── __init__.py       # Package entry
│   ├── server.py         # FastAPI application
│   ├── cli.py            # Command line tool
│   └── static/           # Static files
│       ├── index.html      # Homepage
│       ├── host.html       # Host page
│       └── client.html     # Client page
├── pyproject.toml          # Python dependencies configuration
├── Dockerfile             # Docker build file
├── docker-compose.yml      # Docker compose file
├── start.sh              # Development startup script
├── LICENSE               # MIT License
├── README.md             # Project documentation
├── README_EN.md          # English documentation
└── tests/                # Test directory
```

## Tech Stack

- **Backend**: Python 3.14+ + FastAPI + WebSocket
- **Frontend**: Vanilla JavaScript + WebRTC API
- **Dependency Management**: uv (modern Python package manager)
- **Audio Codec**: Opus (WebRTC default)
- **Deployment**: PyPI, Docker, local development
- **HTTPS**: Self-signed certificates auto-generated, required by modern browsers

## Security Notes

- Audio is disabled by default to protect user privacy
- Room codes are randomly generated to prevent brute force
- Host manually approves client join requests
- Designed for intranet use, no need to expose to public internet
- Auto-generated HTTPS certificates meet modern browser security requirements
- If public deployment is needed, configure strong password and valid HTTPS certificates

## Browser Compatibility

| Feature | Chrome/Edge | Firefox | Safari |
|---------|-------------|---------|--------|
| Video Sharing | ✅ | ✅ | ✅ |
| System Audio | ✅ | ❌ | ⚠️ Limited |
| Microphone Audio | ✅ | ✅ | ✅ |
| Fullscreen Playback | ✅ | ✅ | ✅ |
| Mobile | ✅ | ✅ | ✅ |
| HTTPS Requirement | ✅ Required | ✅ Required | ✅ Required |

### Important Notes
- All modern browsers require **HTTPS environment** to use WebRTC functionality
- HTTP is only suitable for development debugging; production environments must use HTTPS
- Self-signed certificates require manual trust in browsers (usually shows "Your connection is not private" warning)

## License

MIT License

---

## Related Links

- **PyPI**: https://pypi.org/project/quietlink/
- **Docker Hub**: https://hub.docker.com/r/percyc/quietlink
- **GitHub**: https://github.com/percyc/quietlink
- **Demo**: https://quietlink.onrender.com/

---

## Changelog

### v1.0.0 (2025-02-10)

- 🎉 First release
- ✅ PyPI installation support
- ✅ Docker deployment support (AMD64 + ARM64)
- ✅ Command line tool support
- ✅ Optimized project structure
- ✅ Complete documentation and examples

---

## Contributing

Issues and Pull Requests are welcome!
