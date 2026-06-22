<p align="center">
  <img src="docs/assets/colink-logo.svg" alt="CoLink Logo" width="120" />
</p>
<p align="center">
  <p align="center">CoLink • Verbinde alle deine Geräte und arbeite nahtlos zusammen.</p>
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="#funktionen">Funktionen</a> •
  <a href="#schnellstart">Schnellstart</a> •
  <a href="#architektur">Architektur</a> •
  <a href="#entwicklung">Entwicklung</a>
</p>

---

CoLink ist ein zuverlässiges plattformübergreifendes Werkzeug zur Gerätevernetzung. Kopiere auf dem Smartphone und füge auf dem Desktop ein; übertrage Dateien zwischen Laptop und Tablet. Es funktioniert nahtlos, egal ob deine Geräte im selben LAN oder über das Internet verbunden sind.

## Funktionen

- **Zwischenablage-Synchronisierung** — Auf einem Gerät kopieren, auf einem anderen einfügen. Unterstützt Klartext, Rich Text und Bilder.
- **Dateiübertragung** — Dateien zwischen Geräten senden. Direkte LAN-Übertragungen haben keine Größenbeschränkung; Cloud-Relay unterstützt bis zu 10 MB.
- **Textnachrichten** — Notizen und Textausschnitte sofort zwischen Geräten senden.
- **CastBoard** — Verwandle ein anderes Gerät in eine Live-Statusanzeige für deinen Computer. Titelinformationen, Albumcover und synchronisierte Liedtexte werden in Echtzeit übertragen, mit Unterstützung für NetEase Cloud Music, QQ Music, Sogou Music und Spotify. Außerdem synchronisiert es CPU-, Arbeitsspeicher-, Netzwerk- und weitere Auslastungswerte deines Computers. Weitere Funktionen sind geplant.
- **Direkte LAN-Verbindung** — Geräte im selben Netzwerk finden sich automatisch per mDNS und verbinden sich direkt, vollständig ohne Cloud.

| Plattformunterstützung | App | Status |
|------|------|------|
| Windows  | colink-desktop | ✅ Verfügbar |
| macOS    | colink-desktop | 🚧 Bald verfügbar |
| Linux    | colink-desktop | 🚧 Bald verfügbar |
| Android  | colink-android | ✅ Verfügbar |
| iOS      | colink-ios     | 🚧 Geplant |

## Vorschau

| Geräteliste | Nachrichtenliste | Nachrichtenseite |
|:---:|:---:|:---:|
| <img src="docs/assets/Screenshot_2026-06-16-01-37-11-165_com.colink.android.debug.jpg" alt="Geräteliste" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-16-481_com.colink.android.debug.jpg" alt="Nachrichtenliste" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-35-883_com.colink.android.debug-edit.jpg" alt="Nachrichtenseite" width="250" /> |

### CastBoard Demo

https://www.youtube.com/watch?v=w7pMdKMIfjg

## Schnellstart

### 1. Client installieren

| Plattform | Download |
|----------|----------|
| Windows | [Aktuelles Release](https://github.com/CoLinkDev/colink-desktop/releases/latest) |
| Android | [Aktuelles Release](https://github.com/CoLinkDev/colink-android/releases/latest) |

### 2. Verbinden

1. Öffne den Client und registriere ein Konto.
2. Kopple Geräte im selben LAN über den sechsstelligen Kopplungscode oder verbinde sie remote über das Server-Relay.
3. Starte die Zwischenablage-Synchronisierung, sende Dateien oder streame CastBoard.

### Self-Hosting (optional)

Du kannst den CoLink-Server mit Docker selbst hosten. Die Einrichtung ist unter [colink-server](https://github.com/CoLinkDev/colink-server) beschrieben.

## Architektur

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
│ Win/Mac/Linux │      │ Android        │       │ Kontoverwaltung │
└───────┬───────┘      └───────┬────────┘       └─────────────────┘
        │                      │
        │  LAN (mDNS + WS)     │
        └──────────────────────┘
```

| Kommunikationsweg | Transport | Zweck |
|------|----------|------|
| Client ↔ Server | HTTPS + WSS | Authentifizierung, Geräteverwaltung, Cloud-Relay |
| Client ↔ Client (LAN) | mDNS + WebSocket | Direktes P2P im selben Netzwerk |
| Frontend ↔ Server | HTTPS | Kontoverwaltung |

## Sicherheit

- Jedes Gerät besitzt ein eigenes Ed25519-Schlüsselpaar als nicht fälschbare kryptografische Identität mit Unterstützung für Online-Rotation.
- LAN-Verbindungen bauen gegenseitiges Vertrauen über einen vierstufigen beidseitigen Handshake auf. Die Erstkopplung nutzt einen aus SHA-256 abgeleiteten sechsstelligen Kopplungscode gegen MITM-Angriffe.
- LAN-Nachrichten sind Ende-zu-Ende-verschlüsselt: X25519-ECDH-Schlüsselaustausch, aus HKDF-SHA256 abgeleitete Sitzungsschlüssel und AES-256-GCM/ChaCha20-Poly1305 AEAD.
- JWT Access Tokens sind 15 Minuten gültig. Refresh Tokens werden nach einmaliger Nutzung sofort rotiert, alte Tokens werden zur Replay-Erkennung widerrufen markiert.
- Der Server speichert keine Nachrichten, Dateien oder Zwischenablageinhalte dauerhaft, sondern nur Konto- und Geräte-Metadaten.

## Entwicklung

Dieses Projekt verwendet eine Multi-Repository-Struktur. Jede Komponente wird eigenständig gepflegt:

| Repository | Technologie | Beschreibung |
|------|--------|------|
| [colink-server](https://github.com/CoLinkDev/colink-server) | Go, Gin, GORM, PostgreSQL | Backend-API-Server und WebSocket-Relay |
| [colink-desktop](https://github.com/CoLinkDev/colink-desktop) | Tauri 2.x (Rust + React/TS) | Desktop-Client für Windows, macOS und Linux |
| [colink-android](https://github.com/CoLinkDev/colink-android) | Kotlin, Jetpack Compose | Android-Client |
| [colink-frontend](https://github.com/CoLinkDev/colink-frontend) | Vue 3, TypeScript | Web-Frontend für Konto- und Sitzungsverwaltung |
| [CoLinkProtocol](https://github.com/CoLinkDev/CoLinkProtocol) | Markdown | Protokollspezifikationen und API-Dokumentation |

Klone das Haupt-Repository und alle Unter-Repositories in dasselbe übergeordnete Verzeichnis:

```bash
git clone https://github.com/CoLinkDev/CoLink.git
cd CoLink
git clone https://github.com/CoLinkDev/colink-server.git
git clone https://github.com/CoLinkDev/colink-desktop.git
git clone https://github.com/CoLinkDev/colink-android.git
git clone https://github.com/CoLinkDev/colink-frontend.git
git clone https://github.com/CoLinkDev/CoLinkProtocol.git
```

### Bauen und Ausführen

Jedes Unterprojekt hat eigene Einrichtungsanweisungen. Siehe die jeweilige README:

- **Server** — `colink-server/README.md`
- **Desktop** — `colink-desktop/README.md`
- **Android** — `colink-android/README.md`
- **Frontend** — `colink-frontend/README.md`
