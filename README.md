<p align="center">
  <h1 align="center">CoLink</h1>
  <p align="center">Connect your devices, seamlessly.</p>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#supported-platforms">Platforms</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#security">Security</a>
</p>

---

CoLink is a cross-platform tool that connects all your devices together. Copy text on your phone, paste it on your desktop. Send files from your laptop to your tablet. It just works — whether your devices are on the same Wi-Fi or across the internet.

## Features

**Clipboard Sync** — Copy on one device, paste on another. Supports text, rich text, and images.

**File Transfer** — Send files between your devices with drag-and-drop. LAN transfers have no size limit; cloud relay supports up to 10 MB.

**Text Messaging** — Send quick notes and text snippets between devices instantly.

## Supported Platforms

| Platform | Status |
|----------|--------|
| Windows  | ✅ Available |
| macOS    | ✅ Available |
| Linux    | ✅ Available |
| Android  | ✅ Available |
| iOS      | 🚧 Planned  |

## How It Works

CoLink automatically picks the best path for your data:

- **Same network** — Data flows directly between devices over LAN. Fast, private, no size limits.
- **Different networks** — Data is relayed through the CoLink server. Nothing is stored on the server.

## Security

- Per-device Ed25519 key pairs for authentication
- Mutual cryptographic handshake on LAN connections
- No message or file persistence on the server
- JWT-based session management with short-lived tokens

---

## For Developers

This repository serves as the entry point for the CoLink project. The actual source code lives in separate repositories:

| Repository | Description |
|-----------|-------------|
| [colink-server](https://github.com/CoLinkDev/colink-server) | Backend service (Go, Gin, PostgreSQL) |
| [colink-frontend](https://github.com/CoLinkDev/colink-frontend) | Web app for account management (Vue 3, TypeScript) |
| [ColinkAPI](https://github.com/CoLinkDev/ColinkAPI) | Protocol & API documentation |

### Setting Up the Development Environment

1. Clone this repository and all project repos into the same directory:

```bash
git clone https://github.com/CoLinkDev/CoLink.git
cd CoLink
git clone https://github.com/CoLinkDev/colink-server.git
git clone https://github.com/CoLinkDev/colink-frontend.git
git clone https://github.com/CoLinkDev/ColinkAPI.git
```

2. Each sub-project has its own README with setup instructions. Refer to them for building and running individually.

3. Shared configuration files (like `AGENTS.md`) in this root directory apply to all sub-projects during development.

### Project Structure

```
CoLink/
├── AGENTS.md             # Shared AI agent instructions
├── README.md             # This file
├── .gitignore
├── colink-server/        # ← separate git repo
├── colink-frontend/      # ← separate git repo
└── ColinkAPI/            # ← separate git repo
```

## License

Proprietary. All rights reserved.
