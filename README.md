# Venezuela Resiste 🇻🇪

Directorio bilingüe (ES/EN) de recursos verificados para ayudar a Venezuela desde Madrid tras el terremoto del 24 de junio de 2026.

🌐 **[venezuelaresiste.netlify.app](https://venezuelaresiste.netlify.app)**
📢 **Canal de alertas: [t.me/VenezuelaAvisos](https://t.me/VenezuelaAvisos)**

---

## Qué incluye

- 🗺️ Mapa interactivo con +38 puntos de recogida en la Comunidad de Madrid
- 🔎 Plataformas verificadas para buscar personas desaparecidas
- 💳 Bizum y transferencias bancarias verificadas (Cruz Roja, WCK, Meals4Hope, Save the Children, Cáritas)
- 💚 Directorio de ONGs con canales de donación seguros
- 📡 Datos sísmicos en tiempo real vía USGS API
- 🤖 Bot de Telegram con alertas automáticas de réplicas
- 📬 Formulario para reportar nuevos puntos de recogida
- 🛡️ Guía anti-estafas

---

## Estructura

```
index.html          → Web completa (un solo archivo, sin dependencias)
bot/
  bot.py            → Bot de Telegram · alertas de réplicas vía USGS
  requirements.txt
  railway.json      → Config de despliegue en Railway
  .env.example      → Variables de entorno necesarias
```

---

## Despliegue

### Web → Netlify

1. Conecta este repositorio en [netlify.com](https://netlify.com)
2. Branch: `main` · Publish directory: `.`
3. Cada `git push` actualiza la web automáticamente

### Bot → Railway

1. Ve a [railway.app](https://railway.app) → New Project → Deploy from GitHub
2. Root Directory: `bot`
3. Añade las variables de entorno:

| Variable | Descripción | Ejemplo |
|---|---|---|
| `TELEGRAM_TOKEN` | Token del bot (de @BotFather) | `123456:ABC...` |
| `TELEGRAM_CHAT` | ID del canal | `-1004427169066` |
| `MIN_MAG` | Magnitud mínima para alertar | `4.5` |

---

## Contribuir

¿Conoces un punto de recogida que no está en el mapa? Usa el formulario en la web o abre un Issue en este repositorio.

---

## Fuentes de datos

- Actividad sísmica: [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/fdsnws/event/1/)
- Puntos de recogida: comunidad, medios locales y verificación manual
- Organizaciones: Cruz Roja, MSF, UNICEF, GlobalGiving, WCK, Aldeas Infantiles, We Love Foundation

---

*Esta web no recauda donaciones. Es un directorio de recursos verificados mantenido por voluntarios.*
