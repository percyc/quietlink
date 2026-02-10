#!/usr/bin/env python3
"""QuietLink CLI - 现代化命令行接口"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def generate_certs():
    """生成 SSL 证书"""
    cert_dir = Path("quietlink/certs")
    cert_dir.mkdir(parents=True, exist_ok=True)

    cert_file = cert_dir / "cert.pem"
    key_file = cert_dir / "key.pem"

    if not cert_file.exists() or not key_file.exists():
        print("📜 生成自签名证书...")
        subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-keyout",
                str(key_file),
                "-out",
                str(cert_file),
                "-days",
                "365",
                "-nodes",
                "-subj",
                "/CN=localhost",
            ],
            check=True,
        )


def run_server(port, https):
    """启动服务器"""
    cmd = ["uvicorn", "quietlink.server:app", "--host", "0.0.0.0", "--port", str(port)]

    if https:
        generate_certs()
        cmd.extend(
            [
                "--ssl-certfile",
                "quietlink/certs/cert.pem",
                "--ssl-keyfile",
                "quietlink/certs/key.pem",
            ]
        )

    protocol = "https" if https else "http"

    print(f"\n✅ 准备启动服务器...")
    print(f"📡 服务器地址: {protocol}://localhost:{port}")
    print(f"🔗 访问链接：")
    print(f"   共享端: {protocol}://localhost:{port}/host.html")
    print(f"   观看端: {protocol}://localhost:{port}/client.html")

    try:
        hostname = (
            subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
        )
        print(f"\n💡 局域网访问（替换为你的IP）:")
        print(f"   {protocol}://{hostname}:{port}/host.html\n")
    except:
        pass

    subprocess.run(cmd)


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description="QuietLink - WebRTC LAN Screen Sharing System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  quietlink                    在默认端口 8080 启动
  quietlink --port 9000        在端口 9000 启动
  quietlink --https             启用 HTTPS 模式
        """,
    )

    parser.add_argument(
        "--port", "-p", default="8080", type=int, help="服务器端口（默认: 8080）"
    )
    parser.add_argument(
        "--https", action="store_true", help="启用 HTTPS 模式（自动生成自签名证书）"
    )

    args = parser.parse_args()

    try:
        run_server(args.port, args.https)
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
