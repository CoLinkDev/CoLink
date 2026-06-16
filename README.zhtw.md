<p align="center">
  <img src="docs/assets/colink-logo.svg" alt="CoLink Logo" width="120" />
</p>
<p align="center">
  <p align="center">CoLink • 連接你的所有裝置，無縫協作。</p>
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="#功能">功能</a> •
  <a href="#架構">架構</a> •
  <a href="#開發">快速開始</a>
</p>

---

CoLink 是一款穩定的跨平台裝置互聯工具。在手機上複製，在桌面上貼上；在筆記型電腦和平板之間傳輸檔案。無論裝置處於同一區域網路，還是透過網際網路連線，都能無縫運作。

## 功能

- **剪貼簿同步** — 在一台裝置上複製，在另一台裝置上貼上。支援純文字、富文字和圖片。
- **檔案傳輸** — 在裝置之間傳送檔案。區域網路直連傳輸沒有大小限制；雲端中繼最大支援 10 MB。
- **文字訊息** — 在裝置之間即時傳送筆記和文字片段。
- **CastBoard** — 將另一台裝置變成即時的電腦狀態顯示器。即時推送曲目資訊、專輯封面和同步歌詞（支援網易雲音樂、QQ 音樂、Spotify），後續將增加更多功能。
- **區域網路直連** — 同一網路下的裝置透過 mDNS 自動發現並直連，完全繞過雲端。

| 平台支援 | 應用程式 | 狀態 |
|------|------|------|
| Windows  | colink-desktop | ✅ 可用 |
| macOS    | colink-desktop | 🚧 即將可用 |
| Linux    | colink-desktop | 🚧 即將可用 |
| Android  | colink-android | ✅ 可用 |
| iOS      | colink-ios     | 🚧 規劃中 |

## 功能預覽

| 裝置列表 | 訊息列表 | 訊息頁面 |
|:---:|:---:|:---:|
| <img src="docs/assets/Screenshot_2026-06-16-01-37-11-165_com.colink.android.debug.jpg" alt="裝置列表" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-16-481_com.colink.android.debug.jpg" alt="訊息列表" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-35-883_com.colink.android.debug-edit.jpg" alt="訊息頁面" width="250" /> |

### CastBoard Demo

https://www.youtube.com/watch?v=w7pMdKMIfjg

## 架構

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
│ Win/Mac/Linux │      │ Android        │       │ 帳戶管理         │
└───────┬───────┘      └───────┬────────┘       └─────────────────┘
        │                      │
        │  LAN (mDNS + WS)     │
        └──────────────────────┘
```

| 通訊路徑 | 傳輸協定 | 用途 |
|------|----------|------|
| 用戶端 ↔ 伺服器 | HTTPS + WSS | 認證、裝置管理、雲端中繼 |
| 用戶端 ↔ 用戶端（區域網路） | mDNS + WebSocket | 同一網路下的直連 P2P |
| 前端 ↔ 伺服器 | HTTPS | 帳戶管理 |

## 安全性

- 每台裝置持有獨立的 Ed25519 金鑰對，作為不可偽造的密碼學身份，支援線上輪換
- 區域網路連線透過四步雙向握手建立互信，首次配對使用 SHA-256 派生的 6 位配對碼防止 MITM
- 區域網路訊息端到端加密：X25519 ECDH 金鑰協商 + HKDF-SHA256 派生工作階段金鑰 + AES-256-GCM/ChaCha20-Poly1305 AEAD
- JWT Access Token 有效期 15 分鐘；Refresh Token 單次使用後立即輪換，舊權杖標記撤銷以偵測重放
- 伺服器不持久化任何訊息、檔案或剪貼簿內容，僅儲存帳戶與裝置中繼資料

## 開發

本專案採用多儲存庫結構，各元件獨立維護：

| 儲存庫 | 技術棧 | 描述 |
|------|--------|------|
| [colink-server](https://github.com/CoLinkDev/colink-server) | Go, Gin, GORM, PostgreSQL | 後端 API 伺服器與 WebSocket 中繼 |
| [colink-desktop](https://github.com/CoLinkDev/colink-desktop) | Tauri 2.x (Rust + React/TS) | 桌面用戶端（Windows、macOS、Linux） |
| [colink-android](https://github.com/CoLinkDev/colink-android) | Kotlin, Jetpack Compose | Android 用戶端 |
| [colink-frontend](https://github.com/CoLinkDev/colink-frontend) | Vue 3, TypeScript | 帳戶與工作階段管理 Web 前端 |
| [CoLinkProtocol](https://github.com/CoLinkDev/CoLinkProtocol) | Markdown | 協定規範與 API 文件 |

將主儲存庫和所有子儲存庫複製到同一父目錄下：

```bash
git clone https://github.com/CoLinkDev/CoLink.git
cd CoLink
git clone https://github.com/CoLinkDev/colink-server.git
git clone https://github.com/CoLinkDev/colink-desktop.git
git clone https://github.com/CoLinkDev/colink-android.git
git clone https://github.com/CoLinkDev/colink-frontend.git
git clone https://github.com/CoLinkDev/CoLinkProtocol.git
```

### 建置與執行

各子專案有各自的設定說明，請參考對應的 README：

- **伺服器** — `colink-server/README.md`
- **桌面端** — `colink-desktop/README.md`
- **Android** — `colink-android/README.md`
- **前端** — `colink-frontend/README.md`
