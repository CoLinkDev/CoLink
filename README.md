<p align="center">
  <img src="docs/assets/colink-logo.svg" alt="CoLink Logo" width="120" />
</p>
<p align="center">
  <p align="center">CoLink • Connect all your devices for seamless collaboration.</p>
</p>

<p align="center">
  <a href="README.zhcn.md">简体中文</a> •
  <a href="README.ja.md">日本語</a> •
  <a href="README.ko.md">한국어</a> •
  <a href="README.zhtw.md">繁體中文</a> •
  <a href="README.de.md">Deutsch</a> •
  <a href="README.es.md">Español</a> •
  <a href="README.ru.md">Русский</a>
</p>
<p align="center">
  <a href="#features">Features</a> •
  <a href="#quickstart">Quick Start</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#development">Development</a>
</p>

---

CoLink is a reliable cross-platform device connectivity tool. Copy on your phone and paste on your desktop; transfer files between your laptop and tablet. It works seamlessly whether your devices are on the same LAN or connected over the internet.

## Features

- **Clipboard Sync** — Copy on one device and paste on another. Supports plain text, rich text, and images.
- **File Transfer** — Send files between devices. Direct LAN transfers have no size limit; cloud relay supports up to 10 MB.
- **Text Messages** — Send notes and text snippets between devices instantly.
- **CastBoard** — Turn another device into a live status display for your computer. It pushes track information, album art, and synced lyrics in real time, with support for NetEase Cloud Music, QQ Music, Sogou Music, and Spotify. It also syncs your computer's CPU, memory, network, and other usage metrics. More capabilities are planned.
- **Direct LAN Connection** — Devices on the same network discover each other automatically through mDNS and connect directly without going through the cloud.

| Platform Support | App | Status |
|------|------|------|
| Windows  | colink-desktop | ✅ Available |
| macOS    | colink-desktop | 🚧 Coming soon |
| Linux    | colink-desktop | 🚧 Coming soon |
| Android  | colink-android | ✅ Available |
| iOS      | colink-ios     | 🚧 Planned |

## Preview

| Device List | Message List | Message Page |
|:---:|:---:|:---:|
| <img src="docs/assets/Screenshot_2026-06-16-01-37-11-165_com.colink.android.debug.jpg" alt="Device list" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-16-481_com.colink.android.debug.jpg" alt="Message list" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-35-883_com.colink.android.debug-edit.jpg" alt="Message page" width="250" /> |

### CastBoard Demo

https://www.youtube.com/watch?v=w7pMdKMIfjg

## Quick Start

### 1. Install a Client

| Platform | Download |
|----------|----------|
| Windows | [Latest Release](https://github.com/CoLinkDev/colink-desktop/releases/latest) |
| Android | [Latest Release](https://github.com/CoLinkDev/colink-android/releases/latest) |

### 2. Connect

1. Open the client and sign up.
2. Pair devices on the same LAN via the 6-digit pairing code, or connect remotely through the server relay.
3. Start syncing clipboard, sending files, or streaming CastBoard.

### Self-hosting (Optional)

You can self-host the CoLink server using Docker. See [colink-server](https://github.com/CoLinkDev/colink-server) for setup instructions.

## Architecture

```
                        ┌─────────────────────┐
                        │   colink-server     │
                        │   (Go / Gin)        │
                        │   REST + WS Relay   │
                        └────────┬────────────┘
                                 │
               HTTPS / WSS       │       HTTPS / WSS
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐      ┌────────────────┐       ┌─────────────────┐
│ colink-desktop│      │ colink-android │       │ colink-frontend │
│ Tauri 2.x     │      │ Kotlin/Compose │       │ Vue 3 Web App   │
│ Win/Mac/Linux │      │ Android        │       │ Account Mgmt    │
└───────┬───────┘      └───────┬────────┘       └─────────────────┘
        │                      │
        │  LAN (mDNS + WS)     │
        └──────────────────────┘
```

| Communication Path | Transport | Purpose |
|------|----------|------|
| Client ↔ Server | HTTPS + WSS | Authentication, device management, cloud relay |
| Client ↔ Client (LAN) | mDNS + WebSocket | Direct P2P on the same network |
| Frontend ↔ Server | HTTPS | Account management |

## Security

- Each device has its own Ed25519 key pair as a non-forgeable cryptographic identity, with online rotation support.
- LAN connections establish mutual trust through a four-step mutual handshake. First-time pairing uses a SHA-256-derived 6-digit pairing code to prevent MITM attacks.
- LAN messages are end-to-end encrypted with X25519 ECDH key agreement, HKDF-SHA256 session keys, and AES-256-GCM/ChaCha20-Poly1305 AEAD.
- JWT access tokens are valid for 15 minutes. Refresh tokens are rotated immediately after single use, and old tokens are marked revoked to detect replay.
- The server does not persist messages, files, or clipboard contents. It only stores account and device metadata.

## Development

This project uses a multi-repository structure. Each component is maintained independently:

| Repository | Tech Stack | Description |
|------|--------|------|
| [colink-server](https://github.com/CoLinkDev/colink-server) | Go, Gin, GORM, PostgreSQL | Backend API server and WebSocket relay |
| [colink-desktop](https://github.com/CoLinkDev/colink-desktop) | Tauri 2.x (Rust + React/TS) | Desktop client for Windows, macOS, and Linux |
| [colink-android](https://github.com/CoLinkDev/colink-android) | Kotlin, Jetpack Compose | Android client |
| [colink-frontend](https://github.com/CoLinkDev/colink-frontend) | Vue 3, TypeScript | Account and session management web frontend |
| [CoLinkProtocol](https://github.com/CoLinkDev/CoLinkProtocol) | Markdown | Protocol specifications and API documentation |

Clone the root repository and all sub-repositories into the same parent directory:

```bash
git clone https://github.com/CoLinkDev/CoLink.git
cd CoLink
git clone https://github.com/CoLinkDev/colink-server.git
git clone https://github.com/CoLinkDev/colink-desktop.git
git clone https://github.com/CoLinkDev/colink-android.git
git clone https://github.com/CoLinkDev/colink-frontend.git
git clone https://github.com/CoLinkDev/CoLinkProtocol.git
```

### Build and Run

Each sub-project has its own setup instructions. See the corresponding README:

- **Server** — `colink-server/README.md`
- **Desktop** — `colink-desktop/README.md`
- **Android** — `colink-android/README.md`
- **Frontend** — `colink-frontend/README.md`
