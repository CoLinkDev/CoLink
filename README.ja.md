<p align="center">
  <img src="docs/assets/colink-logo.svg" alt="CoLink Logo" width="120" />
</p>
<p align="center">
  <p align="center">CoLink • すべてのデバイスをつなぎ、シームレスに連携します。</p>
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="#機能">機能</a> •
  <a href="#クイックスタート">クイックスタート</a> •
  <a href="#アーキテクチャ">アーキテクチャ</a> •
  <a href="#開発">開発</a>
</p>

---

CoLink は、安定したクロスプラットフォームのデバイス連携ツールです。スマートフォンでコピーしてデスクトップに貼り付けたり、ノート PC とタブレットの間でファイルを転送したりできます。デバイスが同じ LAN にある場合でも、インターネット経由で接続している場合でも、シームレスに動作します。

## 機能

- **クリップボード同期** — あるデバイスでコピーし、別のデバイスで貼り付けます。プレーンテキスト、リッチテキスト、画像に対応しています。
- **ファイル転送** — デバイス間でファイルを送信します。LAN 直結転送にはサイズ制限がなく、クラウドリレーは最大 10 MB まで対応します。
- **テキストメッセージ** — メモやテキスト断片をデバイス間で即座に送信できます。
- **CastBoard** — 別のデバイスをコンピューターのリアルタイム状態表示画面にします。トラック情報、アルバムアート、同期歌詞をリアルタイムに送信し、NetEase Cloud Music、QQ Music、Spotify に対応しています。今後さらに機能を追加予定です。
- **LAN 直結** — 同じネットワーク上のデバイスは mDNS で自動検出され、クラウドを経由せず直接接続します。

| 対応プラットフォーム | アプリ | 状態 |
|------|------|------|
| Windows  | colink-desktop | ✅ 利用可能 |
| macOS    | colink-desktop | 🚧 近日対応 |
| Linux    | colink-desktop | 🚧 近日対応 |
| Android  | colink-android | ✅ 利用可能 |
| iOS      | colink-ios     | 🚧 計画中 |

## プレビュー

| デバイス一覧 | メッセージ一覧 | メッセージ画面 |
|:---:|:---:|:---:|
| <img src="docs/assets/Screenshot_2026-06-16-01-37-11-165_com.colink.android.debug.jpg" alt="デバイス一覧" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-16-481_com.colink.android.debug.jpg" alt="メッセージ一覧" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-35-883_com.colink.android.debug-edit.jpg" alt="メッセージ画面" width="250" /> |

### CastBoard Demo

https://www.youtube.com/watch?v=w7pMdKMIfjg

## クイックスタート

### 1. クライアントをインストール

| プラットフォーム | ダウンロード |
|----------|----------|
| Windows | [最新リリース](https://github.com/CoLinkDev/colink-desktop/releases/latest) |
| Android | [最新リリース](https://github.com/CoLinkDev/colink-android/releases/latest) |

### 2. 接続

1. クライアントを開いてアカウントを登録します。
2. 同じ LAN 上では 6 桁のペアリングコードでデバイスをペアリングし、リモートではサーバーリレー経由で接続します。
3. クリップボード同期、ファイル送信、CastBoard のストリーミングを開始します。

### セルフホスティング（任意）

Docker を使って CoLink サーバーをセルフホストできます。セットアップ手順は [colink-server](https://github.com/CoLinkDev/colink-server) を参照してください。

## アーキテクチャ

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
│ Win/Mac/Linux │      │ Android        │       │ アカウント管理   │
└───────┬───────┘      └───────┬────────┘       └─────────────────┘
        │                      │
        │  LAN (mDNS + WS)     │
        └──────────────────────┘
```

| 通信経路 | 転送方式 | 用途 |
|------|----------|------|
| クライアント ↔ サーバー | HTTPS + WSS | 認証、デバイス管理、クラウドリレー |
| クライアント ↔ クライアント（LAN） | mDNS + WebSocket | 同一ネットワーク内の直接 P2P |
| フロントエンド ↔ サーバー | HTTPS | アカウント管理 |

## セキュリティ

- 各デバイスは偽造できない暗号学的 ID として独立した Ed25519 鍵ペアを持ち、オンラインでのローテーションに対応しています。
- LAN 接続は 4 ステップの相互ハンドシェイクで信頼を確立します。初回ペアリングでは MITM 攻撃を防ぐため、SHA-256 から派生した 6 桁のペアリングコードを使用します。
- LAN メッセージはエンドツーエンドで暗号化されます。X25519 ECDH 鍵合意、HKDF-SHA256 派生セッション鍵、AES-256-GCM/ChaCha20-Poly1305 AEAD を使用します。
- JWT Access Token の有効期間は 15 分です。Refresh Token は 1 回の使用後すぐにローテーションされ、古いトークンはリプレイ検出のため失効済みとして記録されます。
- サーバーはメッセージ、ファイル、クリップボード内容を永続化せず、アカウントとデバイスのメタデータのみを保存します。

## 開発

このプロジェクトはマルチリポジトリ構成です。各コンポーネントは独立して管理されています。

| リポジトリ | 技術スタック | 説明 |
|------|--------|------|
| [colink-server](https://github.com/CoLinkDev/colink-server) | Go, Gin, GORM, PostgreSQL | バックエンド API サーバーと WebSocket リレー |
| [colink-desktop](https://github.com/CoLinkDev/colink-desktop) | Tauri 2.x (Rust + React/TS) | Windows、macOS、Linux 向けデスクトップクライアント |
| [colink-android](https://github.com/CoLinkDev/colink-android) | Kotlin, Jetpack Compose | Android クライアント |
| [colink-frontend](https://github.com/CoLinkDev/colink-frontend) | Vue 3, TypeScript | アカウントとセッション管理の Web フロントエンド |
| [CoLinkProtocol](https://github.com/CoLinkDev/CoLinkProtocol) | Markdown | プロトコル仕様と API ドキュメント |

ルートリポジトリとすべてのサブリポジトリを同じ親ディレクトリにクローンします。

```bash
git clone https://github.com/CoLinkDev/CoLink.git
cd CoLink
git clone https://github.com/CoLinkDev/colink-server.git
git clone https://github.com/CoLinkDev/colink-desktop.git
git clone https://github.com/CoLinkDev/colink-android.git
git clone https://github.com/CoLinkDev/colink-frontend.git
git clone https://github.com/CoLinkDev/CoLinkProtocol.git
```

### ビルドと実行

各サブプロジェクトにはそれぞれ設定手順があります。対応する README を参照してください。

- **サーバー** — `colink-server/README.md`
- **デスクトップ** — `colink-desktop/README.md`
- **Android** — `colink-android/README.md`
- **フロントエンド** — `colink-frontend/README.md`
