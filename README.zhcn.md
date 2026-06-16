<p align="center">
  <img src="docs/assets/colink-logo.svg" alt="CoLink Logo" width="120" />
</p>
<p align="center">
  <p align="center">CoLink • 连接你的所有设备，无缝协作。</p>
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="#功能">功能</a> •
  <a href="#架构">架构</a> •
  <a href="#开发">快速开始</a>
</p>

---

CoLink 是一款稳定的跨平台设备互联工具。在手机上复制，在桌面上粘贴；在笔记本和平板之间传输文件。无论设备处于同一局域网还是通过互联网连接，都能无缝工作。

## 功能

- **剪贴板同步** — 在一台设备上复制，在另一台设备上粘贴。支持纯文本、富文本和图片。
- **文件传输** — 在设备之间发送文件。局域网传输直连无大小限制；云端中继最大支持 10 MB。
- **文本消息** — 在设备之间即时发送笔记和文本片段。
- **CastBoard** — 将另一台设备变成实时的电脑状态显示屏。实时推送曲目信息、专辑封面和同步歌词（支持网易云音乐、QQ音乐、Spotify），后续将增加更多功能。
- **局域网直连** — 同一网络下的设备通过 mDNS 自动发现并直连，完全绕过云端。

| 平台支持 | 应用 | 状态 |
|------|------|------|
| Windows  | colink-desktop | ✅ 可用 |
| macOS    | colink-desktop | 🚧 即将可用 |
| Linux    | colink-desktop | 🚧 即将可用 |
| Android  | colink-android | ✅ 可用 |
| iOS      | colink-ios     | 🚧 计划中 |

## 功能预览

| 设备列表 | 消息列表 | 消息页面 |
|:---:|:---:|:---:|
| <img src="docs/assets/Screenshot_2026-06-16-01-37-11-165_com.colink.android.debug.jpg" alt="设备列表" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-16-481_com.colink.android.debug.jpg" alt="消息列表" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-35-883_com.colink.android.debug-edit.jpg" alt="消息页面" width="250" /> |

### CastBoard Demo

https://www.youtube.com/watch?v=w7pMdKMIfjg

## 架构

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
│ Win/Mac/Linux │      │ Android        │       │ 账户管理         │
└───────┬───────┘      └───────┬────────┘       └─────────────────┘
        │                      │
        │  LAN (mDNS + WS)     │
        └──────────────────────┘
```


| 通信路径 | 传输协议 | 用途 |
|------|----------|------|
| 客户端 ↔ 服务器 | HTTPS + WSS | 认证、设备管理、云端中继 |
| 客户端 ↔ 客户端（局域网） | mDNS + WebSocket | 同一网络下的直连 P2P |
| 前端 ↔ 服务器 | HTTPS | 账户管理 |

## 安全性

- 每台设备持有独立的 Ed25519 密钥对，作为不可伪造的密码学身份，支持在线轮换
- 局域网连接通过四步双向握手建立互信，首次配对使用 SHA-256 派生的 6 位配对码防止 MITM
- 局域网消息端到端加密：X25519 ECDH 密钥协商 + HKDF-SHA256 派生会话密钥 + AES-256-GCM/ChaCha20-Poly1305 AEAD
- JWT Access Token 有效期 15 分钟；Refresh Token 单次使用后立即轮换，旧令牌标记撤销以检测重放
- 服务端不持久化任何消息、文件或剪贴板内容，仅存储账户与设备元数据

## 开发

本项目采用多仓库结构，各组件独立维护：

| 仓库 | 技术栈 | 描述 |
|------|--------|------|
| [colink-server](https://github.com/CoLinkDev/colink-server) | Go, Gin, GORM, PostgreSQL | 后端 API 服务器与 WebSocket 中继 |
| [colink-desktop](https://github.com/CoLinkDev/colink-desktop) | Tauri 2.x (Rust + React/TS) | 桌面客户端（Windows、macOS、Linux） |
| [colink-android](https://github.com/CoLinkDev/colink-android) | Kotlin, Jetpack Compose | Android 客户端 |
| [colink-frontend](https://github.com/CoLinkDev/colink-frontend) | Vue 3, TypeScript | 账户与会话管理 Web 前端 |
| [CoLinkProtocol](https://github.com/CoLinkDev/CoLinkProtocol) | Markdown | 协议规范与 API 文档 |

将主仓库和所有子仓库克隆到同一父目录下：

```bash
git clone https://github.com/CoLinkDev/CoLink.git
cd CoLink
git clone https://github.com/CoLinkDev/colink-server.git
git clone https://github.com/CoLinkDev/colink-desktop.git
git clone https://github.com/CoLinkDev/colink-android.git
git clone https://github.com/CoLinkDev/colink-frontend.git
git clone https://github.com/CoLinkDev/CoLinkProtocol.git
```

### 构建与运行

各子项目有各自的配置说明，请参考对应的 README：

- **服务端** — `colink-server/README.md`
- **桌面端** — `colink-desktop/README.md`
- **Android** — `colink-android/README.md`
- **前端** — `colink-frontend/README.md`
