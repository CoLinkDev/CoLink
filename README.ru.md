<p align="center">
  <img src="docs/assets/colink-logo.svg" alt="CoLink Logo" width="120" />
</p>
<p align="center">
  <p align="center">CoLink • Подключайте все свои устройства и работайте без разрывов.</p>
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="#возможности">Возможности</a> •
  <a href="#архитектура">Архитектура</a> •
  <a href="#разработка">Быстрый старт</a>
</p>

---

CoLink — стабильный кроссплатформенный инструмент для связи устройств. Копируйте на телефоне и вставляйте на рабочем столе; передавайте файлы между ноутбуком и планшетом. Он работает без разрывов как в одной LAN, так и через интернет.

## Возможности

- **Синхронизация буфера обмена** — Копируйте на одном устройстве и вставляйте на другом. Поддерживаются обычный текст, форматированный текст и изображения.
- **Передача файлов** — Отправляйте файлы между устройствами. Прямая передача по LAN не имеет ограничения размера; облачный ретранслятор поддерживает до 10 MB.
- **Текстовые сообщения** — Мгновенно отправляйте заметки и фрагменты текста между устройствами.
- **CastBoard** — Превратите другое устройство в экран состояния компьютера в реальном времени. Он передает информацию о треке, обложку альбома и синхронизированные тексты песен в реальном времени, поддерживая NetEase Cloud Music, QQ Music и Spotify. В дальнейшем появятся новые функции.
- **Прямое подключение по LAN** — Устройства в одной сети автоматически обнаруживают друг друга через mDNS и подключаются напрямую, полностью минуя облако.

| Поддержка платформ | Приложение | Статус |
|------|------|------|
| Windows  | colink-desktop | ✅ Доступно |
| macOS    | colink-desktop | 🚧 Скоро |
| Linux    | colink-desktop | 🚧 Скоро |
| Android  | colink-android | ✅ Доступно |
| iOS      | colink-ios     | 🚧 В планах |

## Предпросмотр

| Список устройств | Список сообщений | Страница сообщения |
|:---:|:---:|:---:|
| <img src="docs/assets/Screenshot_2026-06-16-01-37-11-165_com.colink.android.debug.jpg" alt="Список устройств" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-16-481_com.colink.android.debug.jpg" alt="Список сообщений" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-35-883_com.colink.android.debug-edit.jpg" alt="Страница сообщения" width="250" /> |

### CastBoard Demo

https://www.youtube.com/watch?v=w7pMdKMIfjg

## Архитектура

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
│ Win/Mac/Linux │      │ Android        │       │ Аккаунты        │
└───────┬───────┘      └───────┬────────┘       └─────────────────┘
        │                      │
        │  LAN (mDNS + WS)     │
        └──────────────────────┘
```

| Канал связи | Транспорт | Назначение |
|------|----------|------|
| Клиент ↔ Сервер | HTTPS + WSS | Аутентификация, управление устройствами, облачный ретранслятор |
| Клиент ↔ Клиент (LAN) | mDNS + WebSocket | Прямой P2P в одной сети |
| Фронтенд ↔ Сервер | HTTPS | Управление аккаунтом |

## Безопасность

- Каждое устройство имеет собственную пару ключей Ed25519 как неподделываемую криптографическую идентичность, с поддержкой онлайн-ротации.
- LAN-подключения устанавливают взаимное доверие через четырехшаговое взаимное рукопожатие. При первом сопряжении используется 6-значный код, производный от SHA-256, для защиты от MITM.
- LAN-сообщения шифруются сквозным шифрованием: согласование ключей X25519 ECDH, сеансовые ключи HKDF-SHA256 и AEAD AES-256-GCM/ChaCha20-Poly1305.
- JWT Access Token действителен 15 минут. Refresh Token ротируется сразу после однократного использования, а старые токены помечаются отозванными для обнаружения повторного воспроизведения.
- Сервер не сохраняет сообщения, файлы или содержимое буфера обмена. Он хранит только метаданные аккаунтов и устройств.

## Разработка

Проект использует структуру из нескольких репозиториев. Каждый компонент поддерживается независимо:

| Репозиторий | Технологии | Описание |
|------|--------|------|
| [colink-server](https://github.com/CoLinkDev/colink-server) | Go, Gin, GORM, PostgreSQL | Backend API-сервер и WebSocket-ретранслятор |
| [colink-desktop](https://github.com/CoLinkDev/colink-desktop) | Tauri 2.x (Rust + React/TS) | Настольный клиент для Windows, macOS и Linux |
| [colink-android](https://github.com/CoLinkDev/colink-android) | Kotlin, Jetpack Compose | Android-клиент |
| [colink-frontend](https://github.com/CoLinkDev/colink-frontend) | Vue 3, TypeScript | Web-фронтенд для управления аккаунтами и сеансами |
| [CoLinkProtocol](https://github.com/CoLinkDev/CoLinkProtocol) | Markdown | Спецификации протокола и документация API |

Клонируйте корневой репозиторий и все подрепозитории в один родительский каталог:

```bash
git clone https://github.com/CoLinkDev/CoLink.git
cd CoLink
git clone https://github.com/CoLinkDev/colink-server.git
git clone https://github.com/CoLinkDev/colink-desktop.git
git clone https://github.com/CoLinkDev/colink-android.git
git clone https://github.com/CoLinkDev/colink-frontend.git
git clone https://github.com/CoLinkDev/CoLinkProtocol.git
```

### Сборка и запуск

У каждого подпроекта есть собственные инструкции по настройке. См. соответствующий README:

- **Сервер** — `colink-server/README.md`
- **Настольный клиент** — `colink-desktop/README.md`
- **Android** — `colink-android/README.md`
- **Фронтенд** — `colink-frontend/README.md`
