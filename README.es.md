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

CoLink es una herramienta multiplataforma para conectar dispositivos que reúne la sincronización diaria, el acceso remoto y el control de dispositivos en una sola conexión. Tanto si los dispositivos están en la misma LAN como si se conectan a través de internet, pueden colaborar de forma segura.

## Funciones

- **Sincronización del portapapeles** — Copia en un dispositivo y pega en otro. Admite texto sin formato, texto enriquecido e imágenes.
- **Transferencia de archivos** — Envía archivos entre dispositivos. Las transferencias directas por LAN no tienen límite de tamaño; el relé en la nube admite hasta 10 MB.
- **Mensajes de texto** — Envía notas y fragmentos de texto entre dispositivos al instante.
- **Acceso remoto a archivos** — Explora el sistema de archivos de un dispositivo remoto y transfiere archivos entre dispositivos conectados.
- **Terminal remoto y control de dispositivos** — Abre un terminal interactivo en un ordenador conectado desde el teléfono; según la compatibilidad del dispositivo remoto, controla el estado de energía, la reproducción multimedia y el volumen del sistema.
- **Cámara remota** — Visualiza vídeo en directo de las cámaras de los dispositivos conectados.
- **CastBoard** — Convierte otro dispositivo en una pantalla de estado en tiempo real: muestra la reproducción actual, la carátula y letras sincronizadas (NetEase Cloud Music, QQ Music, Sogou Music y Spotify), y sincroniza CPU, memoria, red y otras métricas del sistema del ordenador.
- **Conexión directa por LAN** — Los dispositivos de la misma red se descubren automáticamente mediante mDNS y se conectan directamente, sin pasar por la nube.

Las funciones de acceso remoto y control dependen de la versión del cliente, las capacidades de la plataforma y los permisos concedidos en ambos dispositivos.

| Plataforma compatible | Aplicación | Estado |
|------|------|------|
| Windows  | colink-desktop | ✅ Disponible |
| macOS    | colink-desktop | 🚧 Próximamente |
| Linux    | colink-desktop | ✅ Disponible |
| Android  | colink-android | ✅ Disponible |
| iOS      | colink-ios     | 🚧 Planificado |

## Vista previa de la interfaz

| Lista de dispositivos | Lista de mensajes | Página de mensajes |
|:---:|:---:|:---:|
| <img src="docs/assets/Screenshot_2026-06-16-01-37-11-165_com.colink.android.debug.jpg" alt="Lista de dispositivos" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-16-481_com.colink.android.debug.jpg" alt="Lista de mensajes" width="250" /> | <img src="docs/assets/Screenshot_2026-06-16-01-37-35-883_com.colink.android.debug-edit.jpg" alt="Página de mensajes" width="250" /> |

### CastBoard Demo

https://www.youtube.com/watch?v=w7pMdKMIfjg

<table>
  <tr>
    <td>Letras sincronizadas</td>
    <td><img src="docs/assets/Screenshot_20260719-172822561.jpg" alt="Letras sincronizadas de CastBoard" width="640" /></td>
  </tr>
  <tr>
    <td>Reproducción actual</td>
    <td><img src="docs/assets/Screenshot_20260719-172830971.jpg" alt="Reproducción actual de CastBoard" width="640" /></td>
  </tr>
  <tr>
    <td>Métricas del sistema</td>
    <td><img src="docs/assets/Screenshot_20260719-172840770.jpg" alt="Métricas del sistema de CastBoard" width="640" /></td>
  </tr>
</table>

## Inicio rápido

### 1. Instalar un cliente

| Plataforma | Descarga |
|----------|----------|
| Windows | [Última versión](https://github.com/CoLinkDev/colink-desktop/releases/latest) |
| Linux | [Última versión](https://github.com/CoLinkDev/colink-desktop/releases/latest) |
| Android | [Última versión](https://github.com/CoLinkDev/colink-android/releases/latest) |

### 2. Conectar

1. Abre el cliente y registra una cuenta.
2. Empareja dispositivos en la misma LAN con el código de 6 dígitos, o conéctalos de forma remota mediante el relé del servidor.
3. Empieza a sincronizar el portapapeles, enviar archivos y mensajes, o usa el acceso remoto, el control de dispositivos y CastBoard.

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
| [CoLinkProtocol](https://github.com/CoLinkDev/CoLinkProtocol) | Markdown | Especificaciones del protocolo y documentación de API (documentación alojada: [CoLink Protocol](https://colinkdev.github.io/CoLinkProtocol/)) |

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
