# 🚀 Guía de Despliegue en Render

Guía paso a paso para desplegar el backend de AI-Blog en Render.

## 📋 Requisitos Previos

1. ✅ Cuenta en [Render](https://render.com) (gratis)
2. ✅ Repositorio de GitHub con tu código
3. ✅ Base de datos PostgreSQL en [Neon](https://neon.tech) (gratis)
4. ✅ API Key de Gemini

## 📝 Paso 1: Obtener la Connection String de Neon

Si ya tienes tu base de datos en Neon:

1. Ve a tu [Neon Dashboard](https://console.neon.tech)
2. Selecciona tu proyecto
3. Ve a la sección **"Connection Details"** o **"Connection String"**
4. Copia la **Connection String** (debe verse así: `postgresql://user:password@host/database`)
5. **Importante**: Si la URL no incluye SSL, agrega `?sslmode=require` al final

### Ejemplo de Connection String de Neon:
```
postgresql://user:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### ⚠️ Notas sobre Neon:
- Neon requiere SSL por defecto, así que agrega `?sslmode=require` a tu URL
- Puedes usar la **Pooled connection** o la **Direct connection**
- La Pooled connection es mejor para aplicaciones web (tiene `-pooler` en el hostname)

## 🔧 Paso 2: Crear el Web Service

1. En Render Dashboard, click en **"New +"** > **"Web Service"**
2. Conecta tu repositorio de GitHub:
   - Si es la primera vez, autoriza Render para acceder a GitHub
   - Selecciona tu repositorio
   - Selecciona la rama (generalmente `main` o `master`)
3. Configura el servicio:

### Configuración Básica:
- **Name**: `ai-blog-backend` (o el nombre que prefieras)
- **Region**: La misma que elegiste para la base de datos
- **Branch**: `main` (o tu rama principal)
- **Root Directory**: `Backend` (si tu código está en una carpeta Backend)
- **Runtime**: `Python 3` (Render detectará la versión del archivo `runtime.txt`)
- **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### ⚠️ Importante:
- Si tu código está en la raíz del repositorio, deja **Root Directory** vacío
- Si está en una carpeta `Backend`, escribe `Backend` en **Root Directory**

## 🔐 Paso 3: Configurar Variables de Entorno

En la sección **"Environment"** del Web Service, agrega estas variables:

### Variables Requeridas:

1. **DATABASE_URL**
   - Valor: La **Connection String** que copiaste de Neon
   - **IMPORTANTE**: Agrega `?sslmode=require` al final si no lo tiene
   - Ejemplo: `postgresql://user:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require`
   - Puedes usar la **Pooled connection** (recomendada) o **Direct connection**

2. **SECRET_KEY**
   - Valor: Una clave secreta aleatoria
   - Genera una con: `openssl rand -hex 32`
   - O usa un generador online de secretos

3. **ALGORITHM**
   - Valor: `HS256`

4. **ACCESS_TOKEN_EXPIRE_MINUTES**
   - Valor: `30`

5. **GEMINI_API_KEY**
   - Valor: Tu API key de Google Gemini
   - Obtén una en: https://makersuite.google.com/app/apikey

6. **FRONTEND_URL**
   - Valor: La URL de tu frontend en GitHub Pages
   - Ejemplo: `https://tuusuario.github.io` o `https://tuusuario.github.io/ai-blog-frontend`
   - Si aún no lo tienes, puedes usar: `http://localhost:3000` temporalmente

### 📝 Ejemplo de Variables:

```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=tu-clave-secreta-super-larga-y-aleatoria-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GEMINI_API_KEY=AIzaSy...tu-api-key-aqui
FRONTEND_URL=https://tuusuario.github.io
```

## 🚀 Paso 4: Desplegar

1. Click en **"Create Web Service"**
2. Render comenzará a construir y desplegar tu aplicación
3. Puedes ver el progreso en los logs
4. El despliegue puede tardar 3-5 minutos

## ✅ Paso 5: Verificar el Despliegue

Una vez desplegado:

1. **Verifica que el servicio esté "Live"** (debe aparecer en verde)

2. **Prueba el endpoint de health:**
   ```
   https://tu-servicio.onrender.com/health
   ```
   Deberías ver el estado de las conexiones

3. **Prueba la documentación:**
   ```
   https://tu-servicio.onrender.com/docs
   ```

4. **Prueba el endpoint raíz:**
   ```
   https://tu-servicio.onrender.com/
   ```

## 🔍 Solución de Problemas

### Error: "Could not import module 'main'"
- Verifica que **Root Directory** esté configurado correctamente
- Si tu código está en `Backend/`, usa `Backend` como Root Directory
- Si está en la raíz, déjalo vacío

### Error: "Module not found"
- Verifica que `requirements.txt` tenga todas las dependencias
- Revisa los logs de build para ver qué módulo falta

### Error de conexión a la base de datos
- Verifica que `DATABASE_URL` sea correcta
- **Asegúrate de agregar `?sslmode=require` al final de la URL de Neon**
- Verifica que tu IP esté permitida en Neon (o habilita "Allow all IPs")
- Prueba con la **Pooled connection** si la Direct no funciona
- Verifica que la base de datos esté activa en Neon

### Error: "GEMINI_API_KEY no está configurada"
- Verifica que la variable de entorno esté escrita correctamente
- No debe tener espacios ni comillas extras
- Verifica que el valor sea tu API key real

### El servicio se detiene después de unos minutos
- En el plan Free, Render "duerme" los servicios después de 15 minutos de inactividad
- La primera petición puede tardar 30-60 segundos en "despertar" el servicio
- Considera usar el plan Starter ($7/mes) para evitar esto

## 📊 Monitoreo

- **Logs**: Ve a tu servicio > **"Logs"** para ver los logs en tiempo real
- **Metrics**: Ve a **"Metrics"** para ver CPU, memoria, etc.
- **Events**: Ve a **"Events"** para ver el historial de despliegues

## 🔄 Actualizar el Código

Cada vez que hagas push a tu repositorio:
1. Render detectará automáticamente los cambios
2. Iniciará un nuevo build
3. Desplegará la nueva versión
4. Puedes ver el progreso en los logs

## 💡 Tips

1. **SSL con Neon**: Siempre agrega `?sslmode=require` a tu DATABASE_URL de Neon
2. **Pooled Connection**: Usa la Pooled connection de Neon para mejor rendimiento
3. **IP Whitelist**: En Neon, verifica que tu IP esté permitida o habilita "Allow all IPs"
4. **Logs útiles**: Los logs muestran las validaciones de conexión al iniciar
5. **Health Check**: Usa `/health` para verificar que todo funcione
6. **CORS**: Asegúrate de configurar `FRONTEND_URL` correctamente

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs del servicio
2. Verifica todas las variables de entorno
3. Prueba el endpoint `/health` para diagnóstico
4. Consulta la [documentación de Render](https://render.com/docs)

¡Listo! Tu backend debería estar funcionando en Render 🎉

