<p align="center">
  <img src="docs/assets/colink-logo.svg" alt="CoLink Logo" width="120" />
</p>
<p align="center">
  <p align="center">CoLink • 모든 기기를 연결해 끊김 없이 협업합니다.</p>
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="#기능">기능</a> •
  <a href="#빠른-시작">빠른 시작</a> •
  <a href="#아키텍처">아키텍처</a> •
  <a href="#개발">개발</a>
</p>

---

CoLink는 안정적인 크로스 플랫폼 기기 연결 도구입니다. 휴대폰에서 복사하고 데스크톱에서 붙여넣거나, 노트북과 태블릿 사이에서 파일을 전송할 수 있습니다. 기기가 같은 LAN에 있든 인터넷을 통해 연결되어 있든 끊김 없이 동작합니다.

## 기능

- **클립보드 동기화** — 한 기기에서 복사하고 다른 기기에서 붙여넣습니다. 일반 텍스트, 리치 텍스트, 이미지를 지원합니다.
- **파일 전송** — 기기 사이에서 파일을 보냅니다. LAN 직접 전송에는 크기 제한이 없으며, 클라우드 릴레이는 최대 10 MB를 지원합니다.
- **텍스트 메시지** — 메모와 텍스트 조각을 기기 사이에서 즉시 보냅니다.
- **CastBoard** — 다른 기기를 컴퓨터의 실시간 상태 표시 화면으로 바꿉니다. 트랙 정보, 앨범 아트, 동기화 가사를 실시간으로 전송하며 NetEase Cloud Music, QQ Music, Spotify를 지원합니다. 더 많은 기능이 추가될 예정입니다.
- **LAN 직접 연결** — 같은 네트워크의 기기는 mDNS로 자동 발견되고 클라우드를 거치지 않고 직접 연결됩니다.

| 지원 플랫폼 | 앱 | 상태 |
|------|------|------|
| Windows  | colink-desktop | ✅ 사용 가능 |
| macOS    | colink-desktop | 🚧 곧 제공 |
| Linux    | colink-desktop | 🚧 곧 제공 |
| Android  | colink-android | ✅ 사용 가능 |
| iOS      | colink-ios     | 🚧 계획 중 |

## 미리 보기

| 기기 목록 | 메시지 목록 | 메시지 화면 |
|:---:|:---:|:---:|
| <img src="docs/assets/Screenshot_2026-06-16-01-37-11-165_com.colink.android.debug.jpg" alt="기기 목록" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-16-481_com.colink.android.debug.jpg" alt="메시지 목록" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-35-883_com.colink.android.debug-edit.jpg" alt="메시지 화면" width="250" /> |

### CastBoard Demo

https://www.youtube.com/watch?v=w7pMdKMIfjg

## 빠른 시작

### 1. 클라이언트 설치

| 플랫폼 | 다운로드 |
|----------|----------|
| Windows | [최신 릴리스](https://github.com/CoLinkDev/colink-desktop/releases/latest) |
| Android | [최신 릴리스](https://github.com/CoLinkDev/colink-android/releases/latest) |

### 2. 연결

1. 클라이언트를 열고 계정을 등록합니다.
2. 같은 LAN에서는 6자리 페어링 코드로 기기를 페어링하거나, 서버 릴레이를 통해 원격으로 연결합니다.
3. 클립보드 동기화, 파일 전송 또는 CastBoard 스트리밍을 시작합니다.

### 셀프 호스팅(선택 사항)

Docker로 CoLink 서버를 직접 호스팅할 수 있습니다. 설정 방법은 [colink-server](https://github.com/CoLinkDev/colink-server)를 참고하세요.

## 아키텍처

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
│ Win/Mac/Linux │      │ Android        │       │ 계정 관리        │
└───────┬───────┘      └───────┬────────┘       └─────────────────┘
        │                      │
        │  LAN (mDNS + WS)     │
        └──────────────────────┘
```

| 통신 경로 | 전송 방식 | 용도 |
|------|----------|------|
| 클라이언트 ↔ 서버 | HTTPS + WSS | 인증, 기기 관리, 클라우드 릴레이 |
| 클라이언트 ↔ 클라이언트(LAN) | mDNS + WebSocket | 같은 네트워크에서 직접 P2P |
| 프런트엔드 ↔ 서버 | HTTPS | 계정 관리 |

## 보안

- 각 기기는 위조할 수 없는 암호학적 신원으로 독립된 Ed25519 키 쌍을 보유하며, 온라인 회전을 지원합니다.
- LAN 연결은 4단계 양방향 핸드셰이크로 상호 신뢰를 설정합니다. 최초 페어링은 MITM을 방지하기 위해 SHA-256에서 파생한 6자리 페어링 코드를 사용합니다.
- LAN 메시지는 종단 간 암호화됩니다. X25519 ECDH 키 합의, HKDF-SHA256 파생 세션 키, AES-256-GCM/ChaCha20-Poly1305 AEAD를 사용합니다.
- JWT Access Token은 15분 동안 유효합니다. Refresh Token은 1회 사용 직후 회전되며, 이전 토큰은 재사용 공격 감지를 위해 폐기 표시됩니다.
- 서버는 메시지, 파일, 클립보드 내용을 영구 저장하지 않고 계정 및 기기 메타데이터만 저장합니다.

## 개발

이 프로젝트는 다중 저장소 구조를 사용합니다. 각 구성 요소는 독립적으로 유지 관리됩니다.

| 저장소 | 기술 스택 | 설명 |
|------|--------|------|
| [colink-server](https://github.com/CoLinkDev/colink-server) | Go, Gin, GORM, PostgreSQL | 백엔드 API 서버와 WebSocket 릴레이 |
| [colink-desktop](https://github.com/CoLinkDev/colink-desktop) | Tauri 2.x (Rust + React/TS) | Windows, macOS, Linux용 데스크톱 클라이언트 |
| [colink-android](https://github.com/CoLinkDev/colink-android) | Kotlin, Jetpack Compose | Android 클라이언트 |
| [colink-frontend](https://github.com/CoLinkDev/colink-frontend) | Vue 3, TypeScript | 계정 및 세션 관리를 위한 Web 프런트엔드 |
| [CoLinkProtocol](https://github.com/CoLinkDev/CoLinkProtocol) | Markdown | 프로토콜 사양과 API 문서 |

루트 저장소와 모든 하위 저장소를 같은 상위 디렉터리에 클론합니다.

```bash
git clone https://github.com/CoLinkDev/CoLink.git
cd CoLink
git clone https://github.com/CoLinkDev/colink-server.git
git clone https://github.com/CoLinkDev/colink-desktop.git
git clone https://github.com/CoLinkDev/colink-android.git
git clone https://github.com/CoLinkDev/colink-frontend.git
git clone https://github.com/CoLinkDev/CoLinkProtocol.git
```

### 빌드 및 실행

각 하위 프로젝트에는 자체 설정 안내가 있습니다. 해당 README를 참고하세요.

- **서버** — `colink-server/README.md`
- **데스크톱** — `colink-desktop/README.md`
- **Android** — `colink-android/README.md`
- **프런트엔드** — `colink-frontend/README.md`
