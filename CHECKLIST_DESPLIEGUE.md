# ✅ Checklist de Despliegue en Render

Usa esta checklist para asegurarte de que todo esté configurado correctamente.

## 📋 Antes de Desplegar

- [ ] Tienes una cuenta en Render
- [ ] Tu código está en un repositorio de GitHub
- [ ] Tienes una API Key de Gemini
- [ ] Has leído la guía completa en `DESPLIEGUE_RENDER.md`

## 🗄️ Base de Datos PostgreSQL (Neon)

- [ ] Tienes una base de datos PostgreSQL en Neon
- [ ] Copiaste la **Connection String** de Neon
- [ ] Agregaste `?sslmode=require` al final de la URL (si no lo tenía)
- [ ] Verificaste que tu IP esté permitida en Neon (o habilitaste "Allow all IPs")
- [ ] La base de datos está activa en Neon

## 🔧 Configuración del Web Service

### Información Básica
- [ ] Nombre del servicio configurado
- [ ] Región seleccionada (misma que la BD)
- [ ] Repositorio de GitHub conectado
- [ ] Rama correcta seleccionada (main/master)

### Build & Deploy
- [ ] **Root Directory**: `Backend` (si tu código está en carpeta Backend) o vacío (si está en raíz)
- [ ] **Build Command**: `pip install -r requirements.txt`
- [ ] **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Variables de Entorno
- [ ] `DATABASE_URL` = Connection String de Neon (con `?sslmode=require` al final)
- [ ] `SECRET_KEY` = Clave secreta aleatoria (puedes usar `openssl rand -hex 32`)
- [ ] `ALGORITHM` = `HS256`
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`
- [ ] `GEMINI_API_KEY` = Tu API key de Gemini
- [ ] `FRONTEND_URL` = URL de tu frontend (o `http://localhost:3000` temporalmente)

## ✅ Verificación Post-Despliegue

- [ ] El servicio muestra estado "Live" (verde)
- [ ] Puedes acceder a `https://tu-servicio.onrender.com/`
- [ ] El endpoint `/health` funciona y muestra conexiones OK
- [ ] La documentación en `/docs` es accesible
- [ ] Los logs muestran "✓ Base de datos: Conexión exitosa"
- [ ] Los logs muestran "✓ Gemini API: Conexión exitosa"

## 🔗 Integración con Frontend

- [ ] Actualizaste `API_BASE_URL` en `Frontend/app.js` con la URL de Render
- [ ] Configuraste `FRONTEND_URL` en Render con la URL de GitHub Pages
- [ ] Probaste el registro de usuario desde el frontend
- [ ] Probaste el login desde el frontend
- [ ] Probaste generar un artículo desde el frontend

## 🐛 Si Algo Sale Mal

- [ ] Revisaste los logs del servicio en Render
- [ ] Verificaste todas las variables de entorno
- [ ] Probaste el endpoint `/health` para diagnóstico
- [ ] Verificaste que la base de datos esté accesible
- [ ] Confirmaste que la API key de Gemini sea válida

## 📝 Notas Importantes

- ⚠️ En el plan Free, Render "duerme" los servicios después de 15 min de inactividad
- ⚠️ La primera petición después de dormir puede tardar 30-60 segundos
- ✅ Usa Internal Database URL (más rápida y segura)
- ✅ Base de datos y Web Service en la misma región = mejor rendimiento

---

**¿Todo marcado?** ¡Tu backend debería estar funcionando perfectamente! 🎉

