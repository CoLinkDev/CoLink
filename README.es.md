<p align="center">
  <img src="docs/assets/colink-logo.svg" alt="CoLink Logo" width="120" />
</p>
<p align="center">
  <p align="center">CoLink • Conecta todos tus dispositivos para colaborar sin interrupciones.</p>
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="#funciones">Funciones</a> •
  <a href="#inicio-rápido">Inicio rápido</a> •
  <a href="#arquitectura">Arquitectura</a> •
  <a href="#desarrollo">Desarrollo</a>
</p>

---

CoLink es una herramienta estable y multiplataforma para conectar dispositivos. Copia en el teléfono y pega en el escritorio; transfiere archivos entre el portátil y la tableta. Funciona sin interrupciones tanto si los dispositivos están en la misma LAN como si se conectan a través de internet.

## Funciones

- **Sincronización del portapapeles** — Copia en un dispositivo y pega en otro. Admite texto sin formato, texto enriquecido e imágenes.
- **Transferencia de archivos** — Envía archivos entre dispositivos. Las transferencias directas por LAN no tienen límite de tamaño; el relé en la nube admite hasta 10 MB.
- **Mensajes de texto** — Envía notas y fragmentos de texto entre dispositivos al instante.
- **CastBoard** — Convierte otro dispositivo en una pantalla de estado en tiempo real para tu ordenador. Envía información de la pista, carátulas y letras sincronizadas en tiempo real, con soporte para NetEase Cloud Music, QQ Music, Sogou Music y Spotify. También sincroniza el uso de CPU, memoria, red y otros recursos del ordenador. Se añadirán más funciones.
- **Conexión directa por LAN** — Los dispositivos de la misma red se descubren automáticamente mediante mDNS y se conectan directamente, sin pasar por la nube.

| Plataforma compatible | Aplicación | Estado |
|------|------|------|
| Windows  | colink-desktop | ✅ Disponible |
| macOS    | colink-desktop | 🚧 Próximamente |
| Linux    | colink-desktop | 🚧 Próximamente |
| Android  | colink-android | ✅ Disponible |
| iOS      | colink-ios     | 🚧 Planificado |

## Vista previa

| Lista de dispositivos | Lista de mensajes | Página de mensajes |
|:---:|:---:|:---:|
| <img src="docs/assets/Screenshot_2026-06-16-01-37-11-165_com.colink.android.debug.jpg" alt="Lista de dispositivos" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-16-481_com.colink.android.debug.jpg" alt="Lista de mensajes" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-35-883_com.colink.android.debug-edit.jpg" alt="Página de mensajes" width="250" /> |

### CastBoard Demo

https://www.youtube.com/watch?v=w7pMdKMIfjg

## Inicio rápido

### 1. Instalar un cliente

| Plataforma | Descarga |
|----------|----------|
| Windows | [Última versión](https://github.com/CoLinkDev/colink-desktop/releases/latest) |
| Android | [Última versión](https://github.com/CoLinkDev/colink-android/releases/latest) |

### 2. Conectar

1. Abre el cliente y registra una cuenta.
2. Empareja dispositivos en la misma LAN con el código de 6 dígitos, o conéctalos de forma remota mediante el relé del servidor.
3. Empieza a sincronizar el portapapeles, enviar archivos o transmitir CastBoard.

### Autoalojamiento (opcional)

Puedes autoalojar el servidor de CoLink con Docker. Consulta [colink-server](https://github.com/CoLinkDev/colink-server) para ver las instrucciones de configuración.

## Arquitectura

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
│ Win/Mac/Linux │      │ Android        │       │ Gestión cuenta  │
└───────┬───────┘      └───────┬────────┘       └─────────────────┘
        │                      │
        │  LAN (mDNS + WS)     │
        └──────────────────────┘
```

| Ruta de comunicación | Transporte | Uso |
|------|----------|------|
| Cliente ↔ Servidor | HTTPS + WSS | Autenticación, gestión de dispositivos, relé en la nube |
| Cliente ↔ Cliente (LAN) | mDNS + WebSocket | P2P directo en la misma red |
| Frontend ↔ Servidor | HTTPS | Gestión de cuentas |

## Seguridad

- Cada dispositivo tiene su propio par de claves Ed25519 como identidad criptográfica no falsificable, con soporte para rotación en línea.
- Las conexiones LAN establecen confianza mutua mediante un protocolo de enlace bidireccional de cuatro pasos. El primer emparejamiento usa un código de 6 dígitos derivado con SHA-256 para evitar ataques MITM.
- Los mensajes LAN están cifrados de extremo a extremo: acuerdo de claves X25519 ECDH, claves de sesión derivadas con HKDF-SHA256 y AEAD AES-256-GCM/ChaCha20-Poly1305.
- Los JWT Access Token son válidos durante 15 minutos. Los Refresh Token se rotan inmediatamente tras un único uso, y los tokens antiguos se marcan como revocados para detectar repetición.
- El servidor no persiste mensajes, archivos ni contenido del portapapeles. Solo almacena metadatos de cuentas y dispositivos.

## Desarrollo

Este proyecto usa una estructura de múltiples repositorios. Cada componente se mantiene de forma independiente:

| Repositorio | Tecnología | Descripción |
|------|--------|------|
| [colink-server](https://github.com/CoLinkDev/colink-server) | Go, Gin, GORM, PostgreSQL | Servidor API backend y relé WebSocket |
| [colink-desktop](https://github.com/CoLinkDev/colink-desktop) | Tauri 2.x (Rust + React/TS) | Cliente de escritorio para Windows, macOS y Linux |
| [colink-android](https://github.com/CoLinkDev/colink-android) | Kotlin, Jetpack Compose | Cliente Android |
| [colink-frontend](https://github.com/CoLinkDev/colink-frontend) | Vue 3, TypeScript | Frontend web para gestión de cuentas y sesiones |
| [CoLinkProtocol](https://github.com/CoLinkDev/CoLinkProtocol) | Markdown | Especificaciones del protocolo y documentación de API |

Clona el repositorio raíz y todos los subrepositorios en el mismo directorio padre:

```bash
git clone https://github.com/CoLinkDev/CoLink.git
cd CoLink
git clone https://github.com/CoLinkDev/colink-server.git
git clone https://github.com/CoLinkDev/colink-desktop.git
git clone https://github.com/CoLinkDev/colink-android.git
git clone https://github.com/CoLinkDev/colink-frontend.git
git clone https://github.com/CoLinkDev/CoLinkProtocol.git
```

### Compilar y ejecutar

Cada subproyecto tiene sus propias instrucciones de configuración. Consulta el README correspondiente:

- **Servidor** — `colink-server/README.md`
- **Escritorio** — `colink-desktop/README.md`
- **Android** — `colink-android/README.md`
- **Frontend** — `colink-frontend/README.md`
