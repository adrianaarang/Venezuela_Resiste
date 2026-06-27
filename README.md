# Venezuela Resiste

Directorio bilingüe (ES/EN) de recursos verificados para venezolanos en el exterior tras el terremoto del 24 de junio de 2026. Incluye datos sísmicos en tiempo real desde USGS y un bot de Telegram para alertas de réplicas.

---

## 🌐 Web · Despliegue en 2 minutos

**Netlify Drop (más fácil):**
1. Ve a https://app.netlify.com/drop
2. Arrastra el archivo `index.html`
3. Listo — URL pública instantánea

**GitHub Pages:**
1. Crea un repo, sube `index.html` como `index.html`
2. Settings → Pages → Branch: main → / (root)
3. URL: `https://tuusuario.github.io/nombre-repo`

La web consulta USGS automáticamente cada 2 minutos desde el navegador del visitante. Sin servidor, sin base de datos.

---

## 🤖 Bot de Telegram · Despliegue

### 1. Crear el bot
1. Habla con @BotFather en Telegram → `/newbot`
2. Guarda el **token** que te da

### 2. Crear canal y obtener el Chat ID
1. Crea un canal público en Telegram (ej: @VenezuelaReplicas)
2. Añade tu bot como administrador
3. Envía un mensaje al canal
4. Ve a: `https://api.telegram.org/bot<TOKEN>/getUpdates`
5. Busca el campo `"id"` dentro de `"chat"` — ese es tu CHAT_ID

### 3. Desplegar en Railway (gratis)
1. Ve a https://railway.app → New Project → Deploy from GitHub
2. Sube la carpeta `bot/` o conecta tu repo
3. En Variables de entorno añade:
   - `TELEGRAM_TOKEN` = tu token
   - `TELEGRAM_CHAT`  = tu chat ID (ej: -1001234567890)
   - `MIN_MAG`        = 4.5 (opcional, es el default)
4. Railway detecta `railway.json` y arranca automáticamente

### Variables de entorno
| Variable | Descripción | Ejemplo |
|---|---|---|
| `TELEGRAM_TOKEN` | Token del bot de @BotFather | `123456:ABC-DEF...` |
| `TELEGRAM_CHAT` | ID del canal o grupo | `-1001234567890` |
| `MIN_MAG` | Magnitud mínima para avisar | `4.5` |

---

## 📡 Fuente de datos

Todos los datos sísmicos provienen de la **API pública del USGS**:
`https://earthquake.usgs.gov/fdsnws/event/1/`

Radio de búsqueda: 350 km desde 10.5°N, 68.0°W (centro de Venezuela).
