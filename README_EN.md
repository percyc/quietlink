# QuietLink - WebRTC Local Area Network Screen Sharing

A WebRTC-based pure LAN screen sharing system with audio/video transmission support, no internet connection required.

[中文](README.md) | ## Features

- 📺 **Screen Sharing**: Host can share entire screen or single window
- 🔊 **Audio Transmission**: Supports system audio sharing (Chrome/Edge), optional enable
- 👁️ **Real-time Viewing**: Clients can watch shared content in real-time
- 🔒 **Room Isolation**: 6-digit room code ensures privacy
- ✅ **Authorization Mechanism**: Host manually approves client join requests
- 📴 **Pure Intranet Operation**: No STUN/TURN servers needed, no internet required
- 📱 **Mobile Support**: Supports fullscreen viewing on phones, responsive design
- 🎨 **Beautiful UI**: Modern gradient design, excellent user experience

## Quick Start

```bash
./start.sh [port] [https]
```

Parameters:
- `port`: Server port, default 8080
- `https`: Optional, enable HTTPS (auto-generate self-signed certificate)

Examples:
```bash
# HTTP mode
./start.sh

# HTTPS mode
./start.sh 8443 https
```

## Online Demo

Visit [https://quietlink.onrender.com/](https://quietlink.onrender.com/) to try the online demo.

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
- [uv](https://github.com/astral-sh/uv) (auto-installed)

## Usage

### Host (Sharing Side)

1. Open browser and visit `http://<server-ip>:8080/host.html`
2. Check "Share System Audio" (optional, disabled by default)
3. Click "Start Screen Sharing" button
4. Select screen or window to share
5. System generates a 6-digit room code (e.g., 123456)
6. Share the room code with viewers
7. Click "Approve" to authorize when receiving join requests

### Client (Viewing Side)

1. Open browser and visit `http://<server-ip>:8080/client.html`
2. Enter room code (e.g., 123456)
3. Click "Join"
4. Wait for host approval
5. After connection, click "Enable Audio" to play audio (if host shared audio)
6. Supports fullscreen viewing

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
| 8080 | HTTP/WebSocket | Signaling service and page service |
| 8443 | HTTPS | Secure connection (optional) |

## Troubleshooting

### Connected but black screen

1. Check browser console for ICE errors
2. Enter `about:webrtc` in Firefox address bar for detailed logs
3. Confirm both ends are on the same network segment

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
├── main.py              # FastAPI signaling server
├── start.sh             # Startup script
├── pyproject.toml       # Python dependencies
├── certs/               # SSL certificate directory (gitignore)
│   ├── cert.pem
│   └── key.pem
└── static/
    ├── host.html        # Host page
    └── client.html      # Client page
```

## Tech Stack

- **Backend**: Python + FastAPI + WebSocket
- **Frontend**: Vanilla JavaScript + WebRTC API
- **Dependency Management**: uv
- **Audio Codec**: Opus (WebRTC default)

## Security Notes

- Audio is disabled by default to protect user privacy
- Room codes are randomly generated to prevent brute force
- Host manually approves client join requests
- Designed for intranet use, no need to expose to public internet
- If public deployment is needed, configure strong password and HTTPS

## Browser Compatibility

| Feature | Chrome/Edge | Firefox | Safari |
|---------|-------------|---------|--------|
| Video Sharing | ✅ | ✅ | ✅ |
| System Audio | ✅ | ❌ | ⚠️ Limited |
| Microphone Audio | ✅ | ✅ | ✅ |
| Fullscreen Playback | ✅ | ✅ | ✅ |
| Mobile | ✅ | ✅ | ✅ |

## License

MIT License